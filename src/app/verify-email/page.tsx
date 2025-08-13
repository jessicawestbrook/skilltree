'use client';

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { CheckCircle, XCircle, Loader2, ArrowRight } from 'lucide-react';

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const verifyEmail = async () => {
      const token = searchParams.get('token');

      if (!token) {
        setStatus('error');
        setMessage('No verification token provided. Please check your email for the correct link.');
        return;
      }

      try {
        const response = await fetch(`/api/auth/verify-email?token=${token}`);
        const data = await response.json();

        if (response.ok && data.success) {
          setStatus('success');
          setMessage(data.message || 'Your email has been verified successfully!');
          
          // Optionally send welcome email (this would need to be done server-side normally)
          // The welcome email should be sent from the API endpoint
          
          // Redirect to login after 3 seconds
          setTimeout(() => {
            router.push('/');
          }, 3000);
        } else {
          setStatus('error');
          setMessage(data.error || 'Failed to verify email. The link may be invalid or expired.');
        }
      } catch (error) {
        setStatus('error');
        setMessage('An error occurred while verifying your email. Please try again.');
        console.error('Verification error:', error);
      }
    };

    verifyEmail();
  }, [searchParams, router]);

  const styles = {
    container: {
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px'
    },
    card: {
      background: 'white',
      borderRadius: '20px',
      padding: '60px 40px',
      maxWidth: '500px',
      width: '100%',
      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
      textAlign: 'center' as const
    },
    iconContainer: {
      marginBottom: '30px'
    },
    title: {
      fontSize: '28px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '20px'
    },
    message: {
      fontSize: '16px',
      color: '#666',
      lineHeight: '1.6',
      marginBottom: '30px'
    },
    button: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '10px',
      padding: '15px 30px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      border: 'none',
      borderRadius: '30px',
      fontSize: '16px',
      fontWeight: 'bold',
      cursor: 'pointer',
      textDecoration: 'none',
      transition: 'transform 0.2s ease',
      boxShadow: '0 4px 15px rgba(102, 126, 234, 0.3)'
    },
    redirectText: {
      fontSize: '14px',
      color: '#999',
      marginTop: '20px'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.iconContainer}>
          {status === 'loading' && (
            <Loader2 size={64} color="#667eea" style={{ animation: 'spin 1s linear infinite' }} />
          )}
          {status === 'success' && (
            <CheckCircle size={64} color="#4caf50" />
          )}
          {status === 'error' && (
            <XCircle size={64} color="#ff4444" />
          )}
        </div>

        <h1 style={styles.title}>
          {status === 'loading' && 'Verifying Your Email...'}
          {status === 'success' && 'Email Verified!'}
          {status === 'error' && 'Verification Failed'}
        </h1>

        <p style={styles.message}>
          {status === 'loading' && 'Please wait while we verify your email address.'}
          {status === 'success' && message}
          {status === 'error' && message}
        </p>

        {status === 'success' && (
          <>
            <button
              onClick={() => router.push('/')}
              style={styles.button}
              onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
              onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
            >
              Go to NeuroQuest
              <ArrowRight size={20} />
            </button>
            <p style={styles.redirectText}>
              Redirecting you to the home page in a few seconds...
            </p>
          </>
        )}

        {status === 'error' && (
          <button
            onClick={() => router.push('/')}
            style={styles.button}
            onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
            onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
          >
            Back to Home
            <ArrowRight size={20} />
          </button>
        )}
      </div>

      <style jsx>{`
        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }}>
        <Loader2 size={64} color="white" style={{ animation: 'spin 1s linear infinite' }} />
      </div>
    }>
      <VerifyEmailContent />
    </Suspense>
  );
}