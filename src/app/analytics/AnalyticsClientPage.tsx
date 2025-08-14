'use client';

import React from 'react';
import { AuthGuard } from '@/components/AuthGuard';
import AnalyticsDashboard from '@/components/AnalyticsDashboard';
import ModernHeader from '@/components/ModernHeader';
import { useUserStats } from '@/hooks/useUserStats';

export default function AnalyticsClientPage() {
  const { userStats } = useUserStats();

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <ModernHeader 
          userStats={userStats}
          isMobile={false}
          calculateProgress={() => 0}
          onAuthClick={() => {}}
        />
        
        <div className="container mx-auto px-4 py-8">
          <AnalyticsDashboard />
        </div>
      </div>
    </AuthGuard>
  );
}