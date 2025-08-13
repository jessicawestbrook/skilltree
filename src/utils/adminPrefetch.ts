// Utility for prefetching admin routes and their data
export const prefetchAdminRoute = async (route: string) => {
  if (typeof window === 'undefined') return;

  // Use requestIdleCallback for better performance
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      // Prefetch the route
      import(`@/app/admin${route}/page`).catch(() => {
        // Silently fail if route doesn't exist
      });
    });
  }
};

// Prefetch multiple admin routes
export const prefetchAdminRoutes = (routes: string[]) => {
  routes.forEach(route => prefetchAdminRoute(route));
};

// Bundle splitting configuration for admin routes
export const adminRouteConfig = {
  // Critical routes that should be loaded immediately
  critical: ['/admin'],
  
  // Secondary routes that can be lazy loaded
  secondary: [
    '/admin/content',
    '/admin/questions',
    '/admin/users',
  ],
  
  // Tertiary routes that are rarely used
  tertiary: [
    '/admin/upload',
    '/admin/settings',
    '/admin/nodes',
    '/admin/paths',
  ]
};

// Preload critical admin assets
export const preloadCriticalAdminAssets = () => {
  if (typeof window === 'undefined') return;
  
  // Preload critical routes during idle time
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      adminRouteConfig.critical.forEach(route => {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = route;
        document.head.appendChild(link);
      });
    });
  }
};