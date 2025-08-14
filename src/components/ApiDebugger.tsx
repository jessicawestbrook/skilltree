'use client';

import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, XCircle, Clock, RefreshCw } from 'lucide-react';

interface ApiStatus {
  endpoint: string;
  status: 'checking' | 'success' | 'error';
  message: string;
  responseTime?: number;
}

const API_ENDPOINTS = [
  '/api/health',
  '/api/progress',
  '/api/activity-feed',
  '/api/analytics',
  '/api/auth/session',
];

export function ApiDebugger() {
  const [apiStatuses, setApiStatuses] = useState<ApiStatus[]>([]);
  const [isVisible, setIsVisible] = useState(false);

  const checkApiEndpoint = async (endpoint: string): Promise<ApiStatus> => {
    const startTime = Date.now();
    
    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });

      const responseTime = Date.now() - startTime;
      const contentType = response.headers.get('content-type') || '';
      
      if (!response.ok) {
        return {
          endpoint,
          status: 'error',
          message: `HTTP ${response.status}: ${response.statusText}`,
          responseTime,
        };
      }

      // Check if response is JSON
      if (!contentType.includes('application/json')) {
        const text = await response.text();
        const isHtml = text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html');
        
        return {
          endpoint,
          status: 'error',
          message: `Expected JSON but got ${contentType}${isHtml ? ' (HTML page)' : ''}`,
          responseTime,
        };
      }

      // Try to parse JSON
      await response.json();
      
      return {
        endpoint,
        status: 'success',
        message: 'OK',
        responseTime,
      };
    } catch (error) {
      const responseTime = Date.now() - startTime;
      return {
        endpoint,
        status: 'error',
        message: error instanceof Error ? error.message : 'Unknown error',
        responseTime,
      };
    }
  };

  const checkAllEndpoints = async () => {
    setApiStatuses(API_ENDPOINTS.map(endpoint => ({
      endpoint,
      status: 'checking' as const,
      message: 'Checking...',
    })));

    const results = await Promise.all(
      API_ENDPOINTS.map(endpoint => checkApiEndpoint(endpoint))
    );

    setApiStatuses(results);
  };

  useEffect(() => {
    // Check for JSON parsing errors in console
    const originalError = console.error;
    console.error = (...args) => {
      const message = args.join(' ');
      if (message.includes('Unexpected token') && message.includes('<!DOCTYPE')) {
        setIsVisible(true);
      }
      originalError.apply(console, args);
    };

    return () => {
      console.error = originalError;
    };
  }, []);

  useEffect(() => {
    if (isVisible && apiStatuses.length === 0) {
      checkAllEndpoints();
    }
  }, [isVisible]);

  if (!isVisible) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <button
          onClick={() => setIsVisible(true)}
          className="bg-red-500 text-white p-2 rounded-full shadow-lg hover:bg-red-600 transition-colors"
          title="API Debugger"
        >
          <AlertCircle size={20} />
        </button>
      </div>
    );
  }

  const getStatusIcon = (status: ApiStatus['status']) => {
    switch (status) {
      case 'checking':
        return <Clock className="h-4 w-4 text-yellow-500 animate-spin" />;
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />;
    }
  };

  return (
    <div className="fixed bottom-4 right-4 z-50 bg-white border border-gray-300 rounded-lg shadow-lg max-w-md w-full">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">API Health Check</h3>
          <div className="flex space-x-2">
            <button
              onClick={checkAllEndpoints}
              className="p-1 text-gray-500 hover:text-gray-700 transition-colors"
              title="Refresh"
            >
              <RefreshCw size={16} />
            </button>
            <button
              onClick={() => setIsVisible(false)}
              className="p-1 text-gray-500 hover:text-gray-700 transition-colors"
              title="Close"
            >
              ✕
            </button>
          </div>
        </div>
      </div>

      <div className="p-4 max-h-80 overflow-y-auto">
        <div className="space-y-3">
          {apiStatuses.map((status) => (
            <div
              key={status.endpoint}
              className="flex items-center justify-between p-2 bg-gray-50 rounded-md"
            >
              <div className="flex items-center space-x-2 flex-1 min-w-0">
                {getStatusIcon(status.status)}
                <span className="text-sm font-mono text-gray-700 truncate">
                  {status.endpoint}
                </span>
              </div>
              
              <div className="flex flex-col items-end space-y-1">
                <span className={`text-xs font-medium ${
                  status.status === 'success' ? 'text-green-600' :
                  status.status === 'error' ? 'text-red-600' :
                  'text-yellow-600'
                }`}>
                  {status.message}
                </span>
                {status.responseTime && (
                  <span className="text-xs text-gray-500">
                    {status.responseTime}ms
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>

        {apiStatuses.some(s => s.status === 'error') && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <h4 className="text-sm font-medium text-red-800 mb-1">
              Common Solutions:
            </h4>
            <ul className="text-xs text-red-700 space-y-1 list-disc list-inside">
              <li>Restart the development server (npm run dev)</li>
              <li>Check environment variables (.env.local)</li>
              <li>Verify database connection</li>
              <li>Clear browser cache and cookies</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}