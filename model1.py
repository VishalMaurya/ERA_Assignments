"""
SESSION 6 - MODEL 1: Fast-Learning Baseline
==========================================

TARGET:
- Parameters: ~3-4k (ultra-efficient baseline)
- Accuracy: ~98-99% (improved target with fast architecture)  
- Epochs: ≤8 (fast convergence focus)
- Strategy: Residual connections, wider shallow network, fast activations

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Fast convergence analysis
- Residual connection effectiveness
- Gradient flow improvements
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class FastResidualBlock(nn.Module):
    """
    Fast-learning residual block with efficient design.
    
    Features:
    - Skip connections for gradient flow
    - SiLU activation for better gradients  
    - Inverted bottleneck design for efficiency
    - GroupNorm for faster convergence
    """
    def __init__(self, in_channels, out_channels, expansion=2, stride=1):
        super(FastResidualBlock, self).__init__()
        
        hidden_dim = in_channels * expansion
        
        # Inverted bottleneck: expand -> depthwise -> compress
        self.expand = nn.Sequential(
            nn.Conv2d(in_channels, hidden_dim, 1, bias=False),
            nn.GroupNorm(4, hidden_dim),  # GroupNorm for faster convergence
            nn.SiLU()  # SiLU for better gradients
        ) if expansion > 1 else nn.Identity()
        
        # Depthwise convolution
        self.depthwise = nn.Sequential(
            nn.Conv2d(hidden_dim, hidden_dim, 3, stride=stride, padding=1, 
                     groups=hidden_dim, bias=False),
            nn.GroupNorm(4, hidden_dim),
            nn.SiLU()
        )
        
        # Compress back
        self.compress = nn.Sequential(
            nn.Conv2d(hidden_dim, out_channels, 1, bias=False),
            nn.GroupNorm(4, out_channels)
        )
        
        # Skip connection
        self.skip = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.skip = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
                nn.GroupNorm(4, out_channels)
            )
    
    def forward(self, x):
        identity = self.skip(x)
        
        out = self.expand(x)
        out = self.depthwise(out)
        out = self.compress(out)
        
        # Residual connection
        out = out + identity
        return F.silu(out)  # SiLU for final activation


class Model_1(nn.Module):
    """
    Fast-Learning CNN for MNIST with ~3-4k parameters.
    
    Architecture Strategy:
    - Wider shallow network: 1→16→20→24→10 (fast learning)
    - Residual connections for gradient flow
    - SiLU activations for better gradients
    - GroupNorm for faster convergence
    - Only 2 pooling operations for speed
    
    Expected Parameter Breakdown:
    - Stem: ~300 params
    - Block 1: ~1200 params
    - Block 2: ~1500 params  
    - Final: ~300 params
    - Total: ~3300 params
    """
    
    def __init__(self, num_classes=10):
        super(Model_1, self).__init__()
        
        # Wider stem for faster feature learning
        self.stem = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1, bias=False),
            nn.GroupNorm(4, 16),
            nn.SiLU()
        )
        
        # Fast residual blocks - wider and shallower
        self.block1 = FastResidualBlock(16, 20, expansion=1, stride=1)  # 28x28
        self.pool1 = nn.MaxPool2d(2)  # 14x14
        
        self.block2 = FastResidualBlock(20, 24, expansion=1, stride=1)  # 14x14
        self.pool2 = nn.MaxPool2d(2)  # 7x7
        
        # Fast final layers
        self.final = nn.Sequential(
            nn.Conv2d(24, 16, kernel_size=3, padding=1, bias=False),
            nn.GroupNorm(4, 16),
            nn.SiLU(),
            nn.Conv2d(16, 10, kernel_size=1, bias=False)
        )
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(0.1)
        
    def forward(self, x):
        # Wide stem for fast feature extraction
        x = self.stem(x)          # 28x28x16
        
        # Residual blocks with skip connections
        x = self.block1(x)        # 28x28x20
        x = self.pool1(x)         # 14x14x20
        x = self.dropout(x)
        
        x = self.block2(x)        # 14x14x24
        x = self.pool2(x)         # 7x7x24
        x = self.dropout(x)
        
        # Fast final classification
        x = self.final(x)         # 7x7x10
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
            'block1': (28, 7),      # Residual block increases RF
            'pool1': (14, 8),
            'block2': (14, 16),     # Another residual block
            'pool2': (7, 18),
            'final': (7, 22)        # Final convolution
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
        'model_name': 'Model_1 (Fast-Learning Baseline)',
        'total_parameters': total_params,
        'memory_footprint_mb': memory_mb,
        'receptive_field_final': rf_info['final'][1],
        'coverage_percentage': (rf_info['final'][1] / 28) * 100,
        'architecture_efficiency': 'Residual Blocks + Wider Shallow + SiLU + GroupNorm',
        'target_accuracy': '98-99%',
        'parameter_budget': '3-4k parameters',
        'convergence_target': '≤8 epochs'
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
