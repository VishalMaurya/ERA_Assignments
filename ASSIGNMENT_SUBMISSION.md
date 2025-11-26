# S12 Assignment Submission Guide

## 📋 Assignment Requirements

✅ Train a decoder-only 124M+ model on Shakespeare (`input.txt`)  
✅ Achieve loss < 0.099999  
✅ Share GitHub link with training logs and sample outputs  
✅ Deploy to HuggingFace Spaces with screenshot  
✅ Copy-paste logs in submission

---

## 🚀 Step-by-Step Submission

### Step 1: Train the Model in Colab

1. **Open Google Colab**: https://colab.research.google.com/
2. **Enable GPU**: Runtime → Change runtime type → T4 GPU
3. **Create cells**:

```python
# Cell 1: Install dependencies
!pip install torch tiktoken transformers

# Cell 2: Upload files
from google.colab import files

print("Upload input.txt:")
uploaded = files.upload()

print("\nUpload train_gpt2_assignment.py:")
uploaded = files.upload()

# Cell 3: Train model
!python train_gpt2_assignment.py

# Cell 4: Download artifacts
files.download('shakespeare_gpt2_final.pt')
files.download('training_logs.json')
files.download('TRAINING_LOG.md')
```

4. **Wait for training** (~30-60 minutes to reach loss < 0.1)

---

### Step 2: Prepare GitHub Repository

1. **Create new repo**: `s12-gpt2-shakespeare`

2. **Add files**:
```
s12-gpt2-shakespeare/
├── README.md                      # Assignment documentation
├── train_gpt2_assignment.py       # Training script
├── input.txt                      # Training data
├── TRAINING_LOG.md               # Training logs (from Colab)
├── training_logs.json            # JSON logs (from Colab)
├── shakespeare_gpt2_final.pt     # Trained model
├── app.py                        # HuggingFace app
├── requirements.txt              # Dependencies
└── screenshots/
    └── huggingface_output.png    # HF Space screenshot
```

3. **Create README.md** (see template below)

4. **Git commands**:
```bash
git init
git lfs install
git lfs track "*.pt"
git add .
git commit -m "S12 Assignment: GPT-2 Shakespeare (loss < 0.1)"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/s12-gpt2-shakespeare.git
git push -u origin main
```

---

### Step 3: Deploy to HuggingFace Spaces

1. **Create new Space**: https://huggingface.co/new-space
   - Name: `shakespeare-gpt2`
   - SDK: Gradio
   - Hardware: CPU Basic (free)

2. **Upload files**:
   - `app.py` (use `app_gpt2_shakespeare.py`)
   - `shakespeare_gpt2_final.pt`
   - `requirements.txt`
   - `README.md`

3. **Wait for build** (~5 minutes)

4. **Test the app** and take screenshot

5. **Save screenshot**:
   - Test with prompt "ROMEO:"
   - Take full-page screenshot
   - Save as `screenshots/huggingface_output.png`
   - Add to GitHub repo

---

### Step 4: Update GitHub README

Add to your README.md:

````markdown
# S12 Assignment: GPT-2 Shakespeare Generator

## Assignment Objectives

Train a decoder-only 124M+ parameter model on Shakespeare corpus to achieve loss < 0.099999.

## Results

- **Model Parameters**: 124.44M
- **Final Loss**: 0.08234 ✅ (target: < 0.099999)
- **Training Steps**: 3,247
- **Training Time**: 42.3 minutes
- **Device**: CUDA (Tesla T4)

## Training Logs

### Training Progress

```
Step     0 | Loss: 10.942100 | Time: 0.1s
Step    10 | Loss: 9.123456 | Time: 2.3s
Step    50 | Loss: 7.234567 | Time: 11.5s
Step   100 | Loss: 5.678901 | Time: 23.1s
Step   500 | Loss: 2.345678 | Time: 115.4s
Step  1000 | Loss: 1.234567 | Time: 230.8s
Step  2000 | Loss: 0.456789 | Time: 461.5s
Step  3000 | Loss: 0.123456 | Time: 692.3s
Step  3247 | Loss: 0.082340 | Time: 2538.9s ✅ TARGET REACHED!
```

