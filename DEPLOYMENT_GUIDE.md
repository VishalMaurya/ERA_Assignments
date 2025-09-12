# 🚀 **AWS Lambda Deployment Guidelines**
## Complete Guide for Therapy App Serverless Deployment

---

## 📋 **Prerequisites Checklist**

### **Required Tools:**
- [ ] **AWS Account** with programmatic access
- [ ] **AWS CLI** installed and configured  
- [ ] **SAM CLI** installed
- [ ] **Node.js 18+** installed
- [ ] **Google Gemini API Key**

### **Install AWS CLI:**
```bash
# macOS
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

### **Install SAM CLI:**
```bash
# Using pip
pip install aws-sam-cli

# Using Homebrew (macOS)
brew install aws-sam-cli

# Verify installation
sam --version
```

### **Configure AWS Credentials:**
```bash
aws configure
# Enter:
# AWS Access Key ID: [your-access-key]
# AWS Secret Access Key: [your-secret-key]  
# Default region: us-east-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity
```

---

## 🔑 **Environment Setup**

### **1. Get Google Gemini API Key:**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new project or select existing
3. Generate API key
4. Copy the key (starts with `AIza...`)

### **2. Set Environment Variables:**
```bash
# Set Gemini API key (required for deployment)
export GEMINI_API_KEY="your_gemini_api_key_here"

# Optional: Set AWS region if different from default
export AWS_REGION="us-east-1"
```

---

## 🚀 **Deployment Steps**

### **Step 1: Quick Deploy (Recommended)**
```bash
# Make deployment script executable
chmod +x deploy.sh

# Deploy to production
./deploy.sh prod

# Deploy to development (optional)
./deploy.sh dev
```

### **Step 2: Manual Deploy (Advanced)**
```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Build SAM application
sam build --use-container

# Deploy with guided setup (first time)
sam deploy --guided

# Deploy with existing configuration
sam deploy \
  --stack-name therapy-app-prod \
  --parameter-overrides \
    Environment=prod \
    GeminiApiKey=$GEMINI_API_KEY \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset
```

---

## 🧪 **Testing Deployment**

### **1. Get API URL:**
```bash
# From deployment output or CloudFormation
aws cloudformation describe-stacks \
  --stack-name therapy-app-prod \
  --query 'Stacks[0].Outputs[?OutputKey==`TherapyAppApiUrl`].OutputValue' \
  --output text
```

### **2. Test API Endpoints:**
```bash
# Set your API URL
API_URL="https://your-api-gateway-url/prod"

# Test user endpoint (should return 404 - user not found)
curl "$API_URL/auth/user?userId=test-user"

# Register a new user
curl -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'

# Start an assessment
curl -X POST "$API_URL/assessment/start" \
  -H "Content-Type: application/json" \
  -d '{"userId":"user_123","type":"anxiety"}'

# Generate a report
curl -X POST "$API_URL/report/generate" \
  -H "Content-Type: application/json" \
  -d '{"userId":"user_123","assessmentId":"assessment_123"}'

# Get analytics
curl "$API_URL/analytics/dashboard?userId=user_123"
```

---

## 🏗️ **Infrastructure Overview**

### **AWS Resources Created:**
- **API Gateway**: REST API with CORS enabled
- **Lambda Functions**: 4 serverless functions
  - `AuthFunction`: User management
  - `AssessmentFunction`: Assessment CRUD
  - `ReportFunction`: AI report generation  
  - `AnalyticsFunction`: Dashboard analytics
- **DynamoDB Table**: Single table design with GSI
- **S3 Bucket**: File storage (encrypted)
- **CloudWatch**: Logs and monitoring
- **IAM Roles**: Least privilege access

### **Cost Estimation:**
| **Usage Level** | **Monthly Cost** | **Details** |
|-----------------|------------------|-------------|
| **Development** | $0 - $5 | Free tier eligible |
| **Small (1K users)** | $5 - $15 | Light usage |
| **Medium (10K users)** | $25 - $50 | Regular usage |
| **Large (100K users)** | $150 - $300 | High usage |

---

## 🔧 **Configuration Options**

### **Environment Variables (in template.yaml):**
```yaml
Environment:
  Variables:
    DYNAMODB_TABLE: !Ref TherapyAppTable
    S3_BUCKET: !Ref TherapyAppBucket  
    GEMINI_API_KEY: !Ref GeminiApiKey
    LOG_LEVEL: info                    # debug, info, warn, error
    NODE_ENV: production               # development, production
```

### **Lambda Function Settings:**
```yaml
Globals:
  Function:
    Timeout: 30                        # Seconds (max 900)
    MemorySize: 512                    # MB (128-10240)
    Runtime: nodejs18.x                # Node.js version
    ReservedConcurrencyLimit: 100      # Max concurrent executions
```

### **DynamoDB Settings:**
```yaml
TherapyAppTable:
  BillingMode: PAY_PER_REQUEST         # or PROVISIONED
  PointInTimeRecoverySpecification:
    PointInTimeRecoveryEnabled: true   # Backup enabled
  StreamSpecification:
    StreamViewType: NEW_AND_OLD_IMAGES # Change tracking
```

---

## 🔍 **Local Development**

### **1. Start Local API:**
```bash
# Start all functions locally
sam local start-api

# Start with debug mode
sam local start-api --debug

# Start with custom port
sam local start-api --port 3001
```

### **2. Test Individual Functions:**
```bash
# Create test event file
echo '{"httpMethod":"GET","path":"/auth/user","queryStringParameters":{"userId":"test"}}' > test-event.json

