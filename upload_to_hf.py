"""
Upload Shakespeare GPT-2 app to HuggingFace Space
Using HuggingFace API token
"""

import os
from huggingface_hub import HfApi, create_repo, upload_file, upload_folder
from huggingface_hub.utils import RepositoryNotFoundError

# Configuration
HF_TOKEN = os.getenv("HF_TOKEN", "YOUR_TOKEN_HERE")  # Set via environment variable
SPACE_ID = "VishalMaurya/LLM_Decoder"
FILES_DIR = "hf_space_upload"

def upload_to_space():
    """Upload files to HuggingFace Space"""
    
    print("="*80)
    print("🚀 Uploading Shakespeare GPT-2 to HuggingFace Space")
    print("="*80)
    print(f"Space: {SPACE_ID}")
    print(f"Files: {FILES_DIR}/")
    print("="*80)
    print()
    
    # Initialize HF API
    api = HfApi(token=HF_TOKEN)
    
    # Check if files exist
    required_files = [
        'app.py',
        'shakespeare_gpt2_final.pt',
        'requirements.txt',
        'README.md'
    ]
    
    print("📋 Checking files...")
    for file in required_files:
        filepath = os.path.join(FILES_DIR, file)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            size_mb = size / (1024 * 1024)
            print(f"✅ {file:30s} ({size_mb:.1f} MB)")
        else:
            print(f"❌ {file:30s} (MISSING!)")
            return
    
    print()
    print("="*80)
    print("📤 Starting upload...")
    print("="*80)
    print()
    
    try:
        # Upload each file
        for file in required_files:
            filepath = os.path.join(FILES_DIR, file)
            print(f"⬆️  Uploading {file}...")
            
            # For large files, show progress
            if file.endswith('.pt'):
                print(f"   ⚠️  Large file - this will take 2-3 minutes...")
            
            api.upload_file(
                path_or_fileobj=filepath,
                path_in_repo=file,
                repo_id=SPACE_ID,
                repo_type="space",
                token=HF_TOKEN,
            )
            print(f"   ✅ {file} uploaded!")
            print()
        
        print("="*80)
        print("🎉 SUCCESS! All files uploaded!")
        print("="*80)
        print()
        print(f"Your Space is building at:")
        print(f"🔗 https://huggingface.co/spaces/{SPACE_ID}")
        print()
        print("⏳ Wait 3-5 minutes for the build to complete")
        print("Then your app will be live!")
        print()
        print("="*80)
        
    except Exception as e:
        print("="*80)
        print("❌ ERROR during upload!")
        print("="*80)
        print(f"Error: {str(e)}")
        print()
        print("Troubleshooting:")
        print("1. Check your token is valid")
        print("2. Make sure the Space exists: https://huggingface.co/spaces/VishalMaurya/LLM_Decoder")
        print("3. Try creating the Space first at: https://huggingface.co/new-space")
        print()
        return False
    
    return True


if __name__ == "__main__":
    # Check if huggingface_hub is installed
    try:
        import huggingface_hub
        print("✅ huggingface_hub is installed")
        print()
    except ImportError:
        print("❌ huggingface_hub not installed!")
        print()
        print("Install it with:")
        print("  pip install huggingface_hub")
        print()
        exit(1)
    
    # Check if files directory exists
    if not os.path.exists(FILES_DIR):
        print(f"❌ Directory not found: {FILES_DIR}/")
        print()
        print("Run this first:")
        print("  ./UPLOAD_TO_HF.sh")
        print()
        exit(1)
    
    # Upload
    success = upload_to_space()
    
    if success:
        print("🎯 Next steps:")
        print("1. Visit your Space: https://huggingface.co/spaces/VishalMaurya/LLM_Decoder")
        print("2. Wait for build to complete (~3-5 minutes)")
        print("3. Test your app!")
        print("4. Take a screenshot for your assignment")
        print("5. Submit with the Space URL")
        print()

