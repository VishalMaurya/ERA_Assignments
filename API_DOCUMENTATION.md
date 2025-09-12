# 📡 **API Documentation**
## Therapy App Lambda Functions

---

## 🔗 **Base URL**
```
https://[your-api-gateway-url]/prod
```

---

## 🔐 **Authentication API**

### **Register User**
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",           // Optional
  "preferences": {
    "theme": "light",                    // "light" | "dark"
    "notifications": true,               // boolean
    "dataRetention": 365                 // days
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "user_1699123456_abc123",
    "email": "user@example.com",
    "createdAt": "2024-01-01T00:00:00.000Z",
    "preferences": {
      "theme": "light",
      "notifications": true,
      "dataRetention": 365
    },
    "stats": {
      "totalAssessments": 0,
      "completedAssessments": 0,
      "totalTimeSpent": 0
    }
  },
  "message": "User registered successfully",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### **User Login**
```http
POST /auth/login
```

**Request Body:**
```json
{
  "userId": "user_1699123456_abc123"
}
```

### **Get User Profile**
```http
GET /auth/user?userId=user_1699123456_abc123
```

### **Update User Profile**
```http
PUT /auth/user
```

**Request Body:**
```json
{
  "userId": "user_1699123456_abc123",
  "preferences": {
    "theme": "dark"
  },
  "stats": {
    "totalTimeSpent": 150
  }
}
```

---

## 📝 **Assessment API**

### **Start Assessment**
```http
POST /assessment/start
```

