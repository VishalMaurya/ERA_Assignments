'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FontAwesomeIcon, IconProp } from '@/lib/fontawesome';
import { Question, QuestionResponse } from '@/types';
import { generateId, getMoodEmoji } from '@/utils/helpers';

interface QuestionCardProps {
  question: Question;
  questionNumber: number;
  totalQuestions: number;
  onResponse: (response: QuestionResponse) => void;
  onSkip: () => void;
  onBack?: () => void;
  existingResponse?: QuestionResponse;
}

export default function QuestionCard({
  question,
  questionNumber,
  totalQuestions,
  onResponse,
  onSkip,
  onBack,
  existingResponse
}: QuestionCardProps) {
  const [answer, setAnswer] = useState<string | number | string[]>('');
  const [selectedMood, setSelectedMood] = useState('');
  const [showHint, setShowHint] = useState(false);
  const [startTime] = useState(Date.now());

  // Load existing response if available
  useEffect(() => {
    if (existingResponse) {
      setAnswer(existingResponse.answer);
      setSelectedMood(existingResponse.mood || '');
    } else {
      setAnswer(question.type === 'mcq' && question.options ? [] : '');
      setSelectedMood('');
    }
  }, [question.id, existingResponse]);

  const handleSubmit = () => {
    const response: QuestionResponse = {
      questionId: question.id,
      answer,
      mood: selectedMood || undefined,
      timestamp: new Date(),
      timeSpent: Math.floor((Date.now() - startTime) / 1000)
    };

    onResponse(response);
  };

  const isAnswerValid = () => {
    if (!question.required) return true;
    
    switch (question.type) {
      case 'mcq':
        return Array.isArray(answer) ? answer.length > 0 : answer !== '';
      case 'scale':
        return typeof answer === 'number' && answer >= (question.scaleMin || 1) && answer <= (question.scaleMax || 10);
      case 'open-ended':
        return typeof answer === 'string' && answer.trim().length > 0;
      case 'mood':
        return selectedMood !== '';
      default:
        return false;
    }
  };

  const renderQuestionInput = () => {
    switch (question.type) {
      case 'mcq':
        return (
          <div className="space-y-3">
            {question.options?.map((option, index) => (
              <motion.label
                key={index}
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                className={`flex items-center p-4 rounded-lg border-2 transition-all cursor-pointer hover:bg-white/50 ${
                  Array.isArray(answer) 
                    ? answer.includes(option)
                      ? 'border-primary-400 bg-primary-50/50'
                      : 'border-white/30 bg-white/20'
                    : answer === option
                      ? 'border-primary-400 bg-primary-50/50'
                      : 'border-white/30 bg-white/20'
                }`}
              >
                <input
                  type={question.options && question.options.length > 5 ? 'checkbox' : 'radio'}
                  name={`question-${question.id}`}
                  value={option}
                  checked={Array.isArray(answer) ? answer.includes(option) : answer === option}
                  onChange={(e) => {
                    if (question.options && question.options.length > 5) {
                      // Multiple selection for long option lists
                      const currentAnswers = Array.isArray(answer) ? answer : [];
                      if (e.target.checked) {
                        setAnswer([...currentAnswers, option]);
                      } else {
                        setAnswer(currentAnswers.filter(a => a !== option));
                      }
                    } else {
                      // Single selection
                      setAnswer(option);
                    }
                  }}
                  className="mr-3 w-4 h-4 text-primary-600 border-2 border-white/50 rounded focus:ring-primary-400"
                />
                <span className="text-calm-800 font-medium">{option}</span>
              </motion.label>
            ))}
          </div>
        );

      case 'scale':
        const min = question.scaleMin || 1;
        const max = question.scaleMax || 10;
        return (
          <div className="space-y-6">
            <div className="flex justify-between text-sm text-calm-600 px-2">
              <span>{question.scaleLabels?.[0] || `${min}`}</span>
              <span>{question.scaleLabels?.[1] || `${max}`}</span>
            </div>
            
            <div className="flex justify-between items-center px-2">
              {Array.from({ length: max - min + 1 }, (_, i) => {
                const value = min + i;
                const isSelected = answer === value;
                
                return (
                  <motion.button
                    key={value}
                    type="button"
                    onClick={() => setAnswer(value)}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className={`w-10 h-10 rounded-full border-2 font-semibold transition-all ${
                      isSelected
                        ? 'bg-primary-500 border-primary-500 text-white shadow-lg'
                        : 'bg-white/20 border-white/30 text-calm-700 hover:bg-white/40'
                    }`}
                  >
                    {value}
                  </motion.button>
                );
              })}
            </div>

            {typeof answer === 'number' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center p-3 bg-white/20 rounded-lg"
              >
                <span className="text-calm-700 font-medium">
                  Selected: {answer} / {max}
                </span>
              </motion.div>
            )}
          </div>
        );

      case 'open-ended':
        return (
          <div className="space-y-4">
            <textarea
              value={answer as string}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Share your thoughts here..."
              className="w-full p-4 rounded-lg border-2 border-white/30 bg-white/20 backdrop-blur-sm text-calm-800 placeholder-calm-500 focus:border-primary-400 focus:outline-none resize-none transition-all"
              rows={6}
              maxLength={1000}
            />
            <div className="flex justify-between text-sm text-calm-600">
              <span>Take your time - there&apos;s no rush</span>
              <span>{(answer as string).length}/1000</span>
            </div>
          </div>
        );

      case 'mood':
        const moodOptions = [
          { key: 'very-sad', label: 'Very Sad', emoji: '😢' },
          { key: 'sad', label: 'Sad', emoji: '😞' },
          { key: 'anxious', label: 'Anxious', emoji: '😰' },
          { key: 'neutral', label: 'Neutral', emoji: '😐' },
          { key: 'calm', label: 'Calm', emoji: '😌' },
          { key: 'happy', label: 'Happy', emoji: '😊' },
          { key: 'hopeful', label: 'Hopeful', emoji: '🌟' },
          { key: 'grateful', label: 'Grateful', emoji: '🙏' }
        ];

        return (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {moodOptions.map((mood, index) => (
              <motion.button
                key={mood.key}
                type="button"
                onClick={() => {
                  setSelectedMood(mood.key);
                  setAnswer(mood.label);
                }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`p-4 rounded-lg border-2 transition-all text-center ${
                  selectedMood === mood.key
                    ? 'border-primary-400 bg-primary-50/50 shadow-lg'
                    : 'border-white/30 bg-white/20 hover:bg-white/40'
                }`}
              >
                <div className="text-2xl mb-2">{mood.emoji}</div>
                <div className="text-sm font-medium text-calm-800">{mood.label}</div>
              </motion.button>
            ))}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="card p-8 max-w-4xl mx-auto">
      {/* Question Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <span className="text-sm font-medium text-primary-600 bg-primary-100 px-3 py-1 rounded-full">
            Question {questionNumber} of {totalQuestions}
          </span>
          {question.hint && (
            <button
              onClick={() => setShowHint(!showHint)}
              className="p-2 rounded-lg bg-blue-100 hover:bg-blue-200 transition-colors"
              title="Show hint"
            >
              <FontAwesomeIcon icon={'question' as IconProp} className="w-4 h-4 text-blue-600" />
            </button>
          )}
        </div>

        <h2 className="text-2xl md:text-3xl font-bold text-calm-800 mb-4 leading-tight">
          {question.question}
        </h2>

        {question.description && (
          <p className="text-calm-600 text-lg mb-4">
            {question.description}
          </p>
        )}

        {/* Hint */}
        {showHint && question.hint && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4"
          >
            <div className="flex items-start space-x-3">
              <FontAwesomeIcon icon={'lightbulb' as IconProp} className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div>
                <h4 className="font-medium text-blue-800 mb-1">Hint</h4>
                <p className="text-blue-700 text-sm">{question.hint}</p>
                {question.example && (
                  <div className="mt-2 p-2 bg-blue-100 rounded text-blue-700 text-sm">
                    <strong>Example:</strong> {question.example}
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Question Input */}
      <div className="mb-8">
        {renderQuestionInput()}
      </div>

      {/* Mood Selector for non-mood questions */}
      {question.type !== 'mood' && (
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <FontAwesomeIcon icon={'heart' as IconProp} className="w-5 h-5 text-pink-500" />
            <span className="text-sm font-medium text-calm-700">
              How are you feeling right now? (Optional)
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {['calm', 'happy', 'neutral', 'anxious', 'sad', 'frustrated', 'hopeful'].map((mood) => (
              <button
                key={mood}
                type="button"
                onClick={() => setSelectedMood(selectedMood === mood ? '' : mood)}
                className={`px-3 py-1 rounded-full text-sm transition-all ${
                  selectedMood === mood
                    ? 'bg-pink-500 text-white'
                    : 'bg-white/30 text-calm-600 hover:bg-white/50'
                }`}
              >
                {getMoodEmoji(mood)} {mood.charAt(0).toUpperCase() + mood.slice(1)}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0 sm:space-x-4">
        <div className="flex space-x-3">
          {onBack && (
            <button
              onClick={onBack}
              className="btn-ghost flex items-center space-x-2"
            >
              <FontAwesomeIcon icon={'chevron-left' as IconProp} className="w-4 h-4" />
              <span>Back</span>
            </button>
          )}
          
          <button
            onClick={onSkip}
            className="btn-ghost flex items-center space-x-2 text-calm-600"
          >
            <FontAwesomeIcon icon={'forward' as IconProp} className="w-4 h-4" />
            <span>Skip</span>
          </button>
        </div>

        <button
          onClick={handleSubmit}
          disabled={!isAnswerValid()}
          className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span>Continue</span>
          <FontAwesomeIcon icon={'chevron-right' as IconProp} className="w-4 h-4" />
        </button>
      </div>

      {/* Progress indicator */}
      <div className="mt-6 text-center text-sm text-calm-500">
        {question.required ? (
          <span>This question is required</span>
        ) : (
          <span>This question is optional - answer what feels right for you</span>
        )}
      </div>
    </div>
  );
}
