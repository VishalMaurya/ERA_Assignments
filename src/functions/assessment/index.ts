import { LambdaEvent, LambdaResponse, Assessment, AssessmentType } from '../../shared/types';
import { withCors, createSuccessResponse, createErrorResponse, parseEventBody, validateRequired, generateAssessmentId } from '../../shared/utils';

// Simple in-memory storage for demo (replace with DynamoDB in production)
const assessments: Map<string, Assessment> = new Map();

// Assessment Lambda Handler
export const handler = withCors(async (event: LambdaEvent): Promise<LambdaResponse> => {
  const { httpMethod, path } = event;
  
  try {
    if (httpMethod === 'POST' && path.includes('/assessment/start')) {
      return await startAssessment(event);
    }
    
    if (httpMethod === 'PUT' && path.includes('/assessment/')) {
      return await updateAssessment(event);
    }
    
    if (httpMethod === 'POST' && path.includes('/complete')) {
      return await completeAssessment(event);
    }
    
    if (httpMethod === 'GET' && path.includes('/assessment/')) {
      return await getAssessment(event);
    }
    
    return createErrorResponse(404, 'Route not found');
    
  } catch (error) {
    console.error('Assessment handler error:', error);
    return createErrorResponse(500, 'Internal server error');
  }
});

// Start a new assessment
async function startAssessment(event: LambdaEvent): Promise<LambdaResponse> {
  const body = parseEventBody(event);
  if (!body) {
    return createErrorResponse(400, 'Invalid request body');
  }

  const missing = validateRequired(body, ['userId', 'type']);
  if (missing.length > 0) {
    return createErrorResponse(400, `Missing required fields: ${missing.join(', ')}`);
  }

  const { userId, type } = body;
  
  // Get sample questions for assessment type
  const questions = getSampleQuestions(type);
  
  const assessment: Assessment = {
    id: generateAssessmentId(),
    userId,
    type,
    questions,
    responses: [],
    currentQuestionIndex: 0,
    isCompleted: false,
    startedAt: new Date().toISOString(),
    skippedQuestions: [],
    totalTimeSpent: 0
  };

  assessments.set(assessment.id, assessment);
  
  return createSuccessResponse(assessment, 'Assessment started successfully');
}

// Update assessment with new response
async function updateAssessment(event: LambdaEvent): Promise<LambdaResponse> {
  const assessmentId = event.pathParameters?.assessmentId;
  if (!assessmentId) {
    return createErrorResponse(400, 'Assessment ID is required');
  }

  const body = parseEventBody(event);
  if (!body) {
    return createErrorResponse(400, 'Invalid request body');
  }

  const assessment = assessments.get(assessmentId);
  if (!assessment) {
    return createErrorResponse(404, 'Assessment not found');
  }

  const { response, currentQuestionIndex, timeSpent } = body;

  if (response) {
    const existingResponseIndex = assessment.responses.findIndex(r => r.questionId === response.questionId);
    
    if (existingResponseIndex >= 0) {
      assessment.responses[existingResponseIndex] = response;
    } else {
      assessment.responses.push(response);
    }
  }

  if (currentQuestionIndex !== undefined) {
    assessment.currentQuestionIndex = currentQuestionIndex;
  }

  if (timeSpent) {
    assessment.totalTimeSpent += timeSpent;
  }

  assessments.set(assessmentId, assessment);

  return createSuccessResponse(assessment, 'Assessment updated successfully');
}

// Complete assessment
async function completeAssessment(event: LambdaEvent): Promise<LambdaResponse> {
  const assessmentId = event.pathParameters?.assessmentId;
  if (!assessmentId) {
    return createErrorResponse(400, 'Assessment ID is required');
  }

  const assessment = assessments.get(assessmentId);
  if (!assessment) {
    return createErrorResponse(404, 'Assessment not found');
  }

  assessment.isCompleted = true;
  assessment.completedAt = new Date().toISOString();

  assessments.set(assessmentId, assessment);

  return createSuccessResponse(assessment, 'Assessment completed successfully');
}

// Get single assessment
async function getAssessment(event: LambdaEvent): Promise<LambdaResponse> {
  const assessmentId = event.pathParameters?.assessmentId;

  if (!assessmentId) {
    return createErrorResponse(400, 'Assessment ID is required');
  }

  const assessment = assessments.get(assessmentId);
  if (!assessment) {
    return createErrorResponse(404, 'Assessment not found');
  }

  return createSuccessResponse(assessment);
}

// Get sample questions for assessment type
function getSampleQuestions(type: AssessmentType) {
  return [
    {
      id: `${type}_1`,
      type: 'scale',
      text: `How much does ${type} affect your daily life?`,
      environment: 'ocean',
      scaleRange: [1, 10],
      scaleLabels: ['Not at all', 'Significantly'],
      therapyMapping: [type]
    },
    {
      id: `${type}_2`,
      type: 'mcq',
      text: `Which symptoms do you experience most with ${type}?`,
      environment: 'forest',
      options: ['Physical symptoms', 'Emotional symptoms', 'Behavioral changes', 'Cognitive symptoms'],
      therapyMapping: [type]
    },
    {
      id: `${type}_3`,
      type: 'open-ended',
      text: `Describe a recent situation where ${type} impacted you.`,
      environment: 'garden',
      therapyMapping: [type]
    }
  ];
}
