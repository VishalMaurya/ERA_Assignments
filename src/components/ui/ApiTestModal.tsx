'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@/lib/fontawesome';
import type { IconProp } from '@/lib/fontawesome';
import { GeminiService } from '@/lib/gemini';
import type { Assessment } from '@/types';

interface ApiTestModalProps {
  isOpen: boolean;
  onClose: () => void;
  onApiKeyValidated?: (apiKey: string) => void;
}

export default function ApiTestModal({ isOpen, onClose, onApiKeyValidated }: ApiTestModalProps) {
  const [apiKey, setApiKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [testResult, setTestResult] = useState<{
    success: boolean;
    message: string;
    details?: string;
  } | null>(null);

  const handleTest = async () => {
    if (!apiKey.trim()) {
      setTestResult({
        success: false,
        message: 'Please enter an API key',
        details: 'API key cannot be empty'
      });
      return;
    }

    setIsLoading(true);
    setTestResult(null);

    try {
      // Create a simple test assessment for API validation
      const testAssessment: Assessment = {
        id: 'test-' + Date.now(),
        userId: 'test-user',
        type: 'anxiety' as const,
        questions: [
          {
            id: 'test-1',
            type: 'mcq' as const,
            question: 'How often do you feel anxious?',
            options: ['Never', 'Sometimes', 'Often', 'Always'],
            environment: 'forest' as const
          }
        ],
        responses: [
          {
            questionId: 'test-1',
            answer: 'Sometimes',
            mood: 'neutral',
            timestamp: new Date()
          }
        ],
        currentQuestionIndex: 1,
        startedAt: new Date(),
        isCompleted: true,
        completedAt: new Date(),
        skippedQuestions: []
      };

      const geminiService = new GeminiService(apiKey);
      
      // Make a test call to Gemini
      await geminiService.generateAssessmentReport(testAssessment);
      
      setTestResult({
        success: true,
        message: 'API key is valid and working!',
        details: 'Successfully connected to Gemini AI. You can use this API key for generating reports.'
      });

      // If the test is successful and callback is provided, pass the validated API key
      if (onApiKeyValidated) {
        onApiKeyValidated(apiKey);
      }

    } catch (error) {
      console.error('API test failed:', error);
      
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      
      setTestResult({
        success: false,
        message: 'API key test failed',
        details: errorMessage
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setApiKey('');
    setTestResult(null);
    setIsLoading(false);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6"
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <FontAwesomeIcon icon={'stethoscope' as IconProp} className="w-5 h-5 text-blue-600" />
              </div>
              <h2 className="text-xl font-semibold text-calm-800">
                Test Gemini API
              </h2>
            </div>
            <button
              onClick={handleClose}
              className="w-8 h-8 rounded-lg hover:bg-gray-100 flex items-center justify-center transition-colors"
            >
              <FontAwesomeIcon icon={'xmark' as IconProp} className="w-4 h-4 text-gray-500" />
            </button>
          </div>

          {/* Content */}
          <div className="space-y-4">
            <div>
              <label htmlFor="test-api-key" className="block text-sm font-medium text-calm-700 mb-2">
                Gemini API Key
              </label>
              <div className="relative">
                <FontAwesomeIcon 
                  icon={'key' as IconProp} 
                  className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-calm-400" 
                />
                <input
                  id="test-api-key"
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Enter your Gemini API key (AIza...)"
                  className="w-full pl-10 pr-4 py-3 border border-calm-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
              <p className="text-xs text-calm-500 mt-1">
                Your API key will be tested but not saved
              </p>
            </div>

            {/* Test Result */}
            {testResult && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`p-4 rounded-lg border ${
                  testResult.success 
                    ? 'bg-green-50 border-green-200 text-green-800' 
                    : 'bg-red-50 border-red-200 text-red-800'
                }`}
              >
                <div className="flex items-start space-x-3">
                  <FontAwesomeIcon 
                    icon={testResult.success ? 'check-circle' as IconProp : 'exclamation-triangle' as IconProp} 
                    className={`w-5 h-5 mt-0.5 ${testResult.success ? 'text-green-600' : 'text-red-600'}`} 
                  />
                  <div>
                    <p className="font-medium">{testResult.message}</p>
                    {testResult.details && (
                      <p className="text-sm mt-1 opacity-90">{testResult.details}</p>
                    )}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Help Section */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-medium text-blue-800 mb-2">Need an API key?</h3>
              <ol className="text-sm text-blue-700 space-y-1">
                <li>1. Visit <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="underline hover:text-blue-900">Google AI Studio</a></li>
                <li>2. Sign in with your Google account</li>
                <li>3. Click "Create API Key"</li>
                <li>4. Copy the key (starts with "AIza")</li>
              </ol>
            </div>
          </div>

          {/* Footer */}
          <div className="flex space-x-3 mt-6">
            <button
              onClick={handleTest}
              disabled={isLoading || !apiKey.trim()}
              className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Testing...</span>
                </>
              ) : (
                <>
                  <FontAwesomeIcon icon={'stethoscope' as IconProp} className="w-4 h-4" />
                  <span>Test API Key</span>
                </>
              )}
            </button>
            <button
              onClick={handleClose}
              className="px-6 py-3 text-calm-600 hover:text-calm-800 hover:bg-calm-50 rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
