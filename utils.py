"""
Training and Testing Utilities for MNIST CNN Models
===================================================

This module contains utility functions for training and evaluating
CNN models on MNIST dataset with proper logging and monitoring.

Key Features:
- Comprehensive training loop with progress tracking
- Early stopping to prevent overfitting
- Learning rate scheduling
- Model checkpointing
- Detailed logging and metrics collection
- Visualization capabilities
"""

import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import os


def get_data_loaders(batch_size=64, test_batch_size=1000, data_dir='./data'):
    """
    Create MNIST data loaders with proper normalization.
    
    MNIST Statistics:
    - Mean: 0.1307
    - Std: 0.3081
    
    Args:
        batch_size: Training batch size
        test_batch_size: Testing batch size  
        data_dir: Directory to store/load MNIST data
    
    Returns:
        tuple: (train_loader, test_loader)
    """
    # Data normalization - crucial for model convergence
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # MNIST statistics
    ])
    
    # Download and create datasets
    train_dataset = datasets.MNIST(
        data_dir, 
        train=True, 
        download=True, 
        transform=transform
    )
    
    test_dataset = datasets.MNIST(
        data_dir, 
        train=False, 
        download=True, 
        transform=transform
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True,
        num_workers=2,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset, 
        batch_size=test_batch_size, 
        shuffle=False,
        num_workers=2,
        pin_memory=True
    )
    
    print(f"Training samples: {len(train_dataset)}")
    print(f"Test samples: {len(test_dataset)}")
    print(f"Training batches: {len(train_loader)}")
    print(f"Test batches: {len(test_loader)}")
    
    return train_loader, test_loader


def train_one_epoch(model, device, train_loader, optimizer, epoch, log_interval=100):
    """
    Train model for one epoch with detailed progress tracking.
    
    Args:
        model: PyTorch model
        device: Device to run on (cuda/cpu)
        train_loader: Training data loader
        optimizer: Optimizer instance
        epoch: Current epoch number
        log_interval: How often to log progress
    
    Returns:
        tuple: (average_loss, accuracy_percentage)
    """
    model.train()
    
    total_loss = 0
    correct = 0
    total_samples = 0
    
    # Progress bar for better visualization
    pbar = tqdm(train_loader, desc=f'Epoch {epoch}')
    
    for batch_idx, (data, target) in enumerate(pbar):
        # Move data to device
        data, target = data.to(device), target.to(device)
        
        # Zero gradients
        optimizer.zero_grad()
        
        # Forward pass
        output = model(data)
        loss = F.cross_entropy(output, target)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Accumulate metrics
        total_loss += loss.item() * data.size(0)
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        total_samples += data.size(0)
        
        # Update progress bar
        current_accuracy = 100. * correct / total_samples
        pbar.set_postfix({
            'Loss': f'{loss.item():.4f}',
            'Acc': f'{current_accuracy:.2f}%'
        })
        
        # Periodic logging
        if batch_idx % log_interval == 0:
            progress = 100. * batch_idx / len(train_loader)
            current_lr = optimizer.param_groups[0]['lr']
            
            # Optional: log to file or tensorboard here
            pass
    
    # Calculate final metrics
    avg_loss = total_loss / total_samples
    accuracy = 100. * correct / total_samples
    
    return avg_loss, accuracy


def test_model(model, device, test_loader, epoch=None):
    """
    Evaluate model on test set.
    
    Args:
        model: PyTorch model
        device: Device to run on (cuda/cpu)
        test_loader: Test data loader
        epoch: Current epoch (for logging)
    
    Returns:
        tuple: (average_loss, accuracy_percentage)
    """
    model.eval()
    
    test_loss = 0
    correct = 0
    total_samples = 0
    
    # Disable gradient computation for efficiency
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            
            # Forward pass
            output = model(data)
            
            # Accumulate loss
            test_loss += F.cross_entropy(output, target, reduction='sum').item()
            
            # Accumulate correct predictions
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total_samples += data.size(0)
    
    # Calculate metrics
    avg_loss = test_loss / total_samples
    accuracy = 100. * correct / total_samples
    
    return avg_loss, accuracy


