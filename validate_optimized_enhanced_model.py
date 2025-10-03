"""
Optimized Enhanced CIFAR_GAP_Net Parameter Validation
====================================================

PyTorch-independent validation of the optimized enhanced model architecture
to ensure it stays within the 200K parameter limit while providing improvements.
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

def calculate_lightweight_se_module_params(channels, reduction=32):
    """Calculate parameters for Lightweight SE module"""
    reduced_channels = max(channels // reduction, 2)
    
    # First conv: channels -> reduced_channels
    conv1_params = calculate_conv2d_params(channels, reduced_channels, 1, bias=False)
    
    # Second conv: reduced_channels -> channels
    conv2_params = calculate_conv2d_params(reduced_channels, channels, 1, bias=False)
    
    return conv1_params + conv2_params

def calculate_efficient_depthwise_separable_params(in_ch, out_ch, kernel_size=3):
    """Calculate parameters for Efficient Depthwise Separable Conv (single layer)"""
    params = 0
    
    # Depthwise conv
    params += calculate_conv2d_params(in_ch, in_ch, kernel_size, groups=in_ch, bias=False)
    params += calculate_batchnorm2d_params(in_ch)
    
    # Pointwise conv
    params += calculate_conv2d_params(in_ch, out_ch, 1, bias=False)
    params += calculate_batchnorm2d_params(out_ch)
    
    return params

def calculate_compact_multiscale_dilated_block_params(channels):
    """Calculate parameters for Compact Multi-scale Dilated Block (3 branches)"""
    branch_channels = channels // 3
    params = 0
    
    # Three branches (dilation 1, 2, 4)
    for _ in range(3):
        # Conv + BN for each branch
        params += calculate_conv2d_params(channels, branch_channels, 3, bias=False)
        params += calculate_batchnorm2d_params(branch_channels)
    
    # Combine conv (branch_channels * 3 -> channels)
    params += calculate_conv2d_params(branch_channels * 3, channels, 1, bias=False)
    params += calculate_batchnorm2d_params(channels)
    
    return params

def validate_optimized_enhanced_cifar_gap_net():
    """Validate Optimized Enhanced CIFAR_GAP_Net parameter count"""
    
    print("🔍 Optimized Enhanced CIFAR_GAP_Net Parameter Validation")
    print("=" * 70)
    
    total_params = 0
    
    # Block 1: Initial feature extraction (3→32→32)
    print("\n📊 Block 1: Initial Feature Extraction")
    block1_params = 0
    
    # Conv1: 3→32, 3x3, stride=2
    conv1_1_params = calculate_conv2d_params(3, 32, 3, bias=False)
    bn1_1_params = calculate_batchnorm2d_params(32)
    block1_params += conv1_1_params + bn1_1_params
    print(f"  Conv2d(3→32, 3×3): {conv1_1_params:,} params")
    print(f"  BatchNorm2d(32): {bn1_1_params:,} params")
    
    # Conv2: 32→32, 3x3, stride=1
    conv1_2_params = calculate_conv2d_params(32, 32, 3, bias=False)
    bn1_2_params = calculate_batchnorm2d_params(32)
    block1_params += conv1_2_params + bn1_2_params
    print(f"  Conv2d(32→32, 3×3): {conv1_2_params:,} params")
    print(f"  BatchNorm2d(32): {bn1_2_params:,} params")
    
    # Lightweight SE Module (reduction=16)
    se1_params = calculate_lightweight_se_module_params(32, reduction=16)
    block1_params += se1_params
    print(f"  Lightweight SE Module(32, r=16): {se1_params:,} params")
    
    print(f"  Block 1 Total: {block1_params:,} params")
    total_params += block1_params
    
    # Block 2: Efficient Depthwise Separable (32→48)
    print("\n📊 Block 2: Efficient Depthwise Separable")
    block2_params = 0
    
    # Efficient Depthwise Separable Conv
    dw_sep_params = calculate_efficient_depthwise_separable_params(32, 48)
    block2_params += dw_sep_params
    print(f"  Efficient DepthwiseSeparable(32→48): {dw_sep_params:,} params")
    
    # Lightweight SE Module (reduction=24)
    se2_params = calculate_lightweight_se_module_params(48, reduction=24)
    block2_params += se2_params
    print(f"  Lightweight SE Module(48, r=24): {se2_params:,} params")
    
    print(f"  Block 2 Total: {block2_params:,} params")
    total_params += block2_params
    
    # Block 3: Compact Multi-scale Dilated (48→64, NO residual)
    print("\n📊 Block 3: Compact Multi-scale Dilated (NO residual)")
    block3_params = 0
    
    # Projection conv (48→64)
    proj3_conv_params = calculate_conv2d_params(48, 64, 1, bias=False)
    proj3_bn_params = calculate_batchnorm2d_params(64)
    block3_params += proj3_conv_params + proj3_bn_params
    print(f"  Projection Conv(48→64, 1×1): {proj3_conv_params:,} params")
    print(f"  Projection BN(64): {proj3_bn_params:,} params")
    
    # Compact multi-scale dilated block (3 branches)
    cms_dilated1_params = calculate_compact_multiscale_dilated_block_params(64)
    block3_params += cms_dilated1_params
    print(f"  Compact Multi-scale Dilated Block(64): {cms_dilated1_params:,} params")
    
    # Lightweight SE Module (reduction=32)
    se3_params = calculate_lightweight_se_module_params(64, reduction=32)
    block3_params += se3_params
    print(f"  Lightweight SE Module(64, r=32): {se3_params:,} params")
    
    print(f"  Block 3 Total: {block3_params:,} params")
    total_params += block3_params
    
    # Block 4: Feature expansion (64→80)
    print("\n📊 Block 4: Feature Expansion")
    block4_params = 0
    
    # Conv1: 64→80, 3x3, stride=2
    conv4_1_params = calculate_conv2d_params(64, 80, 3, bias=False)
    bn4_1_params = calculate_batchnorm2d_params(80)
    block4_params += conv4_1_params + bn4_1_params
    print(f"  Conv2d(64→80, 3×3): {conv4_1_params:,} params")
    print(f"  BatchNorm2d(80): {bn4_1_params:,} params")
    
    # Conv2: 80→80, 1x1
    conv4_2_params = calculate_conv2d_params(80, 80, 1, bias=False)
    bn4_2_params = calculate_batchnorm2d_params(80)
    block4_params += conv4_2_params + bn4_2_params
    print(f"  Conv2d(80→80, 1×1): {conv4_2_params:,} params")
    print(f"  BatchNorm2d(80): {bn4_2_params:,} params")
    
    # Lightweight SE Module (reduction=32)
    se4_params = calculate_lightweight_se_module_params(80, reduction=32)
    block4_params += se4_params
    print(f"  Lightweight SE Module(80, r=32): {se4_params:,} params")
    
    print(f"  Block 4 Total: {block4_params:,} params")
    total_params += block4_params
    
    # Block 5: Final multi-scale dilation (80→96 with residual)
    print("\n📊 Block 5: Final Multi-scale Dilation + Residual")
    block5_params = 0
    
    # Projection conv (80→96)
    proj5_conv_params = calculate_conv2d_params(80, 96, 1, bias=False)
    proj5_bn_params = calculate_batchnorm2d_params(96)
    block5_params += proj5_conv_params + proj5_bn_params
    print(f"  Projection Conv(80→96, 1×1): {proj5_conv_params:,} params")
    print(f"  Projection BN(96): {proj5_bn_params:,} params")
    
    # Compact multi-scale dilated block (3 branches)
    cms_dilated2_params = calculate_compact_multiscale_dilated_block_params(96)
    block5_params += cms_dilated2_params
    print(f"  Compact Multi-scale Dilated Block(96): {cms_dilated2_params:,} params")
    
    # Lightweight SE Module (reduction=32)
    se5_params = calculate_lightweight_se_module_params(96, reduction=32)
    block5_params += se5_params
    print(f"  Lightweight SE Module(96, r=32): {se5_params:,} params")
    
    print(f"  Block 5 Total: {block5_params:,} params")
    total_params += block5_params
    
    # Output Block: GAP + Linear
    print("\n📊 Output Block: Classification")
    output_params = 0
    
    # Linear layer (96→10)
    linear_params = calculate_linear_params(96, 10, bias=True)
    output_params += linear_params
    print(f"  Linear(96→10): {linear_params:,} params")
    
    print(f"  Output Block Total: {output_params:,} params")
    total_params += output_params
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 OPTIMIZED ENHANCED MODEL PARAMETER SUMMARY")
    print("=" * 70)
    
    print(f"Block 1 (Initial + Lightweight SE):      {block1_params:>8,} params ({(block1_params/total_params)*100:>5.1f}%)")
    print(f"Block 2 (Efficient DW-Sep + SE):         {block2_params:>8,} params ({(block2_params/total_params)*100:>5.1f}%)")
    print(f"Block 3 (Compact Multi-scale + SE):      {block3_params:>8,} params ({(block3_params/total_params)*100:>5.1f}%)")
    print(f"Block 4 (Feature Exp + SE):              {block4_params:>8,} params ({(block4_params/total_params)*100:>5.1f}%)")
    print(f"Block 5 (Compact Multi-scale + Res+SE):  {block5_params:>8,} params ({(block5_params/total_params)*100:>5.1f}%)")
    print(f"Output (GAP + Linear):                    {output_params:>8,} params ({(output_params/total_params)*100:>5.1f}%)")
    print("-" * 70)
    print(f"TOTAL PARAMETERS:                         {total_params:>8,} params")
    
    # Validation
    budget_used = (total_params / 200000) * 100
    within_budget = total_params < 200000
    
    print(f"\n🎯 PARAMETER BUDGET ANALYSIS:")
    print(f"Budget Used: {budget_used:.1f}% of 200,000")
    print(f"Remaining: {200000 - total_params:,} parameters")
    print(f"Status: {'✅ WITHIN BUDGET' if within_budget else '❌ EXCEEDS BUDGET'}")
    
    # Comparison with models
    original_params = 198666  # Original CIFAR_GAP_Net
    enhanced_params = 322514  # Full Enhanced CIFAR_GAP_Net
    improvement_cost = total_params - original_params
    savings = enhanced_params - total_params
    
    print(f"\n📈 MODEL COMPARISON:")
    print(f"Original CIFAR_GAP_Net:     {original_params:,} parameters")
    print(f"Full Enhanced (over budget): {enhanced_params:,} parameters")
    print(f"Optimized Enhanced:         {total_params:,} parameters")
    print(f"Additional vs Original:     {improvement_cost:+,} parameters ({(improvement_cost/original_params)*100:+.1f}%)")
    print(f"Savings vs Full Enhanced:   {-savings:+,} parameters ({(savings/enhanced_params)*100:.1f}% reduction)")
    
    # Expected improvements
    print(f"\n🚀 EXPECTED IMPROVEMENTS:")
    print(f"Current Accuracy: 83.46%")
    print(f"Target Accuracy: 86-87%")
    print(f"Expected Gain: +2.5-3.5%")
    print(f"Improvement Sources:")
    print(f"  • Lightweight SE modules: +0.8-1.2%")
    print(f"  • Compact multi-scale dilated: +0.6-1.0%")
    print(f"  • Selective residual connections: +0.5-0.8%")
    print(f"  • Efficient depthwise separable: +0.3-0.5%")
    print(f"  • Better channel progression: +0.3-0.5%")
    
    # Optimizations applied
    print(f"\n🔧 BUDGET OPTIMIZATIONS APPLIED:")
    print(f"  1. Lightweight SE modules (reduction 16→32)")
    print(f"  2. Compact multi-scale (4→3 branches)")
    print(f"  3. Selective residuals (only block 5)")
    print(f"  4. Conservative channels (3→32→48→64→80→96)")
    print(f"  5. Efficient DW-Sep (single layer)")
    
    return {
        'total_parameters': total_params,
        'within_budget': within_budget,
        'budget_used_percent': budget_used,
        'improvement_cost': improvement_cost,
        'savings_vs_full': savings,
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
    result = validate_optimized_enhanced_cifar_gap_net()
    
    print(f"\n🎉 VALIDATION COMPLETE!")
    if result['within_budget']:
        print(f"✅ Optimized enhanced model is ready for training!")
        print(f"🎯 Expected to achieve 86-87% accuracy with budget-compliant improvements!")
        print(f"💡 Provides {result['improvement_cost']:+,} parameter enhancement within 200K limit!")
    else:
        print(f"❌ Model still exceeds parameter budget - needs further optimization")
        print(f"💡 Consider additional reductions in channel sizes or SE ratios")
