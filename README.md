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

### AWS Lambda:
1. Zip the files: `zip -r therapy-lambda.zip lambda_function.py requirements.txt`
2. Upload to Lambda console
3. Set environment variables:
   - `GEMINI_API_KEY=your_api_key`
   - `GEMINI_MODEL=gemini-2.0-flash` (optional)
4. Configure API Gateway triggers

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