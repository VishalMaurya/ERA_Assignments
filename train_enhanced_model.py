#!/usr/bin/env python3
"""
Enhanced CIFAR_GAP_Net Training Script
=====================================

Training script for the budget-compliant enhanced CIFAR_GAP_Net model
with architectural improvements targeting 85-86% accuracy.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as T
import albumentations as A
from albumentations.pytorch import ToTensorV2
import numpy as np
import matplotlib.pyplot as plt
import time
import json
import os
from datetime import datetime
import argparse

# Import the enhanced model
from budget_compliant_enhanced_cifar_gap_net import (
    BudgetCompliantEnhancedCIFAR_GAP_Net,
    AlbumentationsTransform,
    CIFAR10_MEAN,
    CIFAR10_STD
)

class EnhancedCIFAR10Trainer:
    """Enhanced trainer for the budget-compliant enhanced CIFAR_GAP_Net"""
    
    def __init__(self, model, device, train_loader, val_loader, 
                 optimizer, scheduler, criterion, target_accuracy=85.0):
        self.model = model
        self.device = device
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = criterion
        self.target_accuracy = target_accuracy
        
        # Training history
        self.train_losses = []
        self.train_accuracies = []
        self.val_losses = []
        self.val_accuracies = []
        self.learning_rates = []
        self.best_accuracy = 0.0
        self.best_epoch = 0
        self.target_reached = False
        
        # CIFAR-10 class names
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                           'dog', 'frog', 'horse', 'ship', 'truck']
    
    def train_epoch(self, epoch):
        """Train for one epoch"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(self.train_loader):
            data, target = data.to(self.device), target.to(self.device)
            
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()
            
            running_loss += loss.item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
            
            # Print progress every 100 batches
            if batch_idx % 100 == 0:
                print(f'Epoch {epoch:3d} [{batch_idx:3d}/{len(self.train_loader):3d}] '
                      f'Loss: {loss.item():.4f} Acc: {100.*correct/total:.2f}%')
        
        epoch_loss = running_loss / len(self.train_loader)
        epoch_acc = 100. * correct / total
        
        return epoch_loss, epoch_acc
    
    def validate(self, epoch):
        """Validate the model"""
        self.model.eval()
        val_loss = 0
        correct = 0
        total = 0
        class_correct = [0] * 10
        class_total = [0] * 10
        
        with torch.no_grad():
            for data, target in self.val_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                val_loss += self.criterion(output, target).item()
                
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
                total += target.size(0)
                
                # Per-class accuracy
                for i in range(target.size(0)):
                    label = target[i]
                    class_correct[label] += (pred[i] == label).item()
                    class_total[label] += 1
        
        val_loss /= len(self.val_loader)
        val_acc = 100. * correct / total
        
        # Check if new best
        if val_acc > self.best_accuracy:
            self.best_accuracy = val_acc
            self.best_epoch = epoch
            self.save_checkpoint(epoch, val_acc, is_best=True)
            
            # Check if target reached
            if val_acc >= self.target_accuracy and not self.target_reached:
                self.target_reached = True
                print(f"\n🎉 TARGET ACHIEVED! 🎉")
                print(f"Reached {val_acc:.2f}% accuracy (target: {self.target_accuracy}%) at epoch {epoch}")
                print(f"Enhanced architecture improvements successful! 🚀\n")
        
        # Print per-class accuracies
        print(f"\nPer-class accuracies (Epoch {epoch}):")
        for i, class_name in enumerate(self.class_names):
            if class_total[i] > 0:
                class_acc = 100. * class_correct[i] / class_total[i]
                print(f"  {class_name:>10}: {class_acc:5.1f}%")
        
        return val_loss, val_acc
    
    def save_checkpoint(self, epoch, accuracy, is_best=False):
        """Save model checkpoint"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'accuracy': accuracy,
            'best_accuracy': self.best_accuracy,
            'model_info': self.model.get_model_info()
        }
        
        filename = f'enhanced_cifar_gap_net_epoch_{epoch}.pth'
        torch.save(checkpoint, filename)
        
        if is_best:
            torch.save(checkpoint, 'enhanced_cifar_gap_net_best.pth')
            print(f"💾 New best model saved: {accuracy:.2f}% (epoch {epoch})")
    
    def train(self, epochs):
        """Main training loop"""
        print(f"🚀 Starting Enhanced CIFAR_GAP_Net Training")
        print(f"Target: {self.target_accuracy}% accuracy")
        print(f"Model: {self.model.get_model_info()['total_parameters']:,} parameters")
        print("=" * 60)
        
        start_time = time.time()
        
        for epoch in range(1, epochs + 1):
            epoch_start = time.time()
            
            # Train
            train_loss, train_acc = self.train_epoch(epoch)
            
            # Validate
            val_loss, val_acc = self.validate(epoch)
            
            # Update scheduler
            self.scheduler.step()
            current_lr = self.optimizer.param_groups[0]['lr']
            
            # Store history
            self.train_losses.append(train_loss)
            self.train_accuracies.append(train_acc)
            self.val_losses.append(val_loss)
            self.val_accuracies.append(val_acc)
            self.learning_rates.append(current_lr)
            
            epoch_time = time.time() - epoch_start
            
            # Print epoch summary
            print(f"\nEpoch {epoch:3d}/{epochs} Summary:")
            print(f"  Train Loss: {train_loss:.4f} | Train Acc: {train_acc:6.2f}%")
            print(f"  Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:6.2f}%")
            print(f"  Best Acc:   {self.best_accuracy:6.2f}% (epoch {self.best_epoch})")
            print(f"  LR: {current_lr:.6f} | Time: {epoch_time:.1f}s")
            
            if self.target_reached:
                print(f"  🎯 Target {self.target_accuracy}% ACHIEVED! ✅")
            else:
                remaining = self.target_accuracy - val_acc
                print(f"  📈 Gap to target: {remaining:.2f}%")
            
            print("-" * 60)
        
        total_time = time.time() - start_time
        
        # Training summary
        print(f"\n🎉 Enhanced Training Complete!")
        print(f"Total time: {total_time/60:.1f} minutes")
        print(f"Best accuracy: {self.best_accuracy:.2f}% (epoch {self.best_epoch})")
        print(f"Target {self.target_accuracy}%: {'✅ ACHIEVED' if self.target_reached else '❌ Not reached'}")
        
        # Save final results
        self.save_results()
        self.plot_training_curves()
        
        return self.best_accuracy
    
    def save_results(self):
        """Save training results to JSON"""
        results = {
            'model_info': self.model.get_model_info(),
            'training_results': {
                'best_accuracy': self.best_accuracy,
                'best_epoch': self.best_epoch,
                'target_accuracy': self.target_accuracy,
                'target_reached': self.target_reached,
                'final_accuracy': self.val_accuracies[-1] if self.val_accuracies else 0,
                'total_epochs': len(self.val_accuracies)
            },
            'training_history': {
                'train_losses': self.train_losses,
                'train_accuracies': self.train_accuracies,
                'val_losses': self.val_losses,
                'val_accuracies': self.val_accuracies,
                'learning_rates': self.learning_rates
            }
        }
        
        filename = f'enhanced_training_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📊 Results saved to: {filename}")
    
    def plot_training_curves(self):
        """Plot training curves"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        epochs = range(1, len(self.train_losses) + 1)
        
        # Loss curves
        ax1.plot(epochs, self.train_losses, 'b-', label='Train Loss')
        ax1.plot(epochs, self.val_losses, 'r-', label='Val Loss')
        ax1.set_title('Enhanced Model - Loss Curves')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        ax1.grid(True)
        
        # Accuracy curves
        ax2.plot(epochs, self.train_accuracies, 'b-', label='Train Acc')
        ax2.plot(epochs, self.val_accuracies, 'r-', label='Val Acc')
        ax2.axhline(y=self.target_accuracy, color='g', linestyle='--', label=f'Target {self.target_accuracy}%')
        ax2.axhline(y=self.best_accuracy, color='orange', linestyle='--', label=f'Best {self.best_accuracy:.2f}%')
        ax2.set_title('Enhanced Model - Accuracy Curves')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy (%)')
        ax2.legend()
        ax2.grid(True)
        
        # Learning rate
        ax3.plot(epochs, self.learning_rates, 'g-')
        ax3.set_title('Learning Rate Schedule')
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('Learning Rate')
        ax3.grid(True)
        
        # Best accuracy progression
        best_so_far = []
        current_best = 0
        for acc in self.val_accuracies:
            if acc > current_best:
                current_best = acc
            best_so_far.append(current_best)
        
        ax4.plot(epochs, best_so_far, 'purple', linewidth=2)
        ax4.axhline(y=self.target_accuracy, color='g', linestyle='--', label=f'Target {self.target_accuracy}%')
        ax4.set_title('Best Accuracy Progression')
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Best Accuracy (%)')
        ax4.legend()
        ax4.grid(True)
        
        plt.tight_layout()
        filename = f'enhanced_training_curves_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"📈 Training curves saved to: {filename}")
        plt.show()

