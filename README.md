# S8 Assignment - ResNet Implementation

## 🎯 **Project Overview**

This repository contains the implementation of ResNet (Residual Networks) architecture for the ERA V4 Session 8 assignment.

## 📋 **Assignment Status**

- **Branch**: `s8-resnet`
- **Status**: Ready to begin implementation
- **Previous Assignment**: S7 Advanced NN CIFAR-10 (Completed - 84.29% accuracy achieved)

## 🚀 **Getting Started**

### **Prerequisites**

```bash
pip install -r requirements.txt
```

### **Key Technologies**
- PyTorch
- torchvision
- Albumentations (for data augmentation)
- NumPy

## 🏗️ **ResNet Architecture Concepts**

ResNet (Residual Networks) introduces the concept of skip connections to enable training of very deep neural networks:

### **Key Features:**
- **Residual Blocks**: Skip connections that allow gradients to flow directly through the network
- **Identity Mapping**: Shortcut connections that perform identity mapping
- **Bottleneck Design**: Efficient block design using 1x1, 3x3, 1x1 convolutions
- **Batch Normalization**: Applied after every convolutional layer
- **No Dropout**: ResNets typically don't use dropout in residual blocks

## 📚 **Learning Resources**

### **Key Papers**
1. [Deep Residual Learning for Image Recognition (He et al., 2015)](https://arxiv.org/abs/1512.03385)
2. [Identity Mappings in Deep Residual Networks (He et al., 2016)](https://arxiv.org/abs/1603.05027)

### **ResNet Variants**
- **ResNet-18**: 18 layers, 11.7M parameters
- **ResNet-34**: 34 layers, 21.8M parameters
- **ResNet-50**: 50 layers with bottleneck blocks, 25.6M parameters
- **ResNet-101**: 101 layers, 44.5M parameters
- **ResNet-152**: 152 layers, 60.2M parameters

## 📁 **Project Structure**

```
Session2_Assignment/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── S8_RESNET_ASSIGNMENT.md       # Assignment details
└── (Implementation files to be added)
```

## 🎓 **Previous Assignments**

### **S7 Advanced NN CIFAR-10** ✅ Completed
- Three compliant CIFAR-10 models implemented
- Enhanced model achieved **84.29% accuracy**
- All requirements met: C1-C2-C3-C4-O, RF>44, DW-Sep, Dilated, GAP
- Comprehensive augmentation pipeline with Albumentations

## 📝 **Assignment Requirements**

*Requirements will be added once assignment details are provided*

## 🚀 **Usage**

*Usage instructions will be added as implementation progresses*

## 📊 **Results**

*Training results and model performance will be documented here*

## 🤝 **Contributing**

This is an educational project for ERA V4 coursework.

## 📄 **License**

Educational use only - ERA V4 Assignment

---

**Ready for S8 ResNet Implementation! 🚀**

*Let's build powerful residual networks!*
