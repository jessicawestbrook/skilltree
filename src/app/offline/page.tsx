'use client';

import React, { useEffect, useState } from 'react';
import { WifiOff, RefreshCw, Download, BookOpen, Clock, Home } from 'lucide-react';

export default function OfflinePage() {
  const [isOnline, setIsOnline] = useState(false);
  const [retryAttempts, setRetryAttempts] = useState(0);

  useEffect(() => {
    // Check initial online status
    setIsOnline(navigator.onLine);

    // Listen for online/offline events
    const handleOnline = () => {
      setIsOnline(true);
      setRetryAttempts(0);
    };
    
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const handleRetry = async () => {
    setRetryAttempts(prev => prev + 1);
    
    try {
      // Try to fetch a small resource to test connectivity
      const response = await fetch('/manifest.json', { 
        cache: 'no-cache',
        method: 'HEAD'
      });
      
      if (response.ok) {
        // Connection restored, redirect to home
        window.location.href = '/';
      }
    } catch {
      console.log('Still offline, retry failed');
    }
  };

  const handleGoHome = () => {
    window.location.href = '/';
  };

  if (isOnline) {
    // Auto-redirect when connection is restored
    setTimeout(() => {
      window.location.href = '/';
    }, 1000);
  }

  const styles = {
    container: {
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px',
      fontFamily: 'system-ui, -apple-system, sans-serif',
    },
    card: {
      background: 'white',
      borderRadius: '20px',
      padding: '60px 40px',
      maxWidth: '500px',
      width: '100%',
      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
      textAlign: 'center' as const,
    },
    iconContainer: {
      marginBottom: '30px',
      display: 'flex',
      justifyContent: 'center',
    },
    title: {
      fontSize: '28px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '20px',
    },
    subtitle: {
      fontSize: '18px',
      color: '#666',
      marginBottom: '30px',
      lineHeight: '1.6',
    },
    message: {
      fontSize: '16px',
      color: '#777',
      lineHeight: '1.6',
      marginBottom: '40px',
    },
    buttonContainer: {
      display: 'flex',
      gap: '12px',
      justifyContent: 'center',
      flexWrap: 'wrap' as const,
      marginBottom: '40px',
    },
    button: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      padding: '12px 24px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      border: 'none',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: 'bold',
      cursor: 'pointer',
      transition: 'transform 0.2s ease',
      textDecoration: 'none',
    },
    buttonSecondary: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      padding: '12px 24px',
      backgroundColor: '#6c757d',
      color: 'white',
      border: 'none',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: 'bold',
      cursor: 'pointer',
      transition: 'transform 0.2s ease',
      textDecoration: 'none',
    },
    featureList: {
      textAlign: 'left' as const,
      backgroundColor: '#f8f9fa',
      borderRadius: '12px',
      padding: '24px',
      marginTop: '20px',
    },
    featureItem: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      marginBottom: '16px',
      fontSize: '14px',
      color: '#555',
    },
    statusBadge: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      padding: '8px 16px',
      borderRadius: '20px',
      fontSize: '14px',
      fontWeight: 'bold',
      marginBottom: '20px',
      backgroundColor: isOnline ? '#d4edda' : '#f8d7da',
      color: isOnline ? '#155724' : '#721c24',
      border: `1px solid ${isOnline ? '#c3e6cb' : '#f5c6cb'}`,
    },
    retryInfo: {
      fontSize: '12px',
      color: '#999',
      marginTop: '20px',
    },
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.iconContainer}>
          {isOnline ? (
            <div style={{ color: '#28a745' }}>
              <RefreshCw size={64} />
            </div>
          ) : (
            <WifiOff size={64} color="#dc3545" />
          )}
        </div>

        <div style={styles.statusBadge}>
          {isOnline ? (
            <>
              <RefreshCw size={16} />
              Connection Restored
            </>
          ) : (
            <>
              <WifiOff size={16} />
              You&apos;re Offline
            </>
          )}
        </div>

        <h1 style={styles.title}>
          {isOnline ? 'Back Online!' : 'No Internet Connection'}
        </h1>

        {isOnline ? (
          <div>
            <p style={styles.subtitle}>
              Great! Your connection has been restored. Redirecting you back to NeuroQuest...
            </p>
          </div>
        ) : (
          <div>
            <p style={styles.subtitle}>
              Don&apos;t worry! You can still use NeuroQuest with limited functionality.
            </p>

            <p style={styles.message}>
              Your progress will be saved locally and synced when you&apos;re back online.
            </p>

            <div style={styles.buttonContainer}>
              <button onClick={handleRetry} style={styles.button}>
                <RefreshCw size={20} />
                Try Again
              </button>
              
              <button onClick={handleGoHome} style={styles.buttonSecondary}>
                <Home size={20} />
                Go Home
              </button>
            </div>

            <div style={styles.featureList}>
              <h3 style={{ marginBottom: '16px', color: '#2a2a2a' }}>
                Available Offline:
              </h3>
              
              <div style={styles.featureItem}>
                <BookOpen size={20} color="#667eea" />
                <span>Previously downloaded content</span>
              </div>
              
              <div style={styles.featureItem}>
                <Download size={20} color="#667eea" />
                <span>Cached learning materials</span>
              </div>
              
              <div style={styles.featureItem}>
                <Clock size={20} color="#667eea" />
                <span>Progress tracking (will sync later)</span>
              </div>
            </div>

            {retryAttempts > 0 && (
              <div style={styles.retryInfo}>
                Retry attempts: {retryAttempts}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}