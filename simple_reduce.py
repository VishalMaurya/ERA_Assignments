"""
Simple model size reduction
Extract and convert weights without loading full model
"""
import torch
import os
from dataclasses import dataclass

# Need to define config class for unpickling
@dataclass
class GPTConfig:
    block_size: int = 1024
    vocab_size: int = 50257
    n_layer: int = 12
    n_head: int = 12
    n_embd: int = 768

print("="*80)
print("Reducing Model Size for HuggingFace")
print("="*80)

input_file = 'LLM_Decoder/shakespeare_gpt2_final.pt'

# Load with weights_only to avoid class dependencies
print(f"\n📂 Loading checkpoint...")
checkpoint = torch.load(input_file, map_location='cpu', weights_only=False)

original_size = os.path.getsize(input_file)
print(f"✅ Loaded successfully")
print(f"   Original size: {original_size/(1024**2):.0f} MB")
print(f"   Keys: {list(checkpoint.keys())}")

# Method 1: Remove optimizer (keep float32)
print(f"\n🔧 Creating minimal checkpoint (float32)...")
minimal = {
    'model_state_dict': checkpoint['model_state_dict'],
    'config': checkpoint['config'],
}

torch.save(minimal, 'shakespeare_gpt2_minimal.pt')
minimal_size = os.path.getsize('shakespeare_gpt2_minimal.pt')
print(f"✅ Saved: shakespeare_gpt2_minimal.pt")
print(f"   Size: {minimal_size/(1024**2):.0f} MB")
print(f"   Reduction: {(1 - minimal_size/original_size)*100:.1f}%")

# Method 2: Convert to float16
print(f"\n🎯 Creating float16 checkpoint...")
state_fp16 = {}
count = 0
for key, value in checkpoint['model_state_dict'].items():
    if hasattr(value, 'dtype') and value.dtype == torch.float32:
        state_fp16[key] = value.half()
        count += 1
    else:
        state_fp16[key] = value

fp16_checkpoint = {
    'model_state_dict': state_fp16,
    'config': checkpoint['config'],
}

torch.save(fp16_checkpoint, 'shakespeare_gpt2_fp16.pt')
fp16_size = os.path.getsize('shakespeare_gpt2_fp16.pt')
print(f"✅ Saved: shakespeare_gpt2_fp16.pt")
print(f"   Size: {fp16_size/(1024**2):.0f} MB")
print(f"   Reduction: {(1 - fp16_size/original_size)*100:.1f}%")
print(f"   Converted {count} tensors to float16")

print(f"\n" + "="*80)
print("Summary")
print("="*80)
print(f"Original:  {original_size/(1024**2):7.0f} MB  (in LLM_Decoder/)")
print(f"Minimal:   {minimal_size/(1024**2):7.0f} MB  ✅ No optimizer/logs")
print(f"Float16:   {fp16_size/(1024**2):7.0f} MB  ✅✅ Half precision")
print("="*80)

# Check if under 1GB
if fp16_size < 1024**3:
    print(f"\n🎉 SUCCESS! Float16 model is under 1 GB!")
    print(f"   You can now push to HuggingFace via git!")
    print(f"\n📋 Next steps:")
    print(f"   cp shakespeare_gpt2_fp16.pt LLM_Decoder/shakespeare_gpt2_final.pt")
    print(f"   cd LLM_Decoder")
    print(f"   git add shakespeare_gpt2_final.pt")
    print(f"   git commit --amend -m 'Add Shakespeare GPT-2 (optimized fp16)'")
    print(f"   git push origin main --force")
else:
    print(f"\n⚠️  Still larger than 1 GB")
    print(f"   Use web upload to HuggingFace")

print()

