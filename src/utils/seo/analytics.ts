// Google Analytics 4 (GA4) integration
export const GA_TRACKING_ID = process.env.NEXT_PUBLIC_GA_ID || '';
export const GTM_ID = process.env.NEXT_PUBLIC_GTM_ID || '';

// Check if analytics should be enabled
export const isAnalyticsEnabled = () => {
  return typeof window !== 'undefined' && 
         process.env.NODE_ENV === 'production' && 
         (GA_TRACKING_ID || GTM_ID);
};

// Initialize Google Analytics
export const initGA = () => {
  if (!isAnalyticsEnabled() || !GA_TRACKING_ID) return;

  // Load GA4 script
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_TRACKING_ID}`;
  document.head.appendChild(script);

  // Initialize gtag
  (window as any).dataLayer = (window as any).dataLayer || [];
  (window as any).gtag = function gtag(...args: unknown[]) {
    (window as any).dataLayer.push(args);
  };
  
  (window as any).gtag('js', new Date());
  (window as any).gtag('config', GA_TRACKING_ID, {
    page_title: document.title,
    page_location: window.location.href,
  });
};

// Initialize Google Tag Manager
export const initGTM = () => {
  if (!isAnalyticsEnabled() || !GTM_ID) return;

  // Load GTM script
  const script = document.createElement('script');
  script.innerHTML = `
    (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','${GTM_ID}');
  `;
  document.head.appendChild(script);

  // Add noscript fallback
  const noscript = document.createElement('noscript');
  noscript.innerHTML = `
    <iframe src="https://www.googletagmanager.com/ns.html?id=${GTM_ID}"
            height="0" width="0" style="display:none;visibility:hidden"></iframe>
  `;
  document.body.appendChild(noscript);
};

// Track page views
export const trackPageView = (url: string, title?: string) => {
  if (!isAnalyticsEnabled()) return;

  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('config', GA_TRACKING_ID, {
      page_title: title || document.title,
      page_location: url,
    });
  }
};

// Track custom events
export const trackEvent = (action: string, parameters?: Record<string, any>) => {
  if (!isAnalyticsEnabled()) return;

  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('event', action, parameters);
  }
};

// Learning-specific tracking events
export const trackLearningEvents = {
  // Track when a user starts learning a node
  nodeStarted: (nodeId: string, nodeName: string, domain: string) => {
    trackEvent('node_started', {
      node_id: nodeId,
      node_name: nodeName,
      domain: domain,
      event_category: 'Learning',
    });
  },

  // Track when a user completes a node
  nodeCompleted: (nodeId: string, nodeName: string, domain: string, score: number, timeSpent: number) => {
    trackEvent('node_completed', {
      node_id: nodeId,
      node_name: nodeName,
      domain: domain,
      score: score,
      time_spent: timeSpent,
      event_category: 'Learning',
      value: score, // Use score as the event value
    });
  },

  // Track quiz attempts
  quizAttempted: (nodeId: string, questionIndex: number, isCorrect: boolean) => {
    trackEvent('quiz_question_answered', {
      node_id: nodeId,
      question_index: questionIndex,
      is_correct: isCorrect,
      event_category: 'Engagement',
    });
  },

  // Track user progression milestones
  milestoneReached: (milestone: string, value: number) => {
    trackEvent('milestone_reached', {
      milestone_type: milestone,
      milestone_value: value,
      event_category: 'Achievement',
      value: value,
    });
  },

  // Track search usage
  searchPerformed: (query: string, resultsCount: number) => {
    trackEvent('search', {
      search_term: query,
      results_count: resultsCount,
      event_category: 'Engagement',
    });
  },

  // Track feature usage
  featureUsed: (feature: string, context?: string) => {
    trackEvent('feature_used', {
      feature_name: feature,
      context: context,
      event_category: 'Engagement',
    });
  },

  // Track user registration and authentication
  userRegistered: (method: string) => {
    trackEvent('sign_up', {
      method: method,
      event_category: 'User',
    });
  },

  userSignedIn: (method: string) => {
    trackEvent('login', {
      method: method,
      event_category: 'User',
    });
  },

  // Track user engagement duration
  sessionDuration: (duration: number) => {
    trackEvent('session_duration', {
      duration_seconds: duration,
      event_category: 'Engagement',
      value: Math.round(duration / 60), // Convert to minutes
    });
  },

  // Track errors and issues
  errorOccurred: (errorType: string, errorMessage: string, context?: string) => {
    trackEvent('exception', {
      description: `${errorType}: ${errorMessage}`,
      fatal: false,
      context: context,
      event_category: 'Error',
    });
  },
};

// Performance tracking
export const trackPerformance = {
  // Track page load time
  pageLoadTime: (loadTime: number) => {
    trackEvent('page_load_time', {
      load_time_ms: loadTime,
      event_category: 'Performance',
      value: loadTime,
    });
  },

  // Track Core Web Vitals
  webVitals: (metric: string, value: number) => {
    trackEvent('web_vitals', {
      metric_name: metric,
      metric_value: value,
      event_category: 'Performance',
      value: Math.round(value),
    });
  },
};

// Custom dimensions for enhanced tracking
export const setCustomDimensions = (dimensions: Record<string, string>) => {
  if (!isAnalyticsEnabled()) return;

  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('config', GA_TRACKING_ID, {
      custom_map: dimensions,
    });
  }
};

// User properties for cohort analysis
export const setUserProperties = (properties: Record<string, string | number>) => {
  if (!isAnalyticsEnabled()) return;

  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('set', { user_properties: properties });
  }
};

// Consent management for GDPR compliance
export const updateConsentSettings = (adStorage: boolean, analyticsStorage: boolean) => {
  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('consent', 'update', {
      ad_storage: adStorage ? 'granted' : 'denied',
      analytics_storage: analyticsStorage ? 'granted' : 'denied',
    });
  }
};

// Initialize consent with default settings
export const initializeConsent = () => {
  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('consent', 'default', {
      ad_storage: 'denied',
      analytics_storage: 'denied',
      wait_for_update: 500,
    });
  }
};

// Ecommerce tracking (for premium features)
export const trackPurchase = (transactionId: string, value: number, currency: string = 'USD', items: any[] = []) => {
  if (!isAnalyticsEnabled()) return;

  trackEvent('purchase', {
    transaction_id: transactionId,
    value: value,
    currency: currency,
    items: items,
    event_category: 'Ecommerce',
  });
};

// Social media sharing tracking
export const trackSocialShare = (platform: string, content: string) => {
  trackEvent('share', {
    method: platform,
    content_type: 'learning_node',
    item_id: content,
    event_category: 'Social',
  });
};

// Export everything for easy imports
export default {
  initGA,
  initGTM,
  trackPageView,
  trackEvent,
  trackLearningEvents,
  trackPerformance,
  setCustomDimensions,
  setUserProperties,
  updateConsentSettings,
  initializeConsent,
  trackPurchase,
  trackSocialShare,
  isAnalyticsEnabled,
};