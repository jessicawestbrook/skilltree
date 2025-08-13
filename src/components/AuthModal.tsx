import React, { useState, useEffect, CSSProperties } from 'react';
import { X, User, Mail, Eye, EyeOff, UserPlus, LogIn, KeyRound } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [isForgotPassword, setIsForgotPassword] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [resetEmailSent, setResetEmailSent] = useState(false);
  const [verificationEmailSent, setVerificationEmailSent] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: '',
    rememberMe: false
  });

  const { login, register, resetPassword, isLoading, error, getRememberedEmail } = useAuth();

  // Handle modal close - reset all states
  const handleModalClose = () => {
    // Reset all form states
    setIsLogin(true);
    setIsForgotPassword(false);
    setShowPassword(false);
    setResetEmailSent(false);
    setVerificationEmailSent(false);
    setFormData({ email: '', password: '', username: '', rememberMe: false });
    // Call the parent onClose
    onClose();
  };

  // Pre-populate email field with remembered credentials when modal opens
  useEffect(() => {
    if (isOpen && isLogin && !isForgotPassword) {
      const rememberedEmail = getRememberedEmail();
      if (rememberedEmail) {
        setFormData(prev => ({
          ...prev,
          email: rememberedEmail,
          rememberMe: true // Also check the remember me box
        }));
      }
    }
  }, [isOpen, isLogin, isForgotPassword, getRememberedEmail]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    let result;
    if (isForgotPassword) {
      result = await resetPassword(formData.email);
      if (result.success) {
        setResetEmailSent(true);
      }
      // Keep modal open to show error or success state
      return;
    } else if (isLogin) {
      result = await login({
        email: formData.email,
        password: formData.password,
        rememberMe: formData.rememberMe
      });
    } else {
      result = await register({
        email: formData.email,
        password: formData.password,
        username: formData.username
      });
      if (result?.success && result?.requiresVerification) {
        setVerificationEmailSent(true);
        return;
      }
    }

    // Only close modal on successful login/register (not on error)
    if (result?.success === true && !isForgotPassword && !verificationEmailSent) {
      // Success - close modal and trigger success callback
      handleModalClose();
      if (onSuccess) {
        onSuccess();
      }
    } else if (result?.success === false) {
      // Explicitly handle error case - keep modal open
      console.log('Authentication failed, keeping modal open. Error:', result.error);
      // Modal stays open to display the error
    }
    // The error will be displayed through the error prop from useAuth
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const switchMode = () => {
    setIsLogin(!isLogin);
    setIsForgotPassword(false);
    setResetEmailSent(false);
    setVerificationEmailSent(false);
    setFormData({ email: '', password: '', username: '', rememberMe: false });
  };

  const handleForgotPassword = () => {
    setIsForgotPassword(true);
    setResetEmailSent(false);
    setFormData({ email: '', password: '', username: '', rememberMe: false });
  };

  const handleBackToLogin = () => {
    setIsForgotPassword(false);
    setResetEmailSent(false);
    setVerificationEmailSent(false);
    setIsLogin(true);
    setFormData({ email: '', password: '', username: '', rememberMe: false });
  };

  if (!isOpen) return null;

  const styles = {
    overlay: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.8)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
      padding: '20px'
    } as CSSProperties,
    modal: {
      background: 'white',
      borderRadius: '20px',
      padding: '40px',
      maxWidth: '450px',
      width: '100%',
      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)'
    } as CSSProperties,
    header: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '30px'
    } as CSSProperties,
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      display: 'flex',
      alignItems: 'center',
      gap: '10px'
    } as CSSProperties,
    form: {
      display: 'flex',
      flexDirection: 'column',
      gap: '20px'
    } as CSSProperties,
    inputGroup: {
      position: 'relative'
    } as CSSProperties,
    input: {
      width: '100%',
      padding: '15px 50px 15px 15px',
      border: '2px solid #e0e0e0',
      borderRadius: '12px',
      fontSize: '16px',
      color: '#2a2a2a',
      backgroundColor: '#ffffff',
      transition: 'border-color 0.3s ease',
      outline: 'none'
    } as CSSProperties,
    inputFocus: {
      borderColor: '#667eea'
    } as CSSProperties,
    inputIcon: {
      position: 'absolute',
      right: '15px',
      top: '50%',
      transform: 'translateY(-50%)',
      color: '#999'
    } as CSSProperties,
    passwordToggle: {
      position: 'absolute',
      right: '15px',
      top: '50%',
      transform: 'translateY(-50%)',
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      color: '#999',
      padding: '0'
    } as CSSProperties,
    submitButton: {
      padding: '15px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      border: 'none',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: 'bold',
      cursor: isLoading ? 'not-allowed' : 'pointer',
      transition: 'all 0.3s ease',
      opacity: isLoading ? 0.7 : 1,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '8px'
    } as CSSProperties,
    switchText: {
      textAlign: 'center',
      marginTop: '20px',
      fontSize: '14px',
      color: '#666'
    } as CSSProperties,
    switchButton: {
      background: 'none',
      border: 'none',
      color: '#667eea',
      cursor: 'pointer',
      fontWeight: 'bold',
      textDecoration: 'underline'
    } as CSSProperties,
    error: {
      color: '#ff4444',
      fontSize: '14px',
      textAlign: 'center',
      marginTop: '10px',
      padding: '10px',
      background: '#ffebee',
      borderRadius: '8px',
      border: '1px solid #ff4444'
    } as CSSProperties,
    checkboxGroup: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      marginTop: '5px',
      marginBottom: '10px'
    } as CSSProperties,
    checkbox: {
      width: '16px',
      height: '16px',
      accentColor: '#667eea',
      cursor: 'pointer'
    } as CSSProperties,
    checkboxLabel: {
      fontSize: '14px',
      color: '#666',
      cursor: 'pointer',
      userSelect: 'none'
    } as CSSProperties
  };

  return (
    <div 
      style={styles.overlay}
      onClick={(e) => {
        // Close modal when clicking on overlay (not modal content)
        if (e.target === e.currentTarget) {
          handleModalClose();
        }
      }}
    >
      <div style={styles.modal}>
        <div style={styles.header}>
          <h2 style={styles.title}>
            {isForgotPassword ? (
              <>
                <KeyRound size={28} />
                Reset Password
              </>
            ) : isLogin ? (
              <>
                <LogIn size={28} />
                Welcome Back
              </>
            ) : (
              <>
                <UserPlus size={28} />
                Join NeuroQuest
              </>
            )}
          </h2>
          <button
            onClick={handleModalClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer' }}
          >
            <X size={24} color="#999" />
          </button>
        </div>

        {resetEmailSent ? (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <div style={{ marginBottom: '20px', color: '#4caf50' }}>
              ✓ Password reset email sent!
            </div>
            <p style={{ color: '#666', marginBottom: '20px' }}>
              Please check your email for instructions to reset your password.
            </p>
            <button
              onClick={handleBackToLogin}
              style={styles.submitButton}
            >
              Back to Sign In
            </button>
          </div>
        ) : verificationEmailSent ? (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <div style={{ marginBottom: '20px', color: '#4caf50', fontSize: '48px' }}>
              ✅
            </div>
            <h3 style={{ color: '#2a2a2a', marginBottom: '20px' }}>
              Registration Successful!
            </h3>
            <p style={{ color: '#666', marginBottom: '20px', lineHeight: '1.6' }}>
              Your account has been created for <strong>{formData.email}</strong>.
            </p>
            <p style={{ color: '#999', fontSize: '14px', marginBottom: '20px' }}>
              Note: Email verification is currently disabled in development mode.
              You can now sign in with your credentials.
            </p>
            <button
              onClick={handleBackToLogin}
              style={styles.submitButton}
            >
              Continue to Sign In
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={styles.form}>
            {isForgotPassword && (
              <p style={{ color: '#666', marginBottom: '10px', fontSize: '14px' }}>
                Enter your email address and we&apos;ll send you a link to reset your password.
              </p>
            )}
            
            <div style={styles.inputGroup}>
              <input
                type="email"
                name="email"
                placeholder="Email address"
                value={formData.email}
                onChange={handleChange}
                required
                style={styles.input}
              />
              <Mail size={20} style={styles.inputIcon} />
            </div>

            {!isLogin && !isForgotPassword && (
              <>
                <div style={styles.inputGroup}>
                  <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    style={styles.input}
                  />
                  <User size={20} style={styles.inputIcon} />
                </div>
              </>
            )}

            {!isForgotPassword && (
              <div style={styles.inputGroup}>
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  placeholder="Password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  style={styles.input}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={styles.passwordToggle}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            )}

            {isLogin && !isForgotPassword && (
              <>
                <div style={styles.checkboxGroup}>
                  <input
                    type="checkbox"
                    id="rememberMe"
                    name="rememberMe"
                    checked={formData.rememberMe}
                    onChange={handleChange}
                    style={styles.checkbox}
                  />
                  <label htmlFor="rememberMe" style={styles.checkboxLabel}>
                    Remember me
                  </label>
                </div>
                <div style={{ textAlign: 'right', marginTop: '-5px' }}>
                  <button
                    type="button"
                    onClick={handleForgotPassword}
                    style={{ 
                      ...styles.switchButton, 
                      fontSize: '13px',
                      textDecoration: 'none'
                    }}
                  >
                    Forgot password?
                  </button>
                </div>
              </>
            )}

            {error && <div style={styles.error}>{error}</div>}

            <button type="submit" style={styles.submitButton} disabled={isLoading}>
              {isLoading ? (
                'Processing...'
              ) : isForgotPassword ? (
                <>
                  <Mail size={20} />
                  Send Reset Email
                </>
              ) : isLogin ? (
                <>
                  <LogIn size={20} />
                  Sign In
                </>
              ) : (
                <>
                  <UserPlus size={20} />
                  Create Account
                </>
              )}
            </button>
          </form>
        )}

        {!resetEmailSent && !verificationEmailSent && (
          <div style={styles.switchText}>
            {isForgotPassword ? (
              <>
                Remember your password?{' '}
                <button onClick={handleBackToLogin} style={styles.switchButton}>
                  Sign in
                </button>
              </>
            ) : (
              <>
                {isLogin ? "Don't have an account? " : "Already have an account? "}
                <button onClick={switchMode} style={styles.switchButton}>
                  {isLogin ? 'Sign up' : 'Sign in'}
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};