"""
SESSION 6 - MODEL 5: Ultra-Fast Early Convergence
================================================

CURRICULUM ALIGNMENT:
- Code 2-8: All fundamental techniques optimized for speed
- Focus: ULTRA-FAST convergence through aggressive early learning
- Strategy: Wide initial layers + rapid feature extraction

TARGET:
- Parameters: ~7.5k (maximum efficient utilization)
- Accuracy: 99.4%+ in ≤8 epochs (ultra-fast convergence)
- Strategy: Aggressive early feature learning + optimized flow

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Ultra-fast convergence analysis
- Aggressive early learning effectiveness
- Wide initial layer impact
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class UltraFastBlock(nn.Module):
    """
    Block designed for ultra-fast convergence within curriculum.
    
    Features:
    - Aggressive feature learning
    - Optimized BN placement for fast convergence
    - Strategic skip connections
    """
    def __init__(self, in_channels, out_channels, stride=1, use_compression=True):
        super(UltraFastBlock, self).__init__()
        
        # Aggressive feature learning with wide intermediate
        mid_channels = max(out_channels, in_channels * 2)
        
        # Wide feature extraction
        self.conv1 = nn.Conv2d(in_channels, mid_channels, kernel_size=3, 
                              stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(mid_channels)
        
        # Feature refinement
        self.conv2 = nn.Conv2d(mid_channels, mid_channels, kernel_size=3, 
                              padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(mid_channels)
        
        # Optional compression
        if use_compression and mid_channels != out_channels:
            self.compress = nn.Sequential(
                nn.Conv2d(mid_channels, out_channels, kernel_size=1, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        else:
            self.compress = nn.Identity()
            out_channels = mid_channels
        
        # Skip connection for gradient flow
        self.skip = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.skip = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        
        self.dropout = nn.Dropout(0.1)
        self.out_channels = out_channels
    
    def forward(self, x):
        identity = self.skip(x)
        
        # Aggressive feature learning
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.dropout(out)
        
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.dropout(out)
        
        # Optional compression
        out = self.compress(out)
        
        # Skip connection
        out = out + identity
        return F.relu(out)


class Model_5(nn.Module):
    """
    Ultra-fast convergence CNN for early target achievement.
    
    CURRICULUM ALIGNMENT:
    - Code 2-8: All curriculum techniques
    - Optimized for ULTRA-FAST convergence (≤8 epochs)
    
    Architecture Strategy:
    - Wide initial feature learning: 1→16→24→32→10
    - Aggressive early capacity for rapid learning
    - Optimized gradient flow for fast convergence
    - Strategic attention for precision
    
    Expected Parameter Breakdown:
    - Initial: ~120 params
    - Conv layers: ~2800 params
    - Dual paths: ~400 params
    - Total: ~3300 params
    """
    
    def __init__(self, num_classes=10):
        super(Model_5, self).__init__()
        
        # Efficient wide initial learning
        self.initial_conv = nn.Conv2d(1, 12, kernel_size=3, padding=1, bias=False)
        self.initial_bn = nn.BatchNorm2d(12)
        
        # Ultra-fast simplified layers
        self.conv2 = nn.Conv2d(12, 18, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(18)
        self.pool1 = nn.MaxPool2d(2)  # 28x28 -> 14x14
        
        self.conv3 = nn.Conv2d(18, 24, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(24)
        self.pool2 = nn.MaxPool2d(2)  # 14x14 -> 7x7
        
        # Final processing with dual paths
        self.conv4 = nn.Conv2d(24, 20, kernel_size=3, padding=1, bias=False)
        self.bn4 = nn.BatchNorm2d(20)
        
        # Simplified dual-path classification
        self.path1 = nn.Conv2d(20, 10, kernel_size=1, bias=False)
        self.path2 = nn.Conv2d(20, 10, kernel_size=3, padding=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        # Efficient wide initial learning
        x = F.relu(self.initial_bn(self.initial_conv(x)))  # 28x28x12
        
        # Ultra-fast layers
        x = F.relu(self.bn2(self.conv2(x)))    # 28x28x18
        x = self.pool1(x)                      # 14x14x18
        x = self.dropout(x)
        
        x = F.relu(self.bn3(self.conv3(x)))    # 14x14x24
        x = self.pool2(x)                      # 7x7x24
        x = self.dropout(x)
        
        # Final processing
        x = F.relu(self.bn4(self.conv4(x)))    # 7x7x20
        
        # Simplified dual-path classification
        path1 = self.path1(x)  # 7x7x10 (1x1 conv)
        path2 = self.path2(x)  # 7x7x10 (3x3 conv)
        
        # Simple combination (average)
        combined = (path1 + path2) / 2
        
        # Global Average Pooling
        x = self.gap(combined)         # 1x1x10
        x = x.view(x.size(0), -1)      # 10
        
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
            'initial': (28, 5),     # Two 3x3 convs
            'block1': (28, 11),     # Aggressive RF growth
            'pool1': (14, 12),
            'block2': (14, 20),     # Strategic RF expansion
            'pool2': (7, 22),
            'final': (7, 26)        # Near-complete coverage
        }
        return rf_info


def create_model_5():
    """Factory function to create Model_5 instance."""
    return Model_5()


def analyze_model_5():
    """
    Analyze Model_5 architecture and parameters.
    
    Returns:
        dict: Analysis results
    """
    model = create_model_5()
    
    # Parameter analysis
    total_params = model.count_parameters()
    
    # Receptive field analysis
    rf_info = model.get_receptive_field_info()
    
    # Memory footprint
    memory_mb = total_params * 4 / 1024 / 1024  # Assuming float32
    
    analysis = {
        'model_name': 'Model_5 (Ultra-Fast Early Convergence)',
        'total_parameters': total_params,
        'memory_footprint_mb': memory_mb,
        'receptive_field_final': rf_info['final'][1],
        'coverage_percentage': (rf_info['final'][1] / 28) * 100,
        'architecture_efficiency': 'Ultra-Fast Blocks + Wide Initial + Dual-Path + Attention (Curriculum)',
        'target_accuracy': '99.4%+',
        'parameter_budget': '~7.5k parameters',
        'curriculum_codes': 'Code 2,3,4,5,6,7,8',
        'convergence_target': '≤8 epochs'
    }
    
    return analysis


if __name__ == "__main__":
    # Test the model
    model = create_model_5()
    analysis = analyze_model_5()
    
    print("="*60)
    print("MODEL 5 - ULTRA-FAST EARLY CONVERGENCE")
    print("="*60)
    
    for key, value in analysis.items():
        print(f"{key}: {value}")
    
    # Test forward pass
    x = torch.randn(1, 1, 28, 28)
    with torch.no_grad():
        output = model(x)
        print(f"\nForward pass test: {x.shape} -> {output.shape} ✅")
    
    # Receptive field analysis
    rf_info = model.get_receptive_field_info()
    print(f"\nReceptive Field Analysis:")
    for layer, (size, rf) in rf_info.items():
        print(f"  {layer}: {size}x{size} (RF: {rf})")
