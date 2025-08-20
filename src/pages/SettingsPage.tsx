import React, { useState, useEffect } from 'react'
import { useTheme } from '../contexts/ThemeContext'
import { useAuth } from '../contexts/AuthContext'
import { useNotifications } from '../contexts/NotificationContext'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { 
  MoonIcon, 
  SunIcon,
  BellIcon,
  LanguageIcon,
  ShieldCheckIcon,
  UserCircleIcon,
  ArrowLeftIcon
} from '@heroicons/react/24/outline'

interface Setting {
  label: string
  description: string
  control: React.ReactElement
  comingSoon?: boolean
}

interface SettingsSection {
  title: string
  icon: React.ReactElement
  settings: Setting[]
}

const SettingsPage: React.FC = () => {
  const { darkMode, toggleDarkMode } = useTheme()
  const { user } = useAuth()
  const { preferences, updatePreferences } = useNotifications()
  const navigate = useNavigate()
  
  const [currentUsername, setCurrentUsername] = useState<string>('')
  const [newUsername, setNewUsername] = useState<string>('')
  const [isEditingUsername, setIsEditingUsername] = useState(false)
  const [usernameLoading, setUsernameLoading] = useState(false)
  const [usernameError, setUsernameError] = useState<string>('')
  const [usernameSuccess, setUsernameSuccess] = useState<string>('')

  useEffect(() => {
    if (user) {
      fetchUserProfile()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const fetchUserProfile = async () => {
    if (!user) return
    
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('username')
        .eq('id', user.id)
        .single()
      
      if (error) {
        console.error('Error fetching profile:', error)
        // If profile doesn't exist, create one
        if (error.code === 'PGRST116') {
          await supabase
            .from('profiles')
            .insert({ id: user.id, email: user.email })
        }
        return
      }
      
      setCurrentUsername(data.username || '')
    } catch (err) {
      console.error('Error in fetchUserProfile:', err)
    }
  }

  const validateUsername = (username: string) => {
    if (!username.trim()) {
      return 'Username cannot be empty'
    }
    if (username.length < 3) {
      return 'Username must be at least 3 characters long'
    }
    if (username.length > 30) {
      return 'Username must be less than 30 characters'
    }
    if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
      return 'Username can only contain letters, numbers, underscores, and hyphens'
    }
    return null
  }

  const checkUsernameAvailability = async (username: string) => {
    const { data, error } = await supabase
      .from('profiles')
      .select('id')
      .eq('username', username)
      .neq('id', user?.id)
      .single()
    
    if (error && error.code !== 'PGRST116') {
      throw error
    }
    
    return !data // true if available (no data found)
  }

  const handleUsernameUpdate = async () => {
    if (!user || !newUsername) return
    
    setUsernameLoading(true)
    setUsernameError('')
    setUsernameSuccess('')
    
    try {
      // Validate username format
      const validationError = validateUsername(newUsername)
      if (validationError) {
        setUsernameError(validationError)
        return
      }
      
      // Check if username is available
      const isAvailable = await checkUsernameAvailability(newUsername)
      if (!isAvailable) {
        setUsernameError('Username is already taken')
        return
      }
      
      // Update username in database
      const { error } = await supabase
        .from('profiles')
        .upsert({ 
          id: user.id, 
          email: user.email, 
          username: newUsername,
          updated_at: new Date().toISOString()
        })
      
      if (error) throw error
      
      setCurrentUsername(newUsername)
      setNewUsername('')
      setIsEditingUsername(false)
      setUsernameSuccess('Username updated successfully!')
      
      // Clear success message after 3 seconds
      setTimeout(() => setUsernameSuccess(''), 3000)
      
    } catch (error) {
      console.error('Error updating username:', error)
      setUsernameError('Failed to update username. Please try again.')
    } finally {
      setUsernameLoading(false)
    }
  }

  const startEditingUsername = () => {
    setNewUsername(currentUsername)
    setIsEditingUsername(true)
    setUsernameError('')
    setUsernameSuccess('')
  }

  const cancelEditingUsername = () => {
    setNewUsername('')
    setIsEditingUsername(false)
    setUsernameError('')
    setUsernameSuccess('')
  }

  const settingsSections: SettingsSection[] = [
    {
      title: 'Appearance',
      icon: darkMode ? <MoonIcon className="h-5 w-5" /> : <SunIcon className="h-5 w-5" />,
      settings: [
        {
          label: 'Dark Mode',
          description: 'Toggle between light and dark theme',
          control: (
            <button
              onClick={toggleDarkMode}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                darkMode ? 'bg-primary-600' : 'bg-neutral-300'
              }`}
              role="switch"
              aria-checked={darkMode}
            >
              <span className="sr-only">Toggle dark mode</span>
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  darkMode ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          )
        }
      ]
    },
    {
      title: 'Notifications',
      icon: <BellIcon className="h-5 w-5" />,
      settings: [
        {
          label: 'Achievement Notifications',
          description: 'Get notified when you earn achievements and complete learning goals',
          control: (
            <button
              onClick={() => updatePreferences({ achievement_notifications: !preferences?.achievement_notifications })}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                preferences?.achievement_notifications ? 'bg-primary-600' : 'bg-neutral-300'
              }`}
              role="switch"
              aria-checked={preferences?.achievement_notifications}
            >
              <span className="sr-only">Toggle achievement notifications</span>
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  preferences?.achievement_notifications ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          )
        },
        {
          label: 'Progress Updates',
          description: 'Receive updates about your learning progress and milestones',
          control: (
            <button
              onClick={() => updatePreferences({ progress_notifications: !preferences?.progress_notifications })}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                preferences?.progress_notifications ? 'bg-primary-600' : 'bg-neutral-300'
              }`}
              role="switch"
              aria-checked={preferences?.progress_notifications}
            >
              <span className="sr-only">Toggle progress notifications</span>
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  preferences?.progress_notifications ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          )
        },
        {
          label: 'Learning Reminders',
          description: 'Get gentle reminders to continue your learning journey',
          control: (
            <button
              onClick={() => updatePreferences({ reminder_notifications: !preferences?.reminder_notifications })}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                preferences?.reminder_notifications ? 'bg-primary-600' : 'bg-neutral-300'
              }`}
              role="switch"
              aria-checked={preferences?.reminder_notifications}
            >
              <span className="sr-only">Toggle reminder notifications</span>
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  preferences?.reminder_notifications ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          )
        },
        {
          label: 'System Notifications',
          description: 'Important system updates and announcements',
          control: (
            <button
              onClick={() => updatePreferences({ system_notifications: !preferences?.system_notifications })}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                preferences?.system_notifications ? 'bg-primary-600' : 'bg-neutral-300'
              }`}
              role="switch"
              aria-checked={preferences?.system_notifications}
            >
              <span className="sr-only">Toggle system notifications</span>
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  preferences?.system_notifications ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          )
        }
      ]
    },
    {
      title: 'Language & Region',
      icon: <LanguageIcon className="h-5 w-5" />,
      settings: [
        {
          label: 'Language',
          description: 'Choose your preferred language',
          control: (
            <select 
              className="px-3 py-1 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
              disabled
            >
              <option>English</option>
            </select>
          ),
          comingSoon: true
        }
      ]
    },
    {
      title: 'Privacy & Security',
      icon: <ShieldCheckIcon className="h-5 w-5" />,
      settings: [
        {
          label: 'Data Collection',
          description: 'Manage how your data is collected and used',
          control: (
            <button className="text-primary-600 hover:text-primary-700 text-sm font-medium" disabled>
              Manage
            </button>
          ),
          comingSoon: true
        },
        {
          label: 'Account Privacy',
          description: 'Control who can see your progress and achievements',
          control: (
            <select 
              className="px-3 py-1 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
              disabled
            >
              <option>Private</option>
            </select>
          ),
          comingSoon: true
        }
      ]
    }
  ]

  if (!user) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-6">
        <div className="text-center py-8">
          <UserCircleIcon className="h-12 w-12 text-neutral-400 mx-auto mb-3" />
          <h2 className="text-xl font-bold mb-2">Sign in to access settings</h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-4 text-sm">
            You need to be logged in to customize your experience
          </p>
          <button
            onClick={() => navigate('/login')}
            className="btn-primary"
          >
            Sign In
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      <div className="mb-4">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center text-neutral-600 dark:text-neutral-400 hover:text-neutral-800 dark:hover:text-neutral-200 mb-2"
        >
          <ArrowLeftIcon className="h-4 w-4 mr-2" />
          Back
        </button>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-neutral-600 dark:text-neutral-400 text-sm mt-1">
          Customize your SkillTree experience
        </p>
      </div>

      <div className="space-y-4">
        {settingsSections.map((section) => (
          <div key={section.title} className="card py-4">
            <div className="flex items-center gap-2 mb-3">
              <div className="text-primary-600 dark:text-primary-400">
                {section.icon}
              </div>
              <h2 className="text-lg font-semibold">{section.title}</h2>
            </div>
            
            <div className="space-y-3">
              {section.settings.map((setting) => (
                <div
                  key={setting.label}
                  className={`flex items-center justify-between py-2 ${
                    'comingSoon' in setting && setting.comingSoon ? 'opacity-60' : ''
                  }`}
                >
                  <div className="flex-1 pr-4">
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium text-sm">{setting.label}</h3>
                      {'comingSoon' in setting && setting.comingSoon && (
                        <span className="text-xs bg-neutral-200 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-400 px-1.5 py-0.5 rounded">
                          Coming Soon
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-neutral-600 dark:text-neutral-400 mt-0.5">
                      {setting.description}
                    </p>
                  </div>
                  <div className="flex-shrink-0">
                    {setting.control}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 card py-4 bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 border-primary-200 dark:border-primary-800">
        <h3 className="text-lg font-semibold mb-3">Account Information</h3>
        
        {/* Username Management */}
        <div className="mb-4">
          <span className="text-neutral-600 dark:text-neutral-400 text-xs">Username:</span>
          {!isEditingUsername ? (
            <div className="flex items-center gap-2 mt-1">
              <span className="font-medium text-sm">
                {currentUsername || 'Not set'}
              </span>
              <button
                onClick={startEditingUsername}
                className="text-primary-600 hover:text-primary-700 text-xs font-medium"
              >
                {currentUsername ? 'Change' : 'Set'}
              </button>
            </div>
          ) : (
            <div className="mt-1">
              <div className="flex items-center gap-2 mb-1">
                <input
                  type="text"
                  value={newUsername}
                  onChange={(e) => setNewUsername(e.target.value)}
                  placeholder="Enter username"
                  className="flex-1 px-2 py-1 text-xs border border-neutral-300 dark:border-neutral-600 rounded bg-white dark:bg-neutral-800 focus:outline-none focus:ring-1 focus:ring-primary-500 focus:border-transparent"
                  disabled={usernameLoading}
                />
                <button
                  onClick={handleUsernameUpdate}
                  disabled={usernameLoading || !newUsername.trim()}
                  className="px-2 py-1 bg-primary-600 hover:bg-primary-700 disabled:bg-neutral-400 text-white text-xs font-medium rounded transition-colors"
                >
                  {usernameLoading ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={cancelEditingUsername}
                  disabled={usernameLoading}
                  className="px-2 py-1 bg-neutral-200 hover:bg-neutral-300 dark:bg-neutral-700 dark:hover:bg-neutral-600 text-neutral-700 dark:text-neutral-300 text-xs font-medium rounded transition-colors"
                >
                  Cancel
                </button>
              </div>
              {usernameError && (
                <p className="text-red-600 dark:text-red-400 text-xs mb-1">{usernameError}</p>
              )}
              {usernameSuccess && (
                <p className="text-green-600 dark:text-green-400 text-xs mb-1">{usernameSuccess}</p>
              )}
              <p className="text-neutral-500 text-xs">
                3-30 characters, letters, numbers, underscores and hyphens only
              </p>
            </div>
          )}
        </div>

        {/* Other Account Info */}
        <div className="space-y-1 text-xs border-t border-neutral-200 dark:border-neutral-700 pt-3">
          <p>
            <span className="text-neutral-600 dark:text-neutral-400">Email:</span>{' '}
            <span className="font-medium">{user.email}</span>
          </p>
          <p>
            <span className="text-neutral-600 dark:text-neutral-400">Member Since:</span>{' '}
            <span className="font-medium">
              {new Date(user.created_at || '').toLocaleDateString()}
            </span>
          </p>
        </div>
      </div>

      <div className="mt-4 text-center text-xs text-neutral-500">
        <p>Version 1.0.0 • © 2024 SkillTree</p>
      </div>
    </div>
  )
}

export default SettingsPage