**Request Body:**
```json
{
  "userId": "user_1699123456_abc123",
  "type": "anxiety"                      // See assessment types below
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "assessment_1699123456_def456",
    "userId": "user_1699123456_abc123",
    "type": "anxiety",
    "questions": [
      {
        "id": "anxiety_1",
        "type": "scale",
        "text": "How much does anxiety affect your daily life?",
        "environment": "ocean",
        "scaleRange": [1, 10],
        "scaleLabels": ["Not at all", "Significantly"],
        "therapyMapping": ["anxiety"]
      }
    ],
    "responses": [],
    "currentQuestionIndex": 0,
    "isCompleted": false,
    "startedAt": "2024-01-01T00:00:00.000Z",
    "skippedQuestions": [],
    "totalTimeSpent": 0
  },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### **Update Assessment**
```http
PUT /assessment/{assessmentId}
```

**Request Body:**
```json
{
  "userId": "user_1699123456_abc123",
  "response": {
    "questionId": "anxiety_1",
    "answer": 7,
    "answeredAt": "2024-01-01T00:01:00.000Z",
    "mood": "anxious",
    "timeSpent": 30
  },
  "currentQuestionIndex": 1,
  "timeSpent": 30
}
```

### **Complete Assessment**
```http
POST /assessment/{assessmentId}/complete
```

**Request Body:**
```json
{
  "userId": "user_1699123456_abc123"
}
```

### **Get Assessment**
```http
GET /assessment/{assessmentId}?userId=user_1699123456_abc123
```

---

## 📊 **Report API**

### **Generate Report**
```http
POST /report/generate
```

**Request Body:**
```json
{
  "userId": "user_1699123456_abc123",
  "assessmentId": "assessment_1699123456_def456"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "report_1699123456_ghi789",
    "assessmentId": "assessment_1699123456_def456",
    "userId": "user_1699123456_abc123",
    "summary": "Based on your anxiety assessment, you've shown great self-awareness...",
    "patterns": ["Self-reflection", "Awareness of symptoms", "Seeking help"],
    "severityLevel": "moderate",
    "recommendations": [
      {
        "therapyType": "anxiety",
        "priority": "primary",
        "confidence": 0.8,
        "reasoning": ["Based on responses showing moderate impact", "Evidence-based approach"],
        "suggestedExercises": ["mindful_breathing", "daily_reflection"],
        "estimatedDuration": "6-8 weeks",
        "successPredictors": ["Regular practice", "Self-awareness"],
        "potentialBarriers": ["Time constraints", "Initial resistance"]
      }
    ],
    "insights": [
      "Your responses indicate good self-awareness about your mental health.",
      "The fact that you completed this assessment shows commitment to growth."
    ],
    "nextSteps": [
      "Start with daily mindfulness practices for 5-10 minutes",
      "Consider keeping a mood journal to track patterns"
    ],
    "generatedAt": "2024-01-01T00:05:00.000Z",
    "generationTimeMs": 1200,
    "aiModel": "gemini-2.0-flash"
  },
  "message": "Report generated successfully",
  "timestamp": "2024-01-01T00:05:00.000Z"
}
```

### **Get Report**
```http
GET /report/{reportId}?userId=user_1699123456_abc123
```

### **Get User Reports**
```http
GET /reports?userId=user_1699123456_abc123
```

---

## 📈 **Analytics API**

### **Dashboard Analytics**
```http
GET /analytics/dashboard?userId=user_1699123456_abc123
```

**Response:**
```json
{
  "success": true,
  "data": {
    "totalAssessments": 5,
    "totalTimeSpent": 150,
    "averageSessionTime": 30,
    "completionRate": 80,
    "totalReports": 3,
    "thisMonthAssessments": 2,
    "improvementTrend": "improving",
    "typeDistribution": {
      "anxiety": 2,
      "mindfulness": 1,
      "sleep": 1,
      "self-compassion": 1
    },
    "lastAssessmentDate": "2024-01-01",
    "nextRecommendedAssessment": "emotion-regulation"
  },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### **Progress Analytics**
```http
GET /analytics/progress?userId=user_1699123456_abc123
```

**Response:**
```json
{
  "success": true,
  "data": {
    "progressTimeline": [
      {
        "date": "2024-01-01",
        "assessmentType": "anxiety",
        "severityLevel": "moderate",
        "insightsCount": 3,
        "recommendationsCount": 2
      }
    ],
    "wellbeingTrend": [
      {
        "date": "2024-01-01",
        "score": 6.5,
        "assessmentType": "anxiety"
      }
    ],
    "therapyEffectiveness": {
      "anxiety": {
        "count": 2,
        "effectiveness": 0.85
      }
    },
    "milestoneAchievements": [
      {
        "title": "First Assessment Completed",
        "description": "Took the first step in your mental health journey",
        "date": "2024-01-01",
        "icon": "🎯"
      }
    ]
  },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

---

## 📋 **Assessment Types**

| **Type** | **Description** | **Focus Area** |
|----------|-----------------|----------------|
| `anxiety` | Anxiety and worry patterns | Anxiety disorders |
| `ocd` | Obsessive-compulsive patterns | OCD symptoms |
| `anger` | Anger management | Emotional regulation |
| `mindfulness` | Present-moment awareness | Mindfulness practices |
| `sleep` | Sleep quality and patterns | Sleep disorders |
| `self-compassion` | Self-kindness and acceptance | Self-relationship |
| `trauma` | Trauma and PTSD symptoms | Trauma recovery |
| `general` | Overall mental wellbeing | General assessment |
| `behavioral-activation` | Activity and mood | Depression |
| `habit-reversal` | Habit change | Behavioral patterns |
| `problem-solving` | Problem-solving skills | Cognitive skills |
| `acceptance-commitment` | Acceptance and values | ACT therapy |
| `mindful-cognitive` | Mindful cognitive therapy | CBT + Mindfulness |
| `emotion-regulation` | Emotional management | DBT skills |
| `interpersonal` | Relationship skills | Social connections |
| `positive-psychology` | Strengths and positivity | Positive mental health |
| `strengths` | Personal strengths | Character strengths |
| `relaxation` | Relaxation techniques | Stress management |
| `breathing` | Breathing exercises | Anxiety/stress |
| `exercise` | Physical activity | Physical wellness |
| `nutrition` | Eating patterns | Nutritional wellness |
| `schema` | Core beliefs | Schema therapy |
| `narrative` | Life story | Narrative therapy |
| `motivation` | Motivation and goals | Motivational enhancement |
| `solution-focused` | Solution-oriented | Solution-focused therapy |

---

## 🔧 **Request/Response Format**

### **Standard Success Response:**
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation completed successfully",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### **Standard Error Response:**
```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

---

## 📊 **HTTP Status Codes**

| **Code** | **Meaning** | **Usage** |
|----------|-------------|-----------|
| `200` | Success | Request completed successfully |
| `400` | Bad Request | Invalid request body or parameters |
| `404` | Not Found | Resource not found |
| `409` | Conflict | Resource already exists |
| `500` | Internal Server Error | Unexpected server error |

---

## 🧪 **Testing with cURL**

### **Complete Flow Example:**
```bash
# Set your API URL
API_URL="https://your-api-gateway-url/prod"

# 1. Register user
USER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}')

# Extract user ID
USER_ID=$(echo $USER_RESPONSE | jq -r '.data.id')

# 2. Start assessment
ASSESSMENT_RESPONSE=$(curl -s -X POST "$API_URL/assessment/start" \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"$USER_ID\",\"type\":\"anxiety\"}")

# Extract assessment ID  
ASSESSMENT_ID=$(echo $ASSESSMENT_RESPONSE | jq -r '.data.id')

# 3. Update assessment with response
curl -X PUT "$API_URL/assessment/$ASSESSMENT_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"userId\":\"$USER_ID\",
    \"response\":{
      \"questionId\":\"anxiety_1\",
      \"answer\":7,
      \"answeredAt\":\"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)\"
    },
    \"currentQuestionIndex\":1,
    \"timeSpent\":30
  }"

# 4. Complete assessment
curl -X POST "$API_URL/assessment/$ASSESSMENT_ID/complete" \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"$USER_ID\"}"

# 5. Generate report
REPORT_RESPONSE=$(curl -s -X POST "$API_URL/report/generate" \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"$USER_ID\",\"assessmentId\":\"$ASSESSMENT_ID\"}")

# 6. Get analytics
curl "$API_URL/analytics/dashboard?userId=$USER_ID"
```

---

## 🔒 **Security Notes**

- All endpoints use HTTPS
- CORS is enabled for web clients
- No authentication required (session-based)
- User IDs are not guessable
- API keys are server-side only
- Input validation on all endpoints

---

**📡 Your API is ready to power therapy applications! 🌟**
