import React from 'react'
import { useTheme } from '../contexts/ThemeContext'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
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
  const navigate = useNavigate()

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
          label: 'Email Notifications',
          description: 'Receive updates about new content and achievements',
          control: (
            <button
              className="relative inline-flex h-6 w-11 items-center rounded-full bg-neutral-300"
              disabled
            >
              <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-1" />
            </button>
          ),
          comingSoon: true
        },
        {
          label: 'Learning Reminders',
          description: 'Get reminded to continue your learning journey',
          control: (
            <button
              className="relative inline-flex h-6 w-11 items-center rounded-full bg-neutral-300"
              disabled
            >
              <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-1" />
            </button>
          ),
          comingSoon: true
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
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center py-12">
          <UserCircleIcon className="h-16 w-16 text-neutral-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-2">Sign in to access settings</h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
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
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-6">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center text-neutral-600 dark:text-neutral-400 hover:text-neutral-800 dark:hover:text-neutral-200 mb-4"
        >
          <ArrowLeftIcon className="h-4 w-4 mr-2" />
          Back
        </button>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-neutral-600 dark:text-neutral-400 mt-2">
          Customize your SkillTree experience
        </p>
      </div>

      <div className="space-y-8">
        {settingsSections.map((section) => (
          <div key={section.title} className="card">
            <div className="flex items-center gap-3 mb-4">
              <div className="text-primary-600 dark:text-primary-400">
                {section.icon}
              </div>
              <h2 className="text-xl font-semibold">{section.title}</h2>
            </div>
            
            <div className="space-y-4">
              {section.settings.map((setting) => (
                <div
                  key={setting.label}
                  className={`flex items-center justify-between py-3 ${
                    'comingSoon' in setting && setting.comingSoon ? 'opacity-60' : ''
                  }`}
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium">{setting.label}</h3>
                      {'comingSoon' in setting && setting.comingSoon && (
                        <span className="text-xs bg-neutral-200 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-400 px-2 py-0.5 rounded">
                          Coming Soon
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-neutral-600 dark:text-neutral-400">
                      {setting.description}
                    </p>
                  </div>
                  <div className="ml-4">
                    {setting.control}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-12 card bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 border-primary-200 dark:border-primary-800">
        <h3 className="text-lg font-semibold mb-2">Account Information</h3>
        <div className="space-y-2 text-sm">
          <p>
            <span className="text-neutral-600 dark:text-neutral-400">Email:</span>{' '}
            <span className="font-medium">{user.email}</span>
          </p>
          <p>
            <span className="text-neutral-600 dark:text-neutral-400">User ID:</span>{' '}
            <span className="font-mono text-xs">{user.id}</span>
          </p>
          <p>
            <span className="text-neutral-600 dark:text-neutral-400">Member Since:</span>{' '}
            <span className="font-medium">
              {new Date(user.created_at || '').toLocaleDateString()}
            </span>
          </p>
        </div>
      </div>

      <div className="mt-8 text-center text-sm text-neutral-500">
        <p>Version 1.0.0 • © 2024 SkillTree</p>
      </div>
    </div>
  )
}

export default SettingsPage