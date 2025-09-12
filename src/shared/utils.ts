import { LambdaResponse, LambdaEvent } from './types';

export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
  'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
  'Content-Type': 'application/json',
};

export const createResponse = <T>(
  statusCode: number,
  data?: T,
  error?: string,
  message?: string
): LambdaResponse => {
  const response = {
    success: statusCode >= 200 && statusCode < 300,
    timestamp: new Date().toISOString(),
    ...(data !== undefined && { data }),
    ...(error && { error }),
    ...(message && { message })
  };

  return {
    statusCode,
    headers: corsHeaders,
    body: JSON.stringify(response),
  };
};

export const createSuccessResponse = <T>(data: T, message?: string): LambdaResponse => {
  return createResponse(200, data, undefined, message);
};

export const createErrorResponse = (statusCode: number, error: string): LambdaResponse => {
  return createResponse(statusCode, undefined, error);
};

export const parseEventBody = <T>(event: LambdaEvent): T | null => {
  if (!event.body) return null;
  
  try {
    return JSON.parse(event.body) as T;
  } catch (error) {
    console.error('Error parsing event body:', error);
    return null;
  }
};

export const validateRequired = (obj: any, fields: string[]): string[] => {
  const missing: string[] = [];
  
  for (const field of fields) {
    if (!obj || obj[field] === undefined || obj[field] === null || obj[field] === '') {
      missing.push(field);
    }
  }
  
  return missing;
};

export const generateId = (prefix: string): string => {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2);
  return `${prefix}_${timestamp}_${random}`;
};

export const generateUserId = (): string => generateId('user');
export const generateAssessmentId = (): string => generateId('assessment');
export const generateReportId = (): string => generateId('report');

export const withCors = (handler: (event: LambdaEvent, context: any) => Promise<LambdaResponse>) => {
  return async (event: LambdaEvent, context: any): Promise<LambdaResponse> => {
    // Handle preflight requests
    if (event.httpMethod === 'OPTIONS') {
      return {
        statusCode: 200,
        headers: corsHeaders,
        body: '',
      };
    }

    console.log('Request:', {
      requestId: context.awsRequestId,
      method: event.httpMethod,
      path: event.path,
      pathParameters: event.pathParameters,
      queryStringParameters: event.queryStringParameters,
    });
    
    try {
      const response = await handler(event, context);
      console.log('Response:', {
        requestId: context.awsRequestId,
        statusCode: response.statusCode,
      });
      return response;
    } catch (error) {
      console.error('Unhandled error:', error);
      const errorResponse = createErrorResponse(500, 'Internal server error');
      return errorResponse;
    }
  };
};
