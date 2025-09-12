# 🧠 Simple Therapy Assessment Lambda

Single Python file Lambda function for therapy assessment with AI recommendations.

## 📋 Features

- **GET /** - API documentation and usage examples
- **GET /assessment** - Returns therapy assessment form with prefilled sample data  
- **POST /assessment** - Processes assessment and returns AI recommendations using Google Gemini

## 🚀 Quick Test

```bash
# Test locally
python lambda_function.py

# Or test individual endpoints
python -c "
import lambda_function
import json

# Test home page
event = {'httpMethod': 'GET', 'path': '/'}
result = lambda_function.lambda_handler(event, {})
print(json.dumps(json.loads(result['body']), indent=2))
"
```

## 📡 API Endpoints

### 1. Home Page - GET /
Returns API documentation with usage examples.

### 2. Assessment Form - GET /assessment  
Returns a JSON therapy assessment form with prefilled sample data:

```json
{
  "personal_info": {
    "name": "John Doe",
    "age": 28,
    "occupation": "Software Developer"
  },
  "responses": {
    "anxiety_level": "Often",
    "sleep_quality": 4,
    "stress_sources": ["Work", "Financial"],
    "mood_description": "Feeling overwhelmed lately..."
  }
}
```

### 3. AI Recommendations - POST /assessment
Submit the assessment data and get AI-powered recommendations:

```bash
curl -X POST https://your-lambda-url/assessment \
  -H "Content-Type: application/json" \
  -d '{
    "personal_info": {"name": "John", "age": 28},
    "responses": {
      "anxiety_level": "Often",
      "mood_description": "Feeling stressed"
    }
  }'
```

Returns structured AI recommendations including:
- Personal summary
- Key insights  
- Recommended therapies
- Coping strategies
- Progress tracking suggestions

## 🔧 Environment Variables

Required environment variables for AI recommendations:

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export GEMINI_MODEL="gemini-2.0-flash"  # Optional, defaults to gemini-2.0-flash
```

Available Gemini models:
- `gemini-2.0-flash` (default - fast and efficient)
- `gemini-1.5-pro` (more comprehensive analysis)
- `gemini-1.5-flash` (balanced performance)

If `GEMINI_API_KEY` is not set, fallback recommendations are provided.

## 🏗️ Deployment

### Option 1: Simple Upload (for testing)
1. Install dependencies: `pip install -r requirements.txt`
2. Zip everything: `zip -r therapy-lambda.zip lambda_function.py requirements.txt site-packages/`
3. Upload to Lambda console
4. Set environment variables and configure API Gateway

### Option 2: Production with Lambda Layer (Recommended)
See detailed guide: **[LAMBDA_LAYER_SETUP.md](./LAMBDA_LAYER_SETUP.md)**

**Step-by-Step Deployment:**

#### 🔄 Pull Code to AWS CloudShell
```bash
# Access AWS CloudShell from AWS Console
git clone https://github.com/VishalMaurya/ERA_Assignments.git
cd ERA_Assignments/Session2_Assignment
git checkout simple-demo-app
```

#### 📦 Create Lambda Layer
```bash
# Create layer structure
mkdir -p lambda-layer/python/lib/python3.12/site-packages

# Install dependencies
pip install google-generativeai -t lambda-layer/python/lib/python3.12/site-packages/

# Package layer
cd lambda-layer
zip -r9 therapy-app-dependencies.zip python/

# Deploy layer to AWS
aws lambda publish-layer-version \
    --layer-name therapy-app-dependencies \
    --description "Google Generative AI dependencies" \
    --zip-file fileb://therapy-app-dependencies.zip \
    --compatible-runtimes python3.12 \
    --region us-east-1
```

#### 🚀 Deploy Lambda Function
```bash
# Go back to main directory
cd ..

# Create IAM role for Lambda
aws iam create-role \
    --role-name therapy-app-lambda-role \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }'

# Attach execution policy
aws iam attach-role-policy \
    --role-name therapy-app-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Package function code
zip therapy-function.zip lambda_function.py

# Get account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create Lambda function with layer
aws lambda create-function \
    --function-name therapy-assessment-app \
    --runtime python3.12 \
    --role arn:aws:iam::$ACCOUNT_ID:role/therapy-app-lambda-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://therapy-function.zip \
    --description "Therapy assessment app with AI recommendations" \
    --timeout 60 \
    --memory-size 512 \
    --environment Variables='{
        "GEMINI_API_KEY":"YOUR_API_KEY_HERE",
        "GEMINI_MODEL":"gemini-2.0-flash"
    }' \
    --layers arn:aws:lambda:us-east-1:$ACCOUNT_ID:layer:therapy-app-dependencies:1 \
    --region us-east-1
```

#### 🌐 Configure API Gateway
```bash
# Create REST API
API_ID=$(aws apigateway create-rest-api \
    --name therapy-assessment-api \
    --description "API for therapy assessment app" \
    --query 'id' --output text)

# Get root resource ID
ROOT_ID=$(aws apigateway get-resources \
    --rest-api-id $API_ID \
    --query 'items[0].id' --output text)

# Create /assessment resource
ASSESSMENT_ID=$(aws apigateway create-resource \
    --rest-api-id $API_ID \
    --parent-id $ROOT_ID \
    --path-part assessment \
    --query 'id' --output text)

# Create methods (GET /, GET /assessment, POST /assessment)
aws apigateway put-method --rest-api-id $API_ID --resource-id $ROOT_ID --http-method GET --authorization-type NONE
aws apigateway put-method --rest-api-id $API_ID --resource-id $ASSESSMENT_ID --http-method GET --authorization-type NONE
aws apigateway put-method --rest-api-id $API_ID --resource-id $ASSESSMENT_ID --http-method POST --authorization-type NONE

# Configure Lambda integration
LAMBDA_ARN="arn:aws:lambda:us-east-1:$ACCOUNT_ID:function:therapy-assessment-app"

aws apigateway put-integration \
    --rest-api-id $API_ID --resource-id $ROOT_ID --http-method GET \
    --type AWS_PROXY --integration-http-method POST \
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations

aws apigateway put-integration \
    --rest-api-id $API_ID --resource-id $ASSESSMENT_ID --http-method GET \
    --type AWS_PROXY --integration-http-method POST \
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations

aws apigateway put-integration \
    --rest-api-id $API_ID --resource-id $ASSESSMENT_ID --http-method POST \
    --type AWS_PROXY --integration-http-method POST \
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations

# Grant API Gateway permission to invoke Lambda
aws lambda add-permission \
    --function-name therapy-assessment-app \
    --statement-id apigateway-access \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:us-east-1:$ACCOUNT_ID:$API_ID/*/*"

