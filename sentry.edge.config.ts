import * as Sentry from '@sentry/nextjs';

const SENTRY_DSN = process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN;
const ENVIRONMENT = process.env.SENTRY_ENVIRONMENT || process.env.NEXT_PUBLIC_SENTRY_ENVIRONMENT || 'development';

Sentry.init({
  dsn: SENTRY_DSN,
  
  // Environment configuration
  environment: ENVIRONMENT,
  enabled: process.env.NODE_ENV === 'production',
  
  // Performance Monitoring for Edge Runtime
  tracesSampleRate: ENVIRONMENT === 'production' ? 0.1 : 1.0,
  
  // Release tracking
  release: process.env.SENTRY_RELEASE || process.env.NEXT_PUBLIC_SENTRY_RELEASE,
  
  // Edge-specific configuration
  beforeSend(event, hint) {
    // Filter out non-error events in development
    if (ENVIRONMENT === 'development' && event.level !== 'error') {
      return null;
    }
    
    // Add edge runtime context
    event.tags = {
      ...event.tags,
      runtime: 'edge',
    };
    
    return event;
  },
});