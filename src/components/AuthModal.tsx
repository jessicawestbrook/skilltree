import React, { useState, CSSProperties } from 'react';
import { X, User, Mail, Eye, EyeOff, UserPlus, LogIn } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: '',
    displayName: ''
  });

  const { login, register, isLoading, error } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    let result;
    if (isLogin) {
      result = await login({
        email: formData.email,
        password: formData.password
      });
    } else {
      result = await register({
        email: formData.email,
        password: formData.password,
        username: formData.username,
        displayName: formData.displayName || formData.username
      });
    }

    if (result.success) {
      onClose();
      setFormData({ email: '', password: '', username: '', displayName: '' });
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const switchMode = () => {
    setIsLogin(!isLogin);
    setFormData({ email: '', password: '', username: '', displayName: '' });
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
    } as CSSProperties
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <div style={styles.header}>
          <h2 style={styles.title}>
            {isLogin ? <LogIn size={28} /> : <UserPlus size={28} />}
            {isLogin ? 'Welcome Back' : 'Join NeuroQuest'}
          </h2>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer' }}
          >
            <X size={24} color="#999" />
          </button>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
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

          {!isLogin && (
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

              <div style={styles.inputGroup}>
                <input
                  type="text"
                  name="displayName"
                  placeholder="Display name (optional)"
                  value={formData.displayName}
                  onChange={handleChange}
                  style={styles.input}
                />
                <User size={20} style={styles.inputIcon} />
              </div>
            </>
          )}

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

          {error && <div style={styles.error}>{error}</div>}

          <button type="submit" style={styles.submitButton} disabled={isLoading}>
            {isLoading ? (
              'Processing...'
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

        <div style={styles.switchText}>
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button onClick={switchMode} style={styles.switchButton}>
            {isLogin ? 'Sign up' : 'Sign in'}
          </button>
        </div>
      </div>
    </div>
  );
};