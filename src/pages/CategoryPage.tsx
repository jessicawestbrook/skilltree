import React, { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { 
  AcademicCapIcon, 
  ChartBarIcon, 
  BookOpenIcon,
  StarIcon,
  UserGroupIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid'
import { useAuth } from '../contexts/AuthContext'
import { SkillTreeNode } from '../types/database.types'
import LearningContentModal from '../components/LearningContentModal'
import CompetencyAssessment from '../components/CompetencyAssessment'

const CategoryPage: React.FC = () => {
  const { categoryId } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [category, setCategory] = useState<SkillTreeNode | null>(null)
  const [subcategories, setSubcategories] = useState<SkillTreeNode[]>([])
  const [loading, setLoading] = useState(true)
  const [isStarred, setIsStarred] = useState(false)
  const [stats, setStats] = useState({
    totalSubcategories: 0,
    totalModules: 0,
    withContent: 0,
    userProgress: 0
  })
  const [selectedNode, setSelectedNode] = useState<SkillTreeNode | null>(null)
  const [showLearningModal, setShowLearningModal] = useState(false)

  useEffect(() => {
    if (categoryId) {
      fetchCategoryData()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [categoryId, user])

  const fetchCategoryData = async () => {
    try {
      // Fetch category details
      const { data: categoryData, error: categoryError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('id', categoryId)
        .single()

      if (categoryError) throw categoryError
      setCategory(categoryData)

      // Fetch subcategories
      const { data: subcategoriesData, error: subcategoriesError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('parent_id', categoryId)
        .order('name')

      if (subcategoriesError) throw subcategoriesError
      setSubcategories(subcategoriesData || [])

      // Calculate stats
      const allDescendants = await fetchAllDescendants(categoryId!)
      const withContent = allDescendants.filter(n => n.has_learning_content).length
      
      setStats({
        totalSubcategories: subcategoriesData?.filter(n => (n.type as string) === 'category').length || 0,
        totalModules: allDescendants.length,
        withContent,
        userProgress: 0 // Will be calculated based on user progress
      })

      // Check if starred by user
      if (user) {
        try {
          const { data: starData, error: starError } = await supabase
            .from('user_starred_nodes')
            .select('id')
            .eq('user_id', user.id)
            .eq('skill_node_id', categoryId)
            .single()

          // Only set starred if query was successful and data exists
          setIsStarred(!starError && !!starData)
        } catch (error) {
          // Silently handle starring errors - user can still use the page
          console.warn('Could not check starred status:', error)
          setIsStarred(false)
        }

        // Calculate user progress
        const { data: progressData } = await supabase
          .from('user_progress')
          .select('*')
          .eq('user_id', user.id)
          .in('skill_node_id', allDescendants.map(n => n.id))

        const completed = progressData?.filter(p => p.status === 'completed' && p.rating >= 70).length || 0
        const progress = withContent > 0 ? Math.round((completed / withContent) * 100) : 0
        setStats(prev => ({ ...prev, userProgress: progress }))
      }
    } catch (error) {
      console.error('Error fetching category:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchAllDescendants = async (nodeId: string): Promise<SkillTreeNode[]> => {
    const descendants: SkillTreeNode[] = []
    
    const { data: children } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('parent_id', nodeId)

    if (children) {
      for (const child of children) {
        descendants.push(child)
        const childDescendants = await fetchAllDescendants(child.id)
        descendants.push(...childDescendants)
      }
    }

    return descendants
  }

  const toggleStar = async () => {
    if (!user) {
      navigate('/login')
      return
    }

    try {
      let success = false
      if (isStarred) {
        const { error } = await supabase
          .from('user_starred_nodes')
          .delete()
          .eq('user_id', user.id)
          .eq('skill_node_id', categoryId)
        success = !error
      } else {
        const { error } = await supabase
          .from('user_starred_nodes')
          .insert({
            user_id: user.id,
            skill_node_id: categoryId
          })
        success = !error
      }
      
      if (success) {
        setIsStarred(!isStarred)
      } else {
        console.warn('Could not update starred status - table may not be properly configured')
      }
    } catch (error) {
      console.warn('Error toggling star:', error)
      // Don't show error to user since starring is not critical functionality
    }
  }

  const handleNodeClick = (node: SkillTreeNode) => {
    if ((node.type as string) === 'category') {
      navigate(`/category/${node.id}`)
    } else if (node.has_learning_content) {
      setSelectedNode(node)
      setShowLearningModal(true)
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

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <nav className="mb-6">
        <ol className="flex items-center space-x-2 text-sm">
          <li>
            <Link to="/learning-paths" className="text-primary-600 hover:text-primary-700">
              Learning Paths
            </Link>
          </li>
          <li className="text-neutral-400">/</li>
          <li className="text-neutral-600 dark:text-neutral-400">{category.name}</li>
        </ol>
      </nav>

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
                {category.learning_area && (
                  <p className="text-neutral-600 dark:text-neutral-400 mt-1">
                    {category.learning_area}
                  </p>
                )}
              </div>
            </div>
          </div>
          
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

      {/* Competency Assessment */}
      <div className="mb-6">
        <CompetencyAssessment
          categoryId={categoryId!}
          categoryName={category.name}
          onComplete={(score, passed) => {
            // Update user progress when assessment is completed
            if (user && passed) {
              supabase
                .from('user_progress')
                .upsert({
                  user_id: user.id,
                  skill_node_id: categoryId,
                  status: 'completed',
                  rating: score,
                  last_accessed: new Date().toISOString()
                })
                .then(() => {
                  // Refresh category data to update progress
                  fetchCategoryData()
                })
            }
          }}
        />
      </div>

      {/* Subcategories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {subcategories.map(subcat => (
          <div
            key={subcat.id}
            onClick={() => handleNodeClick(subcat)}
            className="bg-white dark:bg-neutral-800 rounded-lg shadow hover:shadow-lg transition-all cursor-pointer p-4"
          >
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-semibold text-neutral-900 dark:text-white">
                {subcat.name}
              </h3>
              {(subcat.type as string) === 'category' && (
                <span className="text-xs bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 px-2 py-1 rounded">
                  Category
                </span>
              )}
            </div>
            
            {subcat.learning_area && (
              <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3 line-clamp-2">
                {subcat.learning_area}
              </p>
            )}
            
            <div className="flex items-center justify-between text-xs text-neutral-500">
              {subcat.has_learning_content ? (
                <span className="flex items-center gap-1">
                  <BookOpenIcon className="h-3 w-3" />
                  Has content
                </span>
              ) : (
                <span className="flex items-center gap-1">
                  <UserGroupIcon className="h-3 w-3" />
                  {(subcat.type as string) === 'category' ? 'Explore' : 'No content yet'}
                </span>
              )}
            </div>
          </div>
        ))}
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
    </div>
  )
}

export default CategoryPage