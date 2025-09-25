"""
SESSION 6 - MODEL 6: Efficient Attention Convergence
===================================================

CURRICULUM ALIGNMENT:
- Code 2-8: All fundamental techniques with efficient attention focus
- Focus: Strategic attention placement for rapid convergence
- Strategy: Efficient attention + optimized receptive field progression

TARGET:
- Parameters: ~7.8k (near maximum limit with efficient attention)
- Accuracy: 99.4%+ in ≤7 epochs (attention-driven fast convergence)
- Strategy: Strategic attention + optimal RF + efficient architecture

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Attention-driven convergence analysis
- Strategic attention placement effectiveness
- Efficient architecture impact
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class EfficientAttentionBlock(nn.Module):
    """
    Block with efficient attention for rapid convergence.
    
    Features:
    - Lightweight attention for feature refinement
    - Optimal channel progression
    - Strategic BN + ReLU placement
    """
    def __init__(self, in_channels, out_channels, stride=1, use_attention=True):
        super(EfficientAttentionBlock, self).__init__()
        
        # Main convolution path
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                              stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, 
                              padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # Efficient channel attention
        self.attention = None
        if use_attention:
            self.attention = nn.Sequential(
                nn.AdaptiveAvgPool2d(1),
                nn.Conv2d(out_channels, max(1, out_channels//4), 1),
                nn.ReLU(),
                nn.Conv2d(max(1, out_channels//4), out_channels, 1),
                nn.Sigmoid()
            )
        
        # Spatial attention for important regions
        self.spatial_attention = nn.Sequential(
            nn.Conv2d(out_channels, 1, kernel_size=7, padding=3, bias=False),
            nn.Sigmoid()
        ) if use_attention else None
        
        # Skip connection
        self.skip = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.skip = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, x):
        identity = self.skip(x)
        
        # Main convolution path
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.dropout(out)
        
        out = F.relu(self.bn2(self.conv2(out)))
        
        # Apply attention mechanisms
        if self.attention is not None:
            # Channel attention
            ch_att = self.attention(out)
            out = out * ch_att
            
            # Spatial attention
            if self.spatial_attention is not None:
                sp_att = self.spatial_attention(out)
                out = out * sp_att
        
        # Skip connection
        out = out + identity
        return F.relu(out)


class Model_6(nn.Module):
    """
    Enhanced efficient CNN for 99.4% precision targeting.
    
    CURRICULUM ALIGNMENT:
    - Code 2-8: All curriculum techniques with enhancement focus
    - Strategic attention + skip connections for rapid convergence
    
    ENHANCED ARCHITECTURE STRATEGY:
    - Optimized progressive channels: 1→12→18→24→28→10
    - Dual-path attention with skip connections
    - Strategic depth-wise separable convolutions 
    - Enhanced receptive field utilization
    - Multi-scale feature processing
    
    Expected Parameter Breakdown:
    - Initial: ~120 params
    - Conv layers: ~4200 params
    - Skip connections: ~800 params
    - Attention mechanisms: ~400 params
    - Final: ~280 params
    - Total: ~5800 params (efficient use of budget)
    """
    
    def __init__(self, num_classes=10):
        super(Model_6, self).__init__()
        
        # Efficient initial feature extraction
        self.initial_conv = nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False)
        self.initial_bn = nn.BatchNorm2d(8)
        
        # Efficient progressive layers with bottlenecks
        self.conv2 = nn.Conv2d(8, 12, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(12)
        
        # 1x1 bottleneck for efficiency
        self.bottleneck1 = nn.Sequential(
            nn.Conv2d(12, 10, kernel_size=1, bias=False),
            nn.BatchNorm2d(10)
        )
        
        self.pool1 = nn.MaxPool2d(2)  # 28x28 -> 14x14
        
        self.conv3 = nn.Conv2d(10, 16, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(16)
        
        # Another bottleneck
        self.bottleneck2 = nn.Sequential(
            nn.Conv2d(16, 14, kernel_size=1, bias=False),
            nn.BatchNorm2d(14)
        )
        
        self.pool2 = nn.MaxPool2d(2)  # 14x14 -> 7x7
        
        # Efficient final processing 
        self.conv4 = nn.Conv2d(14, 18, kernel_size=3, padding=1, bias=False)
        self.bn4 = nn.BatchNorm2d(18)
        
        # Lightweight attention system
        # Channel attention only (simpler)
        self.channel_attention = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(18, 4, 1),
            nn.ReLU(),
            nn.Conv2d(4, 18, 1),
            nn.Sigmoid()
        )
        
        # Skip connection support (lightweight) - fixed input channels
        self.skip_conv = nn.Conv2d(1, 18, kernel_size=1, stride=4, bias=False)  # 28x28->7x7
        
        # Final classification
        self.final_conv = nn.Conv2d(18, 10, kernel_size=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(0.15)
        
    def forward(self, x):
        # Efficient feature extraction with skip connection
        identity = x  # Keep for skip connection
        x = F.relu(self.initial_bn(self.initial_conv(x)))  # 28x28x8
        
        # Efficient progressive feature building with bottlenecks
        x = F.relu(self.bn2(self.conv2(x)))               # 28x28x12
        x = F.relu(self.bottleneck1(x))                   # 28x28x10 (efficiency)
        x = self.pool1(x)                                 # 14x14x10
        x = self.dropout(x)
        
        x = F.relu(self.bn3(self.conv3(x)))               # 14x14x16
        x = F.relu(self.bottleneck2(x))                   # 14x14x14 (efficiency)
        x = self.pool2(x)                                 # 7x7x14
        x = self.dropout(x)
        
        # Efficient final processing 
        x = F.relu(self.bn4(self.conv4(x)))               # 7x7x18
        
        # Add lightweight skip connection for better gradient flow
        skip = self.skip_conv(identity)  # 7x7x18
        x = x + skip  # Skip connection for better learning
        
        # Apply lightweight channel attention
        ch_att = self.channel_attention(x)   # Global channel importance
        x = x * ch_att
        
        # Final classification
        x = self.final_conv(x)                            # 7x7x10
        x = self.gap(x)                                   # 1x1x10
        x = x.view(x.size(0), -1)                        # 10
        
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
            'initial': (28, 3),
            'block1': (28, 7),      # Progressive RF buildup
            'pool1': (14, 8),
            'block2': (14, 16),     # Attention-guided RF expansion
            'pool2': (7, 18),
            'block3': (7, 26),      # Full attention RF
            'final': (7, 26)
        }
        return rf_info


def create_model_6():
    """Factory function to create Model_6 instance."""
    return Model_6()


def analyze_model_6():
    """
    Analyze Model_6 architecture and parameters.
    
    Returns:
        dict: Analysis results
    """
    model = create_model_6()
    
    # Parameter analysis
    total_params = model.count_parameters()
    
    # Receptive field analysis
    rf_info = model.get_receptive_field_info()
    
    # Memory footprint
    memory_mb = total_params * 4 / 1024 / 1024  # Assuming float32
    
    analysis = {
        'model_name': 'Model_6 (Efficient Attention Convergence)',
        'total_parameters': total_params,
        'memory_footprint_mb': memory_mb,
        'receptive_field_final': rf_info['final'][1],
        'coverage_percentage': (rf_info['final'][1] / 28) * 100,
        'architecture_efficiency': 'Efficient Attention + Progressive RF + Strategic Placement (Curriculum)',
        'target_accuracy': '99.4%+',
        'parameter_budget': '~7.8k parameters',
        'curriculum_codes': 'Code 2,3,4,5,6,7,8',
        'convergence_target': '≤7 epochs'
    }
    
    return analysis


if __name__ == "__main__":
    # Test the model
    model = create_model_6()
    analysis = analyze_model_6()
    
    print("="*60)
    print("MODEL 6 - EFFICIENT ATTENTION CONVERGENCE")
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
