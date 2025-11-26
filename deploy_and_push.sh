#!/bin/bash

cd /Users/vishalmaurya/Documents/Projects/ERA_V4/Session2_Assignment

echo "🚀 Deploying Model to HuggingFace"
echo "======================================"
echo ""

# Check if deployment model exists
if [ ! -f "shakespeare_gpt2_minimal.pt" ]; then
    echo "❌ shakespeare_gpt2_minimal.pt not found!"
    echo "   Run: python create_deployment_model.py first"
    exit 1
fi

# Get file sizes
DEPLOY_SIZE=$(du -h shakespeare_gpt2_minimal.pt | cut -f1)
echo "✅ Found deployment model: $DEPLOY_SIZE"
echo ""

# Step 1: Copy to LLM_Decoder (overwrites the large one)
echo "📂 Step 1: Copying deployment model to LLM_Decoder..."
cp shakespeare_gpt2_minimal.pt LLM_Decoder/shakespeare_gpt2_final.pt
echo "✅ Copied"
echo ""

# Step 2: Navigate to LLM_Decoder
cd LLM_Decoder

# Step 3: Remove large file from git history
echo "🧹 Step 2: Removing large file from git history..."
git rm --cached shakespeare_gpt2_final.pt 2>/dev/null
echo "✅ Removed from cache"
echo ""

# Step 4: Add the new smaller file
echo "➕ Step 3: Adding deployment model..."
git add shakespeare_gpt2_final.pt
NEW_SIZE=$(du -h shakespeare_gpt2_final.pt | cut -f1)
echo "✅ Added deployment model ($NEW_SIZE)"
echo ""

# Step 5: Commit
echo "💾 Step 4: Committing..."
git commit -m "Add Shakespeare GPT-2 (deployment-ready, removed optimizer/logs)"
echo "✅ Committed"
echo ""

# Step 6: Push to HuggingFace with force
echo "🚀 Step 5: Pushing to HuggingFace..."
echo "   (Using force push to replace large file)"
git push origin main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "🎉 SUCCESS!"
    echo "======================================"
    echo ""
    echo "Your app is deploying at:"
    echo "https://huggingface.co/spaces/VishalMaurya/LLM_Decoder"
    echo ""
    echo "Wait 3-5 minutes for build to complete"
    echo ""
    echo "📊 Model size reduced:"
    echo "   Before: ~1.4 GB"
    echo "   After:  $NEW_SIZE"
    echo ""
else
    echo ""
    echo "❌ Push failed!"
    echo "Check the error message above"
    echo ""
fi

