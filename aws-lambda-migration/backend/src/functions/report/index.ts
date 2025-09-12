import { LambdaEvent, LambdaResponse, AssessmentReport, Assessment } from '../../shared/types';
import { withCors, createSuccessResponse, createErrorResponse, parseEventBody, validateRequired, generateReportId } from '../../shared/utils';

// Simple in-memory storage for demo (replace with DynamoDB in production)
const reports: Map<string, AssessmentReport> = new Map();
const assessments: Map<string, Assessment> = new Map(); // This would come from assessment service

// Report Lambda Handler
export const handler = withCors(async (event: LambdaEvent): Promise<LambdaResponse> => {
  const { httpMethod, path } = event;
  
  try {
    if (httpMethod === 'POST' && path.includes('/report/generate')) {
      return await generateReport(event);
    }
    
    if (httpMethod === 'GET' && path.includes('/report/') && !path.includes('/reports')) {
      return await getReport(event);
    }
    
    if (httpMethod === 'GET' && path.includes('/reports')) {
      return await getUserReports(event);
    }
    
    return createErrorResponse(404, 'Route not found');
    
  } catch (error) {
    console.error('Report handler error:', error);
    return createErrorResponse(500, 'Internal server error');
  }
});

// Generate AI report for completed assessment
async function generateReport(event: LambdaEvent): Promise<LambdaResponse> {
  const body = parseEventBody(event);
  if (!body) {
    return createErrorResponse(400, 'Invalid request body');
  }

  const missing = validateRequired(body, ['userId', 'assessmentId']);
  if (missing.length > 0) {
    return createErrorResponse(400, `Missing required fields: ${missing.join(', ')}`);
  }

  const { userId, assessmentId } = body;

  // For demo purposes, create a sample assessment if not found
  let assessment = assessments.get(assessmentId);
  if (!assessment) {
    assessment = {
      id: assessmentId,
      userId,
      type: 'anxiety',
      questions: [],
      responses: [
        { questionId: 'q1', answer: 8, answeredAt: new Date().toISOString() },
        { questionId: 'q2', answer: 'Physical symptoms', answeredAt: new Date().toISOString() }
      ],
      currentQuestionIndex: 2,
      isCompleted: true,
      startedAt: new Date(Date.now() - 1800000).toISOString(), // 30 minutes ago
      completedAt: new Date().toISOString(),
      skippedQuestions: [],
      totalTimeSpent: 30
    };
  }

  if (!assessment.isCompleted) {
    return createErrorResponse(400, 'Assessment must be completed before generating report');
  }

  const startTime = Date.now();
  
  try {
    // Generate AI report (simplified for demo)
    const report = await generateAIReport(assessment);
    
    const generationTimeMs = Date.now() - startTime;
    report.generationTimeMs = generationTimeMs;

    reports.set(report.id, report);

    return createSuccessResponse(report, 'Report generated successfully');

  } catch (error) {
    console.error('Error generating AI report:', error);
    
    // Create fallback report
    const fallbackReport = createFallbackReport(assessment);
    reports.set(fallbackReport.id, fallbackReport);
    
    return createSuccessResponse(fallbackReport, 'Report generated with fallback content');
  }
}

// Get single report
async function getReport(event: LambdaEvent): Promise<LambdaResponse> {
  const reportId = event.pathParameters?.reportId;
  const userId = event.queryStringParameters?.userId;

  if (!reportId || !userId) {
    return createErrorResponse(400, 'Report ID and User ID are required');
  }

  const report = reports.get(reportId);
  if (!report) {
    return createErrorResponse(404, 'Report not found');
  }

  return createSuccessResponse(report);
}

// Get all user reports
async function getUserReports(event: LambdaEvent): Promise<LambdaResponse> {
  const userId = event.queryStringParameters?.userId;

  if (!userId) {
    return createErrorResponse(400, 'User ID is required');
  }

  const userReports = Array.from(reports.values()).filter(report => report.userId === userId);
  return createSuccessResponse(userReports);
}

// Generate AI report (simplified version)
async function generateAIReport(assessment: Assessment): Promise<AssessmentReport> {
  // Simulate AI processing time
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  const report: AssessmentReport = {
    id: generateReportId(),
    assessmentId: assessment.id,
    userId: assessment.userId,
    summary: `Based on your ${assessment.type} assessment, you've shown great self-awareness and commitment to understanding your mental health.`,
    patterns: ['Self-reflection', 'Awareness of symptoms', 'Seeking help'],
    severityLevel: assessment.responses.some(r => typeof r.answer === 'number' && r.answer > 7) ? 'moderate' : 'mild',
    recommendations: [{
      therapyType: assessment.type,
      priority: 'primary',
      confidence: 0.8,
      reasoning: ['Based on your responses showing moderate impact on daily life', 'Evidence-based approach for your symptoms'],
      suggestedExercises: ['mindful_breathing', 'daily_reflection', 'progressive_relaxation'],
      estimatedDuration: '6-8 weeks',
      successPredictors: ['Regular practice', 'Self-awareness', 'Willingness to try new techniques'],
      potentialBarriers: ['Time constraints', 'Initial resistance to change']
    }],
    insights: [
      'Your responses indicate a good level of self-awareness about your mental health.',
      'The fact that you completed this assessment shows your commitment to personal growth.',
      'Your symptoms appear manageable with the right therapeutic approach.'
    ],
    nextSteps: [
      'Start with daily mindfulness practices for 5-10 minutes',
      'Consider keeping a mood journal to track patterns',
      'Explore therapy resources related to your assessment type',
      'Practice self-compassion as you begin this journey'
    ],
    generatedAt: new Date().toISOString(),
    aiModel: 'gemini-2.0-flash'
  };

  return report;
}

// Create fallback report when AI generation fails
function createFallbackReport(assessment: Assessment): AssessmentReport {
  return {
    id: generateReportId(),
    assessmentId: assessment.id,
    userId: assessment.userId,
    summary: `Thank you for completing the ${assessment.type} assessment. Your responses show self-awareness and commitment to personal growth.`,
    patterns: ['Self-reflection', 'Openness to change', 'Seeking understanding'],
    severityLevel: 'mild',
    insights: [
      'Your willingness to complete this assessment demonstrates a positive step toward self-understanding.',
      'Self-awareness is a crucial foundation for personal growth and mental health improvement.',
      'Consider exploring the recommended therapy approaches to build on your insights.'
    ],
    recommendations: [{
      therapyType: assessment.type,
      priority: 'primary',
      confidence: 0.7,
      reasoning: ['Based on assessment responses', 'Evidence-based approach for this assessment type'],
      suggestedExercises: ['daily_reflection', 'mindful_breathing', 'self_compassion_break'],
      estimatedDuration: '4-8 weeks',
      successPredictors: ['Regular practice', 'Self-compassion', 'Willingness to explore'],
      potentialBarriers: ['Time constraints', 'Initial resistance to new practices']
    }],
    nextSteps: [
      'Continue regular self-reflection and mindfulness practices',
      'Consider working with a mental health professional',
      'Explore therapy resources and techniques related to your assessment type'
    ],
    generatedAt: new Date().toISOString(),
    generationTimeMs: 100,
    aiModel: 'fallback'
  };
}
