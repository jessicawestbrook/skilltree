import React, { useState, useRef, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import SearchBar from './SearchBar'
import { supabase } from '../services/supabase'
import { SkillTreeNode } from '../types/database.types'
import {
  ChevronDownIcon,
  ChevronLeftIcon,
  HomeIcon,
  AcademicCapIcon,
  ChatBubbleBottomCenterTextIcon,
  Cog6ToothIcon,
  UserCircleIcon,
  ArrowRightOnRectangleIcon,
  ArrowRightIcon,
  UserPlusIcon,
  ShieldCheckIcon,
  LanguageIcon,
  BookOpenIcon,
  SparklesIcon,
  DocumentTextIcon,
  QueueListIcon,
  ClipboardDocumentListIcon,
  PuzzlePieceIcon
} from '@heroicons/react/24/outline'

const UnifiedDropdownMenu: React.FC = () => {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [subjectCategories, setSubjectCategories] = useState<SkillTreeNode[]>([])
  const [subjectsHovered, setSubjectsHovered] = useState(false)
  const [flashcardsHovered, setFlashcardsHovered] = useState(false)
  const [testsHovered, setTestsHovered] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const subjectsRef = useRef<HTMLDivElement>(null)
  const flashcardsRef = useRef<HTMLDivElement>(null)
  const testsRef = useRef<HTMLDivElement>(null)

  // Fetch subject categories
  const fetchSubjectCategories = async () => {
    try {
      // Replicate the same logic as Layout to get the third-level categories
      const { data: rootNodes, error: rootError } = await supabase
        .from('skill_tree_nodes')
        .select('id, name')
        .is('parent_id', null)
        .eq('type', 'category')
        .limit(5)

      if (rootError) throw rootError
      if (!rootNodes || rootNodes.length === 0) return

      const { data: secondLevel, error: secondError } = await supabase
        .from('skill_tree_nodes')
        .select('id, name, parent_id')
        .in('parent_id', rootNodes.map(r => r.id))
        .eq('type', 'category')
        .order('name')

      if (secondError) throw secondError
      if (!secondLevel || secondLevel.length === 0) return

      const { data: thirdLevel, error: thirdError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .in('parent_id', secondLevel.map(s => s.id))
        .eq('type', 'category')
        .order('name')
        .limit(9)

      if (thirdError) throw thirdError
      setSubjectCategories(thirdLevel || [])
    } catch (error) {
      console.error('Error fetching subject categories:', error)
    }
  }

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

  // Fetch subject categories on component mount
  useEffect(() => {
    fetchSubjectCategories()
  }, [])

  const handleSignOut = async () => {
    await signOut()
    setDropdownOpen(false)
    navigate('/')
  }

  const navigationItems = [
    { to: '/', label: 'Home', icon: HomeIcon },
    { to: '/skill-tree', label: 'Skill Tree', icon: AcademicCapIcon },
    { to: '/text-tree', label: 'Text-Only View', icon: DocumentTextIcon },
    { to: '/learning-paths', label: 'Learning Paths', icon: BookOpenIcon },
    { to: '/intro-assessment', label: 'Skill Assessment', icon: SparklesIcon },
  ]

  const flashcardItems = [
    { to: '/spelling-bee', label: 'Spelling Bee', icon: LanguageIcon },
    { to: '/vocabulary-trainer', label: 'Vocabulary Trainer', icon: BookOpenIcon },
    { to: '/language-trainer', label: 'Language Trainer', icon: LanguageIcon },
    { to: '/study-lists', label: 'Study Lists', icon: QueueListIcon },
  ]

  const testItems = [
    { to: '/standardized-tests', label: 'All Tests', icon: ClipboardDocumentListIcon },
    { to: '/test/sat', label: 'SAT', icon: PuzzlePieceIcon },
    { to: '/test/act', label: 'ACT', icon: PuzzlePieceIcon },
    { to: '/test/lsat', label: 'LSAT', icon: PuzzlePieceIcon },
    { to: '/iq-test', label: 'IQ Tests', icon: PuzzlePieceIcon },
  ]

  const otherItems = [
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
        <div className="absolute right-0 z-50 mt-2 w-56 rounded-lg shadow-xl bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 divide-y divide-neutral-200 dark:divide-neutral-700">
          {/* User Info Section (if logged in) */}
          {user && (
            <div className="px-3 py-2">
              <p className="text-xs font-medium text-neutral-900 dark:text-white truncate">
                {user.email}
              </p>
              <p className="text-xs text-neutral-500 dark:text-neutral-400">
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
                className="flex items-center justify-between w-full px-2 py-1.5 text-xs font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-md transition-colors"
              >
                <span className="flex items-center">
                  <ArrowRightIcon className="h-3 w-3 mr-1.5" />
                  Sign In
                </span>
              </Link>
              <Link
                to="/signup"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center justify-between w-full px-2 py-1.5 mt-1.5 text-xs font-medium text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20 hover:bg-primary-100 dark:hover:bg-primary-900/30 rounded-md transition-colors"
              >
                <span className="flex items-center">
                  <UserPlusIcon className="h-3 w-3 mr-1.5" />
                  Sign Up
                </span>
              </Link>
            </div>
          )}

          {/* Search Section - Only visible on small screens */}
          <div className="sm:hidden p-2 border-b border-neutral-200 dark:border-neutral-700">
            <SearchBar placeholder="Search..." className="w-full" />
          </div>

          {/* Navigation Section */}
          <div className="py-1">
            {/* Main Navigation */}
            {navigationItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setDropdownOpen(false)}
                className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <item.icon className="h-3 w-3 mr-2 text-neutral-500" />
                {item.label}
              </Link>
            ))}

            {/* Subjects Section with Submenu */}
            <div className="border-t border-neutral-200 dark:border-neutral-700 mt-1 pt-1 relative" ref={subjectsRef}>
              <div
                className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors cursor-pointer"
                onMouseEnter={() => setSubjectsHovered(true)}
                onMouseLeave={() => setSubjectsHovered(false)}
              >
                <ChevronLeftIcon className="h-3 w-3 mr-2 text-neutral-400" />
                <AcademicCapIcon className="h-3 w-3 mr-2 text-neutral-500" />
                Subjects
              </div>

              {/* Submenu */}
              {subjectsHovered && (
                <div
                  className="absolute right-full top-0 mr-1 w-48 bg-white dark:bg-neutral-800 rounded-lg shadow-xl border border-neutral-200 dark:border-neutral-700 py-1 z-50"
                  onMouseEnter={() => setSubjectsHovered(true)}
                  onMouseLeave={() => setSubjectsHovered(false)}
                >
                  {subjectCategories.length > 0 ? (
                    subjectCategories.map((category) => (
                      <Link
                        key={category.id}
                        to={`/category/${category.id}`}
                        onClick={() => {
                          setDropdownOpen(false)
                          setSubjectsHovered(false)
                        }}
                        className="block px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        {category.name}
                      </Link>
                    ))
                  ) : (
                    <div className="px-3 py-1.5 text-xs text-neutral-500 dark:text-neutral-400">
                      Loading subjects...
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Flashcards Section with Submenu */}
            <div className="border-t border-neutral-200 dark:border-neutral-700 mt-1 pt-1 relative" ref={flashcardsRef}>
              <div
                className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors cursor-pointer"
                onMouseEnter={() => setFlashcardsHovered(true)}
                onMouseLeave={() => setFlashcardsHovered(false)}
              >
                <ChevronLeftIcon className="h-3 w-3 mr-2 text-neutral-400" />
                <LanguageIcon className="h-3 w-3 mr-2 text-neutral-500" />
                Flashcards
              </div>

              {/* Submenu */}
              {flashcardsHovered && (
                <div
                  className="absolute right-full top-0 mr-1 w-48 bg-white dark:bg-neutral-800 rounded-lg shadow-xl border border-neutral-200 dark:border-neutral-700 py-1 z-50"
                  onMouseEnter={() => setFlashcardsHovered(true)}
                  onMouseLeave={() => setFlashcardsHovered(false)}
                >
                  {flashcardItems.map((item) => (
                    <Link
                      key={item.to}
                      to={item.to}
                      onClick={() => {
                        setDropdownOpen(false)
                        setFlashcardsHovered(false)
                      }}
                      className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                    >
                      <item.icon className="h-3 w-3 mr-2 text-neutral-500" />
                      {item.label}
                    </Link>
                  ))}
                </div>
              )}
            </div>

            {/* Tests Section with Submenu */}
            <div className="border-t border-neutral-200 dark:border-neutral-700 mt-1 pt-1 relative" ref={testsRef}>
              <div
                className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors cursor-pointer"
                onMouseEnter={() => setTestsHovered(true)}
                onMouseLeave={() => setTestsHovered(false)}
              >
                <ChevronLeftIcon className="h-3 w-3 mr-2 text-neutral-400" />
                <ClipboardDocumentListIcon className="h-3 w-3 mr-2 text-neutral-500" />
                Tests
              </div>

              {/* Submenu */}
              {testsHovered && (
                <div
                  className="absolute right-full top-0 mr-1 w-48 bg-white dark:bg-neutral-800 rounded-lg shadow-xl border border-neutral-200 dark:border-neutral-700 py-1 z-50"
                  onMouseEnter={() => setTestsHovered(true)}
                  onMouseLeave={() => setTestsHovered(false)}
                >
                  {testItems.map((item) => (
                    <Link
                      key={item.to}
                      to={item.to}
                      onClick={() => {
                        setDropdownOpen(false)
                        setTestsHovered(false)
                      }}
                      className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                    >
                      <item.icon className="h-3 w-3 mr-2 text-neutral-500" />
                      {item.label}
                    </Link>
                  ))}
                </div>
              )}
            </div>

            {/* Other Items */}
            <div className="border-t border-neutral-200 dark:border-neutral-700 mt-1 pt-1">
              {otherItems.map((item) => (
                <Link
                  key={item.to}
                  to={item.to}
                  onClick={() => setDropdownOpen(false)}
                  className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                >
                  <item.icon className="h-3 w-3 mr-2 text-neutral-500" />
                  {item.label}
                </Link>
              ))}
            </div>
            
          </div>

          {/* User-specific items and Settings */}
          {user && (
            <div className="py-1">
              <Link
                to="/profile"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <UserCircleIcon className="h-3 w-3 mr-2 text-neutral-500" />
                Profile
              </Link>
              {userItems.map((item) => (
                <Link
                  key={item.to}
                  to={item.to}
                  onClick={() => setDropdownOpen(false)}
                  className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                >
                  <item.icon className="h-3 w-3 mr-2 text-neutral-500" />
                  {item.label}
                </Link>
              ))}
              
              {/* Admin link */}
              {isAdmin && (
                <Link
                  to="/admin"
                  onClick={() => setDropdownOpen(false)}
                  className="flex items-center px-3 py-1.5 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                >
                  <ShieldCheckIcon className="h-3 w-3 mr-2 text-neutral-500" />
                  Admin Panel
                </Link>
              )}
            </div>
          )}

          {/* Sign Out Section */}
          {user && (
            <div className="p-1.5">
              <button
                onClick={handleSignOut}
                className="flex items-center justify-center w-full px-2 py-1.5 text-xs font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors"
              >
                <ArrowRightOnRectangleIcon className="h-3 w-3 mr-1.5" />
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