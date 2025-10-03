"""
CIFAR-10 Advanced Model Validation Script
=========================================

Validates the model architecture against assignment requirements:
- Parameter count < 200K
- Receptive field > 44
- Architecture components (C1, C2, C3, C4, O)
- No max pooling (strided convolutions only)
- Dilated kernels present
- Depthwise separable convolutions
- Global Average Pooling
"""

import torch
import torch.nn as nn
import numpy as np
from cifar10_advanced_model import AdvancedCIFAR10Model, create_advanced_cifar10_model

def validate_no_maxpool(model):
    """Check that model doesn't use MaxPool layers"""
    has_maxpool = False
    maxpool_layers = []
    
    for name, module in model.named_modules():
        if isinstance(module, (nn.MaxPool2d, nn.MaxPool1d, nn.MaxPool3d)):
            has_maxpool = True
            maxpool_layers.append(name)
    
    return not has_maxpool, maxpool_layers

def validate_strided_convs(model):
    """Check for strided convolutions"""
    strided_convs = []
    
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            if hasattr(module, 'stride') and module.stride != (1, 1):
                strided_convs.append({
                    'name': name,
                    'stride': module.stride,
                    'in_channels': module.in_channels,
                    'out_channels': module.out_channels
                })
    
    return len(strided_convs) > 0, strided_convs

def validate_dilated_convs(model):
    """Check for dilated convolutions"""
    dilated_convs = []
    
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            if hasattr(module, 'dilation') and module.dilation != (1, 1):
                dilated_convs.append({
                    'name': name,
                    'dilation': module.dilation,
                    'in_channels': module.in_channels,
                    'out_channels': module.out_channels
                })
    
    return len(dilated_convs) > 0, dilated_convs

def validate_depthwise_separable(model):
    """Check for depthwise separable convolutions"""
    depthwise_convs = []
    
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            if hasattr(module, 'groups') and module.groups == module.in_channels and module.groups > 1:
                depthwise_convs.append({
                    'name': name,
                    'groups': module.groups,
                    'in_channels': module.in_channels,
                    'out_channels': module.out_channels
                })
    
    return len(depthwise_convs) > 0, depthwise_convs

def validate_global_avg_pool(model):
    """Check for Global Average Pooling"""
    has_gap = False
    gap_layers = []
    
    for name, module in model.named_modules():
        if isinstance(module, (nn.AdaptiveAvgPool2d, nn.AdaptiveAvgPool1d)):
            has_gap = True
            gap_layers.append(name)
    
    return has_gap, gap_layers

def validate_no_fc_after_conv(model):
    """Check that there are no FC layers directly after convolutional layers"""
    modules_list = list(model.named_modules())
    has_fc_after_conv = False
    violations = []
    
    for i, (name, module) in enumerate(modules_list[:-1]):
        if isinstance(module, nn.Conv2d):
            # Check next few modules
            for j in range(i+1, min(i+4, len(modules_list))):
                next_name, next_module = modules_list[j]
                if isinstance(next_module, nn.Linear):
                    # Check if there's GAP or flatten in between
                    gap_found = False
                    for k in range(i+1, j):
                        _, intermediate = modules_list[k]
                        if isinstance(intermediate, (nn.AdaptiveAvgPool2d, nn.Flatten)):
                            gap_found = True
                            break
                    
                    if not gap_found:
                        has_fc_after_conv = True
                        violations.append(f"{name} -> {next_name}")
    
    return not has_fc_after_conv, violations

def test_model_forward_pass(model, batch_size=4):
    """Test model forward pass with different input sizes"""
    model.eval()
    
    test_cases = [
        (batch_size, 3, 32, 32),  # Standard CIFAR-10
        (1, 3, 32, 32),           # Single image
        (8, 3, 32, 32),           # Larger batch
    ]
    
    results = []
    
    for input_shape in test_cases:
        try:
            dummy_input = torch.randn(input_shape)
            
            with torch.no_grad():
                output = model(dummy_input)
            
            results.append({
                'input_shape': input_shape,
                'output_shape': output.shape,
                'success': True,
                'output_range': (output.min().item(), output.max().item())
            })
            
        except Exception as e:
            results.append({
                'input_shape': input_shape,
                'output_shape': None,
                'success': False,
                'error': str(e)
            })
    
    return results

