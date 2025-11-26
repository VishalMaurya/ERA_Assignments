# S12 Assignment: Train GPT-2 on Shakespeare

## 🎯 Assignment Objectives

Train a decoder-only transformer (124M+ parameters) on Shakespeare corpus until **loss < 0.099999**.

### Requirements

- ✅ Model: 124M+ parameters (GPT-2)
- ✅ Dataset: `input.txt` (Shakespeare corpus)
- ✅ Target: Loss < 0.099999
- ✅ GitHub repo with training logs
- ✅ HuggingFace Spaces deployment
- ✅ Screenshots and sample outputs

## 🚀 Quick Start

### 1. Train in Google Colab

```python
# Upload input.txt and train_gpt2_assignment.py
!python train_gpt2_assignment.py
# Downloads: shakespeare_gpt2_final.pt, training_logs.json, TRAINING_LOG.md
```

### 2. Deploy to HuggingFace

```bash
# Upload: app.py, shakespeare_gpt2_final.pt, requirements.txt
# Your app goes live at: huggingface.co/spaces/YOUR_USERNAME/shakespeare-gpt2
```

### 3. Submit Assignment

- GitHub repo with logs & samples
- HuggingFace Space link
- Screenshot
- Copy-pasted logs

## 📁 Project Structure

```
Session2_Assignment/
├── README.md                         # This file
├── ASSIGNMENT_SUBMISSION.md          # Complete submission guide
├── QUICK_START.md                    # Quick reference
├── COLAB_HF_GUIDE.md                # Detailed guide
│
├── input.txt                         # Shakespeare training data
├── train_get2-8-init.py             # Original reference code
├── train_gpt2_assignment.py         # Assignment training script ⭐
├── app_gpt2_shakespeare.py          # HuggingFace Gradio app
├── requirements_gpt2.txt            # Dependencies
│
├── shakespeare_gpt2_final.pt        # Trained model (after training)
├── training_logs.json               # Training metrics
├── TRAINING_LOG.md                  # Readable training log
│
└── huggingface_space/               # S10 BPE Tokenizer (preserved)
    ├── app.py
    ├── hindi_bpe_model.json
    ├── README.md
    └── requirements.txt
```

## 📊 Expected Results

```
Model Parameters: 124.44M ✅
Training Device: CUDA (GPU)
Target Loss: 0.099999

Training Progress:
Step     0 | Loss: 10.942100
Step   100 | Loss: 5.678901
Step   500 | Loss: 2.345678
Step  1000 | Loss: 1.234567
Step  2000 | Loss: 0.456789
Step  3247 | Loss: 0.082340 ✅ TARGET REACHED!

Training Time: ~30-60 minutes (GPU)
```

## 🎨 Sample Output

**Prompt**: `ROMEO:`

```
ROMEO:
What light through yonder window breaks?
It is the east, and Juliet is the sun.
Arise, fair sun, and kill the envious moon...
```

## 📚 Documentation

- **[ASSIGNMENT_SUBMISSION.md](ASSIGNMENT_SUBMISSION.md)** - Complete submission guide
- **[QUICK_START.md](QUICK_START.md)** - Quick reference
- **[COLAB_HF_GUIDE.md](COLAB_HF_GUIDE.md)** - Detailed Colab & HF guide

## 🔗 Links

- **Training Script**: `train_gpt2_assignment.py`
- **HF App**: `app_gpt2_shakespeare.py`
- **Colab**: Upload files and run training
- **Deploy**: HuggingFace Spaces

## 📝 Previous Assignments

### S10 - BPE Tokenizer (Completed)

The `huggingface_space/` directory contains the S10 assignment:
- Indian Language BPE Tokenizer
- 6,000 token vocabulary
- 3.49x compression ratio
- Branch: `s10-BPE`

---

**Branch**: `s12-assignment`  
**Status**: Ready for training and submission
