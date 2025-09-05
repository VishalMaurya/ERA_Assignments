'use client';

import { motion } from 'framer-motion';
import { FontAwesomeIcon, IconProp } from '@/lib/fontawesome';
import { AssessmentType } from '@/types';
import { getAssessmentTitle } from '@/utils/helpers';

interface ReportGenerationProps {
  assessmentType: AssessmentType;
  stage: string;
  onCancel: () => void;
}

export default function ReportGeneration({ assessmentType, stage, onCancel }: ReportGenerationProps) {
  const stages = [
    {
      title: 'Collecting reflections',
      description: 'Gathering your responses...',
      icon: 'file-text' as IconProp,
      color: 'text-blue-500',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Analyzing patterns',
      description: 'AI is identifying behavioral patterns...',
      icon: 'brain' as IconProp,
      color: 'text-purple-500',
      bgColor: 'bg-purple-100'
    },
    {
      title: 'Building recommendations',
      description: 'Creating personalized guidance...',
      icon: 'wand-sparkles' as IconProp,
      color: 'text-emerald-500',
      bgColor: 'bg-emerald-100'
    }
  ];

  const getCurrentStageIndex = () => {
    if (stage.includes('Analyzing') || stage.includes('patterns')) return 1;
    if (stage.includes('recommendations') || stage.includes('Generating')) return 2;
    return 0;
  };

  const currentStageIndex = getCurrentStageIndex();

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        {/* Neural network animation */}
        {Array.from({ length: 20 }, (_, i) => (
          <motion.div
            key={`node-${i}`}
            className="absolute w-2 h-2 bg-white rounded-full opacity-30"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              scale: [1, 1.5, 1],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: 2 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}

        {/* Data streams */}
        {Array.from({ length: 8 }, (_, i) => (
          <motion.div
            key={`stream-${i}`}
            className="absolute h-px bg-gradient-to-r from-transparent via-white to-transparent opacity-20"
            style={{
              width: '200px',
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              x: [-200, window.innerWidth || 1200],
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 3,
              ease: 'linear',
            }}
          />
        ))}

        {/* Floating particles */}
        {Array.from({ length: 15 }, (_, i) => (
          <motion.div
            key={`particle-${i}`}
            className="absolute w-1 h-1 bg-white rounded-full opacity-40"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -100, 0],
              x: [0, Math.random() * 50 - 25, 0],
              opacity: [0.2, 0.6, 0.2],
            }}
            transition={{
              duration: 4 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto px-4 py-16 flex items-center justify-center min-h-screen">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-2xl"
        >
          {/* Cancel Button */}
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            onClick={onCancel}
            className="absolute top-8 right-8 p-3 rounded-full bg-white/10 hover:bg-white/20 transition-colors"
          >
            <FontAwesomeIcon icon={'xmark' as IconProp} className="w-6 h-6 text-white" />
          </motion.button>

          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mb-12"
          >
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Generating Your Report
            </h1>
            <h2 className="text-xl text-purple-200 mb-6">
              {getAssessmentTitle(assessmentType)}
            </h2>
            <p className="text-purple-100 text-lg">
              Our AI is carefully analyzing your responses to create personalized insights and recommendations.
            </p>
          </motion.div>

          {/* AI Brain Animation */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ 
              type: 'spring', 
              stiffness: 200, 
              damping: 15,
              delay: 0.4 
            }}
            className="mb-12"
          >
            <div className="relative w-32 h-32 mx-auto">
              <motion.div
                className="w-full h-full bg-gradient-to-br from-blue-400 to-purple-600 rounded-full flex items-center justify-center shadow-2xl"
                animate={{
                  scale: [1, 1.1, 1],
                  rotate: [0, 5, -5, 0],
                }}
                transition={{
                  duration: 4,
                  repeat: Infinity,
                  ease: 'easeInOut',
                }}
              >
                <FontAwesomeIcon icon={'brain' as IconProp} className="w-16 h-16 text-white" />
              </motion.div>
              
              {/* Pulse rings */}
              {Array.from({ length: 3 }, (_, i) => (
                <motion.div
                  key={i}
                  className="absolute inset-0 border-2 border-white/30 rounded-full"
                  animate={{
                    scale: [1, 2, 1],
                    opacity: [0.5, 0, 0.5],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    delay: i * 0.7,
                  }}
                />
              ))}
            </div>
          </motion.div>

          {/* Progress Stages */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="space-y-6 mb-8"
          >
            {stages.map((stageInfo, index) => {
              const isActive = index === currentStageIndex;
              const isCompleted = index < currentStageIndex;
              
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.8 + index * 0.2 }}
                  className={`flex items-center space-x-4 p-4 rounded-lg transition-all duration-500 ${
                    isActive
                      ? 'bg-white/20 border border-white/30 shadow-lg'
                      : isCompleted
                        ? 'bg-white/10 border border-white/20'
                        : 'bg-white/5 border border-white/10'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-500 ${
                    isActive
                      ? stageInfo.bgColor + ' ' + stageInfo.color + ' animate-pulse'
                      : isCompleted
                        ? 'bg-emerald-100 text-emerald-600'
                        : 'bg-white/10 text-white/50'
                  }`}>
                    {isCompleted ? (
                      <motion.svg
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-6 h-6"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </motion.svg>
                                          ) : (
                      <FontAwesomeIcon icon={stageInfo.icon} className="w-6 h-6" />
                    )}
                  </div>
                  
                  <div className="flex-1 text-left">
                    <h3 className={`font-semibold transition-colors duration-500 ${
                      isActive || isCompleted ? 'text-white' : 'text-white/70'
                    }`}>
                      {stageInfo.title}
                    </h3>
                    <p className={`text-sm transition-colors duration-500 ${
                      isActive || isCompleted ? 'text-white/80' : 'text-white/50'
                    }`}>
                      {isActive ? stage : stageInfo.description}
                    </p>
                  </div>
                  
                  {isActive && (
                    <motion.div
                      className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    />
                  )}
                </motion.div>
              );
            })}
          </motion.div>

          {/* Current Stage Display */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 1.2 }}
            className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20"
          >
            <p className="text-white/90 text-lg font-medium">
              {stage || 'Preparing your personalized report...'}
            </p>
            <div className="mt-4 w-full bg-white/20 rounded-full h-2 overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-blue-400 to-purple-500 rounded-full"
                initial={{ width: '0%' }}
                animate={{ width: `${((currentStageIndex + 1) / stages.length) * 100}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
              />
            </div>
          </motion.div>

          {/* Footer */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 1.4 }}
            className="text-purple-200 text-sm mt-8"
          >
            This typically takes 30-60 seconds. Thank you for your patience.
          </motion.p>
        </motion.div>
      </div>
    </div>
  );
}
