/**
 * Tests for credential storage utilities
 */

import {
  storeRememberedCredentials,
  getRememberedCredentials,
  clearRememberedCredentials,
  hasRememberedCredentials,
  refreshRememberedCredentials,
  recordFailedAttempt,
  clearFailedAttempts,
  isAccountLocked
} from '../../utils/credentialStorage';

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};

  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
});

describe('Credential Storage', () => {
  beforeEach(() => {
    localStorageMock.clear();
  });

  describe('storeRememberedCredentials', () => {
    it('should store credentials with correct expiration', () => {
      const email = 'test@example.com';
      storeRememberedCredentials(email);

      const stored = localStorageMock.getItem('neuroquest_remembered_credentials');
      expect(stored).toBeTruthy();
    });
  });

  describe('getRememberedCredentials', () => {
    it('should return credentials if they exist and are not expired', () => {
      const email = 'test@example.com';
      storeRememberedCredentials(email);

      const credentials = getRememberedCredentials();
      expect(credentials).toEqual({ email });
    });

    it('should return null if no credentials are stored', () => {
      const credentials = getRememberedCredentials();
      expect(credentials).toBeNull();
    });

    it('should return credentials with indefinite storage', () => {
      const email = 'test@example.com';
      
      // Manually store credentials with indefinite expiration
      const indefiniteCredentials = {
        email,
        rememberedAt: Date.now() - 31 * 24 * 60 * 60 * 1000, // 31 days ago
        expiresAt: Number.MAX_SAFE_INTEGER // Indefinite storage
      };
      
      localStorageMock.setItem(
        'neuroquest_remembered_credentials',
        btoa(encodeURIComponent(JSON.stringify(indefiniteCredentials)))
      );

      const credentials = getRememberedCredentials();
      expect(credentials).toEqual({ email });
      
      // Should NOT have cleared the credentials since we have indefinite storage
      const stored = localStorageMock.getItem('neuroquest_remembered_credentials');
      expect(stored).toBeTruthy();
    });

    it('should clear credentials that are expired (non-indefinite)', () => {
      const email = 'test@example.com';
      
      // Manually store credentials with past expiration (non-indefinite)
      const expiredCredentials = {
        email,
        rememberedAt: Date.now() - 31 * 24 * 60 * 60 * 1000, // 31 days ago
        expiresAt: Date.now() - 1000 // 1 second ago (should be cleared)
      };
      
      localStorageMock.setItem(
        'neuroquest_remembered_credentials',
        btoa(encodeURIComponent(JSON.stringify(expiredCredentials)))
      );

      const credentials = getRememberedCredentials();
      expect(credentials).toBeNull();
      
      // Should have cleared the expired credentials
      const stored = localStorageMock.getItem('neuroquest_remembered_credentials');
      expect(stored).toBeNull();
    });
  });

  describe('hasRememberedCredentials', () => {
    it('should return true if valid credentials exist', () => {
      const email = 'test@example.com';
      storeRememberedCredentials(email);

      expect(hasRememberedCredentials()).toBe(true);
    });

    it('should return false if no credentials exist', () => {
      expect(hasRememberedCredentials()).toBe(false);
    });
  });

  describe('clearRememberedCredentials', () => {
    it('should remove stored credentials', () => {
      const email = 'test@example.com';
      storeRememberedCredentials(email);

      expect(hasRememberedCredentials()).toBe(true);
      
      clearRememberedCredentials();
      
      expect(hasRememberedCredentials()).toBe(false);
    });
  });

  describe('refreshRememberedCredentials', () => {
    it('should maintain indefinite expiration', () => {
      const email = 'test@example.com';
      storeRememberedCredentials(email);

      refreshRememberedCredentials();

      const stored = localStorageMock.getItem('neuroquest_remembered_credentials');
      const credentials = JSON.parse(decodeURIComponent(atob(stored!)));

      // Should maintain indefinite expiration
      expect(credentials.expiresAt).toBe(Number.MAX_SAFE_INTEGER);
    });
  });

  describe('Error handling', () => {
    it('should handle corrupted data gracefully', () => {
      // Store corrupted data
      localStorageMock.setItem('neuroquest_remembered_credentials', 'corrupted-data');

      const credentials = getRememberedCredentials();
      expect(credentials).toBeNull();
      
      // The corrupted data should still exist (not automatically cleared)
      // The function just returns null when it cannot parse the data
      const stored = localStorageMock.getItem('neuroquest_remembered_credentials');
      expect(stored).toBe('corrupted-data');
    });

    it('should handle localStorage errors gracefully', () => {
      // Mock localStorage to throw errors
      const originalSetItem = localStorageMock.setItem;
      localStorageMock.setItem = () => {
        throw new Error('Storage quota exceeded');
      };

      // Should not throw when storing fails
      expect(() => {
        storeRememberedCredentials('test@example.com');
      }).not.toThrow();

      // Restore original setItem
      localStorageMock.setItem = originalSetItem;
    });
  });

  describe('recordFailedAttempt', () => {
    beforeEach(() => {
      localStorageMock.clear();
    });

    it('should record first failed attempt', () => {
      const email = 'test@example.com';
      const isLocked = recordFailedAttempt(email);

      expect(isLocked).toBe(false);
      const stored = localStorageMock.getItem('neuroquest_failed_attempts');
      expect(stored).toBeTruthy();
    });

    it('should increment failed attempts for same email', () => {
      const email = 'test@example.com';
      
      recordFailedAttempt(email);
      recordFailedAttempt(email);
      recordFailedAttempt(email);

      const stored = localStorageMock.getItem('neuroquest_failed_attempts');
      const decoded = JSON.parse(decodeURIComponent(atob(stored!)));
      const attempt = decoded.find((a: any) => a.email === email);
      
      expect(attempt.attempts).toBe(3);
    });

    it('should lock account after max failed attempts', () => {
      const email = 'test@example.com';
      
      // Record 5 failed attempts
      for (let i = 0; i < 5; i++) {
        recordFailedAttempt(email);
      }

      const isLocked = recordFailedAttempt(email);
      expect(isLocked).toBe(true);
    });

    it('should reset attempts after one hour', () => {
      const email = 'test@example.com';
      
      // Record initial attempts
      recordFailedAttempt(email);
      recordFailedAttempt(email);
      
      // Manually modify the lastAttempt time to simulate time passing
      const stored1 = localStorageMock.getItem('neuroquest_failed_attempts');
      const decoded1 = JSON.parse(decodeURIComponent(atob(stored1!)));
      const attempt1 = decoded1.find((a: any) => a.email === email);
      attempt1.lastAttempt = Date.now() - 2 * 60 * 60 * 1000; // 2 hours ago
      
      localStorageMock.setItem(
        'neuroquest_failed_attempts',
        btoa(encodeURIComponent(JSON.stringify(decoded1)))
      );
      
      recordFailedAttempt(email);
      
      const stored2 = localStorageMock.getItem('neuroquest_failed_attempts');
      const decoded2 = JSON.parse(decodeURIComponent(atob(stored2!)));
      const attempt2 = decoded2.find((a: any) => a.email === email);
      
      expect(attempt2.attempts).toBe(1); // Should reset to 1
    });

    it('should handle localStorage errors gracefully', () => {
      const originalSetItem = localStorageMock.setItem;
      localStorageMock.setItem = () => {
        throw new Error('Storage quota exceeded');
      };

      expect(() => {
        recordFailedAttempt('test@example.com');
      }).not.toThrow();

      localStorageMock.setItem = originalSetItem;
    });
  });

  describe('clearFailedAttempts', () => {
    beforeEach(() => {
      localStorageMock.clear();
    });

    it('should clear failed attempts for specific email', () => {
      const email1 = 'test1@example.com';
      const email2 = 'test2@example.com';
      
      recordFailedAttempt(email1);
      recordFailedAttempt(email2);
      
      clearFailedAttempts(email1);
      
      const stored = localStorageMock.getItem('neuroquest_failed_attempts');
      if (stored) {
        const decoded = JSON.parse(decodeURIComponent(atob(stored)));
        expect(decoded.find((a: any) => a.email === email1)).toBeUndefined();
        expect(decoded.find((a: any) => a.email === email2)).toBeDefined();
      }
    });

    it('should remove storage when no attempts remain', () => {
      const email = 'test@example.com';
      
      recordFailedAttempt(email);
      clearFailedAttempts(email);
      
      const stored = localStorageMock.getItem('neuroquest_failed_attempts');
      expect(stored).toBeNull();
    });

    it('should handle non-existent email gracefully', () => {
      expect(() => {
        clearFailedAttempts('nonexistent@example.com');
      }).not.toThrow();
    });

    it('should handle localStorage errors gracefully', () => {
      const originalRemoveItem = localStorageMock.removeItem;
      localStorageMock.removeItem = () => {
        throw new Error('Storage error');
      };

      expect(() => {
        clearFailedAttempts('test@example.com');
      }).not.toThrow();

      localStorageMock.removeItem = originalRemoveItem;
    });
  });

  describe('isAccountLocked', () => {
    beforeEach(() => {
      localStorageMock.clear();
    });

    it('should return unlocked for account with no failed attempts', () => {
      const result = isAccountLocked('test@example.com');
      
      expect(result.locked).toBe(false);
      expect(result.remainingTime).toBeUndefined();
    });

    it('should return unlocked for account with attempts below threshold', () => {
      const email = 'test@example.com';
      
      recordFailedAttempt(email);
      recordFailedAttempt(email);
      
      const result = isAccountLocked(email);
      
      expect(result.locked).toBe(false);
    });

    it('should return locked for account that exceeds threshold', () => {
      const email = 'test@example.com';
      
      // Record enough attempts to trigger lockout (5 attempts locks on the 5th)
      for (let i = 0; i < 5; i++) {
        const isLocked = recordFailedAttempt(email);
        if (i === 4) {
          expect(isLocked).toBe(true); // Should be locked on 5th attempt
        }
      }
      
      const result = isAccountLocked(email);
      
      expect(result.locked).toBe(true);
      expect(result.remainingTime).toBeGreaterThan(0);
    });

    it('should clear expired lockout', () => {
      const email = 'test@example.com';
      
      // Record enough attempts to trigger lockout
      for (let i = 0; i < 5; i++) {
        recordFailedAttempt(email);
      }
      
      // Manually modify the lockout time to simulate expiration
      const stored1 = localStorageMock.getItem('neuroquest_failed_attempts');
      const decoded1 = JSON.parse(decodeURIComponent(atob(stored1!)));
      const attempt1 = decoded1.find((a: any) => a.email === email);
      attempt1.lockedUntil = Date.now() - 1000; // 1 second ago (expired)
      
      localStorageMock.setItem(
        'neuroquest_failed_attempts',
        btoa(encodeURIComponent(JSON.stringify(decoded1)))
      );
      
      const result = isAccountLocked(email);
      
      expect(result.locked).toBe(false);
      
      // Verify attempts were cleared
      const stored2 = localStorageMock.getItem('neuroquest_failed_attempts');
      expect(stored2).toBeNull();
    });

    it('should handle localStorage errors gracefully', () => {
      const originalGetItem = localStorageMock.getItem;
      localStorageMock.getItem = () => {
        throw new Error('Storage error');
      };

      const result = isAccountLocked('test@example.com');
      
      expect(result.locked).toBe(false);
      
      localStorageMock.getItem = originalGetItem;
    });

    it('should handle corrupted data gracefully', () => {
      localStorageMock.setItem('neuroquest_failed_attempts', 'corrupted-data');
      
      const result = isAccountLocked('test@example.com');
      
      expect(result.locked).toBe(false);
    });
  });
});