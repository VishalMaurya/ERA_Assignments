import json
import os
import time

# Try to import google.generativeai, handle gracefully if not available
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google.generativeai not available. Using fallback mode for local testing.")


def lambda_handler(event, context):
    """
    Simple Therapy Assessment Lambda Function
    
    Endpoints:
    1. GET / - Home page with API documentation
    2. GET /assessment - Returns therapy assessment form with prefilled data
    3. POST /assessment - Processes assessment and returns AI recommendations
    """
    
    # Extract HTTP method and path
    http_method = event.get('httpMethod', '')
    path = event.get('path', '/')
    
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
            body = json.loads(event.get('body', '{}'))
            response_data = generate_ai_recommendations(body)
            
        else:
            response_data = {
                'success': False,
                'error': 'Route not found',
                'available_endpoints': [
                    'GET / - API documentation',
                    'GET /assessment - Get assessment form',
                    'POST /assessment - Submit assessment for AI analysis'
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
        'description': 'Simple Python Lambda for therapy assessment with AI recommendations',
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
                'ai_model': 'google-gemini-2.0-flash',
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
    """Generate recommendations using Google Gemini AI"""
    
    # Check if Gemini is available
    if not GENAI_AVAILABLE:
        raise Exception('Google Generative AI library not available')
    
    # Configure Gemini API
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise Exception('GEMINI_API_KEY environment variable not set')
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Build prompt for AI
    prompt = build_therapy_prompt(personal_info, responses)
    
    # Generate content
    start_time = time.time()
    response = model.generate_content(prompt)
    processing_time = int((time.time() - start_time) * 1000)
    
    # Parse AI response
    try:
        # Try to extract JSON from response
        ai_text = response.text
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
        return parse_text_response(response.text, processing_time)


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
