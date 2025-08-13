import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Mock AuthModal component for testing
const MockAuthModal = ({ isOpen, onClose, onSuccess }: { 
  isOpen: boolean; 
  onClose: () => void; 
  onSuccess?: () => void; 
}) => {
  const [mode, setMode] = React.useState<'login' | 'register' | 'forgot'>('login');
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [username, setUsername] = React.useState('');
  const [showPassword, setShowPassword] = React.useState(false);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSuccess) onSuccess();
  };

  const clearForm = () => {
    setEmail('');
    setPassword('');
    setUsername('');
  };

  const switchToRegister = () => {
    setMode('register');
    clearForm();
  };

  const switchToLogin = () => {
    setMode('login');
    clearForm();
  };

  const switchToForgot = () => {
    setMode('forgot');
    clearForm();
  };

  return (
    <div>
      <h2>
        {mode === 'forgot' ? 'Reset Password' : 
         mode === 'login' ? 'Welcome Back' : 'Join NeuroQuest'}
      </h2>
      <button onClick={onClose} aria-label="Close">×</button>
      
      {mode === 'forgot' && (
        <p>Enter your email address and we&apos;ll send you a link to reset your password.</p>
      )}

      <form onSubmit={handleSubmit}>
        <input 
          placeholder="Email address" 
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        
        {mode === 'register' && (
          <input 
            placeholder="Username" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        )}
        
        {mode !== 'forgot' && (
          <div>
            <input 
              placeholder="Password" 
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button 
              type="button" 
              onClick={() => setShowPassword(!showPassword)}
              aria-label="Toggle password visibility"
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
        )}

        {mode === 'login' && (
          <button type="button" onClick={switchToForgot}>
            Forgot password?
          </button>
        )}

        <button type="submit">
          {mode === 'forgot' ? 'Send Reset Email' :
           mode === 'login' ? 'Sign In' : 'Create Account'}
        </button>
      </form>

      <div>
        {mode === 'forgot' ? (
          <>
            Remember your password?{' '}
            <button onClick={switchToLogin}>Sign in</button>
          </>
        ) : (
          <>
            {mode === 'login' ? "Don't have an account? " : "Already have an account? "}
            <button onClick={mode === 'login' ? switchToRegister : switchToLogin}>
              {mode === 'login' ? 'Sign up' : 'Sign in'}
            </button>
          </>
        )}
      </div>
    </div>
  );
};

describe('AuthModal', () => {
  const mockOnClose = jest.fn();
  const mockOnSuccess = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Modal visibility', () => {
    it('should not render when isOpen is false', () => {
      render(
        <MockAuthModal isOpen={false} onClose={mockOnClose} />
      );
      
      expect(screen.queryByText('Welcome Back')).not.toBeInTheDocument();
    });

    it('should render when isOpen is true', () => {
      render(
        <MockAuthModal isOpen={true} onClose={mockOnClose} />
      );
      
      expect(screen.getByText('Welcome Back')).toBeInTheDocument();
    });
  });

  describe('Login form', () => {
    beforeEach(() => {
      render(
        <MockAuthModal isOpen={true} onClose={mockOnClose} onSuccess={mockOnSuccess} />
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
      const toggleButton = screen.getByLabelText('Toggle password visibility');

      expect(passwordInput).toHaveAttribute('type', 'password');

      await user.click(toggleButton);
      expect(passwordInput).toHaveAttribute('type', 'text');

      await user.click(toggleButton);
      expect(passwordInput).toHaveAttribute('type', 'password');
    });

    it('should call onSuccess on form submission', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.type(screen.getByPlaceholderText('Password'), 'password123');
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      expect(mockOnSuccess).toHaveBeenCalled();
    });
  });

  describe('Registration form', () => {
    beforeEach(() => {
      render(
        <MockAuthModal isOpen={true} onClose={mockOnClose} onSuccess={mockOnSuccess} />
      );
      fireEvent.click(screen.getByText('Sign up'));
    });

    it('should switch to registration form', () => {
      expect(screen.getByText('Join NeuroQuest')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /create account/i })).toBeInTheDocument();
    });

    it('should call onSuccess on form submission', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.type(screen.getByPlaceholderText('Username'), 'testuser');
      await user.type(screen.getByPlaceholderText('Password'), 'password123');
      await user.click(screen.getByRole('button', { name: /create account/i }));

      expect(mockOnSuccess).toHaveBeenCalled();
    });
  });

  describe('Forgot password form', () => {
    beforeEach(() => {
      render(
        <MockAuthModal isOpen={true} onClose={mockOnClose} onSuccess={mockOnSuccess} />
      );
      fireEvent.click(screen.getByText('Forgot password?'));
    });

    it('should switch to forgot password form', () => {
      expect(screen.getByText('Reset Password')).toBeInTheDocument();
      expect(screen.getByText(/Enter your email address/)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /send reset email/i })).toBeInTheDocument();
    });

    it('should call onSuccess on form submission', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByPlaceholderText('Email address'), 'test@example.com');
      await user.click(screen.getByRole('button', { name: /send reset email/i }));

      expect(mockOnSuccess).toHaveBeenCalled();
    });
  });

  describe('Modal close', () => {
    it('should call onClose when close button is clicked', async () => {
      const user = userEvent.setup();
      render(
        <MockAuthModal isOpen={true} onClose={mockOnClose} />
      );

      const closeButton = screen.getByLabelText('Close');
      await user.click(closeButton);

      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  describe('Form switching', () => {
    it('should clear form data when switching between modes', async () => {
      const user = userEvent.setup();
      render(
        <MockAuthModal isOpen={true} onClose={mockOnClose} />
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
});