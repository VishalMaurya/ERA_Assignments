import json
import os
import time

# Using direct HTTP requests to Gemini API - no library dependencies needed!
import urllib.request
import urllib.parse


def lambda_handler(event, context):
    """
    Simple Therapy Assessment Lambda Function
    
    Endpoints:
    1. GET / - Home page with API documentation
    2. GET /assessment - Returns therapy assessment form with prefilled data
    3. POST /assessment - Processes assessment and returns AI recommendations
    """
    
    # Extract HTTP method and path (support both API Gateway and Lambda Function URL)
    if 'requestContext' in event and 'http' in event['requestContext']:
        # Lambda Function URL format
        http_method = event['requestContext']['http']['method']
        path = event.get('rawPath', '/')
        print(f"🔗 Lambda Function URL detected: {http_method} {path}")
    else:
        # API Gateway format
        http_method = event.get('httpMethod', '')
        path = event.get('path', '/')
        print(f"🌐 API Gateway detected: {http_method} {path}")
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        'Content-Type': 'application/json'
    }
    
    try:
        # Handle CORS preflight
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Route 1: Home page - Show API documentation
        if http_method == 'GET' and path == '/':
            response_data = get_home_page()
            
        # Route 2: GET assessment form
        elif http_method == 'GET' and path == '/assessment':
            response_data = get_assessment_form()
            
        # Route 3: POST assessment for AI recommendations
        elif http_method == 'POST' and path == '/assessment':
            # Handle body for both API Gateway and Function URL
            raw_body = event.get('body', '{}')
            if event.get('isBase64Encoded', False):
                import base64
                raw_body = base64.b64decode(raw_body).decode('utf-8')
            body = json.loads(raw_body)
            response_data = generate_ai_recommendations(body)
            
        # Route 4: Web UI - Interactive HTML interface
        elif http_method == 'GET' and path == '/UI':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': get_web_ui()
            }
            
        else:
            response_data = {
                'success': False,
                'error': 'Route not found',
                'available_endpoints': [
                    'GET / - API documentation',
                    'GET /assessment - Get assessment form',
                    'POST /assessment - Submit assessment for AI analysis',
                    'GET /UI - Interactive web interface'
                ]
            }
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps(response_data)
            }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data, indent=2)
        }
        
    except Exception as e:
        error_response = {
            'success': False,
            'error': str(e),
            'timestamp': time.time()
        }
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(error_response)
        }


def get_home_page():
    """Returns API documentation and usage examples"""
    return {
        'success': True,
        'api_title': '🧠 Therapy Assessment Demo API',
        'description': 'Simple Python Lambda for therapy assessment with AI recommendations using Google Gemini',
        'version': '1.0.0',
        'endpoints': {
            'get_assessment': {
                'method': 'GET',
                'path': '/assessment',
                'description': 'Get therapy assessment form with prefilled sample data',
                'response': 'JSON form with assessment questions and sample answers',
                'example_curl': 'curl -X GET https://your-api-url/assessment'
            },
            'submit_assessment': {
                'method': 'POST',
                'path': '/assessment',
                'description': 'Submit assessment data and get AI-powered recommendations from Gemini',
                'request_body': 'Assessment form data (same schema as GET response)',
                'response': 'AI recommendations and insights',
                'example_curl': '''curl -X POST https://your-api-url/assessment \\
  -H "Content-Type: application/json" \\
  -d '{
    "personal_info": {
      "name": "John Doe",
      "age": 28
    },
    "responses": {
      "anxiety_level": "Often",
      "mood_description": "Feeling overwhelmed lately"
    }
  }'
                '''
            }
        },
        'usage_flow': [
            '1. GET /assessment - to retrieve the prefilled form',
            '2. Modify any values as needed',
            '3. POST /assessment - to submit and get AI recommendations'
        ],
        'environment_variables': {
            'GEMINI_API_KEY': 'Required - Your Google Gemini API key',
            'GEMINI_MODEL': f'Optional - Gemini model to use (default: {os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")})'
        },
        'timestamp': time.time()
    }


