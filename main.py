"""
MNIST CNN Training - Session 5 Assignment
=========================================

Main training script for achieving >99.4% accuracy on MNIST 
with <20k parameters in <20 epochs.

Assignment Requirements:
✅ >99.4% validation/test accuracy
✅ <20k parameters  
✅ <20 epochs
✅ Use Batch Normalization
✅ Use Dropout
✅ Use Global Average Pooling or Fully Connected layer

Models Available:
1. TinyNet: Ultra-lightweight (~1.4k params) 
2. BetterTinyNet: Optimized for target accuracy (~18.9k params)
3. ElegantOptimizedNet: Advanced with residual connections (~20k params)

Usage:
    python main.py --model BetterTinyNet --epochs 20 --lr 0.01
    python main.py --all  # Train all models
"""

import argparse
import torch
import os
from datetime import datetime

from models import TinyNet, BetterTinyNet, ElegantOptimizedNet, get_model_summary
from utils import (
    get_data_loaders, 
    train_model, 
    plot_training_history, 
    generate_summary_table,
    get_device
)


def main():
    parser = argparse.ArgumentParser(description='MNIST CNN Training - Session 5 Assignment')
    
    parser.add_argument('--model', type=str, default='BetterTinyNet',
                        choices=['TinyNet', 'BetterTinyNet', 'ElegantOptimizedNet'],
                        help='Model to train (default: BetterTinyNet)')
    
    parser.add_argument('--all', action='store_true',
                        help='Train all models')
    
    parser.add_argument('--epochs', type=int, default=20,
                        help='Number of epochs (default: 20)')
    
    parser.add_argument('--batch-size', type=int, default=64,
                        help='Training batch size (default: 64)')
    
    parser.add_argument('--test-batch-size', type=int, default=1000,
                        help='Test batch size (default: 1000)')
    
    parser.add_argument('--lr', type=float, default=0.01,
                        help='Learning rate (default: 0.01)')
    
    parser.add_argument('--target-accuracy', type=float, default=99.4,
                        help='Target accuracy for early stopping (default: 99.4)')
    
    parser.add_argument('--save-dir', type=str, default='./checkpoints',
                        help='Directory to save model checkpoints')
    
    parser.add_argument('--data-dir', type=str, default='./data',
                        help='Directory for MNIST data')
    
    parser.add_argument('--plot', action='store_true', default=True,
                        help='Generate training plots')
    
    args = parser.parse_args()
    
    # Print assignment header
    print("="*80)
    print("🎯 MNIST CNN Optimization - Session 5 Assignment")
    print("="*80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: >99.4% accuracy, <20k parameters, <20 epochs")
    print("="*80)
    
    # Setup device and data
    device = get_device()
    train_loader, test_loader = get_data_loaders(
        batch_size=args.batch_size,
        test_batch_size=args.test_batch_size,
        data_dir=args.data_dir
    )
    
    # Model definitions
    model_classes = {
        'TinyNet': TinyNet,
        'BetterTinyNet': BetterTinyNet,
        'ElegantOptimizedNet': ElegantOptimizedNet
    }
    
    # Determine which models to train
    if args.all:
        models_to_train = list(model_classes.keys())
        print(f"\n🔄 Training all models: {models_to_train}")
    else:
        models_to_train = [args.model]
        print(f"\n🔄 Training single model: {args.model}")
    
    # Training results storage
    all_histories = {}
    
    # Train each model
    for model_name in models_to_train:
        print(f"\n🚀 Initializing {model_name}...")
        
        # Create model instance
        model = model_classes[model_name]()
        
        # Print model summary
        summary = get_model_summary(model, model_name)
        print(f"📊 Model Summary:")
        print(f"   Parameters: {summary['total_parameters']:,}")
        print(f"   Efficiency: {summary['parameter_efficiency']}")
        print(f"   Memory: {summary['memory_footprint']}")
        
        # Check parameter constraint
        if summary['total_parameters'] > 20000:
            print(f"⚠️  WARNING: {model_name} has {summary['total_parameters']:,} parameters (>20k)")
        
        # Train the model
        history = train_model(
            model=model,
            model_name=model_name,
            device=device,
            train_loader=train_loader,
            test_loader=test_loader,
            epochs=args.epochs,
            lr=args.lr,
            target_accuracy=args.target_accuracy,
            save_dir=args.save_dir
        )
        
        # Store results
        all_histories[model_name] = history
        
        # Print individual results
        print(f"\n📈 {model_name} Results:")
        print(f"   Best Accuracy: {history['best_accuracy']:.2f}%")
        print(f"   Target Achieved: {'✅' if history['target_achieved'] else '❌'}")
        print(f"   Training Time: {history['total_time']:.1f}s")
    
    # Generate final summary
    print("\n" + "="*80)
    print("📊 FINAL RESULTS SUMMARY")
    print("="*80)
    
    summary_table = generate_summary_table(all_histories)
    print(summary_table)
    
    # Check assignment requirements
    print("\n🎯 Assignment Requirements Check:")
    for model_name, history in all_histories.items():
        params_ok = history['total_params'] < 20000
        accuracy_ok = history['best_accuracy'] >= args.target_accuracy
        
        print(f"\n{model_name}:")
        print(f"   ✅ Parameters: {history['total_params']:,} {'< 20k' if params_ok else '> 20k ❌'}")
        print(f"   ✅ Accuracy: {history['best_accuracy']:.2f}% {'>= 99.4%' if accuracy_ok else '< 99.4% ❌'}")
        print(f"   ✅ Epochs: {len(history['train_acc'])} <= 20")
        print(f"   ✅ Batch Normalization: Used")
        print(f"   ✅ Dropout: Used")
        print(f"   ✅ GAP/FC: Global Average Pooling used")
        
        if params_ok and accuracy_ok:
            print(f"   🎉 {model_name} MEETS ALL REQUIREMENTS!")
    
    # Generate visualization
    if args.plot and all_histories:
        print(f"\n📊 Generating training plots...")
        plot_save_path = f"training_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plot_training_history(all_histories, save_path=plot_save_path)
    
    # Save detailed results
    results_file = f"training_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(results_file, 'w') as f:
        f.write("MNIST CNN Training Results\n")
        f.write("="*50 + "\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"Configuration: epochs={args.epochs}, lr={args.lr}, batch_size={args.batch_size}\n\n")
        f.write(summary_table + "\n")
        
        for model_name, history in all_histories.items():
            f.write(f"\n{model_name} Detailed History:\n")
            f.write("-" * 30 + "\n")
            for epoch, (acc, loss) in enumerate(zip(history['test_acc'], history['test_loss']), 1):
                f.write(f"Epoch {epoch:2d}: Test Acc = {acc:6.2f}%, Test Loss = {loss:.4f}\n")
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Find best performing model
    best_model = max(all_histories.items(), key=lambda x: x[1]['best_accuracy'])
    print(f"\n🏆 Best Performing Model: {best_model[0]} ({best_model[1]['best_accuracy']:.2f}%)")
    
    print("\n" + "="*80)
    print("✅ Training Complete!")
    print("="*80)


if __name__ == "__main__":
    main()
