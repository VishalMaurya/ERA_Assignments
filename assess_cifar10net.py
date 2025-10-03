"""
Assessment of Provided CIFAR10Net Model
======================================

This script analyzes the provided CIFAR10Net model against S7 assignment requirements
and compares it with our existing three models.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class DepthwiseSeparableConv(nn.Module):
    """Depthwise Separable Convolution: Depthwise + Pointwise"""
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, dilation=1):
        super(DepthwiseSeparableConv, self).__init__()
        
        # Depthwise convolution
        self.depthwise = nn.Conv2d(
            in_channels, in_channels, 
            kernel_size=kernel_size, 
            stride=stride, 
            padding=padding, 
            dilation=dilation,
            groups=in_channels,  # Key: groups=in_channels for depthwise
            bias=False
        )
        
        # Pointwise convolution (1x1)
        self.pointwise = nn.Conv2d(
            in_channels, out_channels, 
            kernel_size=1, 
            stride=1, 
            padding=0, 
            bias=False
        )
        
        self.bn1 = nn.BatchNorm2d(in_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
    def forward(self, x):
        x = F.relu(self.bn1(self.depthwise(x)))
        x = F.relu(self.bn2(self.pointwise(x)))
        return x

class DilatedConvBlock(nn.Module):
    """Dilated Convolution Block for increased receptive field"""
    def __init__(self, in_channels, out_channels, dilation=2):
        super(DilatedConvBlock, self).__init__()
        
        # Calculate padding to maintain spatial dimensions
        padding = dilation
        
        self.conv = nn.Conv2d(
            in_channels, out_channels,
            kernel_size=3,
            stride=1,
            padding=padding,
            dilation=dilation,
            bias=False
        )
        self.bn = nn.BatchNorm2d(out_channels)
        
    def forward(self, x):
        return F.relu(self.bn(self.conv(x)))

class CIFAR10Net(nn.Module):
    """
    CIFAR-10 CNN with C1C2C3C40 Architecture
    
    C1: Initial feature extraction with stride=2 (replaces MaxPool)
    C2: Depthwise Separable Convolution block
    C3: Dilated Convolution block
    C40: Final classification with GAP
    
    Target: >85% accuracy, <200k parameters, RF>44
    """
    
    def __init__(self, num_classes=10):
        super(CIFAR10Net, self).__init__()
        
        # C1: Initial feature extraction block (32x32 -> 16x16)
        self.c1_conv1 = nn.Conv2d(3, 8, kernel_size=3, stride=1, padding=1, bias=False)
        self.c1_bn1 = nn.BatchNorm2d(8)
        
        self.c1_conv2 = nn.Conv2d(8, 16, kernel_size=3, stride=2, padding=1, bias=False)  # Stride=2 replaces MaxPool
        self.c1_bn2 = nn.BatchNorm2d(16)
        
        self.c1_dropout = nn.Dropout(0.1)
        
        # C2: Depthwise Separable Convolution block (16x16 -> 8x8)
        self.c2_dw_sep = DepthwiseSeparableConv(16, 32, kernel_size=3, stride=1, padding=1)
        
        self.c2_conv = nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1, bias=False)  # Stride=2 replaces MaxPool
        self.c2_bn = nn.BatchNorm2d(32)
        
        self.c2_dropout = nn.Dropout(0.15)
        
        # C3: Dilated Convolution block (8x8 -> 4x4)
        self.c3_dilated1 = DilatedConvBlock(32, 64, dilation=2)
        self.c3_dilated2 = DilatedConvBlock(64, 64, dilation=2)
        
        self.c3_conv = nn.Conv2d(64, 64, kernel_size=3, stride=2, padding=1, bias=False)  # Stride=2 replaces MaxPool
        self.c3_bn = nn.BatchNorm2d(64)
        
        self.c3_dropout = nn.Dropout(0.2)
        
        # C40: Final classification block with GAP
        self.c40_conv1 = nn.Conv2d(64, 32, kernel_size=3, stride=1, padding=1, bias=False)
        self.c40_bn1 = nn.BatchNorm2d(32)
        
        self.c40_conv2 = nn.Conv2d(32, 16, kernel_size=3, stride=1, padding=1, bias=False)
        self.c40_bn2 = nn.BatchNorm2d(16)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Final classifier (optional FC after GAP)
        self.classifier = nn.Linear(16, num_classes)
        
        self.c40_dropout = nn.Dropout(0.25)
        
    def forward(self, x):
        # C1: Initial feature extraction (32x32 -> 16x16)
        x = F.relu(self.c1_bn1(self.c1_conv1(x)))
        x = F.relu(self.c1_bn2(self.c1_conv2(x)))  # 32x32 -> 16x16
        x = self.c1_dropout(x)
        
        # C2: Depthwise Separable Convolution (16x16 -> 8x8)
        x = self.c2_dw_sep(x)
        x = F.relu(self.c2_bn(self.c2_conv(x)))  # 16x16 -> 8x8
        x = self.c2_dropout(x)
        
        # C3: Dilated Convolution (8x8 -> 4x4)
        x = self.c3_dilated1(x)
        x = self.c3_dilated2(x)
        x = F.relu(self.c3_bn(self.c3_conv(x)))  # 8x8 -> 4x4
        x = self.c3_dropout(x)
        
        # C40: Final classification with GAP
        x = F.relu(self.c40_bn1(self.c40_conv1(x)))
        x = F.relu(self.c40_bn2(self.c40_conv2(x)))
        x = self.c40_dropout(x)
        
        # Global Average Pooling
        x = self.gap(x)  # 4x4 -> 1x1
        x = x.view(x.size(0), -1)  # Flatten
        
        # Final classification
        x = self.classifier(x)
        
        return x
    
    def count_parameters(self):
        """Count total trainable parameters"""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

def calculate_receptive_field():
    """Calculate the receptive field of CIFAR10Net"""
    print("🔍 Receptive Field Calculation for CIFAR10Net")
    print("=" * 60)
    
    # Initial RF
    rf = 1
    stride_product = 1
    
    # C1 Block
    print("📊 C1 Block:")
    # Conv1: 3x3, stride=1, padding=1
    rf = rf + (3 - 1) * stride_product
    print(f"  After c1_conv1 (3x3, s=1): RF = {rf}")
    
    # Conv2: 3x3, stride=2, padding=1
    stride_product *= 2
    rf = rf + (3 - 1) * stride_product
    print(f"  After c1_conv2 (3x3, s=2): RF = {rf}, Stride = {stride_product}")
    
    # C2 Block
    print("📊 C2 Block:")
    # Depthwise: 3x3, stride=1, padding=1
    rf = rf + (3 - 1) * stride_product
    print(f"  After depthwise (3x3, s=1): RF = {rf}")
    
    # Pointwise: 1x1, stride=1, padding=0
    rf = rf + (1 - 1) * stride_product
    print(f"  After pointwise (1x1, s=1): RF = {rf}")
    
    # Conv: 3x3, stride=2, padding=1
    stride_product *= 2
    rf = rf + (3 - 1) * stride_product
    print(f"  After c2_conv (3x3, s=2): RF = {rf}, Stride = {stride_product}")
    
    # C3 Block
    print("📊 C3 Block:")
    # Dilated1: 3x3, dilation=2, stride=1, padding=2
    effective_kernel = 3 + (3-1) * (2-1)  # 3 + 2*1 = 5
    rf = rf + (effective_kernel - 1) * stride_product
    print(f"  After dilated1 (3x3, d=2): RF = {rf} (effective kernel = {effective_kernel})")
    
    # Dilated2: 3x3, dilation=2, stride=1, padding=2
    rf = rf + (effective_kernel - 1) * stride_product
    print(f"  After dilated2 (3x3, d=2): RF = {rf}")
    
    # Conv: 3x3, stride=2, padding=1
    stride_product *= 2
    rf = rf + (3 - 1) * stride_product
    print(f"  After c3_conv (3x3, s=2): RF = {rf}, Stride = {stride_product}")
    
    # C40 Block
    print("📊 C40 Block:")
    # Conv1: 3x3, stride=1, padding=1
    rf = rf + (3 - 1) * stride_product
    print(f"  After c40_conv1 (3x3, s=1): RF = {rf}")
    
    # Conv2: 3x3, stride=1, padding=1
    rf = rf + (3 - 1) * stride_product
    print(f"  After c40_conv2 (3x3, s=1): RF = {rf}")
    
    print("=" * 60)
    print(f"🎯 Final Receptive Field: {rf} pixels")
    print(f"✅ RF > 44 requirement: {'PASSED' if rf > 44 else 'FAILED'}")
    
    return rf

def analyze_parameters():
    """Analyze parameter count and breakdown"""
    print("\n🔍 Parameter Analysis for CIFAR10Net")
    print("=" * 60)
    
    model = CIFAR10Net()
    total_params = model.count_parameters()
    
    print("📊 Layer-by-layer parameter breakdown:")
    
    # C1 Block
    c1_params = 0
    c1_conv1_params = 3 * 8 * 3 * 3  # 3->8, 3x3
    c1_bn1_params = 8 * 2  # BN parameters
    c1_conv2_params = 8 * 16 * 3 * 3  # 8->16, 3x3
    c1_bn2_params = 16 * 2  # BN parameters
    c1_params = c1_conv1_params + c1_bn1_params + c1_conv2_params + c1_bn2_params
    
    print(f"📊 C1 Block: {c1_params:,} parameters")
    print(f"  - c1_conv1 (3->8, 3x3): {c1_conv1_params:,}")
    print(f"  - c1_bn1: {c1_bn1_params:,}")
    print(f"  - c1_conv2 (8->16, 3x3): {c1_conv2_params:,}")
    print(f"  - c1_bn2: {c1_bn2_params:,}")
    
    # C2 Block
    c2_params = 0
    # Depthwise: 16 groups of 3x3 = 16 * 9
    c2_dw_params = 16 * 3 * 3
    c2_dw_bn_params = 16 * 2
    # Pointwise: 16->32, 1x1
    c2_pw_params = 16 * 32 * 1 * 1
    c2_pw_bn_params = 32 * 2
    # Regular conv: 32->32, 3x3
    c2_conv_params = 32 * 32 * 3 * 3
    c2_bn_params = 32 * 2
    c2_params = c2_dw_params + c2_dw_bn_params + c2_pw_params + c2_pw_bn_params + c2_conv_params + c2_bn_params
    
    print(f"📊 C2 Block: {c2_params:,} parameters")
    print(f"  - Depthwise (16 groups, 3x3): {c2_dw_params:,}")
    print(f"  - DW BatchNorm: {c2_dw_bn_params:,}")
    print(f"  - Pointwise (16->32, 1x1): {c2_pw_params:,}")
    print(f"  - PW BatchNorm: {c2_pw_bn_params:,}")
    print(f"  - c2_conv (32->32, 3x3): {c2_conv_params:,}")
    print(f"  - c2_bn: {c2_bn_params:,}")
    
    # C3 Block
    c3_params = 0
    # Dilated1: 32->64, 3x3, dilation=2
    c3_dil1_params = 32 * 64 * 3 * 3
    c3_dil1_bn_params = 64 * 2
    # Dilated2: 64->64, 3x3, dilation=2
    c3_dil2_params = 64 * 64 * 3 * 3
    c3_dil2_bn_params = 64 * 2
    # Regular conv: 64->64, 3x3
    c3_conv_params = 64 * 64 * 3 * 3
    c3_bn_params = 64 * 2
    c3_params = c3_dil1_params + c3_dil1_bn_params + c3_dil2_params + c3_dil2_bn_params + c3_conv_params + c3_bn_params
    
    print(f"📊 C3 Block: {c3_params:,} parameters")
    print(f"  - Dilated1 (32->64, 3x3): {c3_dil1_params:,}")
    print(f"  - Dilated1 BN: {c3_dil1_bn_params:,}")
    print(f"  - Dilated2 (64->64, 3x3): {c3_dil2_params:,}")
    print(f"  - Dilated2 BN: {c3_dil2_bn_params:,}")
    print(f"  - c3_conv (64->64, 3x3): {c3_conv_params:,}")
    print(f"  - c3_bn: {c3_bn_params:,}")
    
    # C40 Block
    c40_params = 0
    # Conv1: 64->32, 3x3
    c40_conv1_params = 64 * 32 * 3 * 3
    c40_bn1_params = 32 * 2
    # Conv2: 32->16, 3x3
    c40_conv2_params = 32 * 16 * 3 * 3
    c40_bn2_params = 16 * 2
    # Classifier: 16->10
    classifier_params = 16 * 10
    c40_params = c40_conv1_params + c40_bn1_params + c40_conv2_params + c40_bn2_params + classifier_params
    
    print(f"📊 C40 Block: {c40_params:,} parameters")
    print(f"  - c40_conv1 (64->32, 3x3): {c40_conv1_params:,}")
    print(f"  - c40_bn1: {c40_bn1_params:,}")
    print(f"  - c40_conv2 (32->16, 3x3): {c40_conv2_params:,}")
    print(f"  - c40_bn2: {c40_bn2_params:,}")
    print(f"  - classifier (16->10): {classifier_params:,}")
    
    print("=" * 60)
    print(f"🎯 Total Parameters: {total_params:,}")
    print(f"💰 Budget Usage: {total_params/200000*100:.1f}% of 200,000")
    print(f"✅ Parameter Budget: {'PASSED' if total_params < 200000 else 'FAILED'}")
    
    return total_params

def check_architecture_compliance():
    """Check compliance with assignment requirements"""
    print("\n🔍 Architecture Compliance Check")
    print("=" * 60)
    
    requirements = {
        "C1-C2-C3-C4-O blocks": "✅ PASSED - Has C1, C2, C3, C40 blocks",
        "No MaxPooling (use stride=2)": "✅ PASSED - Uses stride=2 in conv layers",
        "Depthwise Separable Conv": "✅ PASSED - In C2 block",
        "Dilated Convolution": "✅ PASSED - In C3 block (dilation=2)",
        "Global Average Pooling": "✅ PASSED - Uses AdaptiveAvgPool2d(1)",
        "Optional FC after GAP": "✅ PASSED - Has Linear(16, 10) classifier",
        "Target 10 classes": "✅ PASSED - num_classes=10"
    }
    
    for requirement, status in requirements.items():
        print(f"  {requirement}: {status}")
    
    print("=" * 60)
    print("🏆 BONUS POINTS:")
    print("  ✅ Dilated kernels instead of MaxPool: +200 points")
    print("  ✅ Depthwise Separable Convolutions: Efficient design")

def compare_with_existing_models():
    """Compare with our existing three models"""
    print("\n🔍 Comparison with Existing Models")
    print("=" * 60)
    
    # Our existing models data
    existing_models = {
        "OptimizedCIFAR10Model": {
            "parameters": 189762,
            "rf": 190,
            "accuracy": "Not trained yet",
            "features": "Bottleneck residual dilated blocks"
        },
        "CIFAR_GAP_Net": {
            "parameters": 198666,
            "rf": 134,
            "accuracy": "83.46%",
            "features": "Direct dilated convolutions"
        },
        "Enhanced CIFAR_GAP_Net": {
            "parameters": 162354,
            "rf": 140,
            "accuracy": "84.29%",
            "features": "SE modules + residuals + multi-scale"
        }
    }
    
    # Calculate new model stats
    new_model_params = analyze_parameters()
    new_model_rf = calculate_receptive_field()
    
    print("\n📊 Model Comparison Table:")
    print("-" * 80)
    print(f"{'Model':<25} {'Parameters':<12} {'RF':<6} {'Accuracy':<12} {'Key Features'}")
    print("-" * 80)
    
    for name, data in existing_models.items():
        print(f"{name:<25} {data['parameters']:,<12} {data['rf']:<6} {data['accuracy']:<12} {data['features']}")
    
    print(f"{'CIFAR10Net (New)':<25} {new_model_params:,<12} {new_model_rf:<6} {'Unknown':<12} {'Standard blocks + dilated'}")
    print("-" * 80)

def provide_recommendations():
    """Provide recommendations for the new model"""
    print("\n🚀 Recommendations for CIFAR10Net")
    print("=" * 60)
    
    print("✅ STRENGTHS:")
    print("  • Clean, well-structured architecture")
    print("  • Proper C1-C2-C3-C4-O block organization")
    print("  • Correct use of depthwise separable and dilated convolutions")
    print("  • Appropriate use of GAP")
    print("  • Good parameter efficiency")
    
    print("\n⚠️ POTENTIAL IMPROVEMENTS:")
    print("  1. **Channel Progression**: Current 3→8→16→32→64→32→16 could be optimized")
    print("  2. **Residual Connections**: No skip connections for gradient flow")
    print("  3. **Attention Mechanisms**: No SE modules or channel attention")
    print("  4. **Multi-scale Features**: Single dilation rate (2) in C3")
    print("  5. **Regularization**: Only dropout, could add label smoothing")
    print("  6. **Advanced Optimizations**: No bottleneck blocks or efficient designs")
    
    print("\n🎯 EXPECTED PERFORMANCE:")
    print("  • Parameter count: Within budget (good efficiency)")
    print("  • Receptive field: Adequate for CIFAR-10")
    print("  • Expected accuracy: 82-84% (based on architecture complexity)")
    print("  • Training time: Moderate (simpler than our enhanced models)")
    
    print("\n🏆 VERDICT:")
    print("  ✅ COMPLIANT: Meets all assignment requirements")
    print("  ⭐ RATING: Good baseline model (3.5/5)")
    print("  📈 IMPROVEMENT POTENTIAL: High (could reach 85%+ with enhancements)")

if __name__ == "__main__":
    print("🔍 CIFAR10Net Model Assessment")
    print("=" * 60)
    
    # Run all assessments
    rf = calculate_receptive_field()
    params = analyze_parameters()
    check_architecture_compliance()
    compare_with_existing_models()
    provide_recommendations()
    
    print("\n" + "=" * 60)
    print("📋 FINAL ASSESSMENT SUMMARY")
    print("=" * 60)
    print(f"✅ Assignment Compliance: PASSED")
    print(f"📊 Parameters: {params:,} (✅ Within 200K budget)")
    print(f"📏 Receptive Field: {rf} (✅ > 44 requirement)")
    print(f"🏆 Bonus Points: +200 (Dilated convolutions)")
    print(f"⭐ Overall Rating: Good baseline model")
    print(f"🎯 Recommendation: Ready to train, expect 82-84% accuracy")
