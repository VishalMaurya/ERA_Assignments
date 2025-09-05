'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconProp } from '@fortawesome/fontawesome-svg-core';
import { TherapyExercise, ExerciseSession, AssessmentType, Achievement, UserProgress } from '@/types';
import { therapyExercises, universalExercises } from '@/data/exercises';
import { therapyEngine } from '@/lib/therapy-engine';
import ExercisePlayer from './ExercisePlayer';

interface TherapyDashboardProps {
  primaryTherapy?: AssessmentType;
  userProgress?: UserProgress;
  onProgressUpdate?: (progress: UserProgress) => void;
}

export default function TherapyDashboard({ 
  primaryTherapy = 'general', 
  userProgress,
  onProgressUpdate 
}: TherapyDashboardProps) {
  const [activeTab, setActiveTab] = useState<'exercises' | 'progress' | 'achievements'>('exercises');
  const [selectedTherapy, setSelectedTherapy] = useState<AssessmentType>(primaryTherapy);
  const [activeExercise, setActiveExercise] = useState<TherapyExercise | null>(null);
  const [completedSessions, setCompletedSessions] = useState<ExerciseSession[]>([]);
  const [filterDifficulty, setFilterDifficulty] = useState<'all' | 'beginner' | 'intermediate' | 'advanced'>('all');

  // Get available exercises for selected therapy
  const availableExercises = [
    ...(therapyExercises[selectedTherapy] || []),
    ...universalExercises
  ].filter(exercise => 
    filterDifficulty === 'all' || exercise.difficulty === filterDifficulty
  );

  // Handle exercise completion
  const handleExerciseComplete = (session: ExerciseSession) => {
    setCompletedSessions(prev => [...prev, session]);
    setActiveExercise(null);
    
    // Update user progress
    if (userProgress && onProgressUpdate) {
      const updatedProgress: UserProgress = {
        ...userProgress,
        totalExercisesCompleted: userProgress.totalExercisesCompleted + 1,
        lastActiveDate: new Date(),
        currentStreak: calculateNewStreak(userProgress),
        skillLevels: {
          ...userProgress.skillLevels,
          [selectedTherapy]: Math.min(100, (userProgress.skillLevels[selectedTherapy] || 0) + 5)
        }
      };
      onProgressUpdate(updatedProgress);
    }
  };

  const calculateNewStreak = (progress: UserProgress): number => {
    const today = new Date();
    const lastActive = new Date(progress.lastActiveDate);
    const daysDiff = Math.floor((today.getTime() - lastActive.getTime()) / (1000 * 60 * 60 * 24));
    
    if (daysDiff <= 1) {
      return progress.currentStreak + 1;
    }
    return 1; // Reset streak
  };

  const getTherapyIcon = (therapy: AssessmentType): IconProp => {
    const iconMap: Record<AssessmentType, IconProp> = {
      anxiety: 'brain',
      ocd: 'bullseye',
      'behavioral-activation': 'play',
      'habit-reversal': 'arrow-right',
      'problem-solving': 'lightbulb',
      mindfulness: 'leaf',
      'acceptance-commitment': 'heart',
      'mindful-cognitive': 'tree',
      anger: 'fire',
      'emotion-regulation': 'heart',
      interpersonal: 'user',
      'self-compassion': 'heart',
      'positive-psychology': 'sun',
      strengths: 'award',
      sleep: 'moon',
      relaxation: 'cloud',
      breathing: 'cloud',
      exercise: 'play',
      nutrition: 'heart',
      trauma: 'shield-alt',
      schema: 'chart-bar',
      narrative: 'book-open',
      motivation: 'arrow-up',
      'solution-focused': 'lightbulb',
      general: 'heart'
    };
    return iconMap[therapy] || 'question';
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'text-green-600 bg-green-100';
      case 'intermediate': return 'text-yellow-600 bg-yellow-100';
      case 'advanced': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-calm-800 mb-2">Therapy Center</h1>
        <p className="text-calm-600">Practice evidence-based exercises to build your mental health skills</p>
      </div>

      {/* Quick Stats */}
      {userProgress && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-gradient-to-r from-primary-500 to-nature-500 text-white rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-primary-100 text-sm">Current Streak</p>
                <p className="text-2xl font-bold">{userProgress.currentStreak} days</p>
              </div>
              <FontAwesomeIcon icon={'fire' as IconProp} className="w-8 h-8 text-primary-200" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg border p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Exercises Completed</p>
                <p className="text-2xl font-bold text-gray-800">{userProgress.totalExercisesCompleted}</p>
              </div>
              <FontAwesomeIcon icon={'check-circle' as IconProp} className="w-8 h-8 text-green-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg border p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Achievements</p>
                <p className="text-2xl font-bold text-gray-800">{userProgress.achievements.length}</p>
              </div>
              <FontAwesomeIcon icon={'award' as IconProp} className="w-8 h-8 text-yellow-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg border p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Skill Level</p>
                <p className="text-2xl font-bold text-gray-800">
                  {Math.round(Object.values(userProgress.skillLevels).reduce((a, b) => a + b, 0) / 
                    Math.max(1, Object.keys(userProgress.skillLevels).length))}%
                </p>
              </div>
              <FontAwesomeIcon icon={'chart-line' as IconProp} className="w-8 h-8 text-blue-500" />
            </div>
          </div>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-8">
          {[
            { key: 'exercises', label: 'Exercises', icon: 'play' },
            { key: 'progress', label: 'Progress', icon: 'chart-line' },
            { key: 'achievements', label: 'Achievements', icon: 'award' }
          ].map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.key
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <FontAwesomeIcon icon={tab.icon as IconProp} className="w-4 h-4 mr-2" />
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Content */}
      <AnimatePresence mode="wait">
        {activeTab === 'exercises' && (
          <motion.div
            key="exercises"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-6"
          >
            {/* Therapy Selection & Filters */}
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
              <div className="flex flex-wrap gap-2">
                {Object.keys(therapyExercises).slice(0, 8).map(therapy => (
                  <button
                    key={therapy}
                    onClick={() => setSelectedTherapy(therapy as AssessmentType)}
                    className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors ${
                      selectedTherapy === therapy
                        ? 'bg-primary-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    <FontAwesomeIcon icon={getTherapyIcon(therapy as AssessmentType)} className="w-4 h-4" />
                    <span className="capitalize">{therapy.replace('-', ' ')}</span>
                  </button>
                ))}
              </div>
              
              <select
                value={filterDifficulty}
                onChange={(e) => setFilterDifficulty(e.target.value as any)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">All Difficulties</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            {/* Exercise Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {availableExercises.map(exercise => (
                <motion.div
                  key={exercise.id}
                  layout
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  whileHover={{ y: -4 }}
                  className="bg-white rounded-lg border hover:border-primary-300 hover:shadow-lg transition-all cursor-pointer"
                  onClick={() => setActiveExercise(exercise)}
                >
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                          <FontAwesomeIcon 
                            icon={getTherapyIcon(exercise.therapyType)} 
                            className="w-5 h-5 text-primary-600" 
                          />
                        </div>
                        <div>
                          <h3 className="font-semibold text-calm-800">{exercise.name}</h3>
                          <div className="flex items-center space-x-2 mt-1">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(exercise.difficulty)}`}>
                              {exercise.difficulty}
                            </span>
                            <span className="text-xs text-gray-500">{exercise.estimatedDuration}min</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <p className="text-calm-600 text-sm mb-4 line-clamp-3">{exercise.description}</p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center text-xs text-gray-500">
                        <FontAwesomeIcon icon={'lightbulb' as IconProp} className="w-3 h-3 mr-1" />
                        {exercise.learningObjectives.length} objectives
                      </div>
                      <button className="text-primary-600 hover:text-primary-700 transition-colors">
                        <FontAwesomeIcon icon={'play' as IconProp} className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {activeTab === 'progress' && (
          <motion.div
            key="progress"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <ProgressView userProgress={userProgress} completedSessions={completedSessions} />
          </motion.div>
        )}

        {activeTab === 'achievements' && (
          <motion.div
            key="achievements"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <AchievementsView userProgress={userProgress} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Exercise Player Modal */}
      <AnimatePresence>
        {activeExercise && (
          <ExercisePlayer
            exercise={activeExercise}
            onComplete={handleExerciseComplete}
            onClose={() => setActiveExercise(null)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

// Progress View Component
function ProgressView({ userProgress, completedSessions }: { 
  userProgress?: UserProgress; 
  completedSessions: ExerciseSession[];
}) {
  if (!userProgress) {
    return (
      <div className="text-center py-12">
        <FontAwesomeIcon icon={'chart-line' as IconProp} className="w-16 h-16 text-gray-300 mb-4" />
        <p className="text-gray-500">Complete some exercises to see your progress</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Skill Levels */}
      <div className="bg-white rounded-lg border p-6">
        <h3 className="text-xl font-bold text-calm-800 mb-4">Skill Development</h3>
        <div className="space-y-4">
          {Object.entries(userProgress.skillLevels).map(([therapy, level]) => (
            <div key={therapy}>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700 capitalize">
                  {therapy.replace('-', ' ')}
                </span>
                <span className="text-sm text-gray-500">{level}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <motion.div
                  className="bg-primary-500 rounded-full h-2"
                  initial={{ width: 0 }}
                  animate={{ width: `${level}%` }}
                  transition={{ duration: 1, delay: 0.2 }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Sessions */}
      <div className="bg-white rounded-lg border p-6">
        <h3 className="text-xl font-bold text-calm-800 mb-4">Recent Exercise Sessions</h3>
        {completedSessions.length === 0 ? (
          <p className="text-gray-500">No completed sessions yet</p>
        ) : (
          <div className="space-y-3">
            {completedSessions.slice(-5).reverse().map(session => (
              <div key={session.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-800">Exercise {session.exerciseId}</p>
                  <p className="text-sm text-gray-500">
                    {session.startTime.toLocaleDateString()}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-green-600">Completed</p>
                  {session.mood && (
                    <p className="text-xs text-gray-500">
                      Mood: {session.mood.before} → {session.mood.after}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// Achievements View Component
function AchievementsView({ userProgress }: { userProgress?: UserProgress }) {
  const allAchievements: Achievement[] = [
    {
      id: 'first_exercise',
      name: 'First Steps',
      description: 'Complete your first therapy exercise',
      icon: 'play',
      criteria: { type: 'completion', threshold: 1, metric: 'exercises' },
      rarity: 'common'
    },
    {
      id: 'streak_7',
      name: 'Week Warrior',
      description: 'Maintain a 7-day practice streak',
      icon: 'fire',
      criteria: { type: 'streak', threshold: 7, metric: 'days' },
      rarity: 'uncommon'
    },
    {
      id: 'exercises_25',
      name: 'Dedicated Practitioner',
      description: 'Complete 25 therapy exercises',
      icon: 'award',
      criteria: { type: 'completion', threshold: 25, metric: 'exercises' },
      rarity: 'rare'
    },
    {
      id: 'skill_master',
      name: 'Skill Master',
      description: 'Reach 80% skill level in any therapy area',
      icon: 'star',
      criteria: { type: 'improvement', threshold: 80, metric: 'skill_level' },
      rarity: 'legendary'
    }
  ];

  const earnedAchievements = userProgress?.achievements || [];
  const availableAchievements = allAchievements.filter(
    achievement => !earnedAchievements.some(earned => earned.id === achievement.id)
  );

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case 'common': return 'border-gray-300 bg-gray-50';
      case 'uncommon': return 'border-green-300 bg-green-50';
      case 'rare': return 'border-blue-300 bg-blue-50';
      case 'legendary': return 'border-purple-300 bg-purple-50';
      default: return 'border-gray-300 bg-gray-50';
    }
  };

  return (
    <div className="space-y-8">
      {/* Earned Achievements */}
      <div>
        <h3 className="text-xl font-bold text-calm-800 mb-4">Earned Achievements</h3>
        {earnedAchievements.length === 0 ? (
          <p className="text-gray-500">Complete exercises to earn achievements</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {earnedAchievements.map(achievement => (
              <motion.div
                key={achievement.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`p-4 rounded-lg border-2 ${getRarityColor(achievement.rarity)}`}
              >
                <div className="flex items-center space-x-3">
                  <FontAwesomeIcon icon={achievement.icon as IconProp} className="w-8 h-8 text-yellow-500" />
                  <div>
                    <h4 className="font-semibold text-gray-800">{achievement.name}</h4>
                    <p className="text-sm text-gray-600">{achievement.description}</p>
                    {achievement.earnedDate && (
                      <p className="text-xs text-gray-500 mt-1">
                        Earned {achievement.earnedDate.toLocaleDateString()}
                      </p>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Available Achievements */}
      <div>
        <h3 className="text-xl font-bold text-calm-800 mb-4">Available Achievements</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {availableAchievements.map(achievement => (
            <div
              key={achievement.id}
              className={`p-4 rounded-lg border-2 opacity-75 ${getRarityColor(achievement.rarity)}`}
            >
              <div className="flex items-center space-x-3">
                <FontAwesomeIcon icon={achievement.icon as IconProp} className="w-8 h-8 text-gray-400" />
                <div>
                  <h4 className="font-semibold text-gray-600">{achievement.name}</h4>
                  <p className="text-sm text-gray-500">{achievement.description}</p>
                  <p className="text-xs text-gray-400 mt-1 capitalize">{achievement.rarity}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
