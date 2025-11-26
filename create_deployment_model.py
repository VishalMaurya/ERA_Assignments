#!/usr/bin/env python3
"""
Create deployment-ready model (removes optimizer and logs)
This should reduce file from 1.4 GB to ~500 MB
"""

import torch
import os
from dataclasses import dataclass

@dataclass
class GPTConfig:
    block_size: int = 1024
    vocab_size: int = 50257
    n_layer: int = 12
    n_head: int = 12
    n_embd: int = 768

print("="*80)
print("Creating Deployment Model (Removing Optimizer & Logs)")
print("="*80)
print()

# Load from LLM_Decoder
input_path = 'LLM_Decoder/shakespeare_gpt2_final.pt'
output_path = 'shakespeare_gpt2_deploy.pt'

print(f"📂 Loading: {input_path}")
checkpoint = torch.load(input_path, map_location='cpu')

original_size = os.path.getsize(input_path)
print(f"✅ Loaded")
print(f"   Original size: {original_size/(1024**2):.0f} MB")
print(f"   Contains: {list(checkpoint.keys())}")
print()

# Create deployment checkpoint (ONLY what's needed for inference)
deployment_checkpoint = {
    'model_state_dict': checkpoint['model_state_dict'],
    'config': checkpoint['config'],
}

print(f"💾 Saving deployment model...")
print(f"   Keeping: model_state_dict, config")
print(f"   Removing: optimizer_state_dict, training_log")
print()

torch.save(deployment_checkpoint, output_path)

new_size = os.path.getsize(output_path)
reduction = (1 - new_size/original_size) * 100

print("="*80)
print("Results")
print("="*80)
print(f"Original:    {original_size/(1024**2):6.0f} MB  (with optimizer + logs)")
print(f"Deployment:  {new_size/(1024**2):6.0f} MB  (model only)")
print(f"Reduction:   {reduction:5.1f}%")
print("="*80)
print()

if new_size < 1024**3:  # Under 1 GB
    print("🎉 SUCCESS! Model is now under 1 GB!")
    print()
    print("📋 Next steps:")
    print(f"   1. Copy to LLM_Decoder:")
    print(f"      cp {output_path} LLM_Decoder/shakespeare_gpt2_final.pt")
    print()
    print(f"   2. Push to HuggingFace:")
    print(f"      cd LLM_Decoder")
    print(f"      git add shakespeare_gpt2_final.pt")
    print(f"      git commit --amend -m 'Add Shakespeare GPT-2 (deployment-ready)'")
    print(f"      git push origin main --force")
else:
    print("⚠️  Still over 1 GB. Use web upload to HuggingFace.")
    
print()
print(f"✅ Deployment model saved: {output_path}")
print()

