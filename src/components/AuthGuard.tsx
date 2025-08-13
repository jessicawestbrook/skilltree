'use client';

import React, { ReactNode } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface AuthGuardProps {
  children: ReactNode;
  fallback?: ReactNode;
}

export const AuthGuard: React.FC<AuthGuardProps> = ({ children, fallback }) => {
  const { isLoading, sessionReady } = useAuth();

  // Show loading state while checking session
  if (!sessionReady || isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
        <div className="text-center">
          <div className="animate-pulse mb-4">
            <div className="w-16 h-16 bg-purple-500 rounded-full mx-auto"></div>
          </div>
          <p className="text-gray-600 dark:text-gray-300">Loading your session...</p>
        </div>
      </div>
    );
  }

  // If a fallback is provided and user is not authenticated, show fallback
  if (fallback) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
};