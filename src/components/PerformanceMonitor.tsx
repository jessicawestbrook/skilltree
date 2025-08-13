'use client';

import { useEffect } from 'react';
import { AnalyticsService } from '@/services/analyticsService';

// Type definitions for performance APIs
interface LayoutShiftEntry extends PerformanceEntry {
  value: number;
  hadRecentInput: boolean;
}

interface PerformanceEventTiming extends PerformanceEntry {
  processingStart: number;
}

interface NavigatorWithConnection extends Navigator {
  connection?: {
    effectiveType: string;
    downlink: number;
    rtt: number;
    saveData?: boolean;
  };
}

interface PerformanceWithMemory extends Performance {
  memory?: {
    usedJSHeapSize: number;
    totalJSHeapSize: number;
    jsHeapSizeLimit: number;
  };
}

interface PerformanceMetrics {
  pageLoadTime?: number;
  firstContentfulPaint?: number;
  largestContentfulPaint?: number;
  cumulativeLayoutShift?: number;
  firstInputDelay?: number;
  timeToInteractive?: number;
}

export default function PerformanceMonitor() {
  useEffect(() => {
    // Track performance metrics
    const trackPerformance = () => {
      try {
        // Get navigation timing
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        
        if (navigation) {
          const metrics: PerformanceMetrics = {
            pageLoadTime: navigation.loadEventEnd - navigation.loadEventStart,
            timeToInteractive: navigation.domInteractive - navigation.fetchStart,
          };

          // Track Web Vitals if available
          if ('web-vitals' in window || typeof window !== 'undefined') {
            // FCP - First Contentful Paint
            const fcpEntries = performance.getEntriesByName('first-contentful-paint');
            if (fcpEntries.length > 0) {
              metrics.firstContentfulPaint = fcpEntries[0].startTime;
            }

            // LCP - Largest Contentful Paint
            if ('PerformanceObserver' in window) {
              try {
                const lcpObserver = new PerformanceObserver((list) => {
                  const entries = list.getEntries();
                  const lastEntry = entries[entries.length - 1];
                  metrics.largestContentfulPaint = lastEntry.startTime;
                });
                lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

                // CLS - Cumulative Layout Shift
                const clsObserver = new PerformanceObserver((list) => {
                  let clsValue = 0;
                  for (const entry of list.getEntries()) {
                    const layoutShiftEntry = entry as LayoutShiftEntry;
                    if (!layoutShiftEntry.hadRecentInput) {
                      clsValue += layoutShiftEntry.value;
                    }
                  }
                  metrics.cumulativeLayoutShift = clsValue;
                });
                clsObserver.observe({ entryTypes: ['layout-shift'] });

                // FID - First Input Delay
                const fidObserver = new PerformanceObserver((list) => {
                  for (const entry of list.getEntries()) {
                    const fidEntry = entry as PerformanceEventTiming;
                    metrics.firstInputDelay = fidEntry.processingStart - entry.startTime;
                  }
                });
                fidObserver.observe({ entryTypes: ['first-input'] });

                // Clean up observers after 10 seconds
                setTimeout(() => {
                  lcpObserver.disconnect();
                  clsObserver.disconnect();
                  fidObserver.disconnect();
                }, 10000);
              } catch (error) {
                console.warn('Performance Observer not supported:', error);
              }
            }
          }

          // Track the metrics after a delay to ensure all data is collected
          setTimeout(() => {
            AnalyticsService.trackEvent({
              event_type: 'performance_metrics',
              event_data: {
                ...metrics,
                user_agent: navigator.userAgent,
                viewport_width: window.innerWidth,
                viewport_height: window.innerHeight,
                connection_type: (navigator as NavigatorWithConnection).connection?.effectiveType || 'unknown',
                timestamp: new Date().toISOString()
              }
            });
          }, 3000);
        }
      } catch (error) {
        console.warn('Failed to track performance metrics:', error);
      }
    };

    // Track memory usage if available
    const trackMemoryUsage = () => {
      if ('memory' in performance) {
        const memory = (performance as PerformanceWithMemory).memory;
        if (memory) {
          AnalyticsService.trackEvent({
            event_type: 'memory_usage',
            event_data: {
              used_heap: memory.usedJSHeapSize,
              total_heap: memory.totalJSHeapSize,
              heap_limit: memory.jsHeapSizeLimit,
              timestamp: new Date().toISOString()
            }
          });
        }
      }
    };

    // Track network information if available
    const trackNetworkInfo = () => {
      if ('connection' in navigator) {
        const connection = (navigator as NavigatorWithConnection).connection;
        if (connection) {
          AnalyticsService.trackEvent({
            event_type: 'network_info',
            event_data: {
              effective_type: connection.effectiveType,
              downlink: connection.downlink,
              rtt: connection.rtt,
              save_data: connection.saveData || false,
              timestamp: new Date().toISOString()
            }
          });
        }
      }
    };

    // Run initial tracking
    trackPerformance();
    trackNetworkInfo();

    // Track memory usage periodically (every 5 minutes)
    const memoryInterval = setInterval(trackMemoryUsage, 5 * 60 * 1000);

    // Track page visibility changes
    const handleVisibilityChange = () => {
      AnalyticsService.trackEvent({
        event_type: 'page_visibility',
        event_data: {
          visibility_state: document.visibilityState,
          timestamp: new Date().toISOString()
        }
      });
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    // Track page unload
    const handleBeforeUnload = () => {
      const sessionStats = AnalyticsService.getSessionStats();
      AnalyticsService.trackEvent({
        event_type: 'page_unload',
        event_data: {
          session_duration: sessionStats.duration,
          timestamp: new Date().toISOString()
        }
      });
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    // Cleanup
    return () => {
      clearInterval(memoryInterval);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  // Track errors
  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      AnalyticsService.trackEvent({
        event_type: 'javascript_error',
        event_data: {
          message: event.message,
          filename: event.filename,
          line_number: event.lineno,
          column_number: event.colno,
          stack: event.error?.stack,
          timestamp: new Date().toISOString()
        }
      });
    };

    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      AnalyticsService.trackEvent({
        event_type: 'unhandled_promise_rejection',
        event_data: {
          reason: event.reason?.toString(),
          stack: event.reason?.stack,
          timestamp: new Date().toISOString()
        }
      });
    };

    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, []);

  // This component doesn't render anything
  return null;
}