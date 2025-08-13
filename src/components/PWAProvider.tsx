'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { usePWA, useServiceWorker, useOfflineStorage } from '@/hooks/usePWA';
import PWAInstallPrompt from './PWAInstallPrompt';
import { developmentCleanup } from '@/utils/clearServiceWorkers';

interface PWAContextType {
  isInstalled: boolean;
  isInstallable: boolean;
  isOnline: boolean;
  isStandalone: boolean;
  isUpdateAvailable: boolean;
  install: () => Promise<boolean>;
  updateApp: () => void;
  storeQuizSubmission: (submission: unknown) => Promise<boolean>;
  storeProgressUpdate: (progress: unknown) => Promise<boolean>;
  storeContent: (content: unknown) => Promise<boolean>;
  getStoredContent: (id: string) => Promise<unknown>;
}

const PWAContext = createContext<PWAContextType | undefined>(undefined);

export function PWAProvider({ children }: { children: React.ReactNode }) {
  const [showInstallPrompt, setShowInstallPrompt] = useState(false);
  const [installPromptDismissed, setInstallPromptDismissed] = useState(false);
  
  const pwa = usePWA();
  const serviceWorker = useServiceWorker();
  const offlineStorage = useOfflineStorage();

  useEffect(() => {
    // Show install prompt if installable and not dismissed
    if (pwa.isInstallable && !pwa.isInstalled && !installPromptDismissed) {
      const timer = setTimeout(() => {
        setShowInstallPrompt(true);
      }, 5000); // Show after 5 seconds

      return () => clearTimeout(timer);
    }
  }, [pwa.isInstallable, pwa.isInstalled, installPromptDismissed]);

  useEffect(() => {
    // Handle development mode
    if (process.env.NODE_ENV === 'development') {
      console.log('[PWA] Development mode detected');
      developmentCleanup().then(() => {
        console.log('[PWA] Service Worker registration skipped in development mode');
      });
      return;
    }

    // Register service worker and handle updates
    if ('serviceWorker' in navigator) {
      // Check if service worker file exists first
      fetch('/sw.js', { method: 'HEAD' })
        .then(response => {
          if (response.ok) {
            return navigator.serviceWorker.register('/sw.js');
          } else {
            throw new Error(`Service worker not found: ${response.status}`);
          }
        })
        .then((registration) => {
          console.log('[PWA] Service Worker registered successfully');
          
          // Check for updates every 30 seconds when page is visible
          const checkForUpdates = () => {
            if (document.visibilityState === 'visible') {
              registration.update();
            }
          };

          document.addEventListener('visibilitychange', checkForUpdates);
          const interval = setInterval(checkForUpdates, 30000);

          return () => {
            document.removeEventListener('visibilitychange', checkForUpdates);
            clearInterval(interval);
          };
        })
        .catch((error) => {
          console.error('[PWA] Service Worker registration failed:', error);
        });
    }
  }, []);

  useEffect(() => {
    // Handle app updates
    if (serviceWorker.isUpdateAvailable) {
      // Show update notification or auto-update
      if (confirm('A new version of NeuroQuest is available. Update now?')) {
        serviceWorker.updateServiceWorker();
      }
    }
  }, [serviceWorker.isUpdateAvailable, serviceWorker.updateServiceWorker]);

  useEffect(() => {
    // Handle offline/online status
    const handleOnlineStatus = () => {
      if (navigator.onLine) {
        console.log('[PWA] Back online - syncing data...');
        // Trigger background sync if available
        if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
          navigator.serviceWorker.ready.then((registration) => {
            const syncRegistration = registration as ServiceWorkerRegistration & { sync?: { register: (tag: string) => Promise<void> } };
            syncRegistration.sync?.register('background-sync');
          });
        }
      } else {
        console.log('[PWA] Gone offline - using cached data');
      }
    };

    window.addEventListener('online', handleOnlineStatus);
    window.addEventListener('offline', handleOnlineStatus);

    return () => {
      window.removeEventListener('online', handleOnlineStatus);
      window.removeEventListener('offline', handleOnlineStatus);
    };
  }, []);

  const handleInstall = async () => {
    const success = await pwa.install();
    if (success) {
      setShowInstallPrompt(false);
    }
  };

  const handleInstallDismiss = () => {
    setShowInstallPrompt(false);
    setInstallPromptDismissed(true);
  };

  const contextValue: PWAContextType = {
    isInstalled: pwa.isInstalled,
    isInstallable: pwa.isInstallable,
    isOnline: pwa.isOnline,
    isStandalone: pwa.isStandalone,
    isUpdateAvailable: serviceWorker.isUpdateAvailable,
    install: pwa.install,
    updateApp: serviceWorker.updateServiceWorker,
    storeQuizSubmission: offlineStorage.storeQuizSubmission,
    storeProgressUpdate: offlineStorage.storeProgressUpdate,
    storeContent: offlineStorage.storeContent,
    getStoredContent: offlineStorage.getStoredContent,
  };

  return (
    <PWAContext.Provider value={contextValue}>
      {children}
      
      {/* Install Prompt */}
      {showInstallPrompt && (
        <PWAInstallPrompt
          onInstall={handleInstall}
          onDismiss={handleInstallDismiss}
        />
      )}
      
      {/* Update Notification */}
      {serviceWorker.isUpdateAvailable && (
        <UpdateNotification onUpdate={serviceWorker.updateServiceWorker} />
      )}
      
      {/* Offline Indicator */}
      {!pwa.isOnline && <OfflineIndicator />}
    </PWAContext.Provider>
  );
}

