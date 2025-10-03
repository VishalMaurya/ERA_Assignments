"""
Parameter Validation for Improved Ultra-Efficient Models
========================================================

This script validates the parameter counts for the improved models
without requiring PyTorch installation by calculating parameters manually.
"""

def calculate_conv2d_params(in_channels, out_channels, kernel_size, bias=True, groups=1):
    """Calculate parameters for a Conv2d layer"""
    if isinstance(kernel_size, int):
        kernel_size = (kernel_size, kernel_size)
    
    weight_params = (in_channels // groups) * out_channels * kernel_size[0] * kernel_size[1]
    bias_params = out_channels if bias else 0
    
    return weight_params + bias_params

def calculate_batchnorm2d_params(num_features):
    """Calculate parameters for a BatchNorm2d layer"""
    return 2 * num_features

def calculate_linear_params(in_features, out_features, bias=True):
    """Calculate parameters for a Linear layer"""
    weight_params = in_features * out_features
    bias_params = out_features if bias else 0
    return weight_params + bias_params

def calculate_depthwise_separable_params(in_channels, out_channels, kernel_size=3, bias=False):
    """Calculate parameters for depthwise separable convolution"""
    # Depthwise conv: in_channels groups, each with 1 input channel
    depthwise_params = calculate_conv2d_params(in_channels, in_channels, kernel_size, bias, groups=in_channels)
    # Pointwise conv: 1x1 conv
    pointwise_params = calculate_conv2d_params(in_channels, out_channels, 1, bias)
    return depthwise_params + pointwise_params

def calculate_se_block_params(channels, reduction=4):
    """Calculate parameters for Squeeze-and-Excitation block"""
    hidden_channels = max(channels // reduction, 4)
    fc1_params = calculate_linear_params(channels, hidden_channels, bias=True)
    fc2_params = calculate_linear_params(hidden_channels, channels, bias=True)
    return fc1_params + fc2_params

def validate_improved_model_1():
    """
    ImprovedModel_1: Ultra-Lightweight with Modern Techniques
    Expected Parameters: <3000
    """
    total_params = 0
    
    print("📊 ImprovedModel_1 Parameter Analysis")
    print("-" * 50)
    
    # Block 1: Initial feature extraction
    conv1_params = calculate_conv2d_params(1, 12, 3, bias=False)
    bn1_params = calculate_batchnorm2d_params(12)
    block1_params = conv1_params + bn1_params
    total_params += block1_params
    print(f"Block 1 (conv1 + bn1): {block1_params} parameters")
    
    # Block 2: Depthwise separable conv
    dw_conv_params = calculate_depthwise_separable_params(12, 20, 3, bias=False)
    bn2_params = calculate_batchnorm2d_params(20)
    se1_params = calculate_se_block_params(20, reduction=4)
    block2_params = dw_conv_params + bn2_params + se1_params
    total_params += block2_params
    print(f"Block 2 (dw_conv + bn2 + se1): {block2_params} parameters")
    
    # Block 3: Final feature extraction
    conv3_params = calculate_conv2d_params(20, 10, 3, bias=False)
    total_params += conv3_params
    print(f"Block 3 (conv3): {conv3_params} parameters")
    
    return total_params

def validate_improved_model_2():
    """
    ImprovedModel_2: Balanced Efficiency with Advanced Features
    Expected Parameters: <6000
    """
    total_params = 0
    
    print("📊 ImprovedModel_2 Parameter Analysis")
    print("-" * 50)
    
    # Block 1: Initial features
    conv1_params = calculate_conv2d_params(1, 16, 3, bias=False)
    bn1_params = calculate_batchnorm2d_params(16)
    block1_params = conv1_params + bn1_params
    total_params += block1_params
    print(f"Block 1 (conv1 + bn1): {block1_params} parameters")
    
    # Block 2: Depthwise separable with residual
    dw_conv1_params = calculate_depthwise_separable_params(16, 24, 3, bias=False)
    bn2_params = calculate_batchnorm2d_params(24)
    se1_params = calculate_se_block_params(24, reduction=6)
    residual_proj1_params = calculate_conv2d_params(16, 24, 1, bias=False)
    block2_params = dw_conv1_params + bn2_params + se1_params + residual_proj1_params
    total_params += block2_params
    print(f"Block 2 (dw_conv + bn + se + residual): {block2_params} parameters")
    
    # Block 3: Dilated conv
    conv3_params = calculate_conv2d_params(24, 32, 3, bias=False)  # Dilated conv same params as regular
    bn3_params = calculate_batchnorm2d_params(32)
    se2_params = calculate_se_block_params(32, reduction=8)
    block3_params = conv3_params + bn3_params + se2_params
    total_params += block3_params
    print(f"Block 3 (dilated_conv + bn + se): {block3_params} parameters")
    
    # Block 4: Final compression
    conv4_params = calculate_conv2d_params(32, 10, 1, bias=False)
    total_params += conv4_params
    print(f"Block 4 (conv4): {conv4_params} parameters")
    
    return total_params

def validate_improved_model_3():
    """
    ImprovedModel_3: Maximum Performance Architecture
    Expected Parameters: <8000
    """
    total_params = 0
    
    print("📊 ImprovedModel_3 Parameter Analysis")
    print("-" * 50)
    
    # Block 1: Multi-scale initial features
    conv1_1x1_params = calculate_conv2d_params(1, 4, 1, bias=False)
    conv1_3x3_params = calculate_conv2d_params(1, 8, 3, bias=False)
    conv1_5x5_params = calculate_conv2d_params(1, 4, 5, bias=False)
    bn1_params = calculate_batchnorm2d_params(16)
    block1_params = conv1_1x1_params + conv1_3x3_params + conv1_5x5_params + bn1_params
    total_params += block1_params
    print(f"Block 1 (multi-scale + bn1): {block1_params} parameters")
    
    # Block 2: Enhanced residual block
    dw_conv1_params = calculate_depthwise_separable_params(16, 24, 3, bias=False)
    bn2_params = calculate_batchnorm2d_params(24)
    se1_params = calculate_se_block_params(24, reduction=6)
    residual_proj1_params = calculate_conv2d_params(16, 24, 1, bias=False)
    block2_params = dw_conv1_params + bn2_params + se1_params + residual_proj1_params
    total_params += block2_params
    print(f"Block 2 (enhanced residual): {block2_params} parameters")
    
    # Block 3: Ghost convolution (approximation)
    # Ghost conv: primary_conv + cheap_conv
    primary_channels = 32 // 2  # 16
    ghost_primary_params = calculate_conv2d_params(24, primary_channels, 3, bias=False)
    ghost_cheap_params = calculate_conv2d_params(primary_channels, 32 - primary_channels, 3, bias=False, groups=primary_channels)
    bn3_params = calculate_batchnorm2d_params(32)
    se2_params = calculate_se_block_params(32, reduction=8)
    block3_params = ghost_primary_params + ghost_cheap_params + bn3_params + se2_params
    total_params += block3_params
    print(f"Block 3 (ghost conv + bn + se): {block3_params} parameters")
    
    # Block 4: Spatial attention + conv
    spatial_att_params = calculate_conv2d_params(32, 1, 7, bias=False)
    conv4_params = calculate_conv2d_params(32, 16, 3, bias=False)
    bn4_params = calculate_batchnorm2d_params(16)
    block4_params = spatial_att_params + conv4_params + bn4_params
    total_params += block4_params
    print(f"Block 4 (spatial attention + conv): {block4_params} parameters")
    
    # Final projection
    final_conv_params = calculate_conv2d_params(16, 10, 1, bias=False)
    total_params += final_conv_params
    print(f"Final projection: {final_conv_params} parameters")
    
    return total_params

def main():
    """Validate all improved models"""
    print("🚀 Improved Ultra-Efficient Models Parameter Validation")
    print("=" * 70)
    
    models = [
        ("ImprovedModel_1", validate_improved_model_1, 3000),
        ("ImprovedModel_2", validate_improved_model_2, 6000),
        ("ImprovedModel_3", validate_improved_model_3, 8000)
    ]
    
    all_passed = True
    results = []
    
    for model_name, validator, target_params in models:
        print(f"\n🔍 {model_name} Analysis")
        print("=" * 70)
        
        actual_params = validator()
        
        print(f"\n📈 {model_name} Summary:")
        print(f"   Target: <{target_params:,} parameters")
        print(f"   Actual: {actual_params:,} parameters")
        print(f"   Difference: {actual_params - target_params:+,}")
        
        # Check if within 8000 parameter limit
        if actual_params < 8000:
            margin = 8000 - actual_params
            print(f"   ✅ PASS: {actual_params:,} < 8,000 (margin: +{margin:,})")
            results.append((model_name, actual_params, True, margin))
        else:
            excess = actual_params - 8000
            print(f"   ❌ FAIL: {actual_params:,} > 8,000 (excess: +{excess:,})")
            results.append((model_name, actual_params, False, -excess))
            all_passed = False
        
        print()
    
    # Summary comparison
    print("=" * 70)
    print("📊 COMPARISON WITH ORIGINAL MODELS")
    print("=" * 70)
    
    original_params = [2746, 7522, 7138]
    
    print(f"{'Model':<18} {'Original':<10} {'Improved':<10} {'Change':<10} {'Status':<8}")
    print("-" * 70)
    
    for i, (model_name, improved_params, passed, margin) in enumerate(results):
        orig_params = original_params[i]
        change = improved_params - orig_params
        change_pct = (change / orig_params) * 100
        status = "✅" if passed else "❌"
        
        print(f"{model_name:<18} {orig_params:<10,} {improved_params:<10,} {change:+5,} ({change_pct:+4.1f}%) {status:<8}")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL IMPROVED MODELS PASSED! All models are under 8,000 parameter limit.")
        print("✅ Ready for training with enhanced architectures!")
    else:
        print("⚠️  Some improved models exceed the parameter limit. Architecture needs adjustment.")
    
    print("\n🔧 Key Improvements Applied:")
    print("   • SiLU/Swish activations instead of ReLU")
    print("   • Depthwise separable convolutions for efficiency")
    print("   • Squeeze-and-Excitation (SE) attention blocks")
    print("   • Enhanced residual connections")
    print("   • Multi-scale feature extraction")
    print("   • Ghost convolutions for parameter efficiency")
    print("   • Spatial attention mechanisms")
    print("   • Dilated convolutions for larger receptive fields")
    
    print(f"\n🎯 Expected Performance Improvements:")
    print("   • Better gradient flow (SiLU + residuals)")
    print("   • Enhanced feature representation (attention)")
    print("   • Improved parameter efficiency (depthwise separable)")
    print("   • Larger effective receptive fields (dilated conv)")

if __name__ == "__main__":
    main()
