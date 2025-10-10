# S8 Assignment - ResNet CIFAR-100 from Scratch

## 🎯 **Assignment Objectives**

Train ResNet model from scratch on CIFAR-100 dataset:
- **Target**: 73% top-1 accuracy
- **Training**: ~100 epochs
- **Constraint**: No pre-trained models
- **Deployment**: HuggingFace Spaces

## 📋 **Assignment Status**

- **Branch**: `s8-resnet`
- **Status**: ✅ **IMPLEMENTATION COMPLETE** - Ready to train!
- **Previous Assignment**: S7 Advanced NN CIFAR-10 (84.29% accuracy)

## 🚀 **Quick Start**

### **Installation**

```bash
pip install -r requirements.txt
```

### **Training**

```bash
# Train ResNet-18 (Recommended for quick training)
python train.py --model resnet18 --epochs 100 --batch-size 128

# Train ResNet-34 (More capacity)
python train.py --model resnet34 --epochs 100 --batch-size 128

# Train ResNet-50 (Best performance, longer training)
python train.py --model resnet50 --epochs 100 --batch-size 64

# Resume from checkpoint
python train.py --model resnet18 --epochs 150 --resume checkpoints/checkpoint_epoch_100.pth
```

### **Export for HuggingFace**

```bash
python export_for_huggingface.py --checkpoint checkpoints/best_model.pth --model resnet18
```

### **Local Gradio App Testing**

```bash
python app.py
```

## 📁 **Project Structure**

```
Session2_Assignment/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── S8_RESNET_ASSIGNMENT.md           # Assignment details
│
├── resnet_model.py                    # ResNet architectures (18/34/50)
├── data_utils.py                      # Data loading & augmentation
├── utils.py                           # Training utilities
├── train.py                           # Main training script
│
├── app.py                             # HuggingFace Gradio app
├── export_for_huggingface.py         # Export script for deployment
│
├── resnet_cifar100.ipynb             # Jupyter notebook (optional)
│
├── checkpoints/                       # Saved model checkpoints
│   ├── best_model.pth
│   └── checkpoint_epoch_*.pth
│
├── logs/                              # Training logs and plots
│   ├── training_*.log
│   ├── training_curves_*.png
│   └── training_results.json
│
└── huggingface_space/                # HuggingFace deployment files
    ├── app.py
    ├── resnet_model.py
    ├── best_model.pth
    ├── class_names.json
    ├── model_info.json
    ├── requirements.txt
    └── README.md
```

## 🏗️ **Implementation Details**

### **Models Implemented**

| Model | Layers | Parameters | Best For |
|-------|--------|------------|----------|
| **ResNet-18** | 18 | ~11.2M | Quick training, good baseline |
| **ResNet-34** | 34 | ~21.3M | Balance of speed and accuracy |
| **ResNet-50** | 50 | ~23.5M | Best performance, slower training |

### **Data Augmentation**

Albumentations pipeline for CIFAR-100:
- Horizontal flip (p=0.5)
- ShiftScaleRotate (shift=10%, scale=15%, rotate=15°)
- CoarseDropout (1 hole, 16×16 pixels)
- RandomBrightnessContrast
- HueSaturationValue
- Normalization

### **Training Configuration**

- **Optimizer**: SGD with Nesterov momentum (0.9)
- **Initial LR**: 0.1
- **Scheduler**: CosineAnnealingWarmRestarts (T_0=10, T_mult=2)
- **Weight Decay**: 5e-4
- **Label Smoothing**: 0.1
- **Batch Size**: 128 (ResNet-18/34), 64 (ResNet-50)

### **Key Features**

✅ **Modular Design**: Separate files for model, data, training, utilities  
✅ **Comprehensive Logging**: Detailed logs and JSON results  
✅ **Checkpoint Management**: Save best, periodic, and target checkpoints  
✅ **Visualization**: Automatic training curve plots  
✅ **Resume Training**: Continue from any checkpoint  
✅ **HuggingFace Ready**: One-command export for deployment  
✅ **Gradio App**: Interactive web interface included  

## 🎨 **CIFAR-100 Dataset**

- **Classes**: 100 fine-grained categories
- **Training**: 50,000 images (500 per class)
- **Testing**: 10,000 images (100 per class)
- **Image Size**: 32×32×3 RGB
- **Superclasses**: 20 coarse categories

### **Category Examples**

- **Animals**: bear, leopard, lion, tiger, wolf, elephant, camel, fox, etc.
- **Vehicles**: bicycle, bus, motorcycle, train, rocket, tank, etc.
- **Nature**: forest, mountain, sea, cloud, trees, flowers, etc.
- **Objects**: furniture, appliances, containers, tools, etc.

## 📊 **Training Pipeline**

1. **Data Loading**: CIFAR-100 with Albumentations augmentation
2. **Model Creation**: ResNet-18/34/50 optimized for 32×32 images
3. **Training Loop**: 
   - Batch training with progress bars
   - Validation after each epoch
   - Learning rate scheduling
   - Checkpoint saving (best/periodic)