def analyze_model_architecture(model):
    """Detailed analysis of model architecture"""
    analysis = {
        'total_layers': 0,
        'conv_layers': 0,
        'bn_layers': 0,
        'activation_layers': 0,
        'dropout_layers': 0,
        'pooling_layers': 0,
        'linear_layers': 0
    }
    
    layer_details = []
    
    for name, module in model.named_modules():
        if len(list(module.children())) == 0:  # Leaf modules only
            analysis['total_layers'] += 1
            
            layer_info = {'name': name, 'type': type(module).__name__}
            
            if isinstance(module, nn.Conv2d):
                analysis['conv_layers'] += 1
                layer_info.update({
                    'in_channels': module.in_channels,
                    'out_channels': module.out_channels,
                    'kernel_size': module.kernel_size,
                    'stride': module.stride,
                    'padding': module.padding,
                    'dilation': module.dilation,
                    'groups': module.groups
                })
            elif isinstance(module, nn.BatchNorm2d):
                analysis['bn_layers'] += 1
                layer_info['num_features'] = module.num_features
            elif isinstance(module, (nn.ReLU, nn.ReLU6, nn.LeakyReLU, nn.GELU)):
                analysis['activation_layers'] += 1
            elif isinstance(module, (nn.Dropout, nn.Dropout2d)):
                analysis['dropout_layers'] += 1
                layer_info['p'] = module.p
            elif isinstance(module, (nn.MaxPool2d, nn.AvgPool2d, nn.AdaptiveAvgPool2d)):
                analysis['pooling_layers'] += 1
            elif isinstance(module, nn.Linear):
                analysis['linear_layers'] += 1
                layer_info.update({
                    'in_features': module.in_features,
                    'out_features': module.out_features
                })
            
            layer_details.append(layer_info)
    
    return analysis, layer_details

def calculate_detailed_receptive_field(model):
    """Calculate receptive field through the network"""
    
    # This is a simplified calculation
    # For exact RF, we'd need to trace through the actual architecture
    
    rf_progression = []
    current_rf = 1
    current_stride = 1
    
    # Simplified RF calculation based on typical architecture
    blocks = [
        {'name': 'C1', 'convs': 3, 'kernel_size': 3, 'stride': 1, 'dilation': [1, 1, 2]},
        {'name': 'C2', 'convs': 3, 'kernel_size': 3, 'stride': 2, 'dilation': [1, 1, 2]},
        {'name': 'C3', 'convs': 3, 'kernel_size': 3, 'stride': 2, 'dilation': [1, 1, 3]},
        {'name': 'C4', 'convs': 3, 'kernel_size': 3, 'stride': 2, 'dilation': [1, 1, 4]},
    ]
    
    for block in blocks:
        block_start_rf = current_rf
        
        for i in range(block['convs']):
            kernel_size = block['kernel_size']
            dilation = block['dilation'][i] if i < len(block['dilation']) else 1
            
            # For first conv in block, apply stride
            if i == 0 and block['stride'] > 1:
                current_rf = current_rf * block['stride']
                current_stride = current_stride * block['stride']
            
            # Add kernel contribution
            effective_kernel = (kernel_size - 1) * dilation + 1
            current_rf += (effective_kernel - 1) * current_stride
        
        rf_progression.append({
            'block': block['name'],
            'rf_start': block_start_rf,
            'rf_end': current_rf,
            'stride_cumulative': current_stride
        })
    
    return current_rf, rf_progression

