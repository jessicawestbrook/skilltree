'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { OnboardingContextType, OnboardingStep, OnboardingProgress } from '../types';

const OnboardingContext = createContext<OnboardingContextType | undefined>(undefined);

interface OnboardingProviderProps {
  children: ReactNode;
}

const ONBOARDING_STEPS: OnboardingStep[] = [
  {
    id: 'welcome',
    title: 'Welcome to NeuroQuest',
    description: 'Discover how to master all human knowledge through our interactive learning platform',
    component: 'WelcomeStep',
    estimatedTime: 1,
  },
  {
    id: 'goals',
    title: 'Set Your Learning Goals',
    description: 'Tell us what you want to achieve so we can personalize your experience',
    component: 'GoalsStep',
    estimatedTime: 2,
  },
  {
    id: 'preferences',
    title: 'Customize Your Experience',
    description: 'Choose your difficulty level and study preferences',
    component: 'PreferencesStep',
    estimatedTime: 2,
  },
  {
    id: 'navigation',
    title: 'Learn the Basics',
    description: 'Discover how to navigate the knowledge graph and track your progress',
    component: 'NavigationStep',
    estimatedTime: 3,
  },
  {
    id: 'first-node',
    title: 'Complete Your First Node',
    description: 'Take your first step in the journey to master knowledge',
    component: 'FirstNodeStep',
    estimatedTime: 5,
  },
  {
    id: 'features',
    title: 'Explore Key Features',
    description: 'Learn about learning paths, achievements, and community features',
    component: 'FeaturesStep',
    estimatedTime: 3,
    isOptional: true,
  },
];

const STORAGE_KEY = 'neuroquest_onboarding_progress';

export const OnboardingProvider: React.FC<OnboardingProviderProps> = ({ children }) => {
  const [progress, setProgress] = useState<OnboardingProgress>({
    currentStep: 0,
    completedSteps: [],
    skippedSteps: [],
    totalSteps: ONBOARDING_STEPS.length,
    isCompleted: false,
  });

  const [isOnboarding, setIsOnboarding] = useState(false);

  // Load progress from localStorage on mount
  useEffect(() => {
    const savedProgress = localStorage.getItem(STORAGE_KEY);
    if (savedProgress) {
      try {
        const parsed = JSON.parse(savedProgress) as OnboardingProgress;
        // Convert date strings back to Date objects
        if (parsed.startedAt) {
          parsed.startedAt = new Date(parsed.startedAt);
        }
        if (parsed.completedAt) {
          parsed.completedAt = new Date(parsed.completedAt);
        }
        setProgress(parsed);
        setIsOnboarding(!parsed.isCompleted);
      } catch (error) {
        console.error('Failed to parse onboarding progress:', error);
      }
    }
  }, []);

  // Save progress to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [progress]);

  const getCurrentStep = (): OnboardingStep | null => {
    if (progress.currentStep >= ONBOARDING_STEPS.length) {
      return null;
    }
    return ONBOARDING_STEPS[progress.currentStep];
  };

  const startOnboarding = () => {
    const newProgress: OnboardingProgress = {
      currentStep: 0,
      completedSteps: [],
      skippedSteps: [],
      totalSteps: ONBOARDING_STEPS.length,
      isCompleted: false,
      startedAt: new Date(),
    };
    setProgress(newProgress);
    setIsOnboarding(true);
  };

  const nextStep = () => {
    console.log('nextStep called, current progress:', progress);
    setProgress(prev => {
      const newStep = prev.currentStep + 1;
      console.log('Updating step from', prev.currentStep, 'to', newStep);
      
      // Allow the step to go beyond the last index to signal completion
      if (newStep >= ONBOARDING_STEPS.length) {
        return {
          ...prev,
          currentStep: newStep,
          completedSteps: prev.currentStep < ONBOARDING_STEPS.length ? 
            [...prev.completedSteps, ONBOARDING_STEPS[prev.currentStep].id] : 
            prev.completedSteps,
        };
      }
      
      return {
        ...prev,
        currentStep: newStep,
        completedSteps: prev.currentStep < ONBOARDING_STEPS.length ? 
          [...prev.completedSteps, ONBOARDING_STEPS[prev.currentStep].id] : 
          prev.completedSteps,
      };
    });
  };

  const previousStep = () => {
    setProgress(prev => ({
      ...prev,
      currentStep: Math.max(prev.currentStep - 1, 0),
    }));
  };

  const skipStep = () => {
    const currentStep = getCurrentStep();
    if (currentStep) {
      setProgress(prev => ({
        ...prev,
        skippedSteps: [...prev.skippedSteps, currentStep.id],
        currentStep: prev.currentStep + 1,
      }));
    }
  };

  const completeStep = (stepId: string) => {
    setProgress(prev => ({
      ...prev,
      completedSteps: [...prev.completedSteps.filter(id => id !== stepId), stepId],
      currentStep: prev.currentStep + 1,
    }));
  };

  const completeOnboarding = () => {
    setProgress(prev => ({
      ...prev,
      isCompleted: true,
      completedAt: new Date(),
    }));
    setIsOnboarding(false);
  };

  const resetOnboarding = () => {
    localStorage.removeItem(STORAGE_KEY);
    setProgress({
      currentStep: 0,
      completedSteps: [],
      skippedSteps: [],
      totalSteps: ONBOARDING_STEPS.length,
      isCompleted: false,
    });
    setIsOnboarding(false);
  };

  const value: OnboardingContextType = {
    progress,
    currentStep: getCurrentStep(),
    isOnboarding,
    startOnboarding,
    nextStep,
    previousStep,
    skipStep,
    completeStep,
    completeOnboarding,
    resetOnboarding,
  };

  return (
    <OnboardingContext.Provider value={value}>
      {children}
    </OnboardingContext.Provider>
  );
};

export const useOnboarding = (): OnboardingContextType => {
  const context = useContext(OnboardingContext);
  if (context === undefined) {
    throw new Error('useOnboarding must be used within an OnboardingProvider');
  }
  return context;
};