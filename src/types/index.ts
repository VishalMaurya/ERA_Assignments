export interface User {
  id: string;
  name?: string;
  email?: string;
  createdAt: Date;
}

// Expanded Assessment Types based on Therapy Catalog
export type AssessmentType = 
  // CBT Family
  | 'anxiety'
  | 'ocd' 
  | 'behavioral-activation'
  | 'habit-reversal'
  | 'problem-solving'
  // Mindfulness & Acceptance
  | 'mindfulness'
  | 'acceptance-commitment'
  | 'mindful-cognitive'
  // Emotion Regulation & Interpersonal
  | 'anger'
  | 'emotion-regulation'
  | 'interpersonal'
  // Compassion & Self-Kindness
  | 'self-compassion'
  | 'positive-psychology'
  | 'strengths'
  // Lifestyle & Holistic
  | 'sleep'
  | 'relaxation'
  | 'breathing'
  | 'exercise'
  | 'nutrition'
  // Specialized Therapies
  | 'trauma'
  | 'schema'
  | 'narrative'
  | 'motivation'
  | 'solution-focused'
  // General
  | 'general';

export type QuestionType = 'mcq' | 'open-ended' | 'scale' | 'mood';

export interface Question {
  id: string;
  type: QuestionType;
  question: string;
  description?: string;
  options?: string[];
  scaleMin?: number;
  scaleMax?: number;
  scaleLabels?: string[];
  hint?: string;
  example?: string;
  required?: boolean;
  environment: EnvironmentTheme;
}

export type EnvironmentTheme = 'forest' | 'ocean' | 'mountains' | 'garden' | 'sky' | 'lighthouse' | 'room';

export interface QuestionResponse {
  questionId: string;
  answer: string | number | string[];
  mood?: string;
  timestamp: Date;
  timeSpent?: number; // in seconds
}

export interface Assessment {
  id: string;
  userId: string;
  type: AssessmentType;
  questions: Question[];
  responses: QuestionResponse[];
  currentQuestionIndex: number;
  isCompleted: boolean;
  startedAt: Date;
  completedAt?: Date;
  skippedQuestions: string[];
}

export interface TherapyRecommendation {
  type: string;
  title: string;
  description: string;
  exercises: string[];
  resources: string[];
  priority: 'high' | 'medium' | 'low';
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
  generatedAt: Date;
  rawAIResponse?: string;
  generationTimeMs?: number; // Time taken by Gemini AI to generate report
  processingStartedAt?: Date;
  processingCompletedAt?: Date;
}

export interface DashboardData {
  user: User;
  assessments: Assessment[];
  reports: AssessmentReport[];
  progressMetrics: {
    totalAssessments: number;
    completionRate: number;
    lastAssessment: Date;
    improvementTrend: 'improving' | 'stable' | 'needs_attention';
  };
}

export interface ProgressStep {
  id: string;
  title: string;
  isCompleted: boolean;
  isCurrent: boolean;
  environment: EnvironmentTheme;
}

export interface JourneyState {
  assessmentType: AssessmentType;
  currentStep: number;
  totalSteps: number;
  progressSteps: ProgressStep[];
  currentEnvironment: EnvironmentTheme;
  mood: string;
  canSkip: boolean;
}

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface GeminiConfig {
  apiKey: string;
  model: string;
}

export interface AnimationState {
  isVisible: boolean;
  isAnimating: boolean;
  currentAnimation: string;
}
