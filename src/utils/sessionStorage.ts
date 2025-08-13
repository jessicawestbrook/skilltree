// Session storage utilities for faster initial loads
interface StoredSession {
  user: {
    id: string;
    email: string;
    username: string;
    avatar?: string;
    photoURL?: string;
  };
  expiresAt: number;
}

const SESSION_KEY = 'neuroquest_session';

export const saveSession = (session: StoredSession): void => {
  try {
    if (typeof window !== 'undefined') {
      localStorage.setItem(SESSION_KEY, JSON.stringify(session));
    }
  } catch (error) {
    console.error('Failed to save session:', error);
  }
};

export const getStoredSession = (): StoredSession | null => {
  try {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem(SESSION_KEY);
      if (stored) {
        const session = JSON.parse(stored) as StoredSession;
        // Check if session is expired
        if (session.expiresAt > Date.now()) {
          return session;
        } else {
          // Session expired, clear it
          clearStoredSession();
        }
      }
    }
  } catch (error) {
    console.error('Failed to get stored session:', error);
  }
  return null;
};

export const clearStoredSession = (): void => {
  try {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(SESSION_KEY);
    }
  } catch (error) {
    console.error('Failed to clear session:', error);
  }
};