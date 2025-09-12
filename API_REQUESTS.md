# 🚀 **API Requests - Quick Reference**

## **Base URL**
```
https://c7dicrh73vqm7bu3d2nzvdbgou0voyri.lambda-url.ap-south-1.on.aws
```

---

## **📋 Endpoints**

### **1. GET /** - Home Page
```bash
curl -X GET "https://c7dicrh73vqm7bu3d2nzvdbgou0voyri.lambda-url.ap-south-1.on.aws/"
```

### **2. GET /assessment** - Get Form
```bash
curl -X GET "https://c7dicrh73vqm7bu3d2nzvdbgou0voyri.lambda-url.ap-south-1.on.aws/assessment"
```

### **3. GET /UI** - Web Interface
```bash
# Open in browser or use curl to get HTML
curl -X GET "https://c7dicrh73vqm7bu3d2nzvdbgou0voyri.lambda-url.ap-south-1.on.aws/UI"

# Or just visit in browser:
# https://c7dicrh73vqm7bu3d2nzvdbgou0voyri.lambda-url.ap-south-1.on.aws/UI
```

### **4. POST /assessment** - Submit Assessment
```bash
curl -X POST "https://c7dicrh73vqm7bu3d2nzvdbgou0voyri.lambda-url.ap-south-1.on.aws/assessment" \
  -H "Content-Type: application/json" \
  -d '{
    "personal_info": {
      "name": "John Doe",
      "age": 28,
      "occupation": "Software Developer"
    },
    "responses": {
      "anxiety_level": "Often",
      "sleep_quality": 4,
      "stress_sources": ["Work", "Financial"],
      "mood_description": "Feeling overwhelmed lately",
      "social_support": "Limited",
      "exercise_frequency": "Rarely",
      "therapy_experience": "Never tried therapy before",
      "primary_concerns": ["Anxiety", "Work-life balance"]
    }
  }'
```

---

## **🧪 Quick Tests**

### **Simple POST Test**
```bash
curl -X POST "https://c7dicrh73vqm7bu3d2nzvdbgou0voyri.lambda-url.ap-south-1.on.aws/assessment" \
  -H "Content-Type: application/json" \
  -d '{
    "personal_info": {"name": "Test", "age": 30},
    "responses": {
      "anxiety_level": "Sometimes",
      "mood_description": "Testing the API"
    }
  }'
```

### **Test All Endpoints**
```bash
URL="https://c7dicrh73vqm7bu3d2nzvdbgou0voyri.lambda-url.ap-south-1.on.aws"

echo "🏠 Testing Home:"
curl -X GET "$URL/"

echo -e "\n\n📋 Testing Form:"
curl -X GET "$URL/assessment"

echo -e "\n\n🤖 Testing AI Analysis:"
curl -X POST "$URL/assessment" \
  -H "Content-Type: application/json" \
  -d '{"personal_info":{"name":"QuickTest","age":25},"responses":{"anxiety_level":"Often","mood_description":"Stressed about work"}}'
```

---

## **📝 Request Schema**

### **POST /assessment Request Body:**
```json
{
  "personal_info": {
    "name": "string (required)",
    "age": "number (required)",
    "occupation": "string (optional)"
  },
  "responses": {
    "anxiety_level": "Never|Rarely|Sometimes|Often|Always",
    "sleep_quality": "number (1-10 scale)",
    "stress_sources": ["Work", "Family", "Financial", "Health"],
    "mood_description": "string",
    "social_support": "None|Limited|Moderate|Strong",
    "exercise_frequency": "Daily|Weekly|Rarely|Never",
    "therapy_experience": "string",
    "primary_concerns": ["array", "of", "concerns"]
  }
}
```

---

## **🔧 Environment Variables (Lambda)**
```bash
GEMINI_API_KEY="AIzaSyBCZNjWaPdcplHI4UlRXgjsJMjZHN021Vc"
GEMINI_MODEL="gemini-2.0-flash"  # Optional
```

**Available Models:**
- `gemini-2.0-flash` (default - fast)
- `gemini-1.5-pro` (comprehensive)  
- `gemini-1.5-flash` (balanced)

---

**🎯 Ready to test! Copy-paste any command above.**
