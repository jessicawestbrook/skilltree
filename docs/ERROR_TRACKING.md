# Error Tracking & Monitoring Guide

This document explains the error tracking and performance monitoring system implemented in NeuroQuest using Sentry.

## Overview

The application uses **Sentry** for comprehensive error tracking, performance monitoring, and user feedback collection. The system is designed to:

- Automatically capture JavaScript errors and exceptions
- Monitor API performance and failures
- Track Core Web Vitals and performance metrics
- Provide user feedback collection when errors occur
- Filter out noise and focus on actionable errors

## Configuration

### Environment Variables

Add these environment variables to your `.env.local` file:

```bash
# Sentry Configuration
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn_here
NEXT_PUBLIC_SENTRY_ENVIRONMENT=development|staging|production
NEXT_PUBLIC_SENTRY_RELEASE=1.0.0

# For source map uploading (production only)
SENTRY_ORG=your-sentry-organization
SENTRY_PROJECT=neuroquest
SENTRY_AUTH_TOKEN=your_sentry_auth_token

# Optional: Enable Sentry in development (for testing)
SENTRY_ENABLED=false
```

### Turbopack Compatibility

The configuration is optimized for Turbopack development:

- **Development**: Sentry is disabled by default to avoid conflicts with Turbopack
- **Production**: Full Sentry integration with webpack plugin for source maps
- **Testing**: Set `SENTRY_ENABLED=true` to enable Sentry in development mode

### Sentry Project Setup

