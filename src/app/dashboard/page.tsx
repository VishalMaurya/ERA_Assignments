'use client';

import { useState, useEffect, useMemo } from 'react';
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

interface AnalyticsData {
  totalAssessments: number;
  totalTimeSpent: number; // in minutes
  averageSessionTime: number;
  completionRate: number;
  totalReports: number;
  averageReportGenTime: number; // in milliseconds
  thisMonthAssessments: number;
  improvementTrend: 'improving' | 'stable' | 'declining';
  typeDistribution: Partial<Record<AssessmentType, number>>;
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData>({ assessments: [], reports: [] });
  const [filteredData, setFilteredData] = useState<AssessmentCardData[]>([]);
  const [activeFilter, setActiveFilter] = useState<'all' | AssessmentType>('all');
  const [sortBy, setSortBy] = useState<'date' | 'type' | 'completion'>('date');
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'cards' | 'analytics'>('analytics');
  const router = useRouter();

  // Calculate comprehensive analytics
  const analytics = useMemo<AnalyticsData>(() => {
    const assessments = data.assessments;
    const reports = data.reports;

    if (assessments.length === 0) {
      return {
        totalAssessments: 0,
        totalTimeSpent: 0,
        averageSessionTime: 0,
        completionRate: 0,
        totalReports: 0,
        averageReportGenTime: 0,
        thisMonthAssessments: 0,
        improvementTrend: 'stable',
        typeDistribution: {}
      };
    }

    // Calculate total time spent (in minutes)
    const totalTimeSpentMs = assessments.reduce((total, assessment) => {
      if (assessment.completedAt && assessment.startedAt) {
        return total + (new Date(assessment.completedAt).getTime() - new Date(assessment.startedAt).getTime());
      }
      return total;
    }, 0);
    const totalTimeSpent = Math.round(totalTimeSpentMs / (1000 * 60));

    // Calculate average session time
    const validSessions = assessments.filter(a => a.completedAt && a.startedAt);
    const averageSessionTime = validSessions.length > 0 
      ? Math.round(totalTimeSpent / validSessions.length) 
      : 0;

    // Calculate completion rate
    const totalQuestions = assessments.reduce((total, a) => total + a.questions.length, 0);
    const totalAnswered = assessments.reduce((total, a) => total + a.responses.length, 0);
    const completionRate = totalQuestions > 0 ? Math.round((totalAnswered / totalQuestions) * 100) : 0;

    // Calculate average report generation time
    const reportsWithTime = reports.filter(r => r.generationTimeMs);
    const averageReportGenTime = reportsWithTime.length > 0
      ? Math.round(reportsWithTime.reduce((total, r) => total + (r.generationTimeMs || 0), 0) / reportsWithTime.length)
      : 0;

    // Calculate this month's assessments
    const thisMonth = new Date();
    const thisMonthAssessments = assessments.filter(a => {
      const completedAt = new Date(a.completedAt || 0);
      return completedAt.getMonth() === thisMonth.getMonth() && 
             completedAt.getFullYear() === thisMonth.getFullYear();
    }).length;

    // Calculate type distribution
    const typeDistribution = assessments.reduce((dist, assessment) => {
      dist[assessment.type] = (dist[assessment.type] || 0) + 1;
      return dist;
    }, {} as Record<AssessmentType, number>);

    // Ensure all types are represented (only show types that have data)
    const completeTypeDistribution: Partial<Record<AssessmentType, number>> = {};
    
    // Only include types that have assessments
    Object.entries(typeDistribution).forEach(([type, count]) => {
      if (count > 0) {
        completeTypeDistribution[type as AssessmentType] = count;
      }
    });


    // Calculate improvement trend (simplified)
    const recentAssessments = assessments.filter(a => {
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      return new Date(a.completedAt || 0) >= thirtyDaysAgo;
    });

    let improvementTrend: 'improving' | 'stable' | 'declining' = 'stable';
    if (recentAssessments.length >= 2) {
      const recentAvgCompletion = recentAssessments.reduce((total, a) => 
        total + (a.responses.length / a.questions.length), 0) / recentAssessments.length;
      
      if (recentAvgCompletion > 0.8) improvementTrend = 'improving';
      else if (recentAvgCompletion < 0.6) improvementTrend = 'declining';
    }

    return {
      totalAssessments: assessments.length,
      totalTimeSpent,
      averageSessionTime,
      completionRate,
      totalReports: reports.length,
      averageReportGenTime,
      thisMonthAssessments,
      improvementTrend,
      typeDistribution: completeTypeDistribution
    };
  }, [data]);

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
      // CBT Family
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
      case 'behavioral-activation':
        return {
          bg: 'from-cyan-500 to-blue-600',
          accent: 'bg-cyan-100 text-cyan-700',
          border: 'border-cyan-200',
          text: 'text-cyan-800',
          icon: 'play' as IconProp,
          emoji: '🎬'
        };
      case 'habit-reversal':
        return {
          bg: 'from-indigo-500 to-purple-600',
          accent: 'bg-indigo-100 text-indigo-700',
          border: 'border-indigo-200',
          text: 'text-indigo-800',
          icon: 'arrow-right' as IconProp,
          emoji: '🔄'
        };
      case 'problem-solving':
        return {
          bg: 'from-emerald-500 to-teal-600',
          accent: 'bg-emerald-100 text-emerald-700',
          border: 'border-emerald-200',
          text: 'text-emerald-800',
          icon: 'lightbulb' as IconProp,
          emoji: '🧩'
        };
      
