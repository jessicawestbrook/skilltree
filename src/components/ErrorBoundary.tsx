'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';
import * as Sentry from '@sentry/nextjs';
import { AlertTriangle, RefreshCw, Home, Bug } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  showDetails?: boolean;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
  eventId: string | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      eventId: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('ErrorBoundary caught an error:', error, errorInfo);
    }

    // Send error to Sentry
    const eventId = Sentry.captureException(error, {
      contexts: {
        react: {
          componentStack: errorInfo.componentStack,
        },
      },
      tags: {
        component: 'ErrorBoundary',
      },
    });

    // Update state with error details
    this.setState({
      error,
      errorInfo,
      eventId,
    });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
      eventId: null,
    });
  };

  handleReload = () => {
    window.location.reload();
  };

  handleGoHome = () => {
    window.location.href = '/';
  };

  handleReportFeedback = () => {
    if (this.state.eventId) {
      const user = this.getCurrentUser();
      Sentry.showReportDialog({
        eventId: this.state.eventId,
        user: user ? {
          email: user.email,
          name: user.username,
        } : undefined,
      });
    }
  };

  getCurrentUser() {
    // Get user from localStorage or session
    try {
      const authData = localStorage.getItem('auth-user');
      if (authData) {
        return JSON.parse(authData);
      }
    } catch (error) {
      console.error('Error getting current user:', error);
    }
    return null;
  }

  render() {
    if (this.state.hasError) {
      // Use custom fallback if provided
      if (this.props.fallback) {
        return <>{this.props.fallback}</>;
      }

      // Default error UI
      return (
        <div style={styles.container}>
          <div style={styles.content}>
            <div style={styles.iconContainer}>
              <AlertTriangle size={64} color="#ff4444" />
            </div>
            
            <h1 style={styles.title}>Oops! Something went wrong</h1>
            
            <p style={styles.message}>
              We&apos;re sorry, but something unexpected happened. The error has been logged and we&apos;ll look into it.
            </p>

            {/* Error details in development */}
            {process.env.NODE_ENV === 'development' && this.props.showDetails !== false && (
              <div style={styles.errorDetails}>
                <h3 style={styles.errorTitle}>Error Details (Development Only)</h3>
                <pre style={styles.errorStack}>
                  {this.state.error?.toString()}
                  {'\n\n'}
                  {this.state.errorInfo?.componentStack}
                </pre>
              </div>
            )}

            {/* Action buttons */}
            <div style={styles.buttonContainer}>
              <button onClick={this.handleReset} style={styles.button}>
                <RefreshCw size={20} />
                Try Again
              </button>
              
              <button onClick={this.handleReload} style={styles.buttonSecondary}>
                <RefreshCw size={20} />
                Reload Page
              </button>
              
              <button onClick={this.handleGoHome} style={styles.buttonSecondary}>
                <Home size={20} />
                Go Home
              </button>

              {this.state.eventId && (
                <button onClick={this.handleReportFeedback} style={styles.buttonReport}>
                  <Bug size={20} />
                  Report Issue
                </button>
              )}
            </div>

            {/* Error ID for support */}
            {this.state.eventId && (
              <div style={styles.errorId}>
                <p>Error ID: <code>{this.state.eventId}</code></p>
                <p style={styles.supportText}>
                  Please include this ID if you contact support
                </p>
              </div>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f5f5f5',
    padding: '20px',
  },
  content: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '40px',
    maxWidth: '600px',
    width: '100%',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    textAlign: 'center' as const,
  },
  iconContainer: {
    marginBottom: '24px',
  },
  title: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#2a2a2a',
    marginBottom: '16px',
  },
  message: {
    fontSize: '16px',
    color: '#666',
    lineHeight: '1.6',
    marginBottom: '32px',
  },
  errorDetails: {
    backgroundColor: '#f8f9fa',
    border: '1px solid #dee2e6',
    borderRadius: '8px',
    padding: '20px',
    marginBottom: '24px',
    textAlign: 'left' as const,
  },
  errorTitle: {
    fontSize: '16px',
    fontWeight: 'bold',
    color: '#dc3545',
    marginBottom: '12px',
  },
  errorStack: {
    fontSize: '12px',
    color: '#495057',
    overflow: 'auto',
    maxHeight: '200px',
    whiteSpace: 'pre-wrap' as const,
    wordBreak: 'break-word' as const,
    fontFamily: 'monospace',
  },
  buttonContainer: {
    display: 'flex',
    gap: '12px',
    justifyContent: 'center',
    flexWrap: 'wrap' as const,
  },
  button: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: '12px 24px',
    background: 'linear-gradient(135deg, #059669, #0ea5e9)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'transform 0.2s ease',
  },
  buttonSecondary: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: '12px 24px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'transform 0.2s ease',
  },
  buttonReport: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: '12px 24px',
    backgroundColor: '#ffc107',
    color: '#212529',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'transform 0.2s ease',
  },
  errorId: {
    marginTop: '32px',
    padding: '16px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    fontSize: '14px',
  },
  supportText: {
    color: '#6c757d',
    marginTop: '8px',
    fontSize: '12px',
  },
};

export default ErrorBoundary;