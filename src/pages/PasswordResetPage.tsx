import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { EnvelopeIcon, ArrowLeftIcon } from '@heroicons/react/24/outline'

const PasswordResetPage: React.FC = () => {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  const handlePasswordReset = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    try {
      const { error } = await (supabase.auth as any).resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`,
      })

      if (error) throw error

      setMessage({
        type: 'success',
        text: 'Password reset instructions have been sent to your email!'
      })
      setEmail('')
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.message || 'Failed to send reset email. Please try again.'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-neutral-900 dark:to-neutral-800 px-4">
      <div className="max-w-md w-full">
        <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
              <EnvelopeIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
            </div>
            <h2 className="text-3xl font-bold text-neutral-900 dark:text-white">
              Reset Password
            </h2>
            <p className="text-neutral-600 dark:text-neutral-400 mt-2">
              Enter your email and we'll send you instructions to reset your password
            </p>
          </div>

          {message && (
            <div className={`mb-6 p-4 rounded-lg ${
              message.type === 'success' 
                ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400' 
                : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400'
            }`}>
              {message.text}
            </div>
          )}

          <form onSubmit={handlePasswordReset} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-700"
                placeholder="you@example.com"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-3 font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Sending...' : 'Send Reset Instructions'}
            </button>
          </form>

          <div className="mt-8 text-center space-y-4">
            <Link 
              to="/login" 
              className="flex items-center justify-center text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400"
            >
              <ArrowLeftIcon className="h-4 w-4 mr-2" />
              Back to Sign In
            </Link>
            
            <div className="text-sm text-neutral-600 dark:text-neutral-400">
              Don't have an account?{' '}
              <Link to="/signup" className="text-primary-600 hover:text-primary-700 dark:text-primary-400 font-medium">
                Sign up
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PasswordResetPage