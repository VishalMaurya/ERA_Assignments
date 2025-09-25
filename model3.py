"""
SESSION 6 - MODEL 3: Complete Curriculum Implementation
======================================================

CURRICULUM ALIGNMENT:
- Code 2-8: All from Models 1 & 2 (Skeleton, Lighter, BN, Dropout, GAP, Capacity, Pooling)
- Code 9: Image Augmentation - Handled in training pipeline (RandomRotation, RandomAffine)
- Code 10: Learning Rate Scheduling - Handled in training pipeline (MultiStepLR)
- Complete integration of all Session 6 concepts

TARGET:
- Parameters: <8k (maximum efficiency within constraint)
- Accuracy: 99.4%+ consistently in final epochs
- Epochs: ≤15 (with all curriculum optimizations)
- Strategy: All curriculum techniques combined optimally

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Final 5 Epochs: [Epoch 11-15 accuracies]
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Complete curriculum effectiveness
- All 10 code iterations impact
- Optimal technique combination
- Final Session 6 insights vs Models 1 & 2
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Model_3(nn.Module):
    """
    Final precision CNN for MNIST with <8k parameters.
    
    CURRICULUM ALIGNMENT:
    - Code 2-8: All from Models 1 & 2 (Skeleton, Lighter, BN, Dropout, GAP, Capacity, Pooling)
    - Code 9: Image Augmentation - Handled in training pipeline (RandomRotation, RandomAffine)
    - Code 10: Learning Rate Scheduling - Handled in training pipeline (MultiStepLR)
    - Complete integration of all Session 6 concepts
    
    Architecture Strategy:
    - Enhanced channel progression: 1→8→14→18→24→10
    - Multi-layer blocks for maximum capacity
    - Optimized pooling placement (Code 8)
    - Simple squeeze-excitation attention
    - Strategic dropout
    
    Expected Parameter Breakdown:
    - Stem: ~80 params
    - Conv2: ~1000 params
    - Conv3: ~2300 params
    - Conv4: ~3900 params
    - Attention: ~200 params
    - Final: ~240 params
    - Total: ~7720 params
    """
    
    def __init__(self, num_classes=10):
        super(Model_3, self).__init__()
        
        # Initial convolution (Code 2,3,4)
        self.stem = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(8),
            nn.ReLU()
        )
        
        # Ultra-efficient optimized layers 
        self.conv2 = nn.Conv2d(8, 14, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(14)
        
        self.pool1 = nn.MaxPool2d(2)  # 28x28 -> 14x14 (Code 8: Correct pooling)
        
        self.conv3 = nn.Conv2d(14, 18, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(18)
        
        self.pool2 = nn.MaxPool2d(2)  # 14x14 -> 7x7 (Code 8: Correct pooling)
        
        # Code 7: Additional capacity layer
        self.conv4 = nn.Conv2d(18, 24, kernel_size=3, padding=1, bias=False)
        self.bn4 = nn.BatchNorm2d(24)
        
        # Lightweight attention for final precision
        self.attention = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(24, 6, 1),
            nn.ReLU(),
            nn.Conv2d(6, 24, 1),
            nn.Sigmoid()
        )
        
        # Final classification
        self.final_conv = nn.Conv2d(24, 10, kernel_size=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Advanced dropout scheduling
        self.dropout_light = nn.Dropout(0.1)
        self.dropout_heavy = nn.Dropout(0.2)
        
    def forward(self, x):
        # Stem
        x = self.stem(x)              # 28x28x8
        
        # Ultra-efficient optimized layers
        x = F.relu(self.bn2(self.conv2(x)))  # 28x28x14
        x = self.pool1(x)             # 14x14x14
        x = self.dropout_light(x)
        
        x = F.relu(self.bn3(self.conv3(x)))  # 14x14x18
        x = self.pool2(x)             # 7x7x18
        x = self.dropout_light(x)
        
        # Code 7: Additional capacity
        x = F.relu(self.bn4(self.conv4(x)))  # 7x7x24
        
        # Apply lightweight attention
        att = self.attention(x)
        x = x * att
        
        # Final classification
        x = self.final_conv(x)        # 7x7x10
        x = self.gap(x)               # 1x1x10
        x = x.view(x.size(0), -1)    # 10
        
        return x
    
    def count_parameters(self):
        """Count total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    
    def get_receptive_field(self):
        """Calculate receptive field progression."""
        # Each 3x3 conv adds 2 to RF, each pool2d doubles the gap
        # Conv1: RF=3, Conv2: RF=5, Pool1: RF=10, Conv3: RF=12, Pool2: RF=24, Conv4: RF=26
        return 26
    
    def print_architecture(self):
        """Print detailed architecture for analysis."""
        print("Model_3 Architecture:")
        print("- Input: 1x28x28")
        print("- Stem Conv: 1→8, RF=3")
        print("- Conv2: 8→14, RF=5")
        print("- Pool1: 28→14, RF=10")
        print("- Conv3: 14→18, RF=12")
        print("- Pool2: 14→7, RF=24")
        print("- Conv4: 18→24, RF=26")
        print("- Attention: 24→24")
        print("- Final: 24→10")
        print("- GAP: 7x7→1x1")
        print("- Output: 10")
        print(f"- Receptive Field: {self.get_receptive_field()}")
        print(f"- Parameters: {self.count_parameters():,}")


def create_model_3():
    """Create and return Model_3 instance."""
    return Model_3()


def analyze_model_3():
    """Analyze Model_3 architecture and return metrics."""
    model = create_model_3()
    
    # Test forward pass
    with torch.no_grad():
        test_input = torch.randn(1, 1, 28, 28)
        output = model(test_input)
        output_shape = output.shape
    
    analysis = {
        'model_name': 'Model_3',
        'total_parameters': model.count_parameters(),
        'receptive_field': model.get_receptive_field(),
        'output_shape': output_shape,
        'target_accuracy': '99.4%+ consistently',
        'expected_epochs': '≤15',
        'curriculum_codes': '2-10 (Complete)',
        'architecture_efficiency': 'Complete curriculum + attention + multi-layer processing',
        'parameter_breakdown': {
            'stem': 'Conv2d(1,8) + BN: ~80 params',
            'conv2': 'Conv2d(8,14) + BN: ~1000 params', 
            'conv3': 'Conv2d(14,18) + BN: ~2300 params',
            'conv4': 'Conv2d(18,24) + BN: ~3900 params',
            'attention': 'Conv2d attention: ~200 params',
            'final': 'Conv2d(24,10): ~240 params'
        },
        'innovations': [
            'Complete Session 6 curriculum integration',
            'Optimized channel progression for efficiency',
            'Lightweight squeeze-excitation attention',
            'Strategic dropout scheduling',
            'Perfect balance of capacity and efficiency'
        ]
    }
    
    return analysis


if __name__ == "__main__":
    # Test the model
    model = create_model_3()
    model.print_architecture()
    
    # Analyze model
    analysis = analyze_model_3()
    print(f"\nModel Analysis:")
    print(f"Parameters: {analysis['total_parameters']:,}")
    print(f"Receptive Field: {analysis['receptive_field']}")
    print(f"Target: {analysis['target_accuracy']}")
    print(f"Strategy: {analysis['architecture_efficiency']}")