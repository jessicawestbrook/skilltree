import * as Sentry from '@sentry/nextjs';

const SENTRY_DSN = process.env.NEXT_PUBLIC_SENTRY_DSN;
const ENVIRONMENT = process.env.NEXT_PUBLIC_SENTRY_ENVIRONMENT || 'development';

Sentry.init({
  dsn: SENTRY_DSN,
  
  // Environment configuration
  environment: ENVIRONMENT,
  enabled: process.env.NODE_ENV === 'production' || process.env.SENTRY_ENABLED === 'true',
  
  // Performance Monitoring
  tracesSampleRate: ENVIRONMENT === 'production' ? 0.1 : 1.0,
  
  // Session Replay
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  
  // Release tracking
  release: process.env.NEXT_PUBLIC_SENTRY_RELEASE,
  
  // Integrations
  integrations: [
    Sentry.replayIntegration({
      maskAllText: false,
      blockAllMedia: false,
      maskAllInputs: true,
    }),
    Sentry.browserTracingIntegration(),
  ],
  
  // Error filtering
  beforeSend(event, hint) {
    // Filter out non-error events in development
    if (ENVIRONMENT === 'development' && event.level !== 'error') {
      return null;
    }
    
    // Filter out specific errors
    const error = hint.originalException;
    
    // Ignore network errors that are expected
    if (error && error instanceof Error) {
      if (error.message?.includes('Network request failed')) {
        return null;
      }
      
      // Ignore ResizeObserver errors (common and usually harmless)
      if (error.message?.includes('ResizeObserver loop limit exceeded')) {
        return null;
      }
      
      // Ignore browser extension errors
      if (error.message?.includes('extension://')) {
        return null;
      }
    }
    
    // Add user context if available
    const user = getCurrentUser();
    if (user) {
      event.user = {
        id: user.id,
        email: user.email,
        username: user.username,
      };
    }
    
    return event;
  },
  
  // Breadcrumb filtering
  beforeBreadcrumb(breadcrumb) {
    // Filter out noisy breadcrumbs
    if (breadcrumb.category === 'console' && breadcrumb.level === 'debug') {
      return null;
    }
    
    // Don't log sensitive data in breadcrumbs
    if (breadcrumb.category === 'fetch' || breadcrumb.category === 'xhr') {
      if (breadcrumb.data?.url?.includes('/api/auth')) {
        // Redact auth endpoints data
        if (breadcrumb.data) {
          delete breadcrumb.data.request;
          delete breadcrumb.data.response;
        }
      }
    }
    
    return breadcrumb;
  },
  
  // Additional options
  ignoreErrors: [
    // Browser errors
    'ResizeObserver loop limit exceeded',
    'ResizeObserver loop completed with undelivered notifications',
    'Non-Error promise rejection captured',
    
    // Network errors
    'NetworkError',
    'Network request failed',
    
    // User-caused errors
    'User cancelled',
    'User denied',
    
    // Extension errors
    /extension\:\/\//i,
    /^chrome\:\/\//i,
    /^moz\-extension\:\/\//i,
  ],
  
  denyUrls: [
    // Chrome extensions
    /extensions\//i,
    /^chrome:\/\//i,
    /^chrome-extension:\/\//i,
    /^moz-extension:\/\//i,
    
    // Other browser internals
    /^resource:\/\//i,
    /^webkit-internal:\/\//i,
  ],
});

// Helper function to get current user (implement based on your auth system)
function getCurrentUser() {
  // This should be implemented to return the current user from your auth context
  // For now, returning null as a placeholder
  if (typeof window !== 'undefined') {
    try {
      // Try to get user from localStorage or session
      const authData = localStorage.getItem('auth-user');
      if (authData) {
        return JSON.parse(authData);
      }
    } catch (error) {
      console.error('Error getting current user for Sentry:', error);
    }
  }
  return null;
}