'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconProp } from '@fortawesome/fontawesome-svg-core';
import { Assessment, AssessmentReport } from '@/types';
import { StorageService } from '@/utils/storage';
import { GeminiService } from '@/lib/gemini';
import ReportGeneration from '@/components/report/ReportGeneration';
import ReportDisplay from '@/components/report/ReportDisplay';
import ApiKeyModal from '@/components/ui/ApiKeyModal';
import ApiTestModal from '@/components/ui/ApiTestModal';

export default function ReportPage() {
  const params = useParams();
  const router = useRouter();
  const assessmentId = params.assessmentId as string;

  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [report, setReport] = useState<AssessmentReport | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStage, setGenerationStage] = useState('');
  const [error, setError] = useState('');
  const [showApiKeyModal, setShowApiKeyModal] = useState(false);
  const [showApiTestModal, setShowApiTestModal] = useState(false);

  useEffect(() => {
    loadAssessment();
  }, [assessmentId]);

  const loadAssessment = () => {
    // First check completed assessments
    const assessments = StorageService.getAssessments();
    let foundAssessment = assessments.find(a => a.id === assessmentId);

    // If not found, check current assessment
    if (!foundAssessment) {
      const currentAssessment = StorageService.getCurrentAssessment();
      if (currentAssessment?.id === assessmentId) {
        foundAssessment = currentAssessment;
      }
    }

    if (!foundAssessment) {
      router.push('/');
      return;
    }

    setAssessment(foundAssessment);

    // Check if report already exists
    const existingReport = StorageService.getReportByAssessmentId(assessmentId);
    if (existingReport) {
      setReport(existingReport);
    } else {
      // Check if API key is available and start generation
      const apiKey = StorageService.getGeminiApiKey();
      if (!apiKey) {
        setShowApiKeyModal(true);
      } else {
        generateReport(foundAssessment, apiKey);
      }
    }
  };

  const generateReport = async (assessmentData: Assessment, apiKey: string) => {
    setIsGenerating(true);
    setError('');
    
    try {
      setGenerationStage('Initializing AI analysis...');
      const geminiService = new GeminiService(apiKey);
      
      setGenerationStage('Analyzing your responses...');
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setGenerationStage('Identifying patterns and insights...');
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setGenerationStage('Generating personalized recommendations...');
      const generatedReport = await geminiService.generateAssessmentReport(assessmentData);
      
      setGenerationStage('Finalizing your report...');
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Save the report
      StorageService.saveReport(generatedReport);
      setReport(generatedReport);
      
    } catch (err) {
      console.error('Error generating report:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate report');
    } finally {
      setIsGenerating(false);
      setGenerationStage('');
    }
  };

  const handleApiKeySubmit = (apiKey: string) => {
    StorageService.saveGeminiApiKey(apiKey);
    setShowApiKeyModal(false);
    if (assessment) {
      generateReport(assessment, apiKey);
    }
  };

  const handleRetryGeneration = () => {
    const apiKey = StorageService.getGeminiApiKey();
    if (!apiKey) {
      setShowApiKeyModal(true);
    } else if (assessment) {
      generateReport(assessment, apiKey);
    }
  };

  const handleNewAssessment = () => {
    router.push('/');
  };

  const handleViewDashboard = () => {
    router.push('/dashboard');
  };

  const handleApiKeyValidated = (apiKey: string) => {
    StorageService.saveGeminiApiKey(apiKey);
    setShowApiTestModal(false);
    // Automatically retry report generation with the validated API key
    if (assessment) {
      generateReport(assessment, apiKey);
    }
  };

  if (!assessment) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-calm-600">Loading assessment...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-calm-50 to-primary-50">
      {/* Dashboard Link */}
      <motion.button
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.5 }}
        onClick={() => router.push('/dashboard')}
        className="fixed top-4 right-4 z-30 bg-emerald-600 hover:bg-emerald-700 text-white p-3 rounded-full shadow-lg transition-colors"
        title="Go to Dashboard"
      >
        <FontAwesomeIcon icon={'chart-line' as IconProp} className="w-5 h-5" />
      </motion.button>

      <AnimatePresence mode="wait">
        {isGenerating ? (
          <ReportGeneration
            key="generation"
            assessmentType={assessment.type}
            stage={generationStage}
            onCancel={() => setIsGenerating(false)}
          />
        ) : report ? (
          <ReportDisplay
            key="report"
            report={report}
            assessment={assessment}
            onNewAssessment={handleNewAssessment}
            onViewDashboard={handleViewDashboard}
          />
        ) : error ? (
          <motion.div
            key="error"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="min-h-screen flex items-center justify-center p-4"
          >
            <div className="card p-8 max-w-md text-center">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h2 className="text-xl font-semibold text-calm-800 mb-2">
                Report Generation Failed
              </h2>
              <p className="text-calm-600 mb-4">
                {error}
              </p>
              {error.includes('API key') && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                  <p className="text-sm text-blue-800">
                    <strong>Need help?</strong> Get your free Gemini API key from{' '}
                    <a 
                      href="https://makersuite.google.com/app/apikey" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="underline hover:text-blue-900"
                    >
                      Google AI Studio
                    </a>
                  </p>
                </div>
              )}
              {error.includes('quota') && (
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-6">
                  <p className="text-sm text-orange-800">
                    <strong>Quota exceeded:</strong> Please wait a moment and try again, or check your API billing settings.
                  </p>
                </div>
              )}
              {error.includes('Network') && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
                  <p className="text-sm text-yellow-800">
                    <strong>Connection issue:</strong> Please check your internet connection and try again.
                  </p>
                </div>
              )}
              <div className="space-y-3">
                {error.includes('API key') ? (
                  <>
                    <button
                      onClick={() => setShowApiKeyModal(true)}
                      className="btn-primary w-full"
                    >
                      Enter API Key
                    </button>
                    <button
                      onClick={() => setShowApiTestModal(true)}
                      className="btn-secondary w-full"
                    >
                      Test API Key
                    </button>
                    <button
                      onClick={handleRetryGeneration}
                      className="btn-secondary w-full"
                    >
                      Try Again
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      onClick={handleRetryGeneration}
                      className="btn-primary w-full"
                    >
                      Try Again
                    </button>
                    <button
                      onClick={() => setShowApiTestModal(true)}
                      className="btn-secondary w-full"
                    >
                      Test API Key
                    </button>
                  </>
                )}
                <button
                  onClick={handleNewAssessment}
                  className="btn-secondary w-full"
                >
                  Return Home
                </button>
              </div>
            </div>
          </motion.div>
        ) : null}
      </AnimatePresence>

      <ApiKeyModal
        isOpen={showApiKeyModal}
        onClose={() => setShowApiKeyModal(false)}
        onSubmit={handleApiKeySubmit}
      />

      <ApiTestModal
        isOpen={showApiTestModal}
        onClose={() => setShowApiTestModal(false)}
        onApiKeyValidated={handleApiKeyValidated}
      />
    </div>
  );
}
