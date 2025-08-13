'use client';

import dynamic from 'next/dynamic';
import { LoadingSpinner } from './LoadingSpinner';

// Dynamic imports for heavy admin components
export const DynamicQuestionEditor = dynamic(
  () => import('@/app/admin/questions/new/page').then(mod => mod.default),
  {
    loading: () => <LoadingSpinner message="Loading question editor..." />,
    ssr: false
  }
);

export const DynamicContentEditor = dynamic(
  () => import('@/app/admin/content/new/page').then(mod => mod.default),
  {
    loading: () => <LoadingSpinner message="Loading content editor..." />,
    ssr: false
  }
);

export const DynamicBatchUpload = dynamic(
  () => import('@/app/admin/upload/page').then(mod => mod.default),
  {
    loading: () => <LoadingSpinner message="Loading upload tools..." />,
    ssr: false
  }
);

// Utility function for creating dynamic admin routes
export const createDynamicAdminRoute = <P extends Record<string, unknown>>(
  importFn: () => Promise<{ default: React.ComponentType<P> }>,
  loadingMessage: string = 'Loading...'
) => {
  return dynamic(importFn, {
    loading: () => <LoadingSpinner message={loadingMessage} />,
    ssr: false
  });
};