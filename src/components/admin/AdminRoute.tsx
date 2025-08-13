'use client';

import React, { Suspense } from 'react';
import { LoadingSpinner } from './LoadingSpinner';

interface AdminRouteProps {
  children: React.ReactNode;
  loadingMessage?: string;
}

export const AdminRoute: React.FC<AdminRouteProps> = ({ 
  children, 
  loadingMessage = 'Loading admin content...' 
}) => {
  return (
    <Suspense fallback={<LoadingSpinner message={loadingMessage} />}>
      {children}
    </Suspense>
  );
};

// HOC for wrapping admin pages with code splitting
export function withAdminRoute<P extends object>(
  Component: React.ComponentType<P>,
  loadingMessage?: string
) {
  return function AdminRouteWrapper(props: P) {
    return (
      <AdminRoute loadingMessage={loadingMessage}>
        <Component {...props} />
      </AdminRoute>
    );
  };
}