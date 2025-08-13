import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { DiagConsoleLogger, DiagLogLevel, diag } from '@opentelemetry/api';

// Enable OpenTelemetry debugging in development
if (process.env.NODE_ENV === 'development') {
  diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.INFO);
}

// Configure trace exporter
const traceExporter = new OTLPTraceExporter({
  url: process.env.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT || 'http://localhost:4318/v1/traces',
  headers: process.env.OTEL_EXPORTER_OTLP_HEADERS ? JSON.parse(process.env.OTEL_EXPORTER_OTLP_HEADERS) : {},
});

// Configure metric exporter
const metricExporter = new OTLPMetricExporter({
  url: process.env.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT || 'http://localhost:4318/v1/metrics',
  headers: process.env.OTEL_EXPORTER_OTLP_HEADERS ? JSON.parse(process.env.OTEL_EXPORTER_OTLP_HEADERS) : {},
});

// Initialize the SDK
export const otelSDK = new NodeSDK({
  serviceName: 'neuroquest-api',
  spanProcessor: new BatchSpanProcessor(traceExporter),
  metricReader: new PeriodicExportingMetricReader({
    exporter: metricExporter,
    exportIntervalMillis: 10000, // Export metrics every 10 seconds
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-fs': {
        enabled: false, // Disable fs instrumentation to reduce noise
      },
      '@opentelemetry/instrumentation-http': {
        requestHook: (span, request) => {
          // Add custom attributes to HTTP spans
          if ('headers' in request) {
            span.setAttribute('http.request.body.size', (request as any).headers['content-length'] || 0);
          }
        },
      },
    }),
  ],
});

// Graceful shutdown
process.on('SIGTERM', () => {
  otelSDK
    .shutdown()
    .then(() => console.log('OpenTelemetry terminated successfully'))
    .catch((error) => console.error('Error terminating OpenTelemetry', error))
    .finally(() => process.exit(0));
});

// Custom metrics
import { metrics } from '@opentelemetry/api';

const meter = metrics.getMeter('neuroquest-metrics', '1.0.0');

// Request counter
export const requestCounter = meter.createCounter('http_requests_total', {
  description: 'Total number of HTTP requests',
});

// Response time histogram
export const responseTimeHistogram = meter.createHistogram('http_request_duration_ms', {
  description: 'HTTP request duration in milliseconds',
});

// Active users gauge
export const activeUsersGauge = meter.createUpDownCounter('active_users', {
  description: 'Number of active users',
});

// Database query duration
export const dbQueryDuration = meter.createHistogram('db_query_duration_ms', {
  description: 'Database query duration in milliseconds',
});

// Custom business metrics
export const quizCompletionCounter = meter.createCounter('quiz_completions_total', {
  description: 'Total number of quiz completions',
});

export const learningProgressGauge = meter.createObservableGauge('learning_progress_percentage', {
  description: 'Average learning progress percentage',
});

// Helper function to record API metrics
export function recordApiMetrics(
  method: string,
  path: string,
  statusCode: number,
  duration: number
) {
  requestCounter.add(1, {
    method,
    path,
    status_code: statusCode.toString(),
  });
  
  responseTimeHistogram.record(duration, {
    method,
    path,
    status_code: statusCode.toString(),
  });
}

// Helper function to record database metrics
export function recordDbMetrics(
  operation: string,
  table: string,
  duration: number,
  success: boolean
) {
  dbQueryDuration.record(duration, {
    operation,
    table,
    success: success.toString(),
  });
}