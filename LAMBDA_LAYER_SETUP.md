# 🚀 **AWS Lambda Layer Setup Guide**
## Creating Lambda Layer for Google Generative AI Dependencies

---

## 📋 **Overview**

Lambda layers allow you to package dependencies separately from your function code, making deployments faster and more efficient. This guide shows how to create a layer for the `google-generativeai` package.

---

## 🔄 **Step 1: Pull Code to AWS CloudShell**

### **1.1 Access AWS CloudShell**
1. Log in to AWS Console
2. Click the CloudShell icon (terminal) in the top toolbar
3. Wait for CloudShell to initialize

### **1.2 Clone Repository**
```bash
# Clone your repository
git clone https://github.com/VishalMaurya/ERA_Assignments.git
cd ERA_Assignments/Session2_Assignment

# Switch to the demo app branch
git checkout simple-demo-app

# Verify files
ls -la
# Should see: lambda_function.py, requirements.txt, README.md
```

---

## 📦 **Step 2: Create Lambda Layer Structure**

### **2.1 Create Layer Directory Structure**
```bash
# Create layer directory structure
mkdir -p lambda-layer/python/lib/python3.9/site-packages

# Navigate to layer directory
cd lambda-layer
```

### **2.2 Install Dependencies**
```bash
# Install dependencies into the layer structure
pip install google-generativeai -t python/lib/python3.9/site-packages/

# Verify installation
ls python/lib/python3.9/site-packages/
# Should see: google, grpc, etc.
```

### **2.3 Clean Up Layer (Optional)**
```bash
# Remove unnecessary files to reduce layer size
cd python/lib/python3.9/site-packages/

# Remove test files and caches
find . -type d -name "tests" -exec rm -rf {} +
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

# Check layer size (should be under 50MB unzipped)
du -sh .
cd ../../../..
```

---

## 📋 **Step 3: Package and Deploy Layer**

### **3.1 Create Layer ZIP**
```bash
# From lambda-layer directory
zip -r9 therapy-app-dependencies.zip python/

# Verify ZIP contents
unzip -l therapy-app-dependencies.zip | head -20

# Check ZIP size (should be under 10MB zipped)
ls -lh therapy-app-dependencies.zip
```

### **3.2 Deploy Layer to AWS**
```bash
# Create Lambda layer
aws lambda publish-layer-version \
    --layer-name therapy-app-dependencies \
    --description "Google Generative AI dependencies for therapy app" \
    --zip-file fileb://therapy-app-dependencies.zip \
    --compatible-runtimes python3.9 python3.10 python3.11 \
    --region us-east-1

# Note the LayerVersionArn from the output
```

### **3.3 Get Layer ARN**
```bash
# List layers to get the ARN
aws lambda list-layers --region us-east-1

# Or get specific layer versions
aws lambda list-layer-versions \
    --layer-name therapy-app-dependencies \
    --region us-east-1
```

---

## 🔧 **Step 4: Deploy Lambda Function**

### **4.1 Create Deployment Package**
```bash
# Go back to main directory
cd ..

# Create function ZIP (just the function code)
zip therapy-function.zip lambda_function.py

# Verify function ZIP
unzip -l therapy-function.zip
```

### **4.2 Create Lambda Function**
```bash
# Create IAM role for Lambda (if not exists)
aws iam create-role \
    --role-name therapy-app-lambda-role \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }'

# Attach basic execution policy
aws iam attach-role-policy \
    --role-name therapy-app-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Wait for role to be ready
sleep 10
```

### **4.3 Deploy Function with Layer**
```bash
# Get account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create Lambda function
aws lambda create-function \
    --function-name therapy-assessment-app \
    --runtime python3.9 \
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
    --layers arn:aws:lambda:us-east-1:$ACCOUNT_ID:layer:therapy-app-dependencies:1
```

---

## 🌐 **Step 5: Configure API Gateway**

### **5.1 Create API Gateway**
```bash
# Create REST API
API_ID=$(aws apigateway create-rest-api \
    --name therapy-assessment-api \
    --description "API for therapy assessment app" \
    --query 'id' --output text)

echo "API ID: $API_ID"

# Get root resource ID
ROOT_ID=$(aws apigateway get-resources \
    --rest-api-id $API_ID \
    --query 'items[0].id' --output text)

echo "Root Resource ID: $ROOT_ID"
```

### **5.2 Create Resources and Methods**
```bash
# Create /assessment resource
ASSESSMENT_ID=$(aws apigateway create-resource \
    --rest-api-id $API_ID \
    --parent-id $ROOT_ID \
    --path-part assessment \
    --query 'id' --output text)

# Create GET method for root (home page)
aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $ROOT_ID \
    --http-method GET \
    --authorization-type NONE

# Create GET method for /assessment
aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $ASSESSMENT_ID \
    --http-method GET \
    --authorization-type NONE

# Create POST method for /assessment
aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $ASSESSMENT_ID \
    --http-method POST \
    --authorization-type NONE
```

### **5.3 Configure Lambda Integration**
```bash
# Get Lambda function ARN
LAMBDA_ARN="arn:aws:lambda:us-east-1:$ACCOUNT_ID:function:therapy-assessment-app"

# Configure integration for GET /
aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $ROOT_ID \
    --http-method GET \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations

# Configure integration for GET /assessment
aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $ASSESSMENT_ID \
    --http-method GET \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations

# Configure integration for POST /assessment
aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $ASSESSMENT_ID \
    --http-method POST \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations
```