def create_enhanced_dataloaders(batch_size=128, num_workers=4):
    """Create CIFAR-10 data loaders with fixed augmentation"""
    
    # Fixed augmentation transforms (no warnings)
    train_transforms = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.Affine(scale=(0.85, 1.15), translate_percent=(-0.125, 0.125), 
                rotate=(-15, 15), p=0.5),  # Replaces ShiftScaleRotate
        A.CoarseDropout(max_holes=1, max_height=16, max_width=16, 
                       fill_value=tuple([int(x*255) for x in CIFAR10_MEAN]), p=0.5),
        A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=0.3),
        A.Normalize(mean=CIFAR10_MEAN, std=CIFAR10_STD),
        ToTensorV2(),
    ])
    
    val_transforms = A.Compose([
        A.Normalize(mean=CIFAR10_MEAN, std=CIFAR10_STD),
        ToTensorV2(),
    ])
    
    train_ds = torchvision.datasets.CIFAR10(root='./data', train=True, download=True,
                                           transform=AlbumentationsTransform(train_transforms))
    val_ds = torchvision.datasets.CIFAR10(root='./data', train=False, download=True,
                                         transform=AlbumentationsTransform(val_transforms))
    
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, 
                             num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size*2, shuffle=False, 
                           num_workers=num_workers, pin_memory=True)
    
    return train_loader, val_loader

