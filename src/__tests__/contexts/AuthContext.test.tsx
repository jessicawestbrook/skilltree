import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import { AuthProvider, useAuth } from '../../contexts/AuthContext';
import { supabase } from '../../lib/supabase';
import * as credentialStorage from '../../utils/credentialStorage';

// Mock Supabase
jest.mock('../../lib/supabase', () => ({
  supabase: {
    auth: {
      signInWithPassword: jest.fn(),
      signUp: jest.fn(),
      signOut: jest.fn(),
      resetPasswordForEmail: jest.fn(),
      updateUser: jest.fn(),
      getSession: jest.fn(),
      onAuthStateChange: jest.fn(() => ({
        data: { subscription: { unsubscribe: jest.fn() } }
      }))
    }
  }
}));

// Mock credential storage
jest.mock('../../utils/credentialStorage', () => ({
  storeRememberedCredentials: jest.fn(),
  getRememberedCredentials: jest.fn(),
  clearRememberedCredentials: jest.fn(),
  refreshRememberedCredentials: jest.fn(),
  recordFailedAttempt: jest.fn(),
  clearFailedAttempts: jest.fn(),
  isAccountLocked: jest.fn()
}));

// Mock error logger
jest.mock('../../utils/errorLogger', () => ({
  ErrorLogger: {
    logAuthError: jest.fn(),
    setUserContext: jest.fn(),
    clearUserContext: jest.fn()
  }
}));

// Mock session storage
jest.mock('../../utils/sessionStorage', () => ({
  saveSession: jest.fn(),
  getStoredSession: jest.fn(),
  clearStoredSession: jest.fn()
}));

