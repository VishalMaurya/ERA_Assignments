#!/usr/bin/env python3
"""
Simple validation script without PyTorch dependencies.
Tests imports and function availability.
"""

def test_model_imports():
    """Test that all models can be imported and functions exist."""
    print("🧪 TESTING MODEL IMPORTS & STRUCTURE")
    print("="*50)
    
    models_to_test = [
        ('Model_1', 'model1', 'create_model_1', 'analyze_model_1'),
        ('Model_2', 'model2', 'create_model_2', 'analyze_model_2'), 
        ('Model_3', 'model3', 'create_model_3', 'analyze_model_3'),
        ('Model_4', 'model4', 'create_model_4', 'analyze_model_4'),
        ('Model_5', 'model5', 'create_model_5', 'analyze_model_5'),
        ('Model_6', 'model6', 'create_model_6', 'analyze_model_6'),
        ('Model_7', 'model7', 'create_model_7', 'analyze_model_7')
    ]
    
    successful_imports = 0
    
    for model_name, module_name, create_func, analyze_func in models_to_test:
        print(f"\n🔍 Testing {model_name}...")
        
        try:
            # Test module import
            module = __import__(module_name)
            print(f"  ✅ Import: {module_name} imported successfully")
            
            # Test create function exists
            if hasattr(module, create_func):
                print(f"  ✅ Function: {create_func} found")
            else:
                print(f"  ❌ Function: {create_func} missing")
                available_funcs = [name for name in dir(module) if not name.startswith('_')]
                print(f"     Available functions: {available_funcs}")
                continue
                
            # Test analyze function exists
            if hasattr(module, analyze_func):
                print(f"  ✅ Function: {analyze_func} found")
            else:
                print(f"  ❌ Function: {analyze_func} missing")
                continue
            
            # Check for class definition
            class_name = model_name.replace('_', '_')  # Model_1 -> Model_1
            if hasattr(module, class_name):
                print(f"  ✅ Class: {class_name} found")
            else:
                print(f"  ⚠️  Class: {class_name} not found (may be internal)")
            
            successful_imports += 1
            print(f"  🎉 {model_name}: Import structure OK!")
            
        except ImportError as e:
            print(f"  ❌ Import Error: {e}")
        except SyntaxError as e:
            print(f"  ❌ Syntax Error: {e}")
        except Exception as e:
            print(f"  ❌ Other Error: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 IMPORT RESULTS:")
    print(f"  Total Models: {len(models_to_test)}")
    print(f"  Successful Imports: {successful_imports}")
    print(f"  Success Rate: {successful_imports/len(models_to_test)*100:.1f}%")
    
    if successful_imports == len(models_to_test):
        print(f"🎉 ALL MODEL IMPORTS SUCCESSFUL!")
        print(f"✅ Ready for PyTorch training!")
        return True
    else:
        print(f"⚠️  {len(models_to_test) - successful_imports} models have import issues")
        return False

def check_syntax_errors():
    """Check for obvious syntax errors in model files."""
    print(f"\n🔍 CHECKING SYNTAX...")
    
    model_files = [
        'model1.py', 'model2.py', 'model3.py', 
        'model4.py', 'model5.py', 'model6.py', 'model7.py'
    ]
    
    syntax_ok = 0
    
    for file_name in model_files:
        try:
            with open(file_name, 'r') as f:
                content = f.read()
            
            # Try to compile
            compile(content, file_name, 'exec')
            print(f"  ✅ {file_name}: Syntax OK")
            syntax_ok += 1
            
        except SyntaxError as e:
            print(f"  ❌ {file_name}: Syntax Error at line {e.lineno}: {e.msg}")
        except FileNotFoundError:
            print(f"  ❌ {file_name}: File not found")
        except Exception as e:
            print(f"  ❌ {file_name}: Other error: {e}")
    
    print(f"\n📊 SYNTAX CHECK: {syntax_ok}/{len(model_files)} files OK")
    return syntax_ok == len(model_files)

if __name__ == "__main__":
    print("🚀 MODEL VALIDATION (Without PyTorch)")
    print("="*60)
    
    # Check syntax first
    syntax_ok = check_syntax_errors()
    
    # Test imports
    imports_ok = test_model_imports()
    
    print(f"\n{'='*60}")
    if syntax_ok and imports_ok:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ Models are ready for training with PyTorch!")
    else:
        print("⚠️  ISSUES FOUND - Check output above")
