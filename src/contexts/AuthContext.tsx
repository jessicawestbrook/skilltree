'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { AuthContextType, User, LoginCredentials, RegisterCredentials } from '../types';
import { supabase } from '../lib/supabase';
import type { User as SupabaseUser } from '@supabase/supabase-js';
import { saveSession, getStoredSession, clearStoredSession } from '../utils/sessionStorage';
import { ErrorLogger } from '../utils/errorLogger';

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

  // Helper function to convert Supabase user to our User type
  const mapSupabaseUser = (supabaseUser: SupabaseUser): User => {
    return {
      id: supabaseUser.id,
      email: supabaseUser.email || '',
      username: supabaseUser.user_metadata?.username || supabaseUser.email?.split('@')[0] || '',
      avatar: supabaseUser.user_metadata?.avatar || undefined,
      photoURL: supabaseUser.user_metadata?.photoURL || undefined,
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
                photoURL: mappedUser.photoURL
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
                photoURL: mappedUser.photoURL
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

    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email: credentials.email,
        password: credentials.password
      });

      if (error) {
        const errorMessage = error.message || 'Login failed. Please try again.';
        setError(errorMessage);
        return { success: false, error: errorMessage };
      }

      if (data.user) {
        const mappedUser = mapSupabaseUser(data.user);
        setUser(mappedUser);
        
        // Set user context for error tracking
        ErrorLogger.setUserContext({
          id: mappedUser.id,
          email: mappedUser.email,
          username: mappedUser.username,
        });
        
        // Store session and setup token refresh
        if (data.session?.expires_at) {
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
        const errorMessage = error.message || 'Registration failed. Please try again.';
        setError(errorMessage);
        return { success: false, error: errorMessage };
      }

      if (data.user) {
        // Send verification email
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
            console.error('Failed to send verification email');
          }
        } catch (emailError) {
          console.error('Error sending verification email:', emailError);
        }

        // Note: User needs to confirm email before being fully authenticated
        if (data.session) {
          const mappedUser = mapSupabaseUser(data.user);
          setUser(mappedUser);
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
          photoURL: updates.photoURL
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
    sessionReady: sessionChecked
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