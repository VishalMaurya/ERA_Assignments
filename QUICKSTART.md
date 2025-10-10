# ResNet CIFAR-100 Quick Start Guide

## 🚀 **5-Minute Quick Start**

### **1. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **2. Start Training**

```bash
# Quick test (1 epoch to verify everything works)
python train.py --model resnet18 --epochs 1

# Full training for assignment (100 epochs)
python train.py --model resnet18 --epochs 100 --batch-size 128
```

### **3. Monitor Training**

Training will show:
- Real-time progress bars
- Loss and accuracy per epoch
- Best model checkpoints saved automatically
- Plots saved to `logs/` directory

### **4. Deploy to HuggingFace**

After training completes:

```bash
# Export model and files
python export_for_huggingface.py

# Test locally first
python app.py
```

Then upload `huggingface_space/` directory to HuggingFace Spaces!

---

## 📊 **What to Expect**

### **Training Time (on GPU)**
- **ResNet-18**: ~4-5 hours for 100 epochs
- **ResNet-34**: ~6-7 hours for 100 epochs
- **ResNet-50**: ~8-10 hours for 100 epochs

### **Accuracy Progression**
- **Epoch 20**: ~40-50%
- **Epoch 50**: ~60-65%
- **Epoch 80**: ~68-71%
- **Epoch 100**: ~70-73% ✅ Target

### **Files Generated**
- `checkpoints/best_model.pth` - Best performing model
- `checkpoints/checkpoint_epoch_*.pth` - Periodic checkpoints
- `logs/training_*.log` - Detailed training logs
- `logs/training_curves_*.png` - Training visualization
- `logs/training_results.json` - Structured results

---

## 🛠️ **Common Commands**

### **Training Variations**

```bash
# Use ResNet-34 (better accuracy)
python train.py --model resnet34 --epochs 100

# Smaller batch size (if GPU memory limited)
python train.py --model resnet18 --epochs 100 --batch-size 64

# Resume from checkpoint
python train.py --resume checkpoints/checkpoint_epoch_50.pth --epochs 150

# Different learning rate schedule
python train.py --scheduler multistep --epochs 100
```

### **Testing Individual Components**

```bash
# Test model architecture
python resnet_model.py

# Test data loading
python data_utils.py

# Test utilities
python utils.py

# Test Gradio app (without trained model)
python app.py
```

---

## 📂 **Project Files Overview**

| File | Purpose |
|------|---------|
| `resnet_model.py` | ResNet-18/34/50 architectures |
| `data_utils.py` | Data loading & augmentation |
| `train.py` | Main training script |
| `utils.py` | Training utilities & visualization |
| `app.py` | HuggingFace Gradio application |
| `export_for_huggingface.py` | Deployment preparation |
| `requirements.txt` | Python dependencies |

---

## 🎯 **Assignment Checklist**

- [ ] Install dependencies
- [ ] Run quick test (1 epoch)
- [ ] Train full model (100 epochs)
- [ ] Achieve 73% accuracy
- [ ] Export for HuggingFace
- [ ] Test Gradio app locally
- [ ] Deploy to HuggingFace Spaces
- [ ] Share HuggingFace link

---

## 💡 **Pro Tips**

1. **Start training early** - 100 epochs takes ~4-6 hours
2. **Use GPU** - CPU training will be very slow
3. **Monitor logs** - Check `logs/` directory for progress
4. **Save checkpoints** - Every 10 epochs automatically saved
5. **Test locally first** - Run `python app.py` before deploying

---

## 🐛 **Quick Troubleshooting**

| Problem | Solution |
|---------|----------|
| Out of memory | Reduce `--batch-size` to 64 or 32 |
| Slow training | Check if using GPU, reduce `--num-workers` |
| Poor accuracy | Train longer or try ResNet-34/50 |
| Import errors | Run `pip install -r requirements.txt` again |

---

## 📞 **Need Help?**

Check the full README.md for:
- Detailed documentation
- Training pipeline explanation
- HuggingFace deployment guide
- Complete command reference

---

**Ready to achieve 73% accuracy! 🎯**

```bash
python train.py --model resnet18 --epochs 100 --batch-size 128
```

