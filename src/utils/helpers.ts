import { AssessmentType, EnvironmentTheme } from '@/types';
import { v4 as uuidv4 } from 'uuid';

export const generateId = (): string => uuidv4();

export const formatDate = (date: Date): string => {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

export const formatDateShort = (date: Date): string => {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  }).format(date);
};

export const timeAgo = (date: Date): string => {
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  if (diffInSeconds < 60) return 'just now';
  
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) return `${diffInMinutes} minutes ago`;
  
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) return `${diffInHours} hours ago`;
  
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 7) return `${diffInDays} days ago`;
  
  const diffInWeeks = Math.floor(diffInDays / 7);
  if (diffInWeeks < 4) return `${diffInWeeks} weeks ago`;
  
  const diffInMonths = Math.floor(diffInDays / 30);
  return `${diffInMonths} months ago`;
};

export const getAssessmentTitle = (type: AssessmentType): string => {
  const titles = {
    anxiety: 'Anxiety Assessment',
    ocd: 'OCD Assessment',
    anger: 'Anger Management Assessment',
    general: 'General Wellbeing Assessment'
  };
  return titles[type];
};

export const getAssessmentDescription = (type: AssessmentType): string => {
  const descriptions = {
    anxiety: 'Explore your anxiety patterns and discover personalized coping strategies',
    ocd: 'Understand your thoughts and behaviors to find effective management techniques',
    anger: 'Learn about your anger triggers and develop healthier expression methods',
    general: 'Assess your overall mental wellbeing and identify areas for growth'
  };
  return descriptions[type];
};

export const getEnvironmentColors = (environment: EnvironmentTheme): { primary: string; secondary: string; accent: string } => {
  const colors = {
    forest: {
      primary: '#065f46', // green-800
      secondary: '#10b981', // emerald-500
      accent: '#6ee7b7' // emerald-300
    },
    ocean: {
      primary: '#0c4a6e', // sky-900
      secondary: '#0ea5e9', // sky-500
      accent: '#7dd3fc' // sky-300
    },
    mountains: {
      primary: '#374151', // gray-700
      secondary: '#6b7280', // gray-500
      accent: '#d1d5db' // gray-300
    },
    garden: {
      primary: '#7c2d12', // orange-800
      secondary: '#f97316', // orange-500
      accent: '#fed7aa' // orange-200
    },
    sky: {
      primary: '#1e1b4b', // indigo-900
      secondary: '#6366f1', // indigo-500
      accent: '#c7d2fe' // indigo-200
    },
    lighthouse: {
      primary: '#581c87', // purple-800
      secondary: '#a855f7', // purple-500
      accent: '#ddd6fe' // purple-200
    },
    room: {
      primary: '#92400e', // amber-700
      secondary: '#f59e0b', // amber-500
      accent: '#fde68a' // amber-200
    }
  };
  return colors[environment];
};

export const getEnvironmentGradient = (environment: EnvironmentTheme): string => {
  const gradients = {
    forest: 'from-green-900 via-green-700 to-emerald-600',
    ocean: 'from-blue-900 via-blue-700 to-sky-600',
    mountains: 'from-gray-900 via-gray-700 to-slate-600',
    garden: 'from-orange-900 via-orange-700 to-amber-600',
    sky: 'from-indigo-900 via-indigo-700 to-purple-600',
    lighthouse: 'from-purple-900 via-purple-700 to-pink-600',
    room: 'from-amber-900 via-amber-700 to-yellow-600'
  };
  return gradients[environment];
};

export const getMoodEmoji = (mood: string): string => {
  const moodEmojis: Record<string, string> = {
    'very-sad': '😢',
    'sad': '😞',
    'neutral': '😐',
    'happy': '😊',
    'very-happy': '😄',
    'anxious': '😰',
    'calm': '😌',
    'angry': '😠',
    'frustrated': '😤',
    'tired': '😴',
    'energetic': '⚡',
    'confused': '😕',
    'hopeful': '🌟',
    'grateful': '🙏',
    'worried': '😟'
  };
  return moodEmojis[mood] || '😐';
};

export const calculateProgress = (currentStep: number, totalSteps: number): number => {
  return Math.round((currentStep / totalSteps) * 100);
};

export const getCompletionMessage = (type: AssessmentType): string => {
  const messages = {
    anxiety: 'You\'ve completed your anxiety assessment journey. Your insights are being carefully crafted...',
    ocd: 'Your OCD assessment is complete. We\'re analyzing your responses to provide personalized guidance...',
    anger: 'Well done on completing your anger assessment. Your personalized report is being generated...',
    general: 'Thank you for completing your wellbeing assessment. Your comprehensive report is being prepared...'
  };
  return messages[type];
};

export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const sanitizeInput = (input: string): string => {
  return input.trim().replace(/[<>]/g, '');
};

export const downloadAsJSON = (data: any, filename: string): void => {
  const jsonString = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonString], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `${filename}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  URL.revokeObjectURL(url);
};

export const shuffleArray = <T>(array: T[]): T[] => {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};

export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

export const isValidApiKey = (apiKey: string): boolean => {
  // Basic validation for Gemini API key format
  return apiKey.length > 30 && apiKey.startsWith('AI');
};
