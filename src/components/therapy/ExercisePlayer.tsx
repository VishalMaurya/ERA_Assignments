'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconProp } from '@fortawesome/fontawesome-svg-core';
import { TherapyExercise, ExerciseSession, ExerciseInput } from '@/types';

interface ExercisePlayerProps {
  exercise: TherapyExercise;
  onComplete: (session: ExerciseSession) => void;
  onClose: () => void;
}

export default function ExercisePlayer({ exercise, onComplete, onClose }: ExercisePlayerProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [responses, setResponses] = useState<Record<string, any>>({});
  const [isCompleted, setIsCompleted] = useState(false);
  const [moodBefore, setMoodBefore] = useState<number | null>(null);
  const [moodAfter, setMoodAfter] = useState<number | null>(null);
  const [session] = useState<ExerciseSession>({
    id: Math.random().toString(36).substr(2, 9),
    exerciseId: exercise.id,
    userId: 'current-user', // Would come from auth
    startTime: new Date(),
    responses: {},
    completionStatus: 'started'
  });

  // Steps: intro -> mood-before -> instructions -> inputs -> mood-after -> completion
  const totalSteps = 2 + exercise.instructions.length + exercise.requiredInputs.length + 2;

  const handleNext = () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const handleInputChange = (inputId: string, value: any) => {
    setResponses(prev => ({
      ...prev,
      [inputId]: value
    }));
  };

  const handleComplete = () => {
    const completedSession: ExerciseSession = {
      ...session,
      endTime: new Date(),
      responses,
      completionStatus: 'completed',
      mood: moodBefore && moodAfter ? { before: moodBefore, after: moodAfter } : undefined
    };
    
    setIsCompleted(true);
    onComplete(completedSession);
  };

  const getCurrentStepContent = () => {
    if (currentStep === 0) {
      return <IntroStep exercise={exercise} />;
    } else if (currentStep === 1) {
      return <MoodCheckStep mood={moodBefore} setMood={setMoodBefore} type="before" />;
    } else if (currentStep <= 1 + exercise.instructions.length) {
      const instructionIndex = currentStep - 2;
      return <InstructionStep instruction={exercise.instructions[instructionIndex]} stepNumber={instructionIndex + 1} />;
    } else if (currentStep <= 1 + exercise.instructions.length + exercise.requiredInputs.length) {
      const inputIndex = currentStep - 2 - exercise.instructions.length;
      const input = exercise.requiredInputs[inputIndex];
      return (
        <InputStep 
          input={input} 
          value={responses[input.id]} 
          onChange={(value) => handleInputChange(input.id, value)} 
        />
      );
    } else if (currentStep === totalSteps - 2) {
      return <MoodCheckStep mood={moodAfter} setMood={setMoodAfter} type="after" />;
    } else {
      return <CompletionStep exercise={exercise} />;
    }
  };

  const canProceed = () => {
    if (currentStep === 1 && moodBefore === null) return false;
    if (currentStep === totalSteps - 2 && moodAfter === null) return false;
    
    // Check if current input is completed
    if (currentStep > 1 + exercise.instructions.length && currentStep <= 1 + exercise.instructions.length + exercise.requiredInputs.length) {
      const inputIndex = currentStep - 2 - exercise.instructions.length;
      const input = exercise.requiredInputs[inputIndex];
      if (input.required && !responses[input.id]) return false;
    }
    
    return true;
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-primary-500 to-nature-500 text-white p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold">{exercise.name}</h2>
              <p className="text-primary-100 text-sm">{exercise.estimatedDuration} minutes • {exercise.difficulty}</p>
            </div>
            <button
              onClick={onClose}
              className="text-white/80 hover:text-white transition-colors"
            >
              <FontAwesomeIcon icon={'xmark' as IconProp} className="w-6 h-6" />
            </button>
          </div>
          
          {/* Progress Bar */}
          <div className="mt-4">
            <div className="flex justify-between text-sm text-primary-100 mb-2">
              <span>Step {currentStep + 1} of {totalSteps}</span>
              <span>{Math.round(((currentStep + 1) / totalSteps) * 100)}%</span>
            </div>
            <div className="w-full bg-primary-600 rounded-full h-2">
              <motion.div
                className="bg-white rounded-full h-2"
                initial={{ width: 0 }}
                animate={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {getCurrentStepContent()}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 flex justify-between">
          <button
            onClick={handlePrevious}
            disabled={currentStep === 0}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <FontAwesomeIcon icon={'chevron-left' as IconProp} className="w-4 h-4 mr-2" />
            Previous
          </button>
          
          {currentStep === totalSteps - 1 ? (
            <button
              onClick={handleComplete}
              disabled={!canProceed()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <FontAwesomeIcon icon={'check' as IconProp} className="w-4 h-4 mr-2" />
              Complete Exercise
            </button>
          ) : (
            <button
              onClick={handleNext}
              disabled={!canProceed()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
              <FontAwesomeIcon icon={'chevron-right' as IconProp} className="w-4 h-4 ml-2" />
            </button>
          )}
        </div>
      </motion.div>
    </div>
  );
}

// Step Components
function IntroStep({ exercise }: { exercise: TherapyExercise }) {
  return (
    <div className="text-center space-y-4">
      <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto">
        <FontAwesomeIcon icon={'lightbulb' as IconProp} className="w-8 h-8 text-primary-600" />
      </div>
      <h3 className="text-2xl font-bold text-calm-800">Let's Begin</h3>
      <p className="text-calm-600 text-lg">{exercise.description}</p>
      
      {exercise.learningObjectives.length > 0 && (
        <div className="bg-blue-50 rounded-lg p-4 text-left">
          <h4 className="font-semibold text-blue-800 mb-2">What you'll learn:</h4>
          <ul className="text-blue-700 space-y-1">
            {exercise.learningObjectives.map((objective, index) => (
              <li key={index} className="flex items-start">
                <FontAwesomeIcon icon={'check' as IconProp} className="w-4 h-4 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
                {objective}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function MoodCheckStep({ mood, setMood, type }: { 
  mood: number | null; 
  setMood: (mood: number) => void; 
  type: 'before' | 'after';
}) {
  return (
    <div className="text-center space-y-6">
      <div className="w-16 h-16 bg-nature-100 rounded-full flex items-center justify-center mx-auto">
        <FontAwesomeIcon icon={'heart' as IconProp} className="w-8 h-8 text-nature-600" />
      </div>
      <h3 className="text-2xl font-bold text-calm-800">
        How are you feeling {type === 'before' ? 'right now' : 'after this exercise'}?
      </h3>
      <p className="text-calm-600">
        {type === 'before' 
          ? 'Let\'s check in with your current mood before we start.'
          : 'How has your mood changed after completing this exercise?'
        }
      </p>
      
      <div className="space-y-4">
        <div className="flex justify-center space-x-2">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
            <button
              key={num}
              onClick={() => setMood(num)}
              className={`w-12 h-12 rounded-full border-2 transition-all ${
                mood === num
                  ? 'bg-primary-500 border-primary-500 text-white'
                  : 'border-gray-300 hover:border-primary-300 text-gray-600'
              }`}
            >
              {num}
            </button>
          ))}
        </div>
        <div className="flex justify-between text-sm text-gray-500 px-6">
          <span>Very Low</span>
          <span>Very High</span>
        </div>
      </div>
    </div>
  );
}

function InstructionStep({ instruction, stepNumber }: { instruction: string; stepNumber: number }) {
  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 bg-primary-500 text-white rounded-full flex items-center justify-center font-bold">
          {stepNumber}
        </div>
        <h3 className="text-xl font-semibold text-calm-800">Step {stepNumber}</h3>
      </div>
      <p className="text-calm-700 text-lg leading-relaxed pl-11">{instruction}</p>
    </div>
  );
}

function InputStep({ input, value, onChange }: { 
  input: ExerciseInput; 
  value: any; 
  onChange: (value: any) => void;
}) {
  const renderInput = () => {
    switch (input.type) {
      case 'text':
        return (
          <textarea
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            placeholder="Share your thoughts..."
            className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
            rows={4}
          />
        );
        
      case 'scale':
        return (
          <div className="space-y-4">
            <div className="flex justify-center space-x-2">
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                <button
                  key={num}
                  onClick={() => onChange(num)}
                  className={`w-12 h-12 rounded-full border-2 transition-all ${
                    value === num
                      ? 'bg-primary-500 border-primary-500 text-white'
                      : 'border-gray-300 hover:border-primary-300 text-gray-600'
                  }`}
                >
                  {num}
                </button>
              ))}
            </div>
            <div className="flex justify-between text-sm text-gray-500 px-6">
              <span>Low</span>
              <span>High</span>
            </div>
          </div>
        );
        
      case 'choice':
        return (
          <div className="space-y-3">
            {['Yes', 'No', 'Partially', 'Not sure'].map(option => (
              <button
                key={option}
                onClick={() => onChange(option)}
                className={`w-full p-3 rounded-lg border-2 text-left transition-all ${
                  value === option
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-300'
                }`}
              >
                {option}
              </button>
            ))}
          </div>
        );
        
      default:
        return <div>Input type not supported</div>;
    }
  };

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold text-calm-800">{input.label}</h3>
      {input.required && <p className="text-sm text-gray-500">* Required</p>}
      {renderInput()}
    </div>
  );
}

function CompletionStep({ exercise }: { exercise: TherapyExercise }) {
  return (
    <div className="text-center space-y-6">
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5, type: "spring" }}
        className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto"
      >
        <FontAwesomeIcon icon={'check' as IconProp} className="w-10 h-10 text-green-600" />
      </motion.div>
      
      <h3 className="text-2xl font-bold text-calm-800">Exercise Complete!</h3>
      <p className="text-calm-600 text-lg">
        Great job completing the {exercise.name} exercise. Your responses have been saved and will help inform your personalized recommendations.
      </p>
      
      {exercise.evidenceBase && (
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-blue-800 text-sm">
            <FontAwesomeIcon icon={'lightbulb' as IconProp} className="w-4 h-4 mr-2" />
            <strong>Evidence Base:</strong> {exercise.evidenceBase}
          </p>
        </div>
      )}
    </div>
  );
}
