#!/usr/bin/env python3
"""
SESSION 6 - Model Parameter Validation Script
===========================================

This script validates that all models comply with the 8,000 parameter limit.
Run this script to test each model architecture independently.

Usage:
    python validate_models.py

Or test individual models:
    python validate_models.py --model Model_1
    python validate_models.py --model Model_2
    python validate_models.py --model Model_3
    python validate_models.py --model Model_4
    python validate_models.py --model Model_5
    python validate_models.py --model Model_6
"""

import argparse
import sys
import traceback
from typing import Dict, Any, Optional

# Parameter limit constraint
PARAMETER_LIMIT = 8000

def validate_single_model(model_name: str, parameter_limit: int = 8000) -> Dict[str, Any]:
    """
    Validate a single model against parameter constraints.
    
    Args:
        model_name: Name of the model to validate (e.g., 'Model_1')
        
    Returns:
        Dict containing validation results
    """
    result = {
        'model_name': model_name,
        'success': False,
        'parameters': 0,
        'under_limit': False,
        'margin': 0,
        'error': None
    }
    
    try:
        # Dynamic import based on model name
        if model_name == 'Model_1':
            from model1 import create_model_1, analyze_model_1
            model = create_model_1()
            analysis = analyze_model_1()
        elif model_name == 'Model_2':
            from model2 import create_model_2, analyze_model_2
            model = create_model_2()
            analysis = analyze_model_2()
        elif model_name == 'Model_3':
            from model3 import create_model_3, analyze_model_3
            model = create_model_3()
            analysis = analyze_model_3()
        elif model_name == 'Model_4':
            from model4 import create_model_4, analyze_model_4
            model = create_model_4()
            analysis = analyze_model_4()
        elif model_name == 'Model_5':
            from model5 import create_model_5, analyze_model_5
            model = create_model_5()
            analysis = analyze_model_5()
        elif model_name == 'Model_6':
            from model6 import create_model_6, analyze_model_6
            model = create_model_6()
            analysis = analyze_model_6()
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Count parameters
        total_params = model.count_parameters()
        result['parameters'] = total_params
        result['under_limit'] = total_params < parameter_limit
        result['margin'] = parameter_limit - total_params
        result['success'] = True
        
        # Test forward pass
        import torch
        test_input = torch.randn(1, 1, 28, 28)
        with torch.no_grad():
            output = model(test_input)
            if output.shape != (1, 10):
                result['error'] = f"Invalid output shape: {output.shape}, expected (1, 10)"
                result['success'] = False
        
    except Exception as e:
        result['error'] = str(e)
        result['success'] = False
    
    return result

def print_model_result(result: Dict[str, Any], parameter_limit: int = 8000) -> None:
    """Print formatted validation result for a single model."""
    model_name = result['model_name']
    
    print(f"\n{'='*60}")
    print(f"🏗️  {model_name} VALIDATION")
    print(f"{'='*60}")
    
    if not result['success']:
        print(f"❌ FAILED: {result['error']}")
        return
    
    params = result['parameters']
    under_limit = result['under_limit']
    margin = result['margin']
    
    print(f"📊 Parameters: {params:,}")
    print(f"🎯 Limit Check: {parameter_limit:,}")
    
    if under_limit:
        print(f"✅ PASSED: {params:,} < {parameter_limit:,}")
        print(f"💡 Margin: {margin:,} parameters under limit")
        print(f"📈 Efficiency: {(params/parameter_limit)*100:.1f}% of budget used")
    else:
        print(f"❌ FAILED: {params:,} >= {parameter_limit:,}")
        print(f"⚠️  Excess: {abs(margin):,} parameters over limit")
    
    print(f"🔧 Forward Pass: ✅ Successful")

