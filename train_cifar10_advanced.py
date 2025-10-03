"""
Advanced CIFAR-10 Training Script
================================

Training script for the Advanced Neural Networks assignment.
Target: 85% accuracy with <200K parameters on CIFAR-10.

Key Features:
- Advanced model architecture (C1, C2, C3, C4, O)
- Comprehensive data augmentation
- Optimized training pipeline
- Real-time monitoring and checkpointing
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision
import torchvision.datasets as datasets

import numpy as np
import matplotlib.pyplot as plt
import time
import json
import argparse
from datetime import datetime
import os

# Import our modules
from cifar10_optimized_model import OptimizedCIFAR10Model, create_optimized_cifar10_model
from cifar10_augmentation import get_cifar10_transforms

class CIFAR10Trainer:
    """Advanced trainer for CIFAR-10 model"""
    
    def __init__(self, model, device, train_loader, test_loader, 
                 optimizer, scheduler, criterion):
        self.model = model
        self.device = device
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = criterion
        
        # Training tracking
        self.train_losses = []
        self.train_accuracies = []
        self.test_losses = []
        self.test_accuracies = []
        self.learning_rates = []
        
        self.best_accuracy = 0.0
        self.best_model_state = None
        
        # CIFAR-10 class names for analysis
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
            
            # Zero gradients
            self.optimizer.zero_grad()
            
            # Forward pass
            output = self.model(data)
            loss = self.criterion(output, target)
            
            # Backward pass
            loss.backward()
            
            # Gradient clipping for stability
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            # Update weights
            self.optimizer.step()
            
            # Statistics
            running_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            # Print progress
            if batch_idx % 100 == 0:
                current_lr = self.optimizer.param_groups[0]['lr']
                accuracy = 100. * correct / total
                print(f'Epoch {epoch}, Batch {batch_idx:3d}/{len(self.train_loader)}, '
                      f'Loss: {loss.item():.4f}, Acc: {accuracy:.2f}%, LR: {current_lr:.6f}')
        
        # Calculate epoch metrics
        epoch_loss = running_loss / len(self.train_loader)
        epoch_accuracy = 100. * correct / total
        
        return epoch_loss, epoch_accuracy
    
    def test_epoch(self):
        """Test/validation for one epoch"""
        self.model.eval()
        test_loss = 0
        correct = 0
        total = 0
        
        # Per-class accuracy tracking
        class_correct = list(0. for i in range(10))
        class_total = list(0. for i in range(10))
        
        with torch.no_grad():
            for data, target in self.test_loader:
                data, target = data.to(self.device), target.to(self.device)
                
                output = self.model(data)
                test_loss += self.criterion(output, target).item()
                
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
                
                # Per-class statistics
                c = (predicted == target).squeeze()
                for i in range(target.size(0)):
                    label = target[i]
                    class_correct[label] += c[i].item()
                    class_total[label] += 1
        
        # Calculate metrics
        test_loss /= len(self.test_loader)
        test_accuracy = 100. * correct / total
        
        # Per-class accuracies
        class_accuracies = {}
        for i in range(10):
            if class_total[i] > 0:
                class_accuracies[self.class_names[i]] = 100 * class_correct[i] / class_total[i]
            else:
                class_accuracies[self.class_names[i]] = 0
        
        return test_loss, test_accuracy, class_accuracies
    
    def train(self, epochs, target_accuracy=85.0, save_checkpoints=True):
        """Main training loop"""
        print(f"\n🚀 Starting CIFAR-10 Advanced Training")
        print(f"Target: {target_accuracy}% accuracy in ≤{epochs} epochs")
        print(f"Model parameters: {self.model.count_parameters():,}")
        print("-" * 60)
        
        start_time = time.time()
        target_reached = False
        
        for epoch in range(1, epochs + 1):
            epoch_start = time.time()
            
            # Training
            train_loss, train_acc = self.train_epoch(epoch)
            
            # Testing
            test_loss, test_acc, class_accs = self.test_epoch()
            
            # Learning rate scheduling
            if isinstance(self.scheduler, optim.lr_scheduler.ReduceLROnPlateau):
                self.scheduler.step(test_loss)
            else:
                self.scheduler.step()
            
            current_lr = self.optimizer.param_groups[0]['lr']
            
            # Record metrics
            self.train_losses.append(train_loss)
            self.train_accuracies.append(train_acc)
            self.test_losses.append(test_loss)
            self.test_accuracies.append(test_acc)
            self.learning_rates.append(current_lr)
            
            # Check for best model
            if test_acc > self.best_accuracy:
                improvement = test_acc - self.best_accuracy
                self.best_accuracy = test_acc
                self.best_model_state = self.model.state_dict().copy()
                
                print(f"🎯 New best accuracy: {test_acc:.2f}% (+{improvement:.2f}%)")
                
                if save_checkpoints:
                    self.save_checkpoint(epoch, 'best')
            
            # Epoch summary
            epoch_time = time.time() - epoch_start
            print(f"\nEpoch {epoch:3d}/{epochs}")
            print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
            print(f"Test  Loss: {test_loss:.4f}, Test  Acc: {test_acc:.2f}%")
            print(f"LR: {current_lr:.6f}, Time: {epoch_time:.1f}s")
            
            # Per-class accuracy (every 10 epochs)
            if epoch % 10 == 0:
                print(f"\nPer-class accuracies (Epoch {epoch}):")
                for class_name, acc in class_accs.items():
                    print(f"  {class_name:>10}: {acc:.1f}%")
            
            # Target check
            if test_acc >= target_accuracy and not target_reached:
                print(f"\n🎉 TARGET ACHIEVED! Test Accuracy: {test_acc:.2f}%")
                target_reached = True
                if save_checkpoints:
                    self.save_checkpoint(epoch, 'target_achieved')
            
            # Early stopping check
            if epoch > 50 and test_acc < 70:
                print(f"\n⚠️  Training seems stuck. Consider adjusting hyperparameters.")
            
            print("-" * 60)
        
        total_time = time.time() - start_time
        
        # Load best model
        if self.best_model_state is not None:
            self.model.load_state_dict(self.best_model_state)
        
        print(f"\n🏆 Training Completed!")
        print(f"⏱️  Total time: {total_time/3600:.2f} hours")
        print(f"🎯 Best accuracy: {self.best_accuracy:.2f}%")
        print(f"✅ Target {'ACHIEVED' if self.best_accuracy >= target_accuracy else 'NOT ACHIEVED'}")
        
        return {
            'best_accuracy': self.best_accuracy,
            'target_achieved': self.best_accuracy >= target_accuracy,
            'total_time': total_time,
            'epochs_trained': epochs,
            'train_losses': self.train_losses,
            'train_accuracies': self.train_accuracies,
            'test_losses': self.test_losses,
            'test_accuracies': self.test_accuracies,
            'learning_rates': self.learning_rates
        }
    
    def save_checkpoint(self, epoch, checkpoint_type='regular'):
        """Save model checkpoint"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'best_accuracy': self.best_accuracy,
            'train_losses': self.train_losses,
            'train_accuracies': self.train_accuracies,
            'test_losses': self.test_losses,
            'test_accuracies': self.test_accuracies,
        }
        
        filename = f'cifar10_advanced_{checkpoint_type}_epoch_{epoch}.pth'
        torch.save(checkpoint, filename)
        print(f"💾 Checkpoint saved: {filename}")
    
    def plot_training_curves(self, save_path=None):
        """Plot training curves"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        epochs = range(1, len(self.train_losses) + 1)
        
        # Loss curves
        ax1.plot(epochs, self.train_losses, 'b-', label='Train Loss')
        ax1.plot(epochs, self.test_losses, 'r-', label='Test Loss')
        ax1.set_title('Training and Test Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        ax1.grid(True)
        
        # Accuracy curves
        ax2.plot(epochs, self.train_accuracies, 'b-', label='Train Accuracy')
        ax2.plot(epochs, self.test_accuracies, 'r-', label='Test Accuracy')
        ax2.axhline(y=85, color='g', linestyle='--', label='Target (85%)')
        ax2.set_title('Training and Test Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy (%)')
        ax2.legend()
        ax2.grid(True)
        
        # Learning rate
        ax3.plot(epochs, self.learning_rates, 'g-')
        ax3.set_title('Learning Rate Schedule')
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('Learning Rate')
        ax3.set_yscale('log')
        ax3.grid(True)
        
        # Accuracy zoom (last 50% of training)
        start_idx = len(epochs) // 2
        ax4.plot(epochs[start_idx:], self.test_accuracies[start_idx:], 'r-', linewidth=2)
        ax4.axhline(y=85, color='g', linestyle='--', label='Target (85%)')
        ax4.set_title('Test Accuracy (Second Half)')
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Accuracy (%)')
        ax4.legend()
        ax4.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        plt.show()

def create_data_loaders(batch_size=128, num_workers=4, augmentation_type='standard'):
    """Create CIFAR-10 data loaders"""
    
    # Get transforms
    train_transform = get_cifar10_transforms('train', augmentation_type, use_cutout=True)
    test_transform = get_cifar10_transforms('test', augmentation_type)
    
    # Load datasets
    train_dataset = datasets.CIFAR10(
        root='./data', train=True, download=True, transform=train_transform
    )
    
    test_dataset = datasets.CIFAR10(
        root='./data', train=False, download=True, transform=test_transform
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True,
        num_workers=num_workers, pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size*2, shuffle=False,
        num_workers=num_workers, pin_memory=True
    )
    
    print(f"📊 Dataset loaded:")
    print(f"  Training samples: {len(train_dataset):,}")
    print(f"  Test samples: {len(test_dataset):,}")
    print(f"  Batch size: {batch_size}")
    print(f"  Augmentation: {augmentation_type}")
    
    return train_loader, test_loader

def create_optimizer_and_scheduler(model, optimizer_type='adamw', lr=0.001, 
                                 scheduler_type='cosine', epochs=150):
    """Create optimizer and learning rate scheduler"""
    
    if optimizer_type.lower() == 'adamw':
        optimizer = optim.AdamW(
            model.parameters(),
            lr=lr,
            weight_decay=1e-4,
            betas=(0.9, 0.999)
        )
    elif optimizer_type.lower() == 'sgd':
        optimizer = optim.SGD(
            model.parameters(),
            lr=lr,
            momentum=0.9,
            weight_decay=1e-4,
            nesterov=True
        )
    else:
        raise ValueError(f"Unknown optimizer: {optimizer_type}")
    
    if scheduler_type.lower() == 'cosine':
        scheduler = optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=epochs, eta_min=lr*0.01
        )
    elif scheduler_type.lower() == 'step':
        scheduler = optim.lr_scheduler.StepLR(
            optimizer, step_size=50, gamma=0.1
        )
    elif scheduler_type.lower() == 'plateau':
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=10
        )
    else:
        raise ValueError(f"Unknown scheduler: {scheduler_type}")
    
    print(f"🔧 Optimizer: {optimizer_type.upper()}")
    print(f"📈 Scheduler: {scheduler_type.upper()}")
    print(f"📊 Initial LR: {lr}")
    
    return optimizer, scheduler

def main():
    """Main training function"""
    parser = argparse.ArgumentParser(description='Train Advanced CIFAR-10 Model')
    
    # Model arguments
    parser.add_argument('--epochs', type=int, default=150,
                       help='Number of training epochs (default: 150)')
    parser.add_argument('--batch-size', type=int, default=128,
                       help='Batch size (default: 128)')
    parser.add_argument('--lr', type=float, default=0.001,
                       help='Learning rate (default: 0.001)')
    
    # Training arguments
    parser.add_argument('--optimizer', type=str, default='adamw',
                       choices=['adamw', 'sgd'], help='Optimizer type')
    parser.add_argument('--scheduler', type=str, default='cosine',
                       choices=['cosine', 'step', 'plateau'], help='Scheduler type')
    parser.add_argument('--augmentation', type=str, default='standard',
                       choices=['standard', 'albumentations'], help='Augmentation type')
    
    # System arguments
    parser.add_argument('--num-workers', type=int, default=4,
                       help='Number of data loading workers')
    parser.add_argument('--no-cuda', action='store_true',
                       help='Disable CUDA training')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed')
    
    # Output arguments
    parser.add_argument('--save-plots', action='store_true',
                       help='Save training plots')
    parser.add_argument('--save-checkpoints', action='store_true', default=True,
                       help='Save model checkpoints')
    
    args = parser.parse_args()
    
    # Set random seed
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    
    # Device setup
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    print(f"🖥️  Using device: {device}")
    
    if use_cuda:
        print(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
        print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    # Create model
    print(f"\n🏗️  Creating Optimized CIFAR-10 Model...")
    model, model_info = create_optimized_cifar10_model()
    model = model.to(device)
    
    # Verify requirements
    if not model_info['parameter_requirement_met']:
        print(f"❌ Model has {model_info['total_parameters']:,} parameters (>200K limit)")
        return
    
    if not model_info['rf_requirement_met']:
        print(f"❌ Model RF is {model_info['receptive_field']} (<44 requirement)")
        return
    
    # Create data loaders
    print(f"\n📊 Creating data loaders...")
    train_loader, test_loader = create_data_loaders(
        args.batch_size, args.num_workers, args.augmentation
    )
    
    # Create optimizer and scheduler
    print(f"\n⚙️  Setting up training...")
    optimizer, scheduler = create_optimizer_and_scheduler(
        model, args.optimizer, args.lr, args.scheduler, args.epochs
    )
    
    # Loss function
    criterion = nn.CrossEntropyLoss()
    
    # Create trainer
    trainer = CIFAR10Trainer(
        model, device, train_loader, test_loader,
        optimizer, scheduler, criterion
    )
    
    # Start training
    print(f"\n🎯 Training Configuration:")
    print(f"  Target: 85% accuracy")
    print(f"  Epochs: {args.epochs}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Learning rate: {args.lr}")
    print(f"  Expected time: 2-4 hours")
    
    # Train model
    results = trainer.train(
        epochs=args.epochs,
        target_accuracy=85.0,
        save_checkpoints=args.save_checkpoints
    )
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"cifar10_advanced_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Results saved to: {results_file}")
    
    # Plot training curves
    if args.save_plots:
        plot_file = f"cifar10_advanced_plots_{timestamp}.png"
        trainer.plot_training_curves(save_path=plot_file)
        print(f"📊 Plots saved to: {plot_file}")
    else:
        trainer.plot_training_curves()
    
    # Final summary
    print(f"\n🎯 Final Results:")
    print(f"✅ Best accuracy: {results['best_accuracy']:.2f}%")
    print(f"✅ Target achieved: {results['target_achieved']}")
    print(f"✅ Training time: {results['total_time']/3600:.2f} hours")
    print(f"✅ Model parameters: {model_info['total_parameters']:,} (<200K)")
    print(f"✅ Receptive field: {model_info['receptive_field']} (>44)")

if __name__ == "__main__":
    main()
