'use client';

import React, { useState, CSSProperties } from 'react';
import { Clock, Zap, Gauge, Bell, Mail, Volume2 } from 'lucide-react';

export const PreferencesStep: React.FC = () => {
  const [preferences, setPreferences] = useState({
    difficultyLevel: 'intermediate' as 'beginner' | 'intermediate' | 'advanced',
    studyTime: 30,
    notificationsEnabled: true,
    emailUpdates: true,
    soundEnabled: true,
  });

  const difficultyLevels = [
    {
      id: 'beginner' as const,
      icon: <Zap size={20} color="white" />,
      title: 'Beginner',
      description: 'Start with the basics and build confidence',
      color: '#4ade80',
    },
    {
      id: 'intermediate' as const,
      icon: <Gauge size={20} color="white" />,
      title: 'Intermediate',
      description: 'Challenge yourself with moderate complexity',
      color: '#f59e0b',
    },
    {
      id: 'advanced' as const,
      icon: <Zap size={20} color="white" />,
      title: 'Advanced',
      description: 'Dive deep into complex topics',
      color: '#ef4444',
    },
  ];

  const studyTimeOptions = [15, 30, 45, 60, 90, 120];

  const styles = {
    container: {
      padding: '20px 0',
    } as CSSProperties,
    section: {
      marginBottom: '32px',
    } as CSSProperties,
    sectionTitle: {
      fontSize: '18px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '16px',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
    } as CSSProperties,
    difficultyGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gap: '12px',
    } as CSSProperties,
    difficultyCard: {
      padding: '16px',
      borderRadius: '12px',
      border: '2px solid #e0e0e0',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      textAlign: 'center',
    } as CSSProperties,
    difficultyCardSelected: {
      borderColor: '#667eea',
      background: '#f8f9ff',
      transform: 'translateY(-2px)',
    } as CSSProperties,
    difficultyIcon: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '40px',
      height: '40px',
      borderRadius: '10px',
      marginBottom: '12px',
    } as CSSProperties,
    difficultyTitle: {
      fontSize: '16px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '4px',
    } as CSSProperties,
    difficultyDescription: {
      fontSize: '12px',
      color: '#666',
      lineHeight: '1.3',
    } as CSSProperties,
    timeGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(80px, 1fr))',
      gap: '8px',
    } as CSSProperties,
    timeOption: {
      padding: '12px 8px',
      borderRadius: '8px',
      border: '2px solid #e0e0e0',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      textAlign: 'center',
      fontSize: '14px',
      fontWeight: 'bold',
    } as CSSProperties,
    timeOptionSelected: {
      borderColor: '#667eea',
      background: '#f8f9ff',
      color: '#667eea',
    } as CSSProperties,
    toggleSection: {
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
    } as CSSProperties,
    toggleItem: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '16px',
      background: '#f8f8f8',
      borderRadius: '12px',
    } as CSSProperties,
    toggleLabel: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      fontSize: '16px',
      color: '#2a2a2a',
    } as CSSProperties,
    toggleIcon: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '32px',
      height: '32px',
      borderRadius: '8px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
    } as CSSProperties,
    toggle: {
      position: 'relative',
      width: '48px',
      height: '24px',
      borderRadius: '12px',
      cursor: 'pointer',
      transition: 'background-color 0.3s ease',
    } as CSSProperties,
    toggleSlider: {
      position: 'absolute',
      top: '2px',
      left: '2px',
      width: '20px',
      height: '20px',
      borderRadius: '50%',
      background: 'white',
      transition: 'transform 0.3s ease',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    } as CSSProperties,
    summary: {
      background: 'linear-gradient(135deg, #f8f9ff, #fff)',
      border: '1px solid #e6e8ff',
      borderRadius: '16px',
      padding: '20px',
      marginTop: '24px',
    } as CSSProperties,
    summaryTitle: {
      fontSize: '16px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '12px',
    } as CSSProperties,
    summaryText: {
      fontSize: '14px',
      color: '#666',
      lineHeight: '1.5',
    } as CSSProperties,
  };

  const toggles = [
    {
      key: 'notificationsEnabled' as const,
      icon: <Bell size={16} color="white" />,
      label: 'Learning Reminders',
      description: 'Get notified about your study schedule',
    },
    {
      key: 'emailUpdates' as const,
      icon: <Mail size={16} color="white" />,
      label: 'Email Updates',
      description: 'Receive progress reports and tips',
    },
    {
      key: 'soundEnabled' as const,
      icon: <Volume2 size={16} color="white" />,
      label: 'Sound Effects',
      description: 'Audio feedback for achievements',
    },
  ];

  return (
    <div style={styles.container}>
      {/* Difficulty Level */}
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>
          <Gauge size={20} color="#667eea" />
          Difficulty Level
        </h3>
        <div style={styles.difficultyGrid}>
          {difficultyLevels.map((level) => (
            <div
              key={level.id}
              style={{
                ...styles.difficultyCard,
                ...(preferences.difficultyLevel === level.id ? styles.difficultyCardSelected : {}),
              }}
              onClick={() => setPreferences(prev => ({ ...prev, difficultyLevel: level.id }))}
            >
              <div style={{ ...styles.difficultyIcon, background: level.color }}>
                {level.icon}
              </div>
              <div style={styles.difficultyTitle}>{level.title}</div>
              <div style={styles.difficultyDescription}>{level.description}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Study Time */}
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>
          <Clock size={20} color="#667eea" />
          Daily Study Time
        </h3>
        <div style={styles.timeGrid}>
          {studyTimeOptions.map((time) => (
            <div
              key={time}
              style={{
                ...styles.timeOption,
                ...(preferences.studyTime === time ? styles.timeOptionSelected : {}),
              }}
              onClick={() => setPreferences(prev => ({ ...prev, studyTime: time }))}
            >
              {time}m
            </div>
          ))}
        </div>
      </div>

      {/* Notifications */}
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>
          <Bell size={20} color="#667eea" />
          Preferences
        </h3>
        <div style={styles.toggleSection}>
          {toggles.map((toggle) => (
            <div key={toggle.key} style={styles.toggleItem}>
              <div style={styles.toggleLabel}>
                <div style={styles.toggleIcon}>
                  {toggle.icon}
                </div>
                <div>
                  <div style={{ fontWeight: 'bold' }}>{toggle.label}</div>
                  <div style={{ fontSize: '12px', color: '#666' }}>{toggle.description}</div>
                </div>
              </div>
              <div
                style={{
                  ...styles.toggle,
                  background: preferences[toggle.key] ? '#667eea' : '#ccc',
                }}
                onClick={() => setPreferences(prev => ({ ...prev, [toggle.key]: !prev[toggle.key] }))}
              >
                <div
                  style={{
                    ...styles.toggleSlider,
                    transform: preferences[toggle.key] ? 'translateX(24px)' : 'translateX(0)',
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Summary */}
      <div style={styles.summary}>
        <h4 style={styles.summaryTitle}>Your Learning Profile</h4>
        <p style={styles.summaryText}>
          You&apos;ll start with <strong>{preferences.difficultyLevel}</strong> difficulty content, 
          studying for <strong>{preferences.studyTime} minutes per day</strong>. 
          {preferences.notificationsEnabled && ' We&apos;ll send you helpful reminders.'}
          {preferences.emailUpdates && ' You&apos;ll receive progress updates via email.'}
        </p>
      </div>
    </div>
  );
};