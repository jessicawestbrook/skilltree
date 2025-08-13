'use client';

import { useEffect } from 'react';

/**
 * Hook to suppress hydration warnings caused by browser extensions
 * This is specifically for handling Grammarly and other extensions that inject attributes
 */
export const useSuppressHydrationWarning = () => {
  useEffect(() => {
    // Clean up browser extension attributes on mount
    const cleanupExtensionAttributes = () => {
      const body = document.body;
      
      // Remove Grammarly attributes
      body.removeAttribute('data-new-gr-c-s-check-loaded');
      body.removeAttribute('data-gr-ext-installed');
      
      // Remove other common extension attributes
      body.removeAttribute('data-gramm');
      body.removeAttribute('data-gramm_editor');
      body.removeAttribute('data-gr-c-sponsored');
      
      // Clean up any extension-injected styles or elements
      const grammarlyElements = document.querySelectorAll('[data-grammarly-shadow-root]');
      grammarlyElements.forEach(el => el.remove());
    };

    // Run cleanup after a short delay to ensure DOM is ready
    const timeoutId = setTimeout(cleanupExtensionAttributes, 0);
    
    return () => clearTimeout(timeoutId);
  }, []);
};