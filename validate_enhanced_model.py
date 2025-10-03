"""
Enhanced CIFAR_GAP_Net Parameter Validation
==========================================

PyTorch-independent validation of the enhanced model architecture
to ensure it stays within the 200K parameter limit.
"""

def calculate_conv2d_params(in_channels, out_channels, kernel_size, groups=1, bias=False):
    """Calculate parameters for Conv2d layer"""
    if isinstance(kernel_size, int):
        kernel_size = (kernel_size, kernel_size)
    
    # Weight parameters
    weight_params = (in_channels // groups) * out_channels * kernel_size[0] * kernel_size[1]
    
    # Bias parameters
    bias_params = out_channels if bias else 0
    
    return weight_params + bias_params

def calculate_batchnorm2d_params(num_features):
    """Calculate parameters for BatchNorm2d layer"""
    # Weight (gamma) + bias (beta)
    return num_features * 2

def calculate_linear_params(in_features, out_features, bias=True):
    """Calculate parameters for Linear layer"""
    weight_params = in_features * out_features
    bias_params = out_features if bias else 0
    return weight_params + bias_params

def calculate_se_module_params(channels, reduction=16):
    """Calculate parameters for SE module"""
    reduced_channels = max(channels // reduction, 4)
    
    # First conv: channels -> reduced_channels
    conv1_params = calculate_conv2d_params(channels, reduced_channels, 1, bias=False)
    
    # Second conv: reduced_channels -> channels
    conv2_params = calculate_conv2d_params(reduced_channels, channels, 1, bias=False)
    
    return conv1_params + conv2_params

def calculate_enhanced_depthwise_separable_params(in_ch, out_ch, kernel_size=3):
    """Calculate parameters for Enhanced Depthwise Separable Conv"""
    params = 0
    
    # First depthwise conv
    params += calculate_conv2d_params(in_ch, in_ch, kernel_size, groups=in_ch, bias=False)
    params += calculate_batchnorm2d_params(in_ch)
    
    # First pointwise conv
    params += calculate_conv2d_params(in_ch, in_ch, 1, bias=False)
    params += calculate_batchnorm2d_params(in_ch)
    
    # If channel change needed
    if in_ch != out_ch:
        # Second depthwise conv
        params += calculate_conv2d_params(in_ch, in_ch, kernel_size, groups=in_ch, bias=False)
        params += calculate_batchnorm2d_params(in_ch)
        
        # Second pointwise conv
        params += calculate_conv2d_params(in_ch, out_ch, 1, bias=False)
        params += calculate_batchnorm2d_params(out_ch)
    
    return params

def calculate_multiscale_dilated_block_params(channels):
    """Calculate parameters for Multi-scale Dilated Block"""
    branch_channels = channels // 4
    params = 0
    
    # Four branches (dilation 1, 2, 4, 8)
    for _ in range(4):
        # Conv + BN for each branch
        params += calculate_conv2d_params(channels, branch_channels, 3, bias=False)
        params += calculate_batchnorm2d_params(branch_channels)
    
    # Combine conv (channels -> channels)
    params += calculate_conv2d_params(channels, channels, 1, bias=False)
    params += calculate_batchnorm2d_params(channels)
    
    return params

def validate_enhanced_cifar_gap_net():
    """Validate Enhanced CIFAR_GAP_Net parameter count"""
    
    print("🔍 Enhanced CIFAR_GAP_Net Parameter Validation")
    print("=" * 60)
    
    total_params = 0
    
    # Block 1: Initial feature extraction (3→24→24)
    print("\n📊 Block 1: Initial Feature Extraction")
    block1_params = 0
    
    # Conv1: 3→24, 3x3, stride=2
    conv1_1_params = calculate_conv2d_params(3, 24, 3, bias=False)
    bn1_1_params = calculate_batchnorm2d_params(24)
    block1_params += conv1_1_params + bn1_1_params
    print(f"  Conv2d(3→24, 3×3): {conv1_1_params:,} params")
    print(f"  BatchNorm2d(24): {bn1_1_params:,} params")
    
    # Conv2: 24→24, 3x3, stride=1
    conv1_2_params = calculate_conv2d_params(24, 24, 3, bias=False)
    bn1_2_params = calculate_batchnorm2d_params(24)
    block1_params += conv1_2_params + bn1_2_params
    print(f"  Conv2d(24→24, 3×3): {conv1_2_params:,} params")
    print(f"  BatchNorm2d(24): {bn1_2_params:,} params")
    
    # SE Module
    se1_params = calculate_se_module_params(24, reduction=8)
    block1_params += se1_params
    print(f"  SE Module(24): {se1_params:,} params")
    
    print(f"  Block 1 Total: {block1_params:,} params")
    total_params += block1_params
    
    # Block 2: Enhanced Depthwise Separable (24→48)
    print("\n📊 Block 2: Enhanced Depthwise Separable")
    block2_params = 0
    
    # Enhanced Depthwise Separable Conv
    dw_sep_params = calculate_enhanced_depthwise_separable_params(24, 48)
    block2_params += dw_sep_params
    print(f"  Enhanced DepthwiseSeparable(24→48): {dw_sep_params:,} params")
    
    # SE Module
    se2_params = calculate_se_module_params(48, reduction=8)
    block2_params += se2_params
    print(f"  SE Module(48): {se2_params:,} params")
    
    print(f"  Block 2 Total: {block2_params:,} params")
    total_params += block2_params
    
    # Block 3: Multi-scale Dilated (48→72 with residual)
    print("\n📊 Block 3: Multi-scale Dilated + Residual")
    block3_params = 0
    
    # Projection conv (48→72)
    proj3_conv_params = calculate_conv2d_params(48, 72, 1, bias=False)
    proj3_bn_params = calculate_batchnorm2d_params(72)
    block3_params += proj3_conv_params + proj3_bn_params
    print(f"  Projection Conv(48→72, 1×1): {proj3_conv_params:,} params")
    print(f"  Projection BN(72): {proj3_bn_params:,} params")
    
    # Multi-scale dilated block
    ms_dilated1_params = calculate_multiscale_dilated_block_params(72)
    block3_params += ms_dilated1_params
    print(f"  Multi-scale Dilated Block(72): {ms_dilated1_params:,} params")
    
    # SE Module
    se3_params = calculate_se_module_params(72, reduction=8)
    block3_params += se3_params
    print(f"  SE Module(72): {se3_params:,} params")
    
    print(f"  Block 3 Total: {block3_params:,} params")
    total_params += block3_params
    
    # Block 4: Feature expansion (72→96)
    print("\n📊 Block 4: Feature Expansion")
    block4_params = 0
    
    # Conv1: 72→96, 3x3, stride=2
    conv4_1_params = calculate_conv2d_params(72, 96, 3, bias=False)
    bn4_1_params = calculate_batchnorm2d_params(96)
    block4_params += conv4_1_params + bn4_1_params
    print(f"  Conv2d(72→96, 3×3): {conv4_1_params:,} params")
    print(f"  BatchNorm2d(96): {bn4_1_params:,} params")
    
    # Conv2: 96→96, 1x1
    conv4_2_params = calculate_conv2d_params(96, 96, 1, bias=False)
    bn4_2_params = calculate_batchnorm2d_params(96)
    block4_params += conv4_2_params + bn4_2_params
    print(f"  Conv2d(96→96, 1×1): {conv4_2_params:,} params")
    print(f"  BatchNorm2d(96): {bn4_2_params:,} params")
    
    # SE Module
    se4_params = calculate_se_module_params(96, reduction=8)
    block4_params += se4_params
    print(f"  SE Module(96): {se4_params:,} params")
    
    print(f"  Block 4 Total: {block4_params:,} params")
    total_params += block4_params
    
    # Block 5: High multi-scale dilation (96→128 with residual)
    print("\n📊 Block 5: High Multi-scale Dilation + Residual")
    block5_params = 0
    
    # Projection conv (96→128)
    proj5_conv_params = calculate_conv2d_params(96, 128, 1, bias=False)
    proj5_bn_params = calculate_batchnorm2d_params(128)
    block5_params += proj5_conv_params + proj5_bn_params
    print(f"  Projection Conv(96→128, 1×1): {proj5_conv_params:,} params")
    print(f"  Projection BN(128): {proj5_bn_params:,} params")
    
    # Multi-scale dilated block
    ms_dilated2_params = calculate_multiscale_dilated_block_params(128)
    block5_params += ms_dilated2_params
    print(f"  Multi-scale Dilated Block(128): {ms_dilated2_params:,} params")
    
    # SE Module
    se5_params = calculate_se_module_params(128, reduction=8)
    block5_params += se5_params
    print(f"  SE Module(128): {se5_params:,} params")
    
    print(f"  Block 5 Total: {block5_params:,} params")
    total_params += block5_params
    
    # Output Block: GAP + Linear
    print("\n📊 Output Block: Classification")
    output_params = 0
    
    # Linear layer (128→10)
    linear_params = calculate_linear_params(128, 10, bias=True)
    output_params += linear_params
    print(f"  Linear(128→10): {linear_params:,} params")
    
    print(f"  Output Block Total: {output_params:,} params")
    total_params += output_params
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ENHANCED MODEL PARAMETER SUMMARY")
    print("=" * 60)
    
    print(f"Block 1 (Initial + SE):           {block1_params:>8,} params ({(block1_params/total_params)*100:>5.1f}%)")
    print(f"Block 2 (Enhanced DW-Sep + SE):   {block2_params:>8,} params ({(block2_params/total_params)*100:>5.1f}%)")
    print(f"Block 3 (Multi-scale + Res + SE): {block3_params:>8,} params ({(block3_params/total_params)*100:>5.1f}%)")
    print(f"Block 4 (Feature Exp + SE):       {block4_params:>8,} params ({(block4_params/total_params)*100:>5.1f}%)")
    print(f"Block 5 (Multi-scale + Res + SE): {block5_params:>8,} params ({(block5_params/total_params)*100:>5.1f}%)")
    print(f"Output (GAP + Linear):             {output_params:>8,} params ({(output_params/total_params)*100:>5.1f}%)")
    print("-" * 60)
    print(f"TOTAL PARAMETERS:                  {total_params:>8,} params")
    
    # Validation
    budget_used = (total_params / 200000) * 100
    within_budget = total_params < 200000
    
    print(f"\n🎯 PARAMETER BUDGET ANALYSIS:")
    print(f"Budget Used: {budget_used:.1f}% of 200,000")
    print(f"Remaining: {200000 - total_params:,} parameters")
    print(f"Status: {'✅ WITHIN BUDGET' if within_budget else '❌ EXCEEDS BUDGET'}")
    
    # Comparison with original
    original_params = 198666  # Original CIFAR_GAP_Net
    improvement_cost = total_params - original_params
    print(f"\n📈 COMPARISON WITH ORIGINAL:")
    print(f"Original CIFAR_GAP_Net: {original_params:,} parameters")
    print(f"Enhanced CIFAR_GAP_Net: {total_params:,} parameters")
    print(f"Additional Parameters: {improvement_cost:+,} parameters")
    print(f"Relative Increase: {(improvement_cost/original_params)*100:+.1f}%")
    
    # Expected improvements
    print(f"\n🚀 EXPECTED IMPROVEMENTS:")
    print(f"Current Accuracy: 83.46%")
    print(f"Target Accuracy: 87-88%")
    print(f"Expected Gain: +3.5-4.5%")
    print(f"Improvement Sources:")
    print(f"  • Residual connections: +1.5-2.0%")
    print(f"  • SE modules: +1.0-1.5%")
    print(f"  • Multi-scale dilated: +0.8-1.2%")
    print(f"  • Enhanced DW-Sep: +0.4-0.7%")
    print(f"  • Better channels: +0.3-0.5%")
    
    return {
        'total_parameters': total_params,
        'within_budget': within_budget,
        'budget_used_percent': budget_used,
        'improvement_cost': improvement_cost,
        'blocks': {
            'block1': block1_params,
            'block2': block2_params,
            'block3': block3_params,
            'block4': block4_params,
            'block5': block5_params,
            'output': output_params
        }
    }

if __name__ == "__main__":
    result = validate_enhanced_cifar_gap_net()
    
    print(f"\n🎉 VALIDATION COMPLETE!")
    if result['within_budget']:
        print(f"✅ Enhanced model is ready for training!")
        print(f"🎯 Expected to achieve 87-88% accuracy with architectural improvements!")
    else:
        print(f"❌ Model exceeds parameter budget - needs optimization")
        print(f"💡 Consider reducing channel sizes or SE reduction ratios")
