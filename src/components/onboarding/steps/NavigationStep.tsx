'use client';

import React, { useState, CSSProperties } from 'react';
import { Map, Search, Target, Trophy, BookOpen, ArrowRight, Eye } from 'lucide-react';

export const NavigationStep: React.FC = () => {
  const [currentDemo, setCurrentDemo] = useState(0);

  const demoSteps = [
    {
      title: 'Knowledge Graph',
      icon: <Map size={24} color="white" />,
      description: 'Navigate through interconnected topics and see how knowledge builds upon itself.',
      visual: '🗺️',
      tip: 'Click on any node to explore related concepts'
    },
    {
      title: 'Search & Discover',
      icon: <Search size={24} color="white" />,
      description: 'Find specific topics quickly or browse by category to discover new areas of interest.',
      visual: '🔍',
      tip: 'Use filters to narrow down by difficulty or time commitment'
    },
    {
      title: 'Progress Tracking',
      icon: <Target size={24} color="white" />,
      description: 'Monitor your learning journey with detailed progress bars and achievement milestones.',
      visual: '📊',
      tip: 'Green nodes are completed, blue are available, grey are locked'
    },
    {
      title: 'Achievements',
      icon: <Trophy size={24} color="white" />,
      description: 'Earn badges, points, and level up as you master new concepts and complete challenges.',
      visual: '🏆',
      tip: 'Check your profile to see all earned achievements'
    },
  ];

  const styles = {
    container: {
      padding: '20px 0',
    } as CSSProperties,
    header: {
      textAlign: 'center',
      marginBottom: '32px',
    } as CSSProperties,
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '12px',
    } as CSSProperties,
    subtitle: {
      fontSize: '16px',
      color: '#666',
      lineHeight: '1.6',
    } as CSSProperties,
    demoContainer: {
      border: '2px solid #e6e8ff',
      borderRadius: '16px',
      overflow: 'hidden',
      marginBottom: '24px',
    } as CSSProperties,
    demoContent: {
      padding: '32px',
      textAlign: 'center',
      background: 'linear-gradient(135deg, #f8f9ff, #fff)',
    } as CSSProperties,
    demoVisual: {
      fontSize: '48px',
      marginBottom: '20px',
    } as CSSProperties,
    demoTitle: {
      fontSize: '20px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '12px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '12px',
    } as CSSProperties,
    demoIcon: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '32px',
      height: '32px',
      borderRadius: '8px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
    } as CSSProperties,
    demoDescription: {
      fontSize: '16px',
      color: '#666',
      lineHeight: '1.6',
      marginBottom: '16px',
    } as CSSProperties,
    demoTip: {
      background: '#e6f3ff',
      border: '1px solid #b3d9ff',
      borderRadius: '8px',
      padding: '12px',
      fontSize: '14px',
      color: '#0066cc',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
    } as CSSProperties,
    navigation: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '20px 32px',
      background: '#fff',
      borderTop: '1px solid #e6e8ff',
    } as CSSProperties,
    navButton: {
      padding: '8px 16px',
      border: 'none',
      borderRadius: '8px',
      cursor: 'pointer',
      fontSize: '14px',
      fontWeight: 'bold',
      transition: 'all 0.3s ease',
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
    } as CSSProperties,
    prevButton: {
      background: '#f0f0f0',
      color: '#666',
    } as CSSProperties,
    nextButton: {
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
    } as CSSProperties,
    stepIndicators: {
      display: 'flex',
      gap: '8px',
    } as CSSProperties,
    stepDot: {
      width: '8px',
      height: '8px',
      borderRadius: '50%',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
    } as CSSProperties,
    stepDotActive: {
      background: '#667eea',
    } as CSSProperties,
    stepDotInactive: {
      background: '#d0d0d0',
    } as CSSProperties,
    features: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '16px',
      marginTop: '24px',
    } as CSSProperties,
    feature: {
      padding: '16px',
      background: '#f8f9ff',
      borderRadius: '12px',
      textAlign: 'center',
    } as CSSProperties,
    featureIcon: {
      width: '40px',
      height: '40px',
      margin: '0 auto 12px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      borderRadius: '10px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    } as CSSProperties,
    featureTitle: {
      fontSize: '14px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '4px',
    } as CSSProperties,
    featureDescription: {
      fontSize: '12px',
      color: '#666',
    } as CSSProperties,
  };

  const currentStep = demoSteps[currentDemo];

  const nextDemo = () => {
    setCurrentDemo((prev) => (prev + 1) % demoSteps.length);
  };

  const prevDemo = () => {
    setCurrentDemo((prev) => (prev - 1 + demoSteps.length) % demoSteps.length);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Master the Navigation</h2>
        <p style={styles.subtitle}>
          Learn how to efficiently navigate and make the most of your learning experience
        </p>
      </div>

      <div style={styles.demoContainer}>
        <div style={styles.demoContent}>
          <div style={styles.demoVisual}>{currentStep.visual}</div>
          <h3 style={styles.demoTitle}>
            <div style={styles.demoIcon}>
              {currentStep.icon}
            </div>
            {currentStep.title}
          </h3>
          <p style={styles.demoDescription}>{currentStep.description}</p>
          <div style={styles.demoTip}>
            <Eye size={16} />
            <span>{currentStep.tip}</span>
          </div>
        </div>

        <div style={styles.navigation}>
          <button
            onClick={prevDemo}
            style={{ ...styles.navButton, ...styles.prevButton }}
            disabled={currentDemo === 0}
          >
            ← Previous
          </button>

          <div style={styles.stepIndicators}>
            {demoSteps.map((_, index) => (
              <div
                key={index}
                style={{
                  ...styles.stepDot,
                  ...(index === currentDemo ? styles.stepDotActive : styles.stepDotInactive),
                }}
                onClick={() => setCurrentDemo(index)}
              />
            ))}
          </div>

          <button
            onClick={nextDemo}
            style={{ ...styles.navButton, ...styles.nextButton }}
            disabled={currentDemo === demoSteps.length - 1}
          >
            Next <ArrowRight size={16} />
          </button>
        </div>
      </div>

      <div style={styles.features}>
        <div style={styles.feature}>
          <div style={styles.featureIcon}>
            <BookOpen size={20} color="white" />
          </div>
          <div style={styles.featureTitle}>Learning Paths</div>
          <div style={styles.featureDescription}>Guided sequences of topics</div>
        </div>
        <div style={styles.feature}>
          <div style={styles.featureIcon}>
            <Target size={20} color="white" />
          </div>
          <div style={styles.featureTitle}>Prerequisites</div>
          <div style={styles.featureDescription}>Unlock nodes by completing basics</div>
        </div>
        <div style={styles.feature}>
          <div style={styles.featureIcon}>
            <Trophy size={20} color="white" />
          </div>
          <div style={styles.featureTitle}>Achievements</div>
          <div style={styles.featureDescription}>Earn rewards for your progress</div>
        </div>
      </div>
    </div>
  );
};