// Update Notification Component
function UpdateNotification({ onUpdate }: { onUpdate: () => void }) {
  const [show, setShow] = useState(true);

  if (!show) return null;

  const styles = {
    container: {
      position: 'fixed' as const,
      top: '20px',
      right: '20px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      padding: '16px 20px',
      borderRadius: '12px',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)',
      zIndex: 1000,
      maxWidth: '300px',
      fontSize: '14px',
    },
    title: {
      fontWeight: 'bold',
      marginBottom: '8px',
    },
    message: {
      marginBottom: '12px',
      lineHeight: '1.4',
    },
    buttons: {
      display: 'flex',
      gap: '8px',
    },
    button: {
      padding: '8px 16px',
      border: 'none',
      borderRadius: '8px',
      fontSize: '12px',
      fontWeight: 'bold',
      cursor: 'pointer',
      transition: 'opacity 0.2s ease',
    },
    updateButton: {
      backgroundColor: 'white',
      color: '#667eea',
    },
    laterButton: {
      backgroundColor: 'rgba(255, 255, 255, 0.2)',
      color: 'white',
    },
  };

  return (
    <div style={styles.container}>
      <div style={styles.title}>Update Available</div>
      <div style={styles.message}>
        A new version of NeuroQuest is ready. Update now for the latest features and improvements.
      </div>
      <div style={styles.buttons}>
        <button
          onClick={onUpdate}
          style={{ ...styles.button, ...styles.updateButton }}
        >
          Update Now
        </button>
        <button
          onClick={() => setShow(false)}
          style={{ ...styles.button, ...styles.laterButton }}
        >
          Later
        </button>
      </div>
    </div>
  );
}

// Offline Indicator Component
function OfflineIndicator() {
  const styles = {
    container: {
      position: 'fixed' as const,
      bottom: '20px',
      left: '20px',
      right: '20px',
      background: '#dc3545',
      color: 'white',
      padding: '12px 16px',
      borderRadius: '8px',
      fontSize: '14px',
      fontWeight: 'bold',
      textAlign: 'center' as const,
      zIndex: 999,
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
    },
  };

  return (
    <div style={styles.container}>
      📡 You&apos;re offline - Some features may be limited
    </div>
  );
}

export function usePWAContext() {
  const context = useContext(PWAContext);
  if (context === undefined) {
    throw new Error('usePWAContext must be used within a PWAProvider');
  }
  return context;
}

export default PWAProvider;