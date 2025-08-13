import * as Sentry from '@sentry/nextjs';

const SENTRY_DSN = process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN;
const ENVIRONMENT = process.env.SENTRY_ENVIRONMENT || process.env.NEXT_PUBLIC_SENTRY_ENVIRONMENT || 'development';

Sentry.init({
  dsn: SENTRY_DSN,
  
  // Environment configuration
  environment: ENVIRONMENT,
  enabled: process.env.NODE_ENV === 'production' || process.env.SENTRY_ENABLED === 'true',
  
  // Performance Monitoring
  tracesSampleRate: ENVIRONMENT === 'production' ? 0.1 : 1.0,
  
  // Release tracking
  release: process.env.SENTRY_RELEASE || process.env.NEXT_PUBLIC_SENTRY_RELEASE,
  
  // Server-specific integrations
  integrations: [
    // Basic server integrations
  ],
  
  // Error filtering
  beforeSend(event, hint) {
    // Filter out non-error events in development
    if (ENVIRONMENT === 'development' && event.level !== 'error') {
      return null;
    }
    
    const error = hint.originalException;
    
    // Filter out expected errors
    if (error && error instanceof Error) {
      // Ignore client disconnection errors
      if (error.message?.includes('ECONNRESET') || 
          error.message?.includes('EPIPE') ||
          error.message?.includes('ENOTFOUND')) {
        return null;
      }
      
      // Ignore timeout errors that are expected
      if (error.message?.includes('Timeout') && error.message?.includes('idle')) {
        return null;
      }
    }
    
    // Add additional context for API errors
    if (event.request?.url?.includes('/api/')) {
      event.tags = {
        ...event.tags,
        api_endpoint: true,
      };
      
      // Redact sensitive headers
      if (event.request.headers) {
        const sensitiveHeaders = ['authorization', 'cookie', 'x-api-key'];
        sensitiveHeaders.forEach(header => {
          if (event.request?.headers?.[header]) {
            event.request.headers[header] = '[REDACTED]';
          }
        });
      }
    }
    
    return event;
  },
  
  // Server-specific error filtering
  ignoreErrors: [
    // Connection errors
    'ECONNRESET',
    'EPIPE',
    'ENOTFOUND',
    'ETIMEDOUT',
    
    // HTTP errors that are expected
    'AbortError',
    
    // Database errors that are retryable
    'SequelizeConnectionError',
    'SequelizeTimeoutError',
  ],
  
  // Additional server configuration can be added here
});