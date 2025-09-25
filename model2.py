"""
SESSION 6 - MODEL 2: Optimized Efficiency
=========================================

TARGET:
- Parameters: ~6-7k (balanced efficiency and performance)
- Accuracy: ~99.2-99.3% (close to final target)
- Epochs: ≤15
- Strategy: Advanced techniques, optimal channel progression, dilated convolutions

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Advanced techniques effectiveness
- Parameter allocation optimization
- Receptive field vs accuracy trade-offs
- Final improvements needed for Model 3
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class EfficientBlock(nn.Module):
    """
    Efficient building block combining depthwise separable convolutions
    with squeeze-and-excitation style channel attention.
    """
    def __init__(self, in_channels, out_channels, stride=1, dilation=1):
        super(EfficientBlock, self).__init__()
        
        # Depthwise convolution with optional dilation
        self.depthwise = nn.Conv2d(
            in_channels, in_channels, kernel_size=3, 
            stride=stride, padding=dilation, dilation=dilation,
            groups=in_channels, bias=False
        )
        
        # Pointwise expansion
        self.pointwise1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
        # Optional squeeze-excitation (very lightweight)
        self.se_reduce = nn.Conv2d(out_channels, max(1, out_channels // 8), kernel_size=1)
        self.se_expand = nn.Conv2d(max(1, out_channels // 8), out_channels, kernel_size=1)
        
        # Final pointwise
        self.pointwise2 = nn.Conv2d(out_channels, out_channels, kernel_size=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # Skip connection if dimensions match
        self.skip = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.skip = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        identity = self.skip(x)
        
        # Main path
        out = self.depthwise(x)
        out = F.relu(self.bn1(self.pointwise1(out)))
        
        # Lightweight squeeze-excitation
        se = F.adaptive_avg_pool2d(out, 1)
        se = F.relu(self.se_reduce(se))
        se = torch.sigmoid(self.se_expand(se))
        out = out * se
        
        out = self.bn2(self.pointwise2(out))
        
        # Skip connection
        out += identity
        return F.relu(out)


class Model_2(nn.Module):
    """
    Optimized CNN for MNIST with ~6-7k parameters.
    
    Architecture Strategy:
    - Efficient blocks with attention mechanism
    - Strategic use of dilated convolutions
    - Optimized channel progression: 1→10→16→24→10
    - Mixed convolution types for efficiency
    - Enhanced receptive field management
    
    Expected Parameter Breakdown:
    - Stem: ~300 params
    - Block 1: ~1500 params
    - Block 2: ~2500 params  
    - Block 3: ~2000 params
    - Total: ~6300 params
    """
    
    def __init__(self, num_classes=10):
        super(Model_2, self).__init__()
        
        # Efficient stem
        self.stem = nn.Sequential(
            nn.Conv2d(1, 10, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(10),
            nn.ReLU()
        )
        
        # Efficient blocks with strategic design
        self.block1 = EfficientBlock(10, 16, stride=1)  # 28x28
        self.pool1 = nn.MaxPool2d(2)  # 14x14
        
        self.block2 = EfficientBlock(16, 24, stride=1, dilation=1)  # 14x14
        self.pool2 = nn.MaxPool2d(2)  # 7x7
        
        # Dilated convolution for larger receptive field without pooling
        self.block3 = EfficientBlock(24, 32, stride=1, dilation=2)  # 7x7, larger RF
        
        # Final feature compression
        self.final_conv = nn.Sequential(
            nn.Conv2d(32, 16, kernel_size=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 10, kernel_size=1, bias=False)
        )
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(0.15)
        
    def forward(self, x):
        # Stem
        x = self.stem(x)          # 28x28x10
        
        # Efficient blocks
        x = self.block1(x)        # 28x28x16
        x = self.pool1(x)         # 14x14x16
        x = self.dropout(x)
        
        x = self.block2(x)        # 14x14x24
        x = self.pool2(x)         # 7x7x24
        x = self.dropout(x)
        
        x = self.block3(x)        # 7x7x32 (dilated, larger RF)
        
        # Final compression and classification
        x = self.final_conv(x)    # 7x7x10
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
            'stem': (28, 3),
            'block1': (28, 7),      # Efficient block increases RF
            'pool1': (14, 8),
            'block2': (14, 16),     # Another efficient block
            'pool2': (7, 18),
            'block3': (7, 34),      # Dilated conv dramatically increases RF
            'final': (7, 34)
        }
        return rf_info


class AdvancedModel_2(nn.Module):
    """
    Alternative Model_2 with different optimization strategy.
    Uses group convolutions and channel shuffling.
    """
    
    def __init__(self, num_classes=10):
        super(AdvancedModel_2, self).__init__()
        
        # Initial feature extraction
        self.conv1 = nn.Conv2d(1, 12, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(12)
        
        # Group convolutions for efficiency
        self.group_conv1 = nn.Conv2d(12, 24, kernel_size=3, padding=1, groups=3, bias=False)
        self.bn2 = nn.BatchNorm2d(24)
        self.pool1 = nn.MaxPool2d(2)
        
        # Depthwise separable with channel attention
        self.depthwise = nn.Conv2d(24, 24, kernel_size=3, padding=1, groups=24, bias=False)
        self.pointwise = nn.Conv2d(24, 32, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(32)
        self.pool2 = nn.MaxPool2d(2)
        
        # Final layers
        self.conv_final = nn.Conv2d(32, 10, kernel_size=3, padding=0, bias=False)  # 7x7 -> 5x5
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(0.1)
        
    def channel_shuffle(self, x, groups):
        """Channel shuffle operation for group convolutions."""
        batch_size, channels, height, width = x.size()
        channels_per_group = channels // groups
        
        # Reshape and transpose
        x = x.view(batch_size, groups, channels_per_group, height, width)
        x = x.transpose(1, 2).contiguous()
        x = x.view(batch_size, channels, height, width)
        
        return x
    
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))      # 28x28x12
        
        x = F.relu(self.bn2(self.group_conv1(x))) # 28x28x24
        x = self.channel_shuffle(x, 3)           # Shuffle channels
        x = self.pool1(x)                        # 14x14x24
        x = self.dropout(x)
        
        x = self.depthwise(x)                    # 14x14x24
        x = F.relu(self.bn3(self.pointwise(x))) # 14x14x32
        x = self.pool2(x)                        # 7x7x32
        x = self.dropout(x)
        
        x = self.conv_final(x)                   # 5x5x10
        x = self.gap(x)                          # 1x1x10
        x = x.view(x.size(0), -1)               # 10
        
        return x
    
    def count_parameters(self):
        """Count total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def create_model_2(variant='default'):
    """Factory function to create Model_2 instance."""
    if variant == 'advanced':
        return AdvancedModel_2()
    return Model_2()


