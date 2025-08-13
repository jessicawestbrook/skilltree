'use client';

import React, { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useOnboarding } from '../../contexts/OnboardingContext';
import { OnboardingModal } from './OnboardingModal';

export const OnboardingTrigger: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const { isOnboarding, startOnboarding, progress } = useOnboarding();
  const [showOnboarding, setShowOnboarding] = useState(false);

  useEffect(() => {
    // Check if user is new and hasn't completed onboarding
    if (isAuthenticated && user && !progress.isCompleted) {
      // Check if this is a new user (created recently)
      const isNewUser = user.createdAt && 
        (Date.now() - user.createdAt.getTime()) < 24 * 60 * 60 * 1000; // 24 hours

      // Start onboarding for new users or if explicitly triggered
      if (isNewUser || (!progress.startedAt && !isOnboarding)) {
        setTimeout(() => {
          startOnboarding();
          setShowOnboarding(true);
        }, 1000); // Small delay for better UX
      } else if (isOnboarding && !progress.isCompleted) {
        // Resume existing onboarding
        setShowOnboarding(true);
      }
    }
  }, [isAuthenticated, user, progress, isOnboarding, startOnboarding]);

  const handleCloseOnboarding = () => {
    setShowOnboarding(false);
  };

  return (
    <OnboardingModal 
      isOpen={showOnboarding} 
      onClose={handleCloseOnboarding}
    />
  );
};