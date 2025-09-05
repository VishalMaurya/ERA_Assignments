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
    
    // Track processing time
    const processingStartedAt = new Date();
    const startTime = performance.now();
    
    try {
      const result = await model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();
      
      // Calculate processing time
      const endTime = performance.now();
      const processingCompletedAt = new Date();
      const generationTimeMs = Math.round(endTime - startTime);
      
      const report = this.parseAIResponse(text, assessment);
      
      // Add timing information to the report
      return {
        ...report,
        generationTimeMs,
        processingStartedAt,
        processingCompletedAt
      };
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
      "therapyType": "anxiety|ocd|anger|mindfulness|sleep|general|trauma|strengths",
      "priority": "primary|secondary|supplementary",
      "confidence": 0.8,
      "reasoning": ["Explanation of why this therapy is recommended", "Evidence-based rationale"],
      "suggestedExercises": ["exercise_1", "exercise_2", "exercise_3"],
      "estimatedDuration": "4-6 weeks",
      "successPredictors": ["Factor that increases success", "Another success factor"],
      "potentialBarriers": ["Potential challenge", "Another barrier"]
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
      
      // Transform recommendations to ensure correct format
      const transformedRecommendations = this.transformRecommendations(parsed.recommendations || [], assessment.type);
      
      return {
        id: `report_${Date.now()}`,
        assessmentId: assessment.id,
        userId: assessment.userId,
        summary: parsed.summary || 'Thank you for completing this assessment.',
        patterns: parsed.patterns || [],
        severityLevel: parsed.severityLevel || 'mild',
        recommendations: transformedRecommendations,
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

  private transformRecommendations(recommendations: any[], assessmentType: string): TherapyRecommendation[] {
    if (!recommendations || recommendations.length === 0) {
      return this.getFallbackRecommendations(assessmentType);
    }

    return recommendations.map((rec, index) => {
      // Handle new format (already correct)
      if (rec.therapyType && rec.priority && rec.reasoning) {
        return rec as TherapyRecommendation;
      }

      // Handle old format - transform to new format
      if (rec.type || rec.title) {
        return {
          therapyType: this.mapOldTypeToNew(rec.type, assessmentType),
          priority: this.mapOldPriorityToNew(rec.priority, index),
          confidence: 0.7, // Default confidence
          reasoning: rec.description ? [rec.description] : ['AI-generated recommendation'],
          suggestedExercises: rec.exercises || [],
          estimatedDuration: '4-6 weeks', // Default duration
          successPredictors: rec.resources ? rec.resources.slice(0, 2) : ['Regular practice'],
          potentialBarriers: ['Time constraints', 'Initial resistance']
        } as TherapyRecommendation;
      }

      // Invalid format - skip
      return null;
    }).filter(rec => rec !== null) as TherapyRecommendation[];
  }

  private mapOldTypeToNew(oldType: string, assessmentType: string): string {
    const typeMap: Record<string, string> = {
      'CBT': 'anxiety',
      'DBT': 'anger', 
      'ACT': 'mindfulness',
      'MBSR': 'mindfulness',
      'ERP': 'ocd',
      'HRT': 'ocd',
      'Mindfulness': 'mindfulness',
      'Exercise': 'general'
    };
    return typeMap[oldType] || assessmentType;
  }

  private mapOldPriorityToNew(oldPriority: string, index: number): 'primary' | 'secondary' | 'supplementary' {
    if (oldPriority === 'high' || index === 0) return 'primary';
    if (oldPriority === 'medium' || index < 3) return 'secondary';
    return 'supplementary';
  }

  private getFallbackRecommendations(type: string): TherapyRecommendation[] {
    const commonRecommendations: Record<string, TherapyRecommendation[]> = {
      anxiety: [
        {
          therapyType: 'anxiety',
          priority: 'primary',
          confidence: 0.8,
          reasoning: ['Common cognitive patterns identified', 'Evidence-based approach for anxiety'],
          suggestedExercises: ['thought_record_basic', 'exposure_hierarchy'],
          estimatedDuration: '4-8 weeks',
          successPredictors: ['Willingness to face fears', 'Regular practice'],
          potentialBarriers: ['Avoidance patterns', 'High anxiety sensitivity']
        }
      ],
      ocd: [
        {
          therapyType: 'ocd',
          priority: 'primary',
          confidence: 0.9,
          reasoning: ['Compulsive behaviors identified', 'ERP is gold standard treatment'],
          suggestedExercises: ['erp_planning'],
          estimatedDuration: '8-12 weeks',
          successPredictors: ['Understanding of ERP principles', 'Motivation to resist compulsions'],
          potentialBarriers: ['Fear of anxiety', 'Perfectionist beliefs']
        }
      ],
      anger: [
        {
          therapyType: 'anger',
          priority: 'primary',
          confidence: 0.8,
          reasoning: ['Emotional regulation challenges', 'Anger management skills needed'],
          suggestedExercises: ['anger_diary', 'dbt_stop_skill'],
          estimatedDuration: '6-10 weeks',
          successPredictors: ['Recognition of triggers', 'Commitment to practice'],
          potentialBarriers: ['Impulsivity', 'Blame patterns']
        }
      ],
      sleep: [
        {
          therapyType: 'sleep',
          priority: 'primary',
          confidence: 0.8,
          reasoning: ['Sleep hygiene and relaxation techniques needed', 'CBT-I is effective for sleep issues'],
          suggestedExercises: ['sleep_diary', 'progressive_relaxation', 'sleep_restriction'],
          estimatedDuration: '4-6 weeks',
          successPredictors: ['Consistent bedtime routine', 'Willingness to change habits'],
          potentialBarriers: ['Lifestyle constraints', 'Chronic conditions']
        }
      ],
      mindfulness: [
        {
          therapyType: 'mindfulness',
          priority: 'primary',
          confidence: 0.8,
          reasoning: ['Mindfulness practice supports emotional regulation', 'Evidence-based stress reduction'],
          suggestedExercises: ['body_scan', 'mindful_breathing', 'loving_kindness'],
          estimatedDuration: '6-8 weeks',
          successPredictors: ['Regular practice', 'Open to present moment awareness'],
          potentialBarriers: ['Impatience', 'Difficulty sitting still']
        }
      ],
      'self-compassion': [
        {
          therapyType: 'self-compassion',
          priority: 'primary',
          confidence: 0.7,
          reasoning: ['Self-criticism patterns identified', 'Compassion-focused therapy helps'],
          suggestedExercises: ['self_compassion_break', 'kind_self_talk'],
          estimatedDuration: '4-6 weeks',
          successPredictors: ['Willingness to be kind to self', 'Recognition of self-criticism'],
          potentialBarriers: ['Feeling undeserving', 'Cultural barriers to self-care']
        }
      ],
      trauma: [
        {
          therapyType: 'trauma',
          priority: 'primary',
          confidence: 0.9,
          reasoning: ['Trauma-informed approach needed', 'EMDR or CPT recommended'],
          suggestedExercises: ['grounding_techniques', 'safety_planning'],
          estimatedDuration: '12-20 weeks',
          successPredictors: ['Therapeutic alliance', 'Support system'],
          potentialBarriers: ['Avoidance', 'Trust issues']
        }
      ],
      strengths: [
        {
          therapyType: 'strengths',
          priority: 'primary',
          confidence: 0.7,
          reasoning: ['Strengths-based approach supports resilience', 'Positive psychology techniques'],
          suggestedExercises: ['strengths_identification', 'gratitude_practice'],
          estimatedDuration: '3-5 weeks',
          successPredictors: ['Self-awareness', 'Growth mindset'],
          potentialBarriers: ['Negative self-perception', 'Comparison with others']
        }
      ],
      general: [
        {
          therapyType: 'general',
          priority: 'primary',
          confidence: 0.7,
          reasoning: ['General wellbeing focus', 'Mindfulness supports overall mental health'],
          suggestedExercises: ['daily_mood_check', 'gratitude_moment'],
          estimatedDuration: '2-4 weeks',
          successPredictors: ['Regular practice', 'Open to new approaches'],
          potentialBarriers: ['Lack of specific focus', 'Low motivation']
        }
      ]
    };

    return commonRecommendations[type] || commonRecommendations.general;
  }
}
