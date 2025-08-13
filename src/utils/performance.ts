import * as Sentry from '@sentry/nextjs';
import { ErrorLogger } from './errorLogger';
import React from 'react';

export interface PerformanceMetrics {
  name: string;
  startTime: number;
  endTime?: number;
  duration?: number;
  metadata?: Record<string, any>;
}

/**
 * Performance monitoring utilities
 */
export class PerformanceMonitor {
  private static measurements = new Map<string, PerformanceMetrics>();

  /**
   * Start measuring performance for an operation
   */
  static start(name: string, metadata?: Record<string, any>): void {
    this.measurements.set(name, {
      name,
      startTime: performance.now(),
      metadata,
    });

    // Start Sentry transaction for important operations
    if (this.isImportantOperation(name)) {
      const transaction = Sentry.startSpan({
        name,
        op: 'custom',
      }, () => {});
      
      // Store transaction for later use
      this.measurements.set(`${name}_transaction`, {
        name: `${name}_transaction`,
        startTime: performance.now(),
        metadata: { transaction },
      });
    }
  }

  /**
   * End measurement and log if performance is poor
   */
  static end(name: string): PerformanceMetrics | null {
    const measurement = this.measurements.get(name);
    if (!measurement) {
      console.warn(`Performance measurement '${name}' not found`);
      return null;
    }

    const endTime = performance.now();
    const duration = endTime - measurement.startTime;

    const completedMeasurement: PerformanceMetrics = {
      ...measurement,
      endTime,
      duration,
    };

    // Log slow operations
    if (this.isSlowOperation(name, duration)) {
      ErrorLogger.logPerformanceIssue({
        operation: name,
        duration,
        metadata: measurement.metadata,
      });
    }

    // End Sentry transaction if exists
    const transactionMeasurement = this.measurements.get(`${name}_transaction`);
    if (transactionMeasurement?.metadata?.transaction) {
      transactionMeasurement.metadata.transaction.finish();
      this.measurements.delete(`${name}_transaction`);
    }

    // Clean up
    this.measurements.delete(name);

    // Log in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`Performance: ${name} took ${duration.toFixed(2)}ms`);
    }

