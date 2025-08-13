import { NextRequest, NextResponse } from 'next/server';
import { ErrorLogger } from '@/utils/errorLogger';
import { PerformanceMonitor } from '@/utils/performance';

/**
 * Middleware to automatically track API errors and performance
 */
export function withErrorTracking(
  handler: (req: NextRequest) => Promise<NextResponse> | NextResponse
) {
  return async (req: NextRequest): Promise<NextResponse> => {
    const startTime = Date.now();
    const url = req.url;
    const method = req.method;
    
    // Start performance monitoring
    const operationName = `api_${method.toLowerCase()}_${url.split('/').pop()}`;
    PerformanceMonitor.start(operationName, {
      url,
      method,
      userAgent: req.headers.get('user-agent'),
    });

    try {
      // Execute the handler
      const response = await handler(req);
      const endTime = Date.now();
      
      // Log performance
      PerformanceMonitor.monitorApiRequest(
        url,
        method,
        startTime,
        endTime,
        response.status < 400
      );
      
      // End performance monitoring
      PerformanceMonitor.end(operationName);
      
      return response;
    } catch (error) {
      const endTime = Date.now();
      
      // Log the API error
      ErrorLogger.logApiError(
        error as Error,
        url,
        method,
        500,
        await getRequestBody(req),
        null
      );
      
      // Log performance for failed request
      PerformanceMonitor.monitorApiRequest(
        url,
        method,
        startTime,
        endTime,
        false
      );
      
      // End performance monitoring
      PerformanceMonitor.end(operationName);
      
      // Return error response
      return NextResponse.json(
        { error: 'Internal server error' },
        { status: 500 }
      );
    }
  };
}

/**
 * Extract request body safely
 */
async function getRequestBody(req: NextRequest): Promise<any> {
  try {
    const contentType = req.headers.get('content-type');
    
    if (contentType?.includes('application/json')) {
      return await req.json();
    }
    
    if (contentType?.includes('application/x-www-form-urlencoded')) {
      const formData = await req.formData();
      return Object.fromEntries(formData.entries());
    }
    
    return null;
  } catch (error) {
    return null;
  }
}

/**
 * Higher-order function for API route error handling
 */
export function apiErrorHandler<T extends any[]>(
  handler: (...args: T) => Promise<NextResponse> | NextResponse,
  context?: {
    component?: string;
    action?: string;
  }
) {
  return async (...args: T): Promise<NextResponse> => {
    try {
      return await handler(...args);
    } catch (error) {
      // Extract request information if available
      const req = args[0] as NextRequest;
      const url = req?.url || 'unknown';
      const method = req?.method || 'unknown';
      
      ErrorLogger.logApiError(
        error as Error,
        url,
        method,
        500,
        null,
        null
      );
      
      // Log with additional context if provided
      if (context) {
        ErrorLogger.logError(error as Error, {
          component: context.component,
          action: context.action,
          metadata: { url, method },
        });
      }
      
      return NextResponse.json(
        { error: 'Internal server error' },
        { status: 500 }
      );
    }
  };
}

/**
 * Middleware to set user context from authentication headers
 */
export function withUserContext(
  handler: (req: NextRequest) => Promise<NextResponse> | NextResponse
) {
  return async (req: NextRequest): Promise<NextResponse> => {
    // Extract user information from authorization header or session
    const authHeader = req.headers.get('authorization');
    
    if (authHeader) {
      try {
        // This would typically involve decoding a JWT or validating a session
        // For now, we'll skip setting user context in middleware
        // User context should be set in the auth system itself
      } catch (error) {
        // Ignore errors in user context extraction
      }
    }
    
    return handler(req);
  };
}

/**
 * Combine multiple middleware functions
 */
export function combineMiddleware(
  ...middlewares: Array<
    (handler: (req: NextRequest) => Promise<NextResponse> | NextResponse) => 
    (req: NextRequest) => Promise<NextResponse> | NextResponse
  >
) {
  return (
    handler: (req: NextRequest) => Promise<NextResponse> | NextResponse
  ) => {
    return middlewares.reduceRight(
      (acc, middleware) => middleware(acc),
      handler
    );
  };
}

// Example usage:
// export const middleware = combineMiddleware(
//   withErrorTracking,
//   withUserContext
// );

export default withErrorTracking;