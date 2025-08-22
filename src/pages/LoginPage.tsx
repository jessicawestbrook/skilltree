import React, { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { AcademicCapIcon, EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline'

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signIn } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    const { error } = await signIn(email, password)
    
    if (error) {
      // Provide more user-friendly error messages
      let errorMessage = error.message
      if (error.message?.includes('Invalid login credentials')) {
        errorMessage = 'Invalid email or password. Please check your credentials and try again.'
      } else if (error.message?.includes('Email not confirmed')) {
        errorMessage = 'Please check your email and click the confirmation link before signing in.'
      } else if (error.message?.includes('Too many requests')) {
        errorMessage = 'Too many login attempts. Please wait a moment and try again.'
      }
      
      setError(errorMessage)
      setLoading(false)
    } else {
      // Get the redirect parameter from URL, fallback to profile page
      const redirectTo = searchParams.get('redirect') || '/profile'
      navigate(redirectTo)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-neutral-900 dark:to-neutral-800">
      <div className="bg-white dark:bg-neutral-800 p-8 rounded-2xl shadow-xl w-full max-w-md">
        <div className="flex justify-center mb-6">
          <Link to="/" className="flex items-center space-x-2">
            <AcademicCapIcon className="h-10 w-10 text-primary-600" />
            <span className="font-game text-3xl text-primary-600 dark:text-primary-400">
              SkillTree
            </span>
          </Link>
        </div>

        <h2 className="text-2xl font-bold text-center mb-6">Welcome Back!</h2>

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium mb-2">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-field"
              required
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium mb-2">
              Password
            </label>
            <div className="relative">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field pr-10"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                {showPassword ? (
                  <EyeSlashIcon className="h-5 w-5 text-neutral-400 hover:text-neutral-600" />
                ) : (
                  <EyeIcon className="h-5 w-5 text-neutral-400 hover:text-neutral-600" />
                )}
              </button>
            </div>
          </div>

          <div className="flex justify-end">
            <Link to="/password-reset" className="text-sm text-primary-600 hover:text-primary-700">
              Forgot password?
            </Link>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full py-3 disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-neutral-600 dark:text-neutral-400">
            Don't have an account?{' '}
            <Link to="/signup" className="text-primary-600 hover:text-primary-700 font-medium">
              Sign Up
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default LoginPage