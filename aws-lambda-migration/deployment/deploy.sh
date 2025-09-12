#!/bin/bash

# Therapy App AWS Lambda Deployment Script
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
ENVIRONMENT=${1:-dev}
STACK_NAME="therapy-app-$ENVIRONMENT"

echo -e "${BLUE}🧠 Deploying Therapy App to AWS Lambda${NC}"
echo "Environment: $ENVIRONMENT"

# Check prerequisites
echo -e "${GREEN}Checking prerequisites...${NC}"
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first."
    exit 1
fi

if ! command -v sam &> /dev/null; then
    echo "❌ SAM CLI not found. Please install it first."
    exit 1
fi

# Get API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Please enter your Google Gemini API key:"
    read -s GEMINI_API_KEY
    export GEMINI_API_KEY
fi

# Build and deploy
echo -e "${GREEN}Building backend...${NC}"
cd ../backend
npm install
npm run build

echo -e "${GREEN}Deploying to AWS...${NC}"
sam build --use-container
sam deploy \
    --stack-name "$STACK_NAME" \
    --parameter-overrides \
        Environment="$ENVIRONMENT" \
        GeminiApiKey="$GEMINI_API_KEY" \
    --capabilities CAPABILITY_IAM \
    --no-confirm-changeset

echo -e "${GREEN}✅ Deployment completed!${NC}"

# Get API URL
API_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`TherapyAppApiUrl`].OutputValue' \
    --output text 2>/dev/null || echo "")

if [ -n "$API_URL" ]; then
    echo -e "${BLUE}🌐 API URL: $API_URL${NC}"
    echo -e "${BLUE}🧪 Test: curl $API_URL/auth/user?userId=test${NC}"
fi
