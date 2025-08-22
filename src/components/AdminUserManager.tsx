import React, { useState, useEffect } from 'react'
import { supabase } from '../services/supabase'
import { UserIcon, ShieldCheckIcon } from '@heroicons/react/24/outline'

interface UserProfile {
  id: string
  email: string
  username?: string
  is_admin: boolean
  created_at: string
}

const AdminUserManager: React.FC = () => {
  const [users, setUsers] = useState<UserProfile[]>([])
  const [loading, setLoading] = useState(true)
  const [updating, setUpdating] = useState<string | null>(null)
  const [searchEmail, setSearchEmail] = useState('')

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('id, email, username, is_admin, created_at')
        .order('created_at', { ascending: false })
        .limit(50)

      if (error) throw error
      setUsers(data || [])
    } catch (error) {
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleAdminStatus = async (userId: string, currentStatus: boolean) => {
    setUpdating(userId)
    try {
      const { error } = await supabase
        .from('profiles')
        .update({ 
          is_admin: !currentStatus,
          updated_at: new Date().toISOString()
        })
        .eq('id', userId)

      if (error) throw error

      // Update local state
      setUsers(users.map(user => 
        user.id === userId 
          ? { ...user, is_admin: !currentStatus }
          : user
      ))
    } catch (error) {
      console.error('Error updating admin status:', error)
    } finally {
      setUpdating(null)
    }
  }

  const filteredUsers = users.filter(user => 
    user.email?.toLowerCase().includes(searchEmail.toLowerCase()) ||
    user.username?.toLowerCase().includes(searchEmail.toLowerCase())
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">User Management</h3>
        
        {/* Search */}
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search by email or username..."
            value={searchEmail}
            onChange={(e) => setSearchEmail(e.target.value)}
            className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
          />
        </div>
      </div>

      {/* Users List */}
      <div className="space-y-2">
        {filteredUsers.map((user) => (
          <div
            key={user.id}
            className="flex items-center justify-between p-4 bg-white dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700"
          >
            <div className="flex items-center gap-3">
              <UserIcon className="h-5 w-5 text-neutral-500" />
              <div>
                <p className="font-medium">{user.email}</p>
                {user.username && (
                  <p className="text-sm text-neutral-500">@{user.username}</p>
                )}
                <p className="text-xs text-neutral-400">
                  Joined: {new Date(user.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {user.is_admin && (
                <div className="flex items-center gap-1 px-2 py-1 bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400 rounded-md">
                  <ShieldCheckIcon className="h-4 w-4" />
                  <span className="text-xs font-medium">Admin</span>
                </div>
              )}
              
              <button
                onClick={() => toggleAdminStatus(user.id, user.is_admin)}
                disabled={updating === user.id}
                className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                  user.is_admin
                    ? 'bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/40'
                    : 'bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 hover:bg-blue-200 dark:hover:bg-blue-900/40'
                }`}
              >
                {updating === user.id ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
                ) : user.is_admin ? (
                  'Remove Admin'
                ) : (
                  'Make Admin'
                )}
              </button>
            </div>
          </div>
        ))}

        {filteredUsers.length === 0 && (
          <div className="text-center py-8 text-neutral-500">
            No users found
          </div>
        )}
      </div>

      <div className="text-sm text-neutral-500 bg-yellow-50 dark:bg-yellow-900/10 p-3 rounded-lg">
        <strong>⚠️ Warning:</strong> Admin users have full access to the admin dashboard, 
        content management, and user data. Only grant admin privileges to trusted users.
      </div>
    </div>
  )
}

export default AdminUserManager