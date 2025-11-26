# GPT-2 Shakespeare: Colab Training & HuggingFace Deployment Guide

## 📋 Overview

Train a GPT-2 model on Shakespeare text in Google Colab and deploy it as a HuggingFace Space.

**What You'll Build:**
- GPT-2 model (124M parameters) trained from scratch
- Training on Shakespeare corpus
- Interactive web app for text generation
- Deployment on HuggingFace Spaces

---

## 🚀 Part 1: Training in Google Colab

### Step 1: Setup Colab

1. **Open Google Colab**: https://colab.research.google.com/
2. **Enable GPU**: Runtime → Change runtime type → GPU (T4)
3. **Create New Notebook**

### Step 2: Upload Files

```python
# Cell 1: Upload files
from google.colab import files

# Upload input.txt (Shakespeare text)
print("Upload input.txt:")
uploaded = files.upload()

# Or download from web
# !wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt
```

### Step 3: Install Dependencies

```python
# Cell 2: Install dependencies
!pip install torch tiktoken transformers matplotlib
```

### Step 4: Copy Training Code

Upload `train_gpt2_shakespeare.py` or paste the code directly into cells.

### Step 5: Train Model

```python
# Cell 3: Import and train
from train_gpt2_shakespeare import train

# Train for 100 steps (increase for better results)
model, losses = train(num_steps=100, save_path='shakespeare_gpt2.pt')
```

### Step 6: Monitor Training

```python
# Cell 4: Visualize training
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(losses)
plt.xlabel('Step')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.grid(True)
plt.show()

print(f"Initial Loss: {losses[0]:.4f}")
print(f"Final Loss: {losses[-1]:.4f}")
print(f"Improvement: {(losses[0] - losses[-1]) / losses[0] * 100:.1f}%")
```

### Step 7: Test Generation

```python
# Cell 5: Generate text
import torch
import torch.nn.functional as F
import tiktoken
from train_gpt2_shakespeare import GPT, GPTConfig

# Load model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = GPT(GPTConfig())
checkpoint = torch.load('shakespeare_gpt2.pt', map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

enc = tiktoken.get_encoding('gpt2')

def generate(prompt="ROMEO:", max_length=150):
    tokens = enc.encode(prompt)
    tokens = torch.tensor(tokens).unsqueeze(0).to(device)
    
    with torch.no_grad():
        for _ in range(max_length):
            logits, _ = model(tokens)
            logits = logits[:, -1, :] / 0.8
            probs = F.softmax(logits, dim=-1)
            topk_probs, topk_indices = torch.topk(probs, 50)
            ix = torch.multinomial(topk_probs, 1)
            next_token = torch.gather(topk_indices, -1, ix)
            tokens = torch.cat([tokens, next_token], dim=1)
    
    return enc.decode(tokens[0].tolist())

# Test generation
print(generate("ROMEO:", max_length=100))
```

### Step 8: Download Artifacts

```python
# Cell 6: Download model and logs
from google.colab import files

# Download trained model
files.download('shakespeare_gpt2.pt')

# Download training logs
files.download('training_logs.json')

# Create and download loss plot
plt.figure(figsize=(12, 5))
plt.plot(losses)
plt.xlabel('Training Step')
plt.ylabel('Loss')
plt.title('GPT-2 Training on Shakespeare')
plt.grid(True)
plt.savefig('training_loss.png', dpi=150, bbox_inches='tight')
files.download('training_loss.png')
```

---

## 📊 Expected Results

**Training Metrics:**
- Model Parameters: ~124M
- Initial Loss: ~10-11
- After 50 steps: ~8-9
- After 100 steps: ~7-8
- After 500 steps: ~5-6 (better quality)

**Training Time (GPU T4):**
- 50 steps: ~1-2 minutes
- 100 steps: ~2-3 minutes
- 500 steps: ~10-15 minutes

---

## 🌐 Part 2: Deploy to HuggingFace Spaces

### Step 1: Prepare Files

Create a new directory with these files:

