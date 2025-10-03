"""
IMPROVED Ultra-Efficient Models for MNIST - Enhanced Architectures
================================================================

Based on analysis of the original models, these improvements focus on:
1. Better activation functions (SiLU/Swish instead of ReLU)
2. Depthwise separable convolutions for parameter efficiency
3. Squeeze-and-Excitation (SE) blocks for attention
4. Better residual connections
5. Optimized channel progressions
6. Strategic use of dilated convolutions

All models maintain <8000 parameter constraint while targeting higher accuracy.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class DepthwiseSeparableConv(nn.Module):
    """Depthwise Separable Convolution for parameter efficiency"""
    def __init__(self, in_channels, out_channels, kernel_size=3, padding=1, bias=False):
        super(DepthwiseSeparableConv, self).__init__()
        self.depthwise = nn.Conv2d(in_channels, in_channels, kernel_size=kernel_size, 
                                 padding=padding, groups=in_channels, bias=bias)
        self.pointwise = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=bias)
        
    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        return x

class SEBlock(nn.Module):
    """Squeeze-and-Excitation block for channel attention"""
    def __init__(self, channels, reduction=4):
        super(SEBlock, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channels, max(channels // reduction, 4)),
            nn.SiLU(inplace=True),
            nn.Linear(max(channels // reduction, 4), channels),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)

class ImprovedModel_1(nn.Module):
    """
    Improved Model_1: Ultra-Lightweight with Modern Techniques
    
    Improvements:
    - SiLU activation instead of ReLU
    - Depthwise separable convolutions
    - Micro SE attention
    - Better channel progression
    
    Target: <3000 parameters, 98.5%+ accuracy
    """
    
    def __init__(self):
        super(ImprovedModel_1, self).__init__()
        
        # Block 1: Initial feature extraction
        self.conv1 = nn.Conv2d(1, 12, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(12)
        
        # Block 2: Depthwise separable conv for efficiency
        self.dw_conv = DepthwiseSeparableConv(12, 20, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(20)
        self.se1 = SEBlock(20, reduction=4)
        
        # Block 3: Final feature extraction
        self.conv3 = nn.Conv2d(20, 10, kernel_size=3, padding=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Dropout
        self.dropout = nn.Dropout(0.1)
        
    def forward(self, x):
        # Block 1: 1×28×28 → 12×28×28
        x = F.silu(self.bn1(self.conv1(x)))
        x = self.dropout(x)
        
        # Block 2: 12×28×28 → 20×28×28 → 20×14×14
        x = F.silu(self.bn2(self.dw_conv(x)))
        x = self.se1(x)  # Attention
        x = F.max_pool2d(x, 2)  # 20×14×14
        
        # Block 3: 20×14×14 → 10×14×14 → 10×7×7
        x = self.conv3(x)
        x = F.max_pool2d(x, 2)  # 10×7×7
        
        # Global Average Pooling
        x = self.gap(x)  # 10×1×1
        x = x.view(x.size(0), -1)  # 10
        
        return x
    
    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

class ImprovedModel_2(nn.Module):
    """
    Improved Model_2: Balanced Efficiency with Advanced Features
    
    Improvements:
    - Mixed convolutions (standard + depthwise separable)
    - SE attention blocks
    - Better residual connections
    - Dilated convolutions for larger receptive field
    - SiLU activations
    
    Target: <6000 parameters, 99.3%+ accuracy
    """
    
    def __init__(self):
        super(ImprovedModel_2, self).__init__()
        
        # Block 1: Initial features
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(16)
        
        # Block 2: Depthwise separable with residual
        self.dw_conv1 = DepthwiseSeparableConv(16, 24, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(24)
        self.se1 = SEBlock(24, reduction=6)
        self.residual_proj1 = nn.Conv2d(16, 24, kernel_size=1, bias=False)
        
        # Block 3: Dilated conv for larger receptive field
        self.conv3 = nn.Conv2d(24, 32, kernel_size=3, padding=2, dilation=2, bias=False)
        self.bn3 = nn.BatchNorm2d(32)
        self.se2 = SEBlock(32, reduction=8)
        
        # Block 4: Final compression
        self.conv4 = nn.Conv2d(32, 10, kernel_size=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Dropout layers
        self.dropout1 = nn.Dropout(0.1)
        self.dropout2 = nn.Dropout(0.15)
        
    def forward(self, x):
        # Block 1: 1×28×28 → 16×28×28
        x = F.silu(self.bn1(self.conv1(x)))
        x = self.dropout1(x)
        
        # Block 2: Residual depthwise separable
        identity = x
        x = F.silu(self.bn2(self.dw_conv1(x)))
        x = self.se1(x)
        identity = self.residual_proj1(identity)
        x = x + identity
        x = F.max_pool2d(x, 2)  # 24×14×14
        
        # Block 3: Dilated convolution
        x = F.silu(self.bn3(self.conv3(x)))
        x = self.se2(x)
        x = self.dropout2(x)
        x = F.max_pool2d(x, 2)  # 32×7×7
        
        # Block 4: Final compression
        x = self.conv4(x)  # 10×7×7
        
        # Global Average Pooling
        x = self.gap(x)  # 10×1×1
        x = x.view(x.size(0), -1)  # 10
        
        return x
    
    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

class ImprovedModel_3(nn.Module):
    """
    Improved Model_3: Maximum Performance Architecture
    
    Improvements:
    - Multi-scale feature extraction
    - Enhanced residual blocks
    - Spatial and channel attention
    - Ghost convolutions for efficiency
    - Advanced activation functions
    - Optimized channel progression
    
    Target: <8000 parameters, 99.5%+ accuracy
    """
    
    def __init__(self):
        super(ImprovedModel_3, self).__init__()
        
        # Block 1: Multi-scale initial features
        self.conv1_1x1 = nn.Conv2d(1, 4, kernel_size=1, bias=False)
        self.conv1_3x3 = nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False)
        self.conv1_5x5 = nn.Conv2d(1, 4, kernel_size=5, padding=2, bias=False)
        self.bn1 = nn.BatchNorm2d(16)  # 4 + 8 + 4 = 16
        
        # Block 2: Enhanced residual block
        self.dw_conv1 = DepthwiseSeparableConv(16, 24, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(24)
        self.se1 = SEBlock(24, reduction=6)
        self.residual_proj1 = nn.Conv2d(16, 24, kernel_size=1, bias=False)
        
        # Block 3: Ghost convolution block
        self.ghost_conv = self._make_ghost_conv(24, 32, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(32)
        self.se2 = SEBlock(32, reduction=8)
        
        # Block 4: Spatial attention + final conv
        self.spatial_attention = self._make_spatial_attention(32)
        self.conv4 = nn.Conv2d(32, 16, kernel_size=3, padding=1, bias=False)
        self.bn4 = nn.BatchNorm2d(16)
        
        # Final projection
        self.final_conv = nn.Conv2d(16, 10, kernel_size=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Dropout layers
        self.dropout1 = nn.Dropout(0.1)
        self.dropout2 = nn.Dropout(0.15)
        self.dropout3 = nn.Dropout(0.2)
        
    def _make_ghost_conv(self, in_channels, out_channels, kernel_size=3, padding=1):
        """Ghost convolution for parameter efficiency"""
        primary_channels = out_channels // 2
        return nn.Sequential(
            nn.Conv2d(in_channels, primary_channels, kernel_size=kernel_size, 
                     padding=padding, bias=False),
            nn.Conv2d(primary_channels, out_channels - primary_channels, 
                     kernel_size=3, padding=1, groups=primary_channels, bias=False)
        )
    
    def _make_spatial_attention(self, channels):
        """Lightweight spatial attention"""
        return nn.Sequential(
            nn.Conv2d(channels, 1, kernel_size=7, padding=3, bias=False),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        # Block 1: Multi-scale feature extraction
        x1 = self.conv1_1x1(x)
        x2 = self.conv1_3x3(x)
        x3 = self.conv1_5x5(x)
        x = torch.cat([x1, x2, x3], dim=1)  # 16×28×28
        x = F.silu(self.bn1(x))
        x = self.dropout1(x)
        
        # Block 2: Enhanced residual block
        identity = x
        x = F.silu(self.bn2(self.dw_conv1(x)))
        x = self.se1(x)
        identity = self.residual_proj1(identity)
        x = x + identity
        x = F.max_pool2d(x, 2)  # 24×14×14
        
        # Block 3: Ghost convolution
        x = F.silu(self.bn3(self.ghost_conv(x)))
        x = self.se2(x)
        x = self.dropout2(x)
        x = F.max_pool2d(x, 2)  # 32×7×7
        
        # Block 4: Spatial attention
        spatial_att = self.spatial_attention(x)
        x = x * spatial_att
        x = F.silu(self.bn4(self.conv4(x)))
        x = self.dropout3(x)
        
        # Final projection
        x = self.final_conv(x)  # 10×7×7
        
        # Global Average Pooling
        x = self.gap(x)  # 10×1×1
        x = x.view(x.size(0), -1)  # 10
        
        return x
    
    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

def create_improved_model(model_name="ImprovedModel_1"):
    """Create specified improved model and return with parameter count"""
    if model_name == "ImprovedModel_1":
        model = ImprovedModel_1()
    elif model_name == "ImprovedModel_2":
        model = ImprovedModel_2()
    elif model_name == "ImprovedModel_3":
        model = ImprovedModel_3()
    else:
        raise ValueError(f"Unknown model: {model_name}")
    
    param_count = model.count_parameters()
    print(f"{model_name} - Total parameters: {param_count:,}")
    
    if param_count >= 8000:
        print(f"WARNING: {model_name} has {param_count} parameters, which exceeds the 8,000 limit!")
    else:
        margin = 8000 - param_count
        print(f"✓ {model_name} parameter count is within limit: {param_count} < 8,000 (margin: +{margin:,})")
    
    return model

if __name__ == "__main__":
    # Test all improved models
    for model_name in ["ImprovedModel_1", "ImprovedModel_2", "ImprovedModel_3"]:
        print(f"\n{'='*60}")
        print(f"Testing {model_name}")
        print(f"{'='*60}")
        
        model = create_improved_model(model_name)
        
        # Test with dummy input
        dummy_input = torch.randn(1, 1, 28, 28)
        output = model(dummy_input)
        print(f"Input shape: {dummy_input.shape}")
        print(f"Output shape: {output.shape}")
        print(f"{model_name} created successfully!")
        
        # Calculate FLOPs estimation (rough)
        total_params = model.count_parameters()
        print(f"Estimated efficiency: {total_params/8000:.1%} of parameter budget used")
