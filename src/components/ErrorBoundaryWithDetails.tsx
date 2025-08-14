'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Copy, ChevronDown, ChevronUp } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
  isDetailsExpanded: boolean;
}

export class ErrorBoundaryWithDetails extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null,
    isDetailsExpanded: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
      isDetailsExpanded: false,
    };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    this.setState({
      error,
      errorInfo,
    });

    // Special handling for JSON parsing errors
    if (error.message.includes('Unexpected token') && error.message.includes('<!DOCTYPE')) {
      console.error('🚨 JSON Parsing Error Detected!');
      console.error('This usually means an API route is returning HTML instead of JSON');
      console.error('Common causes:');
      console.error('1. Development server not running properly');
      console.error('2. API route throwing an unhandled error');
      console.error('3. Authentication redirect to login page');
      console.error('4. Next.js error page being returned');
    }
  }

  private handleReload = () => {
    window.location.reload();
  };

  private handleCopyError = () => {
    const errorText = this.getErrorText();
    navigator.clipboard.writeText(errorText).then(() => {
      alert('Error details copied to clipboard');
    });
  };

  private getErrorText = () => {
    const { error, errorInfo } = this.state;
    return `
Error: ${error?.message || 'Unknown error'}
Stack: ${error?.stack || 'No stack trace'}
Component Stack: ${errorInfo?.componentStack || 'No component stack'}
Timestamp: ${new Date().toISOString()}
User Agent: ${navigator.userAgent}
URL: ${window.location.href}
    `.trim();
  };

  private toggleDetails = () => {
    this.setState(prev => ({ isDetailsExpanded: !prev.isDetailsExpanded }));
  };

  public render() {
    if (this.state.hasError) {
      const { error } = this.state;
      const isJsonError = error?.message.includes('Unexpected token') && error?.message.includes('<!DOCTYPE');

      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-lg border border-red-200 max-w-2xl w-full p-6">
            {/* Header */}
            <div className="flex items-center space-x-3 mb-4">
              <div className="flex-shrink-0">
                <AlertTriangle className="h-8 w-8 text-red-500" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">
                  {isJsonError ? 'API Response Error' : 'Something went wrong'}
                </h1>
                <p className="text-sm text-gray-600">
                  {isJsonError 
                    ? 'The application received an unexpected response from the server'
                    : 'An unexpected error occurred while loading this page'
                  }
                </p>
              </div>
            </div>

            {/* Error Message */}
            <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
              <p className="text-sm text-red-800 font-mono">
                {error?.message || 'Unknown error occurred'}
              </p>
            </div>

            {/* JSON Error Specific Help */}
            {isJsonError && (
              <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-4">
                <h3 className="text-sm font-medium text-blue-800 mb-2">
                  Troubleshooting Steps:
                </h3>
                <ul className="text-sm text-blue-700 space-y-1 list-disc list-inside">
                  <li>Check if the development server is running (npm run dev)</li>
                  <li>Verify API routes are not throwing unhandled errors</li>
                  <li>Check browser network tab for failed requests</li>
                  <li>Look for authentication redirects or CORS issues</li>
                  <li>Ensure all environment variables are properly set</li>
                </ul>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex flex-wrap gap-2 mb-4">
              <button
                onClick={this.handleReload}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                <RefreshCw className="h-4 w-4" />
                <span>Reload Page</span>
              </button>
              
              <button
                onClick={this.handleCopyError}
                className="flex items-center space-x-2 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
              >
                <Copy className="h-4 w-4" />
                <span>Copy Error</span>
              </button>

              <button
                onClick={this.toggleDetails}
                className="flex items-center space-x-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
              >
                {this.state.isDetailsExpanded ? (
                  <ChevronUp className="h-4 w-4" />
                ) : (
                  <ChevronDown className="h-4 w-4" />
                )}
                <span>
                  {this.state.isDetailsExpanded ? 'Hide' : 'Show'} Details
                </span>
              </button>
            </div>

            {/* Error Details */}
            {this.state.isDetailsExpanded && (
              <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
                <h3 className="text-sm font-medium text-gray-900 mb-2">Error Details:</h3>
                <pre className="text-xs text-gray-600 font-mono whitespace-pre-wrap break-words">
                  {this.getErrorText()}
                </pre>
              </div>
            )}

            {/* Footer */}
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-xs text-gray-500 text-center">
                If this error persists, please check the browser console for more details.
              </p>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}