      // Mindfulness & Acceptance
      case 'mindfulness':
        return {
          bg: 'from-teal-500 to-green-600',
          accent: 'bg-teal-100 text-teal-700',
          border: 'border-teal-200',
          text: 'text-teal-800',
          icon: 'leaf' as IconProp,
          emoji: '🍃'
        };
      case 'acceptance-commitment':
        return {
          bg: 'from-lime-500 to-green-600',
          accent: 'bg-lime-100 text-lime-700',
          border: 'border-lime-200',
          text: 'text-lime-800',
          icon: 'leaf' as IconProp,
          emoji: '🌱'
        };
      case 'mindful-cognitive':
        return {
          bg: 'from-green-500 to-emerald-600',
          accent: 'bg-green-100 text-green-700',
          border: 'border-green-200',
          text: 'text-green-800',
          icon: 'tree' as IconProp,
          emoji: '🌳'
        };
      
      // Emotion Regulation & Interpersonal
      case 'anger':
        return {
          bg: 'from-red-500 to-rose-600',
          accent: 'bg-red-100 text-red-700',
          border: 'border-red-200',
          text: 'text-red-800',
          icon: 'fire' as IconProp,
          emoji: '🔥'
        };
      case 'emotion-regulation':
        return {
          bg: 'from-rose-500 to-pink-600',
          accent: 'bg-rose-100 text-rose-700',
          border: 'border-rose-200',
          text: 'text-rose-800',
          icon: 'heart' as IconProp,
          emoji: '💗'
        };
      case 'interpersonal':
        return {
          bg: 'from-pink-500 to-rose-600',
          accent: 'bg-pink-100 text-pink-700',
          border: 'border-pink-200',
          text: 'text-pink-800',
          icon: 'user' as IconProp,
          emoji: '👥'
        };
      
      // Compassion & Self-Kindness
      case 'self-compassion':
        return {
          bg: 'from-amber-500 to-orange-600',
          accent: 'bg-amber-100 text-amber-700',
          border: 'border-amber-200',
          text: 'text-amber-800',
          icon: 'heart' as IconProp,
          emoji: '🤗'
        };
      case 'positive-psychology':
        return {
          bg: 'from-yellow-500 to-amber-600',
          accent: 'bg-yellow-100 text-yellow-700',
          border: 'border-yellow-200',
          text: 'text-yellow-800',
          icon: 'sun' as IconProp,
          emoji: '☀️'
        };
      case 'strengths':
        return {
          bg: 'from-orange-500 to-red-600',
          accent: 'bg-orange-100 text-orange-700',
          border: 'border-orange-200',
          text: 'text-orange-800',
          icon: 'award' as IconProp,
          emoji: '🏆'
        };
      
      // Lifestyle & Holistic
      case 'sleep':
        return {
          bg: 'from-slate-500 to-gray-600',
          accent: 'bg-slate-100 text-slate-700',
          border: 'border-slate-200',
          text: 'text-slate-800',
          icon: 'moon' as IconProp,
          emoji: '🌙'
        };
      case 'relaxation':
        return {
          bg: 'from-sky-500 to-blue-600',
          accent: 'bg-sky-100 text-sky-700',
          border: 'border-sky-200',
          text: 'text-sky-800',
          icon: 'cloud' as IconProp,
          emoji: '☁️'
        };
      case 'breathing':
        return {
          bg: 'from-cyan-500 to-teal-600',
          accent: 'bg-cyan-100 text-cyan-700',
          border: 'border-cyan-200',
          text: 'text-cyan-800',
          icon: 'cloud' as IconProp,
          emoji: '💨'
        };
      case 'exercise':
        return {
          bg: 'from-violet-500 to-purple-600',
          accent: 'bg-violet-100 text-violet-700',
          border: 'border-violet-200',
          text: 'text-violet-800',
          icon: 'play' as IconProp,
          emoji: '💪'
        };
      case 'nutrition':
        return {
          bg: 'from-green-500 to-lime-600',
          accent: 'bg-green-100 text-green-700',
          border: 'border-green-200',
          text: 'text-green-800',
          icon: 'heart' as IconProp,
          emoji: '🍎'
        };
      
      // Specialized Therapies
      case 'trauma':
        return {
          bg: 'from-gray-500 to-slate-600',
          accent: 'bg-gray-100 text-gray-700',
          border: 'border-gray-200',
          text: 'text-gray-800',
          icon: 'shield-alt' as IconProp,
          emoji: '🛡️'
        };
      case 'schema':
        return {
          bg: 'from-stone-500 to-gray-600',
          accent: 'bg-stone-100 text-stone-700',
          border: 'border-stone-200',
          text: 'text-stone-800',
          icon: 'chart-bar' as IconProp,
          emoji: '🗺️'
        };
      case 'narrative':
        return {
          bg: 'from-fuchsia-500 to-purple-600',
          accent: 'bg-fuchsia-100 text-fuchsia-700',
          border: 'border-fuchsia-200',
          text: 'text-fuchsia-800',
          icon: 'book-open' as IconProp,
          emoji: '📖'
        };
      case 'motivation':
        return {
          bg: 'from-red-500 to-orange-600',
          accent: 'bg-red-100 text-red-700',
          border: 'border-red-200',
          text: 'text-red-800',
          icon: 'arrow-up' as IconProp,
          emoji: '🚀'
        };
      case 'solution-focused':
        return {
          bg: 'from-emerald-500 to-green-600',
          accent: 'bg-emerald-100 text-emerald-700',
          border: 'border-emerald-200',
          text: 'text-emerald-800',
          icon: 'lightbulb' as IconProp,
          emoji: '💡'
        };
      
