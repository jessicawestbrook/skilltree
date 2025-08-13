'use client';

import React, { useState, CSSProperties } from 'react';
import { Target, BookOpen, Briefcase, GraduationCap, Lightbulb, Heart } from 'lucide-react';

export const GoalsStep: React.FC = () => {
  const [selectedGoals, setSelectedGoals] = useState<string[]>([]);

  const learningGoals = [
    {
      id: 'career',
      icon: <Briefcase size={24} color="white" />,
      title: 'Career Advancement',
      description: 'Build skills for professional growth',
      gradient: 'linear-gradient(135deg, #667eea, #764ba2)',
    },
    {
      id: 'education',
      icon: <GraduationCap size={24} color="white" />,
      title: 'Academic Excellence',
      description: 'Improve grades and test scores',
      gradient: 'linear-gradient(135deg, #f093fb, #f5576c)',
    },
    {
      id: 'curiosity',
      icon: <Lightbulb size={24} color="white" />,
      title: 'Personal Curiosity',
      description: 'Explore topics that fascinate you',
      gradient: 'linear-gradient(135deg, #4facfe, #00f2fe)',
    },
    {
      id: 'hobby',
      icon: <Heart size={24} color="white" />,
      title: 'Hobby & Interests',
      description: 'Deepen knowledge in your passions',
      gradient: 'linear-gradient(135deg, #fa709a, #fee140)',
    },
    {
      id: 'general',
      icon: <BookOpen size={24} color="white" />,
      title: 'General Knowledge',
      description: 'Become a well-rounded learner',
      gradient: 'linear-gradient(135deg, #a8edea, #fed6e3)',
    },
    {
      id: 'specific',
      icon: <Target size={24} color="white" />,
      title: 'Specific Skills',
      description: 'Master particular competencies',
      gradient: 'linear-gradient(135deg, #ffecd2, #fcb69f)',
    },
  ];

  const handleGoalToggle = (goalId: string) => {
    setSelectedGoals(prev => 
      prev.includes(goalId)
        ? prev.filter(id => id !== goalId)
        : [...prev, goalId]
    );
  };

  const styles = {
    container: {
      padding: '20px 0',
    } as CSSProperties,
    header: {
      textAlign: 'center',
      marginBottom: '40px',
    } as CSSProperties,
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '16px',
    } as CSSProperties,
    subtitle: {
      fontSize: '16px',
      color: '#666',
      lineHeight: '1.6',
      maxWidth: '500px',
      margin: '0 auto',
    } as CSSProperties,
    goalsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
      gap: '16px',
      marginBottom: '32px',
    } as CSSProperties,
    goalCard: {
      padding: '20px',
      borderRadius: '16px',
      border: '2px solid transparent',
      background: '#fff',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      position: 'relative',
      overflow: 'hidden',
    } as CSSProperties,
    goalCardSelected: {
      border: '2px solid #667eea',
      transform: 'translateY(-2px)',
      boxShadow: '0 8px 25px rgba(102, 126, 234, 0.15)',
    } as CSSProperties,
    goalIcon: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '48px',
      height: '48px',
      borderRadius: '12px',
      marginBottom: '16px',
    } as CSSProperties,
    goalTitle: {
      fontSize: '18px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '8px',
    } as CSSProperties,
    goalDescription: {
      fontSize: '14px',
      color: '#666',
      lineHeight: '1.4',
    } as CSSProperties,
    selectedIndicator: {
      position: 'absolute',
      top: '12px',
      right: '12px',
      width: '24px',
      height: '24px',
      borderRadius: '50%',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontSize: '12px',
      fontWeight: 'bold',
    } as CSSProperties,
    tip: {
      background: '#f8f9ff',
      border: '1px solid #e6e8ff',
      borderRadius: '12px',
      padding: '16px',
      textAlign: 'center',
    } as CSSProperties,
    tipText: {
      fontSize: '14px',
      color: '#666',
      margin: 0,
    } as CSSProperties,
    counter: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      padding: '8px 16px',
      borderRadius: '20px',
      fontSize: '14px',
      fontWeight: 'bold',
      marginBottom: '24px',
    } as CSSProperties,
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>What are your learning goals?</h2>
        <p style={styles.subtitle}>
          Select the goals that resonate with you. We&apos;ll use this to personalize your learning experience.
        </p>
        {selectedGoals.length > 0 && (
          <div style={styles.counter}>
            <Target size={16} />
            {selectedGoals.length} goal{selectedGoals.length !== 1 ? 's' : ''} selected
          </div>
        )}
      </div>

      <div style={styles.goalsGrid}>
        {learningGoals.map((goal) => {
          const isSelected = selectedGoals.includes(goal.id);
          return (
            <div
              key={goal.id}
              style={{
                ...styles.goalCard,
                ...(isSelected ? styles.goalCardSelected : {}),
              }}
              onClick={() => handleGoalToggle(goal.id)}
            >
              {isSelected && (
                <div style={styles.selectedIndicator}>
                  ✓
                </div>
              )}
              <div style={{ ...styles.goalIcon, background: goal.gradient }}>
                {goal.icon}
              </div>
              <h3 style={styles.goalTitle}>{goal.title}</h3>
              <p style={styles.goalDescription}>{goal.description}</p>
            </div>
          );
        })}
      </div>

      <div style={styles.tip}>
        <p style={styles.tipText}>
          💡 Tip: You can select multiple goals and change them anytime in your profile settings.
        </p>
      </div>
    </div>
  );
};