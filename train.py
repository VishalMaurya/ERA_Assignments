"""
SESSION 6 - TRAINING SCRIPT
===========================

Modular training script for all three models with comprehensive logging and analysis.

TRAINING STRATEGY:
- Model 1: Ultra-lightweight baseline (~3-4k params)
- Model 2: Optimized efficiency (~6-7k params)  
- Model 3: Final precision (<8k params)
- Target: 99.4% consistently in final epochs with ≤15 epochs
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import argparse
import time
from datetime import datetime
import json
import os

# Import our models
from model1 import create_model_1, analyze_model_1
from model2 import create_model_2, analyze_model_2
from model3 import create_model_3, analyze_model_3


class TrainingManager:
    """
    Comprehensive training manager for Session 6 models.
    """
    
    def __init__(self, device='auto'):
        self.device = self._get_device(device)
        self.results = {}
        
    def _get_device(self, device):
        """Get optimal device for training."""
        if device == 'auto':
            if torch.cuda.is_available():
                device = 'cuda'
                print(f"Using GPU: {torch.cuda.get_device_name(0)}")
            else:
                device = 'cpu'
                print("Using CPU")
        return torch.device(device)
    
    def get_data_loaders(self, batch_size=128, test_batch_size=1000, use_augmentation=True):
        """
        Create optimized MNIST data loaders with augmentation.
        
        Args:
            batch_size: Training batch size (increased for efficiency)
            test_batch_size: Testing batch size
            use_augmentation: Whether to apply data augmentation (Code 9)
            
        Returns:
            tuple: (train_loader, test_loader)
        """
        # Code 9 - Image Augmentation: Adding rotations for better generalization
        if use_augmentation:
            transform_train = transforms.Compose([
                transforms.RandomRotation(degrees=7),  # Small rotations for MNIST
                transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),  # Small translations
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ])
            print("📈 Using data augmentation: rotations ±7° and translations ±10%")
        else:
            transform_train = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ])
            print("📊 Using basic transforms (no augmentation)")
        
        # Test transform (no augmentation)
        transform_test = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        train_dataset = datasets.MNIST(
            './data', train=True, download=True, transform=transform_train
        )
        test_dataset = datasets.MNIST(
            './data', train=False, download=True, transform=transform_test
        )
        
        train_loader = DataLoader(
            train_dataset, batch_size=batch_size, shuffle=True,
            num_workers=2, pin_memory=True if self.device.type == 'cuda' else False
        )
        
        test_loader = DataLoader(
            test_dataset, batch_size=test_batch_size, shuffle=False,
            num_workers=2, pin_memory=True if self.device.type == 'cuda' else False
        )
        
        return train_loader, test_loader
    
    def train_epoch(self, model, train_loader, optimizer, criterion, epoch):
        """Train model for one epoch."""
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(self.device), target.to(self.device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()
            total += target.size(0)
            
            if batch_idx % 100 == 0:
                print(f'Epoch {epoch}, Batch {batch_idx}/{len(train_loader)}, '
                      f'Loss: {loss.item():.4f}, Acc: {100.*correct/total:.2f}%')
        
        return running_loss / len(train_loader), 100. * correct / total
    
    def test_model(self, model, test_loader, criterion):
        """Evaluate model on test set."""
        model.eval()
        test_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = model(data)
                test_loss += criterion(output, target).item()
                pred = output.argmax(dim=1)
                correct += pred.eq(target).sum().item()
                total += target.size(0)
        
        test_loss /= len(test_loader)
        accuracy = 100. * correct / total
        
        return test_loss, accuracy
    
    def train_model(self, model_name, model, epochs=15, lr=0.01):
        """
        Complete training pipeline for a model.
        
        Args:
            model_name: Name of the model for logging
            model: Model instance
            epochs: Maximum number of epochs
            lr: Learning rate
            
        Returns:
            dict: Training results and analysis
        """
        print(f"\n{'='*60}")
        print(f"TRAINING {model_name.upper()}")
        print(f"{'='*60}")
        
        # Setup
        model = model.to(self.device)
        train_loader, test_loader = self.get_data_loaders()
        
        # Code 10 - Playing Naively with Learning Rates: Advanced LR scheduling
        optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
        
        # Multi-step scheduler for better convergence
        scheduler = optim.lr_scheduler.MultiStepLR(
            optimizer, milestones=[6, 10, 13], gamma=0.5
        )
        print(f"📊 Using MultiStepLR scheduler: milestones=[6,10,13], gamma=0.5")
        criterion = nn.CrossEntropyLoss()
        
        # Training tracking
        train_losses, train_accs = [], []
        test_losses, test_accs = [], []
        best_accuracy = 0
        consistent_target = 99.4
        
        start_time = time.time()
        
        for epoch in range(1, epochs + 1):
            epoch_start = time.time()
            
            # Training
            train_loss, train_acc = self.train_epoch(
                model, train_loader, optimizer, criterion, epoch
            )
            
            # Testing
            test_loss, test_acc = self.test_model(model, test_loader, criterion)
            
            # Scheduler step
            scheduler.step()
            current_lr = optimizer.param_groups[0]['lr']
            
            # Record metrics
            train_losses.append(train_loss)
            train_accs.append(train_acc)
            test_losses.append(test_loss)
            test_accs.append(test_acc)
            
            epoch_time = time.time() - epoch_start
            
            # Logging
            print(f"Epoch {epoch:2d}/{epochs} | Time: {epoch_time:.1f}s | LR: {current_lr:.6f}")
            print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
            print(f"Test  Loss: {test_loss:.4f} | Test  Acc: {test_acc:.2f}%")
            
            if test_acc > best_accuracy:
                best_accuracy = test_acc
                print(f"🎯 New best accuracy: {best_accuracy:.2f}%")
            
            # Check consistency in final epochs
            if epoch >= epochs - 4:  # Last 5 epochs
                if test_acc >= consistent_target:
                    print(f"✅ Consistent target achieved: {test_acc:.2f}% >= {consistent_target}%")
                else:
                    print(f"⚠️  Below target: {test_acc:.2f}% < {consistent_target}%")
            
            print("-" * 60)
        
        total_time = time.time() - start_time
        
        # Analyze final performance
        final_epochs = test_accs[-5:] if len(test_accs) >= 5 else test_accs[-3:]
        avg_final_accuracy = sum(final_epochs) / len(final_epochs)
        consistency_achieved = all(acc >= consistent_target for acc in final_epochs)
        
        # Compile results
        results = {
            'model_name': model_name,
            'parameters': model.count_parameters(),
            'best_accuracy': best_accuracy,
            'final_epochs_avg': avg_final_accuracy,
            'final_epochs': final_epochs,
            'consistency_achieved': consistency_achieved,
            'total_time': total_time,
            'epochs_trained': epochs,
            'train_accuracies': train_accs,
            'test_accuracies': test_accs,
            'train_losses': train_losses,
            'test_losses': test_losses
        }
        
        print(f"\n🏆 FINAL RESULTS for {model_name}:")
        print(f"   Parameters: {results['parameters']:,}")
        print(f"   Best Accuracy: {results['best_accuracy']:.2f}%")
        print(f"   Final {len(final_epochs)} Epochs Avg: {avg_final_accuracy:.2f}%")
        print(f"   Consistency Target: {'✅ ACHIEVED' if consistency_achieved else '❌ NOT ACHIEVED'}")
        print(f"   Training Time: {total_time:.1f}s")
        
        return results
    
    def train_all_models(self, epochs=15):
        """Train all three models and compare results."""
        print("🚀 SESSION 6 - TRAINING ALL MODELS")
        print("="*60)
        
        models = {
            'Model_1': create_model_1(),
            'Model_2': create_model_2(),
            'Model_3': create_model_3()
        }
        
        all_results = {}
        
        for model_name, model in models.items():
            # Analyze model before training
            if model_name == 'Model_1':
                analysis = analyze_model_1()
            elif model_name == 'Model_2':
                analysis = analyze_model_2()
            else:
                analysis = analyze_model_3()
            
            print(f"\n📊 PRE-TRAINING ANALYSIS - {model_name}")
            print(f"Parameters: {analysis['total_parameters']:,}")
            print(f"Target Accuracy: {analysis['target_accuracy']}")
            print(f"Strategy: {analysis['architecture_efficiency']}")
            
            # Train model
            results = self.train_model(model_name, model, epochs)
            results['analysis'] = analysis
            all_results[model_name] = results
        
        # Final comparison
        self._generate_final_report(all_results)
        
        return all_results
    
    def _generate_final_report(self, all_results):
        """Generate comprehensive final report."""
        print("\n" + "="*80)
        print("📊 SESSION 6 - FINAL COMPARISON REPORT")
        print("="*80)
        
        # Summary table
        print(f"{'Model':<12} {'Params':<8} {'Best Acc':<10} {'Final Avg':<10} {'Target':<8} {'Time':<8}")
        print("-" * 70)
        
        for model_name, results in all_results.items():
            target_met = "✅" if results['consistency_achieved'] else "❌"
            print(f"{model_name:<12} {results['parameters']:<8,} "
                  f"{results['best_accuracy']:<10.2f} {results['final_epochs_avg']:<10.2f} "
                  f"{target_met:<8} {results['total_time']:<8.1f}")
        
        # Detailed analysis
        print(f"\n🎯 TARGET ACHIEVEMENT ANALYSIS:")
        for model_name, results in all_results.items():
            print(f"\n{model_name}:")
            print(f"  Final 5 Epochs: {[f'{acc:.2f}%' for acc in results['final_epochs']]}")
            print(f"  Consistency: {'✅ ACHIEVED' if results['consistency_achieved'] else '❌ FAILED'}")
            if results['parameters'] >= 8000:
                print(f"  ⚠️  Parameter Limit: {results['parameters']:,} >= 8000 (EXCEEDED)")
            else:
                print(f"  ✅ Parameter Limit: {results['parameters']:,} < 8000")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"session6_results_{timestamp}.json"
        
        # Convert numpy arrays to lists for JSON serialization
        json_results = {}
        for model_name, results in all_results.items():
            json_results[model_name] = {
                key: value.tolist() if hasattr(value, 'tolist') else value
                for key, value in results.items()
            }
        
        with open(results_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")


def main():
    """Main training execution."""
    parser = argparse.ArgumentParser(description='Session 6 - CNN Training')
    parser.add_argument('--model', type=str, choices=['1', '2', '3', 'all'], default='all',
                        help='Model to train (default: all)')
    parser.add_argument('--epochs', type=int, default=15,
                        help='Number of epochs (default: 15)')
    parser.add_argument('--device', type=str, default='auto',
                        help='Device to use (default: auto)')
    
    args = parser.parse_args()
    
    # Initialize training manager
    trainer = TrainingManager(device=args.device)
    
    if args.model == 'all':
        # Train all models
        all_results = trainer.train_all_models(epochs=args.epochs)
    else:
        # Train specific model
        if args.model == '1':
            model = create_model_1()
            model_name = 'Model_1'
        elif args.model == '2':
            model = create_model_2()
            model_name = 'Model_2'
        elif args.model == '3':
            model = create_model_3()
            model_name = 'Model_3'
        
        results = trainer.train_model(model_name, model, epochs=args.epochs)
        print(f"\nTraining completed for {model_name}")


if __name__ == "__main__":
    main()
