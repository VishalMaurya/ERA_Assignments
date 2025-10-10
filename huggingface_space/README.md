---
title: ResNet-34 CIFAR-100 Classifier
emoji: 🖼️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 3.50.0
app_file: app.py
pinned: false
---

# ResNet-34 CIFAR-100 Image Classifier

This Space hosts a ResNet-34 model trained from scratch on the CIFAR-100 dataset.

## 🏆 Model Performance

- **Architecture**: ResNet-34 (21.3M parameters)
- **Dataset**: CIFAR-100 (100 classes)
- **Training**: From scratch (no pre-trained weights)
- **Best Accuracy**: **76.25%** (Epoch 69)
- **Target**: 73% ✅ **EXCEEDED by +3.25%**
- **Training Time**: 1.11 hours on Tesla T4
- **GPU Optimizations**: Mixed Precision (FP16), cuDNN Benchmark

## 🎯 Assignment Success

This model was trained as part of the ERA V4 Session 8 assignment:
- ✅ Trained ResNet from scratch
- ✅ Achieved 73% target accuracy
- ✅ Exceeded target by 3.25%
- ✅ Fast training with GPU optimizations
- ✅ Deployed to HuggingFace Spaces

## 🚀 How to Use

1. Upload an image or select an example
2. The model will predict the top-5 most likely categories
3. Confidence scores show how certain the model is

**Best results with**: Small objects, centered composition, similar to CIFAR-100 style

## 📊 Training Details

### Optimization Techniques
- **Mixed Precision (FP16)**: 3x faster training, 70% less memory
- **cuDNN Benchmark**: Automatic algorithm selection
- **Cosine Annealing**: Learning rate scheduling with warm restarts
- **Label Smoothing**: 0.1 for better generalization
- **Data Augmentation**: HorizontalFlip, ShiftScaleRotate, CoarseDropout, ColorJitter

### Training Progression
- **Epoch 1**: 10.19% accuracy
- **Epoch 29**: 73.66% ✅ Target reached!
- **Epoch 69**: 76.25% 🏆 Peak performance!
- **Time to target**: 33 minutes

## 🎨 CIFAR-100 Categories

The model can classify images into 100 different categories organized into 20 superclasses:

### Animals
- **Aquatic mammals**: beaver, dolphin, otter, seal, whale
- **Fish**: aquarium_fish, flatfish, ray, shark, trout
- **Large carnivores**: bear, leopard, lion, tiger, wolf
- **Large omnivores/herbivores**: camel, cattle, chimpanzee, elephant, kangaroo
- **Medium mammals**: fox, porcupine, possum, raccoon, skunk
- **Small mammals**: hamster, mouse, rabbit, shrew, squirrel
- **Reptiles**: crocodile, dinosaur, lizard, snake, turtle
- **Insects**: bee, beetle, butterfly, caterpillar, cockroach
- **Non-insect invertebrates**: crab, lobster, snail, spider, worm

### Plants
- **Flowers**: orchid, poppy, rose, sunflower, tulip
- **Trees**: maple, oak, palm, pine, willow
- **Fruit and vegetables**: apple, mushroom, orange, pear, sweet_pepper

### Objects
- **Food containers**: bottle, bowl, can, cup, plate
- **Household electrical**: clock, keyboard, lamp, telephone, television
- **Household furniture**: bed, chair, couch, table, wardrobe

### Vehicles
- **Vehicles 1**: bicycle, bus, motorcycle, pickup_truck, train
- **Vehicles 2**: lawn_mower, rocket, streetcar, tank, tractor

### Scenes
- **Large outdoor things**: bridge, castle, house, road, skyscraper
- **Natural scenes**: cloud, forest, mountain, plain, sea

### People
- **People**: baby, boy, girl, man, woman

## 🔬 Technical Architecture

### ResNet-34 Structure
```
Input (32×32×3)
├── Conv1: 3→64, 3×3, stride=1
├── Layer1: [64→64] × 3 blocks
├── Layer2: [64→128] × 4 blocks, stride=2
├── Layer3: [128→256] × 6 blocks, stride=2
├── Layer4: [256→512] × 3 blocks, stride=2
├── GlobalAvgPool → 512
└── FC → 100 classes

Total Parameters: 21,328,292
Trainable Parameters: 21,328,292
```

### Key Features
- **Residual Connections**: Skip connections for deep network training
- **Batch Normalization**: After every convolution
- **ReLU Activation**: Efficient non-linearity
- **Global Average Pooling**: Parameter-efficient classification
- **No Dropout**: ResNet's skip connections provide regularization

## 📈 Performance Analysis

### Strengths
- ✅ Exceeded target by 3.25%
- ✅ Fast convergence (target in 33 minutes)
- ✅ Consistent performance across epochs
- ✅ Well-optimized GPU utilization

### Characteristics
- Training Accuracy: 97.97% (Epoch 69)
- Test Accuracy: 76.25% (Epoch 69)
- Some overfitting observed (normal for deep networks)
- Peak performance early (epoch 69 of 100)

## 💡 Usage Tips

### Best Results
- Use images with **centered objects**
- **32×32 resolution** works best
- Clear, uncluttered backgrounds
- Good lighting conditions

### Category Examples
- **Animals**: Natural poses, clear visibility
- **Vehicles**: Side or front views
- **Household items**: Clear product shots
- **Natural scenes**: Landscape compositions

## 🛠️ Technical Stack

- **Framework**: PyTorch 2.0+
- **UI**: Gradio 3.50+
- **Training**: Tesla T4 GPU with Mixed Precision
- **Optimization**: cuDNN Benchmark, Gradient Accumulation
- **Preprocessing**: Albumentations library

## 📚 Model Files

This Space includes:
- `best_model.pth`: Trained model weights (163 MB)
- `app.py`: Gradio application
- `resnet_model.py`: ResNet-34 architecture
- `class_names.json`: 100 CIFAR-100 categories
- `model_info.json`: Training metadata

## 🎓 About ResNet

ResNet (Residual Network) won 1st place in ILSVRC 2015 classification competition. Key innovation: skip connections that allow training of very deep networks by addressing the vanishing gradient problem.

**Paper**: [Deep Residual Learning for Image Recognition (He et al., 2015)](https://arxiv.org/abs/1512.03385)

## 🤝 Acknowledgments

- **Dataset**: CIFAR-100 (Krizhevsky & Hinton)
- **Architecture**: ResNet (He et al., 2015)
- **Training**: ERA V4 Session 8 Assignment
- **GPU**: Tesla T4 (Google Colab / Kaggle)

## 📞 Support

For questions or issues:
- Check training logs for performance details
- Review model_info.json for specifications
- Refer to CIFAR-100 documentation for categories

---

**Built with ❤️ for ERA V4 Session 8 Assignment**  
**Training completed successfully in 1.11 hours! ⚡**  
**Target exceeded: 76.25% accuracy! 🏆**

