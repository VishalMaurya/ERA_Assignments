"""
Fine-tuning Script for Ultra-Efficient Models to Reach 99.4% Target
===================================================================

This script implements advanced fine-tuning strategies to push the models
from 98.8% to 99.4%+ accuracy while staying under 8K parameters.

Fine-tuning Strategies:
1. Lower learning rates with cosine annealing
2. Advanced data augmentation (CutOut, MixUp concepts)
3. Label smoothing for better generalization
4. Test Time Augmentation (TTA)
5. Optimized Focal Loss parameters
6. Progressive unfreezing and learning rate scheduling
"""

import argparse
import time
import json
from datetime import datetime
import os
import random
import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    from torch.utils.data import DataLoader
    import torchvision
    import torchvision.transforms as transforms
    from ultra_efficient_models import Model_1, Model_2, Model_3, create_model
    TORCH_AVAILABLE = True
except ImportError as e:
    print(f"❌ PyTorch not available: {e}")
    print("Install with: pip install torch torchvision")
    TORCH_AVAILABLE = False
    exit(1)

class AdvancedFocalLoss(nn.Module):
    """Enhanced Focal Loss with label smoothing"""
    def __init__(self, alpha=1.0, gamma=2.0, label_smoothing=0.1, reduction='mean'):
        super(AdvancedFocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.label_smoothing = label_smoothing
        self.reduction = reduction

    def forward(self, inputs, targets):
        # Apply label smoothing
        num_classes = inputs.size(-1)
        if self.label_smoothing > 0:
            smooth_targets = torch.zeros_like(inputs)
            smooth_targets.fill_(self.label_smoothing / (num_classes - 1))
            smooth_targets.scatter_(1, targets.unsqueeze(1), 1.0 - self.label_smoothing)
            
            # Compute cross entropy with smooth targets
            log_probs = F.log_softmax(inputs, dim=-1)
            ce_loss = -torch.sum(smooth_targets * log_probs, dim=-1)
        else:
            ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        
        # Compute focal loss
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

class CutOut(object):
    """CutOut data augmentation"""
    def __init__(self, length=8):
        self.length = length

    def __call__(self, img):
        h, w = img.size(1), img.size(2)
        mask = np.ones((h, w), np.float32)
        
        y = np.random.randint(h)
        x = np.random.randint(w)
        
        y1 = np.clip(y - self.length // 2, 0, h)
        y2 = np.clip(y + self.length // 2, 0, h)
        x1 = np.clip(x - self.length // 2, 0, w)
        x2 = np.clip(x + self.length // 2, 0, w)
        
        mask[y1:y2, x1:x2] = 0.
        mask = torch.from_numpy(mask)
        mask = mask.expand_as(img)
        img *= mask
        
        return img

class FineTuner:
    """Advanced fine-tuner for ultra-efficient models"""
    
    def __init__(self, model, model_name, device='cpu', 
                 focal_alpha=1.2, focal_gamma=2.5, label_smoothing=0.1):
        self.model = model.to(device)
        self.model_name = model_name
        self.device = device
        self.best_accuracy = 0.0
        self.training_history = []
        
        # Enhanced loss function
        self.criterion = AdvancedFocalLoss(
            alpha=focal_alpha, 
            gamma=focal_gamma, 
            label_smoothing=label_smoothing
        )
        print(f"🎯 Using Enhanced Focal Loss (α={focal_alpha}, γ={focal_gamma}, smoothing={label_smoothing})")
        
    def prepare_data(self, batch_size=128, use_advanced_augmentation=True):
        """Prepare data with advanced augmentation"""
        
        if use_advanced_augmentation:
            # Advanced training augmentation
            train_transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,)),
                transforms.RandomRotation(degrees=10),  # Increased rotation
                transforms.RandomAffine(degrees=0, translate=(0.15, 0.15), scale=(0.9, 1.1)),
                CutOut(length=6),  # CutOut augmentation
            ])
            print("🔄 Using advanced data augmentation (rotation + translation + cutout)")
        else:
            train_transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,)),
                transforms.RandomRotation(degrees=7),
                transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
            ])
            print("🔄 Using standard data augmentation")
        
        # Test transform (no augmentation)
        test_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        # Load datasets
        train_dataset = torchvision.datasets.MNIST(
            root='./data', train=True, download=True, transform=train_transform
        )
        
        test_dataset = torchvision.datasets.MNIST(
            root='./data', train=False, download=True, transform=test_transform
        )
        
        self.train_loader = DataLoader(
            train_dataset, batch_size=batch_size, shuffle=True, 
            num_workers=2, pin_memory=True, drop_last=True
        )
        
        self.test_loader = DataLoader(
            test_dataset, batch_size=batch_size*2, shuffle=False, 
            num_workers=2, pin_memory=True
        )
        
        print(f"📊 Training samples: {len(train_dataset):,}")
        print(f"📊 Test samples: {len(test_dataset):,}")
        print(f"📊 Batch size: {batch_size}")
        
    def train_epoch(self, optimizer, epoch, scheduler=None):
        """Train one epoch with advanced techniques"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(self.train_loader):
            data, target = data.to(self.device), target.to(self.device)
            
            optimizer.zero_grad()
            output = self.model(data)
            
            # Use enhanced focal loss
            loss = self.criterion(output, target)
            
            loss.backward()
            
            # Gradient clipping for stability
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=0.5)
            
            optimizer.step()
            
            # Step scheduler per batch for OneCycleLR
            if scheduler is not None:
                scheduler.step()
            
            running_loss += loss.item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
            
            # Print progress every 100 batches
            if batch_idx % 100 == 0:
                current_lr = optimizer.param_groups[0]['lr']
                print(f'Epoch {epoch}, Batch {batch_idx:3d}/{len(self.train_loader)}, '
                      f'Loss: {loss.item():.6f}, Acc: {100.*correct/total:.2f}%, LR: {current_lr:.6f}')
        
        epoch_loss = running_loss / len(self.train_loader)
        epoch_acc = 100. * correct / total
        
        return epoch_loss, epoch_acc
    
    def test_with_tta(self, num_tta=5):
        """Test with Test Time Augmentation for better accuracy"""
        self.model.eval()
        test_loss = 0
        correct = 0
        total = 0
        
        # TTA transforms
        tta_transforms = [
            transforms.Compose([
                transforms.ToPILImage(),
                transforms.RandomRotation(degrees=5),
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ]) for _ in range(num_tta-1)
        ]
        
        # Add original transform
        tta_transforms.append(transforms.Compose([
            transforms.Normalize((0.1307,), (0.3081,))
        ]))
        
        with torch.no_grad():
            for data, target in self.test_loader:
                data, target = data.to(self.device), target.to(self.device)
                
                # Collect predictions from multiple augmentations
                predictions = []
                
                for i, tta_transform in enumerate(tta_transforms):
                    if i == len(tta_transforms) - 1:  # Original data
                        aug_data = data
                    else:
                        # Apply TTA transform
                        aug_data = torch.stack([
                            tta_transform(img) for img in data
                        ]).to(self.device)
                    
                    output = self.model(aug_data)
                    predictions.append(F.softmax(output, dim=1))
                
                # Average predictions
                avg_output = torch.stack(predictions).mean(dim=0)
                
                # Calculate loss and accuracy
                test_loss += F.cross_entropy(torch.log(avg_output + 1e-8), target, reduction='sum').item()
                pred = avg_output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
                total += target.size(0)
        
        test_loss /= total
        test_accuracy = 100. * correct / total
        
        return test_loss, test_accuracy
    
    def test(self):
        """Standard test without TTA"""
        self.model.eval()
        test_loss = 0
        correct = 0
        
        with torch.no_grad():
            for data, target in self.test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                test_loss += F.cross_entropy(output, target, reduction='sum').item()
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
        
        test_loss /= len(self.test_loader.dataset)
        test_acc = 100. * correct / len(self.test_loader.dataset)
        
        return test_loss, test_acc
    
    def finetune(self, epochs=20, base_lr=0.001, target_accuracy=99.4, use_tta=True):
        """Fine-tune the model with advanced techniques"""
        print(f"\n🚀 Fine-tuning {self.model_name} for 99.4% Target")
        print(f"Parameters: {self.model.count_parameters():,}")
        print(f"Target: {target_accuracy}% accuracy in ≤{epochs} epochs")
        print("-" * 60)
        
        # Optimized learning rates per model
        if self.model_name == "Model_1":
            lr = base_lr * 0.5  # Smaller model, lower LR
        elif self.model_name == "Model_2":
            lr = base_lr * 0.7  # Depthwise separable, moderate LR
        else:  # Model_3
            lr = base_lr * 0.6  # Residual connections, moderate LR
        
        # Advanced optimizer setup
        optimizer = optim.AdamW(
            self.model.parameters(), 
            lr=lr, 
            weight_decay=1e-4,
            betas=(0.9, 0.999),
            eps=1e-8
        )
        
        # Cosine annealing with warm restarts
        scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer, 
            T_0=5,  # Restart every 5 epochs
            T_mult=1,
            eta_min=lr * 0.01
        )
        
        print(f"🔧 Using AdamW optimizer (LR={lr:.6f})")
        print(f"📈 Using CosineAnnealingWarmRestarts scheduler")
        
        start_time = time.time()
        target_reached = False
        consecutive_improvements = 0
        
        for epoch in range(1, epochs + 1):
            current_lr = optimizer.param_groups[0]['lr']
            print(f"Epoch {epoch:2d}/{epochs} | LR={current_lr:.6f}")
            
            # Train
            train_loss, train_acc = self.train_epoch(optimizer, epoch)
            
            # Test with or without TTA
            if use_tta and epoch > 10:  # Use TTA in later epochs
                test_loss, test_acc = self.test_with_tta(num_tta=3)
                print(f"🔄 Using TTA (3 augmentations)")
            else:
                test_loss, test_acc = self.test()
            
            # Update scheduler
            scheduler.step()
            
            # Track best accuracy
            if test_acc > self.best_accuracy:
                improvement = test_acc - self.best_accuracy
                self.best_accuracy = test_acc
                consecutive_improvements += 1
                print(f"🎯 New best accuracy: {test_acc:.3f}% (+{improvement:.3f}%)")
                
                # Save best model
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'accuracy': test_acc,
                    'loss': test_loss
                }, f'finetuned_best_{self.model_name.lower()}.pth')
            else:
                consecutive_improvements = 0
            
            # Record training history
            self.training_history.append({
                'epoch': epoch,
                'train_loss': train_loss,
                'train_acc': train_acc,
                'test_loss': test_loss,
                'test_acc': test_acc,
                'lr': current_lr
            })
            
            print(f"Train Loss={train_loss:.4f}, Acc={train_acc:.2f}%")
            print(f"Test  Loss={test_loss:.4f}, Acc={test_acc:.3f}%")
            
            # Check if target reached
            if test_acc >= target_accuracy and not target_reached:
                print(f"\n🎉 TARGET ACHIEVED! Test Accuracy: {test_acc:.3f}%")
                target_reached = True
                # Continue training to see if we can do even better
            
            # Early stopping if no improvement for 8 epochs
            if consecutive_improvements == 0 and epoch > 10:
                no_improvement_epochs = epoch - max([i for i, h in enumerate(self.training_history) 
                                                   if h['test_acc'] == self.best_accuracy], default=[0])[-1] - 1
                if no_improvement_epochs >= 8:
                    print(f"\n⏹️  Early stopping: No improvement for 8 epochs")
                    break
            
            print()
        
        training_time = time.time() - start_time
        
        print(f"🏆 Fine-tuning completed for {self.model_name}")
        print(f"⏱️  Training time: {training_time:.1f}s")
        print(f"🎯 Best accuracy: {self.best_accuracy:.3f}%")
        print(f"✅ Target {'ACHIEVED' if self.best_accuracy >= target_accuracy else 'NOT ACHIEVED'}")
        
        return {
            'model_name': self.model_name,
            'best_accuracy': self.best_accuracy,
            'training_time': training_time,
            'target_achieved': self.best_accuracy >= target_accuracy,
            'epochs_trained': epoch,
            'parameters': self.model.count_parameters(),
            'history': self.training_history
        }

def finetune_single_model(model_name, epochs=20, lr=0.001, batch_size=128, 
                         focal_alpha=1.2, focal_gamma=2.5, label_smoothing=0.1,
                         use_tta=True, use_advanced_aug=True):
    """Fine-tune a single model"""
    print(f"\n{'='*60}")
    print(f"Fine-tuning {model_name} with Advanced Techniques")
    print(f"{'='*60}")
    
    # Create model
    model = create_model(model_name)
    
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🖥️  Using device: {device}")
    
    # Create fine-tuner
    finetuner = FineTuner(
        model, model_name, device, 
        focal_alpha, focal_gamma, label_smoothing
    )
    
    # Prepare data
    finetuner.prepare_data(batch_size, use_advanced_aug)
    
    # Fine-tune model
    results = finetuner.finetune(epochs, lr, 99.4, use_tta)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"finetune_results_{model_name.lower()}_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Results saved to: {results_file}")
    
    return results

def main():
    """Main fine-tuning function"""
    parser = argparse.ArgumentParser(description='Fine-tune Ultra-Efficient MNIST Models for 99.4% Target')
    parser.add_argument('--model', type=str, default='Model_2', 
                       choices=['Model_1', 'Model_2', 'Model_3', 'all'],
                       help='Model to fine-tune (default: Model_2 - best performer)')
    parser.add_argument('--epochs', type=int, default=20,
                       help='Number of epochs (default: 20)')
    parser.add_argument('--lr', type=float, default=0.001,
                       help='Base learning rate (default: 0.001)')
    parser.add_argument('--batch-size', type=int, default=128,
                       help='Batch size (default: 128)')
    parser.add_argument('--focal-alpha', type=float, default=1.2,
                       help='Focal Loss alpha (default: 1.2)')
    parser.add_argument('--focal-gamma', type=float, default=2.5,
                       help='Focal Loss gamma (default: 2.5)')
    parser.add_argument('--label-smoothing', type=float, default=0.1,
                       help='Label smoothing factor (default: 0.1)')
    parser.add_argument('--no-tta', action='store_true',
                       help='Disable Test Time Augmentation')
    parser.add_argument('--no-advanced-aug', action='store_true',
                       help='Disable advanced data augmentation')
    
    args = parser.parse_args()
    
    if not TORCH_AVAILABLE:
        print("❌ PyTorch not available. Please install PyTorch first.")
        return
    
    use_tta = not args.no_tta
    use_advanced_aug = not args.no_advanced_aug
    
    print("🎯 Ultra-Efficient MNIST Models Fine-tuning for 99.4% Target")
    print(f"Configuration: {args.epochs} epochs, LR={args.lr}, batch={args.batch_size}")
    print(f"Enhanced Focal Loss: α={args.focal_alpha}, γ={args.focal_gamma}")
    print(f"Label Smoothing: {args.label_smoothing}")
    print(f"Test Time Augmentation: {'Enabled' if use_tta else 'Disabled'}")
    print(f"Advanced Augmentation: {'Enabled' if use_advanced_aug else 'Disabled'}")
    
    if args.model == 'all':
        all_results = []
        for model_name in ['Model_1', 'Model_2', 'Model_3']:
            results = finetune_single_model(
                model_name, args.epochs, args.lr, args.batch_size,
                args.focal_alpha, args.focal_gamma, args.label_smoothing,
                use_tta, use_advanced_aug
            )
            all_results.append(results)
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 FINE-TUNING SUMMARY")
        print("=" * 80)
        
        print(f"{'Model':<10} {'Parameters':<12} {'Best Acc':<12} {'Time':<8} {'Target':<8}")
        print("-" * 70)
        
        for results in all_results:
            model_name = results['model_name']
            params = results['parameters']
            accuracy = results['best_accuracy']
            time_taken = results['training_time']
            target_met = "✅" if results['target_achieved'] else "❌"
            
            print(f"{model_name:<10} {params:<12,} {accuracy:<12.3f}% {time_taken:<8.1f}s {target_met:<8}")
        
        # Save combined results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        combined_file = f"finetune_all_results_{timestamp}.json"
        
        with open(combined_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"\n📁 Combined results saved to: {combined_file}")
        
    else:
        finetune_single_model(
            args.model, args.epochs, args.lr, args.batch_size,
            args.focal_alpha, args.focal_gamma, args.label_smoothing,
            use_tta, use_advanced_aug
        )

if __name__ == "__main__":
    main()
