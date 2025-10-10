"""
ResNet CIFAR-100 Training Script
================================

Train ResNet models from scratch on CIFAR-100 dataset.
Target: 73% top-1 accuracy in ~100 epochs.

Usage:
    python train.py --model resnet18 --epochs 100 --batch-size 128
"""

import torch
import torch.nn as nn
import torch.optim as optim
import argparse
import os
import json
import time
from datetime import datetime
from tqdm import tqdm

from resnet_model import resnet18, resnet34, resnet50, get_model_info
from data_utils import get_cifar100_loaders
from utils import (
    train_epoch, evaluate, save_checkpoint, 
    plot_training_history, setup_logging
)


def parse_args():
    parser = argparse.ArgumentParser(description='Train ResNet on CIFAR-100')
    
    # Model configuration
    parser.add_argument('--model', type=str, default='resnet18',
                       choices=['resnet18', 'resnet34', 'resnet50'],
                       help='Model architecture')
    
    # Training configuration
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=128,
                       help='Batch size for training')
    parser.add_argument('--lr', type=float, default=0.1,
                       help='Initial learning rate')
    parser.add_argument('--momentum', type=float, default=0.9,
                       help='SGD momentum')
    parser.add_argument('--weight-decay', type=float, default=5e-4,
                       help='Weight decay')
    parser.add_argument('--label-smoothing', type=float, default=0.1,
                       help='Label smoothing')
    
    # Learning rate scheduler
    parser.add_argument('--scheduler', type=str, default='cosine',
                       choices=['cosine', 'step', 'multistep'],
                       help='Learning rate scheduler')
    
    # Data configuration
    parser.add_argument('--num-workers', type=int, default=4,
                       help='Number of data loading workers')
    parser.add_argument('--data-dir', type=str, default='./data',
                       help='Directory for dataset')
    
    # Checkpointing
    parser.add_argument('--save-dir', type=str, default='checkpoints',
                       help='Directory to save checkpoints')
    parser.add_argument('--log-dir', type=str, default='logs',
                       help='Directory to save logs')
    parser.add_argument('--save-freq', type=int, default=10,
                       help='Save checkpoint every N epochs')
    
    # Target
    parser.add_argument('--target-accuracy', type=float, default=73.0,
                       help='Target accuracy to achieve')
    
    # Device
    parser.add_argument('--device', type=str, default='cuda',
                       help='Device to use for training')
    
    # Resume
    parser.add_argument('--resume', type=str, default=None,
                       help='Path to checkpoint to resume from')
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    # Setup directories and logging
    os.makedirs(args.save_dir, exist_ok=True)
    os.makedirs(args.log_dir, exist_ok=True)
    logger = setup_logging(args.log_dir)
    
    # Device configuration
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")
    if torch.cuda.is_available():
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Data loaders
    logger.info("Preparing data loaders...")
    train_loader, test_loader, class_names = get_cifar100_loaders(
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        data_dir=args.data_dir
    )
    
    # Create model
    logger.info(f"Creating {args.model} model...")
    if args.model == 'resnet18':
        model = resnet18(num_classes=100)
    elif args.model == 'resnet34':
        model = resnet34(num_classes=100)
    elif args.model == 'resnet50':
        model = resnet50(num_classes=100)
    
    model = model.to(device)
    model_info = get_model_info(model)
    logger.info(f"Total parameters: {model_info['total_parameters']:,}")
    logger.info(f"Model size: {model_info['model_size_mb']:.2f} MB")
    
    # Loss function
    criterion = nn.CrossEntropyLoss(label_smoothing=args.label_smoothing)
    
    # Optimizer
    optimizer = optim.SGD(
        model.parameters(),
        lr=args.lr,
        momentum=args.momentum,
        weight_decay=args.weight_decay,
        nesterov=True
    )
    
    # Learning rate scheduler
    if args.scheduler == 'cosine':
        scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer, T_0=10, T_mult=2, eta_min=1e-6
        )
    elif args.scheduler == 'step':
        scheduler = optim.lr_scheduler.StepLR(
            optimizer, step_size=30, gamma=0.1
        )
    elif args.scheduler == 'multistep':
        scheduler = optim.lr_scheduler.MultiStepLR(
            optimizer, milestones=[60, 80, 90], gamma=0.1
        )
    
    # Resume from checkpoint if specified
    start_epoch = 1
    best_acc = 0.0
    history = {
        'train_loss': [],
        'train_acc': [],
        'test_loss': [],
        'test_acc': [],
        'lr': []
    }
    
    if args.resume:
        logger.info(f"Resuming from checkpoint: {args.resume}")
        checkpoint = torch.load(args.resume)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch'] + 1
        best_acc = checkpoint.get('best_accuracy', 0.0)
        if 'history' in checkpoint:
            history = checkpoint['history']
        logger.info(f"Resumed from epoch {start_epoch-1}, best accuracy: {best_acc:.2f}%")
    
    # Training configuration summary
    logger.info(f"\n{'='*60}")
    logger.info("Training Configuration")
    logger.info(f"{'='*60}")
    logger.info(f"Model: {args.model}")
    logger.info(f"Epochs: {args.epochs}")
    logger.info(f"Batch size: {args.batch_size}")
    logger.info(f"Learning rate: {args.lr}")
    logger.info(f"Optimizer: SGD (momentum={args.momentum}, weight_decay={args.weight_decay})")
    logger.info(f"Scheduler: {args.scheduler}")
    logger.info(f"Label smoothing: {args.label_smoothing}")
    logger.info(f"Target accuracy: {args.target_accuracy}%")
    logger.info(f"{'='*60}\n")
    
    # Training loop
    logger.info(f"🚀 Starting training for {args.epochs} epochs...\n")
    start_time = time.time()
    
    for epoch in range(start_epoch, args.epochs + 1):
        # Train
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device, epoch, logger
        )
        
        # Evaluate
        test_loss, test_acc = evaluate(
            model, test_loader, criterion, device, logger
        )
        
        # Update learning rate
        scheduler.step()
        current_lr = optimizer.param_groups[0]['lr']
        
        # Save history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['test_loss'].append(test_loss)
        history['test_acc'].append(test_acc)
        history['lr'].append(current_lr)
        
        # Log epoch summary
        logger.info(f"\nEpoch {epoch}/{args.epochs}")
        logger.info(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        logger.info(f"Test Loss: {test_loss:.4f} | Test Acc: {test_acc:.2f}%")
        logger.info(f"Learning Rate: {current_lr:.6f}")
        
        # Save best model
        if test_acc > best_acc:
            best_acc = test_acc
            save_checkpoint(
                model, optimizer, epoch, test_acc, history,
                os.path.join(args.save_dir, 'best_model.pth')
            )
            logger.info(f"✨ New best accuracy: {best_acc:.2f}%")
        
        # Check if target reached
        if test_acc >= args.target_accuracy:
            logger.info(f"\n🎉 Target accuracy {args.target_accuracy}% reached!")
            save_checkpoint(
                model, optimizer, epoch, test_acc, history,
                os.path.join(args.save_dir, f'target_model_epoch_{epoch}.pth')
            )
        
        # Save checkpoint periodically
        if epoch % args.save_freq == 0:
            save_checkpoint(
                model, optimizer, epoch, test_acc, history,
                os.path.join(args.save_dir, f'checkpoint_epoch_{epoch}.pth')
            )
        
        logger.info(f"{'-'*60}\n")
    
    # Training complete
    training_time = time.time() - start_time
    logger.info(f"\n{'='*60}")
    logger.info("Training Complete!")
    logger.info(f"{'='*60}")
    logger.info(f"Total training time: {training_time/3600:.2f} hours")
    logger.info(f"Best test accuracy: {best_acc:.2f}%")
    logger.info(f"Target accuracy ({args.target_accuracy}%): {'✅ REACHED' if best_acc >= args.target_accuracy else '❌ NOT REACHED'}")
    logger.info(f"{'='*60}\n")
    
    # Save final results
    results = {
        'model': args.model,
        'epochs': args.epochs,
        'best_accuracy': float(best_acc),
        'training_time_hours': training_time / 3600,
        'target_reached': best_acc >= args.target_accuracy,
        'history': history,
        'config': vars(args),
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S')
    }
    
    with open(os.path.join(args.log_dir, 'training_results.json'), 'w') as f:
        json.dump(results, f, indent=4)
    
    # Plot training curves
    plot_training_history(history, args.target_accuracy, args.log_dir)
    
    logger.info("✅ Training results saved!")
    logger.info(f"📊 Plots saved to: {args.log_dir}")
    logger.info(f"💾 Checkpoints saved to: {args.save_dir}")


if __name__ == "__main__":
    main()

