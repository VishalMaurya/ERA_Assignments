'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon, IconProp } from '@/lib/fontawesome';
import { Assessment, AssessmentReport, AssessmentType } from '@/types';
import { StorageService } from '@/utils/storage';
import { getAssessmentTitle, formatDate } from '@/utils/helpers';
import { useRouter } from 'next/navigation';

interface DashboardData {
  assessments: Assessment[];
  reports: AssessmentReport[];
}

interface AssessmentCardData {
  assessment: Assessment;
  report?: AssessmentReport;
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData>({ assessments: [], reports: [] });
  const [filteredData, setFilteredData] = useState<AssessmentCardData[]>([]);
  const [activeFilter, setActiveFilter] = useState<'all' | AssessmentType>('all');
  const [sortBy, setSortBy] = useState<'date' | 'type' | 'completion'>('date');
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    loadDashboardData();
  }, []);

  useEffect(() => {
    applyFiltersAndSorting();
  }, [data, activeFilter, sortBy]);

  const loadDashboardData = () => {
    try {
      const assessments = StorageService.getAssessments().filter(a => a.isCompleted);
      const reports = StorageService.getReports();
      setData({ assessments, reports });
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyFiltersAndSorting = () => {
    let filtered = data.assessments.map(assessment => ({
      assessment,
      report: data.reports.find(r => r.assessmentId === assessment.id)
    }));

    // Apply filter
    if (activeFilter !== 'all') {
      filtered = filtered.filter(item => item.assessment.type === activeFilter);
    }

    // Apply sorting
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.assessment.completedAt || 0).getTime() - new Date(a.assessment.completedAt || 0).getTime();
        case 'type':
          return a.assessment.type.localeCompare(b.assessment.type);
        case 'completion':
          const aCompletion = (a.assessment.responses.length / a.assessment.questions.length) * 100;
          const bCompletion = (b.assessment.responses.length / b.assessment.questions.length) * 100;
          return bCompletion - aCompletion;
        default:
          return 0;
      }
    });

    setFilteredData(filtered);
  };

  const getAssessmentTypeColor = (type: AssessmentType) => {
    switch (type) {
      case 'anxiety':
        return {
          bg: 'from-blue-500 to-indigo-600',
          accent: 'bg-blue-100 text-blue-700',
          border: 'border-blue-200',
          text: 'text-blue-800',
          icon: 'brain' as IconProp,
          emoji: '🧠'
        };
      case 'ocd':
        return {
          bg: 'from-purple-500 to-violet-600',
          accent: 'bg-purple-100 text-purple-700',
          border: 'border-purple-200',
          text: 'text-purple-800',
          icon: 'bullseye' as IconProp,
          emoji: '🎯'
        };
      case 'anger':
        return {
          bg: 'from-red-500 to-rose-600',
          accent: 'bg-red-100 text-red-700',
          border: 'border-red-200',
          text: 'text-red-800',
          icon: 'fire' as IconProp,
          emoji: '🔥'
        };
      case 'general':
        return {
          bg: 'from-green-500 to-emerald-600',
          accent: 'bg-green-100 text-green-700',
          border: 'border-green-200',
          text: 'text-green-800',
          icon: 'heart' as IconProp,
          emoji: '💚'
        };
    }
  };

  const getCompletionLevel = (assessment: Assessment) => {
    const completion = (assessment.responses.length / assessment.questions.length) * 100;
    if (completion === 100) return { level: 'Complete', color: 'text-green-600', bg: 'bg-green-100' };
    if (completion >= 80) return { level: 'Almost Done', color: 'text-yellow-600', bg: 'bg-yellow-100' };
    return { level: 'Partial', color: 'text-orange-600', bg: 'bg-orange-100' };
  };

  const getTimeSpent = (assessment: Assessment) => {
    if (!assessment.completedAt || !assessment.startedAt) return 'N/A';
    const diffMs = new Date(assessment.completedAt).getTime() - new Date(assessment.startedAt).getTime();
    const minutes = Math.round(diffMs / (1000 * 60));
    if (minutes >= 60) {
      const hours = Math.floor(minutes / 60);
      const remainingMinutes = minutes % 60;
      return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
    }
    return `${minutes}m`;
  };

  const getEmotionalInsight = (assessment: Assessment, report?: AssessmentReport) => {
    if (report) {
      // Use AI-generated severity if available
      const severityLevel = report.severityLevel || 'moderate';
      switch (severityLevel) {
        case 'mild':
          return { text: 'Positive outlook', color: 'text-green-600', icon: 'smile' as IconProp };
        case 'moderate':
          return { text: 'Balanced state', color: 'text-yellow-600', icon: 'meh' as IconProp };
        case 'high':
          return { text: 'Needs attention', color: 'text-red-600', icon: 'frown' as IconProp };
        default:
          return { text: 'Moderate level', color: 'text-blue-600', icon: 'meh' as IconProp };
      }
    }

    // Fallback: analyze mood from responses
    const moods = assessment.responses.map(r => r.mood).filter(Boolean);
    const positiveMoods = moods.filter(m => ['happy', 'calm', 'hopeful'].includes(m || ''));
    const negativeMoods = moods.filter(m => ['sad', 'anxious', 'frustrated'].includes(m || ''));

    if (positiveMoods.length > negativeMoods.length) {
      return { text: 'Positive journey', color: 'text-green-600', icon: 'smile' as IconProp };
    } else if (negativeMoods.length > positiveMoods.length) {
      return { text: 'Challenging path', color: 'text-red-600', icon: 'frown' as IconProp };
    }
    return { text: 'Mixed feelings', color: 'text-yellow-600', icon: 'meh' as IconProp };
  };

  const handleViewReport = (assessmentId: string) => {
    router.push(`/report/${assessmentId}`);
  };

  const handleNewAssessment = () => {
    router.push('/');
  };

  const filterOptions = [
    { key: 'all', label: 'All Assessments', icon: 'chart-bar' as IconProp },
    { key: 'anxiety', label: 'Anxiety', icon: 'brain' as IconProp },
    { key: 'ocd', label: 'OCD', icon: 'bullseye' as IconProp },
    { key: 'anger', label: 'Anger', icon: 'fire' as IconProp },
    { key: 'general', label: 'General', icon: 'heart' as IconProp },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-calm-50 to-primary-50 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-12 h-12 bg-primary-500 rounded-full mx-auto mb-4"
            style={{
              background: 'conic-gradient(from 0deg, transparent, #3B82F6, transparent)'
            }}
          />
          <p className="text-calm-600">Loading your journey...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-calm-50 to-primary-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-calm-200">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <motion.h1 
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-3xl md:text-4xl font-bold text-calm-800 mb-2"
              >
                Your Journey Dashboard 📊
              </motion.h1>
              <motion.p 
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="text-calm-600"
              >
                Track your mental health progress and insights
              </motion.p>
            </div>
            
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleNewAssessment}
              className="btn-primary flex items-center space-x-2 mt-4 md:mt-0"
            >
              <FontAwesomeIcon icon={'home' as IconProp} className="w-4 h-4" />
              <span>New Assessment</span>
            </motion.button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Filters and Stats */}
        <div className="grid lg:grid-cols-4 gap-6 mb-8">
          {/* Quick Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-1"
          >
            <div className="card p-6">
              <h3 className="font-semibold text-calm-800 mb-4 flex items-center">
                <FontAwesomeIcon icon={'chart-line' as IconProp} className="w-5 h-5 mr-2 text-primary-600" />
                Overview
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-calm-600">Total Assessments</span>
                  <span className="font-semibold text-calm-800">{data.assessments.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-calm-600">Reports Generated</span>
                  <span className="font-semibold text-calm-800">{data.reports.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-calm-600">This Month</span>
                  <span className="font-semibold text-calm-800">
                    {data.assessments.filter(a => {
                      const thisMonth = new Date();
                      const completedAt = new Date(a.completedAt || 0);
                      return completedAt.getMonth() === thisMonth.getMonth() && 
                             completedAt.getFullYear() === thisMonth.getFullYear();
                    }).length}
                  </span>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Filters */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-3"
          >
            <div className="card p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <h3 className="font-semibold text-calm-800 mb-2">Filter & Sort</h3>
                  <div className="flex flex-wrap gap-2">
                    {filterOptions.map((option) => (
                      <button
                        key={option.key}
                        onClick={() => setActiveFilter(option.key as any)}
                        className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm transition-all ${
                          activeFilter === option.key
                            ? 'bg-primary-100 text-primary-700 border border-primary-200'
                            : 'bg-calm-100 text-calm-600 hover:bg-calm-200'
                        }`}
                      >
                        <FontAwesomeIcon icon={option.icon} className="w-3 h-3" />
                        <span>{option.label}</span>
                      </button>
                    ))}
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-calm-700 mb-1">Sort by</label>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as any)}
                    className="px-3 py-1.5 border border-calm-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="date">Latest First</option>
                    <option value="type">Assessment Type</option>
                    <option value="completion">Completion Rate</option>
                  </select>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Assessment Cards */}
        {filteredData.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center py-16"
          >
            <div className="w-24 h-24 bg-calm-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FontAwesomeIcon icon={'chart-bar' as IconProp} className="w-8 h-8 text-calm-400" />
            </div>
            <h3 className="text-xl font-semibold text-calm-700 mb-2">No assessments found</h3>
            <p className="text-calm-500 mb-6">
              {activeFilter === 'all' 
                ? "You haven't completed any assessments yet." 
                : `No ${activeFilter} assessments found.`}
            </p>
            <button
              onClick={handleNewAssessment}
              className="btn-primary"
            >
              Start Your First Assessment
            </button>
          </motion.div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <AnimatePresence>
              {filteredData.map((item, index) => {
                const typeColor = getAssessmentTypeColor(item.assessment.type);
                const completion = getCompletionLevel(item.assessment);
                const timeSpent = getTimeSpent(item.assessment);
                const insight = getEmotionalInsight(item.assessment, item.report);

                return (
                  <motion.div
                    key={item.assessment.id}
                    initial={{ opacity: 0, y: 20, scale: 0.9 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -20, scale: 0.9 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    whileHover={{ y: -4, scale: 1.02 }}
                    className="group cursor-pointer"
                    onClick={() => handleViewReport(item.assessment.id)}
                  >
                    <div className={`card overflow-hidden border-2 ${typeColor.border} hover:shadow-xl transition-all duration-300`}>
                      {/* Header with gradient */}
                      <div className={`bg-gradient-to-r ${typeColor.bg} p-4 text-white`}>
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                              <FontAwesomeIcon icon={typeColor.icon} className="w-4 h-4" />
                            </div>
                            <span className="font-semibold">{getAssessmentTitle(item.assessment.type)}</span>
                          </div>
                          <span className="text-2xl">{typeColor.emoji}</span>
                        </div>
                        <p className="text-white/80 text-sm">
                          {formatDate(new Date(item.assessment.completedAt || 0))}
                        </p>
                      </div>

                      {/* Content */}
                      <div className="p-4 space-y-4">
                        {/* Status and Completion */}
                        <div className="flex items-center justify-between">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${completion.bg} ${completion.color}`}>
                            {completion.level}
                          </span>
                          <span className="text-sm text-calm-600">
                            {Math.round((item.assessment.responses.length / item.assessment.questions.length) * 100)}% complete
                          </span>
                        </div>

                        {/* Emotional Insight */}
                        <div className="flex items-center space-x-2">
                          <FontAwesomeIcon icon={insight.icon} className={`w-4 h-4 ${insight.color}`} />
                          <span className={`text-sm font-medium ${insight.color}`}>{insight.text}</span>
                        </div>

                        {/* Stats */}
                        <div className="grid grid-cols-2 gap-4 pt-3 border-t border-calm-100">
                          <div>
                            <p className="text-xs text-calm-500">Time Spent</p>
                            <p className="font-semibold text-calm-700">{timeSpent}</p>
                          </div>
                          <div>
                            <p className="text-xs text-calm-500">Questions</p>
                            <p className="font-semibold text-calm-700">
                              {item.assessment.responses.length}/{item.assessment.questions.length}
                            </p>
                          </div>
                        </div>

                        {/* Report Status */}
                        <div className="flex items-center justify-between pt-3 border-t border-calm-100">
                          {item.report ? (
                            <div className="flex items-center space-x-2 text-green-600">
                              <FontAwesomeIcon icon={'check-circle' as IconProp} className="w-4 h-4" />
                              <span className="text-sm font-medium">Report Available</span>
                            </div>
                          ) : (
                            <div className="flex items-center space-x-2 text-amber-600">
                              <FontAwesomeIcon icon={'clock' as IconProp} className="w-4 h-4" />
                              <span className="text-sm font-medium">Generate Report</span>
                            </div>
                          )}
                          <FontAwesomeIcon 
                            icon={'chevron-right' as IconProp} 
                            className="w-4 h-4 text-calm-400 group-hover:text-primary-500 transition-colors" 
                          />
                        </div>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );
}