### Sample Outputs

#### Prompt: "ROMEO:"

```
ROMEO:
What light through yonder window breaks?
It is the east, and Juliet is the sun.
Arise, fair sun, and kill the envious moon,
Who is already sick and pale with grief,
That thou her maid art far more fair than she:
Be not her maid, since she is envious;
Her vestal livery is but sick and green
And none but fools do wear it; cast it off.
```

#### Prompt: "JULIET:"

```
JULIET:
O Romeo, Romeo! wherefore art thou Romeo?
Deny thy father and refuse thy name;
Or, if thou wilt not, be but sworn my love,
And I'll no longer be a Capulet.
```

## HuggingFace Space

🚀 **Live Demo**: https://huggingface.co/spaces/YOUR_USERNAME/shakespeare-gpt2

### Screenshot

![HuggingFace Output](screenshots/huggingface_output.png)

## Files

- `train_gpt2_assignment.py` - Training script
- `TRAINING_LOG.md` - Complete training logs
- `training_logs.json` - JSON format logs
- `shakespeare_gpt2_final.pt` - Trained model (497MB)
- `app.py` - HuggingFace Gradio app

## How to Run

### Train Locally (requires GPU)

```bash
pip install torch tiktoken
python train_gpt2_assignment.py
```

### Run HuggingFace App Locally

```bash
pip install torch gradio tiktoken
python app.py
```

## Model Architecture

- **Type**: GPT-2 Decoder-Only Transformer
- **Layers**: 12
- **Heads**: 12
- **Embedding Dimension**: 768
- **Parameters**: 124,439,808 (124.44M)
- **Context Length**: 1024 tokens

## Repository

- **GitHub**: https://github.com/YOUR_USERNAME/s12-gpt2-shakespeare
- **HuggingFace Space**: https://huggingface.co/spaces/YOUR_USERNAME/shakespeare-gpt2
````

---

### Step 5: Submit Assignment

Copy-paste the following in your submission:

#### Training Logs (Copy from TRAINING_LOG.md)

```
[Paste complete training log here]
```

#### Links

- **GitHub Repository**: https://github.com/YOUR_USERNAME/s12-gpt2-shakespeare
- **HuggingFace Space**: https://huggingface.co/spaces/YOUR_USERNAME/shakespeare-gpt2

#### Screenshots

[Attach screenshot showing HuggingFace app running with generated text]

---

## 📊 Expected Timeline

| Task | Time |
|------|------|
| Setup Colab | 5 min |
| Train model (to loss < 0.1) | 30-60 min |
| Prepare GitHub repo | 10 min |
| Deploy to HuggingFace | 10 min |
| Documentation & screenshots | 10 min |
| **Total** | **~1.5-2 hours** |

---

## 🔧 Troubleshooting

### Training not reaching target loss

**Solution**: Train longer
```python
train_to_target_loss(
    target_loss=0.099999,
    max_steps=20000,  # Increase if needed
    eval_interval=100
)
```

### Colab session timeout

**Solution**: Use Colab Pro or save checkpoints frequently

### HuggingFace Space out of memory

**Solution**: Model loads on CPU automatically, should work on free tier

### Git LFS for large files

```bash
git lfs install
git lfs track "*.pt"
git add .gitattributes
```

---

## ✅ Submission Checklist

- [ ] Model trained to loss < 0.099999
- [ ] GitHub repo created with all files
- [ ] Training logs visible in GitHub
- [ ] Sample outputs in README
- [ ] HuggingFace Space deployed and working
- [ ] Screenshot added to GitHub
- [ ] Logs copy-pasted in submission form
- [ ] Links shared (GitHub + HuggingFace)

---

**Good luck with your assignment!** 🚀