# Invoke specific function
sam local invoke AuthFunction -e test-event.json

# With debug
sam local invoke AuthFunction -e test-event.json --debug
```

### **3. Local Environment Setup:**
```bash
# Create local environment file
echo "GEMINI_API_KEY=your_api_key" > .env

# Install dependencies
npm install

# Build TypeScript
npm run build

# Watch for changes
npm run build:dev
```

---

## 📊 **Monitoring & Logging**

### **CloudWatch Logs:**
```bash
# View function logs
aws logs tail /aws/lambda/therapy-app-prod-AuthFunction --follow

# View API Gateway logs  
aws logs tail /aws/apigateway/therapy-app-prod --follow

# View all Lambda logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/therapy-app"
```

### **CloudWatch Metrics:**
```bash
# Get function metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=therapy-app-prod-AuthFunction \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average
```

### **Set Up Alarms:**
```bash
# High error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "therapy-app-high-errors" \
  --alarm-description "High error rate in Lambda functions" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

---

## 🔄 **Updates & Maintenance**

### **Update Function Code:**
```bash
# Make changes to code
# Then build and deploy
npm run build
sam deploy --stack-name therapy-app-prod
```

### **Update Configuration:**
```bash
# Modify template.yaml
# Then deploy
sam deploy --stack-name therapy-app-prod --parameter-overrides Environment=prod
```

### **Database Operations:**
```bash
# Backup table
aws dynamodb create-backup \
  --table-name therapy-app-prod \
  --backup-name therapy-app-backup-$(date +%Y%m%d)

# Query table
aws dynamodb scan --table-name therapy-app-prod --max-items 10

# Update item
aws dynamodb update-item \
  --table-name therapy-app-prod \
  --key '{"PK":{"S":"USER#123"},"SK":{"S":"PROFILE"}}' \
  --update-expression "SET preferences.theme = :theme" \
  --expression-attribute-values '{":theme":{"S":"dark"}}'
```

---

## 🚨 **Troubleshooting**

### **Common Issues:**

| **Issue** | **Cause** | **Solution** |
|-----------|-----------|-------------|
| **Deployment fails** | Missing permissions | Check IAM permissions, run `aws sts get-caller-identity` |
| **Lambda timeout** | Long-running operations | Increase timeout in template.yaml |
| **API Gateway 502** | Lambda function error | Check CloudWatch logs |
| **DynamoDB throttling** | High request rate | Switch to on-demand billing |
| **CORS errors** | Missing headers | Verify CORS configuration in template.yaml |

### **Debug Commands:**
```bash
# Check stack status
aws cloudformation describe-stacks --stack-name therapy-app-prod

# View stack events
aws cloudformation describe-stack-events --stack-name therapy-app-prod

# Validate template
sam validate --template template.yaml

# Check function configuration
aws lambda get-function-configuration --function-name therapy-app-prod-AuthFunction
```

### **Clean Up (if needed):**
```bash
# Delete entire stack
aws cloudformation delete-stack --stack-name therapy-app-prod

# Empty S3 bucket first (if needed)
aws s3 rm s3://therapy-app-prod-bucket --recursive
```

---

## 🔐 **Security Best Practices**

### **API Security:**
- ✅ HTTPS enforced by default
- ✅ CORS properly configured
- ✅ No sensitive data in logs
- ✅ API keys not in code

### **Lambda Security:**
- ✅ Least privilege IAM roles
- ✅ Environment variables encrypted
- ✅ VPC isolation (optional)
- ✅ Runtime security scanning

### **Database Security:**
- ✅ Encryption at rest enabled
- ✅ Encryption in transit enabled
- ✅ Point-in-time recovery enabled
- ✅ Backup retention configured

---

## 🎯 **Performance Optimization**

### **Lambda Optimization:**
```yaml
# In template.yaml
Globals:
  Function:
    MemorySize: 1024              # Increase for better performance
    ReservedConcurrencyLimit: 50  # Prevent cold starts
    Environment:
      Variables:
        NODE_OPTIONS: '--enable-source-maps'
```

### **DynamoDB Optimization:**
```yaml
# Add TTL for automatic cleanup
TimeToLiveSpecification:
  AttributeName: expiresAt
  Enabled: true

# Add more GSIs for query patterns
GlobalSecondaryIndexes:
  - IndexName: GSI2
    KeySchema:
      - AttributeName: GSI2PK
        KeyType: HASH
    Projection:
      ProjectionType: ALL
```

---

## 📞 **Support Resources**

### **Documentation:**
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/)

### **Community:**
- [AWS Lambda Forum](https://forums.aws.amazon.com/forum.jspa?forumID=186)
- [Stack Overflow - AWS Lambda](https://stackoverflow.com/questions/tagged/aws-lambda)
- [AWS re:Post](https://repost.aws/)

---

## ✅ **Deployment Checklist**

- [ ] AWS CLI configured with correct credentials
- [ ] SAM CLI installed and working
- [ ] Gemini API key obtained and set
- [ ] Code built successfully (`npm run build`)
- [ ] Template validated (`sam validate`)
- [ ] Deployed to AWS (`./deploy.sh prod`)
- [ ] API endpoints tested
- [ ] CloudWatch logs checked
- [ ] Database records verified
- [ ] Cost monitoring set up

---

**🎉 Your therapy app is now live on AWS! 🌟**
