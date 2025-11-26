#!/bin/bash

# Upload to HuggingFace Space: VishalMaurya/LLM_Decoder
# Run this script to copy all necessary files

echo "🚀 Preparing files for HuggingFace Space upload..."
echo ""

# Create a temporary directory for HF files
HF_DIR="hf_space_upload"
rm -rf $HF_DIR
mkdir -p $HF_DIR

echo "📦 Copying files..."
echo ""

# Copy app.py
cp app.py $HF_DIR/
echo "✅ Copied app.py"

# Copy model
cp shakespeare_gpt2_final.pt $HF_DIR/
echo "✅ Copied shakespeare_gpt2_final.pt (1.4GB)"

# Create requirements.txt
cat > $HF_DIR/requirements.txt << 'EOF'
torch
gradio
tiktoken
EOF
echo "✅ Created requirements.txt"

# Create README.md from HF_README.md
cp HF_README.md $HF_DIR/README.md
echo "✅ Created README.md"

echo ""
echo "✅ All files prepared in: $HF_DIR/"
echo ""
echo "📁 Files ready for upload:"
ls -lh $HF_DIR/
echo ""
echo "─────────────────────────────────────────────────"
echo "🎯 Next Steps:"
echo "─────────────────────────────────────────────────"
echo ""
echo "Option 1: Upload via Web Interface (Easiest)"
echo "  1. Go to: https://huggingface.co/spaces/VishalMaurya/LLM_Decoder"
echo "  2. Click: Files → Add file → Upload files"
echo "  3. Upload all files from: $HF_DIR/"
echo "  4. Done!"
echo ""
echo "Option 2: Upload via Git (if you have git configured)"
echo "  1. cd $HF_DIR"
echo "  2. git init"
echo "  3. git remote add origin https://huggingface.co/spaces/VishalMaurya/LLM_Decoder"
echo "  4. git lfs install"
echo "  5. git lfs track '*.pt'"
echo "  6. git add ."
echo "  7. git commit -m 'Add Shakespeare GPT-2 app'"
echo "  8. git push origin main"
echo ""
echo "─────────────────────────────────────────────────"
echo "💡 Recommended: Use Option 1 (Web Interface)"
echo "─────────────────────────────────────────────────"

