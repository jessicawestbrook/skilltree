'use client';

import React, { useEffect, useState, useRef } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useOnboarding } from '../../contexts/OnboardingContext';
import { OnboardingModal } from './OnboardingModal';

export const OnboardingTrigger: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const { isOnboarding, startOnboarding, progress } = useOnboarding();
  const [showOnboarding, setShowOnboarding] = useState(false);
  const hasInitialized = useRef(false);

  useEffect(() => {
    // Only initialize once when component mounts and user is authenticated
    if (!hasInitialized.current && isAuthenticated && user) {
      hasInitialized.current = true;
      
      if (!progress.isCompleted) {
        // Check if this is a new user (created recently)
        const isNewUser = user.createdAt && 
          (Date.now() - user.createdAt.getTime()) < 24 * 60 * 60 * 1000; // 24 hours

        // Start onboarding for new users
        if (isNewUser && !progress.startedAt) {
          setTimeout(() => {
            startOnboarding();
            setShowOnboarding(true);
          }, 1000); // Small delay for better UX
        } else if (isOnboarding) {
          // Resume existing onboarding
          setShowOnboarding(true);
        }
      }
    }
  }, [isAuthenticated, user, progress.isCompleted, progress.startedAt, isOnboarding, startOnboarding]);

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