'use client';

import React, { useState, useEffect, CSSProperties } from 'react';
import { useRouter } from 'next/navigation';
import { KeyRound, Eye, EyeOff, CheckCircle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export default function ResetPasswordPage() {
  const router = useRouter();
  const { updatePassword, isLoading } = useAuth();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    // Check if we have a valid session/token from the email link
    // Supabase handles this automatically through the URL parameters
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    const result = await updatePassword(password);
    
    if (result.success) {
      setSuccess(true);
      setTimeout(() => {
        router.push('/');
      }, 3000);
    } else {
      setError(result.error || 'Failed to reset password');
    }
  };

  const styles = {
    container: {
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px'
    } as CSSProperties,
    card: {
      background: 'white',
      borderRadius: '20px',
      padding: '40px',
      maxWidth: '450px',
      width: '100%',
      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)'
    } as CSSProperties,
    header: {
      textAlign: 'center',
      marginBottom: '30px'
    } as CSSProperties,
    iconContainer: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '80px',
      height: '80px',
      borderRadius: '50%',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      marginBottom: '20px'
    } as CSSProperties,
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '10px'
    } as CSSProperties,
    subtitle: {
      fontSize: '14px',
      color: '#666'
    } as CSSProperties,
    form: {
      display: 'flex',
      flexDirection: 'column',
      gap: '20px'
    } as CSSProperties,
    inputGroup: {
      position: 'relative'
    } as CSSProperties,
    label: {
      display: 'block',
      marginBottom: '8px',
      fontSize: '14px',
      fontWeight: '600',
      color: '#333'
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
    passwordToggle: {
      position: 'absolute',
      right: '15px',
      top: '42px',
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      color: '#999',
      padding: '0'
    } as CSSProperties,
    button: {
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
    error: {
      color: '#ff4444',
      fontSize: '14px',
      textAlign: 'center',
      padding: '10px',
      background: '#ffebee',
      borderRadius: '8px',
      border: '1px solid #ff4444'
    } as CSSProperties,
    success: {
      textAlign: 'center',
      padding: '20px'
    } as CSSProperties,
    successIcon: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '60px',
      height: '60px',
      borderRadius: '50%',
      background: '#4caf50',
      marginBottom: '20px'
    } as CSSProperties,
    successText: {
      fontSize: '18px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '10px'
    } as CSSProperties,
    redirectText: {
      fontSize: '14px',
      color: '#666'
    } as CSSProperties
  };

  if (success) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <div style={styles.success}>
            <div style={styles.successIcon}>
              <CheckCircle size={30} color="white" />
            </div>
            <div style={styles.successText}>Password Reset Successful!</div>
            <div style={styles.redirectText}>Redirecting you to the home page...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <div style={styles.iconContainer}>
            <KeyRound size={40} color="white" />
          </div>
          <h1 style={styles.title}>Reset Your Password</h1>
          <p style={styles.subtitle}>Enter your new password below</p>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>New Password</label>
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter new password"
              required
              minLength={6}
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

          <div style={styles.inputGroup}>
            <label style={styles.label}>Confirm Password</label>
            <input
              type={showConfirmPassword ? 'text' : 'password'}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm new password"
              required
              minLength={6}
              style={styles.input}
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              style={styles.passwordToggle}
            >
              {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          </div>

          {error && <div style={styles.error}>{error}</div>}

          <button type="submit" style={styles.button} disabled={isLoading}>
            {isLoading ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>
      </div>
    </div>
  );
}