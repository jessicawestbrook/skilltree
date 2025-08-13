import * as Sentry from '@sentry/nextjs';

export interface ErrorContext {
  component?: string;
  action?: string;
  userId?: string;
  userEmail?: string;
  metadata?: Record<string, any>;
  level?: 'error' | 'warning' | 'info' | 'debug';
}

export interface PerformanceContext {
  operation: string;
  duration?: number;
  metadata?: Record<string, any>;
}

/**
 * Enhanced error logging utility with Sentry integration
 */
export class ErrorLogger {
  /**
   * Log an error with context
   */
  static logError(error: Error | string, context?: ErrorContext): string | undefined {
    const errorObj = typeof error === 'string' ? new Error(error) : error;
    
    // Console log in development
    if (process.env.NODE_ENV === 'development') {
      console.error('ErrorLogger:', errorObj, context);
    }
    
    // Set user context if provided
    if (context?.userId || context?.userEmail) {
      Sentry.setUser({
        id: context.userId,
        email: context.userEmail,
      });
    }
    
    // Set additional context
    if (context) {
      Sentry.setContext('error_context', {
        component: context.component,
        action: context.action,
        metadata: context.metadata,
      });
      
      // Set tags for filtering
      Sentry.setTags({
        component: context.component,
        action: context.action,
      });
    }
    
    // Capture exception and return event ID
    return Sentry.captureException(errorObj, {
      level: context?.level || 'error',
    });
  }
  
  /**
   * Log API errors with request/response context
   */
  static logApiError(
    error: Error | string,
    endpoint: string,
    method: string,
    statusCode?: number,
    requestData?: any,
    responseData?: any
  ): string | undefined {
    const errorObj = typeof error === 'string' ? new Error(error) : error;
    
    if (process.env.NODE_ENV === 'development') {
      console.error('API Error:', {
        error: errorObj,
        endpoint,
        method,
        statusCode,
        requestData,
        responseData,
      });
    }
    
    return Sentry.captureException(errorObj, {
      tags: {
        type: 'api_error',
        endpoint,
        method,
        status_code: statusCode?.toString(),
      },
      contexts: {
        api: {
          endpoint,
          method,
          status_code: statusCode,
          request_data: requestData ? this.sanitizeData(requestData) : undefined,
          response_data: responseData ? this.sanitizeData(responseData) : undefined,
        },
      },
    });
  }
  
  /**
   * Log authentication errors
   */
  static logAuthError(error: Error | string, action: string, userEmail?: string): string | undefined {
    return this.logError(error, {
      component: 'Authentication',
      action,
      userEmail,
      level: 'error',
    });
  }
  
  /**
   * Log database errors
   */
  static logDatabaseError(
    error: Error | string,
    query?: string,
    params?: any
  ): string | undefined {
    const errorObj = typeof error === 'string' ? new Error(error) : error;
    
    return Sentry.captureException(errorObj, {
      tags: {
        type: 'database_error',
      },
      contexts: {
        database: {
          query: query ? this.sanitizeQuery(query) : undefined,
          params: params ? this.sanitizeData(params) : undefined,
        },
      },
    });
  }
  
  /**
   * Log performance issues
   */
  static logPerformanceIssue(context: PerformanceContext): void {
    if (process.env.NODE_ENV === 'development') {
      console.warn('Performance Issue:', context);
    }
    
    Sentry.addBreadcrumb({
      category: 'performance',
      message: `Slow operation: ${context.operation}`,
      level: 'warning',
      data: {
        operation: context.operation,
        duration: context.duration,
        metadata: context.metadata,
      },
    });
    
    // Capture as message if duration is very high
    if (context.duration && context.duration > 5000) {
      Sentry.captureMessage(
        `Performance issue: ${context.operation} took ${context.duration}ms`,
        'warning'
      );
    }
  }
  
  /**
   * Log user actions for debugging
   */
  static logUserAction(action: string, metadata?: Record<string, any>): void {
    if (process.env.NODE_ENV === 'development') {
      console.log('User Action:', action, metadata);
    }
    
    Sentry.addBreadcrumb({
      category: 'user',
      message: action,
      level: 'info',
      data: metadata,
    });
  }
  
  /**
   * Log navigation events
   */
  static logNavigation(from: string, to: string): void {
    Sentry.addBreadcrumb({
      category: 'navigation',
      message: `Navigate from ${from} to ${to}`,
      level: 'info',
      data: { from, to },
    });
  }
  
  /**
   * Set user context for all subsequent errors
   */
  static setUserContext(user: {
    id: string;
    email?: string;
    username?: string;
  }): void {
    Sentry.setUser({
      id: user.id,
      email: user.email,
      username: user.username,
    });
  }
  
  /**
   * Clear user context (e.g., on logout)
   */
  static clearUserContext(): void {
    Sentry.setUser(null);
  }
  
  /**
   * Add custom context for errors
   */
  static setContext(key: string, context: Record<string, any>): void {
    Sentry.setContext(key, context);
  }
  
  /**
   * Start a performance transaction
   */
  static startTransaction(name: string, op?: string): unknown {
    return Sentry.startSpan({
      name,
      op: op || 'navigation',
    }, () => {});
  }
  
  /**
   * Sanitize sensitive data before logging
   */
  private static sanitizeData(data: any): any {
    if (!data) return data;
    
    const sensitiveKeys = [
      'password',
      'token',
      'secret',
      'key',
      'authorization',
      'cookie',
      'session',
    ];
    
    if (typeof data === 'object') {
      const sanitized = { ...data };
      for (const key of Object.keys(sanitized)) {
        if (sensitiveKeys.some(sensitiveKey => 
          key.toLowerCase().includes(sensitiveKey))) {
          sanitized[key] = '[REDACTED]';
        }
      }
      return sanitized;
    }
    
    return data;
  }
  
  /**
   * Sanitize SQL queries
   */
  private static sanitizeQuery(query: string): string {
    // Remove potential sensitive data from queries
    return query.replace(/('[^']*'|"[^"]*")/g, '[REDACTED]');
  }
}

/**
 * Wrapper for async operations with error handling
 */
export async function withErrorHandling<T>(
  operation: () => Promise<T>,
  context?: ErrorContext
): Promise<{ data: T | null; error: Error | null }> {
  try {
    const data = await operation();
    return { data, error: null };
  } catch (error) {
    const errorObj = error instanceof Error ? error : new Error(String(error));
    ErrorLogger.logError(errorObj, context);
    return { data: null, error: errorObj };
  }
}

/**
 * Performance monitoring decorator
 */
export function measurePerformance(
  target: any,
  propertyName: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;
  
  descriptor.value = async function (...args: any[]) {
    const startTime = Date.now();
    
    try {
      const result = await originalMethod.apply(this, args);
      const duration = Date.now() - startTime;
      
      if (duration > 1000) {
        ErrorLogger.logPerformanceIssue({
          operation: `${target.constructor.name}.${propertyName}`,
          duration,
          metadata: { args: args.length },
        });
      }
      
      return result;
    } catch (error) {
      const duration = Date.now() - startTime;
      ErrorLogger.logError(error as Error, {
        component: target.constructor.name,
        action: propertyName,
        metadata: { duration, args: args.length },
      });
      throw error;
    }
  };
  
  return descriptor;
}

// Export default instance
export default ErrorLogger;