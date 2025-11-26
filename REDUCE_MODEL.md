# 🔧 Reduce Model Size for HuggingFace

Your model file is **1.4 GB** but HuggingFace git has a **1 GB limit**.

The file is large because it includes:
- ✅ Model weights (124M params = ~500 MB)
- ❌ Optimizer state (~500 MB - not needed for inference)
- ❌ Training logs (~400 MB - not needed)

---

## 🎯 Solution: Remove Unnecessary Data

Run this script to create a minimal version:

```bash
# Make sure you have PyTorch installed
# If not: pip install torch

python reduce_model.py
```

This will create:
1. **`shakespeare_gpt2_minimal.pt`** (~500-600 MB) - Model only
2. **`shakespeare_gpt2_fp16.pt`** (~250-300 MB) - Half precision

---

## 📊 Expected Results

```
Original:       1,400 MB  (full checkpoint)
Minimal:          500 MB  (model only)
Float16:          250 MB  (half precision) ✅ BEST
```

---

## 🚀 After Reducing

### If Float16 < 1 GB (Recommended):

```bash
# Replace the large file with small one
cp shakespeare_gpt2_fp16.pt LLM_Decoder/shakespeare_gpt2_final.pt

# Push to HuggingFace
cd LLM_Decoder
git add shakespeare_gpt2_final.pt
git commit --amend -m "Add Shakespeare GPT-2 app (reduced size)"
git push origin main --force
```

### If Still Too Large:

Use web upload (handles any size):
1. Go to: https://huggingface.co/spaces/VishalMaurya/LLM_Decoder
2. Upload the reduced file manually

---

## ⚠️ Important Note

Float16 model will work perfectly for text generation. The quality difference is negligible for this task.

---

## 📋 Run in Colab (If Local Fails)

If you don't have PyTorch installed locally:

```python
# In Google Colab
!pip install torch

# Upload shakespeare_gpt2_final.pt

# Run reduction
!python reduce_model.py

# Download the reduced file
from google.colab import files
files.download('shakespeare_gpt2_fp16.pt')
```

Then use the downloaded file for HuggingFace!

---

**Ready to reduce**: Run `python reduce_model.py` 🚀