// Test component to access auth context
const TestComponent = () => {
  const auth = useAuth();
  
  return (
    <div>
      <div data-testid="loading">{auth.isLoading ? 'true' : 'false'}</div>
      <div data-testid="authenticated">{auth.isAuthenticated ? 'true' : 'false'}</div>
      <div data-testid="error">{auth.error || 'none'}</div>
      <div data-testid="user">{auth.user?.email || 'none'}</div>
      <button onClick={() => auth.login({ 
        email: 'test@example.com', 
        password: 'password123',
        rememberMe: false 
      })}>Login</button>
      <button onClick={() => auth.register({ 
        email: 'new@example.com', 
        password: 'password123',
        username: 'newuser' 
      })}>Register</button>
      <button onClick={() => auth.logout()}>Logout</button>
    </div>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('Provider', () => {
    it('should provide auth context to children', () => {
      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      expect(screen.getByTestId('loading')).toBeInTheDocument();
      expect(screen.getByTestId('authenticated')).toBeInTheDocument();
    });

    it('should initialize with loading state', async () => {
      // Mock getSession to resolve quickly
      (supabase.auth.getSession as jest.Mock).mockResolvedValue({
        data: { session: null },
        error: null
      });
      
      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      // Initially loading should be true while checking session
      expect(screen.getByTestId('loading').textContent).toBe('true');
      
      // Wait for session check to complete
      await waitFor(() => {
        expect(screen.getByTestId('loading').textContent).toBe('false');
      });
      
      expect(screen.getByTestId('authenticated').textContent).toBe('false');
    });
  });

  describe('Login', () => {
    it('should handle successful login', async () => {
      const mockUser = {
        id: '123',
        email: 'test@example.com',
        user_metadata: { username: 'testuser' }
      };
      
      const mockSession = {
        access_token: 'token123',
        refresh_token: 'refresh123',
        expires_at: Math.floor(Date.now() / 1000) + 3600
      };
      
      (supabase.auth.signInWithPassword as jest.Mock).mockResolvedValue({
        data: { user: mockUser, session: mockSession },
        error: null
      });
      
      (credentialStorage.isAccountLocked as jest.Mock).mockReturnValue({ locked: false });
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Login').click();
      });
      
      await waitFor(() => {
        expect(screen.getByTestId('authenticated').textContent).toBe('true');
        expect(screen.getByTestId('user').textContent).toBe('test@example.com');
      });
      
      expect(credentialStorage.clearFailedAttempts).toHaveBeenCalledWith('test@example.com');
    });

    it('should handle invalid credentials error', async () => {
      (supabase.auth.signInWithPassword as jest.Mock).mockResolvedValue({
        data: null,
        error: { message: 'Invalid login credentials' }
      });
      
      (credentialStorage.isAccountLocked as jest.Mock).mockReturnValue({ locked: false });
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Login').click();
      });
      
      await waitFor(() => {
        expect(screen.getByTestId('error').textContent).toContain('Invalid email or password');
      });
      
      expect(credentialStorage.recordFailedAttempt).toHaveBeenCalledWith('test@example.com');
    });

    it('should handle account lockout', async () => {
      (credentialStorage.isAccountLocked as jest.Mock).mockReturnValue({ 
        locked: true, 
        remainingTime: 5 * 60 * 1000 // 5 minutes
      });
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Login').click();
      });
      
      await waitFor(() => {
        expect(screen.getByTestId('error').textContent).toContain('Account temporarily locked');
        expect(screen.getByTestId('error').textContent).toContain('5 minute');
      });
      
      expect(supabase.auth.signInWithPassword).not.toHaveBeenCalled();
    });

    it('should handle rate limiting error', async () => {
      (supabase.auth.signInWithPassword as jest.Mock).mockResolvedValue({
        data: null,
        error: { message: 'Email rate limit exceeded' }
      });
      
      (credentialStorage.isAccountLocked as jest.Mock).mockReturnValue({ locked: false });
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Login').click();
      });
      
      await waitFor(() => {
        expect(screen.getByTestId('error').textContent).toContain('Too many login attempts');
      });
    });
  });

  describe('Registration', () => {
    it('should handle successful registration', async () => {
      const mockUser = {
        id: '123',
        email: 'new@example.com',
        user_metadata: { username: 'newuser' }
      };
      
      (supabase.auth.signUp as jest.Mock).mockResolvedValue({
        data: { user: mockUser, session: null },
        error: null
      });
      
      // Mock fetch for email verification
      global.fetch = jest.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ success: true })
      });
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Register').click();
      });
      
      await waitFor(() => {
        expect(supabase.auth.signUp).toHaveBeenCalledWith({
          email: 'new@example.com',
          password: 'password123',
          options: {
            data: { username: 'newuser' }
          }
        });
      });
    });

    it('should handle duplicate email error', async () => {
      (supabase.auth.signUp as jest.Mock).mockResolvedValue({
        data: null,
        error: { message: 'User already registered' }
      });
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Register').click();
      });
      
      await waitFor(() => {
        expect(screen.getByTestId('error').textContent).toContain('account with this email already exists');
      });
    });

    it('should handle weak password error', async () => {
      (supabase.auth.signUp as jest.Mock).mockResolvedValue({
        data: null,
        error: { message: 'Password is too weak' }
      });
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Register').click();
      });
      
      await waitFor(() => {
        expect(screen.getByTestId('error').textContent).toContain('stronger password');
      });
    });

    it('should continue registration even if email verification fails', async () => {
      const mockUser = {
        id: '123',
        email: 'new@example.com',
        user_metadata: { username: 'newuser' }
      };
      
      (supabase.auth.signUp as jest.Mock).mockResolvedValue({
        data: { user: mockUser, session: null },
        error: null
      });
      
      // Mock fetch to fail
      global.fetch = jest.fn().mockRejectedValue(new Error('Email service down'));
      
      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Register').click();
      });
      
      await waitFor(() => {
        expect(consoleWarnSpy).toHaveBeenCalledWith(
          expect.stringContaining('Email service unavailable'),
          expect.any(Error)
        );
      });
      
      consoleWarnSpy.mockRestore();
    });
  });

  describe('Logout', () => {
    it('should handle successful logout', async () => {
      (supabase.auth.signOut as jest.Mock).mockResolvedValue({
        error: null
      });
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Logout').click();
      });
      
      await waitFor(() => {
        expect(screen.getByTestId('authenticated').textContent).toBe('false');
        expect(screen.getByTestId('user').textContent).toBe('none');
      });
    });

    it('should handle logout error gracefully', async () => {
      (supabase.auth.signOut as jest.Mock).mockResolvedValue({
        error: { message: 'Network error' }
      });
      
      const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Logout').click();
      });
      
      await waitFor(() => {
        expect(consoleErrorSpy).toHaveBeenCalledWith(
          'Logout error:',
          expect.any(Object)
        );
      });
      
      consoleErrorSpy.mockRestore();
    });
  });

  describe('Remember Me', () => {
    it('should store credentials when remember me is checked', async () => {
      const mockUser = {
        id: '123',
        email: 'test@example.com',
        user_metadata: { username: 'testuser' }
      };
      
      const mockSession = {
        access_token: 'token123',
        refresh_token: 'refresh123',
        expires_at: Math.floor(Date.now() / 1000) + 3600
      };
      
      (supabase.auth.signInWithPassword as jest.Mock).mockResolvedValue({
        data: { user: mockUser, session: mockSession },
        error: null
      });
      
      (credentialStorage.isAccountLocked as jest.Mock).mockReturnValue({ locked: false });
      
      const TestComponentWithRemember = () => {
        const auth = useAuth();
        
        return (
          <button onClick={() => auth.login({ 
            email: 'test@example.com', 
            password: 'password123',
            rememberMe: true 
          })}>Login with Remember</button>
        );
      };
      
      const { getByText } = render(
        <AuthProvider>
          <TestComponentWithRemember />
        </AuthProvider>
      );
      
      await act(async () => {
        getByText('Login with Remember').click();
      });
      
      await waitFor(() => {
        expect(credentialStorage.storeRememberedCredentials).toHaveBeenCalledWith('test@example.com');
      });
    });

    it('should retrieve remembered email on init', async () => {
      (credentialStorage.getRememberedCredentials as jest.Mock).mockReturnValue({
        email: 'remembered@example.com'
      });
      
      const TestComponentWithRemember = () => {
        const auth = useAuth();
        const rememberedEmail = auth.getRememberedEmail();
        
        return (
          <div data-testid="remembered">{rememberedEmail || 'none'}</div>
        );
      };
      
      const { getByTestId } = render(
        <AuthProvider>
          <TestComponentWithRemember />
        </AuthProvider>
      );
      
      expect(getByTestId('remembered').textContent).toBe('remembered@example.com');
    });
  });
});