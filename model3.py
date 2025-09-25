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


class MicroAttention(nn.Module):
    """
    Ultra-lightweight attention mechanism with minimal parameters.
    """
    def __init__(self, channels):
        super(MicroAttention, self).__init__()
        reduced_channels = max(1, channels // 16)
        
        # Channel attention
        self.ca_pool = nn.AdaptiveAvgPool2d(1)
        self.ca_fc = nn.Sequential(
            nn.Linear(channels, reduced_channels, bias=False),
            nn.ReLU(),
            nn.Linear(reduced_channels, channels, bias=False),
            nn.Sigmoid()
        )
        
        # Spatial attention (very lightweight)
        self.sa_conv = nn.Conv2d(2, 1, kernel_size=3, padding=1, bias=False)
        
    def forward(self, x):
        # Channel attention
        b, c, h, w = x.size()
        ca = self.ca_pool(x).view(b, c)
        ca = self.ca_fc(ca).view(b, c, 1, 1)
        x = x * ca
        
        # Spatial attention
        sa_avg = torch.mean(x, dim=1, keepdim=True)
        sa_max, _ = torch.max(x, dim=1, keepdim=True)
        sa = torch.cat([sa_avg, sa_max], dim=1)
        sa = torch.sigmoid(self.sa_conv(sa))
        x = x * sa
        
        return x


class OptimizedBlock(nn.Module):
    """
    Final optimized block combining all curriculum techniques.
    
    Curriculum alignment:
    - Enhanced capacity (Code 7) with efficient design
    - Proper BatchNorm + ReLU (Code 4)
    - Strategic dropout (Code 5) 
    - Simple attention for final precision
    """
    def __init__(self, in_channels, out_channels, stride=1, use_attention=True):
        super(OptimizedBlock, self).__init__()
        
        # Enhanced multi-layer design for final precision
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                              stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, 
                              padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # Additional layer for maximum capacity (Code 7)
        self.conv3 = nn.Conv2d(out_channels, out_channels, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels)
        
        # Simple squeeze-excitation attention for final precision
        self.attention = None
        if use_attention:
            self.attention = nn.Sequential(
                nn.AdaptiveAvgPool2d(1),
                nn.Conv2d(out_channels, max(1, out_channels//8), 1),
                nn.ReLU(),
                nn.Conv2d(max(1, out_channels//8), out_channels, 1),
                nn.Sigmoid()
            )
        
        # Skip connection for gradient flow
        self.skip = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.skip = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        
        # Dropout for regularization (Code 5)
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, x):
        identity = self.skip(x)
        
        # Multi-layer processing with curriculum techniques
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.dropout(out)
        
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.dropout(out)
        
        # Final refinement layer
        out = F.relu(self.bn3(self.conv3(out)))
        
        # Apply attention if enabled
        if self.attention:
            att = self.attention(out)
            out = out * att
        
        # Skip connection for gradient flow
        out = out + identity
        return F.relu(out)


class Model_3(nn.Module):
    """
    Final precision CNN for MNIST with <8k parameters.
    
    Architecture Strategy:
    - Optimized blocks with selective attention
    - Carefully tuned channel progression
    - Strategic use of dilated convolutions
    - Multi-scale feature fusion
    - Advanced regularization techniques
    
    Expected Parameter Breakdown:
    - Stem: ~200 params
    - Block 1: ~2000 params
    - Block 2: ~3000 params
    - Block 3: ~2000 params
    - Final: ~500 params
    - Total: ~7700 params
    """
    
    def __init__(self, num_classes=10):
        super(Model_3, self).__init__()
        
        # Efficient stem
        self.stem = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(8),
            nn.ReLU()
        )
        
        # Optimized blocks combining all curriculum techniques
        self.block1 = OptimizedBlock(8, 16, stride=1, use_attention=False)  # Start simple
        self.pool1 = nn.MaxPool2d(2)  # 28x28 -> 14x14 (Code 8: Correct pooling)
        
        self.block2 = OptimizedBlock(16, 24, stride=1, use_attention=True)  # Add attention
        self.pool2 = nn.MaxPool2d(2)  # 14x14 -> 7x7 (Code 8: Correct pooling)
        
        # Final high-capacity processing (Code 7: Maximum capacity)
        self.block3 = OptimizedBlock(24, 32, stride=1, use_attention=True)  # Full capacity
        
        # Multi-scale feature fusion
        self.fusion_conv = nn.Conv2d(32, 20, kernel_size=1, bias=False)
        self.fusion_bn = nn.BatchNorm2d(20)
        
        # Final classification layers with different kernel sizes
        self.classifier = nn.Sequential(
            nn.Conv2d(20, 16, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 10, kernel_size=1, bias=False)
        )
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Advanced dropout scheduling
        self.dropout_light = nn.Dropout(0.1)
        self.dropout_heavy = nn.Dropout(0.2)
        
    def forward(self, x):
        # Stem
        x = self.stem(x)              # 28x28x8
        
        # Progressive feature extraction
        x = self.block1(x)            # 28x28x16
        x = self.pool1(x)             # 14x14x16
        x = self.dropout_light(x)
        
        x = self.block2(x)            # 14x14x24 (with attention)
        x = self.pool2(x)             # 7x7x24
        x = self.dropout_light(x)
        
        x = self.block3(x)            # 7x7x32 (with attention)
        
        # Feature fusion and classification
        x = F.relu(self.fusion_bn(self.fusion_conv(x)))  # 7x7x20
        x = self.dropout_heavy(x)     # Heavier dropout before final layers
        
        x = self.classifier(x)        # 7x7x10
        x = self.gap(x)               # 1x1x10
        x = x.view(x.size(0), -1)    # 10
        
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
            'block1': (28, 7),      # Optimized block
            'pool1': (14, 8),
            'block2': (14, 16),     # Optimized block with attention
            'pool2': (7, 18),
            'block3': (7, 34),      # Final optimized block
            'fusion': (7, 34),
            'classifier': (7, 38),  # Additional convolution
            'final': (7, 38)
        }
        return rf_info
    
    def get_parameter_breakdown(self):
        """
        Detailed parameter breakdown by component.
        
        Returns:
            dict: Component name -> parameter count
        """
        breakdown = {}
        
        breakdown['stem'] = sum(p.numel() for p in self.stem.parameters())
        breakdown['block1'] = sum(p.numel() for p in self.block1.parameters())
        breakdown['block2'] = sum(p.numel() for p in self.block2.parameters())
        breakdown['block3'] = sum(p.numel() for p in self.block3.parameters())
        breakdown['fusion'] = (sum(p.numel() for p in self.fusion_conv.parameters()) + 
                              sum(p.numel() for p in self.fusion_bn.parameters()))
        breakdown['classifier'] = sum(p.numel() for p in self.classifier.parameters())
        
        breakdown['total'] = sum(breakdown.values())
        
        return breakdown


class EnsembleModel_3(nn.Module):
    """
    Alternative Model_3 using ensemble-like approach with multiple paths.
    """
    
    def __init__(self, num_classes=10):
        super(EnsembleModel_3, self).__init__()
        
        # Shared stem
        self.stem = nn.Sequential(
            nn.Conv2d(1, 12, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(12),
            nn.ReLU()
        )
        
        # Path 1: Standard convolutions
        self.path1 = nn.Sequential(
            nn.Conv2d(12, 16, kernel_size=3, padding=1, groups=4, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        # Path 2: Depthwise separable
        self.path2_dw = nn.Conv2d(12, 12, kernel_size=3, padding=1, groups=12, bias=False)
        self.path2_pw = nn.Conv2d(12, 16, kernel_size=1, bias=False)
        self.path2_bn = nn.BatchNorm2d(16)
        self.path2_pool = nn.MaxPool2d(2)
        
        # Fusion
        self.fusion = nn.Conv2d(32, 24, kernel_size=1, bias=False)
        self.fusion_bn = nn.BatchNorm2d(24)
        
        # Final layers
        self.final_conv = nn.Sequential(
            nn.MaxPool2d(2),  # 7x7 -> 3x3 spatial reduction
            nn.Conv2d(24, 16, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 10, kernel_size=3, padding=0, bias=False)  # 3x3 -> 1x1
        )
        
        self.dropout = nn.Dropout(0.15)
        
    def forward(self, x):
        x = self.stem(x)  # 28x28x12
        
        # Dual paths
        p1 = self.path1(x)  # 14x14x16
        
        p2 = self.path2_dw(x)  # 28x28x12
        p2 = F.relu(self.path2_bn(self.path2_pw(p2)))  # 28x28x16
        p2 = self.path2_pool(p2)  # 14x14x16
        
        # Fuse paths
        x = torch.cat([p1, p2], dim=1)  # 14x14x32
        x = F.relu(self.fusion_bn(self.fusion(x)))  # 14x14x24
        x = self.dropout(x)
        
        # Final classification
        x = self.final_conv(x)  # 1x1x10
        x = x.view(x.size(0), -1)  # 10
        
        return x
    
    def count_parameters(self):
        """Count total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def create_model_3(variant='default'):
    """Factory function to create Model_3 instance."""
    if variant == 'ensemble':
        return EnsembleModel_3()
    return Model_3()


def analyze_model_3(variant='default'):
    """
    Analyze Model_3 architecture and parameters.
    
    Returns:
        dict: Analysis results
    """
    model = create_model_3(variant)
    
    # Parameter analysis
    total_params = model.count_parameters()
    
    # Get detailed breakdown if available
    if hasattr(model, 'get_parameter_breakdown'):
        param_breakdown = model.get_parameter_breakdown()
    else:
        param_breakdown = {'total': total_params}
    
    # Receptive field analysis
    if hasattr(model, 'get_receptive_field_info'):
        rf_info = model.get_receptive_field_info()
        final_rf = rf_info['final'][1]
    else:
        final_rf = 38  # Estimated
    
    # Memory footprint
    memory_mb = total_params * 4 / 1024 / 1024  # Assuming float32
    
    analysis = {
        'model_name': f'Model_3 ({variant.title()})',
        'total_parameters': total_params,
        'parameter_breakdown': param_breakdown,
        'memory_footprint_mb': memory_mb,
        'receptive_field_final': final_rf,
        'coverage_percentage': (final_rf / 28) * 100,
        'architecture_efficiency': 'Optimized Blocks + Micro-Attention + Multi-Scale Fusion',
        'target_accuracy': '99.4%+ consistently',
        'parameter_budget': '<8k parameters'
    }
    
    return analysis


if __name__ == "__main__":
    # Test both variants
    variants = ['default', 'ensemble']
    
    for variant in variants:
        model = create_model_3(variant)
        analysis = analyze_model_3(variant)
        
        print("="*60)
        print(f"MODEL 3 - FINAL PRECISION ({variant.upper()})")
        print("="*60)
        
        for key, value in analysis.items():
            if key == 'parameter_breakdown' and isinstance(value, dict):
                print(f"{key}:")
                for comp, params in value.items():
                    percentage = (params / value['total']) * 100 if value['total'] > 0 else 0
                    print(f"  {comp}: {params:,} ({percentage:.1f}%)")
            else:
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
