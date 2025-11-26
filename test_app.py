"""
Test the Gradio app locally before deploying
"""

import os

# Check if required files exist
print("Checking required files...")
print()

required_files = {
    'app.py': 'Gradio application',
    'shakespeare_gpt2_final.pt': 'Trained model',
    'input.txt': 'Training data (for reference)',
}

all_present = True
for file, description in required_files.items():
    if os.path.exists(file):
        size = os.path.getsize(file)
        size_mb = size / (1024 * 1024)
        print(f"✅ {file:30s} - {description:30s} ({size_mb:.1f} MB)")
    else:
        print(f"❌ {file:30s} - {description:30s} (MISSING!)")
        all_present = False

print()

if not all_present:
    print("⚠️  Some required files are missing!")
    print()
    print("Make sure you have:")
    print("  1. app.py - The Gradio application")
    print("  2. shakespeare_gpt2_final.pt - Your trained model checkpoint")
    print()
    exit(1)

print("✅ All required files present!")
print()
print("To test the app locally:")
print("  1. Install dependencies: pip install torch gradio tiktoken")
print("  2. Run the app: python app.py")
print("  3. Open browser at http://localhost:7860")
print()
print("To deploy to HuggingFace Spaces:")
print("  1. Create new Space at https://huggingface.co/new-space")
print("  2. Choose: Gradio SDK")
print("  3. Upload files:")
print("     - app.py")
print("     - shakespeare_gpt2_final.pt")
print("     - Create README.md (copy from HF_README.md)")
print("     - Create requirements.txt with:")
print("       torch")
print("       gradio")
print("       tiktoken")
print()
print("Note: Your model is trained for 10,000 steps.")
print("      For better quality, continue training to reach loss < 0.1")
print("      Use: python resume_training.py")
print()

