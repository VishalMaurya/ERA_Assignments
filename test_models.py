#!/usr/bin/env python3
"""
Test script to verify all models can be imported and created correctly.
Run this to debug import issues.
"""

def test_model_imports():
    """Test importing all model modules."""
    print("🧪 TESTING MODEL IMPORTS")
    print("="*50)
    
    models_to_test = [
        ('model1', 'create_model_1', 'analyze_model_1'),
        ('model2', 'create_model_2', 'analyze_model_2'),
        ('model3', 'create_model_3', 'analyze_model_3'),
        ('model4', 'create_model_4', 'analyze_model_4'),
        ('model5', 'create_model_5', 'analyze_model_5'),
        ('model6', 'create_model_6', 'analyze_model_6'),
        ('model7', 'create_model_7', 'analyze_model_7')
    ]
    
    successful_imports = 0
    successful_creations = 0
    
    for module_name, create_func, analyze_func in models_to_test:
        print(f"\n🔍 Testing {module_name}...")
        
        # Test import
        try:
            module = __import__(module_name)
            print(f"  ✅ Import: {module_name} imported successfully")
            
            # Check if functions exist
            if hasattr(module, create_func):
                print(f"  ✅ Function: {create_func} found")
            else:
                print(f"  ❌ Function: {create_func} missing")
                available_funcs = [name for name in dir(module) if not name.startswith('_')]
                print(f"     Available functions: {available_funcs}")
                continue
                
            if hasattr(module, analyze_func):
                print(f"  ✅ Function: {analyze_func} found")
            else:
                print(f"  ❌ Function: {analyze_func} missing")
                continue
                
            successful_imports += 1
            
            # Test model creation
            try:
                create_function = getattr(module, create_func)
                model = create_function()
                print(f"  ✅ Creation: Model created successfully")
                
                # Test parameter counting
                if hasattr(model, 'count_parameters'):
                    params = model.count_parameters()
                    print(f"  📊 Parameters: {params:,}")
                    if params < 8000:
                        print(f"  ✅ Compliance: Under 8,000 limit")
                    else:
                        print(f"  ⚠️  Compliance: Over 8,000 limit ({params - 8000:,} excess)")
                else:
                    print(f"  ⚠️  Method: count_parameters not found")
                
                successful_creations += 1
                
            except Exception as e:
                print(f"  ❌ Creation: Failed - {e}")
                
        except ImportError as e:
            print(f"  ❌ Import: {module_name} failed - {e}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 SUMMARY:")
    print(f"  Successful imports: {successful_imports}/7")
    print(f"  Successful creations: {successful_creations}/7")
    
    if successful_imports == 7 and successful_creations == 7:
        print(f"🎉 ALL MODELS WORKING PERFECTLY!")
        return True
    else:
        print(f"⚠️  Some models have issues - check output above")
        return False

def test_train_imports():
    """Test the imports that train.py uses."""
    print(f"\n🧪 TESTING TRAIN.PY IMPORTS")
    print("="*50)
    
    import_tests = [
        "from model1 import create_model_1, analyze_model_1",
        "from model2 import create_model_2, analyze_model_2", 
        "from model3 import create_model_3, analyze_model_3",
        "from model4 import create_model_4, analyze_model_4",
        "from model5 import create_model_5, analyze_model_5",
        "from model6 import create_model_6, analyze_model_6",
        "from model7 import create_model_7, analyze_model_7"
    ]
    
    successful = 0
    for import_stmt in import_tests:
        try:
            exec(import_stmt)
            print(f"✅ {import_stmt}")
            successful += 1
        except Exception as e:
            print(f"❌ {import_stmt}")
            print(f"   Error: {e}")
    
    print(f"\nImport success rate: {successful}/{len(import_tests)}")
    return successful == len(import_tests)

if __name__ == "__main__":
    print("🚀 MODEL TESTING SCRIPT")
    print("="*60)
    
    # Test individual model imports
    models_ok = test_model_imports()
    
    # Test train.py style imports
    imports_ok = test_train_imports()
    
    print(f"\n{'='*60}")
    if models_ok and imports_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Ready to run train.py")
    else:
        print("⚠️  ISSUES FOUND - Check output above")
        print("💡 Fix the issues before running train.py")
