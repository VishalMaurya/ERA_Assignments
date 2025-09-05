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
  therapyMapping?: AssessmentType[];
  cognitivePattern?: string;
  emotionalPattern?: string;
  behavioralPattern?: string;
  severityIndicator?: 'low' | 'moderate' | 'high';
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
  therapyType: AssessmentType;
  priority: 'primary' | 'secondary' | 'supplementary';
  confidence: number;
  reasoning: string[];
  suggestedExercises: string[];
  estimatedDuration: string;
  successPredictors: string[];
  potentialBarriers: string[];
  evidenceLevel?: 'strong' | 'moderate' | 'emerging';
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

// Therapy Exercise System
export interface TherapyExercise {
  id: string;
  name: string;
  type: 'interactive' | 'reflection' | 'behavioral' | 'cognitive';
  therapyType: AssessmentType;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedDuration: number; // minutes
  description: string;
  instructions: string[];
  requiredInputs: ExerciseInput[];
  learningObjectives: string[];
  evidenceBase?: string;
}

export interface ExerciseInput {
  id: string;
  type: 'text' | 'scale' | 'choice' | 'file' | 'audio';
  label: string;
  required: boolean;
  validation?: any;
}

export interface ExerciseSession {
  id: string;
  exerciseId: string;
  userId: string;
  startTime: Date;
  endTime?: Date;
  responses: Record<string, any>;
  completionStatus: 'started' | 'completed' | 'abandoned';
  insights?: string[];
  mood?: {
    before: number;
    after: number;
  };
  difficulty?: number; // 1-10 scale
  helpfulness?: number; // 1-10 scale
}

// Progress Tracking
export interface ProgressMetric {
  id: string;
  userId: string;
  metricType: 'symptom_severity' | 'skill_mastery' | 'engagement' | 'functional_improvement';
  value: number;
  maxValue: number;
  date: Date;
  therapyContext: AssessmentType;
  notes?: string;
}

// Gamification
export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  criteria: {
    type: 'streak' | 'completion' | 'improvement' | 'milestone';
    threshold: number;
    metric: string;
  };
  rarity: 'common' | 'uncommon' | 'rare' | 'legendary';
  earnedDate?: Date;
}

export interface UserProgress {
  userId: string;
  currentStreak: number;
  longestStreak: number;
  totalExercisesCompleted: number;
  skillLevels: Partial<Record<AssessmentType, number>>; // 0-100 scale
  achievements: Achievement[];
  preferredTherapies: AssessmentType[];
  lastActiveDate: Date;
}