def validate_all_models(parameter_limit: int = 8000) -> Dict[str, Dict[str, Any]]:
    """Validate all models and return results."""
    models = ['Model_1', 'Model_2', 'Model_3', 'Model_4', 'Model_5', 'Model_6']
    results = {}
    
    print("🎯 SESSION 6 - MODEL PARAMETER VALIDATION")
    print("="*70)
    print(f"Parameter Limit: {parameter_limit:,}")
    print(f"Total Models: {len(models)}")
    
    for model_name in models:
        print(f"\n🔍 Validating {model_name}...")
        result = validate_single_model(model_name, parameter_limit)
        results[model_name] = result
        
        # Quick status
        if result['success'] and result['under_limit']:
            print(f"   ✅ {result['parameters']:,} params (✅ under limit)")
        elif result['success']:
            print(f"   ❌ {result['parameters']:,} params (❌ over limit)")
        else:
            print(f"   💥 Error: {result['error']}")
    
    return results

def print_summary_report(results: Dict[str, Dict[str, Any]], parameter_limit: int = 8000) -> None:
    """Print comprehensive summary report."""
    print(f"\n{'='*70}")
    print("📋 COMPREHENSIVE VALIDATION REPORT")
    print(f"{'='*70}")
    
    # Summary statistics
    total_models = len(results)
    successful_models = sum(1 for r in results.values() if r['success'])
    compliant_models = sum(1 for r in results.values() if r['success'] and r['under_limit'])
    
    print(f"\n📊 SUMMARY STATISTICS:")
    print(f"   Total Models: {total_models}")
    print(f"   Successfully Loaded: {successful_models}")
    print(f"   Parameter Compliant: {compliant_models}")
    print(f"   Compliance Rate: {(compliant_models/total_models)*100:.1f}%")
    
    # Detailed table
    print(f"\n📋 DETAILED RESULTS:")
    print(f"{'Model':<10} {'Parameters':<12} {'Status':<15} {'Margin':<12} {'Efficiency':<12}")
    print("-" * 70)
    
    for model_name, result in results.items():
        if result['success']:
            params = result['parameters']
            status = "✅ PASSED" if result['under_limit'] else "❌ FAILED"
            margin = f"{result['margin']:+,}"
            efficiency = f"{(params/parameter_limit)*100:.1f}%"
        else:
            params = "ERROR"
            status = "💥 ERROR"
            margin = "N/A"
            efficiency = "N/A"
        
        print(f"{model_name:<10} {str(params):<12} {status:<15} {margin:<12} {efficiency:<12}")
    
    # Final verdict
    print(f"\n🎯 FINAL VERDICT:")
    if compliant_models == total_models:
        print("🎉 ALL MODELS PASSED! Ready for training.")
    else:
        failed_models = [name for name, result in results.items() 
                        if not result['success'] or not result['under_limit']]
        print(f"⚠️  MODELS NEED FIXING: {', '.join(failed_models)}")

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Validate Session 6 model architectures against parameter constraints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validate_models.py                    # Validate all models
    python validate_models.py --model Model_1    # Validate only Model_1
    python validate_models.py --verbose          # Detailed output for all models
        """
    )
    
    parser.add_argument(
        '--model', 
        choices=['Model_1', 'Model_2', 'Model_3', 'Model_4', 'Model_5', 'Model_6'],
        help='Validate specific model only'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation output for each model'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=8000,
        help='Parameter limit (default: 8000)'
    )
    
    args = parser.parse_args()
    
    # Use the parameter limit from arguments
    parameter_limit = args.limit
    
    try:
        if args.model:
            # Validate single model
            print(f"🎯 VALIDATING SINGLE MODEL: {args.model}")
            result = validate_single_model(args.model, parameter_limit)
            print_model_result(result, parameter_limit)
            
            # Exit code based on validation result
            if result['success'] and result['under_limit']:
                print(f"\n✅ {args.model} VALIDATION SUCCESSFUL!")
                sys.exit(0)
            else:
                print(f"\n❌ {args.model} VALIDATION FAILED!")
                sys.exit(1)
        
        else:
            # Validate all models
            results = validate_all_models(parameter_limit)
            
            if args.verbose:
                # Show detailed results for each model
                for model_name, result in results.items():
                    print_model_result(result, parameter_limit)
            
            # Always show summary
            print_summary_report(results, parameter_limit)
            
            # Exit code based on overall compliance
            compliant_models = sum(1 for r in results.values() if r['success'] and r['under_limit'])
            if compliant_models == len(results):
                sys.exit(0)
            else:
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\n❌ Validation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
