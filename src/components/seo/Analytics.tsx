'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { initGA, initGTM, trackPageView, isAnalyticsEnabled } from '../../utils/seo/analytics';

export function Analytics() {
  const pathname = usePathname();

  useEffect(() => {
    // Initialize analytics on mount
    if (isAnalyticsEnabled()) {
      initGA();
      initGTM();
    }
  }, []);

  useEffect(() => {
    // Track page views on route changes
    if (isAnalyticsEnabled()) {
      trackPageView(window.location.href);
    }
  }, [pathname]);

  return null; // This component doesn't render anything visible
}

export default Analytics;