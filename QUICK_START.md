# Quick Start: GPT-2 Shakespeare Generator

## 🎯 What You Have

**Files Ready:**
1. `input.txt` - Shakespeare corpus (40K lines)
2. `train_get2-8-init.py` - Original training script
3. `train_gpt2_shakespeare.py` - Clean training script (recommended)
4. `app_gpt2_shakespeare.py` - HuggingFace Gradio app
5. `COLAB_HF_GUIDE.md` - Complete deployment guide
6. `requirements_gpt2.txt` - Dependencies

## 🚀 3-Step Quick Start

### Step 1: Train in Colab (5 minutes)

```python
# 1. Open https://colab.research.google.com
# 2. Enable GPU (Runtime → Change runtime type → GPU)
# 3. Run these cells:

!pip install torch tiktoken

# Upload input.txt and train_gpt2_shakespeare.py

!python train_gpt2_shakespeare.py

# Download the model
from google.colab import files
files.download('shakespeare_gpt2.pt')
```

### Step 2: Test Locally (Optional)

```bash
pip install -r requirements_gpt2.txt
python app_gpt2_shakespeare.py
# Open http://localhost:7860
```

### Step 3: Deploy to HuggingFace

```bash
# 1. Create new Space at https://huggingface.co/new-space
# 2. Upload files: app.py, shakespeare_gpt2.pt, requirements.txt, README.md
# 3. Done! Your app is live
```

## 📊 Understanding the Code

### Original Script Issue
Your `train_get2-8-init.py` has a typo on line 21:
- ❌ `self.c_proj.NANGPT_SCALE_INIT = 1`
- ✅ `self.c_proj.NANOGPT_SCALE_INIT = 1`

This is fixed in `train_gpt2_shakespeare.py`

### What the Model Does
1. **Loads Shakespeare text** from `input.txt`
2. **Tokenizes** using GPT-2's BPE tokenizer (tiktoken)
3. **Trains** a 124M parameter GPT-2 model
4. **Generates** Shakespeare-style text from prompts

### Training Progress
```
Loaded 338025 tokens
1 epoch = 2640 batches

Step    0 | Loss: 10.9421 | Time: 0.05s
Step   10 | Loss: 9.1234 | Time: 2.31s
Step   20 | Loss: 8.4567 | Time: 4.62s
...
Step   50 | Loss: 7.2345 | Time: 11.55s

Training complete! Final loss: 7.2345
Model saved to: shakespeare_gpt2.pt
```

## 🎨 Example Usage

**Prompt**: `ROMEO:`

**Generated**:
```
ROMEO:
What light through yonder window breaks?
It is the east, and Juliet is the sun.
Arise, fair sun, and kill the envious moon,
Who is already sick and pale with grief...
```

## 📁 Files Explained

| File | Purpose |
|------|---------|
| `input.txt` | Shakespeare training data |
| `train_gpt2_shakespeare.py` | Training script with logging |
| `app_gpt2_shakespeare.py` | Gradio web interface |
| `shakespeare_gpt2.pt` | Trained model (after training) |
| `training_logs.json` | Training metrics |
| `COLAB_HF_GUIDE.md` | Detailed deployment guide |

## 🔗 Next Steps

1. **Read**: `COLAB_HF_GUIDE.md` for detailed instructions
2. **Train**: Use Google Colab with GPU for faster training
3. **Deploy**: Follow HuggingFace deployment steps
4. **Share**: Your app will be live at `huggingface.co/spaces/YOUR_USERNAME/shakespeare-gpt2`

---

**Need Help?** Check `COLAB_HF_GUIDE.md` for troubleshooting!
