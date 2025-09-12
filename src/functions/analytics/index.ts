import { LambdaEvent, LambdaResponse } from '../../shared/types';
import { withCors, createSuccessResponse, createErrorResponse } from '../../shared/utils';

// Analytics Lambda Handler
export const handler = withCors(async (event: LambdaEvent): Promise<LambdaResponse> => {
  const { httpMethod, path } = event;
  
  try {
    if (httpMethod === 'GET' && path.includes('/analytics/dashboard')) {
      return await getDashboardAnalytics(event);
    }
    
    if (httpMethod === 'GET' && path.includes('/analytics/progress')) {
      return await getProgressAnalytics(event);
    }
    
    return createErrorResponse(404, 'Route not found');
    
  } catch (error) {
    console.error('Analytics handler error:', error);
    return createErrorResponse(500, 'Internal server error');
  }
});

// Get dashboard analytics
async function getDashboardAnalytics(event: LambdaEvent): Promise<LambdaResponse> {
  const userId = event.queryStringParameters?.userId;

  if (!userId) {
    return createErrorResponse(400, 'User ID is required');
  }

  // Sample analytics data
  const analytics = {
    totalAssessments: 5,
    totalTimeSpent: 150, // minutes
    averageSessionTime: 30,
    completionRate: 80,
    totalReports: 3,
    thisMonthAssessments: 2,
    improvementTrend: 'improving',
    typeDistribution: {
      'anxiety': 2,
      'mindfulness': 1,
      'sleep': 1,
      'self-compassion': 1
    },
    lastAssessmentDate: new Date().toISOString().split('T')[0],
    nextRecommendedAssessment: 'emotion-regulation'
  };

  return createSuccessResponse(analytics);
}

// Get progress analytics
async function getProgressAnalytics(event: LambdaEvent): Promise<LambdaResponse> {
  const userId = event.queryStringParameters?.userId;

  if (!userId) {
    return createErrorResponse(400, 'User ID is required');
  }

  // Sample progress data
  const progress = {
    progressTimeline: [
      {
        date: '2024-01-01',
        assessmentType: 'anxiety',
        severityLevel: 'moderate',
        insightsCount: 3,
        recommendationsCount: 2
      },
      {
        date: '2024-01-15',
        assessmentType: 'mindfulness',
        severityLevel: 'mild',
        insightsCount: 4,
        recommendationsCount: 1
      }
    ],
    wellbeingTrend: [
      { date: '2024-01-01', score: 6.5, assessmentType: 'anxiety' },
      { date: '2024-01-15', score: 7.2, assessmentType: 'mindfulness' },
      { date: '2024-01-30', score: 7.8, assessmentType: 'sleep' }
    ],
    therapyEffectiveness: {
      'anxiety': { count: 2, effectiveness: 0.85 },
      'mindfulness': { count: 1, effectiveness: 0.92 }
    },
    milestoneAchievements: [
      {
        title: 'First Assessment Completed',
        description: 'Took the first step in your mental health journey',
        date: '2024-01-01',
        icon: '🎯'
      }
    ]
  };

  return createSuccessResponse(progress);
}
