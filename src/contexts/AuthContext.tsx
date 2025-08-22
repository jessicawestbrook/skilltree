import React, { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../services/supabase'

interface AuthContextType {
  user: any | null
  session: any | null
  loading: boolean
  signUp: (email: string, password: string, username?: string) => Promise<any>
  signIn: (email: string, password: string) => Promise<any>
  signOut: () => Promise<any>
  resetPassword: (email: string) => Promise<any>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any | null>(null)
  const [session, setSession] = useState<any | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    (supabase.auth as any).getSession().then(({ data: { session } }: any) => {
      setSession(session)
      setUser(session?.user ?? null)
      setLoading(false)
    })

    const { data } = (supabase.auth as any).onAuthStateChange((_event: any, session: any) => {
      setSession(session)
      setUser(session?.user ?? null)
    })

    return () => data.subscription.unsubscribe()
  }, [])

  const signUp = async (email: string, password: string, username?: string) => {
    try {
      // First check if username is available if provided
      if (username) {
        const { data: existingProfile, error: checkError } = await supabase
          .from('profiles')
          .select('username')
          .eq('username', username)
          .single()
        
        if (existingProfile && !checkError) {
          return { data: null, error: { message: 'Username is already taken' } }
        }
      }

      const { data, error } = await (supabase.auth as any).signUp({
        email,
        password,
        options: {
          emailRedirectTo: `${window.location.origin}/verify-email`
        }
      })
      
      // If signup is successful and username is provided, create/update profile
      if (data?.user && !error && username) {
        const { error: profileError } = await supabase
          .from('profiles')
          .upsert({
            id: data.user.id,
            email: data.user.email,
            username: username,
            updated_at: new Date().toISOString()
          })
        
        if (profileError) {
          console.error('Profile creation error:', profileError)
          // Don't fail the signup if profile creation fails, just log it
        }
      }
      
      // Log for debugging
      if (error) {
        console.error('SignUp Error:', error)
      } else {
        console.log('SignUp Success:', data)
      }
      
      return { data, error }
    } catch (err) {
      console.error('SignUp Exception:', err)
      return { data: null, error: err }
    }
  }

  const signIn = async (email: string, password: string) => {
    try {
      const { data, error } = await (supabase.auth as any).signInWithPassword({
        email,
        password,
      })
      
      // Log for debugging
      if (error) {
        console.error('SignIn Error:', error)
      } else {
        console.log('SignIn Success:', data)
      }
      
      return { data, error }
    } catch (err) {
      console.error('SignIn Exception:', err)
      return { data: null, error: err }
    }
  }

  const signOut = async () => {
    const { error } = await (supabase.auth as any).signOut()
    return { error }
  }

  const resetPassword = async (email: string) => {
    const { data, error } = await (supabase.auth as any).resetPasswordForEmail(email)
    return { data, error }
  }

  const value = {
    user,
    session,
    loading,
    signUp,
    signIn,
    signOut,
    resetPassword,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}