import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AuthModal } from '../../components/AuthModal';

// Mock the AuthContext
const mockLogin = jest.fn();
const mockRegister = jest.fn();
const mockResetPassword = jest.fn();
const mockGetRememberedEmail = jest.fn();

jest.mock('../../contexts/AuthContext', () => ({
  useAuth: () => ({
    login: mockLogin,
    register: mockRegister,
    resetPassword: mockResetPassword,
    isLoading: false,
    error: null,
    getRememberedEmail: mockGetRememberedEmail
  })
}));

// Mock Lucide React icons
jest.mock('lucide-react', () => ({
  X: () => <div data-testid="x-icon">X</div>,
  User: () => <div data-testid="user-icon">User</div>,
  Mail: () => <div data-testid="mail-icon">Mail</div>,
  Eye: () => <div data-testid="eye-icon">Eye</div>,
  EyeOff: () => <div data-testid="eye-off-icon">EyeOff</div>,
  UserPlus: () => <div data-testid="user-plus-icon">UserPlus</div>,
  LogIn: () => <div data-testid="log-in-icon">LogIn</div>,
  KeyRound: () => <div data-testid="key-round-icon">KeyRound</div>
}));

describe('AuthModal', () => {
  const mockOnClose = jest.fn();
  const mockOnSuccess = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    mockLogin.mockResolvedValue({ success: true });
    mockRegister.mockResolvedValue({ success: true });
    mockResetPassword.mockResolvedValue({ success: true });
    mockGetRememberedEmail.mockReturnValue(null);
  });

  describe('Modal visibility', () => {
    it('should not render when isOpen is false', () => {
      render(
        <AuthModal isOpen={false} onClose={mockOnClose} />
      );
      
      expect(screen.queryByText('Welcome Back')).not.toBeInTheDocument();
    });

    it('should render when isOpen is true', () => {
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} />
      );
      
      expect(screen.getByText('Welcome Back')).toBeInTheDocument();
    });
  });

  describe('Login form', () => {
    beforeEach(() => {
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} onSuccess={mockOnSuccess} />
      );
    });

    it('should render login form by default', () => {
      expect(screen.getByText('Welcome Back')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Email address')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
    });

    it('should handle form input changes', async () => {
      const user = userEvent.setup();
      const emailInput = screen.getByPlaceholderText('Email address');
      const passwordInput = screen.getByPlaceholderText('Password');

      await user.type(emailInput, 'test@example.com');
      await user.type(passwordInput, 'password123');

      expect(emailInput).toHaveValue('test@example.com');
      expect(passwordInput).toHaveValue('password123');
    });

    it('should toggle password visibility', async () => {
      const user = userEvent.setup();
      const passwordInput = screen.getByPlaceholderText('Password');
      const toggleButton = passwordInput.parentElement?.querySelector('button');

      expect(passwordInput).toHaveAttribute('type', 'password');

      if (toggleButton) {
        await user.click(toggleButton);
        expect(passwordInput).toHaveAttribute('type', 'text');

        await user.click(toggleButton);
        expect(passwordInput).toHaveAttribute('type', 'password');
      }
    });

    it('should call login and onSuccess on form submission', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.type(screen.getByPlaceholderText('Password'), 'password123');
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      await waitFor(() => {
        expect(mockLogin).toHaveBeenCalledWith({
          email: 'test@example.com',
          password: 'password123',
          rememberMe: false
        });
      });

      await waitFor(() => {
        expect(mockOnSuccess).toHaveBeenCalled();
      });
    });
  });

  describe('Registration form', () => {
    beforeEach(() => {
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} onSuccess={mockOnSuccess} />
      );
      fireEvent.click(screen.getByText('Sign up'));
    });

    it('should switch to registration form', () => {
      expect(screen.getByText('Join SkillTree')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /create account/i })).toBeInTheDocument();
    });

    it('should call register and onSuccess on form submission', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.type(screen.getByPlaceholderText('Username'), 'testuser');
      await user.type(screen.getByPlaceholderText('Password'), 'password123');
      await user.click(screen.getByRole('button', { name: /create account/i }));

      await waitFor(() => {
        expect(mockRegister).toHaveBeenCalledWith({
          email: 'test@example.com',
          password: 'password123',
          username: 'testuser'
        });
      });

      await waitFor(() => {
        expect(mockOnSuccess).toHaveBeenCalled();
      });
    });
  });

  describe('Forgot password form', () => {
    beforeEach(() => {
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} onSuccess={mockOnSuccess} />
      );
      fireEvent.click(screen.getByText('Forgot password?'));
    });

    it('should switch to forgot password form', () => {
      expect(screen.getByText('Reset Password')).toBeInTheDocument();
      expect(screen.getByText(/Enter your email address/)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /send reset email/i })).toBeInTheDocument();
    });

    it('should call resetPassword on form submission', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.click(screen.getByRole('button', { name: /send reset email/i }));

      await waitFor(() => {
        expect(mockResetPassword).toHaveBeenCalledWith('test@example.com');
      });
    });
  });

  describe('Modal close', () => {
    it('should call onClose when close button is clicked', async () => {
      const user = userEvent.setup();
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} />
      );

      const closeButton = screen.getByTestId('x-icon').parentElement;
      if (closeButton) {
        await user.click(closeButton);
        expect(mockOnClose).toHaveBeenCalled();
      }
    });
  });

  describe('Form switching', () => {
    it('should clear form data when switching between modes', async () => {
      const user = userEvent.setup();
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} />
      );

      // Fill login form
      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.type(screen.getByPlaceholderText('Password'), 'password123');

      // Switch to registration
      await user.click(screen.getByText('Sign up'));

      // Check that form is cleared
      expect(screen.getByPlaceholderText('Email address')).toHaveValue('');
      expect(screen.getByPlaceholderText('Password')).toHaveValue('');
      expect(screen.getByPlaceholderText('Username')).toHaveValue('');
    });
  });

  describe('Remember me functionality', () => {
    it('should include rememberMe in login credentials when checked', async () => {
      const user = userEvent.setup();
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} onSuccess={mockOnSuccess} />
      );

      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.type(screen.getByPlaceholderText('Password'), 'password123');
      
      const rememberMeCheckbox = screen.getByLabelText('Remember me');
      await user.click(rememberMeCheckbox);
      
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      await waitFor(() => {
        expect(mockLogin).toHaveBeenCalledWith({
          email: 'test@example.com',
          password: 'password123',
          rememberMe: true
        });
      });
    });

    it('should pre-populate email from remembered credentials', () => {
      mockGetRememberedEmail.mockReturnValue('remembered@example.com');
      
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} />
      );

      expect(screen.getByPlaceholderText('Email address')).toHaveValue('remembered@example.com');
      expect(screen.getByLabelText('Remember me')).toBeChecked();
    });
  });

  describe('Email verification flow', () => {
    it('should show verification message when registration requires verification', async () => {
      mockRegister.mockResolvedValue({ 
        success: true, 
        requiresVerification: true 
      });

      const user = userEvent.setup();
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} />
      );

      await user.click(screen.getByText('Sign up'));
      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.type(screen.getByPlaceholderText('Username'), 'testuser');
      await user.type(screen.getByPlaceholderText('Password'), 'password123');
      await user.click(screen.getByRole('button', { name: /create account/i }));

      await waitFor(() => {
        expect(screen.getByText('Registration Successful!')).toBeInTheDocument();
        expect(screen.getByText(/Your account has been created for/)).toBeInTheDocument();
      });
    });
  });

  describe('Password reset flow', () => {
    it('should show success message after sending reset email', async () => {
      const user = userEvent.setup();
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} />
      );

      await user.click(screen.getByText('Forgot password?'));
      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.click(screen.getByRole('button', { name: /send reset email/i }));

      await waitFor(() => {
        expect(screen.getByText('✓ Password reset email sent!')).toBeInTheDocument();
        expect(screen.getByText(/Please check your email for instructions/)).toBeInTheDocument();
      });
    });
  });

  describe('Error handling', () => {
    it('should handle form interactions correctly', () => {
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} />
      );

      // Test that all basic form elements are present
      expect(screen.getByPlaceholderText('Email address')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
    });

    it('should handle form submission without errors', async () => {
      const user = userEvent.setup();
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} onSuccess={mockOnSuccess} />
      );

      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.type(screen.getByPlaceholderText('Password'), 'password123');

      // Form submission should not throw
      expect(() => {
        fireEvent.click(screen.getByRole('button', { name: /sign in/i }));
      }).not.toThrow();
    });

    it('should keep modal open when login fails with email not confirmed error', async () => {
      // Mock login to return failure with email not confirmed error
      mockLogin.mockResolvedValue({ 
        success: false, 
        error: 'Please check your email and click the verification link to confirm your account before signing in.' 
      });

      const user = userEvent.setup();
      render(
        <AuthModal isOpen={true} onClose={mockOnClose} onSuccess={mockOnSuccess} />
      );

      await user.type(screen.getByPlaceholderText('Email address'), 'unverified@example.com');
      await user.type(screen.getByPlaceholderText('Password'), 'password123');
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Wait for the login attempt to complete
      await waitFor(() => {
        expect(mockLogin).toHaveBeenCalledWith({
          email: 'unverified@example.com',
          password: 'password123',
          rememberMe: false
        });
      });

      // Modal should still be open (onClose should not be called)
      expect(mockOnClose).not.toHaveBeenCalled();
      expect(mockOnSuccess).not.toHaveBeenCalled();

      // Modal content should still be visible
      expect(screen.getByText('Welcome Back')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Email address')).toBeInTheDocument();
    });
  });
});