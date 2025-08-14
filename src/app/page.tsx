'use client';

import React, { Suspense, lazy, useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

// Minimal loading component
const LoadingScreen = () => (
  <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 flex items-center justify-center">
    <div className="text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
      <div className="text-gray-600">Loading SkillTree...</div>
    </div>
  </div>
);

// Lazy load the entire main app
const MainApp = dynamic(() => import('./page-original').then(mod => ({ default: mod.default })), {
  ssr: false,
  loading: () => <LoadingScreen />
});

export default function OptimizedPage() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <LoadingScreen />;
  }

  return (
    <Suspense fallback={<LoadingScreen />}>
      <MainApp />
    </Suspense>
  );
}