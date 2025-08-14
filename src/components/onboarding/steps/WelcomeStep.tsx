'use client';

import React, { CSSProperties } from 'react';
import { Trees, Sparkles, Target, Users } from 'lucide-react';

export const WelcomeStep: React.FC = () => {
  const styles = {
    container: {
      textAlign: 'center',
      padding: '20px 0',
    } as CSSProperties,
    hero: {
      marginBottom: '40px',
    } as CSSProperties,
    heroIcon: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '120px',
      height: '120px',
      borderRadius: '50%',
      background: 'linear-gradient(135deg, #059669, #0ea5e9)',
      marginBottom: '24px',
      boxShadow: '0 10px 30px rgba(102, 126, 234, 0.3)',
    } as CSSProperties,
    welcomeText: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '16px',
    } as CSSProperties,
    subtitle: {
      fontSize: '18px',
      color: '#666',
      lineHeight: '1.6',
      maxWidth: '500px',
      margin: '0 auto',
    } as CSSProperties,
    features: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
      gap: '20px',
      marginTop: '40px',
    } as CSSProperties,
    feature: {
      padding: '20px',
      borderRadius: '16px',
      background: '#f8f9ff',
      textAlign: 'center',
    } as CSSProperties,
    featureIcon: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '48px',
      height: '48px',
      borderRadius: '12px',
      background: 'linear-gradient(135deg, #059669, #0ea5e9)',
      marginBottom: '12px',
    } as CSSProperties,
    featureTitle: {
      fontSize: '16px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '8px',
    } as CSSProperties,
    featureDescription: {
      fontSize: '14px',
      color: '#666',
      lineHeight: '1.4',
    } as CSSProperties,
    stats: {
      display: 'flex',
      justifyContent: 'center',
      gap: '32px',
      marginTop: '32px',
      padding: '24px',
      background: 'linear-gradient(135deg, #f8f9ff, #fff)',
      borderRadius: '16px',
      border: '1px solid #e6e8ff',
    } as CSSProperties,
    stat: {
      textAlign: 'center',
    } as CSSProperties,
    statNumber: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#667eea',
      display: 'block',
    } as CSSProperties,
    statLabel: {
      fontSize: '12px',
      color: '#666',
      textTransform: 'uppercase',
      letterSpacing: '0.5px',
    } as CSSProperties,
  };

  const features = [
    {
      icon: <Trees size={24} color="white" />,
      title: 'Smart Learning',
      description: 'AI-powered personalized learning paths'
    },
    {
      icon: <Target size={24} color="white" />,
      title: 'Goal Tracking',
      description: 'Set and achieve your learning objectives'
    },
    {
      icon: <Sparkles size={24} color="white" />,
      title: 'Gamification',
      description: 'Earn points, levels, and achievements'
    },
    {
      icon: <Users size={24} color="white" />,
      title: 'Community',
      description: 'Connect with fellow learners'
    },
  ];

  return (
    <div style={styles.container}>
      <div style={styles.hero}>
        <div style={styles.heroIcon}>
          <Trees size={60} color="white" />
        </div>
        <h1 style={styles.welcomeText}>
          Welcome to SkillTree! 🌳
        </h1>
        <p style={styles.subtitle}>
          Grow Your Skills. Master Your Future. Plant the seeds of knowledge and watch your abilities 
          bloom through personalized learning paths designed for homeschoolers and supplemental learners.
        </p>
      </div>

      <div style={styles.features}>
        {features.map((feature, index) => (
          <div key={index} style={styles.feature}>
            <div style={styles.featureIcon}>
              {feature.icon}
            </div>
            <h3 style={styles.featureTitle}>{feature.title}</h3>
            <p style={styles.featureDescription}>{feature.description}</p>
          </div>
        ))}
      </div>

      <div style={styles.stats}>
        <div style={styles.stat}>
          <span style={styles.statNumber}>10K+</span>
          <span style={styles.statLabel}>Skills to Master</span>
        </div>
        <div style={styles.stat}>
          <span style={styles.statNumber}>50+</span>
          <span style={styles.statLabel}>Learning Paths</span>
        </div>
        <div style={styles.stat}>
          <span style={styles.statNumber}>98%</span>
          <span style={styles.statLabel}>Success Rate</span>
        </div>
      </div>
    </div>
  );
};