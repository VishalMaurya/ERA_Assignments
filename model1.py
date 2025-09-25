"""
SESSION 6 - MODEL 1: Ultra-Lightweight Baseline
==============================================

TARGET:
- Parameters: ~3-4k (ultra-efficient baseline)
- Accuracy: ~97-98% (establish minimum viable architecture)  
- Epochs: ≤15
- Strategy: Depthwise separable convolutions, minimal channels

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Parameter efficiency analysis
- Bottlenecks identified  
- Improvements for Model 2
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class DepthwiseSeparableConv(nn.Module):
    """
    Depthwise Separable Convolution for parameter efficiency.
    
    Standard conv: in_ch * out_ch * k * k parameters
    Depthwise sep: in_ch * k * k + in_ch * out_ch parameters
    Reduction: ~8-9x fewer parameters for 3x3 convolutions
    """
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
        super(DepthwiseSeparableConv, self).__init__()
        
        # Depthwise convolution (one filter per input channel)
        self.depthwise = nn.Conv2d(
            in_channels, in_channels, kernel_size=kernel_size,
            stride=stride, padding=padding, groups=in_channels, bias=False
        )
        
        # Pointwise convolution (1x1 conv to combine channels)
        self.pointwise = nn.Conv2d(
            in_channels, out_channels, kernel_size=1, bias=False
        )
        
        self.bn = nn.BatchNorm2d(out_channels)
        
    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        x = self.bn(x)
        return F.relu(x)


class Model_1(nn.Module):
    """
    Ultra-Lightweight CNN for MNIST with ~3-4k parameters.
    
    Architecture Strategy:
    - Minimal channel progression: 1→8→12→16→10
    - Depthwise separable convolutions for efficiency
    - Strategic pooling and GAP
    - No dense layers (GAP only)
    
    Expected Parameter Breakdown:
    - Block 1: ~200 params
    - Block 2: ~800 params  
    - Block 3: ~2000 params
    - Total: ~3000 params
    """
    
    def __init__(self, num_classes=10):
        super(Model_1, self).__init__()
        
        # Initial feature extraction (standard conv for first layer)
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(8)
        
        # Depthwise separable blocks for efficiency
        self.ds_conv1 = DepthwiseSeparableConv(8, 12)
        self.pool1 = nn.MaxPool2d(2)  # 28x28 → 14x14
        
        self.ds_conv2 = DepthwiseSeparableConv(12, 16)
        self.pool2 = nn.MaxPool2d(2)  # 14x14 → 7x7
        
        # Final feature refinement
        self.ds_conv3 = DepthwiseSeparableConv(16, 20)
        self.conv_final = nn.Conv2d(20, 10, kernel_size=1, bias=False)  # 1x1 to classes
        
        # Global Average Pooling (no FC layer)
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(0.1)
        
    def forward(self, x):
        # Initial feature extraction
        x = F.relu(self.bn1(self.conv1(x)))  # 28x28x8
        
        # Efficient depthwise separable blocks
        x = self.ds_conv1(x)      # 28x28x12
        x = self.pool1(x)         # 14x14x12
        x = self.dropout(x)
        
        x = self.ds_conv2(x)      # 14x14x16  
        x = self.pool2(x)         # 7x7x16
        x = self.dropout(x)
        
        x = self.ds_conv3(x)      # 7x7x20
        x = self.conv_final(x)    # 7x7x10
        
        # Global Average Pooling
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
            'conv1': (28, 3),
            'ds_conv1': (28, 5),
            'pool1': (14, 6),
            'ds_conv2': (14, 10),
            'pool2': (7, 12),
            'ds_conv3': (7, 16),
            'final': (7, 16)
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
        'model_name': 'Model_1 (Ultra-Lightweight)',
        'total_parameters': total_params,
        'memory_footprint_mb': memory_mb,
        'receptive_field_final': rf_info['final'][1],
        'coverage_percentage': (rf_info['final'][1] / 28) * 100,
        'architecture_efficiency': 'Depthwise Separable + Minimal Channels',
        'target_accuracy': '97-98%',
        'parameter_budget': '3-4k parameters'
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
