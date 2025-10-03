"""
Training Script for Ultra-Efficient Models
==========================================

This script trains the three ultra-efficient models to achieve 99.4% accuracy
with <8000 parameters in ≤15 epochs.

Usage:
    python train_ultra_models.py --model Model_1 --epochs 15
    python train_ultra_models.py --model all --epochs 15
    python train_ultra_models.py --model Model_3 --epochs 10 --lr 0.01
"""

import argparse
import time
import json
from datetime import datetime
import os

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

class FocalLoss(nn.Module):
    """
    Focal Loss for addressing class imbalance and hard example mining
    
    Focal Loss = -α(1-pt)^γ * log(pt)
    
    Args:
        alpha (float): Weighting factor for rare class (default: 1.0)
        gamma (float): Focusing parameter (default: 2.0)
        reduction (str): Specifies the reduction to apply to the output
    """
    def __init__(self, alpha=1.0, gamma=2.0, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        # Compute cross entropy
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        
        # Compute p_t
        pt = torch.exp(-ce_loss)
        
        # Compute focal loss
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

class ModelTrainer:
    """Trainer class for ultra-efficient models with Focal Loss"""
    
    def __init__(self, model, model_name, device='cpu', use_focal_loss=True, focal_alpha=1.0, focal_gamma=2.0):
        self.model = model.to(device)
        self.model_name = model_name
        self.device = device
        self.best_accuracy = 0.0
        self.training_history = []
        
        # Setup loss function
        if use_focal_loss:
            self.criterion = FocalLoss(alpha=focal_alpha, gamma=focal_gamma)
            print(f"🎯 Using Focal Loss (α={focal_alpha}, γ={focal_gamma})")
        else:
            self.criterion = nn.CrossEntropyLoss()
            print("📊 Using Cross Entropy Loss")
        
    def prepare_data(self, batch_size=64, use_augmentation=True):
        """Prepare MNIST data loaders with optional data augmentation"""
        
        # Training transform with augmentation
        if use_augmentation:
            train_transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,)),  # MNIST mean and std
                transforms.RandomRotation(degrees=7),  # Light rotation
                transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),  # Light translation
            ])
            print("🔄 Using data augmentation (rotation + translation)")
        else:
            train_transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ])
            print("📊 No data augmentation")
        
        # Test transform (no augmentation)
        test_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        # Download and load training data
        train_dataset = torchvision.datasets.MNIST(
            root='./data', train=True, download=True, transform=train_transform
        )
        
        # Download and load test data
        test_dataset = torchvision.datasets.MNIST(
            root='./data', train=False, download=True, transform=test_transform
        )
        
        self.train_loader = DataLoader(
            train_dataset, batch_size=batch_size, shuffle=True, num_workers=2, pin_memory=True
        )
        
        self.test_loader = DataLoader(
            test_dataset, batch_size=1000, shuffle=False, num_workers=2, pin_memory=True
        )
        
        print(f"📊 Training samples: {len(train_dataset):,}")
        print(f"📊 Test samples: {len(test_dataset):,}")
        print(f"📊 Batch size: {batch_size}")
        
    def train_epoch(self, optimizer, epoch, scheduler=None):
        """Train for one epoch using Focal Loss"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(self.train_loader):
            data, target = data.to(self.device), target.to(self.device)
            
            optimizer.zero_grad()
            output = self.model(data)
            
            # Use the configured loss function (Focal Loss or Cross Entropy)
            loss = self.criterion(output, target)
            
            loss.backward()
            
            # Gradient clipping for stability
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
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
    
    def test(self):
        """Evaluate model on test set"""
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
    
    def train(self, epochs=15, lr=0.01, target_accuracy=99.4, optimizer_type='AdamW'):
        """Train the model with Focal Loss and advanced optimizers"""
        print(f"\n🚀 Training {self.model_name} with Focal Loss")
        print(f"Parameters: {self.model.count_parameters():,}")
        print(f"Target: {target_accuracy}% accuracy in ≤{epochs} epochs")
        print("-" * 60)
        
        # Setup optimizer based on model complexity
        if optimizer_type == 'AdamW':
            # AdamW with model-specific learning rates
            if self.model_name == "Model_1":
                optimizer = optim.AdamW(self.model.parameters(), lr=lr*0.8, weight_decay=1e-3)
            elif self.model_name == "Model_2":
                optimizer = optim.AdamW(self.model.parameters(), lr=lr*0.6, weight_decay=1e-3)
            else:  # Model_3
                optimizer = optim.AdamW(self.model.parameters(), lr=lr*0.4, weight_decay=1e-3)
            print(f"🔧 Using AdamW optimizer with adaptive LR")
        else:
            optimizer = optim.SGD(self.model.parameters(), lr=lr, momentum=0.9, weight_decay=1e-4)
            print(f"🔧 Using SGD optimizer")
        
        # Advanced learning rate scheduler
        scheduler = optim.lr_scheduler.OneCycleLR(
            optimizer, 
            max_lr=lr*2, 
            steps_per_epoch=len(self.train_loader), 
            epochs=epochs,
            pct_start=0.3,
            anneal_strategy='cos'
        )
        print(f"📈 Using OneCycleLR scheduler")
        
        start_time = time.time()
        target_reached = False
        
        for epoch in range(1, epochs + 1):
            current_lr = optimizer.param_groups[0]['lr']
            print(f"Epoch {epoch:2d}/{epochs} | LR={current_lr:.6f}")
            
            # Train
            train_loss, train_acc = self.train_epoch(optimizer, epoch, scheduler)
            
            # Test
            test_loss, test_acc = self.test()
            
            # Update learning rate (OneCycleLR steps per batch, not per epoch)
            # scheduler.step() is called inside train_epoch for OneCycleLR
            
            # Track best accuracy
            if test_acc > self.best_accuracy:
                self.best_accuracy = test_acc
                print(f"🎯 New best accuracy: {test_acc:.2f}%")
                
                # Save best model
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'accuracy': test_acc,
                    'loss': test_loss
                }, f'best_{self.model_name.lower()}.pth')
            
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
            print(f"Test  Loss={test_loss:.4f}, Acc={test_acc:.2f}%")
            
            # Check if target reached
            if test_acc >= target_accuracy and not target_reached:
                print(f"\n🎉 TARGET ACHIEVED! Test Accuracy: {test_acc:.2f}%")
                target_reached = True
                # Continue training to see if we can do better
            
            print()
        
        training_time = time.time() - start_time
        
        print(f"🏆 Training completed for {self.model_name}")
        print(f"⏱️  Training time: {training_time:.1f}s")
        print(f"🎯 Best accuracy: {self.best_accuracy:.2f}%")
        print(f"✅ Target {'ACHIEVED' if self.best_accuracy >= target_accuracy else 'NOT ACHIEVED'}")
        
        return {
            'model_name': self.model_name,
            'best_accuracy': self.best_accuracy,
            'training_time': training_time,
            'target_achieved': self.best_accuracy >= target_accuracy,
            'epochs_trained': epochs,
            'parameters': self.model.count_parameters(),
            'history': self.training_history
        }

def train_single_model(model_name, epochs=15, lr=0.01, batch_size=64, target_accuracy=99.4, 
                      use_focal_loss=True, focal_alpha=1.0, focal_gamma=2.0, use_augmentation=True):
    """Train a single model with Focal Loss"""
    print(f"\n{'='*60}")
    print(f"Training {model_name} with Advanced Configuration")
    print(f"{'='*60}")
    
    # Create model
    model = create_model(model_name)
    
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🖥️  Using device: {device}")
    
    # Create trainer with Focal Loss
    trainer = ModelTrainer(model, model_name, device, use_focal_loss, focal_alpha, focal_gamma)
    
    # Prepare data with augmentation
    trainer.prepare_data(batch_size, use_augmentation)
    
    # Train model
    results = trainer.train(epochs, lr, target_accuracy)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"results_{model_name.lower()}_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Results saved to: {results_file}")
    
    return results

def train_all_models(epochs=15, lr=0.01, batch_size=64):
    """Train all three models"""
    models = ['Model_1', 'Model_2', 'Model_3']
    all_results = []
    
    print("🚀 Training All Ultra-Efficient Models")
    print("=" * 60)
    print(f"Configuration: {epochs} epochs, LR={lr}, batch_size={batch_size}")
    print("Target: 99.4% accuracy with <8000 parameters")
    
    for model_name in models:
        try:
            results = train_single_model(model_name, epochs, lr, batch_size)
            all_results.append(results)
        except Exception as e:
            print(f"❌ Error training {model_name}: {str(e)}")
            continue
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TRAINING SUMMARY")
    print("=" * 60)
    
    print(f"{'Model':<10} {'Parameters':<12} {'Best Acc':<10} {'Time':<8} {'Target':<8}")
    print("-" * 60)
    
    for results in all_results:
        model_name = results['model_name']
        params = results['parameters']
        accuracy = results['best_accuracy']
        time_taken = results['training_time']
        target_met = "✅" if results['target_achieved'] else "❌"
        
        print(f"{model_name:<10} {params:<12,} {accuracy:<10.2f}% {time_taken:<8.1f}s {target_met:<8}")
    
    # Save combined results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_file = f"all_results_{timestamp}.json"
    
    with open(combined_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n📁 Combined results saved to: {combined_file}")
    
    return all_results

def main():
    """Main training function with Focal Loss support"""
    parser = argparse.ArgumentParser(description='Train Ultra-Efficient MNIST Models with Focal Loss')
    parser.add_argument('--model', type=str, default='all', 
                       choices=['Model_1', 'Model_2', 'Model_3', 'all'],
                       help='Model to train (default: all)')
    parser.add_argument('--epochs', type=int, default=15,
                       help='Number of epochs (default: 15)')
    parser.add_argument('--lr', type=float, default=0.01,
                       help='Learning rate (default: 0.01)')
    parser.add_argument('--batch-size', type=int, default=64,
                       help='Batch size (default: 64)')
    parser.add_argument('--target', type=float, default=99.4,
                       help='Target accuracy (default: 99.4)')
    parser.add_argument('--focal-alpha', type=float, default=1.0,
                       help='Focal Loss alpha parameter (default: 1.0)')
    parser.add_argument('--focal-gamma', type=float, default=2.0,
                       help='Focal Loss gamma parameter (default: 2.0)')
    parser.add_argument('--no-focal', action='store_true',
                       help='Disable Focal Loss (use Cross Entropy instead)')
    parser.add_argument('--no-augmentation', action='store_true',
                       help='Disable data augmentation')
    
    args = parser.parse_args()
    
    if not TORCH_AVAILABLE:
        print("❌ PyTorch not available. Please install PyTorch first.")
        return
    
    use_focal_loss = not args.no_focal
    use_augmentation = not args.no_augmentation
    
    print("🎯 Ultra-Efficient MNIST Models Training with Focal Loss")
    print(f"Configuration: {args.epochs} epochs, LR={args.lr}, batch={args.batch_size}")
    print(f"Target: {args.target}% accuracy with <8000 parameters")
    print(f"Focal Loss: {'Enabled' if use_focal_loss else 'Disabled'} (α={args.focal_alpha}, γ={args.focal_gamma})")
    print(f"Data Augmentation: {'Enabled' if use_augmentation else 'Disabled'}")
    
    if args.model == 'all':
        train_all_models(args.epochs, args.lr, args.batch_size)
    else:
        train_single_model(args.model, args.epochs, args.lr, args.batch_size, args.target,
                          use_focal_loss, args.focal_alpha, args.focal_gamma, use_augmentation)

if __name__ == "__main__":
    main()