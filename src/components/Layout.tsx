import React, { useState, useEffect, useRef } from 'react'
import { Outlet, Link } from 'react-router-dom'
import { AcademicCapIcon, Bars3Icon, XMarkIcon, ChevronDownIcon } from '@heroicons/react/24/outline'
import { useTheme } from '../contexts/ThemeContext'
import UnifiedDropdownMenu from './UnifiedDropdownMenu'
import SearchBar from './SearchBar'
import NotificationBell from './NotificationBell'
import { supabase } from '../services/supabase'
import { SkillTreeNode } from '../types/database.types'

const Layout: React.FC = () => {
  const { menuPinned, toggleMenuPinned } = useTheme()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false) // Closed by default
  const [standardizedTestsOpen, setStandardizedTestsOpen] = useState(false)
  const [flashcardsOpen, setFlashcardsOpen] = useState(false)
  const [subjectsOpen, setSubjectsOpen] = useState(false)
  const [subjectCategories, setSubjectCategories] = useState<SkillTreeNode[]>([])
  const standardizedTestsRef = useRef<HTMLDivElement>(null)
  const flashcardsRef = useRef<HTMLDivElement>(null)
  const subjectsRef = useRef<HTMLDivElement>(null)

  const fetchSubjectCategories = async () => {
    try {
      // Get top-level categories (root nodes)
      const { data: rootNodes, error: rootError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .is('parent_id', null)
        .eq('type', 'category')
        .order('name')

      if (rootError) throw rootError
      setSubjectCategories(rootNodes || [])
    } catch (error) {
      console.error('Error fetching subject categories:', error)
    }
  }

  // Fetch subject categories on component mount
  useEffect(() => {
    fetchSubjectCategories()
  }, [])

  // Close mobile menu when switching to pinned
  useEffect(() => {
    if (menuPinned) {
      setMobileMenuOpen(false) // Close mobile menu when pinned
    }
  }, [menuPinned])

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (standardizedTestsRef.current && !standardizedTestsRef.current.contains(event.target as Node)) {
        setStandardizedTestsOpen(false)
      }
      if (flashcardsRef.current && !flashcardsRef.current.contains(event.target as Node)) {
        setFlashcardsOpen(false)
      }
      if (subjectsRef.current && !subjectsRef.current.contains(event.target as Node)) {
        setSubjectsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

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
                  <span className="font-game text-2xl text-primary-600 dark:text-primary-400">
                    SkillTree
                  </span>
                </Link>
              </div>

              {/* Main Navigation - Hidden on mobile (sm and below) */}
              <div className="hidden md:flex items-center space-x-1 ml-8">
                {/* Subjects Dropdown */}
                <div className="relative" ref={subjectsRef}>
                  <button
                    onClick={() => setSubjectsOpen(!subjectsOpen)}
                    className="flex items-center px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                  >
                    Subjects
                    <ChevronDownIcon className={`ml-1 h-4 w-4 transition-transform ${subjectsOpen ? 'rotate-180' : ''}`} />
                  </button>
                  
                  {subjectsOpen && (
                    <div className="absolute top-full left-0 mt-2 w-56 rounded-lg shadow-xl bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 py-1 z-50">
                      {subjectCategories.map(category => (
                        <Link
                          key={category.id}
                          to={`/category/${category.id}`}
                          onClick={() => setSubjectsOpen(false)}
                          className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                        >
                          {category.name}
                        </Link>
                      ))}
                      {subjectCategories.length === 0 && (
                        <div className="px-3 py-1.5 text-xs text-neutral-500 dark:text-neutral-400">
                          Loading subjects...
                        </div>
                      )}
                    </div>
                  )}
                </div>
                {/* Flashcards Dropdown */}
                <div className="relative" ref={flashcardsRef}>
                  <button
                    onClick={() => setFlashcardsOpen(!flashcardsOpen)}
                    className="flex items-center px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                  >
                    Flashcards
                    <ChevronDownIcon className={`ml-1 h-4 w-4 transition-transform ${flashcardsOpen ? 'rotate-180' : ''}`} />
                  </button>
                  
                  {flashcardsOpen && (
                    <div className="absolute top-full left-0 mt-2 w-52 rounded-lg shadow-xl bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 py-1 z-50">
                      <Link
                        to="/spelling-bee"
                        onClick={() => setFlashcardsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        Spelling Bee
                      </Link>
                      <Link
                        to="/vocabulary-trainer"
                        onClick={() => setFlashcardsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        Vocabulary Trainer
                      </Link>
                      <Link
                        to="/language-trainer"
                        onClick={() => setFlashcardsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        Language Trainer
                      </Link>
                      <div className="border-t border-neutral-200 dark:border-neutral-700 my-1"></div>
                      <Link
                        to="/study-lists"
                        onClick={() => setFlashcardsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        Study Lists
                      </Link>
                    </div>
                  )}
                </div>
                {/* Standardized Tests Dropdown */}
                <div className="relative" ref={standardizedTestsRef}>
                  <button
                    onClick={() => setStandardizedTestsOpen(!standardizedTestsOpen)}
                    className="flex items-center px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                  >
                    Tests
                    <ChevronDownIcon className={`ml-1 h-4 w-4 transition-transform ${standardizedTestsOpen ? 'rotate-180' : ''}`} />
                  </button>
                  
                  {standardizedTestsOpen && (
                    <div className="absolute top-full left-0 mt-2 w-52 rounded-lg shadow-xl bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 py-1 z-50">
                      <Link
                        to="/standardized-tests"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        All Tests Overview
                      </Link>
                      <div className="border-t border-neutral-200 dark:border-neutral-600 my-1"></div>
                      <Link
                        to="/test/sat"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        SAT
                      </Link>
                      <Link
                        to="/test/act"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        ACT
                      </Link>
                      <Link
                        to="/test/lsat"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        LSAT
                      </Link>
                      <Link
                        to="/test/gre"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        GRE
                      </Link>
                      <Link
                        to="/test/gmat"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        GMAT
                      </Link>
                      <Link
                        to="/test/mcat"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        MCAT
                      </Link>
                      <div className="border-t border-neutral-200 dark:border-neutral-600 my-1"></div>
                      <Link
                        to="/iq-test"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        IQ Tests
                      </Link>
                    </div>
                  )}
                </div>
                <Link 
                  to="/learning-paths" 
                  className="px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                >
                  Paths
                </Link>
              </div>

              {/* Spacer to push search bar to the right */}
              <div className="flex-1"></div>

              {/* Search Bar - Hidden on small screens */}
              <div className="hidden sm:flex items-center mx-2 lg:mx-4">
                <SearchBar placeholder="Search..." className="w-full max-w-48 lg:max-w-64" />
              </div>

              {/* Notifications and Login */}
              <div className="flex items-center space-x-2 mr-2">
                <NotificationBell />
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