import { GoogleGenerativeAI } from '@google/generative-ai';
import { AssessmentReport, Assessment, TherapyRecommendation } from '@/types';

export class GeminiService {
  private genAI: GoogleGenerativeAI | null = null;

  constructor(apiKey?: string) {
    if (apiKey) {
      if (!this.isValidApiKey(apiKey)) {
        throw new Error('Invalid API key format. Please check your Gemini API key.');
      }
      this.genAI = new GoogleGenerativeAI(apiKey);
    }
  }

  setApiKey(apiKey: string) {
    if (!this.isValidApiKey(apiKey)) {
      throw new Error('Invalid API key format. Please check your Gemini API key.');
    }
    this.genAI = new GoogleGenerativeAI(apiKey);
  }

  private isValidApiKey(apiKey: string): boolean {
    // Basic validation - Gemini API keys typically start with "AIza" and are ~40 characters
    return Boolean(apiKey) && 
           typeof apiKey === 'string' && 
           apiKey.length >= 30 && 
           apiKey.startsWith('AIza');
  }

  async generateAssessmentReport(assessment: Assessment): Promise<AssessmentReport> {
    if (!this.genAI) {
      throw new Error('Gemini AI API key not configured. Please enter your API key.');
    }

    const model = this.genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });

    const prompt = this.buildPrompt(assessment);
    
    try {
      const result = await model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();
      
      return this.parseAIResponse(text, assessment);
    } catch (error) {
      console.error('Error generating report:', error);
      
      // Provide more specific error messages
      if (error instanceof Error) {
        if (error.message.includes('API_KEY_INVALID')) {
          throw new Error('Invalid Gemini API key. Please check your API key and try again.');
        }
        if (error.message.includes('QUOTA_EXCEEDED')) {
          throw new Error('API quota exceeded. Please try again later or check your billing.');
        }
        if (error.message.includes('PERMISSION_DENIED')) {
          throw new Error('API access denied. Please verify your API key has proper permissions.');
        }
        if (error.message.includes('Network')) {
          throw new Error('Network error. Please check your internet connection and try again.');
        }
        if (error.message.includes('SAFETY')) {
          throw new Error('Content was blocked by safety filters. Please try rephrasing your responses.');
        }
        
        // Include the actual error message for debugging
        throw new Error(`Report generation failed: ${error.message}`);
      }
      
      throw new Error('Failed to generate assessment report. Please try again.');
    }
  }

  private buildPrompt(assessment: Assessment): string {
    const { type, responses } = assessment;
    const responseText = responses.map(r => 
      `Question ID: ${r.questionId}, Answer: ${r.answer}, Mood: ${r.mood || 'Not specified'}`
    ).join('\n');

    return `
You are a compassionate AI therapist assistant. Based on the following psychological assessment responses for ${type.toUpperCase()}, please generate a comprehensive, empathetic report.

Assessment Type: ${type.toUpperCase()}
User Responses:
${responseText}

Please provide a structured response in the following JSON format:

{
  "summary": "A warm, empathetic 2-3 sentence summary of the user's current state",
  "patterns": ["Pattern 1", "Pattern 2", "Pattern 3"],
  "severityLevel": "mild|moderate|high",
  "insights": ["Insight 1", "Insight 2", "Insight 3"],
  "recommendations": [
    {
      "type": "CBT|DBT|ACT|MBSR|ERP|HRT|Mindfulness|Exercise",
      "title": "Recommendation Title",
      "description": "Brief description of why this is helpful",
      "exercises": ["Exercise 1", "Exercise 2", "Exercise 3"],
      "resources": ["Resource 1", "Resource 2"],
      "priority": "high|medium|low"
    }
  ],
  "nextSteps": ["Step 1", "Step 2", "Step 3"]
}

Guidelines:
- Be supportive and non-judgmental
- Focus on evidence-based therapies appropriate for ${type}
- For anxiety: Emphasize CBT, ACT, MBSR
- For OCD: Emphasize ERP, HRT, ACT  
- For anger: Emphasize DBT, anger management, mindfulness
- For general wellbeing: Emphasize mindfulness, behavioral activation, self-care
- Provide practical, actionable recommendations
- Acknowledge the user's courage in taking this assessment
- Avoid clinical diagnosis language
- Keep the tone warm, hopeful, and empowering
    `;
  }

  private parseAIResponse(text: string, assessment: Assessment): AssessmentReport {
    try {
      // Extract JSON from the response (AI might include extra text)
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        throw new Error('No JSON found in AI response');
      }

      const parsed = JSON.parse(jsonMatch[0]);
      
      return {
        id: `report_${Date.now()}`,
        assessmentId: assessment.id,
        userId: assessment.userId,
        summary: parsed.summary || 'Thank you for completing this assessment.',
        patterns: parsed.patterns || [],
        severityLevel: parsed.severityLevel || 'mild',
        recommendations: parsed.recommendations || [],
        insights: parsed.insights || [],
        nextSteps: parsed.nextSteps || [],
        generatedAt: new Date(),
        rawAIResponse: text
      };
    } catch (error) {
      console.error('Error parsing AI response:', error);
      
      // Fallback report if parsing fails
      return {
        id: `report_${Date.now()}`,
        assessmentId: assessment.id,
        userId: assessment.userId,
        summary: 'Thank you for completing this assessment. We\'re processing your responses to provide personalized insights.',
        patterns: ['Responses recorded successfully'],
        severityLevel: 'mild',
        recommendations: this.getFallbackRecommendations(assessment.type),
        insights: ['Your responses show self-awareness and willingness to explore your mental health.'],
        nextSteps: ['Continue practicing self-reflection', 'Consider professional support if needed'],
        generatedAt: new Date(),
        rawAIResponse: text
      };
    }
  }

  private getFallbackRecommendations(type: string): TherapyRecommendation[] {
    const commonRecommendations: Record<string, TherapyRecommendation[]> = {
      anxiety: [
        {
          type: 'CBT',
          title: 'Cognitive Behavioral Techniques',
          description: 'Learn to identify and challenge anxious thoughts',
          exercises: ['Thought record keeping', 'Deep breathing exercises', 'Progressive muscle relaxation'],
          resources: ['CBT workbooks', 'Mindfulness apps'],
          priority: 'high'
        }
      ],
      ocd: [
        {
          type: 'ERP',
          title: 'Exposure and Response Prevention',
          description: 'Gradually face fears while resisting compulsions',
          exercises: ['Start with easier exposures', 'Delay compulsive behaviors', 'Track your progress'],
          resources: ['OCD support groups', 'ERP workbooks'],
          priority: 'high'
        }
      ],
      anger: [
        {
          type: 'DBT',
          title: 'Emotion Regulation Skills',
          description: 'Learn healthy ways to manage intense emotions',
          exercises: ['STOP technique', 'Opposite action', 'Distress tolerance skills'],
          resources: ['DBT skill books', 'Anger management classes'],
          priority: 'high'
        }
      ],
      general: [
        {
          type: 'Mindfulness',
          title: 'Mindfulness Practice',
          description: 'Develop awareness and acceptance of present moment experiences',
          exercises: ['Daily meditation', 'Body scan practice', 'Mindful breathing'],
          resources: ['Meditation apps', 'Mindfulness books'],
          priority: 'medium'
        }
      ]
    };

    return commonRecommendations[type] || commonRecommendations.general;
  }
}