def analyze_model_2(variant='default'):
    """
    Analyze Model_2 architecture and parameters.
    
    Returns:
        dict: Analysis results
    """
    model = create_model_2(variant)
    
    # Parameter analysis
    total_params = model.count_parameters()
    
    # Receptive field analysis (for default variant)
    if hasattr(model, 'get_receptive_field_info'):
        rf_info = model.get_receptive_field_info()
        final_rf = rf_info['final'][1]
    else:
        final_rf = 34  # Estimated for advanced variant
    
    # Memory footprint
    memory_mb = total_params * 4 / 1024 / 1024  # Assuming float32
    
    analysis = {
        'model_name': f'Model_2 ({variant.title()})',
        'total_parameters': total_params,
        'memory_footprint_mb': memory_mb,
        'receptive_field_final': final_rf,
        'coverage_percentage': (final_rf / 28) * 100,
        'architecture_efficiency': 'Efficient Blocks + Attention + Dilated Conv',
        'target_accuracy': '99.2-99.3%',
        'parameter_budget': '6-7k parameters'
    }
    
    return analysis


if __name__ == "__main__":
    # Test both variants
    variants = ['default', 'advanced']
    
    for variant in variants:
        model = create_model_2(variant)
        analysis = analyze_model_2(variant)
        
        print("="*60)
        print(f"MODEL 2 - OPTIMIZED EFFICIENCY ({variant.upper()})")
        print("="*60)
        
        for key, value in analysis.items():
            print(f"{key}: {value}")
        
        if hasattr(model, 'get_receptive_field_info'):
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
        
        print("\n")
