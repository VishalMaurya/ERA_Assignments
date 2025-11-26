"""
Reduce model file size for deployment
Keep only model weights, remove optimizer and training logs
Convert to float16 for smaller file size
"""

import torch
import os

print("="*80)
print("Reducing Model Size for HuggingFace Deployment")
print("="*80)

# Load the checkpoint
print("\n📂 Loading checkpoint...")
checkpoint = torch.load('shakespeare_gpt2_final.pt', map_location='cpu')

print(f"✅ Loaded checkpoint")
print(f"   Keys in checkpoint: {list(checkpoint.keys())}")

# Get original size
original_size = os.path.getsize('shakespeare_gpt2_final.pt')
print(f"\n📊 Original file size: {original_size / (1024**3):.2f} GB ({original_size / (1024**2):.0f} MB)")

# Create minimal checkpoint (only what's needed for inference)
minimal_checkpoint = {
    'model_state_dict': checkpoint['model_state_dict'],
    'config': checkpoint['config'],
    'step': checkpoint.get('step', 10000),
    'loss': checkpoint.get('loss', 4.631),
}

print(f"\n🔧 Creating minimal checkpoint...")
print(f"   Keeping: model_state_dict, config, step, loss")
print(f"   Removing: optimizer_state_dict, training_log")

# Save minimal checkpoint
print(f"\n💾 Saving minimal checkpoint...")
torch.save(minimal_checkpoint, 'shakespeare_gpt2_minimal.pt')

minimal_size = os.path.getsize('shakespeare_gpt2_minimal.pt')
print(f"✅ Minimal checkpoint saved: shakespeare_gpt2_minimal.pt")
print(f"   New file size: {minimal_size / (1024**3):.2f} GB ({minimal_size / (1024**2):.0f} MB)")

# Calculate reduction
reduction = ((original_size - minimal_size) / original_size) * 100
print(f"\n📉 Size reduction: {reduction:.1f}%")
print(f"   Reduced by: {(original_size - minimal_size) / (1024**2):.0f} MB")

# Optional: Convert to float16 for even smaller size
print(f"\n🎯 Creating float16 version (for even smaller size)...")

# Load model weights and convert to float16
model_state = checkpoint['model_state_dict']
model_state_fp16 = {}

for key, value in model_state.items():
    if value.dtype == torch.float32:
        model_state_fp16[key] = value.half()  # Convert to float16
    else:
        model_state_fp16[key] = value

minimal_checkpoint_fp16 = {
    'model_state_dict': model_state_fp16,
    'config': checkpoint['config'],
    'step': checkpoint.get('step', 10000),
    'loss': checkpoint.get('loss', 4.631),
}

torch.save(minimal_checkpoint_fp16, 'shakespeare_gpt2_fp16.pt')

fp16_size = os.path.getsize('shakespeare_gpt2_fp16.pt')
print(f"✅ Float16 checkpoint saved: shakespeare_gpt2_fp16.pt")
print(f"   File size: {fp16_size / (1024**3):.2f} GB ({fp16_size / (1024**2):.0f} MB)")

fp16_reduction = ((original_size - fp16_size) / original_size) * 100
print(f"\n📉 Float16 size reduction: {fp16_reduction:.1f}%")
print(f"   Reduced by: {(original_size - fp16_size) / (1024**2):.0f} MB")

print("\n" + "="*80)
print("Summary")
print("="*80)
print(f"Original:       {original_size / (1024**2):6.0f} MB")
print(f"Minimal:        {minimal_size / (1024**2):6.0f} MB  (removed optimizer/logs)")
print(f"Float16:        {fp16_size / (1024**2):6.0f} MB  (half precision)")
print("="*80)

print("\n✅ Recommendation:")
if fp16_size < 1024**3:  # Less than 1 GB
    print(f"   Use: shakespeare_gpt2_fp16.pt ({fp16_size / (1024**2):.0f} MB)")
    print(f"   This fits within HuggingFace's 1 GB git limit!")
    print(f"\n📋 Next steps:")
    print(f"   1. Copy to LLM_Decoder: cp shakespeare_gpt2_fp16.pt LLM_Decoder/shakespeare_gpt2_final.pt")
    print(f"   2. Update app.py to use float16 inference")
    print(f"   3. Push to HuggingFace")
else:
    print(f"   Use: shakespeare_gpt2_minimal.pt ({minimal_size / (1024**2):.0f} MB)")
    print(f"   Use web upload to HuggingFace")

print()

