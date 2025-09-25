#!/usr/bin/env python3
"""
Quick Model Parameter Test
=========================

Simple script to quickly check if all models are under 8,000 parameters.
"""

def quick_test():
    """Quick test of all models."""
    
    print("🚀 Quick Model Parameter Test")
    print("="*50)
    
    models_info = [
        ('Model_1', 'model1', 'create_model_1'),
        ('Model_2', 'model2', 'create_model_2'), 
        ('Model_3', 'model3', 'create_model_3'),
        ('Model_4', 'model4', 'create_model_4'),
        ('Model_5', 'model5', 'create_model_5'),
        ('Model_6', 'model6', 'create_model_6')
    ]
    
    results = []
    all_passed = True
    
    for model_name, module_name, create_func in models_info:
        try:
            # Import and create model
            module = __import__(module_name)
            create_model = getattr(module, create_func)
            model = create_model()
            
            # Count parameters
            params = model.count_parameters()
            under_limit = params < 8000
            
            # Status
            status = "✅ PASS" if under_limit else "❌ FAIL"
            margin = 8000 - params
            
            print(f"{model_name}: {params:,} params | {status} | Margin: {margin:+,}")
            
            results.append((model_name, params, under_limit))
            if not under_limit:
                all_passed = False
                
        except Exception as e:
            print(f"{model_name}: ❌ ERROR - {e}")
            all_passed = False
            results.append((model_name, 0, False))
    
    print("="*50)
    if all_passed:
        print("🎉 ALL MODELS PASSED! Ready for training.")
    else:
        failed = [name for name, _, passed in results if not passed]
        print(f"⚠️  FAILED MODELS: {', '.join(failed)}")
    
    return all_passed

if __name__ == "__main__":
    import sys
    success = quick_test()
    sys.exit(0 if success else 1)
