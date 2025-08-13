/**
 * Secure credential storage utilities for remember me functionality
 * Uses localStorage with encryption for sensitive data
 */

interface StoredCredentials {
  email: string;
  rememberedAt: number;
  expiresAt: number;
}

interface FailedAttempts {
  email: string;
  attempts: number;
  lastAttempt: number;
  lockedUntil?: number;
}

const STORAGE_KEY = 'neuroquest_remembered_credentials';
const FAILED_ATTEMPTS_KEY = 'neuroquest_failed_attempts';
const REMEMBER_DURATION = Number.MAX_SAFE_INTEGER; // Indefinite storage
const LOCKOUT_DURATION = 15 * 60 * 1000; // 15 minutes in milliseconds
const MAX_FAILED_ATTEMPTS = 5;

/**
 * Simple encryption/decryption using base64 encoding
 * Note: This is NOT cryptographically secure, but provides basic obfuscation
 * For production, consider using a proper encryption library
 */
const encode = (data: string): string => {
  return btoa(encodeURIComponent(data));
};

const decode = (data: string): string => {
  try {
    return decodeURIComponent(atob(data));
  } catch {
    return '';
  }
};

/**
 * Store user credentials for remember me functionality
 */
export const storeRememberedCredentials = (email: string): void => {
  try {
    const credentials: StoredCredentials = {
      email,
      rememberedAt: Date.now(),
      expiresAt: Date.now() + REMEMBER_DURATION
    };

    const encoded = encode(JSON.stringify(credentials));
    localStorage.setItem(STORAGE_KEY, encoded);
  } catch (error) {
    console.warn('Failed to store remembered credentials:', error);
  }
};

/**
 * Retrieve stored credentials if they haven't expired
 */
export const getRememberedCredentials = (): { email: string } | null => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return null;

    const decoded = decode(stored);
    if (!decoded) return null;

    const credentials: StoredCredentials = JSON.parse(decoded);
    
    // Check if credentials have expired (skip for indefinite storage)
    if (credentials.expiresAt !== Number.MAX_SAFE_INTEGER && Date.now() > credentials.expiresAt) {
      clearRememberedCredentials();
      return null;
    }

    return { email: credentials.email };
  } catch (error) {
    console.warn('Failed to retrieve remembered credentials:', error);
    clearRememberedCredentials();
    return null;
  }
};

/**
 * Clear stored credentials
 */
export const clearRememberedCredentials = (): void => {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.warn('Failed to clear remembered credentials:', error);
  }
};

/**
 * Check if user has any remembered credentials
 */
export const hasRememberedCredentials = (): boolean => {
  return getRememberedCredentials() !== null;
};

/**
 * Update the expiration time for existing credentials
 */
export const refreshRememberedCredentials = (): void => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return;

    const decoded = decode(stored);
    if (!decoded) return;

    const credentials: StoredCredentials = JSON.parse(decoded);
    
    // Keep indefinite expiration
    credentials.expiresAt = REMEMBER_DURATION;
    
    const encoded = encode(JSON.stringify(credentials));
    localStorage.setItem(STORAGE_KEY, encoded);
  } catch (error) {
    console.warn('Failed to refresh remembered credentials:', error);
  }
};

/**
 * Track failed login attempts for rate limiting
 */
export const recordFailedAttempt = (email: string): boolean => {
  try {
    const stored = localStorage.getItem(FAILED_ATTEMPTS_KEY);
    let attempts: FailedAttempts[] = [];
    
    if (stored) {
      const decoded = decode(stored);
      if (decoded) {
        attempts = JSON.parse(decoded);
      }
    }
    
    const now = Date.now();
    const existingIndex = attempts.findIndex(a => a.email === email);
    
    if (existingIndex >= 0) {
      const existing = attempts[existingIndex];
      
      // Check if lockout period has expired
      if (existing.lockedUntil && now < existing.lockedUntil) {
        return true; // Still locked
      }
      
      // Reset if more than an hour has passed since last attempt
      if (now - existing.lastAttempt > 60 * 60 * 1000) {
        existing.attempts = 1;
      } else {
        existing.attempts++;
      }
      
      existing.lastAttempt = now;
      
      // Lock account if too many attempts
      if (existing.attempts >= MAX_FAILED_ATTEMPTS) {
        existing.lockedUntil = now + LOCKOUT_DURATION;
      }
      
      attempts[existingIndex] = existing;
    } else {
      attempts.push({
        email,
        attempts: 1,
        lastAttempt: now
      });
    }
    
    const encoded = encode(JSON.stringify(attempts));
    localStorage.setItem(FAILED_ATTEMPTS_KEY, encoded);
    
    const current = attempts.find(a => a.email === email);
    return !!(current?.lockedUntil && now < current.lockedUntil);
  } catch (error) {
    console.warn('Failed to record failed attempt:', error);
    return false;
  }
};

/**
 * Clear failed attempts for successful login
 */
export const clearFailedAttempts = (email: string): void => {
  try {
    const stored = localStorage.getItem(FAILED_ATTEMPTS_KEY);
    if (!stored) return;
    
    const decoded = decode(stored);
    if (!decoded) return;
    
    const attempts: FailedAttempts[] = JSON.parse(decoded);
    const filtered = attempts.filter(a => a.email !== email);
    
    if (filtered.length === 0) {
      localStorage.removeItem(FAILED_ATTEMPTS_KEY);
    } else {
      const encoded = encode(JSON.stringify(filtered));
      localStorage.setItem(FAILED_ATTEMPTS_KEY, encoded);
    }
  } catch (error) {
    console.warn('Failed to clear failed attempts:', error);
  }
};

/**
 * Check if account is currently locked
 */
export const isAccountLocked = (email: string): { locked: boolean; remainingTime?: number } => {
  try {
    const stored = localStorage.getItem(FAILED_ATTEMPTS_KEY);
    if (!stored) return { locked: false };
    
    const decoded = decode(stored);
    if (!decoded) return { locked: false };
    
    const attempts: FailedAttempts[] = JSON.parse(decoded);
    const attempt = attempts.find(a => a.email === email);
    
    if (!attempt?.lockedUntil) return { locked: false };
    
    const now = Date.now();
    if (now >= attempt.lockedUntil) {
      // Lockout expired, clean up
      clearFailedAttempts(email);
      return { locked: false };
    }
    
    return {
      locked: true,
      remainingTime: attempt.lockedUntil - now
    };
  } catch (error) {
    console.warn('Failed to check account lock status:', error);
    return { locked: false };
  }
};