### **5.4 Grant API Gateway Permissions**
```bash
# Allow API Gateway to invoke Lambda function
aws lambda add-permission \
    --function-name therapy-assessment-app \
    --statement-id apigateway-access \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:us-east-1:$ACCOUNT_ID:$API_ID/*/*"
```

### **5.5 Deploy API**
```bash
# Create deployment
aws apigateway create-deployment \
    --rest-api-id $API_ID \
    --stage-name prod \
    --description "Production deployment"

# Get API URL
API_URL="https://$API_ID.execute-api.us-east-1.amazonaws.com/prod"
echo "API URL: $API_URL"
```

---

## 🧪 **Step 6: Test Deployment**

### **6.1 Test API Endpoints**
```bash
# Test home page
curl -X GET "$API_URL/"

# Test assessment form
curl -X GET "$API_URL/assessment"

# Test assessment submission
curl -X POST "$API_URL/assessment" \
    -H "Content-Type: application/json" \
    -d '{
        "personal_info": {
            "name": "Test User",
            "age": 30
        },
        "responses": {
            "anxiety_level": "Often",
            "mood_description": "Feeling stressed lately"
        }
    }'
```

### **6.2 Check Lambda Logs**
```bash
# View Lambda function logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/therapy-assessment-app"

# Tail logs (replace with actual log group)
aws logs tail /aws/lambda/therapy-assessment-app --follow
```

---

## 🔄 **Step 7: Update Function (Future Updates)**

### **7.1 Update Function Code**
```bash
# After making changes to lambda_function.py
zip therapy-function.zip lambda_function.py

# Update function
aws lambda update-function-code \
    --function-name therapy-assessment-app \
    --zip-file fileb://therapy-function.zip
```

### **7.2 Update Environment Variables**
```bash
# Update Gemini API key
aws lambda update-function-configuration \
    --function-name therapy-assessment-app \
    --environment Variables='{
        "GEMINI_API_KEY":"your_actual_api_key_here",
        "GEMINI_MODEL":"gemini-1.5-pro"
    }'
```

### **7.3 Update Layer (If Dependencies Change)**
```bash
# Recreate layer with new dependencies
pip install -r requirements.txt -t python/lib/python3.9/site-packages/ --upgrade
zip -r9 therapy-app-dependencies-v2.zip python/

# Publish new layer version
aws lambda publish-layer-version \
    --layer-name therapy-app-dependencies \
    --zip-file fileb://therapy-app-dependencies-v2.zip \
    --compatible-runtimes python3.9 python3.10 python3.11

# Update function to use new layer version
aws lambda update-function-configuration \
    --function-name therapy-assessment-app \
    --layers arn:aws:lambda:us-east-1:$ACCOUNT_ID:layer:therapy-app-dependencies:2
```

---

## 📊 **Monitoring & Maintenance**

### **Check Function Status**
```bash
# Get function configuration
aws lambda get-function-configuration \
    --function-name therapy-assessment-app

# Get function metrics
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Duration \
    --dimensions Name=FunctionName,Value=therapy-assessment-app \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-02T00:00:00Z \
    --period 3600 \
    --statistics Average
```

### **Cost Monitoring**
```bash
# Check Lambda costs
aws ce get-cost-and-usage \
    --time-period Start=2024-01-01,End=2024-01-31 \
    --granularity MONTHLY \
    --metrics BlendedCost \
    --group-by Type=DIMENSION,Key=SERVICE
```

---

## 🗑️ **Cleanup (Optional)**

### **Delete Resources**
```bash
# Delete Lambda function
aws lambda delete-function --function-name therapy-assessment-app

# Delete API Gateway
aws apigateway delete-rest-api --rest-api-id $API_ID

# Delete Layer
aws lambda delete-layer-version \
    --layer-name therapy-app-dependencies \
    --version-number 1

# Delete IAM role
aws iam detach-role-policy \
    --role-name therapy-app-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam delete-role --role-name therapy-app-lambda-role
```

---

## 🎯 **Quick Reference**

### **Essential Commands**
```bash
# Pull code
git clone https://github.com/VishalMaurya/ERA_Assignments.git
cd ERA_Assignments/Session2_Assignment && git checkout simple-demo-app

# Create layer
mkdir -p lambda-layer/python/lib/python3.9/site-packages
pip install google-generativeai -t lambda-layer/python/lib/python3.9/site-packages/
cd lambda-layer && zip -r9 therapy-app-dependencies.zip python/

# Deploy layer
aws lambda publish-layer-version \
    --layer-name therapy-app-dependencies \
    --zip-file fileb://therapy-app-dependencies.zip \
    --compatible-runtimes python3.9

# Deploy function
zip therapy-function.zip lambda_function.py
aws lambda create-function \
    --function-name therapy-assessment-app \
    --runtime python3.9 \
    --role arn:aws:iam::ACCOUNT_ID:role/therapy-app-lambda-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://therapy-function.zip \
    --layers arn:aws:lambda:us-east-1:ACCOUNT_ID:layer:therapy-app-dependencies:1
```

---

## ✅ **Checklist**

- [ ] Code pulled to CloudShell
- [ ] Layer directory created
- [ ] Dependencies installed in layer
- [ ] Layer packaged and deployed
- [ ] Lambda function created
- [ ] Environment variables set
- [ ] API Gateway configured
- [ ] Permissions granted
- [ ] API deployed and tested
- [ ] Monitoring set up

---

**🎉 Your therapy assessment app is now running on AWS Lambda with proper dependency management! 🌟**
