'use client';

import React, { useState, CSSProperties } from 'react';
import { HelpCircle, RotateCcw } from 'lucide-react';
import { useOnboarding } from '../../contexts/OnboardingContext';
import { OnboardingModal } from './OnboardingModal';

interface OnboardingButtonProps {
  variant?: 'help' | 'restart';
  size?: 'small' | 'medium' | 'large';
  showText?: boolean;
}

export const OnboardingButton: React.FC<OnboardingButtonProps> = ({ 
  variant = 'help',
  size = 'medium',
  showText = true
}) => {
  const { startOnboarding, resetOnboarding, progress } = useOnboarding();
  const [showOnboarding, setShowOnboarding] = useState(false);

  const handleClick = () => {
    if (variant === 'restart' || progress.isCompleted) {
      resetOnboarding();
    }
    startOnboarding();
    setShowOnboarding(true);
  };

  const handleCloseOnboarding = () => {
    setShowOnboarding(false);
  };

  const sizeStyles = {
    small: {
      padding: '8px 12px',
      fontSize: '12px',
      iconSize: 14,
    },
    medium: {
      padding: '10px 16px',
      fontSize: '14px',
      iconSize: 16,
    },
    large: {
      padding: '12px 20px',
      fontSize: '16px',
      iconSize: 18,
    },
  };

  const currentSize = sizeStyles[size];

  const styles = {
    button: {
      padding: currentSize.padding,
      background: variant === 'restart' 
        ? 'linear-gradient(135deg, #f59e0b, #d97706)'
        : 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      fontSize: currentSize.fontSize,
      fontWeight: 'bold',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      display: 'inline-flex',
      alignItems: 'center',
      gap: showText ? '8px' : '0',
    } as CSSProperties,
    iconOnly: {
      width: `${currentSize.iconSize + 16}px`,
      height: `${currentSize.iconSize + 16}px`,
      borderRadius: '50%',
      justifyContent: 'center',
    } as CSSProperties,
  };

  const icon = variant === 'restart' 
    ? <RotateCcw size={currentSize.iconSize} />
    : <HelpCircle size={currentSize.iconSize} />;

  const text = variant === 'restart' 
    ? 'Restart Tour'
    : progress.isCompleted 
      ? 'View Tutorial' 
      : 'Get Help';

  return (
    <>
      <button
        style={{
          ...styles.button,
          ...(showText ? {} : styles.iconOnly),
        }}
        onClick={handleClick}
        onMouseEnter={(e) => {
          (e.target as HTMLElement).style.transform = 'translateY(-2px)';
          (e.target as HTMLElement).style.boxShadow = '0 4px 15px rgba(0,0,0,0.2)';
        }}
        onMouseLeave={(e) => {
          (e.target as HTMLElement).style.transform = 'translateY(0)';
          (e.target as HTMLElement).style.boxShadow = 'none';
        }}
        title={!showText ? text : undefined}
      >
        {icon}
        {showText && <span>{text}</span>}
      </button>

      <OnboardingModal 
        isOpen={showOnboarding} 
        onClose={handleCloseOnboarding}
      />
    </>
  );
};