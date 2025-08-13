'use client';

import React, { CSSProperties } from 'react';
import { 
  Users, MessageSquare, BookOpen, Trophy, Zap, 
  Calendar, Target, Smartphone, Bell, Share2 
} from 'lucide-react';

export const FeaturesStep: React.FC = () => {
  const features = [
    {
      category: 'Learning',
      items: [
        {
          icon: <BookOpen size={20} color="white" />,
          title: 'Learning Paths',
          description: 'Curated sequences of topics designed by experts',
          color: '#667eea',
        },
        {
          icon: <Zap size={20} color="white" />,
          title: 'Adaptive Learning',
          description: 'AI adjusts difficulty based on your progress',
          color: '#4facfe',
        },
        {
          icon: <Target size={20} color="white" />,
          title: 'Smart Recommendations',
          description: 'Discover topics based on your interests and goals',
          color: '#fa709a',
        },
      ],
    },
    {
      category: 'Progress & Motivation',
      items: [
        {
          icon: <Trophy size={20} color="white" />,
          title: 'Achievements & Badges',
          description: 'Unlock rewards as you master new concepts',
          color: '#fbbf24',
        },
        {
          icon: <Calendar size={20} color="white" />,
          title: 'Learning Streaks',
          description: 'Build consistent study habits with daily goals',
          color: '#4ade80',
        },
        {
          icon: <Bell size={20} color="white" />,
          title: 'Smart Reminders',
          description: 'Get notified when it&apos;s time to review or learn',
          color: '#f59e0b',
        },
      ],
    },
    {
      category: 'Community & Sharing',
      items: [
        {
          icon: <Users size={20} color="white" />,
          title: 'Study Groups',
          description: 'Connect with learners who share your interests',
          color: '#8b5cf6',
        },
        {
          icon: <MessageSquare size={20} color="white" />,
          title: 'Discussion Forums',
          description: 'Ask questions and help others in topic discussions',
          color: '#06b6d4',
        },
        {
          icon: <Share2 size={20} color="white" />,
          title: 'Share Progress',
          description: 'Showcase your achievements and inspire others',
          color: '#ef4444',
        },
      ],
    },
  ];

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
      marginBottom: '12px',
    } as CSSProperties,
    subtitle: {
      fontSize: '16px',
      color: '#666',
      lineHeight: '1.6',
    } as CSSProperties,
    categoriesContainer: {
      display: 'flex',
      flexDirection: 'column',
      gap: '32px',
    } as CSSProperties,
    category: {
      marginBottom: '24px',
    } as CSSProperties,
    categoryTitle: {
      fontSize: '18px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '16px',
      paddingLeft: '8px',
    } as CSSProperties,
    featuresGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
      gap: '16px',
    } as CSSProperties,
    featureCard: {
      padding: '20px',
      background: '#fff',
      borderRadius: '12px',
      border: '1px solid #e6e8ff',
      transition: 'all 0.3s ease',
      cursor: 'pointer',
    } as CSSProperties,
    featureIcon: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '40px',
      height: '40px',
      borderRadius: '10px',
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
    highlightBanner: {
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      padding: '24px',
      borderRadius: '16px',
      textAlign: 'center',
      marginTop: '32px',
    } as CSSProperties,
    bannerTitle: {
      fontSize: '20px',
      fontWeight: 'bold',
      marginBottom: '8px',
    } as CSSProperties,
    bannerSubtitle: {
      fontSize: '14px',
      opacity: 0.9,
    } as CSSProperties,
    mobileFeature: {
      display: 'flex',
      alignItems: 'center',
      gap: '16px',
      background: '#f8f9ff',
      padding: '20px',
      borderRadius: '12px',
      marginTop: '24px',
    } as CSSProperties,
    mobileIcon: {
      width: '48px',
      height: '48px',
      borderRadius: '12px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0,
    } as CSSProperties,
    mobileContent: {
      flex: 1,
    } as CSSProperties,
    mobileTitle: {
      fontSize: '16px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '4px',
    } as CSSProperties,
    mobileDescription: {
      fontSize: '14px',
      color: '#666',
    } as CSSProperties,
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Explore Powerful Features</h2>
        <p style={styles.subtitle}>
          Discover the tools and features that will accelerate your learning journey
        </p>
      </div>

      <div style={styles.categoriesContainer}>
        {features.map((category, categoryIndex) => (
          <div key={categoryIndex} style={styles.category}>
            <h3 style={styles.categoryTitle}>{category.category}</h3>
            <div style={styles.featuresGrid}>
              {category.items.map((feature, featureIndex) => (
                <div
                  key={featureIndex}
                  style={styles.featureCard}
                  onMouseEnter={(e) => {
                    (e.target as HTMLElement).style.transform = 'translateY(-4px)';
                    (e.target as HTMLElement).style.boxShadow = '0 8px 25px rgba(0,0,0,0.1)';
                  }}
                  onMouseLeave={(e) => {
                    (e.target as HTMLElement).style.transform = 'translateY(0)';
                    (e.target as HTMLElement).style.boxShadow = 'none';
                  }}
                >
                  <div style={{ ...styles.featureIcon, background: feature.color }}>
                    {feature.icon}
                  </div>
                  <h4 style={styles.featureTitle}>{feature.title}</h4>
                  <p style={styles.featureDescription}>{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Mobile App Feature */}
      <div style={styles.mobileFeature}>
        <div style={styles.mobileIcon}>
          <Smartphone size={24} color="white" />
        </div>
        <div style={styles.mobileContent}>
          <div style={styles.mobileTitle}>Learn Anywhere, Anytime</div>
          <div style={styles.mobileDescription}>
            Access your learning content on any device. Continue your progress seamlessly between desktop and mobile.
          </div>
        </div>
      </div>

      {/* Highlight Banner */}
      <div style={styles.highlightBanner}>
        <div style={styles.bannerTitle}>
          🚀 Ready to Transform Your Learning?
        </div>
        <div style={styles.bannerSubtitle}>
          You now have everything you need to start your journey to mastering human knowledge
        </div>
      </div>
    </div>
  );
};