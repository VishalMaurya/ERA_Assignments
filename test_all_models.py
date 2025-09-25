#!/usr/bin/env python3
"""
Test script to verify all models can be created and run successfully.
"""

def test_model_creation_and_forward():
    """Test that all models can be created and perform forward pass."""
    print("🧪 TESTING ALL MODELS - CREATION & FORWARD PASS")
    print("="*60)
    
    # Test data
    import torch
    test_input = torch.randn(2, 1, 28, 28)  # Batch of 2 MNIST images
    
    models_to_test = [
        ('Model_1', 'model1', 'create_model_1'),
        ('Model_2', 'model2', 'create_model_2'), 
        ('Model_3', 'model3', 'create_model_3'),
        ('Model_4', 'model4', 'create_model_4'),
        ('Model_5', 'model5', 'create_model_5'),
        ('Model_6', 'model6', 'create_model_6'),
        ('Model_7', 'model7', 'create_model_7')
    ]
    
    successful_tests = 0
    
    for model_name, module_name, create_func in models_to_test:
        print(f"\n🔍 Testing {model_name}...")
        
        try:
            # Import module
            module = __import__(module_name)
            print(f"  ✅ Import: {module_name} imported successfully")
            
            # Get create function
            if hasattr(module, create_func):
                create_function = getattr(module, create_func)
                print(f"  ✅ Function: {create_func} found")
            else:
                print(f"  ❌ Function: {create_func} missing")
                continue
            
            # Create model
            model = create_function()
            print(f"  ✅ Creation: Model created successfully")
            
            # Count parameters
            if hasattr(model, 'count_parameters'):
                params = model.count_parameters()
                print(f"  📊 Parameters: {params:,}")
                
                if params < 8000:
                    print(f"  ✅ Compliance: Under 8,000 limit")
                else:
                    print(f"  ❌ Compliance: Over 8,000 limit ({params - 8000:,} excess)")
                    continue
            else:
                print(f"  ⚠️  Method: count_parameters not found")
            
            # Test forward pass
            model.eval()
            with torch.no_grad():
                output = model(test_input)
                expected_shape = (2, 10)  # Batch size 2, 10 classes
                
                if output.shape == expected_shape:
                    print(f"  ✅ Forward: {test_input.shape} -> {output.shape}")
                    print(f"  📈 Output range: [{output.min():.3f}, {output.max():.3f}]")
                else:
                    print(f"  ❌ Forward: Wrong output shape {output.shape}, expected {expected_shape}")
                    continue
            
            successful_tests += 1
            print(f"  🎉 {model_name}: ALL TESTS PASSED!")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 FINAL RESULTS:")
    print(f"  Total Models: {len(models_to_test)}")
    print(f"  Successful: {successful_tests}")
    print(f"  Success Rate: {successful_tests/len(models_to_test)*100:.1f}%")
    
    if successful_tests == len(models_to_test):
        print(f"🎉 ALL MODELS WORKING PERFECTLY!")
        print(f"✅ Ready for training!")
        return True
    else:
        print(f"⚠️  Some models have issues")
        return False

if __name__ == "__main__":
    test_model_creation_and_forward()
