#!/bin/bash

cd /Users/vishalmaurya/Documents/Projects/ERA_V4/Session2_Assignment

echo "🔧 Creating Deployment Model"
echo "======================================"
echo ""

# Run with conda python
/Users/vishalmaurya/opt/anaconda3/envs/pytorch/bin/python create_deployment_model.py

echo ""
echo "======================================"
echo "Next steps:"
echo "  cp shakespeare_gpt2_deploy.pt LLM_Decoder/shakespeare_gpt2_final.pt"
echo "  cd LLM_Decoder"
echo "  git add shakespeare_gpt2_final.pt"
echo "  git commit --amend -m 'Add Shakespeare GPT-2 (deployment)'"
echo "  git push origin main --force"
echo ""

