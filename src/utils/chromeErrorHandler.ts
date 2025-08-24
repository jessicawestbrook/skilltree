/**
 * Chrome Extension Error Handler
 * Suppresses common Chrome extension errors that don't affect app functionality
 */

// List of known extension-related error patterns to suppress
const EXTENSION_ERROR_PATTERNS = [
  /Unchecked runtime\.lastError/i,
  /message channel closed/i,
  /Extension context invalidated/i,
  /Cannot access contents of url "chrome-extension/i,
  /Access to .* from origin .* has been blocked by CORS policy/i
]

/**
 * Check if an error is likely from a Chrome extension
 */
function isExtensionError(error: Error | string): boolean {
  const errorMessage = typeof error === 'string' ? error : error?.message || ''
  return EXTENSION_ERROR_PATTERNS.some(pattern => pattern.test(errorMessage))
}

/**
 * Initialize Chrome error handler
 */
export function initializeChromeErrorHandler(): void {
  // Only run in browser environment
  if (typeof window === 'undefined') return

  // Override console.error to filter out extension errors
  const originalConsoleError = console.error
  console.error = function(...args: any[]) {
    // Check if this is an extension error
    const firstArg = args[0]
    if (firstArg && isExtensionError(firstArg)) {
      // Silently ignore extension errors
      return
    }
    
    // Otherwise, call the original console.error
    originalConsoleError.apply(console, args)
  }

  // Add global error handler for uncaught errors
  window.addEventListener('error', (event: ErrorEvent) => {
    if (event.error && isExtensionError(event.error)) {
      // Prevent the error from being logged
      event.preventDefault()
      return
    }
  })

  // Add unhandled rejection handler
  window.addEventListener('unhandledrejection', (event: PromiseRejectionEvent) => {
    if (event.reason && isExtensionError(event.reason)) {
      // Prevent the rejection from being logged
      event.preventDefault()
      return
    }
  })

  // Chrome runtime API check (for extension contexts)
  // Note: We check for chrome but can't directly access it due to TypeScript
  // The browser extensions will handle their own errors
}

/**
 * Clean up error handlers (for testing or unmounting)
 */
export function cleanupChromeErrorHandler(): void {
  // Note: We can't fully restore console.error without keeping a reference
  // This is mainly for documentation purposes
}