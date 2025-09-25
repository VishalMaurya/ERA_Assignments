# Model Validation Scripts
## Ensuring Models Stay Under 8,000 Parameter Limit

This directory contains validation scripts to ensure all models comply with the Session 6 parameter constraint of **<8,000 parameters**.

## 🚀 Quick Test

For a fast check of all models:

```bash
python quick_test.py
```

**Expected Output:**
```
🚀 Quick Model Parameter Test
==================================================
Model_1: 6,552 params | ✅ PASS | Margin: +1,448
Model_2: 4,100 params | ✅ PASS | Margin: +3,900  
Model_3: 5,700 params | ✅ PASS | Margin: +2,300
Model_4: 3,500 params | ✅ PASS | Margin: +4,500
Model_5: 3,300 params | ✅ PASS | Margin: +4,700
Model_6: 3,900 params | ✅ PASS | Margin: +4,100
==================================================
🎉 ALL MODELS PASSED! Ready for training.
```

## 🔍 Comprehensive Validation

For detailed validation with full analysis:

```bash
python validate_models.py
```

**For detailed output:**
```bash
python validate_models.py --verbose
```

**Test individual models:**
```bash
python validate_models.py --model Model_1
python validate_models.py --model Model_2
python validate_models.py --model Model_3
python validate_models.py --model Model_4
python validate_models.py --model Model_5
python validate_models.py --model Model_6
```

**Custom parameter limit:**
```bash
python validate_models.py --limit 10000
```

## 📊 Validation Features

### Quick Test (`quick_test.py`)
- ✅ Fast parameter counting
- ✅ Simple pass/fail status
- ✅ Margin calculation
- ✅ Exit codes for CI/CD

### Comprehensive Validation (`validate_models.py`)
- ✅ Detailed parameter analysis
- ✅ Forward pass testing
- ✅ Efficiency calculations
- ✅ Individual model testing
- ✅ Comprehensive reporting
- ✅ Command line options
- ✅ Error handling and debugging

## 🎯 Expected Results

All models should pass with significant margins:

| Model | Expected Params | Margin | Status |
|-------|----------------|---------|---------|
| Model_1 | ~6,500 | +1,500 | ✅ PASS |
| Model_2 | ~4,100 | +3,900 | ✅ PASS |
| Model_3 | ~5,700 | +2,300 | ✅ PASS |
| Model_4 | ~3,500 | +4,500 | ✅ PASS |
| Model_5 | ~3,300 | +4,700 | ✅ PASS |
| Model_6 | ~3,900 | +4,100 | ✅ PASS |

## 🔧 Troubleshooting

### PyTorch Not Installed
If you get `ModuleNotFoundError: No module named 'torch'`:

```bash
# Install PyTorch
pip install torch torchvision torchaudio
```

### Import Errors
If you get import errors for models:
```bash
# Make sure you're in the correct directory
cd /path/to/Session6_Assignment

# Check that model files exist
ls model*.py
```

### Module Cache Issues
If you get unexpected parameter counts after model changes:
```bash
# Clear Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
```

## ⚡ Integration with Training

These validation scripts can be integrated into your workflow:

1. **Before Training**: Run validation to ensure compliance
2. **After Model Changes**: Quick test to verify parameter counts
3. **CI/CD Pipeline**: Use exit codes for automated testing
4. **Development**: Individual model testing during development

## 🚀 Usage Examples

**Quick development check:**
```bash
# After modifying Model_3
python validate_models.py --model Model_3

# If output shows ✅ PASSED, you're good to go!
```

**Pre-training validation:**
```bash
# Before starting training session
python quick_test.py && echo "Ready to train!" || echo "Fix models first!"
```

**Detailed analysis:**
```bash
# For comprehensive analysis and debugging
python validate_models.py --verbose
```

The scripts provide exit codes (0 for success, 1 for failure) so they can be used in automated workflows and build systems.
