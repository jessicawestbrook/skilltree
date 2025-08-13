'use client';

import React, { useState, useEffect } from 'react';
import { Download, X, Smartphone, Monitor, Zap, Wifi } from 'lucide-react';

interface BeforeInstallPromptEvent extends Event {
  readonly platforms: string[];
  readonly userChoice: Promise<{
    outcome: 'accepted' | 'dismissed';
    platform: string;
  }>;
  prompt(): Promise<void>;
}

declare global {
  interface WindowEventMap {
    beforeinstallprompt: BeforeInstallPromptEvent;
  }
}

interface PWAInstallPromptProps {
  onInstall?: () => void;
  onDismiss?: () => void;
}

export const PWAInstallPrompt: React.FC<PWAInstallPromptProps> = ({
  onInstall,
  onDismiss,
}) => {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [showPrompt, setShowPrompt] = useState(false);
  const [isIOS, setIsIOS] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);
  const [hasBeenDismissed, setHasBeenDismissed] = useState(false);

  useEffect(() => {
    // Check if already installed
    if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
      return;
    }

    // Check if running on iOS
    const iOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    setIsIOS(iOS);

    // Check if user has previously dismissed the prompt
    const dismissed = localStorage.getItem('pwa-install-dismissed');
    if (dismissed) {
      const dismissedDate = new Date(dismissed);
      const now = new Date();
      const daysSinceDismissed = Math.floor((now.getTime() - dismissedDate.getTime()) / (1000 * 60 * 60 * 24));
      
      // Show again after 7 days
      if (daysSinceDismissed < 7) {
        setHasBeenDismissed(true);
        return;
      }
    }

    const handleBeforeInstallPrompt = (e: BeforeInstallPromptEvent) => {
      // Prevent the mini-infobar from appearing on mobile
      e.preventDefault();
      
      // Stash the event so it can be triggered later
      setDeferredPrompt(e);
      
      // Show our custom install prompt after a delay
      setTimeout(() => {
        setShowPrompt(true);
      }, 3000); // Show after 3 seconds
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    // Listen for app installed event
    window.addEventListener('appinstalled', () => {
      setIsInstalled(true);
      setShowPrompt(false);
      onInstall?.();
    });

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, [onInstall]);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    // Show the install prompt
    deferredPrompt.prompt();

    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.userChoice;

    if (outcome === 'accepted') {
      console.log('User accepted the install prompt');
      onInstall?.();
    } else {
      console.log('User dismissed the install prompt');
      handleDismiss();
    }

    // Reset the deferred prompt
    setDeferredPrompt(null);
    setShowPrompt(false);
  };

  const handleDismiss = () => {
    setShowPrompt(false);
    setHasBeenDismissed(true);
    
    // Remember that user dismissed the prompt
    localStorage.setItem('pwa-install-dismissed', new Date().toISOString());
    
    onDismiss?.();
  };

  // Don't show if already installed, dismissed recently, or not supported
  if (isInstalled || hasBeenDismissed || (!deferredPrompt && !isIOS) || !showPrompt) {
    return null;
  }

  const styles = {
    overlay: {
      position: 'fixed' as const,
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px',
    },
    modal: {
      backgroundColor: 'white',
      borderRadius: '20px',
      padding: '40px',
      maxWidth: '450px',
      width: '100%',
      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
      position: 'relative' as const,
    },
    closeButton: {
      position: 'absolute' as const,
      top: '20px',
      right: '20px',
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      color: '#999',
      padding: '8px',
      borderRadius: '50%',
      transition: 'background-color 0.2s ease',
    },
    header: {
      textAlign: 'center' as const,
      marginBottom: '30px',
    },
    icon: {
      marginBottom: '20px',
    },
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '12px',
    },
    subtitle: {
      fontSize: '16px',
      color: '#666',
      lineHeight: '1.5',
    },
    features: {
      marginBottom: '30px',
    },
    featureItem: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      marginBottom: '16px',
      fontSize: '14px',
      color: '#555',
    },
    buttons: {
      display: 'flex',
      gap: '12px',
      justifyContent: 'center',
    },
    installButton: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '15px 30px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      border: 'none',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: 'bold',
      cursor: 'pointer',
      transition: 'transform 0.2s ease',
    },
    laterButton: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '15px 30px',
      backgroundColor: '#f8f9fa',
      color: '#6c757d',
      border: '1px solid #dee2e6',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: 'bold',
      cursor: 'pointer',
      transition: 'all 0.2s ease',
    },
    iosInstructions: {
      backgroundColor: '#f8f9fa',
      borderRadius: '12px',
      padding: '20px',
      marginTop: '20px',
      fontSize: '14px',
      color: '#555',
      lineHeight: '1.5',
    },
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <button
          onClick={handleDismiss}
          style={styles.closeButton}
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#f0f0f0'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
        >
          <X size={20} />
        </button>

        <div style={styles.header}>
          <div style={styles.icon}>
            <Download size={48} color="#667eea" />
          </div>
          <h2 style={styles.title}>Install NeuroQuest</h2>
          <p style={styles.subtitle}>
            Get the full app experience with offline access and faster loading
          </p>
        </div>

        <div style={styles.features}>
          <div style={styles.featureItem}>
            <Zap size={20} color="#667eea" />
            <span>Lightning-fast performance</span>
          </div>
          <div style={styles.featureItem}>
            <Wifi size={20} color="#667eea" />
            <span>Works offline</span>
          </div>
          <div style={styles.featureItem}>
            {isIOS ? <Smartphone size={20} color="#667eea" /> : <Monitor size={20} color="#667eea" />}
            <span>Native app experience</span>
          </div>
        </div>

        {isIOS ? (
          <div>
            <div style={styles.iosInstructions}>
              <strong>To install on iOS:</strong>
              <br />1. Tap the Share button in Safari
              <br />2. Scroll down and tap &quot;Add to Home Screen&quot;
              <br />3. Tap &quot;Add&quot; to install NeuroQuest
            </div>
            <div style={styles.buttons}>
              <button onClick={handleDismiss} style={styles.laterButton}>
                Maybe Later
              </button>
            </div>
          </div>
        ) : (
          <div style={styles.buttons}>
            <button onClick={handleInstallClick} style={styles.installButton}>
              <Download size={20} />
              Install App
            </button>
            <button onClick={handleDismiss} style={styles.laterButton}>
              Maybe Later
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PWAInstallPrompt;