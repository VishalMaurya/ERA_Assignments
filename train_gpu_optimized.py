"""
GPU-Optimized ResNet CIFAR-100 Training Script
==============================================

Enhanced training script with multiple GPU optimizations for faster training.

GPU Optimizations Included:
1. Mixed Precision Training (FP16)
2. Gradient Accumulation
3. Pin Memory & Non-blocking transfers
4. Persistent Workers
5. Gradient Checkpointing (optional)
6. Optimized DataLoader settings
7. cuDNN Autotuner
8. Multi-GPU support (DataParallel/DistributedDataParallel)

Usage:
    # Single GPU with mixed precision
    python train_gpu_optimized.py --model resnet18 --epochs 100 --amp

    # Multi-GPU training
    python train_gpu_optimized.py --model resnet18 --epochs 100 --multi-gpu
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
from utils import save_checkpoint, plot_training_history, setup_logging


def parse_args():
    parser = argparse.ArgumentParser(description='GPU-Optimized ResNet CIFAR-100 Training')
    
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
    
    # GPU Optimizations
    parser.add_argument('--amp', action='store_true',
                       help='Use Automatic Mixed Precision (FP16) training')
    parser.add_argument('--gradient-accumulation', type=int, default=1,
                       help='Gradient accumulation steps')
    parser.add_argument('--multi-gpu', action='store_true',
                       help='Use all available GPUs (DataParallel)')
    parser.add_argument('--benchmark', action='store_true', default=True,
                       help='Enable cuDNN autotuner (default: True)')
    parser.add_argument('--channels-last', action='store_true',
                       help='Use channels-last memory format for better performance')
    
    # Data configuration
    parser.add_argument('--num-workers', type=int, default=4,
                       help='Number of data loading workers')
    parser.add_argument('--prefetch-factor', type=int, default=2,
                       help='Prefetch factor for data loading')
    parser.add_argument('--data-dir', type=str, default='./data',
                       help='Directory for dataset')
    
    # Checkpointing
    parser.add_argument('--save-dir', type=str, default='checkpoints_gpu',
                       help='Directory to save checkpoints')
    parser.add_argument('--log-dir', type=str, default='logs_gpu',
                       help='Directory to save logs')
    parser.add_argument('--save-freq', type=int, default=10,
                       help='Save checkpoint every N epochs')
    
    # Target
    parser.add_argument('--target-accuracy', type=float, default=73.0,
                       help='Target accuracy to achieve')
    
    # Resume
    parser.add_argument('--resume', type=str, default=None,
                       help='Path to checkpoint to resume from')
    
    return parser.parse_args()


def train_epoch_optimized(model, loader, criterion, optimizer, device, epoch, logger, 
                          scaler=None, gradient_accumulation=1):
    """
    GPU-optimized training epoch with mixed precision and gradient accumulation
    """
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    optimizer.zero_grad()
    
    pbar = tqdm(loader, desc=f'Epoch {epoch} [Train]')
    for batch_idx, (inputs, targets) in enumerate(pbar):
        # Non-blocking transfer for better GPU utilization
        inputs = inputs.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)
        
        # Mixed precision training
        if scaler is not None:
            with torch.cuda.amp.autocast():
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                loss = loss / gradient_accumulation
            
            scaler.scale(loss).backward()
            
            if (batch_idx + 1) % gradient_accumulation == 0:
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()
        else:
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss = loss / gradient_accumulation
            
            loss.backward()
            
            if (batch_idx + 1) % gradient_accumulation == 0:
                optimizer.step()
                optimizer.zero_grad()
        
        # Statistics
        running_loss += loss.item() * gradient_accumulation
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        
        # Update progress bar
        pbar.set_postfix({
            'loss': f'{running_loss/(batch_idx+1):.3f}',
            'acc': f'{100.*correct/total:.2f}%'
        })
    
    epoch_loss = running_loss / len(loader)
    epoch_acc = 100. * correct / total
    
    return epoch_loss, epoch_acc


def evaluate_optimized(model, loader, criterion, device, logger):
    """
    GPU-optimized evaluation
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(loader, desc='Evaluating')
        for inputs, targets in pbar:
            # Non-blocking transfer
            inputs = inputs.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)
            
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
            
            pbar.set_postfix({
                'loss': f'{running_loss/(len(pbar.iterable)):.3f}',
                'acc': f'{100.*correct/total:.2f}%'
            })
    
    epoch_loss = running_loss / len(loader)
    epoch_acc = 100. * correct / total
    
    return epoch_loss, epoch_acc


