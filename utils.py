"""
Training Utilities for ResNet CIFAR-100
======================================

Utility functions for training, evaluation, checkpointing,
visualization, and logging.
"""

import torch
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
from tqdm import tqdm
from datetime import datetime


def setup_logging(log_dir='logs'):
    """Setup logging configuration"""
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'training_{timestamp}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def train_epoch(model, loader, criterion, optimizer, device, epoch, logger):
    """
    Train model for one epoch
    
    Args:
        model: PyTorch model
        loader: Training data loader
        criterion: Loss function
        optimizer: Optimizer
        device: Device to train on
        epoch: Current epoch number
        logger: Logger object
    
    Returns:
        epoch_loss, epoch_accuracy
    """
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(loader, desc=f'Epoch {epoch} [Train]')
    for batch_idx, (inputs, targets) in enumerate(pbar):
        inputs, targets = inputs.to(device), targets.to(device)
        
        # Forward pass
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Statistics
        running_loss += loss.item()
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


def evaluate(model, loader, criterion, device, logger):
    """
    Evaluate model on validation/test set
    
    Args:
        model: PyTorch model
        loader: Validation/test data loader
        criterion: Loss function
        device: Device to evaluate on
        logger: Logger object
    
    Returns:
        epoch_loss, epoch_accuracy
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(loader, desc='Evaluating')
        for inputs, targets in pbar:
            inputs, targets = inputs.to(device), targets.to(device)
            
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


def save_checkpoint(model, optimizer, epoch, accuracy, history, path):
    """
    Save model checkpoint
    
    Args:
        model: PyTorch model
        optimizer: Optimizer
        epoch: Current epoch
        accuracy: Current accuracy
        history: Training history dict
        path: Path to save checkpoint
    """
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'accuracy': accuracy,
        'best_accuracy': max(history['test_acc']) if history['test_acc'] else accuracy,
        'history': history
    }, path)
    print(f"💾 Checkpoint saved: {path}")


def plot_training_history(history, target_accuracy, save_dir='logs'):
    """
    Plot training curves
    
    Args:
        history: Training history dict
        target_accuracy: Target accuracy line
        save_dir: Directory to save plots
    """
    sns.set_style('whitegrid')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    epochs = range(1, len(history['train_loss']) + 1)
    
    # Loss curves
    axes[0, 0].plot(epochs, history['train_loss'], label='Train Loss', linewidth=2, color='blue')
    axes[0, 0].plot(epochs, history['test_loss'], label='Test Loss', linewidth=2, color='red')
    axes[0, 0].set_xlabel('Epoch', fontsize=12)
    axes[0, 0].set_ylabel('Loss', fontsize=12)
    axes[0, 0].set_title('Training and Test Loss', fontsize=14, fontweight='bold')
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Accuracy curves
    axes[0, 1].plot(epochs, history['train_acc'], label='Train Acc', linewidth=2, color='blue')
    axes[0, 1].plot(epochs, history['test_acc'], label='Test Acc', linewidth=2, color='red')
    axes[0, 1].axhline(y=target_accuracy, color='green', linestyle='--', 
                       label=f'Target ({target_accuracy}%)', linewidth=2)
    axes[0, 1].set_xlabel('Epoch', fontsize=12)
    axes[0, 1].set_ylabel('Accuracy (%)', fontsize=12)
    axes[0, 1].set_title('Training and Test Accuracy', fontsize=14, fontweight='bold')
    axes[0, 1].legend(fontsize=10)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Learning rate
    axes[1, 0].plot(epochs, history['lr'], linewidth=2, color='green')
    axes[1, 0].set_xlabel('Epoch', fontsize=12)
    axes[1, 0].set_ylabel('Learning Rate', fontsize=12)
    axes[1, 0].set_title('Learning Rate Schedule', fontsize=14, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_yscale('log')
    
    # Best accuracy progression
    best_acc_progression = []
    current_best = 0
    for acc in history['test_acc']:
        if acc > current_best:
            current_best = acc
        best_acc_progression.append(current_best)
    
    axes[1, 1].plot(epochs, best_acc_progression, linewidth=2, color='purple')
    axes[1, 1].axhline(y=target_accuracy, color='green', linestyle='--', 
                       label=f'Target ({target_accuracy}%)', linewidth=2)
    axes[1, 1].set_xlabel('Epoch', fontsize=12)
    axes[1, 1].set_ylabel('Best Accuracy (%)', fontsize=12)
    axes[1, 1].set_title('Best Accuracy Progression', fontsize=14, fontweight='bold')
    axes[1, 1].legend(fontsize=10)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_path = os.path.join(save_dir, f'training_curves_{timestamp}.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"📊 Training curves saved: {save_path}")
    plt.close()


def get_lr(optimizer):
    """Get current learning rate from optimizer"""
    for param_group in optimizer.param_groups:
        return param_group['lr']


def count_parameters(model):
    """Count total and trainable parameters"""
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return total_params, trainable_params


if __name__ == "__main__":
    # Test plotting
    print("Testing plotting utilities...")
    
    # Create dummy history
    import numpy as np
    history = {
        'train_loss': list(np.linspace(2.0, 0.5, 100)),
        'test_loss': list(np.linspace(2.0, 0.6, 100)),
        'train_acc': list(np.linspace(20, 85, 100)),
        'test_acc': list(np.linspace(15, 73, 100)),
        'lr': list(np.logspace(-1, -6, 100))
    }
    
    plot_training_history(history, target_accuracy=73.0, save_dir='.')
    print("✅ Test plot created!")