# Deploy API
aws apigateway create-deployment \
    --rest-api-id $API_ID \
    --stage-name prod \
    --description "Production deployment"

# Get API URL
API_URL="https://$API_ID.execute-api.us-east-1.amazonaws.com/prod"
echo "🎉 API URL: $API_URL"
```

#### 🧪 Test Your Deployment
```bash
# Test all endpoints
curl -X GET "$API_URL/"                    # Home page
curl -X GET "$API_URL/assessment"          # Assessment form
curl -X POST "$API_URL/assessment" \       # AI recommendations
    -H "Content-Type: application/json" \
    -d '{
        "personal_info": {"name": "Test User", "age": 30},
        "responses": {
            "anxiety_level": "Often",
            "mood_description": "Feeling stressed lately"
        }
    }'
```

**Benefits of Layer Approach:**
- ✅ Faster deployments (dependencies separate from code)
- ✅ Smaller function packages (under 1MB vs 50MB+)
- ✅ Reusable across functions
- ✅ Better version management
- ✅ Production-grade setup

### 🔄 Function Updates (After Initial Deployment)
```bash
# Update function code only (fast!)
zip therapy-function.zip lambda_function.py
aws lambda update-function-code \
    --function-name therapy-assessment-app \
    --zip-file fileb://therapy-function.zip

# Update environment variables
aws lambda update-function-configuration \
    --function-name therapy-assessment-app \
    --environment Variables='{
        "GEMINI_API_KEY":"your_updated_key",
        "GEMINI_MODEL":"gemini-1.5-pro"
    }'
```

### 🧹 Cleanup (Optional)
```bash
# Delete all resources to avoid charges
aws lambda delete-function --function-name therapy-assessment-app
aws apigateway delete-rest-api --rest-api-id $API_ID
aws lambda delete-layer-version --layer-name therapy-app-dependencies --version-number 1
aws iam detach-role-policy --role-name therapy-app-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role --role-name therapy-app-lambda-role
```

### Local Development:
```bash
pip install -r requirements.txt
python lambda_function.py
```

## 📝 Sample Response

```json
{
  "success": true,
  "patient_info": {
    "name": "John Doe",
    "assessment_date": "2024-01-01 12:00:00"
  },
  "ai_analysis": {
    "summary": "Based on your responses, you're experiencing moderate anxiety...",
    "recommended_therapies": [
      {
        "therapy_name": "Cognitive Behavioral Therapy",
        "suitability_reason": "Effective for anxiety management",
        "expected_outcomes": "Better coping skills"
      }
    ],
    "immediate_coping_strategies": [
      "Practice deep breathing exercises",
      "Try progressive muscle relaxation"
    ]
  }
}
```

**Simple, effective, and ready to deploy! 🌟**