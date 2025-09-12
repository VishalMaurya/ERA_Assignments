import { LambdaEvent, LambdaResponse, User } from '../../shared/types';
import { withCors, createSuccessResponse, createErrorResponse, parseEventBody, validateRequired, generateUserId } from '../../shared/utils';

// Simple in-memory storage for demo (replace with DynamoDB in production)
const users: Map<string, User> = new Map();

// Auth Lambda Handler
export const handler = withCors(async (event: LambdaEvent): Promise<LambdaResponse> => {
  const { httpMethod, path } = event;
  
  try {
    if (httpMethod === 'POST' && path.includes('/auth/register')) {
      return await registerUser(event);
    }
    
    if (httpMethod === 'POST' && path.includes('/auth/login')) {
      return await loginUser(event);
    }
    
    if (httpMethod === 'GET' && path.includes('/auth/user')) {
      return await getUser(event);
    }
    
    if (httpMethod === 'PUT' && path.includes('/auth/user')) {
      return await updateUser(event);
    }
    
    return createErrorResponse(404, 'Route not found');
    
  } catch (error) {
    console.error('Auth handler error:', error);
    return createErrorResponse(500, 'Internal server error');
  }
});

// Register new user
async function registerUser(event: LambdaEvent): Promise<LambdaResponse> {
  const body = parseEventBody(event);
  if (!body) {
    return createErrorResponse(400, 'Invalid request body');
  }

  const { email, preferences } = body;
  
  const user: User = {
    id: generateUserId(),
    email: email || undefined,
    createdAt: new Date().toISOString(),
    preferences: {
      theme: preferences?.theme || 'light',
      notifications: preferences?.notifications ?? true,
      dataRetention: preferences?.dataRetention || 365
    },
    stats: {
      totalAssessments: 0,
      completedAssessments: 0,
      totalTimeSpent: 0
    }
  };

  users.set(user.id, user);
  return createSuccessResponse(user, 'User registered successfully');
}

// Login user (simplified - just return user data)
async function loginUser(event: LambdaEvent): Promise<LambdaResponse> {
  const body = parseEventBody(event);
  if (!body) {
    return createErrorResponse(400, 'Invalid request body');
  }

  const missing = validateRequired(body, ['userId']);
  if (missing.length > 0) {
    return createErrorResponse(400, `Missing required fields: ${missing.join(', ')}`);
  }

  const { userId } = body;

  const user = users.get(userId);
  if (!user) {
    return createErrorResponse(404, 'User not found');
  }

  return createSuccessResponse(user, 'Login successful');
}

// Get user profile
async function getUser(event: LambdaEvent): Promise<LambdaResponse> {
  const userId = event.queryStringParameters?.userId;

  if (!userId) {
    return createErrorResponse(400, 'User ID is required');
  }

  const user = users.get(userId);
  if (!user) {
    return createErrorResponse(404, 'User not found');
  }

  return createSuccessResponse(user);
}

// Update user profile
async function updateUser(event: LambdaEvent): Promise<LambdaResponse> {
  const body = parseEventBody(event);
  if (!body) {
    return createErrorResponse(400, 'Invalid request body');
  }

  const missing = validateRequired(body, ['userId']);
  if (missing.length > 0) {
    return createErrorResponse(400, `Missing required fields: ${missing.join(', ')}`);
  }

  const { userId, preferences, stats } = body;

  const existingUser = users.get(userId);
  if (!existingUser) {
    return createErrorResponse(404, 'User not found');
  }

  // Update user
  const updatedUser: User = {
    ...existingUser,
    ...(preferences && {
      preferences: {
        ...existingUser.preferences,
        ...preferences
      }
    }),
    ...(stats && {
      stats: {
        ...existingUser.stats,
        ...stats
      }
    })
  };

  users.set(userId, updatedUser);
  return createSuccessResponse(updatedUser, 'User updated successfully');
}
