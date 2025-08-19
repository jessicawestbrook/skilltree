import React, { useState, useEffect } from 'react'
import { Outlet, Link } from 'react-router-dom'
import { AcademicCapIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { useTheme } from '../contexts/ThemeContext'
import UnifiedDropdownMenu from './UnifiedDropdownMenu'

const Layout: React.FC = () => {
  const { menuPinned, toggleMenuPinned } = useTheme()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false) // Closed by default

  // Close mobile menu when switching to pinned
  useEffect(() => {
    if (menuPinned) {
      setMobileMenuOpen(false) // Close mobile menu when pinned
    }
  }, [menuPinned])

  const handleToggleMenuPinned = () => {
    toggleMenuPinned()
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Floating Controls - Only hamburger button when menu is hidden */}
      {!menuPinned && !mobileMenuOpen && (
        <div className="fixed top-4 right-4 z-[9999]">
          <button
            onClick={() => setMobileMenuOpen(true)}
            className="p-3 bg-white dark:bg-neutral-800 rounded-lg shadow-xl border-2 border-neutral-300 dark:border-neutral-600 hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
          >
            <Bars3Icon className="h-6 w-6 text-neutral-700 dark:text-neutral-300" />
          </button>
        </div>
      )}

      {/* Header - Conditional display based on menuPinned */}
      {(menuPinned || mobileMenuOpen) && (
        <header className={`bg-white dark:bg-neutral-800 shadow-md ${!menuPinned && mobileMenuOpen ? 'fixed top-0 left-0 right-0 z-40' : ''}`}>
          <nav className="w-full pl-4 sm:pl-6 lg:pl-8 pr-0">
            <div className="flex items-center h-16">
              {/* Logo/Brand */}
              <div className="flex items-center">
                <Link to="/" className="flex items-center space-x-2">
                  <AcademicCapIcon className="h-8 w-8 text-primary-600" />
                  <span className="font-game text-2xl bg-gradient-to-r from-primary-600 to-gold-500 bg-clip-text text-transparent">
                    SkillTree
                  </span>
                </Link>
              </div>

              {/* Main Navigation - Hidden on mobile */}
              <div className="hidden md:flex items-center space-x-1 ml-8">
                <Link 
                  to="/skill-tree" 
                  className="px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                >
                  Skill Tree
                </Link>
                <Link 
                  to="/spelling-bee" 
                  className="px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                >
                  Spelling Bee
                </Link>
                <Link 
                  to="/iq-test" 
                  className="px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                >
                  IQ Tests
                </Link>
                <Link 
                  to="/standardized-tests" 
                  className="px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                >
                  Standardized Tests
                </Link>
                <Link 
                  to="/reading-comprehension" 
                  className="px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                >
                  Reading
                </Link>
                <Link 
                  to="/career-advancement" 
                  className="px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                >
                  Career
                </Link>
                <Link 
                  to="/learning-paths" 
                  className="px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                >
                  Paths
                </Link>
              </div>

              {/* Spacer to push everything to the right */}
              <div className="flex-1"></div>

              {/* Login */}
              <div className="flex items-center mr-2">
                <UnifiedDropdownMenu />
              </div>

              {/* Far right: Close button - No margin */}
              <div className="flex items-center">
                {/* Close mobile menu button - Only when unpinned and mobile menu open */}
                {!menuPinned && mobileMenuOpen && (
                  <button
                    onClick={() => setMobileMenuOpen(false)}
                    className="p-2 text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                    title="Close menu"
                  >
                    <XMarkIcon className="h-5 w-5" />
                  </button>
                )}

                {/* Unpin menu button - Always show X to allow switching to hamburger mode */}
                {menuPinned && (
                  <button
                    onClick={handleToggleMenuPinned}
                    className="p-2 text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                    title="Switch to hamburger menu"
                  >
                    <XMarkIcon className="h-5 w-5" />
                  </button>
                )}
              </div>
            </div>
          </nav>
        </header>
      )}

      {/* Main Content */}
      <div className={`flex-1 ${menuPinned ? 'pt-0' : (!menuPinned && mobileMenuOpen) ? 'pt-16' : 'pt-0'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <main>
            <Outlet />
          </main>
        </div>
      </div>

    </div>
  )
}

export default Layout