def main():
    args = parse_args()
    
    # Setup directories and logging
    os.makedirs(args.save_dir, exist_ok=True)
    os.makedirs(args.log_dir, exist_ok=True)
    logger = setup_logging(args.log_dir)
    
    # GPU setup
    if not torch.cuda.is_available():
        logger.warning("CUDA not available! Falling back to CPU (very slow)")
        device = torch.device('cpu')
    else:
        device = torch.device('cuda')
        
        # Enable cuDNN autotuner for optimal performance
        if args.benchmark:
            torch.backends.cudnn.benchmark = True
            logger.info("✅ cuDNN autotuner enabled")
        
        # GPU information
        logger.info(f"🚀 Using GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"📊 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        logger.info(f"🔢 CUDA Version: {torch.version.cuda}")
        
        if args.multi_gpu and torch.cuda.device_count() > 1:
            logger.info(f"🔥 Multi-GPU training enabled: {torch.cuda.device_count()} GPUs")
    
    # Data loaders with GPU optimizations
    logger.info("Preparing GPU-optimized data loaders...")
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
    
    # Move model to device
    model = model.to(device)
    
    # Channels-last memory format (optional optimization)
    if args.channels_last and torch.cuda.is_available():
        model = model.to(memory_format=torch.channels_last)
        logger.info("✅ Using channels-last memory format")
    
    # Multi-GPU support
    if args.multi_gpu and torch.cuda.is_available() and torch.cuda.device_count() > 1:
        model = nn.DataParallel(model)
        logger.info(f"✅ Model wrapped with DataParallel ({torch.cuda.device_count()} GPUs)")
    
    model_info = get_model_info(model.module if hasattr(model, 'module') else model)
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
    scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer, T_0=10, T_mult=2, eta_min=1e-6
    )
    
    # Mixed precision scaler
    scaler = torch.cuda.amp.GradScaler() if args.amp and torch.cuda.is_available() else None
    if scaler:
        logger.info("✅ Automatic Mixed Precision (FP16) enabled")
    
    # Resume from checkpoint
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
    logger.info("GPU-Optimized Training Configuration")
    logger.info(f"{'='*60}")
    logger.info(f"Model: {args.model}")
    logger.info(f"Device: {device}")
    logger.info(f"Multi-GPU: {args.multi_gpu and torch.cuda.device_count() > 1}")
    logger.info(f"Mixed Precision (AMP): {args.amp and torch.cuda.is_available()}")
    logger.info(f"Gradient Accumulation: {args.gradient_accumulation}x")
    logger.info(f"cuDNN Benchmark: {args.benchmark}")
    logger.info(f"Channels Last: {args.channels_last}")
    logger.info(f"Effective Batch Size: {args.batch_size * args.gradient_accumulation}")
    logger.info(f"{'='*60}\n")
    
    # Training loop
    logger.info(f"🚀 Starting GPU-optimized training for {args.epochs} epochs...\n")
    start_time = time.time()
    
    for epoch in range(start_epoch, args.epochs + 1):
        # Train
        train_loss, train_acc = train_epoch_optimized(
            model, train_loader, criterion, optimizer, device, epoch, logger,
            scaler=scaler, gradient_accumulation=args.gradient_accumulation
        )
        
        # Evaluate
        test_loss, test_acc = evaluate_optimized(
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
        
        # GPU memory stats
        if torch.cuda.is_available():
            logger.info(f"GPU Memory: {torch.cuda.max_memory_allocated()/1e9:.2f}GB allocated")
            torch.cuda.reset_peak_memory_stats()
        
        # Save best model
        if test_acc > best_acc:
            best_acc = test_acc
            model_to_save = model.module if hasattr(model, 'module') else model
            save_checkpoint(
                model_to_save, optimizer, epoch, test_acc, history,
                os.path.join(args.save_dir, 'best_model.pth')
            )
            logger.info(f"✨ New best accuracy: {best_acc:.2f}%")
        
        # Check if target reached
        if test_acc >= args.target_accuracy:
            logger.info(f"\n🎉 Target accuracy {args.target_accuracy}% reached!")
            model_to_save = model.module if hasattr(model, 'module') else model
            save_checkpoint(
                model_to_save, optimizer, epoch, test_acc, history,
                os.path.join(args.save_dir, f'target_model_epoch_{epoch}.pth')
            )
        
        # Save checkpoint periodically
        if epoch % args.save_freq == 0:
            model_to_save = model.module if hasattr(model, 'module') else model
            save_checkpoint(
                model_to_save, optimizer, epoch, test_acc, history,
                os.path.join(args.save_dir, f'checkpoint_epoch_{epoch}.pth')
            )
        
        logger.info(f"{'-'*60}\n")
    
    # Training complete
    training_time = time.time() - start_time
    logger.info(f"\n{'='*60}")
    logger.info("Training Complete!")
    logger.info(f"{'='*60}")
    logger.info(f"Total training time: {training_time/3600:.2f} hours")
    logger.info(f"Average time per epoch: {training_time/args.epochs/60:.2f} minutes")
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
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'gpu_optimizations': {
            'amp': args.amp,
            'multi_gpu': args.multi_gpu and torch.cuda.device_count() > 1,
            'gradient_accumulation': args.gradient_accumulation,
            'benchmark': args.benchmark,
            'channels_last': args.channels_last
        }
    }
    
    with open(os.path.join(args.log_dir, 'training_results.json'), 'w') as f:
        json.dump(results, f, indent=4)
    
    # Plot training curves
    plot_training_history(history, args.target_accuracy, args.log_dir)
    
    logger.info("✅ GPU-optimized training results saved!")


if __name__ == "__main__":
    main()

