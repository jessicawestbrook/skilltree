'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode, useMemo } from 'react';
import { AuthContextType, User, LoginCredentials, RegisterCredentials } from '../types';
import { createClient } from '../lib/supabase-client';
import type { User as SupabaseUser } from '@supabase/supabase-js';
import { saveSession, getStoredSession, clearStoredSession } from '../utils/sessionStorage';
import { ErrorLogger } from '../utils/errorLogger';
import { 
  storeRememberedCredentials, 
  getRememberedCredentials, 
  clearRememberedCredentials,
  refreshRememberedCredentials,
  recordFailedAttempt,
  clearFailedAttempts,
  isAccountLocked
} from '../utils/credentialStorage';
import { ProgressService } from '../services/progressService';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sessionChecked, setSessionChecked] = useState(false);
  const [refreshTimer, setRefreshTimer] = useState<NodeJS.Timeout | null>(null);
  
  // Create supabase client once using useMemo
  const supabase = useMemo(() => createClient(), []);

  // Helper function to convert Supabase user to our User type
  const mapSupabaseUser = (supabaseUser: SupabaseUser): User => {
    return {
      id: supabaseUser.id,
      email: supabaseUser.email || '',
      username: supabaseUser.user_metadata?.username || supabaseUser.email?.split('@')[0] || '',
      avatar: supabaseUser.user_metadata?.avatar || undefined,
      photoURL: supabaseUser.user_metadata?.photoURL || undefined,
      birthYear: supabaseUser.user_metadata?.birthYear || undefined,
      createdAt: new Date(supabaseUser.created_at),
      lastLoginAt: supabaseUser.last_sign_in_at ? new Date(supabaseUser.last_sign_in_at) : undefined
    };
  };

  // Setup automatic token refresh
  const setupTokenRefresh = (expiresAt: number) => {
    // Clear any existing timer
    if (refreshTimer) {
      clearTimeout(refreshTimer);
    }

    // Calculate when to refresh (5 minutes before expiry)
    const expiresIn = expiresAt * 1000 - Date.now();
    const refreshIn = Math.max(expiresIn - 5 * 60 * 1000, 0);

    if (refreshIn > 0) {
      const timer = setTimeout(async () => {
        try {
          const { data: { session }, error } = await supabase.auth.refreshSession();
          if (error) {
            console.error('Failed to refresh session:', error);
            // Session expired, log out user
            await logout();
          } else if (session) {
            // Setup next refresh
            if (session.expires_at) {
              setupTokenRefresh(session.expires_at);
            }
          }
        } catch (error) {
          console.error('Error refreshing session:', error);
        }
      }, refreshIn);

      setRefreshTimer(timer);
    }
  };

  // Clear refresh timer on unmount
  useEffect(() => {
    return () => {
      if (refreshTimer) {
        clearTimeout(refreshTimer);
      }
    };
  }, [refreshTimer]);

  // Check for existing session on mount and restore it
  useEffect(() => {
    let mounted = true;

    const restoreSession = async () => {
      try {
        // First try to get session from localStorage for faster initial load
        const storedSession = getStoredSession();
        if (storedSession && mounted) {
          setUser({
            ...storedSession.user,
            createdAt: new Date(),
            lastLoginAt: new Date()
          });
        }

        // Then verify with Supabase
        const { data: { session }, error } = await supabase.auth.getSession();
        
        if (error) {
          ErrorLogger.logAuthError(error, 'session_restore');
          // Try to refresh if there's an error
          const { data: { session: refreshedSession } } = await supabase.auth.refreshSession();
          if (refreshedSession?.user && mounted) {
            setUser(mapSupabaseUser(refreshedSession.user));
            // Setup token refresh
            if (refreshedSession.expires_at) {
              setupTokenRefresh(refreshedSession.expires_at);
            }
          }
        } else if (session?.user && mounted) {
          const mappedUser = mapSupabaseUser(session.user);
          setUser(mappedUser);
          // Store in localStorage for faster next load
          if (session.expires_at) {
            saveSession({
              user: {
                id: mappedUser.id,
                email: mappedUser.email,
                username: mappedUser.username,
                avatar: mappedUser.avatar,
                photoURL: mappedUser.photoURL,
                birthYear: mappedUser.birthYear
              },
              expiresAt: session.expires_at * 1000
            });
            setupTokenRefresh(session.expires_at);
          }
        } else if (!session && mounted) {
          // No valid session, clear stored session
          clearStoredSession();
          setUser(null);
        }
      } catch (error) {
        ErrorLogger.logAuthError(error as Error, 'auth_check');
      } finally {
        if (mounted) {
          setSessionChecked(true);
          setIsLoading(false);
        }
      }
    };

    restoreSession();

    // Listen for auth state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      if (!mounted) return;

      console.log('Auth state changed:', event);
      
      if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
        if (session?.user) {
          const mappedUser = mapSupabaseUser(session.user);
          setUser(mappedUser);
          // Store in localStorage and setup token refresh
          if (session.expires_at) {
            saveSession({
              user: {
                id: mappedUser.id,
                email: mappedUser.email,
                username: mappedUser.username,
                avatar: mappedUser.avatar,
                photoURL: mappedUser.photoURL,
                birthYear: mappedUser.birthYear
              },
              expiresAt: session.expires_at * 1000
            });
            setupTokenRefresh(session.expires_at);
          }
        }
      } else if (event === 'SIGNED_OUT') {
        setUser(null);
        clearStoredSession();
        // Clear refresh timer
        if (refreshTimer) {
          clearTimeout(refreshTimer);
          setRefreshTimer(null);
        }
      } else if (event === 'USER_UPDATED') {
        if (session?.user) {
          setUser(mapSupabaseUser(session.user));
        }
      }
    });

    return () => {
      mounted = false;
      subscription.unsubscribe();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = async (credentials: LoginCredentials): Promise<{ success: boolean; error?: string }> => {
    setIsLoading(true);
    setError(null);

    // Check if account is locked due to failed attempts
    const lockStatus = isAccountLocked(credentials.email);
    if (lockStatus.locked) {
      const remainingMinutes = lockStatus.remainingTime ? Math.ceil(lockStatus.remainingTime / (60 * 1000)) : 15;
      const errorMessage = `Account temporarily locked due to multiple failed login attempts. Please try again in ${remainingMinutes} minute${remainingMinutes !== 1 ? 's' : ''}.`;
      setError(errorMessage);
      setIsLoading(false);
      return { success: false, error: errorMessage };
    }

    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email: credentials.email,
        password: credentials.password
      });

      if (error) {
        // Enhanced error handling for different credential failure scenarios
        let errorMessage = 'Login failed. Please try again.';
        
        switch (error.message) {
          case 'Invalid login credentials':
            errorMessage = 'Invalid email or password. Please check your credentials and try again.';
            // Record failed attempt and clear remembered credentials on invalid login
            recordFailedAttempt(credentials.email);
            if (credentials.rememberMe) {
              clearRememberedCredentials();
            }
            break;
          case 'Email not confirmed':
            errorMessage = 'Please check your email and click the verification link to confirm your account before signing in.';
            // Don't record as failed attempt since this is a verification issue, not bad credentials
            break;
          case 'Email rate limit exceeded':
            errorMessage = 'Too many login attempts. Please wait a few minutes before trying again.';
            break;
          case 'User not found':
            errorMessage = 'No account found with this email address. Please check your email or sign up.';
            break;
          case 'Password is too weak':
            errorMessage = 'Password does not meet security requirements.';
            break;
          case 'Signup disabled':
            errorMessage = 'Account registration is currently disabled.';
            break;
          default:
            // Log unexpected errors for debugging
            ErrorLogger.logAuthError(error, 'login_unexpected_error', credentials.email);
            errorMessage = error.message || 'Login failed. Please try again.';
        }
        
        setError(errorMessage);
        ErrorLogger.logAuthError(error, 'login_failed', credentials.email);
        return { success: false, error: errorMessage };
      }

      if (data.user) {
        const mappedUser = mapSupabaseUser(data.user);
        setUser(mappedUser);
        
        // Clear any failed login attempts on successful login
        clearFailedAttempts(credentials.email);
        
        // Initialize progress data for existing users who don't have it yet
        ProgressService.initializeUserProgress(mappedUser.id).catch(error => {
          console.warn('Failed to initialize user progress data:', error);
          // Don't fail login if progress initialization fails
        });
        
        // Set user context for error tracking
        ErrorLogger.setUserContext({
          id: mappedUser.id,
          email: mappedUser.email,
          username: mappedUser.username,
        });
        
        // Handle remember me functionality
        if (credentials.rememberMe) {
          storeRememberedCredentials(credentials.email);
        } else {
          clearRememberedCredentials();
        }
        
        // Store session and setup token refresh
        if (data.session?.expires_at) {
          saveSession({
            user: {
              id: mappedUser.id,
              email: mappedUser.email,
              username: mappedUser.username,
              avatar: mappedUser.avatar,
              photoURL: mappedUser.photoURL,
              birthYear: mappedUser.birthYear
            },
            expiresAt: data.session.expires_at * 1000
          });
          setupTokenRefresh(data.session.expires_at);
        }
      }
      
      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Login failed. Please try again.';
      ErrorLogger.logAuthError(error as Error, 'login', credentials.email);
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (credentials: RegisterCredentials): Promise<{ success: boolean; error?: string; requiresVerification?: boolean }> => {
    setIsLoading(true);
    setError(null);

    try {
      const { data, error } = await supabase.auth.signUp({
        email: credentials.email,
        password: credentials.password,
        options: {
          data: {
            username: credentials.username
          }
        }
      });

      if (error) {
        // Enhanced error handling for registration failures
        let errorMessage = 'Registration failed. Please try again.';
        
        switch (error.message) {
          case 'User already registered':
          case 'Email address already in use':
            errorMessage = 'An account with this email already exists. Please sign in instead.';
            break;
          case 'Password should be at least 6 characters':
            errorMessage = 'Password must be at least 6 characters long.';
            break;
          case 'Invalid email':
          case 'Unable to validate email address: invalid format':
            errorMessage = 'Please enter a valid email address.';
            break;
          case 'Password is too weak':
            errorMessage = 'Password is too weak. Please use a stronger password with at least 8 characters, including uppercase, lowercase, and numbers.';
            break;
          case 'Signup disabled':
            errorMessage = 'New registrations are currently disabled. Please contact support.';
            break;
          case 'Email rate limit exceeded':
            errorMessage = 'Too many registration attempts. Please wait a few minutes before trying again.';
            break;
          default:
            // Log unexpected registration errors
            ErrorLogger.logAuthError(error, 'register_unexpected_error', credentials.email);
            errorMessage = error.message || 'Registration failed. Please try again.';
        }
        
        setError(errorMessage);
        ErrorLogger.logAuthError(error, 'registration_failed', credentials.email);
        return { success: false, error: errorMessage };
      }

      if (data.user) {
        // Try to send verification email but don't fail registration if it doesn't work
        try {
          const response = await fetch('/api/auth/send-verification', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              userId: data.user.id,
              email: data.user.email,
              username: credentials.username
            })
          });

          if (!response.ok) {
            console.warn('Verification email could not be sent, but registration succeeded');
            // Don't fail the registration, just log the warning
          }
        } catch (emailError) {
          console.warn('Email service unavailable, but registration succeeded:', emailError);
          // Continue with registration even if email fails
        }

        // Note: User account is created successfully even if email fails
        if (data.session) {
          const mappedUser = mapSupabaseUser(data.user);
          setUser(mappedUser);
          
          // Initialize default progress data for new user
          ProgressService.initializeUserProgress(mappedUser.id).catch(error => {
            console.warn('Failed to initialize user progress data:', error);
            // Don't fail registration if progress initialization fails
          });
          
          // Store session and setup token refresh
          if (data.session.expires_at) {
            saveSession({
              user: {
                id: mappedUser.id,
                email: mappedUser.email,
                username: mappedUser.username,
                avatar: mappedUser.avatar,
                photoURL: mappedUser.photoURL
              },
              expiresAt: data.session.expires_at * 1000
            });
            setupTokenRefresh(data.session.expires_at);
          }
        }
        
        return { success: true, requiresVerification: true };
      }
      
      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Registration failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<void> => {
    setIsLoading(true);
    try {
      // Clear refresh timer before logging out
      if (refreshTimer) {
        clearTimeout(refreshTimer);
        setRefreshTimer(null);
      }

      const { error } = await supabase.auth.signOut();
      
      if (error) {
        console.error('Logout error:', error);
      }
      
      setUser(null);
      setError(null);
      clearStoredSession();
      clearRememberedCredentials();
      
      // Clear user context for error tracking
      ErrorLogger.clearUserContext();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateProfile = async (updates: Partial<User>): Promise<{ success: boolean; error?: string }> => {
    if (!user) return { success: false, error: 'Not authenticated' };

    setIsLoading(true);
    setError(null);

    try {
      const { data, error } = await supabase.auth.updateUser({
        data: {
          username: updates.username,
          avatar: updates.avatar,
          photoURL: updates.photoURL,
          birthYear: updates.birthYear
        }
      });

      if (error) {
        const errorMessage = error.message || 'Profile update failed. Please try again.';
        setError(errorMessage);
        return { success: false, error: errorMessage };
      }

      if (data.user) {
        setUser(mapSupabaseUser(data.user));
      }
      
      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Profile update failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const resetPassword = async (email: string): Promise<{ success: boolean; error?: string }> => {
    setIsLoading(true);
    setError(null);

    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`
      });

      if (error) {
        const errorMessage = error.message || 'Failed to send reset email. Please try again.';
        setError(errorMessage);
        return { success: false, error: errorMessage };
      }

      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to send reset email. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const updatePassword = async (newPassword: string): Promise<{ success: boolean; error?: string }> => {
    setIsLoading(true);
    setError(null);

    try {
      const { error } = await supabase.auth.updateUser({
        password: newPassword
      });

      if (error) {
        const errorMessage = error.message || 'Failed to update password. Please try again.';
        setError(errorMessage);
        return { success: false, error: errorMessage };
      }

      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update password. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const refreshSession = async (): Promise<{ success: boolean; error?: string }> => {
    try {
      const { data: { session }, error } = await supabase.auth.refreshSession();
      
      if (error) {
        return { success: false, error: error.message };
      }
      
      if (session?.user) {
        const mappedUser = mapSupabaseUser(session.user);
        setUser(mappedUser);
        // Store updated session and setup next refresh
        if (session.expires_at) {
          saveSession({
            user: {
              id: mappedUser.id,
              email: mappedUser.email,
              username: mappedUser.username,
              avatar: mappedUser.avatar,
              photoURL: mappedUser.photoURL
            },
            expiresAt: session.expires_at * 1000
          });
          setupTokenRefresh(session.expires_at);
        }
      }
      
      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to refresh session';
      return { success: false, error: errorMessage };
    }
  };

  const getRememberedEmail = (): string | null => {
    const credentials = getRememberedCredentials();
    return credentials ? credentials.email : null;
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading: isLoading || !sessionChecked,
    error,
    login,
    register,
    logout,
    updateProfile,
    resetPassword,
    updatePassword,
    refreshSession,
    sessionReady: sessionChecked,
    getRememberedEmail
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};