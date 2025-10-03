"""
Test Script for Ultra-Efficient Models
======================================

This script tests the ultra-efficient models to ensure they:
1. Have correct parameter counts (<8000)
2. Accept MNIST input (1x28x28)
3. Produce correct output (10 classes)
4. Have proper forward pass functionality
"""

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from ultra_efficient_models import Model_1, Model_2, Model_3, create_model
    TORCH_AVAILABLE = True
except ImportError:
    print("⚠️  PyTorch not available. Running parameter validation only.")
    TORCH_AVAILABLE = False

def test_model_architecture(model_class, model_name, expected_max_params=8000):
    """Test a single model architecture"""
    print(f"\n🧪 Testing {model_name}")
    print("-" * 50)
    
    if not TORCH_AVAILABLE:
        print("❌ PyTorch not available - skipping functional tests")
        return False
    
    try:
        # Create model
        model = model_class()
        
        # Count parameters
        param_count = model.count_parameters()
        print(f"📊 Parameter count: {param_count:,}")
        
        # Check parameter limit
        if param_count >= expected_max_params:
            print(f"❌ FAIL: {param_count:,} >= {expected_max_params:,} parameters")
            return False
        else:
            margin = expected_max_params - param_count
            print(f"✅ PASS: {param_count:,} < {expected_max_params:,} (margin: +{margin:,})")
        
        # Test forward pass with MNIST-sized input
        print("🔄 Testing forward pass...")
        model.eval()
        
        # Single sample test
        dummy_input = torch.randn(1, 1, 28, 28)
        with torch.no_grad():
            output = model(dummy_input)
        
        print(f"📥 Input shape: {dummy_input.shape}")
        print(f"📤 Output shape: {output.shape}")
        
        # Verify output shape
        if output.shape != (1, 10):
            print(f"❌ FAIL: Expected output shape (1, 10), got {output.shape}")
            return False
        
        # Test batch processing
        print("🔄 Testing batch processing...")
        batch_input = torch.randn(32, 1, 28, 28)  # Batch of 32
        with torch.no_grad():
            batch_output = model(batch_input)
        
        print(f"📥 Batch input shape: {batch_input.shape}")
        print(f"📤 Batch output shape: {batch_output.shape}")
        
        if batch_output.shape != (32, 10):
            print(f"❌ FAIL: Expected batch output shape (32, 10), got {batch_output.shape}")
            return False
        
        # Test output range (should be logits, not probabilities)
        output_min = output.min().item()
        output_max = output.max().item()
        print(f"📊 Output range: [{output_min:.3f}, {output_max:.3f}]")
        
        # Apply softmax to check if it produces valid probabilities
        probs = F.softmax(output, dim=1)
        prob_sum = probs.sum().item()
        print(f"📊 Probability sum after softmax: {prob_sum:.6f}")
        
        if abs(prob_sum - 1.0) > 1e-5:
            print(f"❌ FAIL: Probabilities don't sum to 1.0: {prob_sum}")
            return False
        
        print(f"✅ {model_name} passed all tests!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR in {model_name}: {str(e)}")
        return False

def test_receptive_field_analysis():
    """Analyze receptive field coverage for each model"""
    print(f"\n🔍 Receptive Field Analysis")
    print("-" * 50)
    
    # Theoretical receptive field calculations
    rf_data = {
        "Model_1": {
            "layers": [
                ("Input", 28, 1),
                ("Conv1 (3x3)", 28, 3),
                ("Conv2 (3x3)", 28, 5),
                ("MaxPool (2x2)", 14, 10),
                ("Conv3 (3x3)", 14, 12),
                ("MaxPool (2x2)", 7, 16),
                ("GAP", 1, 16)
            ],
            "final_rf": 16,
            "coverage": "57%"
        },
        "Model_2": {
            "layers": [
                ("Input", 28, 1),
                ("Conv1 (3x3)", 28, 3),
                ("Conv2 (3x3)", 28, 5),
                ("MaxPool (2x2)", 14, 10),
                ("Conv3 (3x3)", 14, 12),
                ("Conv4 (3x3)", 14, 14),
                ("MaxPool (2x2)", 7, 28),
                ("Conv5 (3x3)", 7, 30),
                ("GAP", 1, 30)
            ],
            "final_rf": 30,
            "coverage": "107%"
        },
        "Model_3": {
            "layers": [
                ("Input", 28, 1),
                ("Conv1 (3x3)", 28, 3),
                ("Conv2 (3x3) + Residual", 28, 5),
                ("MaxPool (2x2)", 14, 10),
                ("Conv3 (3x3)", 14, 12),
                ("MaxPool (2x2)", 7, 24),
                ("Conv4 (3x3)", 7, 26),
                ("GAP", 1, 26)
            ],
            "final_rf": 26,
            "coverage": "93%"
        }
    }
    
    for model_name, data in rf_data.items():
        print(f"\n📐 {model_name} Receptive Field:")
        for layer_name, spatial_size, rf in data["layers"]:
            print(f"   {layer_name:<25} | Size: {spatial_size:2d}×{spatial_size:2d} | RF: {rf:2d}×{rf:2d}")
        
        final_rf = data["final_rf"]
        coverage = data["coverage"]
        print(f"   {'Final Coverage':<25} | RF: {final_rf}×{final_rf} | {coverage} of 28×28")
        
        if final_rf >= 28:
            print(f"   ✅ Full image coverage achieved!")
        else:
            print(f"   ⚠️  Partial coverage: {coverage}")

def main():
    """Run comprehensive tests on all ultra-efficient models"""
    print("🚀 Ultra-Efficient Models Comprehensive Testing")
    print("=" * 60)
    
    if not TORCH_AVAILABLE:
        print("⚠️  PyTorch not installed. Install with: pip install torch torchvision")
        print("📊 Running parameter validation only...\n")
        
        # Import and run parameter validation
        import subprocess
        result = subprocess.run(["python3", "validate_ultra_models.py"], 
                              capture_output=True, text=True)
        print(result.stdout)
        return
    
    # Test all models
    models_to_test = [
        (Model_1, "Model_1"),
        (Model_2, "Model_2"),
        (Model_3, "Model_3")
    ]
    
    results = []
    for model_class, model_name in models_to_test:
        success = test_model_architecture(model_class, model_name)
        results.append((model_name, success))
    
    # Test create_model function
    print(f"\n🏭 Testing create_model() function")
    print("-" * 50)
    
    try:
        for model_name in ["Model_1", "Model_2", "Model_3"]:
            model = create_model(model_name)
            print(f"✅ create_model('{model_name}') successful")
    except Exception as e:
        print(f"❌ create_model() failed: {str(e)}")
        results.append(("create_model", False))
    else:
        results.append(("create_model", True))
    
    # Receptive field analysis
    test_receptive_field_analysis()
    
    # Summary
    print(f"\n📋 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<15} | {status}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Models are ready for training.")
        print("🚀 Next steps:")
        print("   1. Train Model_1 for baseline (~98% accuracy)")
        print("   2. Train Model_2 for efficiency (~99.2% accuracy)")
        print("   3. Train Model_3 for precision (99.4%+ accuracy)")
        print("   4. Achieve target in ≤15 epochs")
    else:
        print("⚠️  Some tests failed. Please review the models.")
    
    print(f"\n📊 Parameter Summary:")
    if TORCH_AVAILABLE:
        for model_class, model_name in models_to_test:
            model = model_class()
            params = model.count_parameters()
            print(f"   {model_name}: {params:,} parameters")

if __name__ == "__main__":
    main()
