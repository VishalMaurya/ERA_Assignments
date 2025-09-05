'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconProp } from '@fortawesome/fontawesome-svg-core';
import { AssessmentType, Assessment, Question, QuestionResponse, JourneyState } from '@/types';
import { getQuestionsForAssessment } from '@/data/questions';
import { generateId, getAssessmentTitle } from '@/utils/helpers';
import { StorageService } from '@/utils/storage';
import ProgressBar from '@/components/assessment/ProgressBar';
import QuestionCard from '@/components/assessment/QuestionCard';
import EnvironmentBackground from '@/components/assessment/EnvironmentBackground';
import JourneyComplete from '@/components/assessment/JourneyComplete';
import ApiKeyModal from '@/components/ui/ApiKeyModal';

export default function AssessmentPage() {
  const params = useParams();
  const router = useRouter();
  const assessmentType = params.type as AssessmentType;

  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCompleted, setIsCompleted] = useState(false);
  const [showApiKeyModal, setShowApiKeyModal] = useState(false);
  const [journeyState, setJourneyState] = useState<JourneyState | null>(null);

  useEffect(() => {
    initializeAssessment();
  }, [assessmentType]);

  const initializeAssessment = () => {
    // Validate assessment type by checking if questions exist
    const assessmentQuestions = getQuestionsForAssessment(assessmentType);
    if (assessmentQuestions.length === 0) {
      router.push('/');
      return;
    }

    // Check for existing assessment in progress
    const existingAssessment = StorageService.getCurrentAssessment();
    if (existingAssessment && existingAssessment.type === assessmentType) {
      setAssessment(existingAssessment);
      setQuestions(existingAssessment.questions);
      setCurrentQuestionIndex(existingAssessment.currentQuestionIndex);
      setResponses(existingAssessment.responses);
      if (existingAssessment.isCompleted) {
        setIsCompleted(true);
      }
    } else {
      // Create new assessment
      const newAssessment: Assessment = {
        id: generateId(),
        userId: generateId(), // In a real app, this would come from auth
        type: assessmentType,
        questions: assessmentQuestions,
        responses: [],
        currentQuestionIndex: 0,
        isCompleted: false,
        startedAt: new Date(),
        skippedQuestions: []
      };

      setAssessment(newAssessment);
      setQuestions(assessmentQuestions);
      StorageService.saveCurrentAssessment(newAssessment);
    }

    // Initialize journey state
    setJourneyState({
      assessmentType,
      currentStep: 0,
      totalSteps: assessmentQuestions.length,
      progressSteps: assessmentQuestions.map((q, index) => ({
        id: q.id,
        title: `Step ${index + 1}`,
        isCompleted: false,
        isCurrent: index === 0,
        environment: q.environment
      })),
      currentEnvironment: assessmentQuestions[0]?.environment || 'garden',
      mood: '',
      canSkip: true
    });

    setIsLoading(false);
  };

  const handleQuestionResponse = (response: QuestionResponse) => {
    if (!assessment) return;

    const updatedResponses = [...responses];
    const existingResponseIndex = updatedResponses.findIndex(r => r.questionId === response.questionId);

    if (existingResponseIndex >= 0) {
      updatedResponses[existingResponseIndex] = response;
    } else {
      updatedResponses.push(response);
    }

    setResponses(updatedResponses);

    // Update assessment
    const updatedAssessment = {
      ...assessment,
      responses: updatedResponses,
      currentQuestionIndex: Math.min(currentQuestionIndex + 1, questions.length)
    };

    setAssessment(updatedAssessment);
    StorageService.saveCurrentAssessment(updatedAssessment);

    // Move to next question or complete
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      updateJourneyState(currentQuestionIndex + 1);
    } else {
      completeAssessment(updatedAssessment);
    }
  };

  const handleSkipQuestion = () => {
    if (!assessment) return;

    const updatedAssessment = {
      ...assessment,
      skippedQuestions: [...assessment.skippedQuestions, questions[currentQuestionIndex].id],
      currentQuestionIndex: Math.min(currentQuestionIndex + 1, questions.length)
    };

    setAssessment(updatedAssessment);
    StorageService.saveCurrentAssessment(updatedAssessment);

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      updateJourneyState(currentQuestionIndex + 1);
    } else {
      completeAssessment(updatedAssessment);
    }
  };

  const updateJourneyState = (newIndex: number) => {
    if (!journeyState) return;

    const updatedProgressSteps = journeyState.progressSteps.map((step, index) => ({
      ...step,
      isCompleted: index < newIndex,
      isCurrent: index === newIndex
    }));

    setJourneyState({
      ...journeyState,
      currentStep: newIndex,
      progressSteps: updatedProgressSteps,
      currentEnvironment: questions[newIndex]?.environment || journeyState.currentEnvironment
    });
  };

  const completeAssessment = (finalAssessment: Assessment) => {
    const completedAssessment = {
      ...finalAssessment,
      isCompleted: true,
      completedAt: new Date()
    };

    setAssessment(completedAssessment);
    StorageService.saveAssessment(completedAssessment);
    StorageService.clearCurrentAssessment();
    setIsCompleted(true);

    // Check if API key is available for report generation
    const apiKey = StorageService.getGeminiApiKey();
    if (!apiKey) {
      setShowApiKeyModal(true);
    }
  };

  const handleGoBack = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
      updateJourneyState(currentQuestionIndex - 1);
    }
  };

  const handleExitAssessment = () => {
    if (window.confirm('Are you sure you want to exit? Your progress will be saved.')) {
      router.push('/');
    }
  };

  const handleApiKeySubmit = (apiKey: string) => {
    StorageService.saveGeminiApiKey(apiKey);
    setShowApiKeyModal(false);
    if (assessment) {
      router.push(`/report/${assessment.id}`);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-calm-600">Loading your journey...</p>
        </div>
      </div>
    );
  }

  if (isCompleted) {
    return (
      <>
        <JourneyComplete
          assessment={assessment!}
          onGenerateReport={() => {
            const apiKey = StorageService.getGeminiApiKey();
            if (!apiKey) {
              setShowApiKeyModal(true);
            } else if (assessment) {
              router.push(`/report/${assessment.id}`);
            }
          }}
          onReturnHome={() => router.push('/')}
        />
        
        <ApiKeyModal
          isOpen={showApiKeyModal}
          onClose={() => setShowApiKeyModal(false)}
          onSubmit={handleApiKeySubmit}
        />
      </>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
  
  // Calculate response intensity for interactive background
  const calculateResponseIntensity = () => {
    if (responses.length === 0) return 0.5;
    
    let totalIntensity = 0;
    responses.forEach(response => {
      const answer = response.answer;
      
      // Simple intensity calculation based on answer patterns
      if (typeof answer === 'string') {
        // Higher intensity for more severe responses
        if (answer.toLowerCase().includes('always') || 
            answer.toLowerCase().includes('constantly') ||
            answer.toLowerCase().includes('severe') ||
            answer.toLowerCase().includes('extreme')) {
          totalIntensity += 1.0;
        } else if (answer.toLowerCase().includes('often') || 
                   answer.toLowerCase().includes('frequently') ||
                   answer.toLowerCase().includes('moderate')) {
          totalIntensity += 0.7;
        } else if (answer.toLowerCase().includes('sometimes') ||
                   answer.toLowerCase().includes('occasionally')) {
          totalIntensity += 0.4;
        } else {
          totalIntensity += 0.2;
        }
      } else if (Array.isArray(answer)) {
        // Multiple selections might indicate higher intensity
        totalIntensity += Math.min(1.0, answer.length * 0.3);
      }
    });
    
    return Math.min(1.0, totalIntensity / responses.length);
  };
  
  // Get the most recent mood or default to neutral
  const getCurrentMood = () => {
    const recentResponses = responses.slice(-3); // Look at last 3 responses
    for (let i = recentResponses.length - 1; i >= 0; i--) {
      if (recentResponses[i].mood) {
        return recentResponses[i].mood;
      }
    }
    return 'neutral';
  };
  
  const responseIntensity = calculateResponseIntensity();
  const currentMood = getCurrentMood();

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Environment Background */}
      <EnvironmentBackground 
        environment={currentQuestion?.environment || 'garden'}
        userMood={currentMood}
        responseIntensity={responseIntensity}
        isInteractive={true}
      />

      {/* Progress Bar */}
      <ProgressBar
        progress={progress}
        currentStep={currentQuestionIndex + 1}
        totalSteps={questions.length}
        assessmentTitle={getAssessmentTitle(assessmentType)}
        onExit={handleExitAssessment}
      />

      {/* Dashboard Link */}
      <motion.button
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 1 }}
        onClick={() => router.push('/dashboard')}
        className="fixed top-4 right-4 z-30 bg-emerald-600 hover:bg-emerald-700 text-white p-3 rounded-full shadow-lg transition-colors"
        title="Go to Dashboard"
      >
        <FontAwesomeIcon icon={'chart-line' as IconProp} className="w-5 h-5" />
      </motion.button>

      {/* Question Content */}
      <div className="relative z-10 container mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentQuestionIndex}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ 
              duration: 0.2,
              ease: "easeOut"
            }}
            className="max-w-4xl mx-auto"
          >
            <QuestionCard
              question={currentQuestion}
              questionNumber={currentQuestionIndex + 1}
              totalQuestions={questions.length}
              onResponse={handleQuestionResponse}
              onSkip={handleSkipQuestion}
              onBack={currentQuestionIndex > 0 ? handleGoBack : undefined}
              existingResponse={responses.find(r => r.questionId === currentQuestion.id)}
            />
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
