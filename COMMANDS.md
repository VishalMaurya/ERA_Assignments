# ResNet CIFAR-100 Command Reference

Quick reference for all important commands.

## 🚀 **Quick Commands**

```bash
# Install and train in one go
pip install -r requirements.txt && python train.py --model resnet18 --epochs 100
```

---

## 📦 **Setup**

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python resnet_model.py
python data_utils.py
```

---

## 🏋️ **Training**

### **Basic Training**

```bash
# ResNet-18 (fastest, recommended for testing)
python train.py --model resnet18 --epochs 100 --batch-size 128

# ResNet-34 (balanced)
python train.py --model resnet34 --epochs 100 --batch-size 128

# ResNet-50 (best accuracy)
python train.py --model resnet50 --epochs 100 --batch-size 64
```

### **Advanced Training Options**

```bash
# Custom learning rate
python train.py --model resnet18 --epochs 100 --lr 0.05

# Different scheduler
python train.py --model resnet18 --epochs 100 --scheduler multistep

# Custom batch size
python train.py --model resnet18 --epochs 100 --batch-size 64

# More workers for data loading
python train.py --model resnet18 --epochs 100 --num-workers 8

# Save every 5 epochs
python train.py --model resnet18 --epochs 100 --save-freq 5
```

### **Resume Training**

```bash
# Resume from last checkpoint
python train.py --resume checkpoints/checkpoint_epoch_100.pth --epochs 150

# Resume and change settings
python train.py --resume checkpoints/checkpoint_epoch_50.pth --epochs 150 --lr 0.01
```

---

## 🧪 **Testing & Validation**

```bash
# Test model architecture
python resnet_model.py

# Test data loading
python data_utils.py

# Test utilities (creates sample plot)
python utils.py

# Quick training test (1 epoch)
python train.py --model resnet18 --epochs 1
```

---

## 🤗 **HuggingFace Deployment**

### **Export Model**

```bash
# Export best model
python export_for_huggingface.py

# Export specific checkpoint
python export_for_huggingface.py --checkpoint checkpoints/checkpoint_epoch_100.pth

# Export with custom output directory
python export_for_huggingface.py --output-dir my_custom_space

# Export ResNet-34 model
python export_for_huggingface.py --model resnet34 --checkpoint checkpoints/best_model.pth
```

### **Test Locally**

```bash
# Run Gradio app locally
python app.py

# Test with specific port
# (Modify app.py: iface.launch(server_port=7860))
python app.py
```

---

## 📊 **Monitoring**

### **View Training Logs**

```bash
# Follow training log in real-time
tail -f logs/training_*.log

# View all logs
cat logs/training_*.log

# Check results JSON
cat logs/training_results.json | python -m json.tool
```

### **Check Checkpoints**

```bash
# List checkpoints
ls -lh checkpoints/

# Check checkpoint details (requires Python)
python -c "import torch; print(torch.load('checkpoints/best_model.pth', map_location='cpu').keys())"
```

---

## 🔍 **Debugging**

### **Check GPU Availability**

```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}')"
```

### **Test Data Pipeline**

```bash
# Test data loading
python -c "from data_utils import get_cifar100_loaders; train_loader, test_loader, _ = get_cifar100_loaders(batch_size=4, num_workers=0); print('Data loading successful!')"
```

### **Check Model Parameters**

```bash
# Count parameters
python -c "from resnet_model import resnet18, get_model_info; model = resnet18(); info = get_model_info(model); print(f'Parameters: {info[\"total_parameters\"]:,}')"
```

---

## 📁 **File Operations**

### **Clean Up**

```bash
# Remove all checkpoints
rm -rf checkpoints/*

# Remove all logs
rm -rf logs/*

# Remove HuggingFace export
rm -rf huggingface_space/

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### **Backup**

```bash
# Backup checkpoints
cp -r checkpoints/ checkpoints_backup/

# Backup logs
cp -r logs/ logs_backup/

# Create compressed backup
tar -czf resnet_cifar100_backup_$(date +%Y%m%d).tar.gz checkpoints/ logs/
```

---

## 🎯 **Complete Workflow**

### **From Scratch to Deployment**

```bash
# 1. Setup
pip install -r requirements.txt

# 2. Quick test
python train.py --model resnet18 --epochs 1

# 3. Full training
python train.py --model resnet18 --epochs 100 --batch-size 128

# 4. Check results
cat logs/training_results.json

# 5. Export for HuggingFace
python export_for_huggingface.py

# 6. Test locally
python app.py

# 7. Deploy to HuggingFace Spaces
# (Upload huggingface_space/ directory)
```

---

## 💡 **Useful Combinations**

### **Fast Prototyping**

```bash
# Quick test with small model
python train.py --model resnet18 --epochs 10 --batch-size 64
```

### **Production Training**

```bash
# Full training with all optimizations
python train.py --model resnet34 --epochs 150 --batch-size 128 --num-workers 8
```

### **Memory Constrained**

```bash
# Smaller batch size
python train.py --model resnet18 --epochs 100 --batch-size 32 --num-workers 2
```

### **Continue Training**

```bash
# Resume and train more
python train.py --resume checkpoints/checkpoint_epoch_100.pth --epochs 150
```

---

## 📊 **Monitoring & Analysis**

### **Live Monitoring**

```bash
# Watch training progress (in another terminal)
watch -n 1 "tail -n 20 logs/training_*.log"

# Monitor GPU usage
watch -n 1 nvidia-smi
```

### **Post-Training Analysis**

```bash
# View training curves
open logs/training_curves_*.png

# Check final accuracy
python -c "import json; data = json.load(open('logs/training_results.json')); print(f\"Best Accuracy: {data['best_accuracy']:.2f}%\")"
```

---

## 🔧 **Troubleshooting Commands**

### **Fix Common Issues**

```bash
# Out of memory - reduce batch size
python train.py --model resnet18 --epochs 100 --batch-size 32

# Slow data loading - adjust workers
python train.py --model resnet18 --epochs 100 --num-workers 0

# Check data directory
ls -lh data/cifar-100-python/

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 🎓 **Learning & Experimentation**

### **Compare Models**

```bash
# Train all three models (sequential)
python train.py --model resnet18 --epochs 50
python train.py --model resnet34 --epochs 50
python train.py --model resnet50 --epochs 50 --batch-size 64
```

### **Experiment with Hyperparameters**

```bash
# Different learning rates
python train.py --model resnet18 --epochs 50 --lr 0.05
python train.py --model resnet18 --epochs 50 --lr 0.01

# Different schedulers
python train.py --model resnet18 --epochs 50 --scheduler step
python train.py --model resnet18 --epochs 50 --scheduler multistep
```

---

## 📝 **Documentation Commands**

```bash
# View README
cat README.md

# View quick start
cat QUICKSTART.md

# View implementation summary
cat IMPLEMENTATION_SUMMARY.md

# View this file
cat COMMANDS.md
```

---

## 🎯 **Assignment Submission**

```bash
# 1. Verify model is trained
ls -lh checkpoints/best_model.pth

# 2. Check accuracy achieved
cat logs/training_results.json | grep best_accuracy

# 3. Prepare for deployment
python export_for_huggingface.py

# 4. Verify export
ls -lh huggingface_space/

# 5. Test app
python app.py

# 6. Create submission package
tar -czf s8_resnet_submission.tar.gz checkpoints/ logs/ huggingface_space/ *.py *.md requirements.txt
```

---

**Quick Reference Complete! Use these commands to train and deploy your ResNet CIFAR-100 model. 🚀**