```
shakespeare_gpt/
├── app.py                    # Gradio app (use app_gpt2_shakespeare.py)
├── shakespeare_gpt2.pt       # Trained model (downloaded from Colab)
├── requirements.txt          # Dependencies
└── README.md                 # App documentation
```

### Step 2: Create requirements.txt

```txt
torch
gradio
tiktoken
```

### Step 3: Create README.md for HF Space

```markdown
---
title: Shakespeare GPT-2 Generator
emoji: 📜
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Shakespeare GPT-2 Generator

Generate Shakespeare-style text using a GPT-2 model trained from scratch.

## Model Details
- Architecture: GPT-2 (124M parameters)
- Training Data: Complete works of Shakespeare
- Framework: PyTorch
- Tokenizer: tiktoken (GPT-2 BPE)

## Usage
1. Enter a prompt (e.g., "ROMEO:", "To be or not to be,")
2. Adjust generation parameters
3. Click Submit to generate text

## Parameters
- **Max Length**: Number of tokens to generate
- **Temperature**: Controls randomness (lower = more focused)
- **Top-K**: Limits vocabulary for sampling
```

### Step 4: Deploy to HuggingFace

**Option A: Web Interface**

1. Go to https://huggingface.co/new-space
2. Name your Space (e.g., "shakespeare-gpt2")
3. Select "Gradio" SDK
4. Upload all files
5. Wait for build & deploy

**Option B: Git (Recommended)**

```bash
# Install git-lfs
git lfs install

# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/shakespeare-gpt2
cd shakespeare-gpt2

# Add files
cp app.py shakespeare_gpt2.pt requirements.txt README.md .

# Commit and push
git add .
git commit -m "Initial commit: Shakespeare GPT-2"
git push
```

### Step 5: Test Your App

Visit: `https://huggingface.co/spaces/YOUR_USERNAME/shakespeare-gpt2`

---

## 🔧 Troubleshooting

### Issue: Model Too Large
**Solution**: Use Git LFS for large files

```bash
git lfs track "*.pt"
git add .gitattributes
```

### Issue: Out of Memory on HF
**Solution**: Reduce model size or use CPU

```python
# In app.py, force CPU
device = 'cpu'
```

### Issue: Slow Generation
**Solution**: Reduce max_length or use smaller model

---

## 📈 Improving Results

### Train Longer
```python
# In Colab
train(num_steps=1000)  # Better quality
```

### Adjust Learning Rate
```python
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)  # Lower LR
```

### Use Gradient Accumulation
```python
# For larger effective batch size
accumulation_steps = 4
for i, (x, y) in enumerate(dataloader):
    loss = model(x, y)[1] / accumulation_steps
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

---

## 📁 File Structure Summary

**Local Development:**
```
Session2_Assignment/
├── input.txt                      # Shakespeare corpus
├── train_get2-8-init.py          # Original training script
├── train_gpt2_shakespeare.py     # Clean training script
├── app_gpt2_shakespeare.py       # Gradio app
├── COLAB_HF_GUIDE.md            # This guide
└── shakespeare_gpt2.pt          # Trained model (after training)
```

**HuggingFace Space:**
```
shakespeare-gpt2/
├── app.py                        # Gradio interface
├── shakespeare_gpt2.pt          # Trained model
├── requirements.txt             # Dependencies
└── README.md                    # Space documentation
```

---

## 🎯 Quick Start Checklist

- [ ] Open Google Colab with GPU
- [ ] Upload `input.txt`
- [ ] Install dependencies
- [ ] Run training script
- [ ] Download trained model
- [ ] Create HuggingFace Space
- [ ] Upload files
- [ ] Test deployed app

---

## 🔗 Useful Links

- **Google Colab**: https://colab.research.google.com/
- **HuggingFace Spaces**: https://huggingface.co/spaces
- **Gradio Docs**: https://gradio.app/docs/
- **Original GPT-2**: https://github.com/openai/gpt-2

---

**Happy Training!** 🚀

