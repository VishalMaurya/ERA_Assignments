// Shared types for Lambda functions (adapted from your original app)
export type AssessmentType = 
  | 'anxiety' | 'ocd' | 'behavioral-activation' | 'habit-reversal' | 'problem-solving'
  | 'mindfulness' | 'acceptance-commitment' | 'mindful-cognitive'
  | 'anger' | 'emotion-regulation' | 'interpersonal'
  | 'self-compassion' | 'positive-psychology' | 'strengths'
  | 'sleep' | 'relaxation' | 'breathing' | 'exercise' | 'nutrition'
  | 'trauma' | 'schema' | 'narrative' | 'motivation' | 'solution-focused'
  | 'general';

export type QuestionType = 'mcq' | 'scale' | 'open-ended';
export type Environment = 'ocean' | 'forest' | 'mountains' | 'garden' | 'space';

export interface Question {
  id: string;
  type: QuestionType;
  text: string;
  environment: Environment;
  options?: string[];
  scaleRange?: [number, number];
  scaleLabels?: [string, string];
  therapyMapping: string[];
  cognitivePattern?: string;
  emotionalPattern?: string;
  behavioralPattern?: string;
  severityIndicator?: 'low' | 'moderate' | 'high';
}

export interface QuestionResponse {
  questionId: string;
  answer: string | number;
  answeredAt: string;
  mood?: string;
  timeSpent?: number;
}

export interface Assessment {
  id: string;
  userId: string;
  type: AssessmentType;
  questions: Question[];
  responses: QuestionResponse[];
  currentQuestionIndex: number;
  isCompleted: boolean;
  startedAt: string;
  completedAt?: string;
  skippedQuestions: string[];
  totalTimeSpent: number;
}

export interface TherapyRecommendation {
  therapyType: AssessmentType;
  priority: 'primary' | 'secondary' | 'supplementary';
  confidence: number;
  reasoning: string[];
  suggestedExercises: string[];
  estimatedDuration: string;
  successPredictors: string[];
  potentialBarriers: string[];
  evidenceLevel?: 'high' | 'moderate' | 'emerging';
}

export interface AssessmentReport {
  id: string;
  assessmentId: string;
  userId: string;
  summary: string;
  patterns: string[];
  severityLevel: 'mild' | 'moderate' | 'high';
  recommendations: TherapyRecommendation[];
  insights: string[];
  nextSteps: string[];
  generatedAt: string;
  generationTimeMs?: number;
  aiModel?: string;
}

export interface User {
  id: string;
  email?: string;
  createdAt: string;
  preferences: {
    theme?: 'light' | 'dark';
    notifications?: boolean;
    dataRetention?: number;
  };
  stats: {
    totalAssessments: number;
    completedAssessments: number;
    totalTimeSpent: number;
    lastAssessment?: string;
  };
}

// Lambda Event Types
export interface LambdaEvent {
  httpMethod: string;
  path: string;
  pathParameters?: Record<string, string>;
  queryStringParameters?: Record<string, string>;
  headers: Record<string, string>;
  body?: string;
  requestContext: {
    requestId: string;
    accountId: string;
    resourceId: string;
    stage: string;
    requestTime: string;
    identity: {
      sourceIp: string;
      userAgent: string;
    };
  };
}

export interface LambdaResponse {
  statusCode: number;
  headers: Record<string, string>;
  body: string;
  isBase64Encoded?: boolean;
}
