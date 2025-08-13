'use client';

import React, { useState, useEffect, CSSProperties } from 'react';
import { Bell, BellOff, X, Check, AlertCircle } from 'lucide-react';
import { pushNotificationService } from '../services/pushNotificationService';

interface NotificationPermissionProps {
  onClose?: () => void;
  embedded?: boolean;
}

export const NotificationPermission: React.FC<NotificationPermissionProps> = ({ 
  onClose, 
  embedded = false 
}) => {
  const [permission, setPermission] = useState<NotificationPermission>('default');
  const [isLoading, setIsLoading] = useState(false);
  const [showBanner, setShowBanner] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check current permission status
    const status = pushNotificationService.getPermissionStatus();
    setPermission(status);
    
    // Show banner if permission not granted and not embedded
    if (!embedded && status === 'default') {
      const hasSeenBanner = localStorage.getItem('notification_banner_seen');
      if (!hasSeenBanner) {
        setTimeout(() => setShowBanner(true), 3000); // Show after 3 seconds
      }
    }

    // Initialize push notification service
    pushNotificationService.initialize();
  }, [embedded]);

  const handleEnableNotifications = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await pushNotificationService.requestPermission();
      setPermission(result);
      
      if (result === 'granted') {
        // Test notification
        await pushNotificationService.showLocalNotification({
          title: '🎉 Notifications Enabled!',
          body: 'You\'ll now receive updates about your learning progress',
          tag: 'welcome'
        });
        
        // Mark banner as seen
        localStorage.setItem('notification_banner_seen', 'true');
        
        if (!embedded) {
          setTimeout(() => setShowBanner(false), 2000);
        }
      } else if (result === 'denied') {
        setError('Notifications were blocked. Please enable them in your browser settings.');
      }
    } catch (err) {
      console.error('Failed to enable notifications:', err);
      setError('Failed to enable notifications. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisableNotifications = async () => {
    setIsLoading(true);
    
    try {
      const success = await pushNotificationService.unsubscribeUser();
      if (success) {
        setPermission('default');
      }
    } catch (err) {
      console.error('Failed to disable notifications:', err);
      setError('Failed to disable notifications. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCloseBanner = () => {
    setShowBanner(false);
    localStorage.setItem('notification_banner_seen', 'true');
    if (onClose) onClose();
  };

  const handleTestNotification = async () => {
    await pushNotificationService.showLocalNotification({
      title: '🧠 Test Notification',
      body: 'This is a test notification from NeuroQuest!',
      tag: 'test',
      actions: [
        { action: 'open', title: 'Open App' }
      ]
    });
  };

  const styles = {
    banner: {
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      background: 'white',
      borderRadius: '12px',
      padding: '20px',
      maxWidth: '400px',
      boxShadow: '0 10px 40px rgba(0,0,0,0.15)',
      display: showBanner && !embedded ? 'block' : 'none',
      zIndex: 1000,
      animation: 'slideIn 0.3s ease-out'
    } as CSSProperties,
    embeddedContainer: {
      background: 'white',
      borderRadius: '12px',
      padding: '24px',
      border: '1px solid #e0e0e0',
      marginBottom: '20px'
    } as CSSProperties,
    header: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '16px'
    } as CSSProperties,
    title: {
      fontSize: '18px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      display: 'flex',
      alignItems: 'center',
      gap: '8px'
    } as CSSProperties,
    closeButton: {
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      padding: '4px',
      color: '#999'
    } as CSSProperties,
    content: {
      marginBottom: '20px'
    } as CSSProperties,
    description: {
      fontSize: '14px',
      color: '#666',
      lineHeight: '1.5',
      marginBottom: '16px'
    } as CSSProperties,
    benefits: {
      display: 'flex',
      flexDirection: 'column',
      gap: '8px',
      marginBottom: '16px'
    } as CSSProperties,
    benefit: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontSize: '13px',
      color: '#555'
    } as CSSProperties,
    buttonGroup: {
      display: 'flex',
      gap: '12px'
    } as CSSProperties,
    button: {
      padding: '10px 20px',
      borderRadius: '8px',
      border: 'none',
      fontSize: '14px',
      fontWeight: 'bold',
      cursor: isLoading ? 'not-allowed' : 'pointer',
      transition: 'all 0.3s ease',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      opacity: isLoading ? 0.7 : 1
    } as CSSProperties,
    primaryButton: {
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white'
    } as CSSProperties,
    secondaryButton: {
      background: '#f0f0f0',
      color: '#666'
    } as CSSProperties,
    status: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '12px',
      borderRadius: '8px',
      marginBottom: '16px'
    } as CSSProperties,
    statusEnabled: {
      background: '#e8f5e9',
      color: '#2e7d32'
    } as CSSProperties,
    statusDisabled: {
      background: '#fff3e0',
      color: '#e65100'
    } as CSSProperties,
    statusDenied: {
      background: '#ffebee',
      color: '#c62828'
    } as CSSProperties,
    error: {
      color: '#ff4444',
      fontSize: '13px',
      marginTop: '8px',
      display: 'flex',
      alignItems: 'center',
      gap: '6px'
    } as CSSProperties
  };

  // For embedded mode (settings page)
  if (embedded) {
    return (
      <div style={styles.embeddedContainer}>
        <div style={styles.title}>
          <Bell size={20} />
          Push Notifications
        </div>
        
        {permission === 'granted' && (
          <div style={{ ...styles.status, ...styles.statusEnabled }}>
            <Check size={16} />
            Notifications are enabled
          </div>
        )}
        
        {permission === 'denied' && (
          <div style={{ ...styles.status, ...styles.statusDenied }}>
            <BellOff size={16} />
            Notifications are blocked in browser settings
          </div>
        )}
        
        {permission === 'default' && (
          <div style={{ ...styles.status, ...styles.statusDisabled }}>
            <AlertCircle size={16} />
            Notifications are not enabled
          </div>
        )}

        <p style={styles.description}>
          Stay motivated with timely reminders, achievement celebrations, and learning milestones.
        </p>

        <div style={styles.buttonGroup}>
          {permission !== 'granted' && permission !== 'denied' && (
            <button
              onClick={handleEnableNotifications}
              disabled={isLoading}
              style={{ ...styles.button, ...styles.primaryButton }}
            >
              <Bell size={16} />
              {isLoading ? 'Enabling...' : 'Enable Notifications'}
            </button>
          )}
          
          {permission === 'granted' && (
            <>
              <button
                onClick={handleTestNotification}
                style={{ ...styles.button, ...styles.secondaryButton }}
              >
                Test Notification
              </button>
              <button
                onClick={handleDisableNotifications}
                disabled={isLoading}
                style={{ ...styles.button, ...styles.secondaryButton }}
              >
                <BellOff size={16} />
                {isLoading ? 'Disabling...' : 'Disable'}
              </button>
            </>
          )}
        </div>

        {error && (
          <div style={styles.error}>
            <AlertCircle size={14} />
            {error}
          </div>
        )}
      </div>
    );
  }

  // Banner mode (popup)
  return (
    <div style={styles.banner}>
      <div style={styles.header}>
        <div style={styles.title}>
          <Bell size={20} />
          Enable Notifications
        </div>
        <button onClick={handleCloseBanner} style={styles.closeButton}>
          <X size={18} />
        </button>
      </div>

      <div style={styles.content}>
        <p style={styles.description}>
          Never miss a learning opportunity! Get notified about:
        </p>
        
        <div style={styles.benefits}>
          <div style={styles.benefit}>
            <Check size={14} color="#4caf50" />
            Daily learning reminders
          </div>
          <div style={styles.benefit}>
            <Check size={14} color="#4caf50" />
            Achievement unlocks
          </div>
          <div style={styles.benefit}>
            <Check size={14} color="#4caf50" />
            Streak milestones
          </div>
          <div style={styles.benefit}>
            <Check size={14} color="#4caf50" />
            New content updates
          </div>
        </div>
      </div>

      <div style={styles.buttonGroup}>
        <button
          onClick={handleEnableNotifications}
          disabled={isLoading}
          style={{ ...styles.button, ...styles.primaryButton }}
        >
          <Bell size={16} />
          {isLoading ? 'Enabling...' : 'Enable'}
        </button>
        <button
          onClick={handleCloseBanner}
          style={{ ...styles.button, ...styles.secondaryButton }}
        >
          Maybe Later
        </button>
      </div>

      {error && (
        <div style={styles.error}>
          <AlertCircle size={14} />
          {error}
        </div>
      )}

      <style jsx>{`
        @keyframes slideIn {
          from {
            transform: translateY(100%);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
};