#!/usr/bin/env python3
"""
PyTorch-independent parameter estimation for all models.
Estimates parameters by analyzing the architecture definitions.
"""

import re
import os

def estimate_conv2d_params(in_channels, out_channels, kernel_size, bias=False):
    """Estimate Conv2d parameters."""
    if isinstance(kernel_size, int):
        k_h = k_w = kernel_size
    else:
        k_h, k_w = kernel_size
    
    weight_params = in_channels * out_channels * k_h * k_w
    bias_params = out_channels if bias else 0
    return weight_params + bias_params

def estimate_batchnorm2d_params(num_features):
    """Estimate BatchNorm2d parameters."""
    return 2 * num_features  # weight + bias

def estimate_model_params(model_file):
    """Estimate parameters for a model by parsing its definition."""
    try:
        with open(model_file, 'r') as f:
            content = f.read()
        
        total_params = 0
        
        # Find Conv2d layers
        conv_pattern = r'nn\.Conv2d\((\d+),\s*(\d+),\s*kernel_size=(\d+)(?:.*?bias=(\w+))?'
        for match in re.finditer(conv_pattern, content):
            in_ch = int(match.group(1))
            out_ch = int(match.group(2))
            kernel = int(match.group(3))
            bias = match.group(4) != 'False' if match.group(4) else True
            
            params = estimate_conv2d_params(in_ch, out_ch, kernel, bias)
            total_params += params
            
        # Find BatchNorm2d layers
        bn_pattern = r'nn\.BatchNorm2d\((\d+)\)'
        for match in re.finditer(bn_pattern, content):
            num_features = int(match.group(1))
            params = estimate_batchnorm2d_params(num_features)
            total_params += params
            
        return total_params
        
    except Exception as e:
        return f"Error: {e}"

def check_all_models():
    """Check parameter estimates for all models."""
    print("🔍 PARAMETER ESTIMATION (PyTorch-Independent)")
    print("="*60)
    
    models = [
        ('model1.py', 'Model_1'),
        ('model2.py', 'Model_2'), 
        ('model3.py', 'Model_3'),
        ('model4.py', 'Model_4'),
        ('model5.py', 'Model_5'),
        ('model6.py', 'Model_6'),
        ('model7.py', 'Model_7')
    ]
    
    compliant_models = 0
    
    for model_file, model_name in models:
        if os.path.exists(model_file):
            estimated_params = estimate_model_params(model_file)
            
            if isinstance(estimated_params, int):
                status = "✅ COMPLIANT" if estimated_params < 8000 else "❌ OVER LIMIT"
                gap = estimated_params - 8000
                gap_str = f"({gap:+,} vs limit)" if gap != 0 else "(within limit)"
                
                print(f"{model_name:>8}: {estimated_params:>6,} params {status} {gap_str}")
                
                if estimated_params < 8000:
                    compliant_models += 1
            else:
                print(f"{model_name:>8}: {estimated_params}")
        else:
            print(f"{model_name:>8}: File not found")
    
    print(f"\n📊 SUMMARY: {compliant_models}/{len(models)} models compliant")
    
    if compliant_models == len(models):
        print("🎉 ALL MODELS UNDER 8,000 PARAMETER LIMIT!")
    else:
        print("⚠️  Some models need parameter reduction")
        
    return compliant_models == len(models)

if __name__ == "__main__":
    check_all_models()