def train_model(model, model_name, device, train_loader, test_loader, 
                epochs=20, lr=0.01, target_accuracy=99.4, save_dir='./checkpoints'):
    """
    Complete training pipeline with early stopping and checkpointing.
    
    Args:
        model: PyTorch model to train
        model_name: Name for saving checkpoints
        device: Device to run on
        train_loader: Training data loader
        test_loader: Test data loader
        epochs: Maximum number of epochs
        lr: Initial learning rate
        target_accuracy: Target accuracy for early stopping
        save_dir: Directory to save model checkpoints
    
    Returns:
        dict: Training history and metrics
    """
    
    print(f"\n{'='*60}")
    print(f"Training {model_name}")
    print(f"{'='*60}")
    
    # Create save directory
    os.makedirs(save_dir, exist_ok=True)
    
    # Move model to device
    model = model.to(device)
    
    # Print model summary
    total_params = model.count_parameters() if hasattr(model, 'count_parameters') else \
                   sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total Parameters: {total_params:,}")
    
    # Setup optimizer and scheduler
    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=6, gamma=0.5)
    
    # Training tracking
    best_accuracy = 0
    early_stop_counter = 0
    early_stop_patience = 5
    
    history = {
        'train_loss': [],
        'train_acc': [],
        'test_loss': [],
        'test_acc': [],
        'lr': []
    }
    
    start_time = time.time()
    
    for epoch in range(1, epochs + 1):
        epoch_start = time.time()
        
        # Training phase
        train_loss, train_acc = train_one_epoch(
            model, device, train_loader, optimizer, epoch
        )
        
        # Testing phase
        test_loss, test_acc = test_model(model, device, test_loader, epoch)
        
        # Learning rate scheduling
        scheduler.step()
        current_lr = optimizer.param_groups[0]['lr']
        
        # Record history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['test_loss'].append(test_loss)
        history['test_acc'].append(test_acc)
        history['lr'].append(current_lr)
        
        # Calculate epoch time
        epoch_time = time.time() - epoch_start
        
        # Logging
        print(f"\nEpoch {epoch:2d}/{epochs} | Time: {epoch_time:.1f}s | LR: {current_lr:.6f}")
        print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"Test  Loss: {test_loss:.4f} | Test  Acc: {test_acc:.2f}%")
        
        # Model checkpointing
        if test_acc > best_accuracy:
            best_accuracy = test_acc
            early_stop_counter = 0
            
            # Save best model
            checkpoint_path = os.path.join(save_dir, f'{model_name}_best.pth')
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'best_accuracy': best_accuracy,
                'history': history
            }, checkpoint_path)
            
            print(f"🎯 New best accuracy: {best_accuracy:.2f}% (saved to {checkpoint_path})")
        else:
            early_stop_counter += 1
        
        # Early stopping check
        if test_acc >= target_accuracy:
            print(f"\n🎉 TARGET ACHIEVED! Test Accuracy: {test_acc:.2f}% >= {target_accuracy}%")
            break
            
        if early_stop_counter >= early_stop_patience:
            print(f"\n⏰ Early stopping triggered after {early_stop_patience} epochs without improvement")
            break
    
    # Training summary
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"Training Complete - {model_name}")
    print(f"{'='*60}")
    print(f"Total Time: {total_time:.1f}s")
    print(f"Best Test Accuracy: {best_accuracy:.2f}%")
    print(f"Final Learning Rate: {current_lr:.6f}")
    print(f"Parameters: {total_params:,}")
    
    # Add final metrics to history
    history['best_accuracy'] = best_accuracy
    history['total_time'] = total_time
    history['total_params'] = total_params
    history['target_achieved'] = best_accuracy >= target_accuracy
    
    return history


def plot_training_history(histories, save_path=None):
    """
    Plot training histories for multiple models.
    
    Args:
        histories: Dict of model_name -> history
        save_path: Optional path to save the plot
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    for model_name, history in histories.items():
        epochs = range(1, len(history['train_loss']) + 1)
        
        # Training & Test Loss
        ax1.plot(epochs, history['train_loss'], label=f'{model_name} Train')
        ax1.plot(epochs, history['test_loss'], label=f'{model_name} Test', linestyle='--')
    
    ax1.set_title('Training & Test Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)
    
    for model_name, history in histories.items():
        epochs = range(1, len(history['train_acc']) + 1)
        
        # Training & Test Accuracy
        ax2.plot(epochs, history['train_acc'], label=f'{model_name} Train')
        ax2.plot(epochs, history['test_acc'], label=f'{model_name} Test', linestyle='--')
    
    ax2.set_title('Training & Test Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(True)
    ax2.axhline(y=99.4, color='r', linestyle=':', label='Target (99.4%)')
    
    # Test Accuracy Comparison
    for model_name, history in histories.items():
        epochs = range(1, len(history['test_acc']) + 1)
        ax3.plot(epochs, history['test_acc'], label=f'{model_name}', linewidth=2)
    
    ax3.set_title('Test Accuracy Comparison')
    ax3.set_xlabel('Epoch')
    ax3.set_ylabel('Test Accuracy (%)')
    ax3.legend()
    ax3.grid(True)
    ax3.axhline(y=99.4, color='r', linestyle=':', label='Target (99.4%)')
    
    # Learning Rate
    for model_name, history in histories.items():
        epochs = range(1, len(history['lr']) + 1)
        ax4.plot(epochs, history['lr'], label=f'{model_name}')
    
    ax4.set_title('Learning Rate Schedule')
    ax4.set_xlabel('Epoch')
    ax4.set_ylabel('Learning Rate')
    ax4.legend()
    ax4.grid(True)
    ax4.set_yscale('log')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()


def generate_summary_table(histories):
    """
    Generate a formatted summary table of training results.
    
    Args:
        histories: Dict of model_name -> history
    
    Returns:
        str: Formatted table string
    """
    header = f"{'Model':<20} {'Parameters':<12} {'Best Acc':<10} {'Target':<8} {'Time':<8}"
    separator = "="*60
    
    lines = [separator, header, separator]
    
    for model_name, history in histories.items():
        params = f"{history['total_params']:,}"
        best_acc = f"{history['best_accuracy']:.2f}%"
        target = "✅" if history['target_achieved'] else "❌"
        time_str = f"{history['total_time']:.1f}s"
        
        line = f"{model_name:<20} {params:<12} {best_acc:<10} {target:<8} {time_str:<8}"
        lines.append(line)
    
    lines.append(separator)
    
    return "\n".join(lines)


def get_device():
    """Get the best available device for training."""
    if torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device('cpu')
        print("Using CPU")
    
    return device


if __name__ == "__main__":
    # Test utilities
    print("Testing utilities...")
    
    # Test data loading
    train_loader, test_loader = get_data_loaders(batch_size=64)
    print(f"✅ Data loaders created successfully")
    
    # Test device detection
    device = get_device()
    print(f"✅ Device: {device}")
    
    print("All utilities working correctly!")
