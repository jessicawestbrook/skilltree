// This file is used to register instrumentation for Sentry
// It runs before any other code in your application

export async function register() {
  // Only run in production or when explicitly enabled
  if (process.env.NODE_ENV === 'production' || process.env.SENTRY_ENABLED === 'true') {
    if (process.env.NEXT_RUNTIME === 'nodejs') {
      // Server-side instrumentation
      await import('../sentry.server.config');
    } else if (process.env.NEXT_RUNTIME === 'edge') {
      // Edge runtime instrumentation
      await import('../sentry.edge.config');
    }
  }
  
  // Initialize OpenTelemetry
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    if (process.env.NODE_ENV === 'production' || process.env.OTEL_ENABLED === 'true') {
      const { otelSDK } = await import('./lib/telemetry');
      otelSDK.start();
      console.log('OpenTelemetry instrumentation started');
    }
  }
}

export async function onRequestError(
  err: unknown,
  request: {
    path: string;
    method: string;
    headers: Record<string, string | string[] | undefined>;
  },
  context: {
    routerKind: 'Pages Router' | 'App Router';
    routePath: string;
    routeType: 'route' | 'page' | 'layout' | 'loading' | 'not-found' | 'error';
    renderSource: 'react-server-components' | 'server-side-rendering' | 'edge-runtime' | 'nodejs-runtime';
  }
) {
  // Dynamically import Sentry to avoid issues during build/static generation
  const { captureRequestError } = await import('@sentry/nextjs');
  
  // Capture the error with additional context
  captureRequestError(err, request, context);
}