def main():
    """Main validation function"""
    print("🔍 CIFAR-10 Advanced Model Validation")
    print("=" * 60)
    
    # Create model
    print("🏗️  Creating model...")
    model, model_info = create_advanced_cifar10_model()
    
    print(f"\n📊 Basic Model Information:")
    print(f"  Total parameters: {model_info['total_parameters']:,}")
    print(f"  Receptive field: {model_info['receptive_field']}")
    print(f"  Parameter budget used: {model_info['parameter_budget_used']:.1f}%")
    
    # Requirement checks
    print(f"\n✅ Assignment Requirements Check:")
    
    # 1. Parameter count
    param_ok = model_info['parameter_requirement_met']
    print(f"  Parameters < 200K: {'✅ PASS' if param_ok else '❌ FAIL'} "
          f"({model_info['total_parameters']:,})")
    
    # 2. Receptive field
    rf_ok = model_info['rf_requirement_met']
    print(f"  Receptive field > 44: {'✅ PASS' if rf_ok else '❌ FAIL'} "
          f"({model_info['receptive_field']})")
    
    # 3. No max pooling
    no_maxpool, maxpool_layers = validate_no_maxpool(model)
    print(f"  No max pooling: {'✅ PASS' if no_maxpool else '❌ FAIL'}")
    if maxpool_layers:
        print(f"    Found MaxPool layers: {maxpool_layers}")
    
    # 4. Strided convolutions
    has_strided, strided_convs = validate_strided_convs(model)
    print(f"  Strided convolutions: {'✅ PASS' if has_strided else '❌ FAIL'}")
    if has_strided:
        print(f"    Found {len(strided_convs)} strided convolutions")
    
    # 5. Dilated convolutions
    has_dilated, dilated_convs = validate_dilated_convs(model)
    print(f"  Dilated convolutions: {'✅ PASS' if has_dilated else '❌ FAIL'}")
    if has_dilated:
        print(f"    Found {len(dilated_convs)} dilated convolutions")
    
    # 6. Depthwise separable
    has_depthwise, depthwise_convs = validate_depthwise_separable(model)
    print(f"  Depthwise separable: {'✅ PASS' if has_depthwise else '❌ FAIL'}")
    if has_depthwise:
        print(f"    Found {len(depthwise_convs)} depthwise convolutions")
    
    # 7. Global Average Pooling
    has_gap, gap_layers = validate_global_avg_pool(model)
    print(f"  Global Average Pooling: {'✅ PASS' if has_gap else '❌ FAIL'}")
    if has_gap:
        print(f"    Found GAP layers: {gap_layers}")
    
    # 8. No FC after conv
    no_fc_after_conv, violations = validate_no_fc_after_conv(model)
    print(f"  No FC after conv: {'✅ PASS' if no_fc_after_conv else '❌ FAIL'}")
    if violations:
        print(f"    Violations: {violations}")
    
    # Forward pass test
    print(f"\n🧪 Forward Pass Testing:")
    forward_results = test_model_forward_pass(model)
    
    for result in forward_results:
        if result['success']:
            print(f"  Input {result['input_shape']}: ✅ PASS")
            print(f"    Output shape: {result['output_shape']}")
            print(f"    Output range: [{result['output_range'][0]:.3f}, {result['output_range'][1]:.3f}]")
        else:
            print(f"  Input {result['input_shape']}: ❌ FAIL")
            print(f"    Error: {result['error']}")
    
    # Detailed architecture analysis
    print(f"\n🔍 Architecture Analysis:")
    analysis, layer_details = analyze_model_architecture(model)
    
    print(f"  Total layers: {analysis['total_layers']}")
    print(f"  Conv layers: {analysis['conv_layers']}")
    print(f"  BatchNorm layers: {analysis['bn_layers']}")
    print(f"  Activation layers: {analysis['activation_layers']}")
    print(f"  Dropout layers: {analysis['dropout_layers']}")
    print(f"  Pooling layers: {analysis['pooling_layers']}")
    print(f"  Linear layers: {analysis['linear_layers']}")
    
    # Detailed RF calculation
    print(f"\n📏 Detailed Receptive Field Analysis:")
    detailed_rf, rf_progression = calculate_detailed_receptive_field(model)
    
    for block_info in rf_progression:
        print(f"  {block_info['block']}: RF {block_info['rf_start']} → {block_info['rf_end']}")
    
    print(f"  Final RF: {detailed_rf}")
    
    # Overall validation result
    all_requirements = [
        param_ok, rf_ok, no_maxpool, has_strided, 
        has_dilated, has_depthwise, has_gap, no_fc_after_conv
    ]
    
    all_passed = all(all_requirements)
    
    print(f"\n🎯 Overall Validation Result:")
    print(f"  {'✅ ALL REQUIREMENTS PASSED!' if all_passed else '❌ SOME REQUIREMENTS FAILED'}")
    
    if all_passed:
        print(f"  🚀 Model is ready for CIFAR-10 training!")
        print(f"  🎯 Target: 85% accuracy with {model_info['total_parameters']:,} parameters")
    else:
        print(f"  ⚠️  Please fix the failing requirements before training")
    
    # Architecture summary
    print(f"\n📋 Architecture Summary:")
    print(f"  C1: 3×32×32 → 32×32×32 (initial features)")
    print(f"  C2: 32×32×32 → 64×16×16 (strided reduction)")
    print(f"  C3: 64×16×16 → 128×8×8 (strided reduction)")
    print(f"  C4: 128×8×8 → 256×4×4 (strided reduction)")
    print(f"  O:  256×4×4 → 10 (GAP + classification)")
    
    return all_passed

if __name__ == "__main__":
    validation_passed = main()
    
    if validation_passed:
        print(f"\n🎉 Validation completed successfully!")
        print(f"✅ Ready to start training with: python train_cifar10_advanced.py")
    else:
        print(f"\n⚠️  Validation failed. Please check the requirements.")
        exit(1)
