import React, { useState } from 'react'
import { Outlet, Link } from 'react-router-dom'
import { AcademicCapIcon } from '@heroicons/react/24/outline'
import RandomQuestionBox from './RandomQuestionBox'
import RecommendedContent from './RecommendedContent'
import UnifiedDropdownMenu from './UnifiedDropdownMenu'
import { useAuth } from '../contexts/AuthContext'

const Layout: React.FC = () => {
  const { user } = useAuth()
  const [showRandomQuestion, setShowRandomQuestion] = useState(true)
  const showRecommended = true

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white dark:bg-neutral-800 shadow-md">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
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
            <div className="hidden md:flex items-center space-x-1">
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

            {/* Unified Dropdown Menu */}
            <div className="flex items-center">
              <UnifiedDropdownMenu />
            </div>
          </div>
        </nav>
      </header>

      <div className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col lg:flex-row gap-6">
            {/* Recommended Content - Upper Left */}
            {user && showRecommended && (
              <aside className="lg:w-96 order-first">
                <div className="sticky top-4 space-y-4">
                  <RecommendedContent />
                  {showRandomQuestion && (
                    <div className="hidden lg:block">
                      <RandomQuestionBox onClose={() => setShowRandomQuestion(false)} />
                    </div>
                  )}
                </div>
              </aside>
            )}
            
            {/* Random Question Box for non-logged-in users - Hidden on mobile */}
            {!user && showRandomQuestion && (
              <aside className="hidden lg:block lg:w-80 order-first">
                <div className="sticky top-4">
                  <RandomQuestionBox onClose={() => setShowRandomQuestion(false)} />
                </div>
              </aside>
            )}
            
            {/* Main Content */}
            <main className="flex-1">
              <Outlet />
            </main>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Layout