'use client';

import React, { useState, useEffect, CSSProperties } from 'react';
import { Bell, Clock, Trophy, Users, Sparkles, Save, Check } from 'lucide-react';
import { NotificationPermission } from './NotificationPermission';
import { createClient } from '@/lib/supabase-client';
import { useAuth } from '../contexts/AuthContext';

interface NotificationPreferences {
  daily_reminders: boolean;
  achievement_alerts: boolean;
  streak_notifications: boolean;
  friend_activity: boolean;
  new_content: boolean;
  reminder_time: string;
}

export const NotificationSettings: React.FC = () => {
  const { user } = useAuth();
  const [preferences, setPreferences] = useState<NotificationPreferences>({
    daily_reminders: true,
    achievement_alerts: true,
    streak_notifications: true,
    friend_activity: true,
    new_content: true,
    reminder_time: '09:00'
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  useEffect(() => {
    loadPreferences();
  }, [user]);

  const loadPreferences = async () => {
    if (!user) return;

    try {
      const supabase = createClient();
      const { data, error } = await supabase
        .from('user_notification_preferences')
        .select('*')
        .eq('user_id', user.id)
        .single();

      if (data && !error) {
        setPreferences(data);
      }
    } catch (error) {
      console.error('Failed to load preferences:', error);
    }
  };

  const savePreferences = async () => {
    if (!user) return;

    setIsLoading(true);
    try {
      const supabase = createClient();
      const { error } = await supabase
        .from('user_notification_preferences')
        .upsert({
          user_id: user.id,
          ...preferences,
          updated_at: new Date().toISOString()
        }, {
          onConflict: 'user_id'
        });

      if (!error) {
        setIsSaved(true);
        setTimeout(() => setIsSaved(false), 3000);
      }
    } catch (error) {
      console.error('Failed to save preferences:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggle = (key: keyof NotificationPreferences) => {
    if (key === 'reminder_time') return;
    setPreferences(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const handleTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPreferences(prev => ({
      ...prev,
      reminder_time: e.target.value
    }));
  };

  const styles = {
    container: {
      maxWidth: '600px',
      margin: '0 auto',
      padding: '20px'
    } as CSSProperties,
    header: {
      marginBottom: '32px'
    } as CSSProperties,
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '8px'
    } as CSSProperties,
    subtitle: {
      fontSize: '14px',
      color: '#666'
    } as CSSProperties,
    section: {
      marginBottom: '24px'
    } as CSSProperties,
    sectionTitle: {
      fontSize: '16px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '16px',
      paddingBottom: '8px',
      borderBottom: '2px solid #f0f0f0'
    } as CSSProperties,
    preferenceItem: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '16px',
      background: '#f8f9fa',
      borderRadius: '8px',
      marginBottom: '12px',
      transition: 'background 0.2s'
    } as CSSProperties,
    preferenceInfo: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      flex: 1
    } as CSSProperties,
    preferenceIcon: {
      width: '40px',
      height: '40px',
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea, #764ba2)'
    } as CSSProperties,
    preferenceText: {
      flex: 1
    } as CSSProperties,
    preferenceName: {
      fontSize: '14px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '4px'
    } as CSSProperties,
    preferenceDescription: {
      fontSize: '12px',
      color: '#666'
    } as CSSProperties,
    toggle: {
      position: 'relative',
      width: '48px',
      height: '24px',
      background: '#ccc',
      borderRadius: '12px',
      cursor: 'pointer',
      transition: 'background 0.3s'
    } as CSSProperties,
    toggleActive: {
      background: 'linear-gradient(135deg, #667eea, #764ba2)'
    } as CSSProperties,
    toggleKnob: {
      position: 'absolute',
      top: '2px',
      left: '2px',
      width: '20px',
      height: '20px',
      background: 'white',
      borderRadius: '50%',
      transition: 'transform 0.3s',
      boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
    } as CSSProperties,
    toggleKnobActive: {
      transform: 'translateX(24px)'
    } as CSSProperties,
    timeInput: {
      padding: '8px 12px',
      borderRadius: '8px',
      border: '1px solid #e0e0e0',
      fontSize: '14px',
      color: '#2a2a2a'
    } as CSSProperties,
    saveButton: {
      padding: '12px 24px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      fontSize: '14px',
      fontWeight: 'bold',
      cursor: isLoading ? 'not-allowed' : 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      margin: '32px auto 0',
      opacity: isLoading ? 0.7 : 1,
      transition: 'all 0.3s'
    } as CSSProperties,
    savedMessage: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      color: '#4caf50',
      fontSize: '14px',
      marginTop: '16px',
      justifyContent: 'center'
    } as CSSProperties
  };

  const notificationTypes = [
    {
      key: 'daily_reminders',
      icon: <Clock size={20} color="white" />,
      name: 'Daily Reminders',
      description: 'Get reminded to continue your learning journey'
    },
    {
      key: 'achievement_alerts',
      icon: <Trophy size={20} color="white" />,
      name: 'Achievements',
      description: 'Celebrate when you unlock new achievements'
    },
    {
      key: 'streak_notifications',
      icon: <Sparkles size={20} color="white" />,
      name: 'Streak Milestones',
      description: 'Keep your learning streak alive with timely alerts'
    },
    {
      key: 'friend_activity',
      icon: <Users size={20} color="white" />,
      name: 'Friend Activity',
      description: 'Stay updated on your friends\' progress'
    },
    {
      key: 'new_content',
      icon: <Bell size={20} color="white" />,
      name: 'New Content',
      description: 'Discover new learning materials and challenges'
    }
  ];

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Notification Settings</h2>
        <p style={styles.subtitle}>
          Customize how and when you receive notifications
        </p>
      </div>

      {/* Push Notification Permission */}
      <NotificationPermission embedded={true} />

      {/* Notification Preferences */}
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Notification Types</h3>
        
        {notificationTypes.map(type => (
          <div key={type.key} style={styles.preferenceItem}>
            <div style={styles.preferenceInfo}>
              <div style={styles.preferenceIcon}>
                {type.icon}
              </div>
              <div style={styles.preferenceText}>
                <div style={styles.preferenceName}>{type.name}</div>
                <div style={styles.preferenceDescription}>{type.description}</div>
              </div>
            </div>
            
            <div
              style={{
                ...styles.toggle,
                ...(preferences[type.key as keyof NotificationPreferences] ? styles.toggleActive : {})
              }}
              onClick={() => handleToggle(type.key as keyof NotificationPreferences)}
            >
              <div
                style={{
                  ...styles.toggleKnob,
                  ...(preferences[type.key as keyof NotificationPreferences] ? styles.toggleKnobActive : {})
                }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Reminder Time */}
      {preferences.daily_reminders && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>Reminder Time</h3>
          <div style={styles.preferenceItem}>
            <div style={styles.preferenceInfo}>
              <div style={styles.preferenceIcon}>
                <Clock size={20} color="white" />
              </div>
              <div style={styles.preferenceText}>
                <div style={styles.preferenceName}>Daily Reminder Time</div>
                <div style={styles.preferenceDescription}>
                  Choose when to receive your daily learning reminder
                </div>
              </div>
            </div>
            
            <input
              type="time"
              value={preferences.reminder_time}
              onChange={handleTimeChange}
              style={styles.timeInput}
            />
          </div>
        </div>
      )}

      {/* Save Button */}
      <button
        onClick={savePreferences}
        disabled={isLoading}
        style={styles.saveButton}
      >
        <Save size={16} />
        {isLoading ? 'Saving...' : 'Save Preferences'}
      </button>

      {isSaved && (
        <div style={styles.savedMessage}>
          <Check size={16} />
          Preferences saved successfully!
        </div>
      )}
    </div>
  );
};