def get_assessment_form():
    """Returns therapy assessment form with prefilled sample data"""
    return {
        'success': True,
        'form_title': 'Psychological Therapy Assessment',
        'form_description': 'Complete this assessment to receive personalized therapy recommendations powered by Google Gemini AI',
        'personal_info': {
            'name': 'John Doe',
            'age': 28,
            'email': 'john.doe@example.com',
            'occupation': 'Software Developer',
            'location': 'San Francisco, CA'
        },
        'assessment_questions': [
            {
                'id': 'anxiety_level',
                'question': 'How often do you feel anxious or worried?',
                'type': 'multiple_choice',
                'options': ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
            },
            {
                'id': 'sleep_quality',
                'question': 'How would you rate your sleep quality? (1-10)',
                'type': 'scale',
                'scale_info': '1 = Very Poor, 10 = Excellent'
            },
            {
                'id': 'stress_sources',
                'question': 'What are your main sources of stress? (Select multiple)',
                'type': 'multiple_select',
                'options': ['Work', 'Relationships', 'Financial', 'Health', 'Family', 'Other']
            },
            {
                'id': 'mood_description',
                'question': 'Describe your typical mood over the past month',
                'type': 'text'
            },
            {
                'id': 'coping_strategies',
                'question': 'What coping strategies have you tried? (Select multiple)',
                'type': 'multiple_select',
                'options': ['Exercise', 'Meditation', 'Therapy', 'Medication', 'Talking to friends', 'None']
            },
            {
                'id': 'therapy_goals',
                'question': 'What would you like to achieve through therapy?',
                'type': 'text'
            }
        ],
        'prefilled_responses': {
            'anxiety_level': 'Often',
            'sleep_quality': 4,
            'stress_sources': ['Work', 'Financial'],
            'mood_description': 'I have been feeling overwhelmed and anxious most days, especially about work deadlines and financial responsibilities. Sometimes I feel like I cannot catch a break.',
            'coping_strategies': ['Exercise', 'Talking to friends'],
            'therapy_goals': 'I want to learn better stress management techniques and reduce my anxiety levels so I can feel more balanced and enjoy life again.'
        },
        'responses': {
            'anxiety_level': 'Often',
            'sleep_quality': 4,
            'stress_sources': ['Work', 'Financial'],
            'mood_description': 'I have been feeling overwhelmed and anxious most days, especially about work deadlines and financial responsibilities. Sometimes I feel like I cannot catch a break.',
            'coping_strategies': ['Exercise', 'Talking to friends'],
            'therapy_goals': 'I want to learn better stress management techniques and reduce my anxiety levels so I can feel more balanced and enjoy life again.'
        },
        'instructions': {
            'how_to_submit': 'Send this entire object (or modified version) to POST /assessment',
            'note': 'You can modify any values in the "responses" section before submitting',
            'required_fields': ['personal_info', 'responses']
        },
        'timestamp': time.time()
    }


