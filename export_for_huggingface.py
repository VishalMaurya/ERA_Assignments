"""
Export Model for HuggingFace Deployment
======================================

Script to prepare model and files for HuggingFace Spaces deployment.
"""

import torch
import json
import os
import shutil
from resnet_model import resnet18, resnet34, resnet50


# CIFAR-100 class names
CIFAR100_CLASSES = [
    'apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle',
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
    'turtle', 'wardrobe', 'whale', 'willow_tree', 'wolf', 'woman', 'worm'
]


def export_for_huggingface(
    checkpoint_path='checkpoints/best_model.pth',
    model_name='resnet18',
    output_dir='huggingface_space',
    copy_app=True
):
    """
    Export model and necessary files for HuggingFace Spaces
    
    Args:
        checkpoint_path: Path to trained model checkpoint
        model_name: Model architecture name
        output_dir: Directory to export files
        copy_app: Whether to copy app.py and requirements
    """
    print(f"🚀 Exporting model for HuggingFace Spaces...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load checkpoint
    print(f"📦 Loading checkpoint from {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    # Save model state dict only (smaller file)
    model_save_path = os.path.join(output_dir, 'best_model.pth')
    if 'model_state_dict' in checkpoint:
        torch.save(checkpoint['model_state_dict'], model_save_path)
        print(f"💾 Model state dict saved to {model_save_path}")
        
        # Save model info
        model_info = {
            'model_name': model_name,
            'epoch': checkpoint.get('epoch', 'unknown'),
            'accuracy': float(checkpoint.get('accuracy', 0)),
            'best_accuracy': float(checkpoint.get('best_accuracy', 0))
        }
    else:
        torch.save(checkpoint, model_save_path)
        print(f"💾 Model saved to {model_save_path}")
        model_info = {'model_name': model_name}
    
    # Save class names
    class_names_path = os.path.join(output_dir, 'class_names.json')
    with open(class_names_path, 'w') as f:
        json.dump(CIFAR100_CLASSES, f, indent=2)
    print(f"📝 Class names saved to {class_names_path}")
    
    # Save model info
    model_info_path = os.path.join(output_dir, 'model_info.json')
    with open(model_info_path, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"📊 Model info saved to {model_info_path}")
    
    # Copy necessary files
    if copy_app:
        files_to_copy = [
            ('app.py', 'app.py'),
            ('resnet_model.py', 'resnet_model.py'),
        ]
        
        for src, dst in files_to_copy:
            if os.path.exists(src):
                dst_path = os.path.join(output_dir, dst)
                shutil.copy(src, dst_path)
                print(f"📄 Copied {src} to {dst_path}")
        
        # Create requirements.txt for HuggingFace
        requirements = [
            "torch",
            "torchvision",
            "gradio",
            "Pillow",
            "numpy"
        ]
        
        req_path = os.path.join(output_dir, 'requirements.txt')
        with open(req_path, 'w') as f:
            f.write('\n'.join(requirements))
        print(f"📦 Requirements saved to {req_path}")
    
    # Create README for HuggingFace
    readme_content = f"""---
title: ResNet CIFAR-100 Classifier
emoji: 🖼️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 3.50.0
app_file: app.py
pinned: false
---

# ResNet CIFAR-100 Image Classifier

This Space hosts a ResNet model trained from scratch on the CIFAR-100 dataset.

## Model Information
- **Architecture**: {model_name.upper()}
- **Dataset**: CIFAR-100 (100 classes)
- **Training**: From scratch (no pre-trained weights)
- **Accuracy**: {model_info.get('best_accuracy', 'N/A'):.2f}%

## How to Use
1. Upload an image or select an example
2. The model will predict the top-5 most likely categories
3. Confidence scores show how certain the model is

## Categories
The model can classify images into 100 different categories including:
- Animals (mammals, fish, reptiles, insects)
- Vehicles (cars, trains, planes)
- Household items (furniture, appliances)
- Natural scenes (forests, mountains, seas)
- And many more!

## About ResNet
ResNet (Residual Network) is a deep learning architecture that uses skip connections 
to enable training of very deep networks. This implementation is optimized for 
CIFAR-100's 32×32 pixel images.

---
Built with ❤️ for ERA V4 Assignment
"""
    
    readme_path = os.path.join(output_dir, 'README.md')
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print(f"📖 README saved to {readme_path}")
    
    print(f"\n✅ Export complete!")
    print(f"📁 All files saved to: {output_dir}")
    print(f"\n🚀 To deploy on HuggingFace Spaces:")
    print(f"1. Create a new Space on HuggingFace (https://huggingface.co/spaces)")
    print(f"2. Choose 'Gradio' as the SDK")
    print(f"3. Upload all files from '{output_dir}' directory")
    print(f"4. Your app will be live in a few minutes!")
    
    return output_dir


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Export model for HuggingFace')
    parser.add_argument('--checkpoint', type=str, default='checkpoints/best_model.pth',
                       help='Path to model checkpoint')
    parser.add_argument('--model', type=str, default='resnet18',
                       choices=['resnet18', 'resnet34', 'resnet50'],
                       help='Model architecture')
    parser.add_argument('--output-dir', type=str, default='huggingface_space',
                       help='Output directory')
    
    args = parser.parse_args()
    
    export_for_huggingface(
        checkpoint_path=args.checkpoint,
        model_name=args.model,
        output_dir=args.output_dir
    )

