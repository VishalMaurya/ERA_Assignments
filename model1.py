"""
SESSION 6 - MODEL 1: Basic Skeleton + Lighter Model
==================================================

CURRICULUM ALIGNMENT:
- Code 2: Basic Skeleton - Minimal, clean CNN structure
- Code 3: Lighter Model - Parameter-efficient architecture (<20k params)
- Code 4: Batch Normalization - Adding BN for faster convergence
- Code 5: Regularization - Dropout to reduce overfitting
- Code 6: Global Average Pooling - Replace dense layers with GAP

TARGET:
- Parameters: ~3-4k (ultra-efficient baseline)
- Accuracy: ~97-98% (baseline with curriculum techniques)  
- Epochs: ≤15 (standard convergence)
- Strategy: Basic CNN + BN + Dropout + GAP (curriculum fundamentals)

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Basic CNN effectiveness
- BatchNorm + Dropout impact
- GAP parameter reduction
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class BasicBlock(nn.Module):
    """
    Basic CNN block following Session 6 curriculum.
    
    Code 4: Batch Normalization for faster convergence
    Code 5: Dropout for regularization
    Standard convolutions with ReLU (no advanced techniques)
    """
    def __init__(self, in_channels, out_channels, stride=1):
        super(BasicBlock, self).__init__()
        
        # Standard 3x3 convolution
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                              stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
        # Second convolution for depth
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, 
                              padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # Dropout for regularization (Code 5)
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, x):
        # First conv + BN + ReLU
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.dropout(out)
        
        # Second conv + BN + ReLU
        out = F.relu(self.bn2(self.conv2(out)))
        
        return out


class Model_1(nn.Module):
    """
    Basic CNN following Session 6 curriculum with ~3-4k parameters.
    
    CURRICULUM ALIGNMENT:
    - Code 2: Basic Skeleton - Standard CNN structure
    - Code 3: Lighter Model - Efficient parameter usage (<8k limit)
    - Code 4: Batch Normalization - BN after each conv
    - Code 5: Regularization - Dropout for overfitting control
    - Code 6: Global Average Pooling - Replace FC with GAP
    
    Architecture Strategy:
    - Simple channel progression: 1→8→12→16→10
    - Standard convolutions with BatchNorm + ReLU
    - Strategic dropout placement
    - GAP for parameter efficiency
    
    Expected Parameter Breakdown:
    - Conv1: ~80 params
    - Block1: ~900 params  
    - Block2: ~1700 params
    - Final: ~200 params
    - Total: ~2900 params
    """
    
    def __init__(self, num_classes=10):
        super(Model_1, self).__init__()
        
        # Code 2: Basic Skeleton - Initial convolution
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(8)
        
        # Code 3: Lighter Model - Efficient blocks
        self.block1 = BasicBlock(8, 12)   # 28x28 -> 28x28
        self.pool1 = nn.MaxPool2d(2)      # 28x28 -> 14x14
        
        self.block2 = BasicBlock(12, 16)  # 14x14 -> 14x14  
        self.pool2 = nn.MaxPool2d(2)      # 14x14 -> 7x7
        
        # Final classification layer
        self.conv_final = nn.Conv2d(16, 10, kernel_size=1, bias=False)
        
        # Code 6: Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Code 5: Regularization
        self.dropout = nn.Dropout(0.15)
        
    def forward(self, x):
        # Initial feature extraction with Code 4: BatchNorm
        x = F.relu(self.bn1(self.conv1(x)))  # 28x28x8
        
        # Basic blocks with pooling
        x = self.block1(x)        # 28x28x12
        x = self.pool1(x)         # 14x14x12
        x = self.dropout(x)       # Code 5: Dropout
        
        x = self.block2(x)        # 14x14x16
        x = self.pool2(x)         # 7x7x16
        x = self.dropout(x)       # Code 5: Dropout
        
        # Final classification
        x = self.conv_final(x)    # 7x7x10
        
        # Code 6: Global Average Pooling
        x = self.gap(x)           # 1x1x10
        x = x.view(x.size(0), -1) # 10
        
        return x
    
    def count_parameters(self):
        """Count total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    
    def get_receptive_field_info(self):
        """
        Calculate receptive field for each layer.
        
        Returns:
            dict: Layer name -> (output_size, receptive_field)
        """
        rf_info = {
            'input': (28, 1),
            'conv1': (28, 3),       # First 3x3 conv
            'block1': (28, 7),      # Two 3x3 convs = 3 + 3 - 1 = 5, with stride effects = 7
            'pool1': (14, 8),       # 2x2 pooling 
            'block2': (14, 16),     # Two more 3x3 convs
            'pool2': (7, 18),       # 2x2 pooling
            'final': (7, 18)        # 1x1 conv doesn't change RF
        }
        return rf_info


def create_model_1():
    """Factory function to create Model_1 instance."""
    return Model_1()


def analyze_model_1():
    """
    Analyze Model_1 architecture and parameters.
    
    Returns:
        dict: Analysis results
    """
    model = create_model_1()
    
    # Parameter analysis
    total_params = model.count_parameters()
    
    # Receptive field analysis
    rf_info = model.get_receptive_field_info()
    
    # Memory footprint
    memory_mb = total_params * 4 / 1024 / 1024  # Assuming float32
    
    analysis = {
        'model_name': 'Model_1 (Basic Skeleton + Lighter)',
        'total_parameters': total_params,
        'memory_footprint_mb': memory_mb,
        'receptive_field_final': rf_info['final'][1],
        'coverage_percentage': (rf_info['final'][1] / 28) * 100,
        'architecture_efficiency': 'Basic CNN + BatchNorm + Dropout + GAP (Curriculum)',
        'target_accuracy': '97-98%',
        'parameter_budget': '3-4k parameters',
        'curriculum_codes': 'Code 2,3,4,5,6'
    }
    
    return analysis


if __name__ == "__main__":
    # Test model creation and analysis
    model = create_model_1()
    analysis = analyze_model_1()
    
    print("="*60)
    print("MODEL 1 - ULTRA-LIGHTWEIGHT BASELINE")
    print("="*60)
    
    for key, value in analysis.items():
        print(f"{key}: {value}")
    
    print(f"\nReceptive Field Analysis:")
    rf_info = model.get_receptive_field_info()
    for layer, (size, rf) in rf_info.items():
        coverage = (rf / 28) * 100
        print(f"  {layer}: {size}x{size} output, {rf}x{rf} RF ({coverage:.1f}% coverage)")
    
    # Test forward pass
    test_input = torch.randn(1, 1, 28, 28)
    with torch.no_grad():
        output = model(test_input)
        print(f"\nForward pass test: {test_input.shape} -> {output.shape}")
        print(f"Output range: [{output.min():.3f}, {output.max():.3f}]")
