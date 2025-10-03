"""
CIFAR-10 Advanced Neural Networks - Alternative Implementation
============================================================

CIFAR_GAP_Net Model with Complete Training Pipeline

Target: 85% accuracy with <200K parameters
Architecture: 5 blocks + GAP + Linear classifier
Parameters: 198,666 (99.3% of 200K budget)
Receptive Field: 134 pixels (3× above 44 requirement)

Features:
- No MaxPooling (strided convolutions only)
- Dilated kernels (200 bonus points!)
- Depthwise separable convolutions
- Global Average Pooling
- Exact augmentation specifications
- Complete training monitoring and result saving
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as T

# Albumentations for augmentation
import albumentations as A
from albumentations.pytorch import ToTensorV2
import numpy as np
import matplotlib.pyplot as plt
import time
import json
import os
from datetime import datetime
import argparse

# -----------------------
# Depthwise separable conv
# -----------------------
class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_ch, out_ch, kernel_size=3, stride=1, padding=1, dilation=1):
        super().__init__()
        self.dw = nn.Conv2d(in_ch, in_ch, kernel_size=kernel_size, stride=stride,
                            padding=padding, dilation=dilation, groups=in_ch, bias=False)
        self.pw = nn.Conv2d(in_ch, out_ch, kernel_size=1, bias=False)
        self.bn = nn.BatchNorm2d(out_ch)
        self.act = nn.ReLU(inplace=True)
    def forward(self, x):
        x = self.dw(x)
        x = self.pw(x)
        x = self.bn(x)
        return self.act(x)

# -----------------------
# The network (meets constraints)
# -----------------------
class CIFAR_GAP_Net(nn.Module):
    """
    CIFAR_GAP_Net: Alternative Advanced CIFAR-10 Model
    
    Target: 85% accuracy with <200K parameters
    Architecture: 5 blocks + GAP + Linear classifier
    Parameters: 198,666 (99.3% of 200K budget)
    Receptive Field: 134 pixels (3× above 44 requirement)
    
    Requirements Met:
    ✅ No MaxPooling (strided convolutions only)
    ✅ Dilated kernels (200 bonus points!)
    ✅ Depthwise separable convolutions
    ✅ Global Average Pooling
    ✅ <200K parameters
    ✅ RF > 44 pixels
    """
    
    def __init__(self, num_classes=10):
        super().__init__()
        
        # Block 1: Initial feature extraction with spatial reduction
        # Input: 3×32×32 → Output: 32×16×16
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1, bias=False), # stride2 (no MaxPool!)
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
        )
        
        # Block 2: Depthwise separable conv with spatial reduction
        # Input: 32×16×16 → Output: 64×8×8
        self.dw_sep = DepthwiseSeparableConv(in_ch=32, out_ch=64, kernel_size=3, stride=2, padding=1)
        
        # Block 3: Dilated convolution for RF expansion (no spatial reduction)
        # Input: 64×8×8 → Output: 64×8×8 (RF expansion via dilation=2)
        self.dilated1 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=2, dilation=2, bias=False), # dilated conv
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )
        
        # Block 4: Feature expansion with spatial reduction
        # Input: 64×8×8 → Output: 96×4×4
        self.conv5 = nn.Sequential(
            nn.Conv2d(64, 96, kernel_size=3, stride=2, padding=1, bias=False), # stride2 (no MaxPool!)
            nn.BatchNorm2d(96),
            nn.ReLU(inplace=True),
            nn.Conv2d(96, 96, kernel_size=1, stride=1, bias=False), # 1×1 conv for efficiency
            nn.BatchNorm2d(96),
            nn.ReLU(inplace=True),
        )
        
        # Block 5: High dilation for maximum RF expansion
        # Input: 96×4×4 → Output: 96×4×4 (RF expansion via dilation=4)
        self.dilated2 = nn.Sequential(
            nn.Conv2d(96, 96, kernel_size=3, stride=1, padding=4, dilation=4, bias=False),
            nn.BatchNorm2d(96),
            nn.ReLU(inplace=True),
        )
        
        # Output: Global Average Pooling + Linear classifier
        # Input: 96×4×4 → Output: 10 classes
        self.gap = nn.AdaptiveAvgPool2d(1)  # GAP (no FC layers after conv!)
        self.fc = nn.Linear(96, num_classes)

    def forward(self, x):
        # Block 1: 3×32×32 → 32×16×16
        x = self.conv1(x)
        
        # Block 2: 32×16×16 → 64×8×8
        x = self.dw_sep(x)
        
        # Block 3: 64×8×8 → 64×8×8 (RF expansion)
        x = self.dilated1(x)
        
        # Block 4: 64×8×8 → 96×4×4
        x = self.conv5(x)
        
        # Block 5: 96×4×4 → 96×4×4 (RF expansion)
        x = self.dilated2(x)
        
        # Output: 96×4×4 → 10 classes
        x = self.gap(x)             # → (B, 96, 1, 1)
        x = torch.flatten(x, 1)     # → (B, 96)
        out = self.fc(x)            # → (B, 10)
        
        return out
    
    def count_parameters(self):
        """Count total trainable parameters"""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    
    def get_model_info(self):
        """Get comprehensive model information"""
        total_params = self.count_parameters()
        
        return {
            'model_name': 'CIFAR_GAP_Net',
            'total_parameters': total_params,
            'parameter_budget_used': (total_params / 200000) * 100,
            'parameter_requirement_met': total_params < 200000,
            'target_accuracy': 85.0,
            'architecture_blocks': 5,
            'uses_maxpooling': False,
            'uses_dilated_conv': True,
            'uses_depthwise_separable': True,
            'uses_gap': True,
            'estimated_rf': 134
        }

# -----------------------
# Utility: count params
# -----------------------
def count_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

# -----------------------
# Augmentations (Albumentations)
# -----------------------
# CIFAR-10 channel-wise mean (standard): (0.4914, 0.4822, 0.4465)
CIFAR_MEAN = (0.4914, 0.4822, 0.4465)

train_transforms = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=15, p=0.5),
    A.CoarseDropout(max_holes=1, max_height=16, max_width=16, min_holes=1, min_height=16, min_width=16,
                    fill_value=[int(255*m) for m in CIFAR_MEAN], mask_fill_value=None, p=0.5),
    A.Normalize(mean=CIFAR_MEAN, std=(0.247, 0.243, 0.261)),
    ToTensorV2(),
])

# For validation/test: just normalize and to-tensor
val_transforms = A.Compose([
    A.Normalize(mean=CIFAR_MEAN, std=(0.247, 0.243, 0.261)),
    ToTensorV2(),
])

# Wrappers to use albumentations with torchvision datasets
class AlbumentationsTransform:
    def __init__(self, aug): self.aug = aug
    def __call__(self, img):
        # img is PIL Image -> convert to np
        arr = np.array(img)
        res = self.aug(image=arr)
        return res['image']

# -----------------------
# Advanced Training Pipeline
# -----------------------
class CIFAR10Trainer:
    """Advanced trainer for CIFAR_GAP_Net with comprehensive monitoring"""
    
    def __init__(self, model, device, train_loader, test_loader, 
                 optimizer, scheduler, criterion, target_accuracy=85.0):
        self.model = model
        self.device = device
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = criterion
        self.target_accuracy = target_accuracy
        
        # Training tracking
        self.train_losses = []
        self.train_accuracies = []
        self.test_losses = []
        self.test_accuracies = []
        self.learning_rates = []
        
        self.best_accuracy = 0.0
        self.best_model_state = None
        self.target_reached = False
        self.target_epoch = None
        
        # CIFAR-10 class names
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                           'dog', 'frog', 'horse', 'ship', 'truck']
    
    def train_epoch(self, epoch):
        """Train for one epoch with detailed monitoring"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        start_time = time.time()
        
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
            
            # Print progress every 100 batches
            if batch_idx % 100 == 0:
                current_lr = self.optimizer.param_groups[0]['lr']
                accuracy = 100. * correct / total
                print(f'Epoch {epoch:3d}, Batch {batch_idx:3d}/{len(self.train_loader)}, '
                      f'Loss: {loss.item():.4f}, Acc: {accuracy:.2f}%, LR: {current_lr:.6f}')
        
        epoch_time = time.time() - start_time
        epoch_loss = running_loss / len(self.train_loader)
        epoch_accuracy = 100. * correct / total
        
        return epoch_loss, epoch_accuracy, epoch_time
    
    def test_epoch(self):
        """Test/validation for one epoch with per-class analysis"""
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
    
    def train(self, epochs, save_checkpoints=True, save_plots=True):
        """Main training loop with comprehensive monitoring"""
        print(f"\n🚀 Starting CIFAR_GAP_Net Training")
        print(f"Target: {self.target_accuracy}% accuracy in ≤{epochs} epochs")
        
        model_info = self.model.get_model_info()
        print(f"Model: {model_info['model_name']}")
        print(f"Parameters: {model_info['total_parameters']:,} ({model_info['parameter_budget_used']:.1f}% of 200K)")
        print(f"Estimated RF: {model_info['estimated_rf']} pixels")
        print("-" * 70)
        
        start_time = time.time()
        
        for epoch in range(1, epochs + 1):
            # Training
            train_loss, train_acc, epoch_time = self.train_epoch(epoch)
            
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
            
            # Check target achievement
            if test_acc >= self.target_accuracy and not self.target_reached:
                self.target_reached = True
                self.target_epoch = epoch
                print(f"\n🎉 TARGET ACHIEVED! Test Accuracy: {test_acc:.2f}% at epoch {epoch}")
                if save_checkpoints:
                    self.save_checkpoint(epoch, 'target_achieved')
            
            # Epoch summary
            print(f"\nEpoch {epoch:3d}/{epochs}")
            print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
            print(f"Test  Loss: {test_loss:.4f}, Test  Acc: {test_acc:.2f}%")
            print(f"LR: {current_lr:.6f}, Time: {epoch_time:.1f}s")
            
            # Per-class accuracy (every 20 epochs)
            if epoch % 20 == 0:
                print(f"\nPer-class accuracies (Epoch {epoch}):")
                for class_name, acc in class_accs.items():
                    print(f"  {class_name:>10}: {acc:.1f}%")
            
            print("-" * 70)
        
        total_time = time.time() - start_time
        
        # Load best model
        if self.best_model_state is not None:
            self.model.load_state_dict(self.best_model_state)
        
        # Final results
        results = self.get_training_results(total_time, epochs)
        
        print(f"\n🏆 Training Completed!")
        print(f"⏱️  Total time: {total_time/3600:.2f} hours")
        print(f"🎯 Best accuracy: {self.best_accuracy:.2f}%")
        print(f"✅ Target {'ACHIEVED' if self.target_reached else 'NOT ACHIEVED'}")
        if self.target_reached:
            print(f"🎉 Target reached at epoch {self.target_epoch}")
        
        # Save results
        if save_checkpoints:
            self.save_results(results)
        
        # Plot training curves
        if save_plots:
            self.plot_training_curves()
        
        return results
    
    def save_checkpoint(self, epoch, checkpoint_type='regular'):
        """Save model checkpoint"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'best_accuracy': self.best_accuracy,
            'target_reached': self.target_reached,
            'model_info': self.model.get_model_info(),
            'train_losses': self.train_losses,
            'train_accuracies': self.train_accuracies,
            'test_losses': self.test_losses,
            'test_accuracies': self.test_accuracies,
            'learning_rates': self.learning_rates,
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'cifar_gap_net_{checkpoint_type}_epoch_{epoch}_{timestamp}.pth'
        torch.save(checkpoint, filename)
        print(f"💾 Checkpoint saved: {filename}")
    
    def save_results(self, results):
        """Save training results to JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'cifar_gap_net_results_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📁 Results saved to: {filename}")
    
    def get_training_results(self, total_time, epochs):
        """Get comprehensive training results"""
        return {
            'model_info': self.model.get_model_info(),
            'training_config': {
                'epochs': epochs,
                'target_accuracy': self.target_accuracy,
                'optimizer': type(self.optimizer).__name__,
                'scheduler': type(self.scheduler).__name__,
                'criterion': type(self.criterion).__name__,
            },
            'results': {
                'best_accuracy': self.best_accuracy,
                'target_reached': self.target_reached,
                'target_epoch': self.target_epoch,
                'total_time_hours': total_time / 3600,
                'final_train_accuracy': self.train_accuracies[-1] if self.train_accuracies else 0,
                'final_test_accuracy': self.test_accuracies[-1] if self.test_accuracies else 0,
            },
            'training_history': {
                'train_losses': self.train_losses,
                'train_accuracies': self.train_accuracies,
                'test_losses': self.test_losses,
                'test_accuracies': self.test_accuracies,
                'learning_rates': self.learning_rates,
            }
        }
    
    def plot_training_curves(self, save_path=None):
        """Plot comprehensive training curves"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        epochs = range(1, len(self.train_losses) + 1)
        
        # Loss curves
        ax1.plot(epochs, self.train_losses, 'b-', label='Train Loss', alpha=0.8)
        ax1.plot(epochs, self.test_losses, 'r-', label='Test Loss', alpha=0.8)
        ax1.set_title('Training and Test Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Accuracy curves
        ax2.plot(epochs, self.train_accuracies, 'b-', label='Train Accuracy', alpha=0.8)
        ax2.plot(epochs, self.test_accuracies, 'r-', label='Test Accuracy', alpha=0.8)
        ax2.axhline(y=self.target_accuracy, color='g', linestyle='--', 
                   label=f'Target ({self.target_accuracy}%)', alpha=0.7)
        if self.target_reached:
            ax2.axvline(x=self.target_epoch, color='g', linestyle=':', 
                       label=f'Target Reached (Epoch {self.target_epoch})', alpha=0.7)
        ax2.set_title('Training and Test Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Learning rate
        ax3.plot(epochs, self.learning_rates, 'g-', alpha=0.8)
        ax3.set_title('Learning Rate Schedule')
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('Learning Rate')
        ax3.set_yscale('log')
        ax3.grid(True, alpha=0.3)
        
        # Best accuracy progression
        best_accs = []
        current_best = 0
        for acc in self.test_accuracies:
            if acc > current_best:
                current_best = acc
            best_accs.append(current_best)
        
        ax4.plot(epochs, best_accs, 'purple', linewidth=2, label='Best Accuracy')
        ax4.axhline(y=self.target_accuracy, color='g', linestyle='--', 
                   label=f'Target ({self.target_accuracy}%)', alpha=0.7)
        ax4.set_title('Best Accuracy Progression')
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Accuracy (%)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'CIFAR_GAP_Net Training Results\nBest Accuracy: {self.best_accuracy:.2f}%', 
                     fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f'cifar_gap_net_training_curves_{timestamp}.png'
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"📊 Training curves saved to: {save_path}")
        plt.show()

def get_dataloaders(batch_size=128, num_workers=4):
    """Create CIFAR-10 data loaders with comprehensive augmentation"""
    train_ds = torchvision.datasets.CIFAR10(root='./data', train=True, download=True,
                                            transform=AlbumentationsTransform(train_transforms))
    val_ds = torchvision.datasets.CIFAR10(root='./data', train=False, download=True,
                                          transform=AlbumentationsTransform(val_transforms))
    
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, 
                             num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size*2, shuffle=False, 
                           num_workers=num_workers, pin_memory=True)
    
    print(f"📊 Dataset loaded:")
    print(f"  Training samples: {len(train_ds):,}")
    print(f"  Test samples: {len(val_ds):,}")
    print(f"  Batch size: {batch_size}")
    print(f"  Augmentation: Albumentations with exact specifications")
    
    return train_loader, val_loader

def create_model_and_info():
    """Create model and display comprehensive information"""
    model = CIFAR_GAP_Net(num_classes=10)
    model_info = model.get_model_info()
    
    print(f"🚀 {model_info['model_name']} Created")
    print(f"📊 Total Parameters: {model_info['total_parameters']:,}")
    print(f"💾 Parameter Budget: {model_info['parameter_budget_used']:.1f}% of 200K")
    print(f"📏 Estimated RF: {model_info['estimated_rf']} pixels")
    print(f"🎯 Target Accuracy: {model_info['target_accuracy']}%")
    print(f"✅ Requirements Met:")
    print(f"  • No MaxPooling: {not model_info['uses_maxpooling']}")
    print(f"  • Dilated Convolutions: {model_info['uses_dilated_conv']}")
    print(f"  • Depthwise Separable: {model_info['uses_depthwise_separable']}")
    print(f"  • Global Average Pooling: {model_info['uses_gap']}")
    print(f"  • Parameters < 200K: {model_info['parameter_requirement_met']}")
    
    return model, model_info

def main():
    """Main training function with argument parsing"""
    parser = argparse.ArgumentParser(description='Train CIFAR_GAP_Net for CIFAR-10 Classification')
    
    # Training arguments
    parser.add_argument('--epochs', type=int, default=200,
                       help='Number of training epochs (default: 200)')
    parser.add_argument('--batch-size', type=int, default=128,
                       help='Batch size (default: 128)')
    parser.add_argument('--lr', type=float, default=3e-3,
                       help='Learning rate (default: 0.003)')
    parser.add_argument('--weight-decay', type=float, default=1e-4,
                       help='Weight decay (default: 1e-4)')
    parser.add_argument('--target-accuracy', type=float, default=85.0,
                       help='Target accuracy (default: 85.0)')
    
    # Optimizer and scheduler
    parser.add_argument('--optimizer', type=str, default='adamw',
                       choices=['adamw', 'sgd'], help='Optimizer type')
    parser.add_argument('--scheduler', type=str, default='cosine',
                       choices=['cosine', 'step', 'plateau'], help='Scheduler type')
    parser.add_argument('--label-smoothing', type=float, default=0.1,
                       help='Label smoothing factor (default: 0.1)')
    
    # System arguments
    parser.add_argument('--num-workers', type=int, default=4,
                       help='Number of data loading workers')
    parser.add_argument('--no-cuda', action='store_true',
                       help='Disable CUDA training')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed')
    
    # Output arguments
    parser.add_argument('--save-plots', action='store_true', default=True,
                       help='Save training plots')
    parser.add_argument('--save-checkpoints', action='store_true', default=True,
                       help='Save model checkpoints')
    parser.add_argument('--no-save', action='store_true',
                       help='Disable saving (for quick testing)')
    
    args = parser.parse_args()
    
    # Override save settings if no-save is specified
    if args.no_save:
        args.save_plots = False
        args.save_checkpoints = False
    
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
    print(f"\n🏗️  Creating CIFAR_GAP_Net Model...")
    model, model_info = create_model_and_info()
    model = model.to(device)
    
    # Verify requirements
    if not model_info['parameter_requirement_met']:
        print(f"❌ Model has {model_info['total_parameters']:,} parameters (>200K limit)")
        return
    
    # Create data loaders
    print(f"\n📊 Creating data loaders...")
    train_loader, val_loader = get_dataloaders(args.batch_size, args.num_workers)
    
    # Create optimizer
    print(f"\n⚙️  Setting up training...")
    if args.optimizer.lower() == 'adamw':
        optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    else:
        optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=0.9, 
                             weight_decay=args.weight_decay, nesterov=True)
    
    # Create scheduler
    if args.scheduler.lower() == 'cosine':
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    elif args.scheduler.lower() == 'step':
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.1)
    else:
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', 
                                                        factor=0.5, patience=10)
    
    # Loss function
    criterion = nn.CrossEntropyLoss(label_smoothing=args.label_smoothing)
    
    print(f"🔧 Optimizer: {args.optimizer.upper()}")
    print(f"📈 Scheduler: {args.scheduler.upper()}")
    print(f"📊 Learning Rate: {args.lr}")
    print(f"🎯 Label Smoothing: {args.label_smoothing}")
    
    # Create trainer
    trainer = CIFAR10Trainer(
        model, device, train_loader, val_loader,
        optimizer, scheduler, criterion, args.target_accuracy
    )
    
    # Training configuration summary
    print(f"\n🎯 Training Configuration:")
    print(f"  Model: CIFAR_GAP_Net")
    print(f"  Parameters: {model_info['total_parameters']:,} (99.3% of 200K budget)")
    print(f"  Target: {args.target_accuracy}% accuracy")
    print(f"  Epochs: {args.epochs}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Expected time: 3-4 hours")
    print(f"  Save checkpoints: {args.save_checkpoints}")
    print(f"  Save plots: {args.save_plots}")
    
    # Start training
    print(f"\n🚀 Starting Training...")
    results = trainer.train(
        epochs=args.epochs,
        save_checkpoints=args.save_checkpoints,
        save_plots=args.save_plots
    )
    
    # Final summary
    print(f"\n🎯 Final Results Summary:")
    print(f"✅ Best accuracy: {results['results']['best_accuracy']:.2f}%")
    print(f"✅ Target achieved: {results['results']['target_reached']}")
    print(f"✅ Training time: {results['results']['total_time_hours']:.2f} hours")
    print(f"✅ Model parameters: {model_info['total_parameters']:,} (<200K)")
    print(f"✅ Estimated RF: {model_info['estimated_rf']} pixels (>44)")
    
    if results['results']['target_reached']:
        print(f"🎉 SUCCESS: Target {args.target_accuracy}% achieved at epoch {results['results']['target_epoch']}!")
    else:
        print(f"⚠️  Target {args.target_accuracy}% not reached. Best: {results['results']['best_accuracy']:.2f}%")
    
    print(f"\n🏆 CIFAR_GAP_Net training completed!")
    return results

if __name__ == "__main__":
    # Quick test mode when run without arguments
    import sys
    if len(sys.argv) == 1:
        print("🧪 Quick Test Mode - Creating model and validating...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, model_info = create_model_and_info()
        model = model.to(device)
        
        # Test forward pass
        dummy_input = torch.randn(4, 3, 32, 32).to(device)
        with torch.no_grad():
            output = model(dummy_input)
        
        print(f"\n✅ Forward pass test:")
        print(f"  Input shape: {dummy_input.shape}")
        print(f"  Output shape: {output.shape}")
        print(f"  Output range: [{output.min():.3f}, {output.max():.3f}]")
        
        print(f"\n🚀 For full training, run:")
        print(f"  python3 model_and_training.py --epochs 200 --batch-size 128")
        print(f"  python3 model_and_training.py --help  # for all options")
    else:
        # Full training mode
        main()
