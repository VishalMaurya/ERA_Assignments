# 🧠 **Therapy App - AWS Lambda Serverless**

Serverless psychological therapy assessment application built with AWS Lambda, API Gateway, and DynamoDB.

## 🚀 **Quick Deploy**

```bash
./deploy.sh prod
```

## 📁 **Project Structure**

```
Session2_Assignment/                  # AWS Lambda Therapy App
├── src/functions/                   # 4 Lambda Functions
│   ├── auth/                        # User authentication & management
│   ├── assessment/                  # Assessment CRUD operations
│   ├── report/                      # AI report generation
│   └── analytics/                   # Dashboard analytics
├── src/shared/                      # Shared utilities & types
├── package.json                     # Dependencies
├── template.yaml                    # AWS SAM infrastructure
├── deploy.sh                        # One-command deployment
├── tsconfig.json                    # TypeScript configuration
└── README.md                        # This file
```

## 🔧 **API Endpoints**

| **Function** | **Endpoints** | **Purpose** |
|--------------|---------------|-------------|
| **Auth** | `/auth/*` | User registration, login, profile |
| **Assessment** | `/assessment/*` | Start, update, complete assessments |
| **Report** | `/report/*` | Generate AI reports with Gemini |
| **Analytics** | `/analytics/*` | Dashboard metrics & insights |

## 🛠️ **Prerequisites**

- AWS CLI configured
- SAM CLI installed
- Google Gemini API key

## 📋 **Deployment Steps**

1. **Install AWS CLI & SAM**
   ```bash
   # Install AWS CLI
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip && sudo ./aws/install
   
   # Install SAM CLI
   pip install aws-sam-cli
   
   # Configure AWS
   aws configure
   ```

2. **Deploy to AWS**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh prod
   ```

3. **Test API**
   ```bash
   # The deployment script will output your API URL
   curl https://[YOUR-API-URL]/prod/auth/user?userId=test
   ```

## 🏗️ **Architecture**

```
React Frontend → API Gateway → Lambda Functions → DynamoDB
                                      ↓
                               Google Gemini AI
```

## 💰 **Cost Estimate**

- **1K users/month**: ~$5
- **10K users/month**: ~$25
- **100K users/month**: ~$150

## 📊 **Features**

- ✅ **28 Assessment Types** (anxiety, OCD, mindfulness, etc.)
- ✅ **AI-Powered Reports** with Google Gemini
- ✅ **Real-time Analytics** dashboard
- ✅ **Serverless Auto-scaling** 
- ✅ **Pay-per-use Pricing**

## 🔍 **Testing**

```bash
# Local testing
sam local start-api

# Test endpoints
curl http://localhost:3000/auth/register -d '{"email":"test@example.com"}'
```

---

**🎉 Your serverless therapy app is ready to scale! 🌟**
