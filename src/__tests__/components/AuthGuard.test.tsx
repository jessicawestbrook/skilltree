import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { AuthGuard } from '../../components/AuthGuard';
import { useAuth } from '../../contexts/AuthContext';

// Mock the AuthContext
jest.mock('../../contexts/AuthContext', () => ({
  useAuth: jest.fn(),
}));

const mockUseAuth = useAuth as jest.MockedFunction<typeof useAuth>;

// Mock components
const MockedChildComponent = () => (
  <div data-testid="protected-content">Protected Content</div>
);

const MockedFallbackComponent = () => (
  <div data-testid="fallback-content">Fallback Content</div>
);

describe('AuthGuard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('when user is authenticated', () => {
    beforeEach(() => {
      mockUseAuth.mockReturnValue({
        user: {
          id: 'user123',
          email: 'test@example.com',
          username: 'testuser'
        },
        isAuthenticated: true,
        isLoading: false,
        sessionReady: true,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);
    });

    it('should render children when user is authenticated', () => {
      render(
        <AuthGuard>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.getByTestId('protected-content')).toBeInTheDocument();
      expect(screen.queryByTestId('fallback-content')).not.toBeInTheDocument();
    });

    it('should render children immediately without loading state', () => {
      render(
        <AuthGuard>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.getByTestId('protected-content')).toBeInTheDocument();
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
  });

  describe('when user is not authenticated', () => {
    beforeEach(() => {
      mockUseAuth.mockReturnValue({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        sessionReady: true,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);
    });

    it('should render fallback when user is not authenticated', () => {
      render(
        <AuthGuard fallback={<MockedFallbackComponent />}>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
      expect(screen.getByTestId('fallback-content')).toBeInTheDocument();
    });

    it('should render default fallback when no fallback provided', () => {
      render(
        <AuthGuard>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
      expect(screen.getByText('Please sign in to access this content.')).toBeInTheDocument();
    });

    it('should not render children when user is not authenticated', () => {
      render(
        <AuthGuard fallback={<MockedFallbackComponent />}>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
    });
  });

  describe('when authentication is loading', () => {
    beforeEach(() => {
      mockUseAuth.mockReturnValue({
        user: null,
        isAuthenticated: false,
        isLoading: true,
        sessionReady: false,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);
    });

    it('should show loading state when authentication is being checked', () => {
      render(
        <AuthGuard>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.getByText('Loading...')).toBeInTheDocument();
      expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
      expect(screen.queryByTestId('fallback-content')).not.toBeInTheDocument();
    });

    it('should show loading even with fallback provided', () => {
      render(
        <AuthGuard fallback={<MockedFallbackComponent />}>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.getByText('Loading...')).toBeInTheDocument();
      expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
      expect(screen.queryByTestId('fallback-content')).not.toBeInTheDocument();
    });
  });

  describe('when session has not been checked yet', () => {
    beforeEach(() => {
      mockUseAuth.mockReturnValue({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        sessionReady: false,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);
    });

    it('should show loading state when session has not been checked', () => {
      render(
        <AuthGuard>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.getByText('Loading...')).toBeInTheDocument();
      expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
    });
  });

  describe('authentication state transitions', () => {
    it('should transition from loading to authenticated content', async () => {
      // Start with loading state
      mockUseAuth.mockReturnValue({
        user: null,
        isAuthenticated: false,
        isLoading: true,
        sessionReady: false,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);

      const { rerender } = render(
        <AuthGuard>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.getByText('Loading...')).toBeInTheDocument();

      // Transition to authenticated
      mockUseAuth.mockReturnValue({
        user: {
          id: 'user123',
          email: 'test@example.com',
          username: 'testuser'
        },
        isAuthenticated: true,
        isLoading: false,
        sessionReady: true,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);

      rerender(
        <AuthGuard>
          <MockedChildComponent />
        </AuthGuard>
      );

      await waitFor(() => {
        expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
        expect(screen.getByTestId('protected-content')).toBeInTheDocument();
      });
    });

    it('should transition from loading to unauthenticated fallback', async () => {
      // Start with loading state
      mockUseAuth.mockReturnValue({
        user: null,
        isAuthenticated: false,
        isLoading: true,
        sessionReady: false,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);

      const { rerender } = render(
        <AuthGuard fallback={<MockedFallbackComponent />}>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.getByText('Loading...')).toBeInTheDocument();

      // Transition to unauthenticated
      mockUseAuth.mockReturnValue({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        sessionReady: true,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);

      rerender(
        <AuthGuard fallback={<MockedFallbackComponent />}>
          <MockedChildComponent />
        </AuthGuard>
      );

      await waitFor(() => {
        expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
        expect(screen.getByTestId('fallback-content')).toBeInTheDocument();
        expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
      });
    });
  });

  describe('edge cases', () => {
    it('should handle null children gracefully', () => {
      mockUseAuth.mockReturnValue({
        user: {
          id: 'user123',
          email: 'test@example.com',
          username: 'testuser'
        },
        isAuthenticated: true,
        isLoading: false,
        sessionReady: true,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);

      render(
        <AuthGuard>
          {null}
        </AuthGuard>
      );

      // Should not crash and should render nothing
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });

    it('should handle multiple children', () => {
      mockUseAuth.mockReturnValue({
        user: {
          id: 'user123',
          email: 'test@example.com',
          username: 'testuser'
        },
        isAuthenticated: true,
        isLoading: false,
        sessionReady: true,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);

      render(
        <AuthGuard>
          <div data-testid="child1">Child 1</div>
          <div data-testid="child2">Child 2</div>
        </AuthGuard>
      );

      expect(screen.getByTestId('child1')).toBeInTheDocument();
      expect(screen.getByTestId('child2')).toBeInTheDocument();
    });

    it('should handle complex fallback components', () => {
      mockUseAuth.mockReturnValue({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        sessionReady: true,
        login: jest.fn(),
        logout: jest.fn(),
        signup: jest.fn(),
        resetPassword: jest.fn(),
        updateProfile: jest.fn()
      } as any);

      const ComplexFallback = () => (
        <div>
          <h1 data-testid="fallback-title">Access Denied</h1>
          <p data-testid="fallback-message">You need to log in</p>
          <button data-testid="fallback-button">Sign In</button>
        </div>
      );

      render(
        <AuthGuard fallback={<ComplexFallback />}>
          <MockedChildComponent />
        </AuthGuard>
      );

      expect(screen.getByTestId('fallback-title')).toBeInTheDocument();
      expect(screen.getByTestId('fallback-message')).toBeInTheDocument();
      expect(screen.getByTestId('fallback-button')).toBeInTheDocument();
      expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
    });
  });
});