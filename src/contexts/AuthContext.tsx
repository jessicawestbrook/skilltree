'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { AuthContextType, User, LoginCredentials, RegisterCredentials } from '../types';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check for existing session on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const savedUser = localStorage.getItem('neuroquest_user');
        if (savedUser) {
          const userData = JSON.parse(savedUser);
          // Convert date strings back to Date objects
          userData.createdAt = new Date(userData.createdAt);
          if (userData.lastLoginAt) {
            userData.lastLoginAt = new Date(userData.lastLoginAt);
          }
          setUser(userData);
        }
      } catch (err) {
        console.error('Error checking auth:', err);
        localStorage.removeItem('neuroquest_user');
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (credentials: LoginCredentials): Promise<{ success: boolean; error?: string }> => {
    setIsLoading(true);
    setError(null);

    try {
      // Simulate API call - in a real app, this would be a server request
      await new Promise(resolve => setTimeout(resolve, 1000));

      // For demo purposes, create a mock user
      // In a real app, this would come from your authentication service
      const mockUser: User = {
        id: `user_${Date.now()}`,
        email: credentials.email,
        username: credentials.email.split('@')[0],
        displayName: credentials.email.split('@')[0],
        createdAt: new Date(),
        lastLoginAt: new Date()
      };

      setUser(mockUser);
      localStorage.setItem('neuroquest_user', JSON.stringify(mockUser));
      
      return { success: true };
    } catch (err) {
      const errorMessage = 'Login failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (credentials: RegisterCredentials): Promise<{ success: boolean; error?: string }> => {
    setIsLoading(true);
    setError(null);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      // For demo purposes, create a mock user
      const mockUser: User = {
        id: `user_${Date.now()}`,
        email: credentials.email,
        username: credentials.username,
        displayName: credentials.displayName || credentials.username,
        createdAt: new Date(),
        lastLoginAt: new Date()
      };

      setUser(mockUser);
      localStorage.setItem('neuroquest_user', JSON.stringify(mockUser));
      
      return { success: true };
    } catch (err) {
      const errorMessage = 'Registration failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<void> => {
    setIsLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setUser(null);
      localStorage.removeItem('neuroquest_user');
      setError(null);
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const updateProfile = async (updates: Partial<User>): Promise<{ success: boolean; error?: string }> => {
    if (!user) return { success: false, error: 'Not authenticated' };

    setIsLoading(true);
    setError(null);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));

      const updatedUser = { ...user, ...updates };
      setUser(updatedUser);
      localStorage.setItem('neuroquest_user', JSON.stringify(updatedUser));
      
      return { success: true };
    } catch (err) {
      const errorMessage = 'Profile update failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    error,
    login,
    register,
    logout,
    updateProfile
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