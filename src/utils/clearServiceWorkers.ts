/**
 * Utility to clear existing service workers in development mode
 * This helps prevent conflicts when switching between development and production
 */

export const clearExistingServiceWorkers = async (): Promise<void> => {
  if (typeof window === 'undefined' || !('serviceWorker' in navigator)) {
    return;
  }

  try {
    const registrations = await navigator.serviceWorker.getRegistrations();
    
    for (const registration of registrations) {
      console.log('[SW Cleanup] Unregistering service worker:', registration.scope);
      await registration.unregister();
    }
    
    if (registrations.length > 0) {
      console.log(`[SW Cleanup] Cleared ${registrations.length} service worker(s)`);
      // Optionally reload to ensure clean state
      if (process.env.NODE_ENV === 'development') {
        console.log('[SW Cleanup] Consider refreshing the page for a clean state');
      }
    }
  } catch (error) {
    console.warn('[SW Cleanup] Failed to clear service workers:', error);
  }
};

/**
 * Clear service worker cache in development
 */
export const clearServiceWorkerCache = async (): Promise<void> => {
  if (typeof window === 'undefined' || !('caches' in window)) {
    return;
  }

  try {
    const cacheNames = await caches.keys();
    
    for (const cacheName of cacheNames) {
      console.log('[SW Cleanup] Clearing cache:', cacheName);
      await caches.delete(cacheName);
    }
    
    if (cacheNames.length > 0) {
      console.log(`[SW Cleanup] Cleared ${cacheNames.length} cache(s)`);
    }
  } catch (error) {
    console.warn('[SW Cleanup] Failed to clear caches:', error);
  }
};

/**
 * Development mode cleanup - clears both service workers and caches
 */
export const developmentCleanup = async (): Promise<void> => {
  if (process.env.NODE_ENV !== 'development') {
    return;
  }

  console.log('[SW Cleanup] Running development cleanup...');
  await Promise.all([
    clearExistingServiceWorkers(),
    clearServiceWorkerCache()
  ]);
  console.log('[SW Cleanup] Development cleanup completed');
};