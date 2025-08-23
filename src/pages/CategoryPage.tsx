import React, { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate, useLocation, Link } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { 
  AcademicCapIcon, 
  ChartBarIcon, 
  BookOpenIcon,
  StarIcon,
  ClockIcon,
  TrophyIcon,
  BoltIcon
} from '@heroicons/react/24/outline'
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid'
import { useAuth } from '../contexts/AuthContext'
import { SkillTreeNode } from '../types/database.types'
import LearningContentModal from '../components/LearningContentModal'
import AdaptiveAssessment from '../components/AdaptiveAssessment'
import SEO from '../components/SEO'
import Breadcrumb from '../components/Breadcrumb'
import CategoryLink from '../components/CategoryLink'
import { AssessmentSession } from '../services/adaptiveAssessmentService'
import { createCourseStructuredData } from '../utils/structuredData'
import { resolveCategoryPath, buildCategoryPath } from '../utils/categoryPaths'

const CategoryPage: React.FC = () => {
  const params = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  
  // Handle path-based routes only - reconstruct from segments
  const { segment1, segment2, segment3, segment4 } = params
  const pathSegments = [segment1, segment2, segment3, segment4].filter(Boolean)
  const categoryPath = pathSegments.join('/')
  const [resolvedCategoryId, setResolvedCategoryId] = useState<string | null>(null)
  const [category, setCategory] = useState<SkillTreeNode | null>(null)
  const [subcategories, setSubcategories] = useState<SkillTreeNode[]>([])
  const [subcategoryChildren, setSubcategoryChildren] = useState<Record<string, SkillTreeNode[]>>({})
  const [ancestors, setAncestors] = useState<SkillTreeNode[]>([])
  const [loading, setLoading] = useState(true)
  const [isStarred, setIsStarred] = useState(false)
  const [starredSubcategories, setStarredSubcategories] = useState<Set<string>>(new Set())
  const [stats, setStats] = useState({
    totalSubcategories: 0,
    totalModules: 0,
    withContent: 0,
    userProgress: 0
  })
  const [selectedNode, setSelectedNode] = useState<SkillTreeNode | null>(null)
  const [showLearningModal, setShowLearningModal] = useState(false)
  const [showAdaptiveAssessment, setShowAdaptiveAssessment] = useState(false)

  // Resolve category path to ID
  useEffect(() => {
    const resolvePath = async () => {
      if (categoryPath) {
        const resolvedId = await resolveCategoryPath(location.pathname)
        if (resolvedId) {
          setResolvedCategoryId(resolvedId)
        } else {
          // Category not found
          setLoading(false)
        }
      }
    }
    
    resolvePath()
  }, [categoryPath, location.pathname])

  useEffect(() => {
    if (resolvedCategoryId) {
      fetchCategoryData()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resolvedCategoryId, user])

  const fetchAncestors = async (nodeId: string): Promise<SkillTreeNode[]> => {
    const ancestors: SkillTreeNode[] = []
    let currentId = nodeId

    while (currentId) {
      const { data: node, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('id', currentId)
        .single()

      if (error || !node) break

      if (node.parent_id) {
        ancestors.unshift(node) // Add to beginning to maintain order
        currentId = node.parent_id
      } else {
        // This is the root node, add it and stop
        if (node.name !== 'Knowledge') { // Don't include the root "Knowledge" node
          ancestors.unshift(node)
        }
        break
      }
    }

    return ancestors
  }

  const fetchCategoryData = async () => {
    if (!resolvedCategoryId) return
    
    try {
      // Fetch category details and all descendants in parallel
      const [categoryResult, subcategoriesResult, allDescendantsResult] = await Promise.all([
        supabase
          .from('skill_tree_nodes')
          .select('*')
          .eq('id', resolvedCategoryId)
          .single(),
        supabase
          .from('skill_tree_nodes')
          .select('*')
          .eq('parent_id', resolvedCategoryId)
          .order('display_order', { nullsFirst: false })
          .order('name'),
        // For now, just get direct descendants for basic stats
        supabase
          .from('skill_tree_nodes')
          .select('id, learning_content_ids')
          .eq('parent_id', resolvedCategoryId)
      ])

      if (categoryResult.error) throw categoryResult.error
      setCategory(categoryResult.data)

      // Fetch ancestors for breadcrumb
      const ancestorNodes = await fetchAncestors(categoryResult.data.parent_id || '')
      setAncestors(ancestorNodes)

      if (subcategoriesResult.error) throw subcategoriesResult.error
      const subcategoriesData = subcategoriesResult.data || []
      setSubcategories(subcategoriesData)

      // Get direct children for basic stats calculation
      const directChildren = allDescendantsResult.data || []

      // Fetch children for each subcategory in parallel (only if we have subcategories)
      const childrenData: Record<string, SkillTreeNode[]> = {}
      if (subcategoriesData.length > 0 && subcategoriesData.length <= 20) { // Only load children if reasonable number
        const childrenPromises = subcategoriesData.map(async (subcat) => {
          const { data: children, error: childrenError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('parent_id', subcat.id)
            .order('display_order', { nullsFirst: false })
            .order('name')
            .limit(5)

          return { subcatId: subcat.id, children: childrenError ? [] : (children || []) }
        })

        const childrenResults = await Promise.all(childrenPromises)
        childrenResults.forEach(({ subcatId, children }) => {
          childrenData[subcatId] = children
        })
      }
      setSubcategoryChildren(childrenData)

      // Calculate simplified stats using only direct children
      const withContent = directChildren.filter(n => n.learning_content_ids && n.learning_content_ids.length > 0).length
      
      setStats({
        totalSubcategories: subcategoriesData.filter(n => !n.learning_content_ids || n.learning_content_ids.length === 0).length,
        totalModules: directChildren.length,
        withContent,
        userProgress: 0 // Will be calculated based on user progress
      })

      // Check if starred by user
      if (user) {
        try {
          const { data: starData, error: starError } = await supabase
            .from('starred_items')
            .select('id')
            .eq('user_id', user.id)
            .eq('item_type', 'skill_node')
            .eq('item_id', resolvedCategoryId)
            .limit(1)

          if (starError) {
            console.warn('Could not check starred status:', starError)
            setIsStarred(false)
          } else {
            setIsStarred(starData && starData.length > 0)
          }
        } catch (error) {
          console.warn('Exception checking starred status:', error)
          setIsStarred(false)
        }

        // Calculate user progress (simplified to direct children only)
        if (directChildren.length > 0) {
          const { data: progressData } = await supabase
            .from('user_progress')
            .select('*')
            .eq('user_id', user.id)
            .in('skill_id', directChildren.map(n => n.id))

          const completed = progressData?.filter(p => p.status === 'completed' && p.rating >= 70).length || 0
          const progress = withContent > 0 ? Math.round((completed / withContent) * 100) : 0
          setStats(prev => ({ ...prev, userProgress: progress }))
        }
      }
    } catch (error) {
      console.error('Error fetching category:', error)
    } finally {
      setLoading(false)
    }
  }


  const toggleStar = async () => {
    if (!user) {
      const redirectTo = location.pathname + location.search
      navigate(`/login?redirect=${encodeURIComponent(redirectTo)}`)
      return
    }

    try {
      let success = false
      if (isStarred) {
        const { error } = await supabase
          .from('starred_items')
          .delete()
          .eq('user_id', user.id)
          .eq('item_type', 'skill_node')
          .eq('item_id', resolvedCategoryId)
        success = !error
      } else {
        const { error } = await supabase
          .from('starred_items')
          .insert({
            user_id: user.id,
            item_type: 'skill_node',
            item_id: resolvedCategoryId
          })
        success = !error
      }
      
      if (success) {
        setIsStarred(!isStarred)
      } else {
        console.warn('Could not update starred status')
      }
    } catch (error) {
      console.warn('Error toggling star:', error)
    }
  }

  const fetchStarredSubcategories = useCallback(async () => {
    if (!user || subcategories.length === 0) return

    try {
      const { data: starData, error } = await supabase
        .from('starred_items')
        .select('item_id')
        .eq('user_id', user.id)
        .eq('item_type', 'skill_node')
        .in('item_id', subcategories.map(sub => sub.id))

      if (error) {
        console.warn('Could not fetch starred subcategories:', error)
        return
      }

      const starredIds = new Set(starData?.map(item => item.item_id) || [])
      setStarredSubcategories(starredIds)
    } catch (error) {
      console.warn('Exception fetching starred subcategories:', error)
    }
  }, [user, subcategories])

  const toggleSubcategoryStar = async (subcategoryId: string) => {
    if (!user) {
      const redirectTo = location.pathname + location.search
      navigate(`/login?redirect=${encodeURIComponent(redirectTo)}`)
      return
    }

    try {
      const isCurrentlyStarred = starredSubcategories.has(subcategoryId)
      let success = false

      if (isCurrentlyStarred) {
        const { error } = await supabase
          .from('starred_items')
          .delete()
          .eq('user_id', user.id)
          .eq('item_type', 'skill_node')
          .eq('item_id', subcategoryId)
        success = !error
      } else {
        const { error } = await supabase
          .from('starred_items')
          .insert({
            user_id: user.id,
            item_type: 'skill_node',
            item_id: subcategoryId
          })
        success = !error
      }

      if (success) {
        const newStarredSubcategories = new Set(starredSubcategories)
        if (isCurrentlyStarred) {
          newStarredSubcategories.delete(subcategoryId)
        } else {
          newStarredSubcategories.add(subcategoryId)
        }
        setStarredSubcategories(newStarredSubcategories)
      }
    } catch (error) {
      console.error('Error toggling subcategory star:', error)
    }
  }

  // Fetch starred subcategories when subcategories or user changes
  useEffect(() => {
    fetchStarredSubcategories()
  }, [fetchStarredSubcategories])

  const handleNodeClick = async (node: SkillTreeNode) => {
    if (node.learning_content_ids && node.learning_content_ids.length > 0) {
      // This node has learning content - prioritize showing the learning modal
      setSelectedNode(node)
      setShowLearningModal(true)
    } else {
      // This is a category node with no learning content - navigate using hierarchical path
      try {
        const categoryPath = await buildCategoryPath(node.id)
        navigate(categoryPath ? `/${categoryPath}` : `/learning/${node.id}`)
      } catch (error) {
        console.warn('Failed to navigate to category:', error)
      }
    }
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-neutral-200 dark:bg-neutral-700 rounded w-1/3"></div>
          <div className="h-4 bg-neutral-200 dark:bg-neutral-700 rounded w-2/3"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-32 bg-neutral-200 dark:bg-neutral-700 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (!category) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <p className="text-center text-neutral-500">Category not found</p>
      </div>
    )
  }

  // Create breadcrumb data from actual category hierarchy
  // Note: We'll build these URLs properly using CategoryLink within Breadcrumb component
  const breadcrumbs = [
    { name: 'Home', url: '/' },
    ...ancestors.map(ancestor => ({
      name: ancestor.name,
      url: ``, // Will be handled by Breadcrumb component using CategoryLink
      categoryId: ancestor.id
    })),
    { name: category.name, url: location.pathname, current: true }
  ]

  // Generate SEO keywords based on category
  const keywords = [
    category.name.toLowerCase(),
    `${category.name.toLowerCase()} learning`,
    `${category.name.toLowerCase()} course`,
    `${category.name.toLowerCase()} education`,
    'online learning',
    'skill development'
  ]

  return (
    <>
      <SEO
        title={`${category.name} - Interactive Learning Course`}
        description={category.description || `Master ${category.name} with interactive lessons, practice questions, and adaptive assessments. Learn at your own pace with gamified skill trees.`}
        keywords={keywords}
        url={location.pathname}
        type="course"
        structuredData={createCourseStructuredData(category)}
      />
      <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <Breadcrumb items={breadcrumbs} />

      {/* Header */}
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 mb-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-3 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
                <AcademicCapIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-neutral-900 dark:text-white">
                  {category.name}
                </h1>
                {category.description && (
                  <p className="text-neutral-600 dark:text-neutral-400 mt-1 text-sm leading-tight">
                    {category.description}
                  </p>
                )}
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            {/* Start Learning Button */}
            {category.learning_content_ids && category.learning_content_ids.length > 0 && (
              <button
                onClick={() => {
                  setSelectedNode(category)
                  setShowLearningModal(true)
                }}
                className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors font-medium"
                title="Start learning this content"
              >
                <BookOpenIcon className="h-5 w-5" />
                Start Learning
              </button>
            )}
            
            <button
              onClick={toggleStar}
              className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg transition-colors"
              title={isStarred ? 'Unstar' : 'Star'}
            >
              {isStarred ? (
                <StarIconSolid className="h-6 w-6 text-yellow-500" />
              ) : (
                <StarIcon className="h-6 w-6 text-neutral-400" />
              )}
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-3">
            <div className="flex items-center gap-2 text-neutral-600 dark:text-neutral-400 mb-1">
              <AcademicCapIcon className="h-4 w-4" />
              <span className="text-xs">Subcategories</span>
            </div>
            <p className="text-2xl font-bold text-neutral-900 dark:text-white">
              {stats.totalSubcategories}
            </p>
          </div>
          
          <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-3">
            <div className="flex items-center gap-2 text-neutral-600 dark:text-neutral-400 mb-1">
              <BookOpenIcon className="h-4 w-4" />
              <span className="text-xs">Total Modules</span>
            </div>
            <p className="text-2xl font-bold text-neutral-900 dark:text-white">
              {stats.totalModules}
            </p>
          </div>
          
          <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-3">
            <div className="flex items-center gap-2 text-neutral-600 dark:text-neutral-400 mb-1">
              <ClockIcon className="h-4 w-4" />
              <span className="text-xs">With Content</span>
            </div>
            <p className="text-2xl font-bold text-neutral-900 dark:text-white">
              {stats.withContent}
            </p>
          </div>
          
          <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-3">
            <div className="flex items-center gap-2 text-neutral-600 dark:text-neutral-400 mb-1">
              <ChartBarIcon className="h-4 w-4" />
              <span className="text-xs">Your Progress</span>
            </div>
            <p className="text-2xl font-bold text-primary-600 dark:text-primary-400">
              {stats.userProgress}%
            </p>
          </div>
        </div>
      </div>

      {/* Learning and Assessment Section */}
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
              <BookOpenIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-neutral-900 dark:text-white">
                Learn & Test Your Knowledge
              </h2>
              <p className="text-neutral-600 dark:text-neutral-400">
                Study {category.name} content or take an adaptive assessment to demonstrate your skills
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowAdaptiveAssessment(true)}
              className="px-6 py-3 bg-neutral-200 dark:bg-neutral-700 text-neutral-800 dark:text-neutral-200 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors flex items-center gap-2 font-medium"
            >
              <BoltIcon className="h-5 w-5" />
              Start Assessment
            </button>
            {stats.withContent > 0 && (
              <Link
                to={`/learning/${resolvedCategoryId}`}
                className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2 font-medium"
              >
                <BookOpenIcon className="h-5 w-5" />
                Start Learning
              </Link>
            )}
          </div>
        </div>
        
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-4">
            <div className="flex items-center gap-2 text-gold-600 dark:text-gold-400 mb-2">
              <BoltIcon className="h-5 w-5" />
              <span className="font-medium">Computer Adaptive</span>
            </div>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Questions adapt to your skill level in real-time
            </p>
          </div>
          
          <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-4">
            <div className="flex items-center gap-2 text-primary-600 dark:text-primary-400 mb-2">
              <TrophyIcon className="h-5 w-5" />
              <span className="font-medium">Point-Based Scoring</span>
            </div>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Earn more points for harder questions
            </p>
          </div>
          
          <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-4">
            <div className="flex items-center gap-2 text-green-600 dark:text-green-400 mb-2">
              <ClockIcon className="h-5 w-5" />
              <span className="font-medium">Flexible Length</span>
            </div>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Stop anytime or continue for higher scores
            </p>
          </div>
        </div>
      </div>

      {/* Subcategories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {subcategories.map(subcat => {
          const children = subcategoryChildren[subcat.id] || []
          return (
            <div
              key={subcat.id}
              className="bg-white dark:bg-neutral-800 rounded-lg shadow hover:shadow-lg transition-all p-4"
            >
              <div className="flex items-start justify-between mb-3">
                <CategoryLink
                  categoryId={subcat.id}
                  className="font-semibold text-neutral-900 dark:text-white hover:text-primary-600 transition-colors flex-1"
                >
                  {subcat.name}
                </CategoryLink>
                <button
                  onClick={(e) => {
                    e.preventDefault()
                    toggleSubcategoryStar(subcat.id)
                  }}
                  className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded transition-colors ml-2 flex-shrink-0"
                  title={starredSubcategories.has(subcat.id) ? 'Unstar' : 'Star'}
                >
                  {starredSubcategories.has(subcat.id) ? (
                    <StarIconSolid className="h-4 w-4 text-yellow-500" />
                  ) : (
                    <StarIcon className="h-4 w-4 text-neutral-400 hover:text-yellow-500" />
                  )}
                </button>
              </div>
              
              
              {children.length > 0 && (
                <div className="space-y-2">
                  {children.map(child => {
                    const isCategory = !child.learning_content_ids || child.learning_content_ids.length === 0
                    const hasContent = child.learning_content_ids && child.learning_content_ids.length > 0
                    
                    const content = (
                      <>
                        {hasContent ? (
                          <BookOpenIcon className="h-3 w-3 text-green-500 flex-shrink-0" />
                        ) : (
                          <div className="h-3 w-3 border border-neutral-300 dark:border-neutral-600 rounded-full flex-shrink-0"></div>
                        )}
                        <span className="truncate">{child.name}</span>
                      </>
                    )
                    
                    if (isCategory) {
                      return (
                        <CategoryLink
                          key={child.id}
                          categoryId={child.id}
                          className="flex items-center gap-2 text-sm text-neutral-600 dark:text-neutral-400 hover:text-primary-600 py-1 px-2 rounded hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
                        >
                          {content}
                        </CategoryLink>
                      )
                    } else {
                      return (
                        <div
                          key={child.id}
                          onClick={() => handleNodeClick(child)}
                          className="flex items-center gap-2 text-sm text-neutral-600 dark:text-neutral-400 hover:text-primary-600 cursor-pointer py-1 px-2 rounded hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
                        >
                          {content}
                        </div>
                      )
                    }
                  })}
                  {children.length === 5 && (
                    <CategoryLink
                      categoryId={subcat.id}
                      className="text-xs text-primary-600 dark:text-primary-400 hover:underline py-1 px-2 block"
                    >
                      View all...
                    </CategoryLink>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {subcategories.length === 0 && (
        <div className="text-center py-12">
          <p className="text-neutral-500 dark:text-neutral-400">
            No subcategories found in this category
          </p>
        </div>
      )}

      {/* Learning Modal */}
      {selectedNode && showLearningModal && (
        <LearningContentModal
          node={selectedNode}
          isOpen={showLearningModal}
          onClose={() => {
            setShowLearningModal(false)
            setSelectedNode(null)
          }}
        />
      )}

      {/* Adaptive Assessment Modal */}
      {showAdaptiveAssessment && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
            <AdaptiveAssessment
              categoryId={resolvedCategoryId!}
              categoryName={category.name}
              sessionType="assessment"
              onComplete={(session: AssessmentSession) => {
                // Update user progress when assessment is completed
                if (user) {
                  supabase
                    .from('user_progress')
                    .upsert({
                      user_id: user.id,
                      skill_id: resolvedCategoryId,
                      status: 'completed',
                      rating: session.total_points,
                      last_accessed: new Date().toISOString()
                    })
                    .then(() => {
                      // Refresh category data to update progress
                      fetchCategoryData()
                    })
                }
                setShowAdaptiveAssessment(false)
              }}
              onExit={() => setShowAdaptiveAssessment(false)}
            />
          </div>
        </div>
      )}
    </div>
    </>
  )
}

export default CategoryPage