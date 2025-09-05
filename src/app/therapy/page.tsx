'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconProp } from '@fortawesome/fontawesome-svg-core';
import { Assessment, AssessmentType, UserProgress, TherapyRecommendation } from '@/types';
import { StorageService } from '@/utils/storage';
import { therapyEngine } from '@/lib/therapy-engine';
import TherapyDashboard from '@/components/therapy/TherapyDashboard';

export default function TherapyPage() {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [userProgress, setUserProgress] = useState<UserProgress | null>(null);
  const [recommendations, setRecommendations] = useState<TherapyRecommendation[]>([]);
  const [selectedTherapy, setSelectedTherapy] = useState<AssessmentType>('general');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      setLoading(true);
      
      // Load assessments
      const userAssessments = StorageService.getAssessments();
      setAssessments(userAssessments);

      // Load or create user progress
      let progress = loadUserProgress();
      if (!progress) {
        progress = createInitialProgress();
        saveUserProgress(progress);
      }
      setUserProgress(progress);

      // Generate recommendations from most recent assessment
      if (userAssessments.length > 0) {
        const latestAssessment = userAssessments[userAssessments.length - 1];
        const therapyRecommendations = await therapyEngine.generateRecommendations(latestAssessment);
        setRecommendations(therapyRecommendations);
        
        // Set primary therapy from recommendations
        if (therapyRecommendations.length > 0) {
          setSelectedTherapy(therapyRecommendations[0].therapyType);
        }
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUserProgress = (): UserProgress | null => {
    try {
      const stored = localStorage.getItem('userProgress');
      if (stored) {
        const progress = JSON.parse(stored);
        // Convert date strings back to Date objects
        progress.lastActiveDate = new Date(progress.lastActiveDate);
        progress.achievements = progress.achievements.map((achievement: any) => ({
          ...achievement,
          earnedDate: achievement.earnedDate ? new Date(achievement.earnedDate) : undefined
        }));
        return progress;
      }
    } catch (error) {
      console.error('Error loading user progress:', error);
    }
    return null;
  };

  const createInitialProgress = (): UserProgress => {
    return {
      userId: 'current-user',
      currentStreak: 0,
      longestStreak: 0,
      totalExercisesCompleted: 0,
      skillLevels: {},
      achievements: [],
      preferredTherapies: [],
      lastActiveDate: new Date()
    };
  };

  const saveUserProgress = (progress: UserProgress) => {
    try {
      localStorage.setItem('userProgress', JSON.stringify(progress));
    } catch (error) {
      console.error('Error saving user progress:', error);
    }
  };

  const handleProgressUpdate = (updatedProgress: UserProgress) => {
    setUserProgress(updatedProgress);
    saveUserProgress(updatedProgress);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-nature-50 flex items-center justify-center">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"
          />
          <p className="text-calm-600">Loading your therapy center...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-nature-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center"
          >
            <h1 className="text-4xl font-bold text-gradient mb-4">Therapy Center</h1>
            <p className="text-xl text-calm-600 max-w-3xl mx-auto">
              Practice evidence-based exercises tailored to your needs. Build skills, track progress, 
              and develop lasting mental health habits.
            </p>
          </motion.div>

          {/* Recommendations Summary */}
          {recommendations.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="mt-8 bg-gradient-to-r from-primary-500 to-nature-500 rounded-lg p-6 text-white"
            >
              <div className="flex items-center space-x-3 mb-4">
                <FontAwesomeIcon icon={'lightbulb' as IconProp} className="w-6 h-6" />
                <h2 className="text-xl font-semibold">Personalized Recommendations</h2>
              </div>
              <p className="text-primary-100 mb-4">
                Based on your assessment, we recommend focusing on these therapeutic approaches:
              </p>
              <div className="flex flex-wrap gap-2">
                {recommendations.slice(0, 3).map((rec, index) => (
                  <span
                    key={rec.therapyType}
                    className={`px-3 py-1 rounded-full text-sm font-medium ${
                      index === 0 
                        ? 'bg-white text-primary-600' 
                        : 'bg-primary-600 text-white border border-primary-400'
                    }`}
                  >
                    {rec.therapyType.replace('-', ' ').replace(/^\w/, c => c.toUpperCase())}
                    {index === 0 && ' (Primary)'}
                  </span>
                ))}
              </div>
            </motion.div>
          )}
        </div>
      </div>

      {/* No Assessments State */}
      {assessments.length === 0 && (
        <div className="max-w-4xl mx-auto px-6 py-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center bg-white rounded-lg p-12 shadow-lg"
          >
            <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <FontAwesomeIcon icon={'stethoscope' as IconProp} className="w-10 h-10 text-primary-600" />
            </div>
            <h2 className="text-2xl font-bold text-calm-800 mb-4">Start Your Journey</h2>
            <p className="text-calm-600 mb-8 max-w-2xl mx-auto">
              To get personalized therapy recommendations and exercises, take your first assessment. 
              This will help us understand your unique needs and suggest the most effective approaches.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.a
                href="/"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-primary"
              >
                <FontAwesomeIcon icon={'play' as IconProp} className="w-4 h-4 mr-2" />
                Take Assessment
              </motion.a>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setSelectedTherapy('general')}
                className="btn-secondary"
              >
                <FontAwesomeIcon icon={'heart' as IconProp} className="w-4 h-4 mr-2" />
                Explore General Exercises
              </motion.button>
            </div>
          </motion.div>
        </div>
      )}

      {/* Therapy Dashboard */}
      {(assessments.length > 0 || selectedTherapy === 'general') && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <TherapyDashboard
            primaryTherapy={selectedTherapy}
            userProgress={userProgress || undefined}
            onProgressUpdate={handleProgressUpdate}
          />
        </motion.div>
      )}

      {/* Assessment History */}
      {assessments.length > 0 && (
        <div className="max-w-6xl mx-auto px-6 py-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg border p-6"
          >
            <h3 className="text-xl font-bold text-calm-800 mb-4">Your Assessment History</h3>
            <div className="space-y-3">
              {assessments.slice(-5).reverse().map(assessment => (
                <div
                  key={assessment.id}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                      <FontAwesomeIcon 
                        icon={'brain' as IconProp} 
                        className="w-5 h-5 text-primary-600" 
                      />
                    </div>
                    <div>
                      <p className="font-medium text-gray-800 capitalize">
                        {assessment.type.replace('-', ' ')} Assessment
                      </p>
                      <p className="text-sm text-gray-500">
                        Completed {assessment.completedAt?.toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-500">
                      {assessment.responses.length} questions
                    </span>
                    <motion.a
                      href={`/dashboard`}
                      whileHover={{ scale: 1.05 }}
                      className="text-primary-600 hover:text-primary-700 transition-colors"
                    >
                      <FontAwesomeIcon icon={'arrow-right' as IconProp} className="w-4 h-4" />
                    </motion.a>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
}
