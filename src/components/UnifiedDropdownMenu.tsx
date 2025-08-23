import React, { useState, useRef, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import SearchBar from './SearchBar'
import CategoryLink from './CategoryLink'
import { supabase } from '../services/supabase'
import { SkillTreeNode } from '../types/database.types'
import {
  ChevronDownIcon,
  ChevronLeftIcon,
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
      // Get top-level categories (root nodes) - same as Layout component
      const { data: rootNodes, error: rootError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .is('parent_id', null)
        .or('learning_content_ids.is.null,learning_content_ids.eq.{}')
        .order('display_order', { nullsFirst: false })
        .order('name')

      if (rootError) throw rootError
      setSubjectCategories(rootNodes || [])
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
        // Logged in: Show "My Learning" link + dropdown button
        <div className="flex items-center rounded-lg overflow-hidden bg-primary-100 dark:bg-primary-900/30">
          <Link
            to="/profile"
            className="flex items-center gap-2 px-4 py-2 font-medium text-primary-700 dark:text-primary-400 hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-all"
          >
            <UserCircleIcon className="h-5 w-5" />
            <span>My Learning</span>
          </Link>
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="px-2 py-2 text-primary-700 dark:text-primary-400 hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-all border-l border-primary-200 dark:border-primary-800"
          >
            <ChevronDownIcon className={`h-4 w-4 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
          </button>
        </div>
      ) : (
        // Not logged in: Show Sign Up/Login button
        <button
          onClick={() => setDropdownOpen(!dropdownOpen)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg font-medium bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-all"
        >
          <span>Sign Up / Login</span>
          <ChevronDownIcon className={`h-4 w-4 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
        </button>
      )}

      {dropdownOpen && (
        <div className="absolute right-0 z-50 mt-2 w-56 rounded-lg shadow-xl bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5">
          {/* Sign Out Section (if logged in) */}
          {user && (
            <button
              onClick={handleSignOut}
              className="flex items-center justify-between w-full px-3 py-1.5 text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
            >
              <span className="flex items-center">
                <ArrowRightOnRectangleIcon className="h-3 w-3 mr-1.5" />
                Sign Out
              </span>
            </button>
          )}

          {/* Auth Section (if not logged in) */}
          {!user && (
            <div className="py-1">
              <Link
                to="/login"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <ArrowRightIcon className="h-3 w-3 mr-2 text-neutral-500" />
                Sign In
              </Link>
              <Link
                to="/signup"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center px-3 py-1.5 text-sm text-primary-600 dark:text-primary-400 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <UserPlusIcon className="h-3 w-3 mr-2 text-primary-500" />
                Sign Up
              </Link>
            </div>
          )}

          {/* Search Section - Only visible on small screens */}
          <div className="sm:hidden p-2">
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
                className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <item.icon className="h-3 w-3 mr-2 text-neutral-500" />
                {item.label}
              </Link>
            ))}

            {/* Subjects Section with Submenu */}
            <div className="relative" ref={subjectsRef}>
              <div
                className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors cursor-pointer"
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
                      <CategoryLink
                        key={category.id}
                        categoryId={category.id}
                        onClick={() => {
                          setDropdownOpen(false)
                          setSubjectsHovered(false)
                        }}
                        className="block px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        {category.name}
                      </CategoryLink>
                    ))
                  ) : (
                    <div className="px-3 py-1.5 text-sm text-neutral-500 dark:text-neutral-400">
                      Loading subjects...
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Flashcards Section with Submenu */}
            <div className="relative" ref={flashcardsRef}>
              <div
                className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors cursor-pointer"
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
                      className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                    >
                      <item.icon className="h-3 w-3 mr-2 text-neutral-500" />
                      {item.label}
                    </Link>
                  ))}
                </div>
              )}
            </div>

            {/* Tests Section with Submenu */}
            <div className="relative" ref={testsRef}>
              <div
                className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors cursor-pointer"
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
                      className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                    >
                      <item.icon className="h-3 w-3 mr-2 text-neutral-500" />
                      {item.label}
                    </Link>
                  ))}
                </div>
              )}
            </div>

            {/* Learning Paths */}
            <Link
              to="/learning-paths"
              onClick={() => setDropdownOpen(false)}
              className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
            >
              <BookOpenIcon className="h-3 w-3 mr-2 text-neutral-500" />
              Learning Paths
            </Link>

            {/* Other Items */}
            {otherItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setDropdownOpen(false)}
                className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              >
                <item.icon className="h-3 w-3 mr-2 text-neutral-500" />
                {item.label}
              </Link>
            ))}

            {/* User-specific items and Settings */}
            {user && (
              <>
                {userItems.map((item) => (
                  <Link
                    key={item.to}
                    to={item.to}
                    onClick={() => setDropdownOpen(false)}
                    className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
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
                    className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                  >
                    <ShieldCheckIcon className="h-3 w-3 mr-2 text-neutral-500" />
                    Admin Panel
                  </Link>
                )}
              </>
            )}
            
          </div>

        </div>
      )}
    </div>
  )
}

export default UnifiedDropdownMenu