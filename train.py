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

# Import our models with error handling
try:
    from model1 import create_model_1, analyze_model_1
    print("✅ Model 1 imported successfully")
except ImportError as e:
    print(f"❌ Model 1 import failed: {e}")
    
try:
    from model2 import create_model_2, analyze_model_2
    print("✅ Model 2 imported successfully")
except ImportError as e:
    print(f"❌ Model 2 import failed: {e}")
    
try:
    from model3 import create_model_3, analyze_model_3
    print("✅ Model 3 imported successfully")
except ImportError as e:
    print(f"❌ Model 3 import failed: {e}")
    # Fallback - check what's actually available
    try:
        import model3
        available_funcs = [name for name in dir(model3) if name.startswith('create_') or name.startswith('analyze_')]
        print(f"   Available functions in model3: {available_funcs}")
    except:
        print("   Cannot import model3 module at all")
        
try:
    from model4 import create_model_4, analyze_model_4
    print("✅ Model 4 imported successfully")
except ImportError as e:
    print(f"❌ Model 4 import failed: {e}")
    
try:
    from model5 import create_model_5, analyze_model_5
    print("✅ Model 5 imported successfully")
except ImportError as e:
    print(f"❌ Model 5 import failed: {e}")
    
try:
    from model6 import create_model_6, analyze_model_6
    print("✅ Model 6 imported successfully")
except ImportError as e:
    print(f"❌ Model 6 import failed: {e}")
    
try:
    from model7 import create_model_7, analyze_model_7
    print("✅ Model 7 imported successfully")
except ImportError as e:
    print(f"❌ Model 7 import failed: {e}")


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
        """Train model for one epoch following curriculum approach."""
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
        
        # Code 10 - Learning Rate Scheduling: Curriculum-aligned approach
        optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
        
        # MultiStepLR scheduler following curriculum (Code 10)
        scheduler = optim.lr_scheduler.MultiStepLR(
            optimizer, milestones=[6, 10, 13], gamma=0.1
        )
        print(f"📊 Using MultiStepLR scheduler: milestones=[6,10,13], gamma=0.1 (Code 10)")
        criterion = nn.CrossEntropyLoss()
        
        # Training tracking
        train_losses, train_accs = [], []
        test_losses, test_accs = [], []
        best_accuracy = 0
        consistent_target = 99.4
        
        start_time = time.time()
        
        for epoch in range(1, epochs + 1):
            epoch_start = time.time()
            
            # Training with curriculum approach
            train_loss, train_acc = self.train_epoch(
                model, train_loader, optimizer, criterion, epoch
            )
            
            # Testing
            test_loss, test_acc = self.test_model(model, test_loader, criterion)
            
            # Code 10: Scheduler step per epoch (MultiStepLR)
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
        """Train all models and compare results."""
        print("🚀 SESSION 6 - TRAINING ALL MODELS")
        print("="*60)
        
        # Create models with error handling
        models = {}
        
        # Model 1
        try:
            models['Model_1'] = create_model_1()
            print("✅ Model_1 created successfully")
        except Exception as e:
            print(f"❌ Model_1 creation failed: {e}")
            
        # Model 2
        try:
            models['Model_2'] = create_model_2()
            print("✅ Model_2 created successfully")
        except Exception as e:
            print(f"❌ Model_2 creation failed: {e}")
            
        # Model 3
        try:
            models['Model_3'] = create_model_3()
            print("✅ Model_3 created successfully")
        except Exception as e:
            print(f"❌ Model_3 creation failed: {e}")
            
        # Model 4
        try:
            models['Model_4'] = create_model_4()
            print("✅ Model_4 created successfully")
        except Exception as e:
            print(f"❌ Model_4 creation failed: {e}")
            
        # Model 5
        try:
            models['Model_5'] = create_model_5()
            print("✅ Model_5 created successfully")
        except Exception as e:
            print(f"❌ Model_5 creation failed: {e}")
            
        # Model 6
        try:
            models['Model_6'] = create_model_6()
            print("✅ Model_6 created successfully")
        except Exception as e:
            print(f"❌ Model_6 creation failed: {e}")
            
        # Model 7
        try:
            models['Model_7'] = create_model_7()
            print("✅ Model_7 created successfully")
        except Exception as e:
            print(f"❌ Model_7 creation failed: {e}")
        
        print(f"\n📊 Successfully created {len(models)}/7 models")
        
        all_results = {}
        
        for model_name, model in models.items():
            # Analyze model before training with error handling
            analysis = None
            try:
                if model_name == 'Model_1':
                    analysis = analyze_model_1()
                elif model_name == 'Model_2':
                    analysis = analyze_model_2()
                elif model_name == 'Model_3':
                    analysis = analyze_model_3()
                elif model_name == 'Model_4':
                    analysis = analyze_model_4()
                elif model_name == 'Model_5':
                    analysis = analyze_model_5()
                elif model_name == 'Model_6':
                    analysis = analyze_model_6()
                elif model_name == 'Model_7':
                    analysis = analyze_model_7()
                    
                print(f"✅ {model_name} analysis completed")
                    
            except Exception as e:
                print(f"❌ {model_name} analysis failed: {e}")
                # Create minimal analysis fallback
                analysis = {
                    'total_parameters': model.count_parameters() if hasattr(model, 'count_parameters') else 0,
                    'target_accuracy': 'Unknown',
                    'architecture_efficiency': 'Analysis failed'
                }
                
            if analysis is None:
                print(f"⚠️  Skipping {model_name} - no analysis available")
                continue
            
            print(f"\n📊 PRE-TRAINING ANALYSIS - {model_name}")
            print(f"Parameters: {analysis['total_parameters']:,}")
            print(f"Target Accuracy: {analysis['target_accuracy']}")
            print(f"Strategy: {analysis['architecture_efficiency']}")
            
            # Validate 8,000 parameter constraint before training
            if analysis['total_parameters'] >= 8000:
                print(f"❌ PARAMETER LIMIT EXCEEDED: {analysis['total_parameters']:,} >= 8,000")
                print(f"   Skipping {model_name} - exceeds limit by {analysis['total_parameters'] - 8000:,} parameters")
                continue
            else:
                print(f"✅ Parameter constraint satisfied: {8000 - analysis['total_parameters']:,} under limit")
            
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
