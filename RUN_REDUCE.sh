#!/bin/bash

echo "🔧 Reducing Model Size for HuggingFace"
echo "======================================"
echo ""

# Activate pytorch conda environment
echo "📦 Activating pytorch environment..."
source /Users/vishalmaurya/opt/anaconda3/etc/profile.d/conda.sh
conda activate pytorch

echo "✅ Environment activated"
echo ""

# Run the reduction script
echo "🚀 Running model reduction..."
python reduce_model.py

echo ""
echo "======================================"
echo "✅ Model reduction complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Check the created files:"
echo "      - shakespeare_gpt2_minimal.pt (~500 MB)"
echo "      - shakespeare_gpt2_fp16.pt (~250 MB)"
echo ""
echo "   2. Copy the smaller file to LLM_Decoder:"
echo "      cp shakespeare_gpt2_fp16.pt LLM_Decoder/shakespeare_gpt2_final.pt"
echo ""
echo "   3. Push to HuggingFace:"
echo "      cd LLM_Decoder"
echo "      git add shakespeare_gpt2_final.pt"
echo "      git commit --amend -m 'Add Shakespeare GPT-2 (optimized)'"
echo "      git push origin main --force"
echo ""
