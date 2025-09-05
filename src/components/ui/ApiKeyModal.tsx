'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon, IconProp } from '@/lib/fontawesome';
import { isValidApiKey } from '@/utils/helpers';

interface ApiKeyModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (apiKey: string) => void;
}

export default function ApiKeyModal({ isOpen, onClose, onSubmit }: ApiKeyModalProps) {
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!apiKey.trim()) {
      setError('Please enter your Gemini API key');
      return;
    }

    if (!isValidApiKey(apiKey.trim())) {
      setError('Please enter a valid Gemini API key (should start with "AI" and be longer than 30 characters)');
      return;
    }

    setIsSubmitting(true);

    try {
      // Simulate API key validation
      await new Promise(resolve => setTimeout(resolve, 1000));
      onSubmit(apiKey.trim());
      setApiKey('');
    } catch (err) {
      setError('Invalid API key. Please check and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    if (!isSubmitting) {
      setApiKey('');
      setError('');
      onClose();
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={handleClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ type: 'spring', duration: 0.5 }}
            className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                  <FontAwesomeIcon icon={'key' as IconProp} className="w-5 h-5 text-primary-600" />
                </div>
                <h2 className="text-xl font-semibold text-calm-800">
                  Gemini API Key Required
                </h2>
              </div>
              <button
                onClick={handleClose}
                disabled={isSubmitting}
                className="p-2 hover:bg-calm-100 rounded-lg transition-colors disabled:opacity-50"
              >
                <FontAwesomeIcon icon={'xmark' as IconProp} className="w-5 h-5 text-calm-500" />
              </button>
            </div>

            {/* Content */}
            <div className="mb-6">
              <p className="text-calm-600 mb-4">
                To generate your personalized assessment report, we need your Gemini API key. 
                This ensures your data stays private and secure.
              </p>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                <div className="flex items-start space-x-3">
                  <FontAwesomeIcon icon={'shield-alt' as IconProp} className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-blue-800 mb-1">Your Privacy is Protected</h4>
                    <p className="text-sm text-blue-700">
                      Your API key is stored locally in your browser and is never sent to our servers. 
                      It&apos;s only used to communicate directly with Google&apos;s Gemini AI service.
                    </p>
                  </div>
                </div>
              </div>

              <div className="text-sm text-calm-600 space-y-2">
                <p><strong>To get your API key:</strong></p>
                <ol className="list-decimal list-inside space-y-1 ml-4">
                  <li>Visit <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Google AI Studio</a></li>
                  <li>Sign in with your Google account</li>
                  <li>Click &quot;Create API Key&quot;</li>
                  <li>Copy the generated key and paste it below</li>
                </ol>
              </div>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="apiKey" className="block text-sm font-medium text-calm-700 mb-2">
                  Gemini API Key
                </label>
                <input
                  type="password"
                  id="apiKey"
                  value={apiKey}
                  onChange={(e) => {
                    setApiKey(e.target.value);
                    setError('');
                  }}
                  placeholder="Enter your Gemini API key..."
                  className="w-full px-4 py-3 border border-calm-300 rounded-lg focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-colors"
                  disabled={isSubmitting}
                />
                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-2 flex items-center space-x-2 text-red-600"
                  >
                    <FontAwesomeIcon icon={'exclamation-circle' as IconProp} className="w-4 h-4" />
                    <span className="text-sm">{error}</span>
                  </motion.div>
                )}
              </div>

              <div className="flex space-x-3">
                <button
                  type="button"
                  onClick={handleClose}
                  disabled={isSubmitting}
                  className="flex-1 btn-secondary disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting || !apiKey.trim()}
                  className="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Validating...</span>
                    </div>
                  ) : (
                    'Generate Report'
                  )}
                </button>
              </div>
            </form>

            {/* Footer */}
            <div className="mt-4 text-xs text-calm-500 text-center">
              <p>
                By providing your API key, you agree that we&apos;ll use it only to generate your assessment report. 
                You can revoke this key at any time from Google AI Studio.
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
