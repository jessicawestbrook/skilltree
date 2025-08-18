import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { 
  EnvelopeIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  ArrowPathIcon 
} from '@heroicons/react/24/outline'

const EmailVerificationPage: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [verifying, setVerifying] = useState(true)
  const [verified, setVerified] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [resending, setResending] = useState(false)
  const [resendMessage, setResendMessage] = useState<string | null>(null)

  useEffect(() => {
    // Check if user is already verified
    if (user?.email_confirmed_at) {
      setVerified(true)
      setVerifying(false)
      // Redirect to home after 2 seconds
      setTimeout(() => navigate('/'), 2000)
    } else {
      setVerifying(false)
    }
  }, [user, navigate])

  const handleResendVerification = async () => {
    if (!user?.email) return
    
    setResending(true)
    setResendMessage(null)
    setError(null)

    try {
      const { error } = await supabase.auth.resend({
        type: 'signup',
        email: user.email,
        options: {
          emailRedirectTo: `${window.location.origin}/verify-email`
        }
      })

      if (error) throw error

      setResendMessage('Verification email sent! Please check your inbox.')
    } catch (err: any) {
      setError(err.message || 'Failed to resend verification email')
    } finally {
      setResending(false)
    }
  }

  if (verifying) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-neutral-900 dark:to-neutral-800">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-neutral-600 dark:text-neutral-400">Verifying your email...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-neutral-900 dark:to-neutral-800 px-4">
      <div className="max-w-md w-full">
        <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            {verified ? (
              <>
                <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full mb-4">
                  <CheckCircleIcon className="h-8 w-8 text-green-600 dark:text-green-400" />
                </div>
                <h2 className="text-3xl font-bold text-neutral-900 dark:text-white">
                  Email Verified!
                </h2>
                <p className="text-neutral-600 dark:text-neutral-400 mt-2">
                  Your email has been successfully verified. Redirecting you to the app...
                </p>
              </>
            ) : (
              <>
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                  <EnvelopeIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
                </div>
                <h2 className="text-3xl font-bold text-neutral-900 dark:text-white">
                  Verify Your Email
                </h2>
                <p className="text-neutral-600 dark:text-neutral-400 mt-2">
                  {user?.email ? (
                    <>We've sent a verification email to <strong>{user.email}</strong></>
                  ) : (
                    'Please check your email for a verification link'
                  )}
                </p>
              </>
            )}
          </div>

          {!verified && (
            <>
              {error && (
                <div className="mb-6 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 flex items-start">
                  <XCircleIcon className="h-5 w-5 mr-2 flex-shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              {resendMessage && (
                <div className="mb-6 p-4 rounded-lg bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 flex items-start">
                  <CheckCircleIcon className="h-5 w-5 mr-2 flex-shrink-0 mt-0.5" />
                  <span>{resendMessage}</span>
                </div>
              )}

              <div className="space-y-4">
                <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-4">
                  <h3 className="font-semibold mb-2">Didn't receive the email?</h3>
                  <ul className="text-sm text-neutral-600 dark:text-neutral-400 space-y-1">
                    <li>• Check your spam or junk folder</li>
                    <li>• Make sure you entered the correct email</li>
                    <li>• Wait a few minutes and try again</li>
                  </ul>
                </div>

                <button
                  onClick={handleResendVerification}
                  disabled={resending || !user}
                  className="w-full btn-primary py-3 font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  {resending ? (
                    <>
                      <ArrowPathIcon className="h-5 w-5 mr-2 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <EnvelopeIcon className="h-5 w-5 mr-2" />
                      Resend Verification Email
                    </>
                  )}
                </button>

                <div className="text-center">
                  <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                    You can still use the app while your email is being verified
                  </p>
                  <Link 
                    to="/" 
                    className="text-primary-600 hover:text-primary-700 dark:text-primary-400 font-medium"
                  >
                    Continue to App →
                  </Link>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default EmailVerificationPage