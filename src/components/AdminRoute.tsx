import React, { useState, useEffect } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'

interface AdminRouteProps {
  children: React.ReactNode
}

const AdminRoute: React.FC<AdminRouteProps> = ({ children }) => {
  const { user, loading: authLoading } = useAuth()
  const [isAdmin, setIsAdmin] = useState<boolean | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAdminStatus()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const checkAdminStatus = async () => {
    if (!user) {
      setIsAdmin(false)
      setLoading(false)
      return
    }

    try {
      console.log('Checking admin status for user:', user.id)
      
      const { data, error } = await supabase
        .from('profiles')
        .select('is_admin')
        .eq('id', user.id)
        .maybeSingle() // Use maybeSingle instead of single to handle no rows gracefully

      if (error) {
        console.error('Error checking admin status:', error)
        // If no profile exists, create one
        if (error.code === 'PGRST116') {
          console.log('No profile found, creating one...')
          const { error: insertError } = await supabase
            .from('profiles')
            .insert({
              id: user.id,
              email: user.email,
              is_admin: false,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString()
            })
          
          if (insertError) {
            console.error('Error creating profile:', insertError)
          }
        }
        setIsAdmin(false)
      } else if (!data) {
        console.log('No profile data returned')
        setIsAdmin(false)
      } else {
        console.log('Admin status:', data.is_admin)
        setIsAdmin(data.is_admin === true)
      }
    } catch (error) {
      console.error('Error checking admin status:', error)
      setIsAdmin(false)
    } finally {
      setLoading(false)
    }
  }

  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (!isAdmin) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4 text-neutral-800 dark:text-neutral-200">Access Denied</h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            You don't have permission to access this page.
          </p>
          <Navigate to="/" replace />
        </div>
      </div>
    )
  }

  return <>{children}</>
}

export default AdminRoute