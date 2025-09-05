'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Leaf, 
  Heart, 
  Moon, 
  Award, 
  RotateCcw, 
  Zap, 
  Shield, 
  TrendingUp,
  Stethoscope,
  Play,
  ShieldCheck,
  Sparkles,
  ChevronRight,
  Users,
  Lightbulb,
  Target,
  Wind,
  Dumbbell,
  Apple,
  BookOpen,
  Map,
  Compass,
  Smile,
  Flame
} from 'lucide-react';
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
    icon: React.ComponentType<any>;
    color: string;
    gradient: string;
    category: string;
  }> = [
    // CBT Family
    { type: 'anxiety', icon: Brain, color: 'text-blue-600', gradient: 'from-blue-500 to-indigo-600', category: 'CBT' },
    { type: 'ocd', icon: RotateCcw, color: 'text-purple-600', gradient: 'from-purple-500 to-violet-600', category: 'CBT' },
    { type: 'behavioral-activation', icon: Target, color: 'text-emerald-600', gradient: 'from-emerald-500 to-teal-600', category: 'CBT' },
    { type: 'habit-reversal', icon: RotateCcw, color: 'text-cyan-600', gradient: 'from-cyan-500 to-blue-600', category: 'CBT' },
    { type: 'problem-solving', icon: Lightbulb, color: 'text-yellow-600', gradient: 'from-yellow-500 to-amber-600', category: 'CBT' },
    
    // Mindfulness & Acceptance
    { type: 'mindfulness', icon: Leaf, color: 'text-teal-600', gradient: 'from-teal-500 to-green-600', category: 'Mindfulness' },
    { type: 'acceptance-commitment', icon: Compass, color: 'text-indigo-600', gradient: 'from-indigo-500 to-purple-600', category: 'Mindfulness' },
    { type: 'mindful-cognitive', icon: Brain, color: 'text-green-600', gradient: 'from-green-500 to-emerald-600', category: 'Mindfulness' },
    
    // Emotion Regulation & Interpersonal
    { type: 'anger', icon: Flame, color: 'text-red-600', gradient: 'from-red-500 to-rose-600', category: 'Emotional' },
    { type: 'emotion-regulation', icon: Heart, color: 'text-pink-600', gradient: 'from-pink-500 to-rose-600', category: 'Emotional' },
    { type: 'interpersonal', icon: Users, color: 'text-blue-600', gradient: 'from-blue-500 to-indigo-600', category: 'Emotional' },
    
    // Compassion & Self-Kindness
    { type: 'self-compassion', icon: Heart, color: 'text-amber-600', gradient: 'from-amber-500 to-orange-600', category: 'Compassion' },
    { type: 'positive-psychology', icon: Smile, color: 'text-yellow-600', gradient: 'from-yellow-500 to-orange-600', category: 'Compassion' },
    { type: 'strengths', icon: Award, color: 'text-orange-600', gradient: 'from-orange-500 to-red-600', category: 'Compassion' },
    
    // Lifestyle & Holistic
    { type: 'sleep', icon: Moon, color: 'text-slate-600', gradient: 'from-slate-500 to-gray-600', category: 'Lifestyle' },
    { type: 'relaxation', icon: Leaf, color: 'text-green-600', gradient: 'from-green-500 to-teal-600', category: 'Lifestyle' },
    { type: 'breathing', icon: Wind, color: 'text-sky-600', gradient: 'from-sky-500 to-blue-600', category: 'Lifestyle' },
    { type: 'exercise', icon: Dumbbell, color: 'text-red-600', gradient: 'from-red-500 to-orange-600', category: 'Lifestyle' },
    { type: 'nutrition', icon: Apple, color: 'text-green-600', gradient: 'from-green-500 to-lime-600', category: 'Lifestyle' },
    
    // Specialized Therapies
    { type: 'trauma', icon: Shield, color: 'text-indigo-600', gradient: 'from-indigo-500 to-blue-600', category: 'Specialized' },
    { type: 'schema', icon: Map, color: 'text-violet-600', gradient: 'from-violet-500 to-purple-600', category: 'Specialized' },
    { type: 'narrative', icon: BookOpen, color: 'text-emerald-600', gradient: 'from-emerald-500 to-green-600', category: 'Specialized' },
    { type: 'motivation', icon: Target, color: 'text-red-600', gradient: 'from-red-500 to-pink-600', category: 'Specialized' },
    { type: 'solution-focused', icon: Lightbulb, color: 'text-blue-600', gradient: 'from-blue-500 to-cyan-600', category: 'Specialized' },
    
    // General
    { type: 'general', icon: Heart, color: 'text-green-600', gradient: 'from-green-500 to-emerald-600', category: 'General' },
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

      <div className={`relative z-10 container mx-auto px-4 py-12 ${selectedAssessment ? 'pb-32' : 'pb-12'}`}>
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
              <TrendingUp className="w-4 h-4" />
              <span>Analytics Dashboard</span>
              <span className="text-xs bg-emerald-500 px-2 py-1 rounded-full group-hover:bg-emerald-400 transition-colors">
                25+ Assessments
              </span>
            </button>
                                    <button
                          onClick={() => setShowApiTestModal(true)}
                          className="inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-3 rounded-lg transition-colors shadow-lg hover:shadow-xl"
                        >
                          <Stethoscope className="w-4 h-4" />
                          <span>Test Gemini API</span>
                        </button>
                        
                        <button
                          onClick={() => router.push('/therapy')}
                          className="inline-flex items-center space-x-2 bg-purple-600 hover:bg-purple-700 text-white font-medium px-6 py-3 rounded-lg transition-colors shadow-lg hover:shadow-xl"
                        >
                          <Play className="w-4 h-4" />
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
              <Brain className="w-6 h-6 text-primary-600" />
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
              <ShieldCheck className="w-6 h-6 text-nature-600" />
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
              <Sparkles className="w-6 h-6 text-purple-600" />
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
          className="max-w-7xl mx-auto"
        >
          <h2 className="text-3xl font-bold text-center text-calm-800 mb-4">
            Choose Your Journey
          </h2>
          <p className="text-center text-calm-600 mb-8">
            Discover all 25 therapeutic assessments across different categories
          </p>
          
          {/* Category-based Scrollable Assessment Cards */}
          <div className="space-y-8 mb-12">
            {['CBT', 'Mindfulness', 'Emotional', 'Compassion', 'Lifestyle', 'Specialized', 'General'].map((category, categoryIndex) => {
              const categoryAssessments = assessmentTypes.filter(a => a.category === category);
              if (categoryAssessments.length === 0) return null;
              
              return (
                <motion.div
                  key={category}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: 0.5 + categoryIndex * 0.1 }}
                  className="space-y-4"
                >
                  <h3 className="text-xl font-semibold text-calm-800 mb-4 flex items-center">
                    <div className="w-1 h-6 bg-gradient-to-b from-primary-500 to-primary-600 rounded-full mr-3"></div>
                    {category === 'CBT' ? 'Cognitive Behavioral Therapy' : 
                     category === 'Mindfulness' ? 'Mindfulness & Acceptance' :
                     category === 'Emotional' ? 'Emotion Regulation' :
                     category === 'Compassion' ? 'Self-Compassion & Strengths' :
                     category === 'Lifestyle' ? 'Lifestyle & Wellness' :
                     category === 'Specialized' ? 'Specialized Therapies' :
                     'General Wellbeing'}
                    <span className="ml-2 text-sm bg-calm-100 text-calm-600 px-2 py-1 rounded-full">
                      {categoryAssessments.length} assessments
                    </span>
                  </h3>
                  
                  <div className="overflow-x-auto pb-4">
                    <div className="flex space-x-4 w-max">
                      {categoryAssessments.map((assessment, index) => (
                        <motion.div
                          key={assessment.type}
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ duration: 0.4, delay: 0.1 * index }}
                          className={`flex-shrink-0 w-80 card card-hover p-6 transition-all duration-300 cursor-pointer ${
                            selectedAssessment === assessment.type
                              ? 'ring-2 ring-primary-400 bg-primary-50/50 scale-105'
                              : 'hover:bg-white/70 hover:scale-102'
                          }`}
                          onClick={() => setSelectedAssessment(assessment.type)}
                          whileHover={{ y: -4 }}
                          whileTap={{ scale: 0.98 }}
                        >
                          {/* Header */}
                          <div className="flex items-start justify-between mb-4">
                            <div className={`p-3 rounded-xl bg-gradient-to-r ${assessment.gradient} text-white shadow-lg`}>
                              <assessment.icon className="w-6 h-6" />
                            </div>
                            <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all ${
                              selectedAssessment === assessment.type
                                ? 'border-primary-400 bg-primary-400'
                                : 'border-calm-300'
                            }`}>
                              {selectedAssessment === assessment.type && (
                                <motion.div
                                  initial={{ scale: 0 }}
                                  animate={{ scale: 1 }}
                                  className="w-2 h-2 bg-white rounded-full"
                                />
                              )}
                            </div>
                          </div>

                          {/* Content */}
                          <div className="space-y-3">
                            <h4 className="text-lg font-semibold text-calm-800 leading-tight">
                              {getAssessmentTitle(assessment.type)}
                            </h4>
                            <p className="text-sm text-calm-600 leading-relaxed line-clamp-3">
                              {getAssessmentDescription(assessment.type)}
                            </p>
                          </div>

                          {/* Footer */}
                          <div className="mt-4 pt-4 border-t border-calm-100 flex items-center justify-between">
                            <div className="text-xs text-calm-500">
                              <span>8-12 min</span>
                              <span className="mx-1">•</span>
                              <span>Evidence-based</span>
                            </div>
                            {selectedAssessment === assessment.type && (
                              <motion.div
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="text-xs font-medium text-primary-600 bg-primary-100 px-2 py-1 rounded-full"
                              >
                                Selected
                              </motion.div>
                            )}
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* Call to Action for non-selected state */}
          {!selectedAssessment && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
              className="text-center mt-16 mb-32"
            >
              <motion.div
                initial={{ opacity: 0.7 }}
                animate={{ opacity: 1 }}
                className="bg-white/40 backdrop-blur-sm border border-calm-200 rounded-2xl p-8 shadow-lg max-w-md mx-auto"
              >
                <div className="flex items-center justify-center space-x-3 mb-4">
                  <div className="w-12 h-12 bg-calm-300 rounded-full flex items-center justify-center">
                    <Target className="w-6 h-6 text-calm-600" />
                  </div>
                  <div className="text-left">
                    <h3 className="font-semibold text-calm-700">Choose an Assessment</h3>
                    <p className="text-sm text-calm-500">
                      Select from the categories above
                    </p>
                  </div>
                </div>
                
                <div className="w-full bg-calm-200 text-calm-500 font-semibold py-4 px-8 rounded-xl cursor-not-allowed">
                  <div className="flex items-center justify-center space-x-3">
                    <Target className="w-5 h-5" />
                    <span className="text-lg">Select Assessment First</span>
                  </div>
                </div>
                
                <p className="mt-4 text-xs text-calm-500 text-center">
                  Browse through our evidence-based assessments to get started
                </p>
              </motion.div>
            </motion.div>
          )}

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

        {/* Floating Begin Journey Panel */}
        {selectedAssessment && (
          <motion.div
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 100 }}
            transition={{ type: 'spring', stiffness: 400, damping: 25 }}
            className="fixed bottom-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-t border-calm-200 shadow-2xl"
          >
            <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
              <div className="flex flex-col sm:flex-row items-center justify-between space-y-3 sm:space-y-0">
                {/* Assessment Info */}
                <div className="flex items-center space-x-3 sm:space-x-4">
                  <div className="flex items-center space-x-3">
                    {(() => {
                      const assessment = assessmentTypes.find(a => a.type === selectedAssessment);
                      if (!assessment) return null;
                      return (
                        <div className={`p-2 sm:p-3 rounded-xl bg-gradient-to-r ${assessment.gradient} text-white shadow-lg`}>
                          <assessment.icon className="w-4 h-4 sm:w-5 sm:h-5" />
                        </div>
                      );
                    })()}
                    <div>
                      <h3 className="font-semibold text-calm-800 text-sm sm:text-base">
                        {getAssessmentTitle(selectedAssessment)} Assessment
                      </h3>
                      <p className="text-xs text-calm-600">8-12 minutes • Evidence-based</p>
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center space-x-3 w-full sm:w-auto">
                  <button
                    onClick={() => setSelectedAssessment(null)}
                    className="px-3 py-2 text-calm-600 hover:text-calm-800 transition-colors text-sm font-medium"
                  >
                    Change
                  </button>
                  <motion.button
                    onClick={startJourney}
                    className="flex-1 sm:flex-none bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold py-3 px-4 sm:px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <div className="flex items-center justify-center space-x-2">
                      <Play className="w-4 h-4" />
                      <span className="text-sm sm:text-base">Begin Journey</span>
                      <ChevronRight className="w-4 h-4" />
                    </div>
                  </motion.button>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* API Test Modal */}
        <ApiTestModal
          isOpen={showApiTestModal}
          onClose={() => setShowApiTestModal(false)}
          onApiKeyValidated={handleApiKeyValidated}
        />
      </div>
    </div>
  );
}