1. **Create a Sentry Account**: Sign up at [sentry.io](https://sentry.io)
2. **Create a Project**: Choose "Next.js" as the platform
3. **Get Your DSN**: Copy the DSN from your project settings
4. **Generate Auth Token**: Create an auth token for source map uploads

## Components

### 1. Configuration Files

- **`sentry.client.config.ts`**: Client-side Sentry configuration
- **`sentry.server.config.ts`**: Server-side Sentry configuration  
- **`sentry.edge.config.ts`**: Edge runtime configuration
- **`next.config.mjs`**: Next.js configuration with Sentry webpack plugin

### 2. Error Boundary

The `ErrorBoundary` component wraps the entire application and catches React errors:

```tsx
import ErrorBoundary from '../components/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <YourApp />
    </ErrorBoundary>
  );
}
```

Features:
- Catches and reports React component errors
- Shows user-friendly error messages
- Provides retry and navigation options
- Collects user feedback when errors occur
- Shows detailed error information in development

### 3. Error Logger Utility

The `ErrorLogger` class provides structured error logging:

```typescript
import { ErrorLogger } from '@/utils/errorLogger';

// Basic error logging
ErrorLogger.logError(new Error('Something went wrong'), {
  component: 'UserProfile',
  action: 'updateProfile',
  userId: user.id,
});

// API error logging
ErrorLogger.logApiError(
  error,
  '/api/users/profile',
  'PUT',
  500,
  requestData,
  responseData
);

// Authentication errors
ErrorLogger.logAuthError(error, 'login', user.email);

// Database errors
ErrorLogger.logDatabaseError(error, query, params);
```

### 4. Performance Monitoring

The `PerformanceMonitor` class tracks application performance:

```typescript
import { PerformanceMonitor } from '@/utils/performance';

// Manual measurement
PerformanceMonitor.start('data-fetch');
// ... perform operation
PerformanceMonitor.end('data-fetch');

// Automatic measurement
const result = await PerformanceMonitor.measure(
  'api-call',
  () => fetch('/api/data'),
  { endpoint: '/api/data' }
);

// Decorator usage
class ApiService {
  @measurePerformance('fetch-users')
  async fetchUsers() {
    // ... implementation
  }
}
```

## Error Filtering

The system automatically filters out:

- **Browser Extension Errors**: Errors from browser extensions
- **Network Errors**: Expected network failures
- **Development Noise**: Console logs and non-critical warnings
- **User-Caused Errors**: User cancellations and denials
- **Sensitive Data**: Authentication and payment information

## Security & Privacy

### Data Sanitization

Sensitive information is automatically redacted:
- Passwords and tokens
- Authorization headers
- Personal identifiable information
- Database query parameters

### User Context

When errors occur, the system safely captures:
- User ID and email (if authenticated)
- Component and action context
- Browser and device information
- Application state (sanitized)

## Monitoring Dashboards

### Sentry Dashboard Features

1. **Error Tracking**
   - Real-time error alerts
   - Error grouping and frequency
   - Stack traces with source maps
   - User impact analysis

2. **Performance Monitoring**
   - Transaction performance
   - Database query performance
   - API endpoint monitoring
   - Core Web Vitals tracking

3. **Release Tracking**
   - Deploy-based error attribution
   - Regression detection
   - Performance impact of releases

## Usage Examples

### In React Components

```tsx
import { ErrorLogger } from '@/utils/errorLogger';
import { PerformanceMonitor } from '@/utils/performance';

function UserProfile() {
  useEffect(() => {
    PerformanceMonitor.start('profile-load');
    
    loadUserProfile()
      .then(() => {
        PerformanceMonitor.end('profile-load');
      })
      .catch((error) => {
        ErrorLogger.logError(error, {
          component: 'UserProfile',
          action: 'loadProfile',
        });
      });
  }, []);

  return <div>...</div>;
}
```

### In API Routes

```typescript
// pages/api/users/[id].ts
import { ErrorLogger } from '@/utils/errorLogger';

export default async function handler(req, res) {
  try {
    const user = await getUserById(req.query.id);
    res.json(user);
  } catch (error) {
    ErrorLogger.logApiError(
      error,
      req.url,
      req.method,
      500,
      req.body
    );
    res.status(500).json({ error: 'Internal server error' });
  }
}
```

### Authentication Context

```typescript
// In AuthContext
import { ErrorLogger } from '@/utils/errorLogger';

const login = async (credentials) => {
  try {
    const result = await supabase.auth.signInWithPassword(credentials);
    
    // Set user context for future errors
    if (result.user) {
      ErrorLogger.setUserContext({
        id: result.user.id,
        email: result.user.email,
      });
    }
    
    return result;
  } catch (error) {
    ErrorLogger.logAuthError(error, 'login', credentials.email);
    throw error;
  }
};

const logout = async () => {
  // Clear user context
  ErrorLogger.clearUserContext();
  await supabase.auth.signOut();
};
```

## Alerts & Notifications

### Setting Up Alerts

1. **Error Rate Alerts**: Notify when error rate exceeds threshold
2. **Performance Alerts**: Alert on slow response times
3. **New Error Alerts**: Immediate notification of new error types
4. **Release Health**: Monitor deploy success/failure

### Integration Channels

- Email notifications
- Slack integration
- Discord webhooks
- Custom webhook endpoints

## Best Practices

### 1. Error Context

Always provide context when logging errors:

```typescript
// Good
ErrorLogger.logError(error, {
  component: 'QuizComponent',
  action: 'submitAnswer',
  quizId: quiz.id,
  questionId: question.id,
  userId: user.id,
});

// Avoid
console.error(error);
```

### 2. Performance Monitoring

Monitor critical user journeys:

```typescript
// Login flow
PerformanceMonitor.start('user-login-flow');
// ... login steps
PerformanceMonitor.end('user-login-flow');

// Quiz completion
PerformanceMonitor.measure('quiz-submission', async () => {
  return await submitQuizAnswers(answers);
});
```

### 3. User Feedback

Encourage users to provide feedback on errors:

```typescript
// In error boundary or error handler
if (eventId) {
  Sentry.showReportDialog({
    eventId,
    user: getCurrentUser(),
  });
}
```

### 4. Error Boundaries

Use multiple error boundaries for better isolation:

```tsx
// App level
<ErrorBoundary>
  <App />
</ErrorBoundary>

// Feature level
<ErrorBoundary fallback={<QuizErrorFallback />}>
  <QuizComponent />
</ErrorBoundary>
```

## Troubleshooting

### Common Issues

1. **Source Maps Not Uploading**
   - Check `SENTRY_AUTH_TOKEN` environment variable
   - Verify org/project names in `sentry.properties`
   - Ensure build process includes source map generation

2. **No Errors Being Captured**
   - Verify DSN configuration
   - Check network connectivity to Sentry
   - Ensure Sentry is enabled in production

3. **Too Many Errors**
   - Review error filtering configuration
   - Adjust sample rates
   - Add more specific error filtering

4. **Performance Data Missing**
   - Check `tracesSampleRate` configuration
   - Verify performance monitoring is enabled
   - Ensure transactions are being created

### Debug Mode

Enable debug mode in development:

```typescript
// In sentry config
Sentry.init({
  debug: process.env.NODE_ENV === 'development',
  // ... other config
});
```

## Maintenance

### Regular Tasks

1. **Review Error Trends**: Weekly review of error patterns
2. **Update Error Filters**: Adjust filters based on new noise
3. **Performance Baseline**: Monitor performance regression
4. **Release Health**: Track deploy success rates

### Cleanup

- Archive resolved errors after 30 days
- Clean up test/development errors
- Review and update alert thresholds
- Optimize performance monitoring overhead

## Security Considerations

1. **Data Sensitivity**: Never log passwords, tokens, or PII
2. **Rate Limiting**: Implement client-side rate limiting for error reports
3. **Access Control**: Restrict Sentry project access
4. **Data Retention**: Configure appropriate data retention policies

---

For more information, see the [Sentry Next.js Documentation](https://docs.sentry.io/platforms/javascript/guides/nextjs/).