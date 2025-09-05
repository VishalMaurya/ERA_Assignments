'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

export default function TherapyPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('anxiety');

  const therapyCategories = [
    { id: 'anxiety', name: 'Anxiety Management', color: 'blue', exercises: 5 },
    { id: 'mindfulness', name: 'Mindfulness', color: 'green', exercises: 8 },
    { id: 'self-compassion', name: 'Self-Compassion', color: 'purple', exercises: 4 },
    { id: 'sleep', name: 'Sleep Health', color: 'indigo', exercises: 3 },
  ];

  const sampleExercises = {
    anxiety: [
      { name: 'Deep Breathing', duration: '5 min', difficulty: 'Beginner' },
      { name: 'Thought Record', duration: '10 min', difficulty: 'Intermediate' },
      { name: 'Progressive Muscle Relaxation', duration: '15 min', difficulty: 'Beginner' },
    ],
    mindfulness: [
      { name: 'Body Scan Meditation', duration: '12 min', difficulty: 'Beginner' },
      { name: 'Mindful Walking', duration: '8 min', difficulty: 'Beginner' },
      { name: 'Present Moment Awareness', duration: '6 min', difficulty: 'Beginner' },
    ],
    'self-compassion': [
      { name: 'Self-Kindness Exercise', duration: '7 min', difficulty: 'Beginner' },
      { name: 'Loving-Kindness Meditation', duration: '15 min', difficulty: 'Intermediate' },
    ],
    sleep: [
      { name: 'Sleep Hygiene Check', duration: '5 min', difficulty: 'Beginner' },
      { name: 'Bedtime Relaxation', duration: '10 min', difficulty: 'Beginner' },
    ],
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-nature-50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-calm-800 mb-4">
            🧠 Therapy Center
          </h1>
          <p className="text-lg text-calm-600 mb-4">
            Practice evidence-based therapeutic exercises designed to support your mental wellbeing
          </p>
          <div className="text-sm text-calm-500">
            Choose a category to explore guided exercises and techniques
          </div>
        </motion.div>

        {/* Category Selection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
        >
          {therapyCategories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`p-4 rounded-lg border-2 transition-all duration-300 ${
                selectedCategory === category.id
                  ? `border-${category.color}-500 bg-${category.color}-50`
                  : 'border-gray-200 bg-white hover:border-gray-300'
              }`}
            >
              <div className="text-center">
                <h3 className="font-semibold text-calm-800 mb-1">{category.name}</h3>
                <p className="text-xs text-calm-500">{category.exercises} exercises</p>
              </div>
            </button>
          ))}
        </motion.div>

        {/* Exercise List */}
        <motion.div
          key={selectedCategory}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          className="bg-white rounded-lg shadow-lg p-6"
        >
          <h2 className="text-2xl font-bold text-calm-800 mb-6">
            {therapyCategories.find(c => c.id === selectedCategory)?.name} Exercises
          </h2>
          
          <div className="grid gap-4">
            {(sampleExercises as any)[selectedCategory]?.map((exercise: any, index: number) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-calm-800 mb-2">{exercise.name}</h3>
                    <div className="flex gap-4 text-sm text-calm-500">
                      <span>⏱️ {exercise.duration}</span>
                      <span>📊 {exercise.difficulty}</span>
                    </div>
                  </div>
                  <button className="bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors">
                    Start
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Coming Soon Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-8 text-center"
        >
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-amber-800 mb-2">🚀 Coming Soon</h3>
            <p className="text-amber-700 text-sm">
              Interactive guided exercises, progress tracking, personalized recommendations, and more advanced therapy modules
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}