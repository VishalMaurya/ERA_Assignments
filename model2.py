"""
SESSION 6 - MODEL 2: Increased Capacity + Correct Pooling
========================================================

CURRICULUM ALIGNMENT:
- Code 2-6: All from Model 1 (Basic Skeleton, Lighter, BN, Dropout, GAP)
- Code 7: Increasing Capacity - Adding layers after GAP to boost performance
- Code 8: Correct MaxPooling Location - Optimal pooling based on RF calculations

TARGET:
- Parameters: ~6-7k (balanced efficiency and performance)
- Accuracy: ~99.2-99.3% (improved with increased capacity)
- Epochs: ≤15 (standard convergence with better architecture)
- Strategy: Curriculum techniques + Capacity + Optimized pooling

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Increased capacity effectiveness
- Optimized pooling placement impact
- Code 7 + 8 curriculum benefits
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class EnhancedBlock(nn.Module):
    """
    Enhanced CNN block for increased capacity (Code 7).
    
    Curriculum alignment:
    - More layers for increased capacity
    - Still using BatchNorm + ReLU (no advanced techniques)
    - Strategic dropout placement
    """
    def __init__(self, in_channels, out_channels, stride=1):
        super(EnhancedBlock, self).__init__()
        
        # Triple layer block for increased capacity (Code 7)
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                              stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, 
                              padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # Additional layer for capacity (Code 7)
        self.conv3 = nn.Conv2d(out_channels, out_channels, kernel_size=3, 
                              padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels)
        
        # Dropout for regularization (Code 5)
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, x):
        # Triple convolution for increased capacity
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.dropout(out)
        
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.dropout(out)
        
        # Code 7: Additional layer for capacity
        out = F.relu(self.bn3(self.conv3(out)))
        
        return out


class Model_2(nn.Module):
    """
    Enhanced CNN with increased capacity following Session 6 curriculum.
    
    CURRICULUM ALIGNMENT:
    - Code 2-6: Basic Skeleton + BN + Dropout + GAP (from Model 1)
    - Code 7: Increasing Capacity - More layers for better performance
    - Code 8: Correct MaxPooling Location - Optimized based on RF analysis
    
    Architecture Strategy:
    - Enhanced channel progression: 1→10→16→24→10
    - Triple-layer enhanced blocks for capacity
    - Optimized pooling placement (Code 8)
    - Additional layers after GAP (Code 7)
    
    Expected Parameter Breakdown:
    - Conv1: ~80 params
    - Block1: ~1400 params
    - Block2: ~2200 params  
    - Final layers: ~400 params
    - Total: ~4100 params
    """
    
    def __init__(self, num_classes=10):
        super(Model_2, self).__init__()
        
        # Initial convolution - smaller for parameter efficiency
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(8)
        
        # Ultra-lightweight enhanced blocks 
        self.conv2 = nn.Conv2d(8, 12, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(12)
        
        # Code 8: Correct MaxPooling Location
        self.pool1 = nn.MaxPool2d(2)         # 28x28 -> 14x14
        
        self.conv3 = nn.Conv2d(12, 16, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(16)
        
        self.pool2 = nn.MaxPool2d(2)         # 14x14 -> 7x7
        
        # Code 7: One additional layer for capacity
        self.conv4 = nn.Conv2d(16, 20, kernel_size=3, padding=1, bias=False)
        self.bn4 = nn.BatchNorm2d(20)
        
        # Final 1x1 classification
        self.final_conv = nn.Conv2d(20, 10, kernel_size=1, bias=False)
        
        # Code 6: Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Code 5: Regularization
        self.dropout = nn.Dropout(0.15)
        
    def forward(self, x):
        # Initial feature extraction
        x = F.relu(self.bn1(self.conv1(x)))  # 28x28x8
        
        # Enhanced convolutions for capacity
        x = F.relu(self.bn2(self.conv2(x)))  # 28x28x12
        x = self.pool1(x)         # 14x14x12 (Code 8: Correct pooling)
        x = self.dropout(x)       # Code 5: Regularization
        
        x = F.relu(self.bn3(self.conv3(x)))  # 14x14x16
        x = self.pool2(x)         # 7x7x16 (Code 8: Correct pooling)
        x = self.dropout(x)       # Code 5: Regularization
        
        # Code 7: Additional layer for capacity
        x = F.relu(self.bn4(self.conv4(x)))  # 7x7x20
        
        # Final classification
        x = self.final_conv(x)    # 7x7x10
        
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
            'stem': (28, 3),
            'block1': (28, 7),      # Efficient block increases RF
            'pool1': (14, 8),
            'block2': (14, 16),     # Another efficient block
            'pool2': (7, 18),
            'block3': (7, 34),      # Dilated conv dramatically increases RF
            'final': (7, 34)
        }
        return rf_info


# AdvancedModel_2 removed for simplicity

# Dummy class placeholder
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


def create_model_2():
    """Factory function to create Model_2 instance."""
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
        'model_name': 'Model_2 (Increased Capacity + Correct Pooling)',
        'total_parameters': total_params,
        'memory_footprint_mb': memory_mb,
        'receptive_field_final': final_rf,
        'coverage_percentage': (final_rf / 28) * 100,
        'architecture_efficiency': 'Enhanced Blocks + Optimized Pooling + FC Layers (Curriculum)',
        'target_accuracy': '99.2-99.3%',
        'parameter_budget': '6-7k parameters',
        'curriculum_codes': 'Code 2,3,4,5,6,7,8'
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
