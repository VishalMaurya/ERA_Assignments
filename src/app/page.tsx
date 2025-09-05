'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { FontAwesomeIcon, IconProp } from '@/lib/fontawesome';
import { AssessmentType } from '@/types';
import { getAssessmentTitle, getAssessmentDescription } from '@/utils/helpers';
import { useRouter } from 'next/navigation';
import ApiTestModal from '@/components/ui/ApiTestModal';
import { StorageService } from '@/utils/storage';

export default function HomePage() {
  const [selectedAssessment, setSelectedAssessment] = useState<AssessmentType | null>(null);
  const [showApiTestModal, setShowApiTestModal] = useState(false);
  const router = useRouter();

  const assessmentTypes: Array<{
    type: AssessmentType;
    icon: IconProp;
    color: string;
    gradient: string;
  }> = [
    {
      type: 'anxiety',
      icon: 'brain' as IconProp,
      color: 'text-blue-600',
      gradient: 'from-blue-500 to-indigo-600'
    },
    {
      type: 'mindfulness',
      icon: 'leaf' as IconProp,
      color: 'text-teal-600',
      gradient: 'from-teal-500 to-green-600'
    },
    {
      type: 'self-compassion',
      icon: 'heart' as IconProp,
      color: 'text-amber-600',
      gradient: 'from-amber-500 to-orange-600'
    },
    {
      type: 'sleep',
      icon: 'moon' as IconProp,
      color: 'text-slate-600',
      gradient: 'from-slate-500 to-gray-600'
    },
    {
      type: 'strengths',
      icon: 'award' as IconProp,
      color: 'text-orange-600',
      gradient: 'from-orange-500 to-red-600'
    },
    {
      type: 'general',
      icon: 'heart' as IconProp,
      color: 'text-green-600',
      gradient: 'from-green-500 to-emerald-600'
    },
    {
      type: 'ocd',
      icon: 'arrows-spin' as IconProp,
      color: 'text-purple-600',
      gradient: 'from-purple-500 to-violet-600'
    },
    {
      type: 'anger',
      icon: 'fire' as IconProp,
      color: 'text-red-600',
      gradient: 'from-red-500 to-rose-600'
    },
    {
      type: 'trauma',
      icon: 'shield-heart' as IconProp,
      color: 'text-indigo-600',
      gradient: 'from-indigo-500 to-blue-600'
    },
    {
      type: 'emotion-regulation',
      icon: 'scale-balanced' as IconProp,
      color: 'text-emerald-600',
      gradient: 'from-emerald-500 to-teal-600'
    },
    {
      type: 'acceptance-commitment',
      icon: 'check-circle' as IconProp,
      color: 'text-cyan-600',
      gradient: 'from-cyan-500 to-blue-600'
    },
    {
      type: 'breathing',
      icon: 'lungs' as IconProp,
      color: 'text-sky-600',
      gradient: 'from-sky-500 to-blue-600'
    }
  ];

  const startJourney = () => {
    if (selectedAssessment) {
      router.push(`/assessment/${selectedAssessment}`);
    }
  };

  const handleApiKeyValidated = (apiKey: string) => {
    StorageService.saveGeminiApiKey(apiKey);
    setShowApiTestModal(false);
    // Optionally show success message or redirect
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-300/20 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-nature-300/20 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-purple-300/10 rounded-full blur-3xl animate-float"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold text-gradient mb-6">
            Your Psychological Journey
          </h1>
          <p className="text-xl md:text-2xl text-calm-600 max-w-3xl mx-auto leading-relaxed">
            Embark on an immersive self-discovery experience. Understand your patterns, 
            explore your mind, and receive personalized insights powered by AI.
          </p>
          
          {/* Action Buttons */}
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button
              onClick={() => router.push('/dashboard')}
              className="inline-flex items-center space-x-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium px-6 py-3 rounded-lg transition-colors shadow-lg hover:shadow-xl group"
            >
              <FontAwesomeIcon icon={'chart-line' as IconProp} className="w-4 h-4" />
              <span>Analytics Dashboard</span>
              <span className="text-xs bg-emerald-500 px-2 py-1 rounded-full group-hover:bg-emerald-400 transition-colors">
                25+ Assessments
              </span>
            </button>
                                    <button
                          onClick={() => setShowApiTestModal(true)}
                          className="inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-3 rounded-lg transition-colors shadow-lg hover:shadow-xl"
                        >
                          <FontAwesomeIcon icon={'stethoscope' as IconProp} className="w-4 h-4" />
                          <span>Test Gemini API</span>
                        </button>
                        
                        <button
                          onClick={() => router.push('/therapy')}
                          className="inline-flex items-center space-x-2 bg-purple-600 hover:bg-purple-700 text-white font-medium px-6 py-3 rounded-lg transition-colors shadow-lg hover:shadow-xl"
                        >
                          <FontAwesomeIcon icon={'play' as IconProp} className="w-4 h-4" />
                          <span>Therapy Center</span>
                        </button>
          </div>
          <p className="text-sm text-calm-500 mt-3 text-center">
            Access your analytics dashboard, practice therapy exercises, or validate your API key before starting
          </p>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="grid md:grid-cols-3 gap-8 mb-16"
        >
          <div className="card p-6 text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <FontAwesomeIcon icon={'brain' as IconProp} className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold text-calm-800 mb-2">
              AI-Powered Insights
            </h3>
            <p className="text-calm-600">
              Receive personalized reports generated by advanced AI, tailored to your unique responses.
            </p>
          </div>

          <div className="card p-6 text-center">
            <div className="w-12 h-12 bg-nature-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <FontAwesomeIcon icon={'shield-alt' as IconProp} className="w-6 h-6 text-nature-600" />
            </div>
            <h3 className="text-lg font-semibold text-calm-800 mb-2">
              Safe & Private
            </h3>
            <p className="text-calm-600">
              Your responses are processed securely. You control your data and can exit anytime.
            </p>
          </div>

          <div className="card p-6 text-center">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <FontAwesomeIcon icon={'wand-sparkles' as IconProp} className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold text-calm-800 mb-2">
              Immersive Experience
            </h3>
            <p className="text-calm-600">
              Journey through beautiful environments as you explore different aspects of your mind.
            </p>
          </div>
        </motion.div>

        {/* Assessment Selection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="max-w-4xl mx-auto"
        >
          <h2 className="text-3xl font-bold text-center text-calm-800 mb-4">
            Choose Your Journey
          </h2>
          <p className="text-center text-calm-600 mb-8">
            Select from our featured assessments below, or explore 25+ therapeutic assessments from the dashboard
          </p>
          
          <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6 mb-12">
            {assessmentTypes.map((assessment, index) => (
              <motion.div
                key={assessment.type}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.5 + index * 0.1 }}
                className={`card card-hover p-6 transition-all duration-300 cursor-pointer ${
                  selectedAssessment === assessment.type
                    ? 'ring-2 ring-primary-400 bg-primary-50/50'
                    : 'hover:bg-white/70'
                }`}
                onClick={() => setSelectedAssessment(assessment.type)}
              >
                <div className="flex flex-col items-center text-center space-y-3">
                  <div className={`p-3 rounded-lg bg-gradient-to-r ${assessment.gradient} text-white`}>
                    <FontAwesomeIcon icon={assessment.icon} className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-calm-800 mb-2">
                      {getAssessmentTitle(assessment.type)}
                    </h3>
                    <p className="text-sm text-calm-600 mb-3 line-clamp-3">
                      {getAssessmentDescription(assessment.type)}
                    </p>
                    <div className="text-xs text-calm-500">
                      <span>8-10 minutes</span>
                      <span className="mx-1">•</span>
                      <span>Skip anytime</span>
                    </div>
                  </div>
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                    selectedAssessment === assessment.type
                      ? 'border-primary-400 bg-primary-400'
                      : 'border-calm-300'
                  }`}>
                    {selectedAssessment === assessment.type && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-3 h-3 bg-white rounded-full"
                      />
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Start Button */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: selectedAssessment ? 1 : 0.5 }}
            transition={{ duration: 0.3 }}
            className="text-center"
          >
            <button
              onClick={startJourney}
              disabled={!selectedAssessment}
              className={`btn-primary text-lg px-8 py-4 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none ${
                selectedAssessment ? 'animate-glow' : ''
              }`}
            >
              <FontAwesomeIcon icon={'play' as IconProp} className="w-5 h-5 mr-2" />
              Begin Your Journey
              <FontAwesomeIcon icon={'chevron-right' as IconProp} className="w-5 h-5 ml-2" />
            </button>
          </motion.div>

          {/* Disclaimer */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="mt-12 p-6 bg-amber-50 border border-amber-200 rounded-lg"
          >
            <p className="text-sm text-amber-800 text-center">
              <strong>Important:</strong> This assessment is for self-reflection and educational purposes only. 
              It is not a substitute for professional medical advice, diagnosis, or treatment. 
              If you are experiencing severe mental health symptoms, please consult with a qualified healthcare provider.
            </p>
          </motion.div>
        </motion.div>
      </div>

      {/* API Test Modal */}
      <ApiTestModal
        isOpen={showApiTestModal}
        onClose={() => setShowApiTestModal(false)}
        onApiKeyValidated={handleApiKeyValidated}
      />
    </div>
  );
}
