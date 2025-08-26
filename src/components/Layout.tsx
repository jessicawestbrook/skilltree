import React, { useState, useEffect, useRef } from 'react'
import { Outlet, Link } from 'react-router-dom'
import { Bars3Icon, XMarkIcon, ChevronDownIcon } from '@heroicons/react/24/outline'
import { useTheme } from '../contexts/ThemeContext'
import UnifiedDropdownMenu from './UnifiedDropdownMenu'
import SearchBar from './SearchBar'
import NotificationBell from './NotificationBell'
import TreeLogo from './TreeLogo'
import CategoryLink from './CategoryLink'
import { supabase } from '../services/supabase'
import { SkillTreeNode } from '../types/database.types'
import { hiddenSkillsService } from '../services/hiddenNodesService'

const Layout: React.FC = () => {
  const { menuPinned, toggleMenuPinned } = useTheme()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false) // Closed by default
  const [standardizedTestsOpen, setStandardizedTestsOpen] = useState(false)
  const [flashcardsOpen, setFlashcardsOpen] = useState(false)
  const [subjectsOpen, setSubjectsOpen] = useState(false)
  const [subjectCategories, setSubjectCategories] = useState<SkillTreeNode[]>([])
  const [hoveredCategoryId, setHoveredCategoryId] = useState<string | null>(null)
  const [hoveredSubcategoryId, setHoveredSubcategoryId] = useState<string | null>(null)
  const [subcategories, setSubcategories] = useState<Record<string, SkillTreeNode[]>>({})
  const [subSubcategories, setSubSubcategories] = useState<Record<string, SkillTreeNode[]>>({})
  const standardizedTestsRef = useRef<HTMLDivElement>(null)
  const flashcardsRef = useRef<HTMLDivElement>(null)
  const subjectsRef = useRef<HTMLDivElement>(null)
  const hoverTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  const fetchSubjectCategories = async () => {
    try {
      // Get top-level categories (root nodes)
      const { data: rootNodes, error: rootError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .is('parent_id', null)
        .or('learning_content_ids.is.null,learning_content_ids.eq.{}')
        .order('display_order', { nullsFirst: false })
        .order('name')

      if (rootError) throw rootError
      
      // Filter out hidden categories
      const visibleRootNodes = await hiddenSkillsService.filterVisibleSkills(rootNodes || [])
      setSubjectCategories(visibleRootNodes)
      
      // Pre-fetch subcategories for all root categories to show chevrons immediately
      if (visibleRootNodes && visibleRootNodes.length > 0) {
        const subcategoriesData: Record<string, SkillTreeNode[]> = {}
        const subSubcategoriesData: Record<string, SkillTreeNode[]> = {}
        
        for (const category of visibleRootNodes) {
          const { data: childNodes } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('parent_id', category.id)
            .order('display_order', { nullsFirst: false })
            .order('name')
          
          if (childNodes && childNodes.length > 0) {
            // Filter out hidden subcategories
            const visibleChildNodes = await hiddenSkillsService.filterVisibleSkills(childNodes)
            if (visibleChildNodes.length > 0) {
              subcategoriesData[category.id] = visibleChildNodes
            }
            
            // Pre-fetch sub-subcategories for all visible subcategories
            for (const subcategory of visibleChildNodes) {
              const { data: grandchildNodes } = await supabase
                .from('skill_tree_nodes')
                .select('*')
                .eq('parent_id', subcategory.id)
                .order('display_order', { nullsFirst: false })
                .order('name')
              
              if (grandchildNodes && grandchildNodes.length > 0) {
                // Filter out hidden sub-subcategories
                const visibleGrandchildNodes = await hiddenSkillsService.filterVisibleSkills(grandchildNodes)
                if (visibleGrandchildNodes.length > 0) {
                  subSubcategoriesData[subcategory.id] = visibleGrandchildNodes
                }
              }
            }
          }
        }
        
        setSubcategories(subcategoriesData)
        setSubSubcategories(subSubcategoriesData)
      }
    } catch (error) {
      console.error('Error fetching subject categories:', error)
    }
  }

  const fetchSubcategories = async (categoryId: string) => {
    // Return if we already have subcategories for this category
    if (subcategories[categoryId]) return

    try {
      const { data: childNodes, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('parent_id', categoryId)
        .order('display_order', { nullsFirst: false })
        .order('name')

      if (error) throw error
      
      // Filter out hidden nodes
      const visibleChildNodes = await hiddenSkillsService.filterVisibleSkills(childNodes || [])
      
      setSubcategories(prev => ({
        ...prev,
        [categoryId]: visibleChildNodes
      }))
    } catch (error) {
      console.error('Error fetching subcategories:', error)
    }
  }

  const handleCategoryHover = (categoryId: string) => {
    if (hoverTimeoutRef.current) {
      clearTimeout(hoverTimeoutRef.current)
    }
    setHoveredCategoryId(categoryId)
    fetchSubcategories(categoryId)
  }

  const handleCategoryLeave = () => {
    hoverTimeoutRef.current = setTimeout(() => {
      setHoveredCategoryId(null)
    }, 200)
  }

  const handleSubmenuEnter = (categoryId: string) => {
    if (hoverTimeoutRef.current) {
      clearTimeout(hoverTimeoutRef.current)
    }
    setHoveredCategoryId(categoryId)
  }

  const handleSubmenuLeave = () => {
    hoverTimeoutRef.current = setTimeout(() => {
      setHoveredCategoryId(null)
      setHoveredSubcategoryId(null)
    }, 200)
  }

  const fetchSubSubcategories = async (subcategoryId: string) => {
    // Return if we already have sub-subcategories for this subcategory
    if (subSubcategories[subcategoryId]) return

    try {
      const { data: childNodes, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('parent_id', subcategoryId)
        .order('display_order', { nullsFirst: false })
        .order('name')

      if (error) throw error
      
      // Filter out hidden nodes
      const visibleChildNodes = await hiddenSkillsService.filterVisibleSkills(childNodes || [])
      
      setSubSubcategories(prev => ({
        ...prev,
        [subcategoryId]: visibleChildNodes
      }))
    } catch (error) {
      console.error('Error fetching sub-subcategories:', error)
    }
  }

  const subHoverTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  const handleSubcategoryHover = (subcategoryId: string) => {
    // Clear any pending timeout to prevent menu from closing
    if (subHoverTimeoutRef.current) {
      clearTimeout(subHoverTimeoutRef.current)
      subHoverTimeoutRef.current = null
    }
    setHoveredSubcategoryId(subcategoryId)
    fetchSubSubcategories(subcategoryId)
  }

  const handleSubcategoryLeave = () => {
    // Add longer delay to allow cursor to reach the submenu
    subHoverTimeoutRef.current = setTimeout(() => {
      setHoveredSubcategoryId(null)
    }, 300)
  }
  
  const handleSubSubmenuEnter = (subcategoryId: string) => {
    // Clear timeout when entering the third-level menu
    if (subHoverTimeoutRef.current) {
      clearTimeout(subHoverTimeoutRef.current)
      subHoverTimeoutRef.current = null
    }
    setHoveredSubcategoryId(subcategoryId)
  }
  
  const handleSubSubmenuLeave = () => {
    // Add delay when leaving third-level menu
    subHoverTimeoutRef.current = setTimeout(() => {
      setHoveredSubcategoryId(null)
    }, 200)
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
        setHoveredCategoryId(null)
        setHoveredSubcategoryId(null)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
      if (hoverTimeoutRef.current) {
        clearTimeout(hoverTimeoutRef.current)
      }
      if (subHoverTimeoutRef.current) {
        clearTimeout(subHoverTimeoutRef.current)
      }
    }
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
                  <TreeLogo size={32} className="text-primary-600" />
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
                    onClick={() => {
                      setSubjectsOpen(!subjectsOpen)
                      // Reset hover states when toggling menu
                      if (!subjectsOpen) {
                        setHoveredCategoryId(null)
                        setHoveredSubcategoryId(null)
                      }
                    }}
                    className="flex items-center px-3 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                  >
                    Subjects
                    <ChevronDownIcon className={`ml-1 h-4 w-4 transition-transform ${subjectsOpen ? 'rotate-180' : ''}`} />
                  </button>
                  
                  {subjectsOpen && (
                    <div className="absolute top-full left-0 mt-2 w-56 rounded-lg shadow-xl bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 py-1 z-50">
                      {subjectCategories.map(category => (
                        <div 
                          key={category.id}
                          className="relative group"
                        >
                          <div
                            onMouseEnter={() => handleCategoryHover(category.id)}
                            onMouseLeave={handleCategoryLeave}
                          >
                            <CategoryLink
                              categoryId={category.id}
                              onClick={() => {
                                setSubjectsOpen(false)
                                setHoveredCategoryId(null)
                                setHoveredSubcategoryId(null)
                              }}
                              className="flex items-center justify-between px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                            >
                              <span>{category.name}</span>
                              {/* Always show chevron for categories with potential subcategories */}
                              <ChevronDownIcon className="h-5 w-5 -rotate-90 text-primary-600 dark:text-primary-400 flex-shrink-0 ml-2" />
                            </CategoryLink>
                          </div>
                          
                          {/* Subcategory dropdown */}
                          {hoveredCategoryId === category.id && subcategories[category.id] && subcategories[category.id].length > 0 && (
                            <div 
                              className="absolute left-full top-0 ml-1 w-48 rounded-lg shadow-xl bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 py-1 z-50"
                              onMouseEnter={() => handleSubmenuEnter(category.id)}
                              onMouseLeave={handleSubmenuLeave}
                            >
                              {subcategories[category.id].map(subcategory => (
                                <div key={subcategory.id} className="relative">
                                  <div
                                    onMouseEnter={() => handleSubcategoryHover(subcategory.id)}
                                    onMouseLeave={handleSubcategoryLeave}
                                  >
                                    <CategoryLink
                                      categoryId={subcategory.id}
                                      onClick={() => {
                                        setSubjectsOpen(false)
                                        setHoveredCategoryId(null)
                                        setHoveredSubcategoryId(null)
                                      }}
                                      className="flex items-center justify-between px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                                    >
                                      <span>{subcategory.name}</span>
                                      {/* Always show chevron for better UX */}
                                      <ChevronDownIcon className="h-4 w-4 -rotate-90 text-primary-500 dark:text-primary-400 flex-shrink-0 ml-1" />
                                    </CategoryLink>
                                  </div>
                                  
                                  {/* Third level dropdown */}
                                  {hoveredSubcategoryId === subcategory.id && subSubcategories[subcategory.id] && subSubcategories[subcategory.id].length > 0 && (
                                    <div 
                                      className="absolute left-full top-0 -ml-1 w-48 rounded-lg shadow-xl bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 py-1 z-50"
                                      onMouseEnter={() => handleSubSubmenuEnter(subcategory.id)}
                                      onMouseLeave={handleSubSubmenuLeave}
                                    >
                                      {subSubcategories[subcategory.id].map(subSubcategory => (
                                        <CategoryLink
                                          key={subSubcategory.id}
                                          categoryId={subSubcategory.id}
                                          onClick={() => {
                                            setSubjectsOpen(false)
                                            setHoveredCategoryId(null)
                                            setHoveredSubcategoryId(null)
                                          }}
                                          className="block px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                                        >
                                          {subSubcategory.name}
                                        </CategoryLink>
                                      ))}
                                    </div>
                                  )}
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                      {subjectCategories.length === 0 && (
                        <div className="px-3 py-1.5 text-sm text-neutral-500 dark:text-neutral-400">
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
                        to="/spelling-vocabulary"
                        onClick={() => setFlashcardsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        Spelling & Vocabulary
                      </Link>
                      <Link
                        to="/language-trainer"
                        onClick={() => setFlashcardsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        Language Trainer
                      </Link>
                      <div className="border-t border-neutral-200 dark:border-neutral-700 my-1"></div>
                      <Link
                        to="/study-lists"
                        onClick={() => setFlashcardsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
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
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        All Tests Overview
                      </Link>
                      <div className="border-t border-neutral-200 dark:border-neutral-600 my-1"></div>
                      <Link
                        to="/test/sat"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        SAT
                      </Link>
                      <Link
                        to="/test/act"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        ACT
                      </Link>
                      <Link
                        to="/test/lsat"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        LSAT
                      </Link>
                      <Link
                        to="/test/gre"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        GRE
                      </Link>
                      <Link
                        to="/test/gmat"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        GMAT
                      </Link>
                      <Link
                        to="/test/mcat"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                      >
                        MCAT
                      </Link>
                      <div className="border-t border-neutral-200 dark:border-neutral-600 my-1"></div>
                      <Link
                        to="/iq-test"
                        onClick={() => setStandardizedTestsOpen(false)}
                        className="flex items-center px-3 py-1.5 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
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
        <div className="px-4 sm:px-6 lg:px-8 py-2 sm:py-8">
          <main>
            <Outlet />
          </main>
        </div>
      </div>

    </div>
  )
}

export default Layout