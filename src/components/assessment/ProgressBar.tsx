'use client';

import { motion } from 'framer-motion';
import { FontAwesomeIcon, IconProp } from '@/lib/fontawesome';

interface ProgressBarProps {
  progress: number;
  currentStep: number;
  totalSteps: number;
  assessmentTitle: string;
  onExit: () => void;
  onBack?: () => void;
}

export default function ProgressBar({
  progress,
  currentStep,
  totalSteps,
  assessmentTitle,
  onExit,
  onBack
}: ProgressBarProps) {
  return (
    <div className="relative z-20 bg-white/90 backdrop-blur-sm border-b border-white/20 px-4 py-4">
      <div className="container mx-auto">
        <div className="flex items-center justify-between mb-4">
          {/* Left - Back button */}
          <div className="flex items-center space-x-4">
            {onBack && (
              <button
                onClick={onBack}
                className="p-2 rounded-lg bg-white/50 hover:bg-white/70 transition-colors border border-white/30"
                title="Go back"
              >
                <FontAwesomeIcon icon={'arrow-left' as IconProp} className="w-5 h-5 text-calm-600" />
              </button>
            )}
            <div>
              <h1 className="text-lg font-semibold text-calm-800">
                {assessmentTitle}
              </h1>
              <p className="text-sm text-calm-600">
                Question {currentStep} of {totalSteps}
              </p>
            </div>
          </div>

          {/* Right - Exit button */}
          <button
            onClick={onExit}
            className="p-2 rounded-lg bg-white/50 hover:bg-white/70 transition-colors border border-white/30"
            title="Exit assessment"
          >
            <FontAwesomeIcon icon={'xmark' as IconProp} className="w-5 h-5 text-calm-600" />
          </button>
        </div>

        {/* Progress Bar */}
        <div className="relative">
          <div className="w-full bg-white/30 rounded-full h-3 overflow-hidden">
            <motion.div
              className="bg-gradient-to-r from-primary-400 to-primary-600 h-full rounded-full relative"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
            >
              {/* Animated glow effect */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-primary-300 to-primary-500 opacity-50"
                animate={{
                  scale: [1, 1.1, 1],
                  opacity: [0.5, 0.8, 0.5]
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: 'easeInOut'
                }}
              />
            </motion.div>
          </div>

          {/* Progress text */}
          <div className="flex justify-between text-xs text-calm-600 mt-2">
            <span>Started</span>
            <span className="font-medium">
              {Math.round(progress)}% Complete
            </span>
            <span>Report</span>
          </div>

          {/* Step indicators */}
          <div className="flex justify-between absolute -top-1 w-full">
            {Array.from({ length: Math.min(totalSteps, 10) }, (_, index) => {
              const stepNumber = Math.floor((index * totalSteps) / 10) + 1;
              const isCompleted = stepNumber <= currentStep;
              const isCurrent = stepNumber === currentStep;
              
              return (
                <motion.div
                  key={index}
                  className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all duration-300 ${
                    isCompleted || isCurrent
                      ? 'bg-primary-500 border-primary-500'
                      : 'bg-white/50 border-white/30'
                  }`}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                >
                  {isCurrent && (
                    <motion.div
                      className="w-2 h-2 bg-white rounded-full"
                      animate={{
                        scale: [1, 1.2, 1],
                      }}
                      transition={{
                        duration: 1.5,
                        repeat: Infinity,
                        ease: 'easeInOut'
                      }}
                    />
                  )}
                  {isCompleted && !isCurrent && (
                    <div className="w-2 h-2 bg-white rounded-full" />
                  )}
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
