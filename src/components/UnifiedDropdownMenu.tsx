import React, { useState, useRef, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { useTheme } from '../contexts/ThemeContext'
import {
  ChevronDownIcon,
  HomeIcon,
  AcademicCapIcon,
  ChatBubbleBottomCenterTextIcon,
  Cog6ToothIcon,
  UserCircleIcon,
  ArrowRightOnRectangleIcon,
  ArrowRightIcon,
  UserPlusIcon,
  MoonIcon,
  SunIcon,
  ShieldCheckIcon,
  LanguageIcon,
  BookOpenIcon,
  SparklesIcon,
  Bars3Icon
} from '@heroicons/react/24/outline'

const UnifiedDropdownMenu: React.FC = () => {
  const { user, signOut } = useAuth()
  const { darkMode, toggleDarkMode, menuPinned, toggleMenuPinned } = useTheme()
  const navigate = useNavigate()
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSignOut = async () => {
    await signOut()
    setDropdownOpen(false)
    navigate('/')
  }

  const navigationItems = [
    { to: '/', label: 'Home', icon: HomeIcon },
    { to: '/skill-tree', label: 'Skill Tree', icon: AcademicCapIcon },
    { to: '/text-tree', label: 'Text-Only View', icon: AcademicCapIcon },
    { to: '/learning-paths', label: 'Learning Paths', icon: BookOpenIcon },
    { to: '/intro-assessment', label: 'Skill Assessment', icon: SparklesIcon },
    { to: '/spelling-bee', label: 'Spelling Bee', icon: LanguageIcon },
    { to: '/feedback', label: 'Feedback', icon: ChatBubbleBottomCenterTextIcon },
  ]

  const userItems = [
    { to: '/settings', label: 'Settings', icon: Cog6ToothIcon },
  ]

  // Check if user is admin (you may want to add proper admin check)
  const isAdmin = user?.email === 'admin@skilltree.com' // Replace with actual admin check

  return (
    <div className="relative" ref={dropdownRef}>
      {user ? (
        // Logged in: Show username button with dropdown
        <button
          onClick={() => setDropdownOpen(!dropdownOpen)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg font-medium bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-all"
        >
          <UserCircleIcon className="h-5 w-5" />
          <span className="hidden sm:inline">{user.email?.split('@')[0]}</span>
          <ChevronDownIcon className={`h-4 w-4 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
        </button>
      ) : (
        // Not logged in: Show Sign Up/Login button
        <button
          onClick={() => setDropdownOpen(!dropdownOpen)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg font-medium bg-primary-600 text-white hover:bg-primary-700 transition-all"
        >
          <span>Sign Up / Login</span>
          <ChevronDownIcon className={`h-4 w-4 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
        </button>
      )}

      {dropdownOpen && (
        <div className="absolute right-0 z-50 mt-2 w-64 rounded-lg shadow-xl bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 divide-y divide-neutral-200 dark:divide-neutral-700">
          {/* User Info Section (if logged in) */}
          {user && (
            <div className="px-4 py-3">
              <p className="text-sm font-medium text-neutral-900 dark:text-white truncate">
                {user.email}
              </p>
              <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">
                Signed in
              </p>
            </div>
          )}

          {/* Auth Section (if not logged in) */}
          {!user && (
            <div className="p-2">
              <Link
                to="/login"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center justify-between w-full px-3 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-md transition-colors"
              >
                <span className="flex items-center">
                  <ArrowRightIcon className="h-4 w-4 mr-2" />
                  Sign In
                </span>
              </Link>
              <Link
                to="/signup"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center justify-between w-full px-3 py-2 mt-2 text-sm font-medium text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20 hover:bg-primary-100 dark:hover:bg-primary-900/30 rounded-md transition-colors"
              >
                <span className="flex items-center">
                  <UserPlusIcon className="h-4 w-4 mr-2" />
                  Sign Up
                </span>
              </Link>
            </div>
          )}

          {/* Navigation Section */}
          <div className="py-2">
            {navigationItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setDropdownOpen(false)}
                className="flex items-center px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <item.icon className="h-4 w-4 mr-3 text-neutral-500" />
                {item.label}
              </Link>
            ))}
            
            {/* Settings for non-logged in users */}
            {!user && (
              <>
                {/* Menu Pin Toggle */}
                <button
                  onClick={() => {
                    toggleMenuPinned()
                  }}
                  className="flex items-center justify-between w-full px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                >
                  <span className="flex items-center">
                    <Bars3Icon className="h-4 w-4 mr-3 text-neutral-500" />
                    Pin Menu
                  </span>
                  <span className="text-xs text-neutral-400">
                    {menuPinned ? 'On' : 'Off'}
                  </span>
                </button>

                {/* Dark Mode Toggle */}
                <button
                  onClick={() => {
                    toggleDarkMode()
                  }}
                  className="flex items-center justify-between w-full px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                >
                  <span className="flex items-center">
                    {darkMode ? (
                      <SunIcon className="h-4 w-4 mr-3 text-neutral-500" />
                    ) : (
                      <MoonIcon className="h-4 w-4 mr-3 text-neutral-500" />
                    )}
                    {darkMode ? 'Light Mode' : 'Dark Mode'}
                  </span>
                  <span className="text-xs text-neutral-400">
                    {darkMode ? 'On' : 'Off'}
                  </span>
                </button>
              </>
            )}
          </div>

          {/* User-specific items and Settings */}
          {user && (
            <div className="py-2">
              <Link
                to="/profile"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <UserCircleIcon className="h-4 w-4 mr-3 text-neutral-500" />
                Profile
              </Link>
              {userItems.map((item) => (
                <Link
                  key={item.to}
                  to={item.to}
                  onClick={() => setDropdownOpen(false)}
                  className="flex items-center px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                >
                  <item.icon className="h-4 w-4 mr-3 text-neutral-500" />
                  {item.label}
                </Link>
              ))}
              
              {/* Admin link */}
              {isAdmin && (
                <Link
                  to="/admin"
                  onClick={() => setDropdownOpen(false)}
                  className="flex items-center px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                >
                  <ShieldCheckIcon className="h-4 w-4 mr-3 text-neutral-500" />
                  Admin Panel
                </Link>
              )}
              
              {/* Menu Pin Toggle */}
              <button
                onClick={() => {
                  toggleMenuPinned()
                }}
                className="flex items-center justify-between w-full px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <span className="flex items-center">
                  <Bars3Icon className="h-4 w-4 mr-3 text-neutral-500" />
                  Pin Menu
                </span>
                <span className="text-xs text-neutral-400">
                  {menuPinned ? 'On' : 'Off'}
                </span>
              </button>

              {/* Dark Mode Toggle */}
              <button
                onClick={() => {
                  toggleDarkMode()
                }}
                className="flex items-center justify-between w-full px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <span className="flex items-center">
                  {darkMode ? (
                    <SunIcon className="h-4 w-4 mr-3 text-neutral-500" />
                  ) : (
                    <MoonIcon className="h-4 w-4 mr-3 text-neutral-500" />
                  )}
                  {darkMode ? 'Light Mode' : 'Dark Mode'}
                </span>
                <span className="text-xs text-neutral-400">
                  {darkMode ? 'On' : 'Off'}
                </span>
              </button>
            </div>
          )}

          {/* Sign Out Section */}
          {user && (
            <div className="p-2">
              <button
                onClick={handleSignOut}
                className="flex items-center justify-center w-full px-3 py-2 text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors"
              >
                <ArrowRightOnRectangleIcon className="h-4 w-4 mr-2" />
                Sign Out
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default UnifiedDropdownMenu