def main():
    parser = argparse.ArgumentParser(description='Enhanced CIFAR_GAP_Net Training')
    parser.add_argument('--epochs', type=int, default=150, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=128, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.003, help='Learning rate')
    parser.add_argument('--weight-decay', type=float, default=1e-4, help='Weight decay')
    parser.add_argument('--target-accuracy', type=float, default=85.0, help='Target accuracy')
    parser.add_argument('--num-workers', type=int, default=4, help='Number of workers')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    # Set random seed
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    
    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Create enhanced model
    model = BudgetCompliantEnhancedCIFAR_GAP_Net(num_classes=10)
    model = model.to(device)
    
    # Display model info
    model_info = model.get_model_info()
    print(f"\n🚀 Enhanced Model Created:")
    print(f"  Name: {model_info['model_name']}")
    print(f"  Parameters: {model_info['total_parameters']:,}")
    print(f"  Budget: {model_info['parameter_budget_used']:.1f}% of 200K")
    print(f"  Target: {model_info['target_accuracy']}% accuracy")
    
    # Create data loaders
    train_loader, val_loader = create_enhanced_dataloaders(args.batch_size, args.num_workers)
    print(f"\n📊 Data loaded: {len(train_loader.dataset):,} train, {len(val_loader.dataset):,} val")
    
    # Optimizer and scheduler
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    
    # Loss function with label smoothing
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    
    # Create trainer
    trainer = EnhancedCIFAR10Trainer(
        model=model,
        device=device,
        train_loader=train_loader,
        val_loader=val_loader,
        optimizer=optimizer,
        scheduler=scheduler,
        criterion=criterion,
        target_accuracy=args.target_accuracy
    )
    
    # Train
    best_accuracy = trainer.train(args.epochs)
    
    print(f"\n🎯 Final Result: {best_accuracy:.2f}% accuracy")
    print(f"Enhanced model {'✅ SUCCESS' if best_accuracy >= args.target_accuracy else '📈 In Progress'}")

if __name__ == '__main__':
    main()
