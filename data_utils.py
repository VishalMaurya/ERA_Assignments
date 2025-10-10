"""
Data Loading and Augmentation Utilities for CIFAR-100
====================================================

This module handles data loading, augmentation, and preprocessing
for CIFAR-100 dataset.
"""

import torch
from torch.utils.data import Dataset, DataLoader
import torchvision
import albumentations as A
from albumentations.pytorch import ToTensorV2
import numpy as np


# CIFAR-100 statistics
CIFAR100_MEAN = (0.5071, 0.4867, 0.4408)
CIFAR100_STD = (0.2675, 0.2565, 0.2761)


def get_train_transforms():
    """Get training augmentation pipeline"""
    return A.Compose([
        A.HorizontalFlip(p=0.5),
        A.ShiftScaleRotate(
            shift_limit=0.1, 
            scale_limit=0.15, 
            rotate_limit=15, 
            p=0.5
        ),
        A.CoarseDropout(
            max_holes=1, max_height=16, max_width=16,
            min_holes=1, min_height=16, min_width=16,
            fill_value=tuple([int(x * 255) for x in CIFAR100_MEAN]),
            p=0.5
        ),
        A.RandomBrightnessContrast(
            brightness_limit=0.2, 
            contrast_limit=0.2, 
            p=0.5
        ),
        A.HueSaturationValue(
            hue_shift_limit=20, 
            sat_shift_limit=30, 
            val_shift_limit=20, 
            p=0.5
        ),
        A.Normalize(mean=CIFAR100_MEAN, std=CIFAR100_STD),
        ToTensorV2(),
    ])


def get_val_transforms():
    """Get validation/test augmentation pipeline"""
    return A.Compose([
        A.Normalize(mean=CIFAR100_MEAN, std=CIFAR100_STD),
        ToTensorV2(),
    ])


class CIFAR100Dataset(Dataset):
    """Custom CIFAR-100 dataset with Albumentations support"""
    
    def __init__(self, data, targets, transform=None):
        self.data = data
        self.targets = targets
        self.transform = transform
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        image = self.data[idx]
        label = self.targets[idx]
        
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
        
        return image, label


def get_cifar100_loaders(batch_size=128, num_workers=4, data_dir='./data'):
    """
    Get CIFAR-100 train and test dataloaders
    
    Args:
        batch_size: Batch size for dataloaders
        num_workers: Number of workers for data loading
        data_dir: Directory to download/load data
    
    Returns:
        train_loader, test_loader, class_names
    """
    # Download CIFAR-100
    print("Loading CIFAR-100 dataset...")
    trainset = torchvision.datasets.CIFAR100(
        root=data_dir, train=True, download=True
    )
    testset = torchvision.datasets.CIFAR100(
        root=data_dir, train=False, download=True
    )
    
    # Create custom datasets with augmentation
    train_dataset = CIFAR100Dataset(
        trainset.data, 
        trainset.targets, 
        transform=get_train_transforms()
    )
    test_dataset = CIFAR100Dataset(
        testset.data, 
        testset.targets, 
        transform=get_val_transforms()
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
        persistent_workers=True if num_workers > 0 else False
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        persistent_workers=True if num_workers > 0 else False
    )
    
    class_names = trainset.classes
    
    print(f"✅ Training samples: {len(train_dataset)}")
    print(f"✅ Test samples: {len(test_dataset)}")
    print(f"✅ Number of classes: {len(class_names)}")
    print(f"✅ Batches per epoch: {len(train_loader)}")
    
    return train_loader, test_loader, class_names


def denormalize_image(img, mean=CIFAR100_MEAN, std=CIFAR100_STD):
    """
    Denormalize image for visualization
    
    Args:
        img: Normalized image tensor
        mean: Mean used for normalization
        std: Std used for normalization
    
    Returns:
        Denormalized image as numpy array
    """
    img = img.permute(1, 2, 0).cpu().numpy()
    img = img * np.array(std) + np.array(mean)
    img = np.clip(img, 0, 1)
    return img


if __name__ == "__main__":
    # Test data loading
    print("Testing CIFAR-100 data loading...")
    train_loader, test_loader, class_names = get_cifar100_loaders(
        batch_size=128,
        num_workers=2
    )
    
    # Get a batch
    images, labels = next(iter(train_loader))
    print(f"\nBatch shape: {images.shape}")
    print(f"Labels shape: {labels.shape}")
    print(f"First 10 labels: {labels[:10].tolist()}")
    print(f"Sample classes: {[class_names[i] for i in labels[:5].tolist()]}")

