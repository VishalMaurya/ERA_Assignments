'use client';

import { motion } from 'framer-motion';
import { FontAwesomeIcon, IconProp } from '@/lib/fontawesome';
import { Assessment, AssessmentType } from '@/types';
import { getCompletionMessage, getAssessmentTitle } from '@/utils/helpers';
import Confetti from 'react-confetti';
import { useState, useEffect } from 'react';

interface JourneyCompleteProps {
  assessment: Assessment;
  onGenerateReport: () => void;
  onReturnHome: () => void;
}

export default function JourneyComplete({
  assessment,
  onGenerateReport,
  onReturnHome
}: JourneyCompleteProps) {
  const [windowSize, setWindowSize] = useState({ width: 0, height: 0 });
  const [showConfetti, setShowConfetti] = useState(true);

  useEffect(() => {
    const updateWindowSize = () => {
      setWindowSize({ width: window.innerWidth, height: window.innerHeight });
    };

    updateWindowSize();
    window.addEventListener('resize', updateWindowSize);

    // Hide confetti after 5 seconds
    const timer = setTimeout(() => setShowConfetti(false), 5000);

    return () => {
      window.removeEventListener('resize', updateWindowSize);
      clearTimeout(timer);
    };
  }, []);

  // Calculate real statistics from assessment data
  const calculateStats = () => {
    const totalQuestions = assessment.questions.length;
    const answeredQuestions = assessment.responses.length;
    const skippedQuestions = assessment.skippedQuestions.length;
    const completionPercentage = Math.round((answeredQuestions / totalQuestions) * 100);
    
    // Calculate total time taken from start to end
    let totalTimeMinutes = 0;
    if (assessment.completedAt && assessment.startedAt) {
      try {
        const completedAt = typeof assessment.completedAt === 'string' 
          ? new Date(assessment.completedAt) 
          : assessment.completedAt;
        const startedAt = typeof assessment.startedAt === 'string' 
          ? new Date(assessment.startedAt) 
          : assessment.startedAt;
        
        const timeDiffMs = completedAt.getTime() - startedAt.getTime();
        totalTimeMinutes = Math.round(timeDiffMs / (1000 * 60)); // in minutes
      } catch (error) {
        console.warn('Error calculating total time:', error);
        totalTimeMinutes = 0;
      }
    }
    
    // Calculate time from individual responses (sum of time spent on each question)
    const responseTimeSeconds = assessment.responses.reduce((acc, response) => {
      return acc + (response.timeSpent || 0);
    }, 0);
    const responseTimeMinutes = Math.round(responseTimeSeconds / 60);
    
    // Use individual response times if available, otherwise use total time
    let finalTimeMinutes = responseTimeMinutes > 0 ? responseTimeMinutes : totalTimeMinutes;
    
    // Format time display - never show N/A
    let timeDisplay: string;
    if (finalTimeMinutes <= 0) {
      timeDisplay = '< 1m';
    } else if (finalTimeMinutes >= 60) {
      const hours = Math.floor(finalTimeMinutes / 60);
      const minutes = finalTimeMinutes % 60;
      timeDisplay = minutes > 0 ? `${hours}h ${minutes}m` : `${hours}h`;
    } else {
      timeDisplay = `${finalTimeMinutes}m`;
    }
    
    // Calculate average time per question - never show N/A
    const avgTimePerQuestion = answeredQuestions > 0 ? Math.round(responseTimeSeconds / answeredQuestions) : 0;
    const avgTimeDisplay = avgTimePerQuestion <= 0 ? '< 1s' : `${avgTimePerQuestion}s`;
    
    return {
      totalQuestions,
      answeredQuestions,
      skippedQuestions,
      completionPercentage,
      timeSpent: timeDisplay,
      avgTimePerQuestion: avgTimeDisplay,
      totalTimeMinutes: finalTimeMinutes
    };
  };

  const stats = calculateStats();
  
  const completionStats = [
    { 
      icon: 'check-circle' as IconProp, 
      label: 'Questions Answered', 
      value: `${stats.answeredQuestions}/${stats.totalQuestions}`,
      description: `${stats.completionPercentage}% complete`
    },
    { 
      icon: 'clock' as IconProp, 
      label: 'Total Time', 
      value: stats.timeSpent,
      description: stats.totalTimeMinutes > 0 ? 'Well invested!' : 'Quick session'
    },
    { 
      icon: 'wand-sparkles' as IconProp, 
      label: 'Avg. per Question', 
      value: stats.avgTimePerQuestion,
      description: 'Thoughtful responses'
    },
    ...(stats.skippedQuestions > 0 ? [{
      icon: 'forward' as IconProp,
      label: 'Questions Skipped',
      value: `${stats.skippedQuestions}`,
      description: "That's okay!"
    }] : [])
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-900 via-teal-800 to-cyan-900 relative overflow-hidden">
      {/* Confetti */}
      {showConfetti && windowSize.width > 0 && (
        <Confetti
          width={windowSize.width}
          height={windowSize.height}
          recycle={false}
          numberOfPieces={200}
          gravity={0.1}
        />
      )}

      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        {/* Floating orbs */}
        {Array.from({ length: 8 }, (_, i) => (
          <motion.div
            key={i}
            className="absolute rounded-full bg-white/10"
            style={{
              width: `${60 + Math.random() * 40}px`,
              height: `${60 + Math.random() * 40}px`,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -30, 0],
              x: [0, 15, 0],
              scale: [1, 1.1, 1],
              opacity: [0.3, 0.6, 0.3],
            }}
            transition={{
              duration: 4 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}

        {/* Success rays */}
        {Array.from({ length: 12 }, (_, i) => (
          <motion.div
            key={`ray-${i}`}
            className="absolute top-1/2 left-1/2 w-1 bg-gradient-to-t from-transparent via-emerald-300 to-transparent opacity-20"
            style={{
              height: '40vh',
              transformOrigin: 'bottom center',
              rotate: `${i * 30}deg`,
            }}
            animate={{
              scaleY: [0.5, 1.2, 0.5],
              opacity: [0.1, 0.3, 0.1],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              delay: i * 0.2,
            }}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto px-4 py-16 flex items-center justify-center min-h-screen">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-2xl"
        >
          {/* Success Icon */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ 
              type: 'spring', 
              stiffness: 200, 
              damping: 10,
              delay: 0.3 
            }}
            className="w-24 h-24 bg-emerald-400 rounded-full flex items-center justify-center mx-auto mb-8 shadow-2xl"
          >
            <FontAwesomeIcon icon={'check-circle' as IconProp} className="w-12 h-12 text-white" />
          </motion.div>

          {/* Completion Message */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="mb-8"
          >
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Journey Complete! 🎉
            </h1>
            <h2 className="text-xl md:text-2xl text-emerald-200 mb-6">
              {getAssessmentTitle(assessment.type)}
            </h2>
            <p className="text-lg text-emerald-100 leading-relaxed">
              {getCompletionMessage(assessment.type)}
            </p>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.7 }}
            className="grid md:grid-cols-3 gap-4 mb-10"
          >
            {completionStats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.8 + index * 0.1 }}
                className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20 hover:bg-white/15 transition-colors"
              >
                <FontAwesomeIcon icon={stat.icon} className="w-6 h-6 text-emerald-300 mx-auto mb-2" />
                <div className="text-white font-semibold text-lg">{stat.value}</div>
                <div className="text-emerald-200 text-sm font-medium">{stat.label}</div>
                {stat.description && (
                  <div className="text-emerald-300 text-xs mt-1 opacity-80">{stat.description}</div>
                )}
              </motion.div>
            ))}
          </motion.div>

          {/* Appreciation Message */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.9 }}
            className="bg-white/10 backdrop-blur-sm rounded-lg p-6 mb-8 border border-white/20"
          >
            <h3 className="text-xl font-semibold text-white mb-3">
              Thank You for Your Openness 💙
            </h3>
            <p className="text-emerald-100">
              Taking this assessment shows courage and self-awareness. Your willingness to explore 
              your mental health is the first step toward positive change and growth.
            </p>
          </motion.div>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.1 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <button
              onClick={onGenerateReport}
              className="flex items-center justify-center space-x-3 bg-emerald-500 hover:bg-emerald-600 text-white font-semibold px-8 py-4 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
            >
              <FontAwesomeIcon icon={'file-text' as IconProp} className="w-5 h-5" />
              <span>Generate My Report</span>
              <FontAwesomeIcon icon={'wand-sparkles' as IconProp} className="w-5 h-5" />
            </button>

            <button
              onClick={onReturnHome}
              className="flex items-center justify-center space-x-3 bg-white/20 hover:bg-white/30 text-white font-semibold px-8 py-4 rounded-lg transition-all duration-300 border border-white/30"
            >
              <FontAwesomeIcon icon={'home' as IconProp} className="w-5 h-5" />
              <span>Return Home</span>
            </button>
          </motion.div>

          {/* Next Steps Preview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.3 }}
            className="mt-8 text-center"
          >
            <p className="text-emerald-200 text-sm">
              Your personalized report will include insights, patterns, and evidence-based 
              recommendations tailored to your responses.
            </p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
