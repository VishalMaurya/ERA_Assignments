"""
HuggingFace Gradio App for ResNet CIFAR-100
==========================================

Deploy trained ResNet model for CIFAR-100 classification.

To deploy on HuggingFace Spaces:
1. Create a new Space on HuggingFace
2. Upload this app.py, resnet_model.py, and model checkpoint
3. Add requirements.txt with: torch, gradio, Pillow, numpy
"""

import gradio as gr
import torch
import torch.nn.functional as F
from PIL import Image
import numpy as np
import json

from resnet_model import resnet18, resnet34, resnet50


# CIFAR-100 statistics
CIFAR100_MEAN = (0.5071, 0.4867, 0.4408)
CIFAR100_STD = (0.2675, 0.2565, 0.2761)

# Load class names
try:
    with open('class_names.json', 'r') as f:
        CLASS_NAMES = json.load(f)
except:
    # Default CIFAR-100 class names
    CLASS_NAMES = ['apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle',
                   'bicycle', 'bottle', 'bowl', 'boy', 'bridge', 'bus', 'butterfly', 'camel',
                   'can', 'castle', 'caterpillar', 'cattle', 'chair', 'chimpanzee', 'clock',
                   'cloud', 'cockroach', 'couch', 'crab', 'crocodile', 'cup', 'dinosaur',
                   'dolphin', 'elephant', 'flatfish', 'forest', 'fox', 'girl', 'hamster',
                   'house', 'kangaroo', 'keyboard', 'lamp', 'lawn_mower', 'leopard', 'lion',
                   'lizard', 'lobster', 'man', 'maple_tree', 'motorcycle', 'mountain', 'mouse',
                   'mushroom', 'oak_tree', 'orange', 'orchid', 'otter', 'palm_tree', 'pear',
                   'pickup_truck', 'pine_tree', 'plain', 'plate', 'poppy', 'porcupine',
                   'possum', 'rabbit', 'raccoon', 'ray', 'road', 'rocket', 'rose', 'sea',
                   'seal', 'shark', 'shrew', 'skunk', 'skyscraper', 'snail', 'snake', 'spider',
                   'squirrel', 'streetcar', 'sunflower', 'sweet_pepper', 'table', 'tank',
                   'telephone', 'television', 'tiger', 'tractor', 'train', 'trout', 'tulip',
                   'turtle', 'wardrobe', 'whale', 'willow_tree', 'wolf', 'woman', 'worm']


def load_model(model_path='best_model.pth', model_name='resnet18'):
    """Load trained ResNet model"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Create model
    if model_name == 'resnet18':
        model = resnet18(num_classes=100)
    elif model_name == 'resnet34':
        model = resnet34(num_classes=100)
    elif model_name == 'resnet50':
        model = resnet50(num_classes=100)
    
    # Load checkpoint
    try:
        checkpoint = torch.load(model_path, map_location=device)
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        print(f"✅ Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"⚠️ Warning: Could not load model checkpoint: {e}")
        print("Using randomly initialized model")
    
    model = model.to(device)
    model.eval()
    
    return model, device


def preprocess_image(image):
    """Preprocess image for model input"""
    # Resize to 32x32
    image = image.resize((32, 32))
    
    # Convert to numpy array
    image = np.array(image).astype(np.float32) / 255.0
    
    # Normalize
    image = (image - np.array(CIFAR100_MEAN)) / np.array(CIFAR100_STD)
    
    # Convert to tensor
    image = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0)
    
    return image


def predict(image, top_k=5):
    """
    Predict class probabilities for input image
    
    Args:
        image: PIL Image
        top_k: Number of top predictions to return
    
    Returns:
        Dictionary of class names and probabilities
    """
    # Preprocess
    image_tensor = preprocess_image(image).to(device)
    
    # Predict
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = F.softmax(outputs, dim=1)
    
    # Get top-k predictions
    probs, indices = torch.topk(probabilities[0], top_k)
    
    # Create results dictionary
    results = {
        CLASS_NAMES[idx]: float(prob) 
        for idx, prob in zip(indices, probs)
    }
    
    return results


# Load model (global variable)
model, device = load_model()

# Create Gradio interface
title = "🖼️ ResNet CIFAR-100 Image Classifier"
description = """
**Classify images into 100 different categories using ResNet trained from scratch!**

This model was trained on the CIFAR-100 dataset and can recognize 100 different object categories.
Upload an image or try one of the examples below.

**Categories include**: animals, vehicles, household items, natural scenes, and more!

**Note**: Best results with images similar to CIFAR-100 style (small, centered objects).
"""

article = """
### 📊 Model Information
- **Architecture**: ResNet (Residual Networks)
- **Dataset**: CIFAR-100 (100 classes)
- **Training**: From scratch (no pre-trained weights)
- **Target Accuracy**: 73% top-1 accuracy
- **Image Size**: 32×32 pixels

### 🏆 CIFAR-100 Categories
The model can classify images into 100 fine-grained categories organized into 20 superclasses:
- **Aquatic mammals**: beaver, dolphin, otter, seal, whale
- **Fish**: aquarium fish, flatfish, ray, shark, trout
- **Flowers**: orchid, poppy, rose, sunflower, tulip
- **Food containers**: bottle, bowl, can, cup, plate
- **Fruit and vegetables**: apple, mushroom, orange, pear, sweet pepper
- **Household electrical devices**: clock, keyboard, lamp, telephone, television
- **Household furniture**: bed, chair, couch, table, wardrobe
- **Insects**: bee, beetle, butterfly, caterpillar, cockroach
- **Large carnivores**: bear, leopard, lion, tiger, wolf
- **Large man-made outdoor things**: bridge, castle, house, road, skyscraper
- **Large natural outdoor scenes**: cloud, forest, mountain, plain, sea
- **Large omnivores and herbivores**: camel, cattle, chimpanzee, elephant, kangaroo
- **Medium-sized mammals**: fox, porcupine, possum, raccoon, skunk
- **Non-insect invertebrates**: crab, lobster, snail, spider, worm
- **People**: baby, boy, girl, man, woman
- **Reptiles**: crocodile, dinosaur, lizard, snake, turtle
- **Small mammals**: hamster, mouse, rabbit, shrew, squirrel
- **Trees**: maple, oak, palm, pine, willow
- **Vehicles 1**: bicycle, bus, motorcycle, pickup truck, train
- **Vehicles 2**: lawn mower, rocket, streetcar, tank, tractor

### 🚀 How to Use
1. Upload an image or select an example
2. The model will predict the top-5 most likely categories
3. Confidence scores show how certain the model is

### 📚 About ResNet
ResNet (Residual Network) uses skip connections to enable training of very deep networks.
This architecture won 1st place in the ILSVRC 2015 classification competition.

---
**Built with ❤️ for ERA V4 Assignment**
"""

# Example images (you can add your own)
examples = []

# Create interface
iface = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil", label="Upload Image"),
    outputs=gr.Label(num_top_classes=5, label="Predictions"),
    title=title,
    description=description,
    article=article,
    examples=examples,
    theme="default",
    allow_flagging="never",
    examples_per_page=10
)

# Launch app
if __name__ == "__main__":
    iface.launch(share=False)

