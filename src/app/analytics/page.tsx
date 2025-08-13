import React from 'react';
import AnalyticsClientPage from './AnalyticsClientPage';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Learning Analytics - NeuroQuest',
  description: 'View your learning progress, insights, and personalized recommendations',
};

export default function AnalyticsPage() {
  return <AnalyticsClientPage />;
}