      // General
      case 'general':
        return {
          bg: 'from-blue-500 to-indigo-600',
          accent: 'bg-blue-100 text-blue-700',
          border: 'border-blue-200',
          text: 'text-blue-800',
          icon: 'heart' as IconProp,
          emoji: '💚'
        };
      
      // Default fallback
      default:
        return {
          bg: 'from-gray-500 to-slate-600',
          accent: 'bg-gray-100 text-gray-700',
          border: 'border-gray-200',
          text: 'text-gray-800',
          icon: 'question' as IconProp,
          emoji: '❓'
        };
    }
  };

  const formatTime = (minutes: number) => {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
  };

  const formatGenTime = (ms: number) => {
    if (ms < 1000) return `${ms}ms`;
    const seconds = Math.round(ms / 1000 * 10) / 10;
    return `${seconds}s`;
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving': return { icon: 'arrow-up' as IconProp, color: 'text-green-600', bg: 'bg-green-100' };
      case 'declining': return { icon: 'arrow-down' as IconProp, color: 'text-red-600', bg: 'bg-red-100' };
      default: return { icon: 'minus' as IconProp, color: 'text-yellow-600', bg: 'bg-yellow-100' };
    }
  };

  const handleViewReport = (assessmentId: string) => {
    router.push(`/report/${assessmentId}`);
  };

  const handleNewAssessment = () => {
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-calm-50 to-primary-50 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
          role="status"
          aria-live="polite"
          aria-label="Loading dashboard data"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-12 h-12 bg-primary-500 rounded-full mx-auto mb-4"
            style={{
              background: 'conic-gradient(from 0deg, transparent, #3B82F6, transparent)'
            }}
            aria-hidden="true"
          />
          <p className="text-calm-600">Loading your analytics...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-calm-50 to-primary-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-calm-200">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <motion.h1 
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-3xl md:text-4xl font-bold text-calm-800 mb-2 flex items-center"
                id="dashboard-title"
              >
                <FontAwesomeIcon icon={'chart-line' as IconProp} className="w-8 h-8 mr-3 text-primary-600" aria-hidden="true" />
                Mental Health Analytics
              </motion.h1>
              <motion.p 
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="text-calm-600"
                aria-describedby="dashboard-title"
              >
                Comprehensive insights into your mental health journey
              </motion.p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-3">
              {/* View Mode Toggle */}
              <div className="flex bg-calm-100 rounded-lg p-1" role="tablist" aria-label="Dashboard view modes">
                <button
                  onClick={() => setViewMode('analytics')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                    viewMode === 'analytics'
                      ? 'bg-white text-primary-700 shadow-sm'
                      : 'text-calm-600 hover:text-calm-800'
                  }`}
                  role="tab"
                  aria-selected={viewMode === 'analytics'}
                  aria-controls="analytics-panel"
                >
                  <FontAwesomeIcon icon={'chart-bar' as IconProp} className="w-4 h-4 mr-2" aria-hidden="true" />
                  Analytics
                </button>
                <button
                  onClick={() => setViewMode('cards')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                    viewMode === 'cards'
                      ? 'bg-white text-primary-700 shadow-sm'
                      : 'text-calm-600 hover:text-calm-800'
                  }`}
                  role="tab"
                  aria-selected={viewMode === 'cards'}
                  aria-controls="cards-panel"
                >
                  <FontAwesomeIcon icon={'chart-bar' as IconProp} className="w-4 h-4 mr-2" aria-hidden="true" />
                  Assessments
                </button>
              </div>

              <motion.button
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleNewAssessment}
                className="btn-primary flex items-center space-x-2"
                aria-label="Start a new mental health assessment"
              >
                <FontAwesomeIcon icon={'plus' as IconProp} className="w-4 h-4" aria-hidden="true" />
                <span>New Assessment</span>
              </motion.button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {viewMode === 'analytics' ? (
            <motion.div
              key="analytics"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              id="analytics-panel"
              role="tabpanel"
              aria-labelledby="analytics-tab"
            >
              {/* Key Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="card p-6"
                  role="region"
                  aria-labelledby="total-assessments-heading"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                      <FontAwesomeIcon icon={'clipboard' as IconProp} className="w-6 h-6 text-blue-600" aria-hidden="true" />
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getTrendIcon(analytics.improvementTrend).bg} ${getTrendIcon(analytics.improvementTrend).color}`}>
                      <FontAwesomeIcon icon={getTrendIcon(analytics.improvementTrend).icon} className="w-3 h-3 mr-1" aria-hidden="true" />
                      {analytics.improvementTrend}
                    </span>
                  </div>
                  <h3 id="total-assessments-heading" className="text-2xl font-bold text-calm-800 mb-1">{analytics.totalAssessments}</h3>
                  <p className="text-calm-600 text-sm">Total Assessments</p>
                  <p className="text-xs text-calm-500 mt-2">{analytics.thisMonthAssessments} this month</p>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="card p-6"
                  role="region"
                  aria-labelledby="time-invested-heading"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                      <FontAwesomeIcon icon={'clock' as IconProp} className="w-6 h-6 text-green-600" aria-hidden="true" />
                    </div>
                    <span className="text-xs text-calm-500">
                      Avg: {formatTime(analytics.averageSessionTime)}
                    </span>
                  </div>
                  <h3 id="time-invested-heading" className="text-2xl font-bold text-calm-800 mb-1">{formatTime(analytics.totalTimeSpent)}</h3>
                  <p className="text-calm-600 text-sm">Time Invested</p>
                  <div className="mt-2 w-full bg-calm-200 rounded-full h-2">
                    <div 
                      className="bg-green-500 h-2 rounded-full transition-all duration-500" 
                      style={{ width: `${Math.min(100, (analytics.totalTimeSpent / 1000) * 100)}%` }}
                      aria-label={`Progress: ${analytics.totalTimeSpent} minutes of total time invested`}
                    ></div>
                  </div>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                  className="card p-6"
                  role="region"
                  aria-labelledby="completion-rate-heading"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                      <FontAwesomeIcon icon={'check-circle' as IconProp} className="w-6 h-6 text-purple-600" aria-hidden="true" />
                    </div>
                    <span className={`text-xs font-medium ${analytics.completionRate >= 80 ? 'text-green-600' : analytics.completionRate >= 60 ? 'text-yellow-600' : 'text-red-600'}`}>
                      {analytics.completionRate >= 80 ? 'Excellent' : analytics.completionRate >= 60 ? 'Good' : 'Needs Focus'}
                    </span>
                  </div>
                  <h3 id="completion-rate-heading" className="text-2xl font-bold text-calm-800 mb-1">{analytics.completionRate}%</h3>
                  <p className="text-calm-600 text-sm">Completion Rate</p>
                  <div className="mt-2 w-full bg-calm-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full transition-all duration-500 ${
                        analytics.completionRate >= 80 ? 'bg-green-500' : 
                        analytics.completionRate >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${analytics.completionRate}%` }}
                      aria-label={`Completion rate: ${analytics.completionRate} percent`}
                    ></div>
                  </div>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="card p-6"
                  role="region"
                  aria-labelledby="ai-performance-heading"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
                      <FontAwesomeIcon icon={'wand-sparkles' as IconProp} className="w-6 h-6 text-indigo-600" aria-hidden="true" />
                    </div>
                    <span className="text-xs text-calm-500">
                      {analytics.totalReports} reports
                    </span>
                  </div>
                  <h3 id="ai-performance-heading" className="text-2xl font-bold text-calm-800 mb-1">
                    {analytics.averageReportGenTime > 0 ? formatGenTime(analytics.averageReportGenTime) : 'N/A'}
                  </h3>
                  <p className="text-calm-600 text-sm">AI Generation Time</p>
                  <p className="text-xs text-calm-500 mt-2">Powered by Gemini 2.0</p>
                </motion.div>
              </div>

              {/* Main Dashboard Layout */}
              <div className="grid lg:grid-cols-4 gap-6">
                {/* Left Sidebar - Analytics */}
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 }}
                  className="lg:col-span-1 space-y-6"
                >
                  {/* Assessment Type Distribution */}
                  <div className="card p-6 bg-gradient-to-br from-white to-calm-50 shadow-lg" role="region" aria-labelledby="type-distribution-heading">
                    <h3 id="type-distribution-heading" className="text-lg font-bold text-calm-800 mb-6 flex items-center">
                      <FontAwesomeIcon icon={'chart-pie' as IconProp} className="w-5 h-5 mr-3 text-primary-600" aria-hidden="true" />
                      Assessment Types
                    </h3>
                    <div className="space-y-4">
                      {Object.entries(analytics.typeDistribution).map(([type, count]) => {
                        const typeInfo = getAssessmentTypeColor(type as AssessmentType);
                        const percentage = analytics.totalAssessments > 0 ? Math.round((count / analytics.totalAssessments) * 100) : 0;
                        return (
                          <div key={type} className="group">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center space-x-3">
                                <div className={`w-4 h-4 rounded-full bg-gradient-to-r ${typeInfo.bg} shadow-sm`} aria-hidden="true"></div>
                                <span className="text-sm font-semibold text-calm-700 capitalize">{type}</span>
                              </div>
                              <div className="flex items-center space-x-2">
                                <span className="text-sm font-bold text-calm-800">{count}</span>
                                <span className="text-xs text-calm-500 bg-calm-100 px-2 py-1 rounded-full">{percentage}%</span>
                              </div>
                            </div>
                            {/* Progress bar */}
                            <div className="w-full bg-calm-200 rounded-full h-2">
                              <div 
                                className={`bg-gradient-to-r ${typeInfo.bg} h-2 rounded-full transition-all duration-500 ease-out`}
                                style={{ width: `${percentage}%` }}
                              ></div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    
                    {analytics.totalAssessments === 0 && (
                      <div className="text-center py-6">
                        <FontAwesomeIcon icon={'chart-pie' as IconProp} className="w-8 h-8 text-calm-300 mb-2" />
                        <p className="text-sm text-calm-500">No assessments completed yet</p>
                      </div>
                    )}
                  </div>

                  {/* Quick Actions & Stats */}
                  <div className="card p-6 bg-gradient-to-br from-white to-primary-50 shadow-lg" role="region" aria-labelledby="quick-nav-heading">
                    <h3 id="quick-nav-heading" className="text-lg font-bold text-calm-800 mb-6 flex items-center">
                      <FontAwesomeIcon icon={'arrow-up' as IconProp} className="w-5 h-5 mr-3 text-primary-600" aria-hidden="true" />
                      Quick Actions
                    </h3>
                    
                    {/* Key Stats */}
                    <div className="grid grid-cols-2 gap-3 mb-6">
                      <div className="bg-white rounded-lg p-3 text-center shadow-sm">
                        <p className="text-2xl font-bold text-primary-600">{analytics.totalAssessments}</p>
                        <p className="text-xs text-calm-600">Total</p>
                      </div>
                      <div className="bg-white rounded-lg p-3 text-center shadow-sm">
                        <p className="text-2xl font-bold text-green-600">{analytics.totalReports}</p>
                        <p className="text-xs text-calm-600">Reports</p>
                      </div>
                    </div>
                    
                    <div className="space-y-3">
                      <button
                        onClick={handleNewAssessment}
                        className="w-full flex items-center space-x-3 p-4 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 rounded-lg transition-all duration-200 transform hover:scale-105 text-white shadow-md"
                        aria-label="Start a new mental health assessment"
                      >
                        <FontAwesomeIcon icon={'plus' as IconProp} className="w-5 h-5" aria-hidden="true" />
                        <div className="text-left">
                          <div className="font-semibold">New Assessment</div>
                          <div className="text-xs text-white/80">Start your journey</div>
                        </div>
                      </button>
                      
                      <button
                        onClick={() => setActiveFilter('all')}
                        className="w-full flex items-center space-x-3 p-4 bg-white hover:bg-calm-50 rounded-lg transition-all duration-200 transform hover:scale-105 text-left border border-calm-200 shadow-sm"
                        aria-label="View all assessment reports"
                      >
                        <FontAwesomeIcon icon={'chart-bar' as IconProp} className="w-5 h-5 text-calm-600" aria-hidden="true" />
                        <div>
                          <div className="font-semibold text-calm-700">View All Reports</div>
                          <div className="text-xs text-calm-500">Browse insights</div>
                        </div>
                      </button>
                      
                      {analytics.totalAssessments > 0 && (
                        <div className="pt-3 border-t border-calm-200">
                          <div className="text-xs text-calm-500 mb-2">Completion Rate</div>
                          <div className="flex items-center space-x-2">
                            <div className="flex-1 bg-calm-200 rounded-full h-2">
                              <div 
                                className="bg-gradient-to-r from-green-400 to-green-500 h-2 rounded-full transition-all duration-500"
                                style={{ width: `${analytics.completionRate}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-bold text-green-600">{analytics.completionRate}%</span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>

                {/* Right Content - Report Cards */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 }}
                  className="lg:col-span-3"
                >
                  <div className="mb-6">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
                      <div>
                        <h3 className="text-xl font-semibold text-calm-800 mb-2 flex items-center">
                          <FontAwesomeIcon icon={'file-text' as IconProp} className="w-6 h-6 mr-3 text-primary-600" aria-hidden="true" />
                          Assessment Reports
                        </h3>
                        <p className="text-calm-600">Comprehensive insights from your mental health assessments</p>
                      </div>
                      
                      {/* Filters */}
                      <div className="flex flex-wrap gap-2">
                        {[
                          { key: 'all', label: 'All', icon: 'chart-bar' as IconProp },
                          // CBT Family
                          { key: 'anxiety', label: 'Anxiety', icon: 'brain' as IconProp },
                          { key: 'ocd', label: 'OCD', icon: 'bullseye' as IconProp },
                          { key: 'behavioral-activation', label: 'Behavioral', icon: 'play' as IconProp },
                          // Mindfulness
                          { key: 'mindfulness', label: 'Mindfulness', icon: 'leaf' as IconProp },
                          // Emotions
                          { key: 'anger', label: 'Anger', icon: 'fire' as IconProp },
                          { key: 'emotion-regulation', label: 'Emotions', icon: 'heart' as IconProp },
                          // Lifestyle
                          { key: 'sleep', label: 'Sleep', icon: 'moon' as IconProp },
                          { key: 'exercise', label: 'Exercise', icon: 'play' as IconProp },
                          // Specialized
                          { key: 'trauma', label: 'Trauma', icon: 'shield-alt' as IconProp },
                          { key: 'general', label: 'General', icon: 'heart' as IconProp },
                        ].map((option) => (
                          <button
                            key={option.key}
                            onClick={() => setActiveFilter(option.key as any)}
                            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm transition-all ${
                              activeFilter === option.key
                                ? 'bg-primary-100 text-primary-700 border border-primary-200'
                                : 'bg-calm-100 text-calm-600 hover:bg-calm-200'
                            }`}
                            aria-pressed={activeFilter === option.key}
                            aria-label={`Filter by ${option.label} assessments`}
                          >
                            <FontAwesomeIcon icon={option.icon} className="w-3 h-3" aria-hidden="true" />
                            <span>{option.label}</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>

                  {filteredData.length === 0 ? (
                    <div className="text-center py-16">
                      <div className="w-24 h-24 bg-calm-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <FontAwesomeIcon icon={'file-text' as IconProp} className="w-8 h-8 text-calm-400" aria-hidden="true" />
                      </div>
                      <h4 className="text-xl font-semibold text-calm-700 mb-2">No reports available</h4>
                      <p className="text-calm-500 mb-6">
                        {data.assessments.length === 0 
                          ? "Complete your first assessment to see insights here." 
                          : "Generate reports from your completed assessments."}
                      </p>
                      <button
                        onClick={handleNewAssessment}
                        className="btn-primary"
                        aria-label="Start your first mental health assessment"
                      >
                        {data.assessments.length === 0 ? "Start First Assessment" : "New Assessment"}
                      </button>
                    </div>
                  ) : (
                    <div className="grid md:grid-cols-2 gap-6 items-stretch" role="list" aria-label="Assessment report cards">
                      <AnimatePresence>
                        {filteredData.map((item, index) => {
                          const typeColor = getAssessmentTypeColor(item.assessment.type);
                          const completion = (item.assessment.responses.length / item.assessment.questions.length) * 100;
                          const timeSpent = item.assessment.completedAt && item.assessment.startedAt
                            ? Math.round((new Date(item.assessment.completedAt).getTime() - new Date(item.assessment.startedAt).getTime()) / (1000 * 60))
                            : 0;

                          return (
                            <motion.div
                              key={item.assessment.id}
                              initial={{ opacity: 0, y: 20, scale: 0.95 }}
                              animate={{ opacity: 1, y: 0, scale: 1 }}
                              exit={{ opacity: 0, y: -20, scale: 0.95 }}
                              transition={{ duration: 0.3, delay: index * 0.1 }}
                              whileHover={{ y: -4, scale: 1.02 }}
                              className="group cursor-pointer h-full"
                              onClick={() => handleViewReport(item.assessment.id)}
                              role="listitem"
                            >
                              <div className={`card overflow-hidden border-2 ${typeColor.border} hover:shadow-xl transition-all duration-300 h-full flex flex-col`}>
                                {/* Header */}
                                <div className={`bg-gradient-to-r ${typeColor.bg} p-6 text-white`}>
                                  <div className="flex items-center mb-4">
                                    <FontAwesomeIcon icon={typeColor.icon} className="w-6 h-6 mr-3" aria-hidden="true" />
                                    <div className="flex-1">
                                      <h4 className="font-bold text-xl leading-tight">{getAssessmentTitle(item.assessment.type)}</h4>
                                      <p className="text-white/80 text-sm mt-1">{formatDate(new Date(item.assessment.completedAt || 0))}</p>
                                    </div>
                                  </div>
                                  
                                  {/* Quick Stats in Header */}
                                  <div className="grid grid-cols-2 gap-4 text-center">
                                    <div className="bg-white/10 rounded-lg p-2">
                                      <p className="text-white/70 text-xs">Completion</p>
                                      <p className="font-bold text-lg">{Math.round(completion)}%</p>
                                    </div>
                                    <div className="bg-white/10 rounded-lg p-2">
                                      <p className="text-white/70 text-xs">Duration</p>
                                      <p className="font-bold text-lg">{timeSpent > 0 ? formatTime(timeSpent) : 'N/A'}</p>
                                    </div>
                                  </div>
                                </div>

                                {/* Content */}
                                <div className="p-6 space-y-4 flex-1 flex flex-col">
                                  {/* Top Section */}
                                  <div className="space-y-4">
                                    {/* Report Status */}
                                    <div className="flex items-center justify-between">
                                      {item.report ? (
                                        <div className="flex items-center space-x-2 text-green-600">
                                          <FontAwesomeIcon icon={'check-circle' as IconProp} className="w-5 h-5" aria-hidden="true" />
                                          <span className="font-semibold">Report Generated</span>
                                        </div>
                                      ) : (
                                        <div className="flex items-center space-x-2 text-amber-600">
                                          <FontAwesomeIcon icon={'clock' as IconProp} className="w-5 h-5" aria-hidden="true" />
                                          <span className="font-semibold">Report Pending</span>
                                        </div>
                                      )}
                                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                                        completion === 100 ? 'bg-green-100 text-green-700' :
                                        completion >= 80 ? 'bg-yellow-100 text-yellow-700' :
                                        'bg-orange-100 text-orange-700'
                                      }`}>
                                        {completion === 100 ? 'Complete' : completion >= 80 ? 'Nearly Complete' : 'Partial'}
                                      </span>
                                    </div>

                                    {/* Assessment Details */}
                                    <div className="bg-calm-50 rounded-lg p-4">
                                      <div className="grid grid-cols-3 gap-4 text-center">
                                        <div>
                                          <p className="text-xs text-calm-500 mb-1">Questions Answered</p>
                                          <p className="font-bold text-calm-800">{item.assessment.responses.length}/{item.assessment.questions.length}</p>
                                        </div>
                                        <div>
                                          <p className="text-xs text-calm-500 mb-1">Response Rate</p>
                                          <p className="font-bold text-calm-800">{Math.round(completion)}%</p>
                                        </div>
                                        <div>
                                          <p className="text-xs text-calm-500 mb-1">Skipped Questions</p>
                                          <p className="font-bold text-calm-800">{item.assessment.skippedQuestions.length}</p>
                                        </div>
                                      </div>
                                    </div>
                                  </div>

                                  {/* Bottom Section - AI Details and Action */}
                                  <div className="mt-auto space-y-4">
                                    {/* AI Generation Details or Placeholder */}
                                    <div className="border-t border-calm-100 pt-4 min-h-[120px] flex flex-col justify-between">
                                      {item.report ? (
                                        <div>
                                          <div className="flex items-center justify-between mb-3">
                                            <h5 className="font-semibold text-calm-800 flex items-center">
                                              <FontAwesomeIcon icon={'wand-sparkles' as IconProp} className="w-4 h-4 mr-2 text-indigo-500" aria-hidden="true" />
                                              AI Analysis
                                            </h5>
                                            {item.report.severityLevel && (
                                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                                item.report.severityLevel === 'mild' ? 'bg-green-100 text-green-700' :
                                                item.report.severityLevel === 'moderate' ? 'bg-yellow-100 text-yellow-700' :
                                                'bg-red-100 text-red-700'
                                              }`}>
                                                {item.report.severityLevel} level
                                              </span>
                                            )}
                                          </div>
                                          
                                          <div className="grid grid-cols-2 gap-4 text-sm mb-3">
                                            <div>
                                              <p className="text-calm-500 mb-1">Report Generation Time</p>
                                              <p className="font-medium text-indigo-600">
                                                {item.report.generationTimeMs ? formatGenTime(item.report.generationTimeMs) : 'N/A'}
                                              </p>
                                            </div>
                                            <div>
                                              <p className="text-calm-500 mb-1">AI Model Used</p>
                                              <p className="font-medium text-indigo-600">Gemini 2.0 Flash</p>
                                            </div>
                                          </div>
                                          
                                          {item.report.recommendations.length > 0 && (
                                            <div className="pt-3 border-t border-calm-100">
                                              <p className="text-xs text-calm-500 mb-2">Generated Insights</p>
                                              <div className="flex flex-wrap gap-2">
                                                <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                                                  {item.report.recommendations.length} Recommendations
                                                </span>
                                                <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-xs">
                                                  {item.report.insights.length} Key Insights
                                                </span>
                                                <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs">
                                                  {item.report.nextSteps.length} Action Steps
                                                </span>
                                              </div>
                                            </div>
                                          )}
                                        </div>
                                      ) : (
                                        <div className="flex flex-col items-center justify-center py-6 text-center">
                                          <FontAwesomeIcon icon={'clock' as IconProp} className="w-8 h-8 text-amber-400 mb-2" aria-hidden="true" />
                                          <p className="text-sm font-medium text-calm-700 mb-1">Report Generation Pending</p>
                                          <p className="text-xs text-calm-500">Click to generate AI-powered insights</p>
                                        </div>
                                      )}
                                    </div>

                                    {/* Action Button */}
                                    <div className="flex items-center justify-between pt-4 border-t border-calm-100">
                                      <div className="text-xs text-calm-500">
                                        Click to {item.report ? 'view full report' : 'generate report'}
                                      </div>
                                      <FontAwesomeIcon 
                                        icon={'chevron-right' as IconProp} 
                                        className="w-5 h-5 text-calm-400 group-hover:text-primary-500 transition-colors" 
                                        aria-hidden="true"
                                      />
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </motion.div>
                          );
                        })}
                      </AnimatePresence>
                    </div>
                  )}
                </motion.div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="cards"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              id="cards-panel"
              role="tabpanel"
              aria-labelledby="cards-tab"
            >
              {/* Filters and Controls */}
              <div className="card p-6 mb-6">
                <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                  <div>
                    <h3 className="font-semibold text-calm-800 mb-2">Filter & Sort Assessments</h3>
                    <div className="flex flex-wrap gap-2">
                      {[
                        { key: 'all', label: 'All Types', icon: 'chart-bar' as IconProp },
                        // CBT Family
                        { key: 'anxiety', label: 'Anxiety', icon: 'brain' as IconProp },
                        { key: 'ocd', label: 'OCD', icon: 'bullseye' as IconProp },
                        { key: 'behavioral-activation', label: 'Behavioral', icon: 'play' as IconProp },
                        // Mindfulness
                        { key: 'mindfulness', label: 'Mindfulness', icon: 'leaf' as IconProp },
                        // Emotions
                        { key: 'anger', label: 'Anger', icon: 'fire' as IconProp },
                        { key: 'emotion-regulation', label: 'Emotions', icon: 'heart' as IconProp },
                        // Lifestyle
                        { key: 'sleep', label: 'Sleep', icon: 'moon' as IconProp },
                        { key: 'exercise', label: 'Exercise', icon: 'play' as IconProp },
                        // Specialized
                        { key: 'trauma', label: 'Trauma', icon: 'shield-alt' as IconProp },
                        { key: 'general', label: 'General', icon: 'heart' as IconProp },
                      ].map((option) => (
                        <button
                          key={option.key}
                          onClick={() => setActiveFilter(option.key as any)}
                          className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm transition-all ${
                            activeFilter === option.key
                              ? 'bg-primary-100 text-primary-700 border border-primary-200'
                              : 'bg-calm-100 text-calm-600 hover:bg-calm-200'
                          }`}
                          aria-pressed={activeFilter === option.key}
                          aria-label={`Filter by ${option.label} assessments`}
                        >
                          <FontAwesomeIcon icon={option.icon} className="w-3 h-3" aria-hidden="true" />
                          <span>{option.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <label htmlFor="sort-select" className="block text-sm font-medium text-calm-700 mb-1">Sort by</label>
                    <select
                      id="sort-select"
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value as any)}
                      className="px-3 py-1.5 border border-calm-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      aria-label="Sort assessments by"
                    >
                      <option value="date">Latest First</option>
                      <option value="type">Assessment Type</option>
                      <option value="completion">Completion Rate</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Assessment Cards */}
              {filteredData.length === 0 ? (
                <div className="text-center py-16">
                  <div className="w-24 h-24 bg-calm-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <FontAwesomeIcon icon={'chart-bar' as IconProp} className="w-8 h-8 text-calm-400" aria-hidden="true" />
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
                    aria-label="Start your first mental health assessment"
                  >
                    Start Your First Assessment
                  </button>
                </div>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6" role="list" aria-label="Assessment cards">
                  <AnimatePresence>
                    {filteredData.map((item, index) => {
                      const typeColor = getAssessmentTypeColor(item.assessment.type);
                      const completion = (item.assessment.responses.length / item.assessment.questions.length) * 100;
                      const timeSpent = item.assessment.completedAt && item.assessment.startedAt
                        ? Math.round((new Date(item.assessment.completedAt).getTime() - new Date(item.assessment.startedAt).getTime()) / (1000 * 60))
                        : 0;

                      return (
                        <motion.div
                          key={item.assessment.id}
                          initial={{ opacity: 0, y: 20, scale: 0.9 }}
                          animate={{ opacity: 1, y: 0, scale: 1 }}
                          exit={{ opacity: 0, y: -20, scale: 0.9 }}
                          transition={{ duration: 0.3, delay: index * 0.05 }}
                          whileHover={{ y: -4, scale: 1.02 }}
                          className="group cursor-pointer"
                          onClick={() => handleViewReport(item.assessment.id)}
                          role="listitem"
                        >
                          <div className={`card overflow-hidden border-2 ${typeColor.border} hover:shadow-xl transition-all duration-300`}>
                            {/* Header */}
                            <div className={`bg-gradient-to-r ${typeColor.bg} p-4 text-white`}>
                              <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center space-x-2">
                                  <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                                    <FontAwesomeIcon icon={typeColor.icon} className="w-4 h-4" aria-hidden="true" />
                                  </div>
                                  <span className="font-semibold">{getAssessmentTitle(item.assessment.type)}</span>
                                </div>
                                <span className="text-2xl" aria-hidden="true">{typeColor.emoji}</span>
                              </div>
                              <p className="text-white/80 text-sm">
                                {formatDate(new Date(item.assessment.completedAt || 0))}
                              </p>
                            </div>

                            {/* Content */}
                            <div className="p-4 space-y-4">
                              {/* Completion Status */}
                              <div className="flex items-center justify-between">
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                  completion === 100 ? 'bg-green-100 text-green-700' :
                                  completion >= 80 ? 'bg-yellow-100 text-yellow-700' :
                                  'bg-orange-100 text-orange-700'
                                }`}>
                                  {completion === 100 ? 'Complete' : completion >= 80 ? 'Almost Done' : 'Partial'}
                                </span>
                                <span className="text-sm text-calm-600">{Math.round(completion)}%</span>
                              </div>

                              {/* Stats */}
                              <div className="grid grid-cols-2 gap-4 pt-3 border-t border-calm-100">
                                <div>
                                  <p className="text-xs text-calm-500">Time Spent</p>
                                  <p className="font-semibold text-calm-700">{timeSpent > 0 ? formatTime(timeSpent) : 'N/A'}</p>
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
                                    <FontAwesomeIcon icon={'check-circle' as IconProp} className="w-4 h-4" aria-hidden="true" />
                                    <span className="text-sm font-medium">Report Available</span>
                                  </div>
                                ) : (
                                  <div className="flex items-center space-x-2 text-amber-600">
                                    <FontAwesomeIcon icon={'clock' as IconProp} className="w-4 h-4" aria-hidden="true" />
                                    <span className="text-sm font-medium">Generate Report</span>
                                  </div>
                                )}
                                <FontAwesomeIcon 
                                  icon={'chevron-right' as IconProp} 
                                  className="w-4 h-4 text-calm-400 group-hover:text-primary-500 transition-colors" 
                                  aria-hidden="true"
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
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}