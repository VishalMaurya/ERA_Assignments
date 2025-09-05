'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { FontAwesomeIcon, IconProp } from '@/lib/fontawesome';
import { AssessmentReport, Assessment, TherapyRecommendation } from '@/types';
import { getAssessmentTitle, formatDate, downloadAsJSON } from '@/utils/helpers';

interface ReportDisplayProps {
  report: AssessmentReport;
  assessment: Assessment;
  onNewAssessment: () => void;
  onViewDashboard: () => void;
}

export default function ReportDisplay({ 
  report, 
  assessment, 
  onNewAssessment, 
  onViewDashboard 
}: ReportDisplayProps) {
  const [activeSection, setActiveSection] = useState<string>('summary');

  const sections = [
    { id: 'summary', title: 'Summary', icon: 'heart' as IconProp },
    { id: 'patterns', title: 'Patterns', icon: 'chart-bar' as IconProp },
    { id: 'insights', title: 'Insights', icon: 'lightbulb' as IconProp },
    { id: 'raw-responses', title: 'Your Responses', icon: 'file-text' as IconProp },
    { id: 'recommendations', title: 'Recommendations', icon: 'bullseye' as IconProp },
    { id: 'next-steps', title: 'Next Steps', icon: 'arrow-up' as IconProp }
  ];

  const getSeverityColor = (level: string) => {
    switch (level) {
      case 'mild':
        return 'text-green-600 bg-green-100';
      case 'moderate':
        return 'text-yellow-600 bg-yellow-100';
      case 'high':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'primary':
        return 'border-l-red-500 bg-red-50';
      case 'secondary':
        return 'border-l-yellow-500 bg-yellow-50';
      case 'supplementary':
        return 'border-l-green-500 bg-green-50';
      default:
        return 'border-l-gray-500 bg-gray-50';
    }
  };

  const handleDownloadReport = () => {
    const reportData = {
      assessment: {
        type: assessment.type,
        completedAt: assessment.completedAt,
        totalQuestions: assessment.questions.length,
        responsesCount: assessment.responses.length
      },
      report: {
        ...report,
        generatedAt: report.generatedAt
      }
    };
    
    downloadAsJSON(reportData, `${assessment.type}-assessment-report-${new Date().toISOString().split('T')[0]}`);
  };

  const renderRecommendationCard = (recommendation: TherapyRecommendation, index: number) => (
    <motion.div
      key={index}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className={`p-6 rounded-lg border-l-4 ${getPriorityColor(recommendation.priority)} mb-6`}
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-calm-800 mb-2">
            {recommendation.therapyType.replace('-', ' ').replace(/^\w/, c => c.toUpperCase())} Therapy
          </h3>
          <span className="inline-block px-3 py-1 text-xs font-medium bg-primary-100 text-primary-700 rounded-full mb-2">
            {recommendation.priority}
          </span>
          <p className="text-calm-600">
            {recommendation.reasoning.join(' ')}
          </p>
        </div>
        <span className={`px-2 py-1 text-xs font-medium rounded ${
          recommendation.priority === 'primary' ? 'bg-red-100 text-red-700' :
          recommendation.priority === 'secondary' ? 'bg-yellow-100 text-yellow-700' :
          'bg-green-100 text-green-700'
        }`}>
          {recommendation.priority} priority
        </span>
      </div>

      {recommendation.suggestedExercises.length > 0 && (
        <div className="mb-4">
          <h4 className="font-medium text-calm-700 mb-2 flex items-center">
            <FontAwesomeIcon icon={'bullseye' as IconProp} className="w-4 h-4 mr-2" />
            Recommended Exercises
          </h4>
          <ul className="space-y-2">
            {recommendation.suggestedExercises.map((exercise, i) => (
              <li key={i} className="flex items-start space-x-2">
                <FontAwesomeIcon icon={'chevron-right' as IconProp} className="w-4 h-4 text-primary-500 mt-0.5 flex-shrink-0" />
                <span className="text-sm text-calm-600">{exercise}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {recommendation.successPredictors.length > 0 && (
        <div>
          <h4 className="font-medium text-calm-700 mb-2 flex items-center">
            <FontAwesomeIcon icon={'star' as IconProp} className="w-4 h-4 mr-2 text-yellow-500" />
            Success Factors
          </h4>
          <ul className="space-y-1">
            {recommendation.successPredictors.map((factor, i) => (
              <li key={i} className="text-sm text-calm-600 flex items-start">
                <FontAwesomeIcon icon={'check' as IconProp} className="w-3 h-3 mr-2 text-green-500 mt-0.5 flex-shrink-0" />
                {factor}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );

  const renderSectionContent = () => {
    switch (activeSection) {
      case 'summary':
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="bg-gradient-to-r from-primary-50 to-nature-50 p-6 rounded-lg border border-primary-200">
              <h3 className="text-lg font-semibold text-calm-800 mb-4 flex items-center">
                <FontAwesomeIcon icon={'heart' as IconProp} className="w-5 h-5 mr-2 text-primary-600" />
                Your Journey Summary
              </h3>
              <p className="text-calm-700 leading-relaxed text-lg">
                {report.summary}
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="card p-6">
                <h4 className="font-semibold text-calm-800 mb-3">Assessment Details</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-calm-600">Type:</span>
                    <span className="font-medium">{getAssessmentTitle(assessment.type)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-calm-600">Completed:</span>
                    <span className="font-medium">{formatDate(new Date(report.generatedAt))}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-calm-600">Questions Answered:</span>
                    <span className="font-medium">{assessment.responses.length} of {assessment.questions.length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-calm-600">Severity Level:</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(report.severityLevel)}`}>
                      {report.severityLevel.charAt(0).toUpperCase() + report.severityLevel.slice(1)}
                    </span>
                  </div>
                </div>
              </div>

              <div className="card p-6">
                <h4 className="font-semibold text-calm-800 mb-3">Report Overview</h4>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-calm-600 text-sm">Patterns Identified</span>
                    <span className="bg-primary-100 text-primary-700 px-2 py-1 rounded text-sm font-medium">
                      {report.patterns.length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-calm-600 text-sm">Key Insights</span>
                    <span className="bg-nature-100 text-nature-700 px-2 py-1 rounded text-sm font-medium">
                      {report.insights.length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-calm-600 text-sm">Recommendations</span>
                    <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded text-sm font-medium">
                      {report.recommendations.length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-calm-600 text-sm">Action Steps</span>
                    <span className="bg-orange-100 text-orange-700 px-2 py-1 rounded text-sm font-medium">
                      {report.nextSteps.length}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        );

      case 'patterns':
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-calm-800 mb-2 flex items-center">
                <FontAwesomeIcon icon={'chart-bar' as IconProp} className="w-5 h-5 mr-2 text-primary-600" />
                Behavioral Patterns Identified
              </h3>
              <p className="text-calm-600">
                Based on your responses, we&apos;ve identified these key patterns in your thoughts, feelings, and behaviors.
              </p>
            </div>

            <div className="grid gap-4">
              {report.patterns.map((pattern, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="card p-6 border-l-4 border-l-primary-500"
                >
                  <div className="flex items-start space-x-4">
                    <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-primary-600 font-semibold text-sm">{index + 1}</span>
                    </div>
                    <div>
                      <p className="text-calm-700 leading-relaxed">{pattern}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        );

      case 'insights':
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-calm-800 mb-2 flex items-center">
                <FontAwesomeIcon icon={'lightbulb' as IconProp} className="w-5 h-5 mr-2 text-yellow-600" />
                Personal Insights
              </h3>
              <p className="text-calm-600">
                These insights are derived from your unique response patterns and can help guide your personal growth journey.
              </p>
            </div>

            <div className="space-y-4">
              {report.insights.map((insight, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="bg-gradient-to-r from-yellow-50 to-orange-50 p-6 rounded-lg border border-yellow-200"
                >
                  <div className="flex items-start space-x-4">
                    <FontAwesomeIcon icon={'star' as IconProp} className="w-6 h-6 text-yellow-500 flex-shrink-0 mt-1" />
                    <p className="text-calm-700 leading-relaxed">{insight}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        );

      case 'raw-responses':
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-calm-800 mb-2 flex items-center">
                <FontAwesomeIcon icon={'file-text' as IconProp} className="w-5 h-5 mr-2 text-indigo-600" />
                Your Original Responses
              </h3>
              <p className="text-calm-600">
                A complete record of your answers during the assessment for your reference.
              </p>
            </div>

            <div className="space-y-4">
              {assessment.responses.map((response, index) => {
                const question = assessment.questions.find(q => q.id === response.questionId);
                return (
                  <motion.div
                    key={response.questionId}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: index * 0.05 }}
                    className="card p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="space-y-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <span className="text-xs font-medium bg-indigo-100 text-indigo-700 px-2 py-1 rounded">
                              Question {index + 1}
                            </span>
                            <span className="text-xs text-calm-400">
                              {new Date(response.timestamp).toLocaleString()}
                            </span>
                          </div>
                          <h4 className="font-medium text-calm-800 mb-2">
                            {question?.question || 'Question not found'}
                          </h4>
                        </div>
                        {response.mood && (
                          <div className="flex items-center space-x-1 text-sm">
                            <span className="text-calm-500">Mood:</span>
                            <span className="capitalize text-calm-700">{response.mood}</span>
                          </div>
                        )}
                      </div>
                      
                      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-4 rounded-lg border border-indigo-200">
                        <div className="flex items-start space-x-3">
                          <FontAwesomeIcon icon={'chevron-right' as IconProp} className="w-4 h-4 text-indigo-500 mt-0.5 flex-shrink-0" />
                          <div className="flex-1">
                            <span className="text-sm font-medium text-indigo-800">Your Response:</span>
                            <p className="text-indigo-700 mt-1">
                              {Array.isArray(response.answer) 
                                ? response.answer.join(', ') 
                                : response.answer}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </div>

            {assessment.skippedQuestions.length > 0 && (
              <div className="mt-8">
                <h4 className="font-medium text-calm-700 mb-4 flex items-center">
                  <FontAwesomeIcon icon={'forward' as IconProp} className="w-4 h-4 mr-2 text-amber-500" />
                  Skipped Questions ({assessment.skippedQuestions.length})
                </h4>
                <div className="space-y-3">
                  {assessment.skippedQuestions.map((questionId, index) => {
                    const question = assessment.questions.find(q => q.id === questionId);
                    return (
                      <div key={questionId} className="bg-amber-50 border border-amber-200 p-4 rounded-lg">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="text-xs font-medium bg-amber-100 text-amber-700 px-2 py-1 rounded">
                            Skipped
                          </span>
                        </div>
                        <p className="text-amber-800 text-sm">
                          {question?.question || 'Question not found'}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </motion.div>
        );

      case 'recommendations':
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-calm-800 mb-2 flex items-center">
                <FontAwesomeIcon icon={'bullseye' as IconProp} className="w-5 h-5 mr-2 text-green-600" />
                Personalized Recommendations
              </h3>
              <p className="text-calm-600">
                These evidence-based therapeutic approaches are tailored to your specific patterns and needs.
              </p>
            </div>

            {report.recommendations.map((recommendation, index) => 
              renderRecommendationCard(recommendation, index)
            )}
          </motion.div>
        );

      case 'next-steps':
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-calm-800 mb-2 flex items-center">
                <FontAwesomeIcon icon={'arrow-up' as IconProp} className="w-5 h-5 mr-2 text-purple-600" />
                Your Next Steps
              </h3>
              <p className="text-calm-600">
                Practical actions you can take starting today to support your mental health journey.
              </p>
            </div>

            <div className="space-y-4">
              {report.nextSteps.map((step, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="card p-6 hover:shadow-lg transition-shadow"
                >
                  <div className="flex items-start space-x-4">
                    <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-purple-600 font-semibold text-sm">{index + 1}</span>
                    </div>
                    <div className="flex-1">
                      <p className="text-calm-700 leading-relaxed">{step}</p>
                    </div>
                    <FontAwesomeIcon icon={'calendar' as IconProp} className="w-5 h-5 text-purple-500 flex-shrink-0 mt-1" />
                  </div>
                </motion.div>
              ))}
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-8">
              <h4 className="font-semibold text-blue-800 mb-3">Remember</h4>
              <p className="text-blue-700 text-sm leading-relaxed">
                Mental health is a journey, not a destination. Progress takes time, and it&apos;s okay to have setbacks. 
                Be patient and compassionate with yourself as you implement these strategies. If you&apos;re experiencing 
                severe symptoms, please consider reaching out to a mental health professional.
              </p>
            </div>
          </motion.div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-calm-50 to-primary-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-calm-200">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-calm-800 mb-2">
                Your Personal Report
              </h1>
              <div className="space-y-1">
                <p className="text-calm-600">
                  {getAssessmentTitle(assessment.type)} • Generated {formatDate(new Date(report.generatedAt))}
                </p>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-calm-500">Powered by</span>
                  <div className="flex items-center space-x-1">
                    <FontAwesomeIcon icon={'wand-sparkles' as IconProp} className="w-4 h-4 text-blue-600" />
                    <span className="text-sm font-semibold text-blue-600">Gemini AI</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-3 mt-4 md:mt-0">
              <button
                onClick={handleDownloadReport}
                className="btn-secondary flex items-center space-x-2"
              >
                <FontAwesomeIcon icon={'download' as IconProp} className="w-4 h-4" />
                <span>Download</span>
              </button>
              <button
                onClick={onViewDashboard}
                className="btn-secondary flex items-center space-x-2"
              >
                <FontAwesomeIcon icon={'chart-bar' as IconProp} className="w-4 h-4" />
                <span>Dashboard</span>
              </button>
              <button
                onClick={onNewAssessment}
                className="btn-primary flex items-center space-x-2"
              >
                <FontAwesomeIcon icon={'home' as IconProp} className="w-4 h-4" />
                <span>New Assessment</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Navigation Sidebar */}
          <div className="lg:col-span-1">
            <div className="card p-6 sticky top-8">
              <h3 className="font-semibold text-calm-800 mb-4">Report Sections</h3>
              <nav className="space-y-2">
                {sections.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                      activeSection === section.id
                        ? 'bg-primary-100 text-primary-700 border border-primary-200'
                        : 'text-calm-600 hover:bg-calm-100'
                    }`}
                  >
                    <FontAwesomeIcon icon={section.icon} className="w-4 h-4" />
                    <span>{section.title}</span>
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="card p-8">
              {renderSectionContent()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
