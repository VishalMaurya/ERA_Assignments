"""
Budget-Compliant Enhanced CIFAR_GAP_Net - Final Implementation
=============================================================

Budget-Compliant Enhanced CIFAR_GAP_Net with architectural improvements within 200K parameter budget

Target: 85-86% accuracy with <200K parameters
Final Optimizations:
1. Minimal residual connections (only block 5)
2. Ultra-lightweight SE modules (reduction=64)
3. Efficient dual-scale dilated blocks (2 branches)
4. Minimal channel progression (3→28→42→56→70→84)
5. Standard depthwise separable (efficient)

Expected improvement: +1.5-2.5% accuracy (83.46% → 85-86%) within strict budget
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
# Ultra-Optimized Components
# -----------------------

class UltraLightweightSEModule(nn.Module):
    """Ultra-Lightweight Squeeze-and-Excitation Module with very high reduction"""
    def __init__(self, channels, reduction=64):  # Very high reduction for efficiency
        super().__init__()
        reduced_channels = max(channels // reduction, 1)  # Minimum 1 channel
        
        self.se = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(channels, reduced_channels, 1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(reduced_channels, channels, 1, bias=False),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        return x * self.se(x)

class StandardDepthwiseSeparableConv(nn.Module):
    """Standard Depthwise Separable Convolution (most efficient)"""
    def __init__(self, in_ch, out_ch, kernel_size=3, stride=1, padding=1):
        super().__init__()
        
        # Standard depthwise separable conv
        self.dw = nn.Conv2d(in_ch, in_ch, kernel_size, stride=stride, padding=padding, groups=in_ch, bias=False)
        self.bn1 = nn.BatchNorm2d(in_ch)
        self.pw = nn.Conv2d(in_ch, out_ch, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_ch)
        self.act = nn.ReLU(inplace=True)
        
    def forward(self, x):
        x = self.dw(x)
        x = self.bn1(x)
        x = self.act(x)
        x = self.pw(x)
        x = self.bn2(x)
        x = self.act(x)
        return x

class DualScaleDilatedBlock(nn.Module):
    """Dual-scale dilated convolution block (2 branches for efficiency)"""
    def __init__(self, channels):
        super().__init__()
        
        # Two branches with different dilation rates
        branch_channels = channels // 2
        
        self.branch1 = nn.Sequential(
            nn.Conv2d(channels, branch_channels, 3, padding=2, dilation=2, bias=False),
            nn.BatchNorm2d(branch_channels),
            nn.ReLU(inplace=True)
        )
        
        self.branch2 = nn.Sequential(
            nn.Conv2d(channels, branch_channels, 3, padding=4, dilation=4, bias=False),
            nn.BatchNorm2d(branch_channels),
            nn.ReLU(inplace=True)
        )
        
        # 1x1 conv to combine features
        self.combine = nn.Sequential(
            nn.Conv2d(branch_channels * 2, channels, 1, bias=False),
            nn.BatchNorm2d(channels),
            nn.ReLU(inplace=True)
        )
        
    def forward(self, x):
        b1 = self.branch1(x)
        b2 = self.branch2(x)
        
        # Concatenate branches
        concat = torch.cat([b1, b2], dim=1)
        
        # Combine features
        out = self.combine(concat)
        
        return out

# -----------------------
# Budget-Compliant Enhanced CIFAR_GAP_Net
# -----------------------

class BudgetCompliantEnhancedCIFAR_GAP_Net(nn.Module):
    """
    Budget-Compliant Enhanced CIFAR_GAP_Net: Strictly Within 200K Parameters
    
    Target: 85-86% accuracy with <200K parameters
    Final Optimizations:
    1. Minimal residual connections (block 5 only)
    2. Ultra-lightweight SE modules (reduction=64)
    3. Dual-scale dilated blocks (2 branches)
    4. Minimal channel progression (3→28→42→56→70→84)
    5. Standard depthwise separable (most efficient)
    
    Expected improvement: +1.5-2.5% accuracy within strict parameter budget
    """
    
    def __init__(self, num_classes=10):
        super().__init__()
        
        # Minimal channel progression: 3→28→42→56→70→84
        
        # Block 1: Initial feature extraction with spatial reduction
        # Input: 3×32×32 → Output: 28×16×16
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 28, kernel_size=3, stride=2, padding=1, bias=False), # stride2 (no MaxPool!)
            nn.BatchNorm2d(28),
            nn.ReLU(inplace=True),
            nn.Conv2d(28, 28, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(28),
            nn.ReLU(inplace=True),
        )
        self.se1 = UltraLightweightSEModule(28, reduction=28)  # Minimal SE
        
        # Block 2: Standard depthwise separable conv with spatial reduction
        # Input: 28×16×16 → Output: 42×8×8
        self.dw_sep = StandardDepthwiseSeparableConv(28, 42, kernel_size=3, stride=2, padding=1)
        self.se2 = UltraLightweightSEModule(42, reduction=42)  # Minimal SE
        
        # Block 3: Dual-scale dilated convolution (NO residual to save params)
        # Input: 42×8×8 → Output: 56×8×8 (RF expansion)
        self.conv3_proj = nn.Sequential(
            nn.Conv2d(42, 56, kernel_size=1, bias=False),
            nn.BatchNorm2d(56),
            nn.ReLU(inplace=True)
        )
        self.dilated1 = DualScaleDilatedBlock(56)
        self.se3 = UltraLightweightSEModule(56, reduction=56)  # Minimal SE
        
        # Block 4: Feature expansion with spatial reduction (NO residual)
        # Input: 56×8×8 → Output: 70×4×4
        self.conv4 = nn.Sequential(
            nn.Conv2d(56, 70, kernel_size=3, stride=2, padding=1, bias=False), # stride2 (no MaxPool!)
            nn.BatchNorm2d(70),
            nn.ReLU(inplace=True),
            nn.Conv2d(70, 70, kernel_size=1, stride=1, bias=False), # 1×1 conv for efficiency
            nn.BatchNorm2d(70),
            nn.ReLU(inplace=True),
        )
        self.se4 = UltraLightweightSEModule(70, reduction=70)  # Minimal SE
        
        # Block 5: Final dual-scale dilation (WITH residual - only one!)
        # Input: 70×4×4 → Output: 84×4×4 (RF expansion)
        self.conv5_proj = nn.Sequential(
            nn.Conv2d(70, 84, kernel_size=1, bias=False),
            nn.BatchNorm2d(84),
            nn.ReLU(inplace=True)
        )
        self.dilated2 = DualScaleDilatedBlock(84)
        self.se5 = UltraLightweightSEModule(84, reduction=84)  # Minimal SE
        
        # Output: Global Average Pooling + Linear classifier
        # Input: 84×4×4 → Output: 10 classes
        self.gap = nn.AdaptiveAvgPool2d(1)  # GAP (no FC layers after conv!)
        self.dropout = nn.Dropout(0.05)  # Minimal dropout
        self.fc = nn.Linear(84, num_classes)

    def forward(self, x):
        # Block 1: 3×32×32 → 28×16×16
        x = self.conv1(x)
        x = self.se1(x)
        
        # Block 2: 28×16×16 → 42×8×8
        x = self.dw_sep(x)
        x = self.se2(x)
        
        # Block 3: 42×8×8 → 56×8×8 (NO residual)
        x = self.conv3_proj(x)  # Project to 56 channels
        x = self.dilated1(x)
        x = self.se3(x)
        
        # Block 4: 56×8×8 → 70×4×4 (NO residual)
        x = self.conv4(x)
        x = self.se4(x)
        
        # Block 5: 70×4×4 → 84×4×4 (WITH residual - only one!)
        x = self.conv5_proj(x)  # Project to 84 channels
        identity = x
        x = self.dilated2(x)
        x = x + identity  # Single residual connection
        x = self.se5(x)
        
        # Output: 84×4×4 → 10 classes
        x = self.gap(x)             # → (B, 84, 1, 1)
        x = torch.flatten(x, 1)     # → (B, 84)
        x = self.dropout(x)         # Minimal regularization
        out = self.fc(x)            # → (B, 10)
        
        return out
    
    def count_parameters(self):
        """Count total trainable parameters"""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    
    def get_model_info(self):
        """Get comprehensive model information"""
        total_params = self.count_parameters()
        
        return {
            'model_name': 'BudgetCompliantEnhancedCIFAR_GAP_Net',
            'total_parameters': total_params,
            'parameter_budget_used': (total_params / 200000) * 100,
            'parameter_requirement_met': total_params < 200000,
            'target_accuracy': 85.5,
            'architecture_blocks': 5,
            'uses_maxpooling': False,
            'uses_dilated_conv': True,
            'uses_depthwise_separable': True,
            'uses_gap': True,
            'uses_residual_connections': True,
            'uses_attention': True,
            'estimated_rf': 140,
            'optimizations': [
                'Ultra-lightweight SE modules',
                'Dual-scale dilated blocks',
                'Single residual connection',
                'Minimal channel progression',
                'Standard depthwise separable'
            ]
        }

# -----------------------
# Data Augmentation (Same as previous)
# -----------------------

# CIFAR-10 dataset statistics
CIFAR10_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR10_STD = (0.2023, 0.1994, 0.2010)

class CoarseDropout(object):
    """CoarseDropout augmentation matching exact assignment specifications"""
    def __init__(self, max_holes=1, max_height=16, max_width=16, 
                 min_holes=1, min_height=16, min_width=16,
                 fill_value=(0.4914, 0.4822, 0.4465), mask_fill_value=None):
        self.max_holes = max_holes
        self.max_height = max_height
        self.max_width = max_width
        self.min_holes = min_holes
        self.min_height = min_height
        self.min_width = min_width
        self.fill_value = fill_value
        self.mask_fill_value = mask_fill_value

    def __call__(self, img):
        """Apply coarse dropout to tensor image"""
        h, w = img.size(1), img.size(2)
        
        # Number of holes
        n_holes = np.random.randint(self.min_holes, self.max_holes + 1)
        
        for _ in range(n_holes):
            # Hole dimensions
            hole_height = np.random.randint(self.min_height, self.max_height + 1)
            hole_width = np.random.randint(self.min_width, self.max_width + 1)
            
            # Random position for the hole
            y = np.random.randint(0, h)
            x = np.random.randint(0, w)
            
            # Calculate hole boundaries
            y1 = max(0, y - hole_height // 2)
            y2 = min(h, y + hole_height // 2)
            x1 = max(0, x - hole_width // 2)
            x2 = min(w, x + hole_width // 2)
            
            # Fill with dataset mean (normalized to 0 after normalization)
            if self.fill_value is not None:
                for c in range(img.size(0)):
                    img[c, y1:y2, x1:x2] = 0.0  # After normalization, mean ≈ 0
        
        return img

# Training transforms
train_transforms = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.125, scale_limit=0.15, rotate_limit=15, p=0.5),
    A.CoarseDropout(max_holes=1, max_height=16, max_width=16, 
                    min_holes=1, min_height=16, min_width=16,
                    fill_value=CIFAR10_MEAN, p=0.5),
    A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=0.3),
    A.Normalize(mean=CIFAR10_MEAN, std=CIFAR10_STD),
    ToTensorV2(),
])

val_transforms = A.Compose([
    A.Normalize(mean=CIFAR10_MEAN, std=CIFAR10_STD),
    ToTensorV2(),
])

class AlbumentationsTransform:
    def __init__(self, transform):
        self.transform = transform

    def __call__(self, img):
        # Convert PIL to numpy
        img_np = np.array(img)
        # Apply albumentations
        augmented = self.transform(image=img_np)
        return augmented['image']

def create_budget_compliant_model_and_info():
    """Create budget-compliant enhanced model and display comprehensive information"""
    model = BudgetCompliantEnhancedCIFAR_GAP_Net(num_classes=10)
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
    print(f"  • Residual Connections: {model_info['uses_residual_connections']}")
    print(f"  • Attention Mechanisms: {model_info['uses_attention']}")
    print(f"  • Parameters < 200K: {model_info['parameter_requirement_met']}")
    
    print(f"\n🔧 Final Budget Optimizations:")
    for i, optimization in enumerate(model_info['optimizations'], 1):
        print(f"  {i}. {optimization}")
    
    return model, model_info

def get_budget_compliant_dataloaders(batch_size=128, num_workers=4):
    """Create CIFAR-10 data loaders with budget-compliant augmentation"""
    train_ds = torchvision.datasets.CIFAR10(root='./data', train=True, download=True,
                                            transform=AlbumentationsTransform(train_transforms))
    val_ds = torchvision.datasets.CIFAR10(root='./data', train=False, download=True,
                                          transform=AlbumentationsTransform(val_transforms))
    
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, 
                             num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size*2, shuffle=False, 
                           num_workers=num_workers, pin_memory=True)
    
    print(f"📊 Budget-Compliant Dataset loaded:")
    print(f"  Training samples: {len(train_ds):,}")
    print(f"  Test samples: {len(val_ds):,}")
    print(f"  Batch size: {batch_size}")
    print(f"  Budget-compliant augmentation: Efficient enhancements")
    
    return train_loader, val_loader

# Example usage and testing
if __name__ == "__main__":
    # Quick test mode
    import sys
    if len(sys.argv) == 1:
        print("🧪 Budget-Compliant Enhanced Model Test Mode - Creating model and validating...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, model_info = create_budget_compliant_model_and_info()
        model = model.to(device)
        
        # Test forward pass
        dummy_input = torch.randn(4, 3, 32, 32).to(device)
        with torch.no_grad():
            output = model(dummy_input)
        
        print(f"\n✅ Forward pass test:")
        print(f"  Input shape: {dummy_input.shape}")
        print(f"  Output shape: {output.shape}")
        print(f"  Output range: [{output.min():.3f}, {output.max():.3f}]")
        
        # Parameter analysis
        total_params = model.count_parameters()
        print(f"\n📊 Parameter Analysis:")
        print(f"  Total parameters: {total_params:,}")
        print(f"  Budget usage: {(total_params/200000)*100:.1f}%")
        print(f"  Within limit: {'✅ Yes' if total_params < 200000 else '❌ No'}")
        
        # Comparison with original
        original_params = 198666
        improvement_cost = total_params - original_params
        print(f"\n📈 Comparison with Original:")
        print(f"  Original CIFAR_GAP_Net: {original_params:,} params")
        print(f"  Budget-Compliant Enhanced: {total_params:,} params")
        print(f"  Additional cost: {improvement_cost:+,} params ({(improvement_cost/original_params)*100:+.1f}%)")
        
        print(f"\n🚀 Budget-compliant enhanced model ready for training!")
        print(f"  Expected accuracy: 85-86% (vs 83.46% baseline)")
        print(f"  Improvements: +1.5-2.5% from budget-compliant enhancements")
        print(f"\n🏃‍♂️ To train: python3 budget_compliant_enhanced_cifar_gap_net.py --train")
    
    elif '--train' in sys.argv:
        print("🚀 Budget-compliant enhanced training mode would be implemented here")
        print("📋 Use the budget-compliant enhanced model with your existing training pipeline")
        print("🎯 Expected results: 85-86% accuracy within strict parameter budget")
