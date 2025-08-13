'use client';

import React, { CSSProperties } from 'react';
import { X, ArrowLeft, ArrowRight, SkipForward, CheckCircle } from 'lucide-react';
import { useOnboarding } from '../../contexts/OnboardingContext';
import { WelcomeStep } from './steps/WelcomeStep';
import { GoalsStep } from './steps/GoalsStep';
import { PreferencesStep } from './steps/PreferencesStep';
import { NavigationStep } from './steps/NavigationStep';
import { FirstNodeStep } from './steps/FirstNodeStep';
import { FeaturesStep } from './steps/FeaturesStep';

interface OnboardingModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const OnboardingModal: React.FC<OnboardingModalProps> = ({ isOpen, onClose }) => {
  const {
    progress,
    currentStep,
    nextStep,
    previousStep,
    skipStep,
    completeOnboarding,
  } = useOnboarding();

  if (!isOpen || !currentStep) return null;

  const handleNext = () => {
    if (progress.currentStep >= progress.totalSteps - 1) {
      completeOnboarding();
      onClose();
    } else {
      nextStep();
    }
  };

  // Remove unused handleComplete function as it's replaced by handleNext

  const handleSkip = () => {
    if (currentStep.isOptional) {
      skipStep();
      if (progress.currentStep >= progress.totalSteps - 1) {
        completeOnboarding();
        onClose();
      }
    }
  };

  const progressPercentage = ((progress.currentStep + 1) / progress.totalSteps) * 100;

  const styles = {
    overlay: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.8)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 3000,
      padding: '20px',
    } as CSSProperties,
    modal: {
      background: 'white',
      borderRadius: '24px',
      padding: '0',
      maxWidth: '800px',
      width: '100%',
      maxHeight: '90vh',
      overflow: 'hidden',
      boxShadow: '0 25px 50px rgba(0, 0, 0, 0.25)',
      position: 'relative',
    } as CSSProperties,
    header: {
      padding: '30px 40px 20px',
      borderBottom: '1px solid #f0f0f0',
      position: 'relative',
    } as CSSProperties,
    closeButton: {
      position: 'absolute',
      top: '20px',
      right: '20px',
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      padding: '8px',
      borderRadius: '8px',
      transition: 'background-color 0.2s',
    } as CSSProperties,
    progressBar: {
      width: '100%',
      height: '6px',
      background: '#f0f0f0',
      borderRadius: '3px',
      overflow: 'hidden',
      marginBottom: '20px',
    } as CSSProperties,
    progressFill: {
      height: '100%',
      background: 'linear-gradient(90deg, #667eea, #764ba2)',
      borderRadius: '3px',
      transition: 'width 0.3s ease',
      width: `${progressPercentage}%`,
    } as CSSProperties,
    stepIndicator: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      marginBottom: '16px',
      fontSize: '14px',
      color: '#666',
    } as CSSProperties,
    stepBadge: {
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      padding: '4px 12px',
      borderRadius: '12px',
      fontSize: '12px',
      fontWeight: 'bold',
    } as CSSProperties,
    title: {
      fontSize: '28px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '8px',
      lineHeight: '1.2',
    } as CSSProperties,
    description: {
      fontSize: '16px',
      color: '#666',
      lineHeight: '1.5',
    } as CSSProperties,
    content: {
      padding: '40px',
      minHeight: '300px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
    } as CSSProperties,
    footer: {
      padding: '20px 40px 30px',
      borderTop: '1px solid #f0f0f0',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    } as CSSProperties,
    buttonGroup: {
      display: 'flex',
      gap: '12px',
    } as CSSProperties,
    button: {
      padding: '12px 24px',
      border: 'none',
      borderRadius: '12px',
      fontSize: '14px',
      fontWeight: 'bold',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
    } as CSSProperties,
    primaryButton: {
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
    } as CSSProperties,
    secondaryButton: {
      background: '#f8f8f8',
      color: '#666',
      border: '1px solid #e0e0e0',
    } as CSSProperties,
    skipButton: {
      background: 'none',
      color: '#999',
      border: 'none',
      padding: '8px 16px',
      fontSize: '14px',
    } as CSSProperties,
    timeEstimate: {
      fontSize: '12px',
      color: '#999',
      fontStyle: 'italic',
    } as CSSProperties,
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        {/* Header */}
        <div style={styles.header}>
          <button
            onClick={onClose}
            style={styles.closeButton}
            onMouseEnter={(e) => {
              (e.target as HTMLElement).style.backgroundColor = '#f0f0f0';
            }}
            onMouseLeave={(e) => {
              (e.target as HTMLElement).style.backgroundColor = 'transparent';
            }}
          >
            <X size={20} color="#999" />
          </button>

          <div style={styles.progressBar}>
            <div style={styles.progressFill} />
          </div>

          <div style={styles.stepIndicator}>
            <span style={styles.stepBadge}>
              Step {progress.currentStep + 1} of {progress.totalSteps}
            </span>
            {currentStep.estimatedTime && (
              <span style={styles.timeEstimate}>
                ~{currentStep.estimatedTime} min
              </span>
            )}
          </div>

          <h2 style={styles.title}>{currentStep.title}</h2>
          <p style={styles.description}>{currentStep.description}</p>
        </div>

        {/* Content */}
        <div style={styles.content}>
          {/* Dynamic content will be rendered here based on currentStep.component */}
          <OnboardingStepContent stepId={currentStep.id} />
        </div>

        {/* Footer */}
        <div style={styles.footer}>
          <div>
            {currentStep.isOptional && (
              <button
                onClick={handleSkip}
                style={styles.skipButton}
              >
                <SkipForward size={16} />
                Skip this step
              </button>
            )}
          </div>

          <div style={styles.buttonGroup}>
            {progress.currentStep > 0 && (
              <button
                onClick={previousStep}
                style={{ ...styles.button, ...styles.secondaryButton }}
              >
                <ArrowLeft size={16} />
                Back
              </button>
            )}

            <button
              onClick={handleNext}
              style={{ ...styles.button, ...styles.primaryButton }}
            >
              {progress.currentStep >= progress.totalSteps - 1 ? (
                <>
                  <CheckCircle size={16} />
                  Complete
                </>
              ) : (
                <>
                  Next
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Dynamic content component that renders different steps
const OnboardingStepContent: React.FC<{ stepId: string }> = ({ stepId }) => {
  switch (stepId) {
    case 'welcome':
      return <WelcomeStep />;
    case 'goals':
      return <GoalsStep />;
    case 'preferences':
      return <PreferencesStep />;
    case 'navigation':
      return <NavigationStep />;
    case 'first-node':
      return <FirstNodeStep />;
    case 'features':
      return <FeaturesStep />;
    default:
      return <div>Step content not found</div>;
  }
};