    return completedMeasurement;
  }

  /**
   * Measure a function's execution time
   */
  static async measure<T>(
    name: string,
    fn: () => Promise<T> | T,
    metadata?: Record<string, any>
  ): Promise<T> {
    this.start(name, metadata);
    try {
      const result = await fn();
      this.end(name);
      return result;
    } catch (error) {
      this.end(name);
      throw error;
    }
  }

  /**
   * Measure Web Vitals
   */
  static measureWebVitals(): void {
    if (typeof window === 'undefined') return;

    // Measure First Contentful Paint
    this.observePerformanceEntry('first-contentful-paint', (entry) => {
      this.reportWebVital('FCP', entry.startTime);
    });

    // Measure Largest Contentful Paint
    this.observePerformanceEntry('largest-contentful-paint', (entry) => {
      this.reportWebVital('LCP', entry.startTime);
    });

    // Measure Cumulative Layout Shift
    this.observeCLS();

    // Measure First Input Delay
    this.observeFID();
  }

  /**
   * Monitor Core Web Vitals
   */
  private static observePerformanceEntry(
    entryType: string,
    callback: (entry: PerformanceEntry) => void
  ): void {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach(callback);
      });
      observer.observe({ entryTypes: [entryType] });
    }
  }

  /**
   * Observe Cumulative Layout Shift
   */
  private static observeCLS(): void {
    if ('PerformanceObserver' in window) {
      let clsValue = 0;
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!(entry as any).hadRecentInput) {
            clsValue += (entry as any).value;
          }
        }
        this.reportWebVital('CLS', clsValue);
      });
      observer.observe({ entryTypes: ['layout-shift'] });
    }
  }

  /**
   * Observe First Input Delay
   */
  private static observeFID(): void {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          this.reportWebVital('FID', (entry as any).processingStart - entry.startTime);
        }
      });
      observer.observe({ entryTypes: ['first-input'] });
    }
  }

  /**
   * Report Web Vital metrics to Sentry
   */
  private static reportWebVital(name: string, value: number): void {
    // Send to Sentry
    Sentry.addBreadcrumb({
      category: 'web-vital',
      message: `${name}: ${value}`,
      level: 'info',
      data: { name, value },
    });

    // Log poor scores
    const thresholds = {
      FCP: 1800,
      LCP: 2500,
      FID: 100,
      CLS: 0.1,
    };

    if (value > thresholds[name as keyof typeof thresholds]) {
      Sentry.captureMessage(
        `Poor ${name} score: ${value}ms`,
        'warning'
      );
    }

    if (process.env.NODE_ENV === 'development') {
      console.log(`Web Vital - ${name}: ${value}`);
    }
  }

  /**
   * Monitor API request performance
   */
  static monitorApiRequest(
    url: string,
    method: string,
    startTime: number,
    endTime: number,
    success: boolean
  ): void {
    const duration = endTime - startTime;
    
    Sentry.addBreadcrumb({
      category: 'api',
      message: `${method} ${url}`,
      level: success ? 'info' : 'error',
      data: { url, method, duration, success },
    });

    // Report slow API calls
    if (duration > 3000) {
      ErrorLogger.logPerformanceIssue({
        operation: 'api_request',
        duration,
        metadata: { url, method, success },
      });
    }
  }

  /**
   * Check if operation is important enough for detailed tracking
   */
  private static isImportantOperation(name: string): boolean {
    const importantOperations = [
      'page_load',
      'user_login',
      'user_register',
      'data_fetch',
      'file_upload',
      'quiz_submit',
    ];
    return importantOperations.some(op => name.toLowerCase().includes(op));
  }

  /**
   * Determine if operation is slow based on operation type
   */
  private static isSlowOperation(name: string, duration: number): boolean {
    const thresholds: Record<string, number> = {
      page_load: 3000,
      api_request: 2000,
      user_login: 1500,
      user_register: 2000,
      data_fetch: 1000,
      file_upload: 5000,
      quiz_submit: 1000,
      default: 1000,
    };

    const operationType = Object.keys(thresholds).find(type =>
      name.toLowerCase().includes(type)
    );

    const threshold = thresholds[operationType || 'default'];
    return duration > threshold;
  }

  /**
   * Get current performance metrics
   */
  static getCurrentMetrics(): Record<string, any> {
    if (typeof window === 'undefined') return {};

    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    
    return {
      domContentLoaded: navigation?.domContentLoadedEventEnd - navigation?.domContentLoadedEventStart,
      loadComplete: navigation?.loadEventEnd - navigation?.loadEventStart,
      firstByte: navigation?.responseStart - navigation?.requestStart,
      domInteractive: navigation?.domInteractive - navigation?.fetchStart,
      totalLoadTime: navigation?.loadEventEnd - navigation?.fetchStart,
    };
  }
}

/**
 * Decorator for measuring function performance
 */
export function measurePerformance(name?: string) {
  return function (
    target: any,
    propertyName: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const measurementName = name || `${target.constructor.name}.${propertyName}`;

    descriptor.value = async function (...args: any[]) {
      return PerformanceMonitor.measure(
        measurementName,
        () => originalMethod.apply(this, args),
        { args: args.length }
      );
    };

    return descriptor;
  };
}

/**
 * Hook for measuring component render performance
 */
export function usePerformanceMonitor(componentName: string) {
  React.useEffect(() => {
    if (typeof window !== 'undefined') {
      PerformanceMonitor.start(`render_${componentName}`);
      return () => {
        PerformanceMonitor.end(`render_${componentName}`);
      };
    }
  }, [componentName]);
}

// Initialize Web Vitals monitoring on client
if (typeof window !== 'undefined') {
  PerformanceMonitor.measureWebVitals();
}

export default PerformanceMonitor;