def generate_ai_recommendations(assessment_data):
    """Process assessment data and generate AI recommendations using Gemini"""
    
    # Validate input data
    if not assessment_data.get('personal_info') or not assessment_data.get('responses'):
        return {
            'success': False,
            'error': 'Missing required fields: personal_info and responses',
            'required_format': {
                'personal_info': {'name': 'string', 'age': 'number'},
                'responses': {'anxiety_level': 'string', 'mood_description': 'string'}
            }
        }
    
    personal_info = assessment_data['personal_info']
    responses = assessment_data['responses']
    
    # Try to generate AI recommendations
    try:
        ai_recommendations = get_gemini_recommendations(personal_info, responses)
        
        return {
            'success': True,
            'patient_info': {
                'name': personal_info.get('name', 'Anonymous'),
                'assessment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            },
            'ai_analysis': ai_recommendations,
            'metadata': {
                'processing_time_ms': ai_recommendations.get('processing_time_ms', 0),
                'ai_model': os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash'),
                'generated_at': time.time()
            }
        }
        
    except Exception as e:
        # Fallback to predefined recommendations if AI fails
        fallback_recommendations = get_fallback_recommendations(personal_info, responses)
        
        return {
            'success': True,
            'patient_info': {
                'name': personal_info.get('name', 'Anonymous'),
                'assessment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            },
            'ai_analysis': fallback_recommendations,
            'metadata': {
                'processing_time_ms': 50,
                'ai_model': 'fallback-mode',
                'generated_at': time.time(),
                'note': f'AI service unavailable, using fallback recommendations. Error: {str(e)}'
            }
        }


def get_gemini_recommendations(personal_info, responses):
    """Generate recommendations using Google Gemini AI via direct REST API"""
    
    # Get API key from environment
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise Exception('GEMINI_API_KEY environment variable not set')
    
    # Get model name from environment or use default
    model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')
    
    # Build prompt for AI
    prompt = build_therapy_prompt(personal_info, responses)
    
    # Prepare request data
    request_data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    # Make HTTP request to Gemini API
    start_time = time.time()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(request_data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            processing_time = int((time.time() - start_time) * 1000)
            
            # Extract text from response
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                ai_text = response_data['candidates'][0]['content']['parts'][0]['text']
                
                # Parse AI response
                try:
                    # Try to extract JSON from response
                    json_start = ai_text.find('{')
                    json_end = ai_text.rfind('}') + 1
                    
                    if json_start != -1 and json_end != 0:
                        json_str = ai_text[json_start:json_end]
                        recommendations = json.loads(json_str)
                        recommendations['processing_time_ms'] = processing_time
                        recommendations['raw_ai_response'] = ai_text
                        return recommendations
                    else:
                        # If no JSON found, create structured response from text
                        return parse_text_response(ai_text, processing_time)
                        
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    return parse_text_response(ai_text, processing_time)
            else:
                raise Exception('No response from Gemini API')
                
    except urllib.error.HTTPError as e:
        error_details = e.read().decode('utf-8')
        raise Exception(f'Gemini API error: {e.code} - {error_details}')
    except Exception as e:
        raise Exception(f'Failed to call Gemini API: {str(e)}')


def build_therapy_prompt(personal_info, responses):
    """Build comprehensive prompt for Gemini AI"""
    
    # Format responses for prompt
    response_text = ""
    for key, value in responses.items():
        if isinstance(value, list):
            response_text += f"{key}: {', '.join(value)}\n"
        else:
            response_text += f"{key}: {value}\n"
    
    prompt = f"""
You are a compassionate and experienced AI therapy assistant. Based on the following psychological assessment, provide personalized therapy recommendations and insights.

PATIENT INFORMATION:
Name: {personal_info.get('name', 'Anonymous')}
Age: {personal_info.get('age', 'Not specified')}
Occupation: {personal_info.get('occupation', 'Not specified')}

ASSESSMENT RESPONSES:
{response_text}

Please provide your analysis in the following JSON format:

{{
  "summary": "A warm, empathetic 2-3 sentence summary of the person's current mental health state",
  "key_insights": [
    "Important insight about their mental health patterns",
    "Another significant observation",
    "Third key insight about their condition"
  ],
  "recommended_therapies": [
    {{
      "therapy_name": "Cognitive Behavioral Therapy (CBT)",
      "suitability_reason": "Why this therapy is specifically recommended for this person",
      "description": "Brief explanation of what this therapy involves",
      "expected_outcomes": "What benefits they can expect"
    }},
    {{
      "therapy_name": "Another recommended therapy",
      "suitability_reason": "Specific reason for recommendation",
      "description": "What this therapy involves",
      "expected_outcomes": "Expected benefits"
    }}
  ],
  "immediate_coping_strategies": [
    "Specific actionable strategy they can start today",
    "Another practical coping technique",
    "Third immediate strategy"
  ],
  "lifestyle_recommendations": [
    "Lifestyle change recommendation",
    "Another lifestyle suggestion",
    "Third lifestyle improvement"
  ],
  "progress_tracking": [
    "How to measure improvement",
    "Another metric to track",
    "Third progress indicator"
  ],
  "warning_signs": [
    "Red flag to watch out for",
    "Another concerning sign to monitor"
  ],
  "support_resources": [
    "Specific resource recommendation",
    "Another helpful resource"
  ],
  "personal_strengths": [
    "Strength identified from their responses",
    "Another positive quality noted"
  ],
  "next_steps": [
    "Immediate next step to take",
    "Second recommended action",
    "Third step in their journey"
  ]
}}

IMPORTANT GUIDELINES:
- Be warm, empathetic, and encouraging
- Focus on evidence-based therapy approaches
- Provide specific, actionable recommendations
- Acknowledge their courage in seeking help
- Maintain a hopeful and supportive tone
- Avoid making clinical diagnoses
- Consider their specific situation and responses
"""
    
    return prompt


def parse_text_response(ai_text, processing_time):
    """Parse AI text response when JSON extraction fails"""
    return {
        "summary": "Thank you for completing this assessment. Your responses show self-awareness and a willingness to seek support, which are important first steps.",
        "key_insights": [
            "You have shown courage by completing this assessment",
            "Your responses indicate awareness of your mental health needs",
            "You are taking positive steps toward wellbeing"
        ],
        "recommended_therapies": [
            {
                "therapy_name": "Cognitive Behavioral Therapy (CBT)",
                "suitability_reason": "Effective for anxiety and stress management",
                "description": "CBT helps identify and change negative thought patterns",
                "expected_outcomes": "Better emotional regulation and coping skills"
            }
        ],
        "immediate_coping_strategies": [
            "Practice deep breathing exercises for 5 minutes daily",
            "Keep a daily mood journal",
            "Engage in regular physical exercise"
        ],
        "lifestyle_recommendations": [
            "Maintain a consistent sleep schedule",
            "Limit caffeine and alcohol consumption",
            "Practice mindfulness or meditation"
        ],
        "progress_tracking": [
            "Daily mood ratings on a 1-10 scale",
            "Sleep quality and duration tracking",
            "Stress level monitoring"
        ],
        "warning_signs": [
            "Persistent thoughts of self-harm",
            "Inability to function in daily activities"
        ],
        "support_resources": [
            "Mental health crisis hotlines",
            "Local therapy providers",
            "Online mental health resources"
        ],
        "personal_strengths": [
            "Self-awareness and insight",
            "Willingness to seek help"
        ],
        "next_steps": [
            "Consider scheduling a consultation with a mental health professional",
            "Start implementing daily coping strategies",
            "Reach out to trusted friends or family for support"
        ],
        "processing_time_ms": processing_time,
        "raw_ai_response": ai_text
    }


def get_fallback_recommendations(personal_info, responses):
    """Provide fallback recommendations when AI is unavailable"""
    return {
        "summary": f"Thank you for completing this assessment, {personal_info.get('name', 'Anonymous')}. Based on your responses, you are taking important steps toward better mental health.",
        "key_insights": [
            "You have demonstrated self-awareness by completing this assessment",
            "Your willingness to seek support shows personal strength",
            "You are ready to take positive steps toward mental wellness"
        ],
        "recommended_therapies": [
            {
                "therapy_name": "Cognitive Behavioral Therapy (CBT)",
                "suitability_reason": "Widely effective for anxiety, depression, and stress management",
                "description": "CBT focuses on identifying and changing negative thought patterns and behaviors",
                "expected_outcomes": "Improved mood, better coping skills, and reduced anxiety"
            },
            {
                "therapy_name": "Mindfulness-Based Stress Reduction (MBSR)",
                "suitability_reason": "Excellent for managing stress and improving overall wellbeing",
                "description": "MBSR combines mindfulness meditation and body awareness",
                "expected_outcomes": "Reduced stress, better emotional regulation, improved focus"
            }
        ],
        "immediate_coping_strategies": [
            "Practice deep breathing: 4 counts in, hold for 4, exhale for 6",
            "Try the 5-4-3-2-1 grounding technique when feeling overwhelmed",
            "Take short walks outside to clear your mind"
        ],
        "lifestyle_recommendations": [
            "Establish a regular sleep routine (7-9 hours per night)",
            "Engage in physical activity for at least 30 minutes daily",
            "Limit screen time before bedtime"
        ],
        "progress_tracking": [
            "Keep a daily mood journal with ratings from 1-10",
            "Track sleep quality and duration",
            "Monitor stress levels throughout the day"
        ],
        "warning_signs": [
            "Thoughts of self-harm or suicide",
            "Inability to perform daily activities for several days"
        ],
        "support_resources": [
            "National Suicide Prevention Lifeline: 988",
            "Crisis Text Line: Text HOME to 741741",
            "Psychology Today therapist finder"
        ],
        "personal_strengths": [
            "Self-awareness and willingness to seek help",
            "Ability to complete self-reflection exercises"
        ],
        "next_steps": [
            "Research local mental health professionals",
            "Start implementing one coping strategy today",
            "Share your mental health journey with a trusted friend or family member"
        ],
        "processing_time_ms": 50
    }


def get_web_ui():
    """Returns HTML web interface for therapy assessment"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Therapy Assessment</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .form-section {
            padding: 30px;
        }
        
        .section-title {
            color: #2c3e50;
            font-size: 1.4em;
            margin-bottom: 20px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ecf0f1;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-group textarea {
            height: 100px;
            resize: vertical;
        }
        
        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .checkbox-item input[type="checkbox"] {
            width: auto;
        }
        
        .submit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            width: 100%;
            margin-top: 20px;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
        }
        
        .submit-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
            font-size: 18px;
        }
        
        .results {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .results h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .insight-item {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
            border-left: 3px solid #27ae60;
        }
        
        .therapy-item {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
            border-left: 3px solid #3498db;
        }
        
        .strategy-item {
            background: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 6px;
            border-left: 3px solid #e74c3c;
        }
        
        .error {
            background: #ffe6e6;
            color: #c0392b;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #e74c3c;
            margin-top: 20px;
        }
        
        @media (max-width: 600px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .form-section {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Therapy Assessment</h1>
            <p>AI-Powered Mental Health Recommendations</p>
        </div>
        
        <div class="form-section">
            <form id="assessmentForm">
                <div class="section-title">Personal Information</div>
                
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" id="name" name="name" required>
                </div>
                
                <div class="form-group">
                    <label for="age">Age</label>
                    <input type="number" id="age" name="age" min="18" max="100" required>
                </div>
                
                <div class="form-group">
                    <label for="occupation">Occupation (Optional)</label>
                    <input type="text" id="occupation" name="occupation">
                </div>
                
                <div class="section-title">Assessment Questions</div>
                
                <div class="form-group">
                    <label for="anxiety_level">How often do you experience anxiety?</label>
                    <select id="anxiety_level" name="anxiety_level" required>
                        <option value="">Select...</option>
                        <option value="Never">Never</option>
                        <option value="Rarely">Rarely</option>
                        <option value="Sometimes">Sometimes</option>
                        <option value="Often">Often</option>
                        <option value="Always">Always</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="sleep_quality">Sleep Quality (1-10, where 10 is excellent)</label>
                    <input type="range" id="sleep_quality" name="sleep_quality" min="1" max="10" value="5">
                    <span id="sleep_value">5</span>
                </div>
                
                <div class="form-group">
                    <label>What are your main sources of stress? (Check all that apply)</label>
                    <div class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" id="stress_work" name="stress_sources" value="Work">
                            <label for="stress_work">Work</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="stress_family" name="stress_sources" value="Family">
                            <label for="stress_family">Family</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="stress_financial" name="stress_sources" value="Financial">
                            <label for="stress_financial">Financial</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="stress_health" name="stress_sources" value="Health">
                            <label for="stress_health">Health</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="stress_relationships" name="stress_sources" value="Relationships">
                            <label for="stress_relationships">Relationships</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="stress_other" name="stress_sources" value="Other">
                            <label for="stress_other">Other</label>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="mood_description">How would you describe your current mood and mental state?</label>
                    <textarea id="mood_description" name="mood_description" placeholder="Please describe how you've been feeling lately..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="social_support">How would you rate your social support system?</label>
                    <select id="social_support" name="social_support" required>
                        <option value="">Select...</option>
                        <option value="None">None</option>
                        <option value="Limited">Limited</option>
                        <option value="Moderate">Moderate</option>
                        <option value="Strong">Strong</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="exercise_frequency">How often do you exercise?</label>
                    <select id="exercise_frequency" name="exercise_frequency" required>
                        <option value="">Select...</option>
                        <option value="Daily">Daily</option>
                        <option value="Weekly">Weekly</option>
                        <option value="Rarely">Rarely</option>
                        <option value="Never">Never</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="therapy_experience">Previous therapy experience</label>
                    <textarea id="therapy_experience" name="therapy_experience" placeholder="Have you tried therapy before? What was your experience?"></textarea>
                </div>
                
                <button type="submit" class="submit-btn" id="submitBtn">
                    Get AI Recommendations
                </button>
            </form>
            
            <div id="loading" class="loading" style="display: none;">
                🧠 Analyzing your responses with AI...
            </div>
            
            <div id="results" class="results" style="display: none;"></div>
            <div id="error" class="error" style="display: none;"></div>
        </div>
    </div>

    <script>
        // Update sleep quality display
        document.getElementById('sleep_quality').addEventListener('input', function() {
            document.getElementById('sleep_value').textContent = this.value;
        });

        // Form submission
        document.getElementById('assessmentForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const error = document.getElementById('error');
            
            // Hide previous results/errors
            results.style.display = 'none';
            error.style.display = 'none';
            
            // Show loading
            loading.style.display = 'block';
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            
            try {
                // Collect form data
                const formData = new FormData(e.target);
                
                // Validate required fields
                const name = formData.get('name');
                const age = formData.get('age');
                const anxietyLevel = formData.get('anxiety_level');
                const moodDescription = formData.get('mood_description');
                const socialSupport = formData.get('social_support');
                const exerciseFreq = formData.get('exercise_frequency');
                
                if (!name || !age || !anxietyLevel || !moodDescription || !socialSupport || !exerciseFreq) {
                    throw new Error('Please fill in all required fields');
                }
                
                if (isNaN(age) || age < 18 || age > 100) {
                    throw new Error('Please enter a valid age between 18 and 100');
                }
                
                // Get stress sources
                const stressSources = [];
                document.querySelectorAll('input[name="stress_sources"]:checked').forEach(checkbox => {
                    stressSources.push(checkbox.value);
                });
                
                // Add occupation if provided
                const occupation = formData.get('occupation');
                const personalInfo = {
                    name: name,
                    age: parseInt(age)
                };
                if (occupation && occupation.trim()) {
                    personalInfo.occupation = occupation.trim();
                }
                
                // Build request data
                const requestData = {
                    personal_info: personalInfo,
                    responses: {
                        anxiety_level: anxietyLevel,
                        sleep_quality: parseInt(formData.get('sleep_quality')),
                        stress_sources: stressSources,
                        mood_description: moodDescription,
                        social_support: socialSupport,
                        exercise_frequency: exerciseFreq,
                        therapy_experience: formData.get('therapy_experience') || '',
                        primary_concerns: stressSources.length > 0 ? stressSources : ['General wellness']
                    }
                };
                
                // Make API call - use current domain + /assessment
                const apiUrl = window.location.origin + '/assessment';
                console.log('🚀 Sending request to:', apiUrl);
                console.log('📋 Request data:', requestData);
                
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });
                
                console.log('📡 Response status:', response.status);
                console.log('📡 Response headers:', response.headers);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                console.log('📊 Response data:', data);
                
                if (data.success) {
                    console.log('✅ Success! Calling displayResults...');
                    displayResults(data);
                } else {
                    console.log('❌ API returned success=false');
                    throw new Error(data.error || 'Unknown error occurred');
                }
                
            } catch (err) {
                console.error('Error:', err);
                console.error('Request data was:', requestData);
                
                let errorMessage = 'Error: ' + err.message;
                if (err.message.includes('fetch')) {
                    errorMessage += ' (Check if API endpoint is accessible)';
                } else if (err.message.includes('pattern')) {
                    errorMessage += ' (Invalid data format - check form inputs)';
                }
                
                error.textContent = errorMessage;
                error.style.display = 'block';
            } finally {
                loading.style.display = 'none';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Get AI Recommendations';
            }
        });
        
        function displayResults(data) {
            console.log('🎯 displayResults called with data:', data);
            
            const results = document.getElementById('results');
            console.log('📋 Results element:', results);
            
            if (!results) {
                console.error('❌ Results element not found!');
                return;
            }
            
            const analysis = data.ai_analysis;
            console.log('🧠 AI Analysis:', analysis);
            
            if (!analysis) {
                console.error('❌ No ai_analysis in response data!');
                return;
            }
            
            let html = `
                <h3>🎯 Assessment Results for ${data.patient_info.name}</h3>
                <p><strong>Assessment Date:</strong> ${data.patient_info.assessment_date}</p>
                
                <h4>📋 Summary</h4>
                <p>${analysis.summary}</p>
                
                <h4>💡 Key Insights</h4>
            `;
            
            analysis.key_insights.forEach(insight => {
                html += `<div class="insight-item">${insight}</div>`;
            });
            
            html += `<h4>🏥 Recommended Therapies</h4>`;
            analysis.recommended_therapies.forEach(therapy => {
                html += `
                    <div class="therapy-item">
                        <strong>${therapy.therapy_name}</strong><br>
                        <em>Why it fits:</em> ${therapy.suitability_reason}<br>
                        <em>Expected outcomes:</em> ${therapy.expected_outcomes}
                    </div>
                `;
            });
            
            html += `<h4>⚡ Immediate Coping Strategies</h4>`;
            analysis.immediate_coping_strategies.forEach(strategy => {
                html += `<div class="strategy-item">${strategy}</div>`;
            });
            
            if (analysis.progress_tracking) {
                html += `
                    <h4>📊 Progress Tracking</h4>
                    <div class="insight-item">
                        <strong>Metrics to monitor:</strong> ${analysis.progress_tracking.metrics_to_monitor.join(', ')}<br>
                        <strong>Check-in frequency:</strong> ${analysis.progress_tracking.check_in_frequency}
                    </div>
                `;
            }
            
            html += `
                <p><small>
                    <strong>AI Model:</strong> ${data.metadata.ai_model} | 
                    <strong>Processing Time:</strong> ${data.metadata.processing_time_ms}ms
                </small></p>
            `;
            
            console.log('📝 Setting HTML content...');
            results.innerHTML = html;
            results.style.display = 'block';
            
            console.log('✅ Results displayed successfully!');
            console.log('📊 Results element after update:', results);
            
            // Scroll to results
            results.scrollIntoView({ behavior: 'smooth' });
            console.log('🎯 Scrolled to results section');
        }
    </script>
</body>
</html>'''


# For local testing
if __name__ == "__main__":
    # Test the function locally
    
    # Test 1: Home page
    print("=== Testing Home Page ===")
    event1 = {"httpMethod": "GET", "path": "/"}
    result1 = lambda_handler(event1, {})
    print(json.dumps(json.loads(result1['body']), indent=2))
    
    print("\n=== Testing Assessment Form ===")
    event2 = {"httpMethod": "GET", "path": "/assessment"}
    result2 = lambda_handler(event2, {})
    print(json.dumps(json.loads(result2['body']), indent=2))
    
    print("\n=== Testing Assessment Submission ===")
    test_data = {
        "personal_info": {"name": "Test User", "age": 30},
        "responses": {
            "anxiety_level": "Often",
            "mood_description": "Feeling stressed about work"
        }
    }
    event3 = {
        "httpMethod": "POST", 
        "path": "/assessment",
        "body": json.dumps(test_data)
    }
    result3 = lambda_handler(event3, {})
    print(json.dumps(json.loads(result3['body']), indent=2))