4. **Result Logging**: JSON, plots, and detailed logs
5. **Export**: Prepare for HuggingFace deployment

## 🚀 **HuggingFace Deployment Guide**

### **Step 1: Train Model**

```bash
python train.py --model resnet18 --epochs 100
```

### **Step 2: Export Files**

```bash
python export_for_huggingface.py
```

This creates `huggingface_space/` directory with:
- `app.py` - Gradio application
- `resnet_model.py` - Model architecture
- `best_model.pth` - Trained weights
- `class_names.json` - CIFAR-100 classes
- `requirements.txt` - Dependencies
- `README.md` - Space documentation

### **Step 3: Deploy to HuggingFace**

1. Go to [HuggingFace Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose "Gradio" as SDK
4. Upload all files from `huggingface_space/`
5. Space will build and deploy automatically!

## 📈 **Expected Results**

### **Training Progress**

- **Epoch 1-20**: ~30-45% accuracy (learning basic features)
- **Epoch 20-50**: ~50-65% accuracy (learning complex patterns)
- **Epoch 50-80**: ~65-72% accuracy (fine-tuning)
- **Epoch 80-100**: ~70-73% accuracy (convergence)

### **Target Achievement**

- **ResNet-18**: Expected 70-72% (may need 120 epochs for 73%)
- **ResNet-34**: Expected 71-73% (~100 epochs)
- **ResNet-50**: Expected 72-74% (~100 epochs)

## 🛠️ **Command Reference**

### **Training Commands**

```bash
# Basic training
python train.py --model resnet18 --epochs 100

# With custom settings
python train.py --model resnet34 --epochs 150 --batch-size 128 --lr 0.1

# Resume training
python train.py --resume checkpoints/checkpoint_epoch_100.pth --epochs 150

# Different scheduler
python train.py --model resnet18 --scheduler multistep --epochs 100
```

### **Export Commands**

```bash
# Export best model
python export_for_huggingface.py

# Export specific checkpoint
python export_for_huggingface.py --checkpoint checkpoints/checkpoint_epoch_100.pth

# Export with custom output directory
python export_for_huggingface.py --output-dir my_space
```

### **Testing Commands**

```bash
# Test model architecture
python resnet_model.py

# Test data loading
python data_utils.py

# Test utilities (creates sample plot)
python utils.py

# Run local Gradio app
python app.py
```

## 📚 **Key Concepts**

### **ResNet Architecture**

- **Residual Connections**: Skip connections that add input to output
- **Identity Mapping**: Allows gradients to flow without degradation
- **Bottleneck Blocks**: 1×1 → 3×3 → 1×1 convolutions (ResNet-50)
- **Basic Blocks**: Two 3×3 convolutions (ResNet-18/34)

### **Why ResNet for CIFAR-100?**

- **Deep Architecture**: Can learn complex features for 100 classes
- **Gradient Flow**: Skip connections prevent vanishing gradients
- **Proven Performance**: ResNet has excellent track record on CIFAR
- **Scalable**: Easy to adjust depth for performance vs speed

## 🎓 **References**

1. [Deep Residual Learning for Image Recognition (He et al., 2015)](https://arxiv.org/abs/1512.03385)
2. [Identity Mappings in Deep Residual Networks (He et al., 2016)](https://arxiv.org/abs/1603.05027)
3. [CIFAR-100 Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)

## 🏆 **Assignment Checklist**

- [x] **ResNet Implementation**: ResNet-18/34/50 architectures
- [x] **CIFAR-100 Training**: Complete training pipeline
- [ ] **73% Accuracy**: Target to be achieved during training
- [x] **HuggingFace App**: Gradio application ready
- [x] **Deployment Ready**: Export script for HuggingFace Spaces
- [x] **Documentation**: Comprehensive README and comments
- [x] **No Pre-training**: Training from scratch only

## 💡 **Tips for Success**

1. **Start with ResNet-18**: Faster training for experimentation
2. **Monitor Overfitting**: Watch train vs test accuracy gap
3. **Adjust Learning Rate**: If not converging, try different schedulers
4. **Data Augmentation**: Already optimized, but can experiment
5. **Batch Size**: Larger is better if GPU memory allows
6. **Training Time**: Be patient, 100 epochs may take 4-6 hours on GPU

## 🐛 **Troubleshooting**

- **Out of Memory**: Reduce batch size with `--batch-size 64`
- **Slow Training**: Use GPU, check `--num-workers` setting
- **Poor Accuracy**: Train longer or try ResNet-34/50
- **Checkpoint Errors**: Ensure model name matches checkpoint

---

## 🎯 **Ready to Train!**

Everything is set up and ready. Start training with:

```bash
python train.py --model resnet18 --epochs 100 --batch-size 128
```

Good luck reaching 73% accuracy! 🚀

---

**Built with ❤️ for ERA V4 Session 8 Assignment**
