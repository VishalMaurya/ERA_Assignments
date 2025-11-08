"""
HuggingFace Authentication Setup
=================================

Guide to authenticate with HuggingFace to access gated datasets.
"""

import os

def setup_authentication():
    """Guide through HuggingFace authentication."""
    
    print("="*70)
    print("🔐 HuggingFace Authentication Setup")
    print("="*70)
    
    print("\n📋 Steps to authenticate:")
    print("\n1️⃣  Create HuggingFace Account (if needed):")
    print("   → Visit: https://huggingface.co/join")
    
    print("\n2️⃣  Accept Dataset Terms:")
    print("   → Visit: https://huggingface.co/datasets/uonlp/CulturaX")
    print("   → Click 'Agree and access dataset'")
    
    print("\n3️⃣  Get Access Token:")
    print("   → Visit: https://huggingface.co/settings/tokens")
    print("   → Click 'New token'")
    print("   → Name it (e.g., 'corpus-download')")
    print("   → Select 'Read' access")
    print("   → Copy the token")
    
    print("\n4️⃣  Login (choose ONE method):")
    print("\n   METHOD A: Using CLI (Recommended)")
    print("   → Run: huggingface-cli login")
    print("   → Paste your token when prompted")
    
    print("\n   METHOD B: Using Python")
    print("   → Run this script with your token:")
    print("   → python setup_hf_auth.py --token YOUR_TOKEN_HERE")
    
    print("\n   METHOD C: Environment Variable")
    print("   → export HF_TOKEN=YOUR_TOKEN_HERE")
    
    print("\n" + "="*70)
    print("✅ After authentication, run:")
    print("   python download_indian_language.py")
    print("="*70)

def login_with_token(token):
    """Login with provided token."""
    try:
        from huggingface_hub import login
        login(token=token)
        print("✅ Successfully authenticated!")
        print("🚀 You can now download gated datasets")
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, default=None,
                       help='HuggingFace access token')
    parser.add_argument('--test', action='store_true',
                       help='Test if already authenticated')
    
    args = parser.parse_args()
    
    if args.token:
        print("🔐 Authenticating with provided token...")
        login_with_token(args.token)
    elif args.test:
        try:
            from huggingface_hub import whoami
            user = whoami()
            print(f"✅ Already authenticated as: {user['name']}")
        except Exception as e:
            print(f"❌ Not authenticated: {e}")
            print("\n💡 Run: python setup_hf_auth.py")
    else:
        setup_authentication()

