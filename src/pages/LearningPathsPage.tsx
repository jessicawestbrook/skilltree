import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import { SkillTreeNode } from '../types/database.types'
import { buildCategoryPath } from '../utils/categoryPaths'
import {
  AcademicCapIcon,
  ArrowRightIcon,
  CheckCircleIcon,
  LockClosedIcon,
  ChartBarIcon,
  BookOpenIcon,
  SparklesIcon,
  ClockIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

interface LearningPath {
  id: string
  name: string
  description: string
  category: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  estimatedHours: number
  nodes: string[]
  prerequisites: string[]
  icon: React.ReactNode
  color: string
}

interface PathProgress {
  pathId: string
  completedNodes: string[]
  currentNode: string | null
  percentComplete: number
}

const LearningPathsPage: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [selectedPath, setSelectedPath] = useState<LearningPath | null>(null)
  const [pathProgress, setPathProgress] = useState<Map<string, PathProgress>>(new Map())
  const [nodes, setNodes] = useState<Map<string, SkillTreeNode>>(new Map())
  const [userProgress, setUserProgress] = useState<Set<string>>(new Set())
  const [loading, setLoading] = useState(true)

  // Define learning paths - in production these would come from the database
  const learningPaths: LearningPath[] = [
    {
      id: 'web-dev-basics',
      name: 'Web Development Fundamentals',
      description: 'Learn the basics of HTML, CSS, and JavaScript to build modern websites',
      category: 'technology',
      difficulty: 'beginner',
      estimatedHours: 40,
      nodes: ['html-basics', 'css-fundamentals', 'javascript-intro', 'responsive-design'],
      prerequisites: [],
      icon: <BookOpenIcon className="h-6 w-6" />,
      color: 'blue'
    },
    {
      id: 'data-science-intro',
      name: 'Introduction to Data Science',
      description: 'Master the fundamentals of data analysis, statistics, and machine learning',
      category: 'technology',
      difficulty: 'intermediate',
      estimatedHours: 60,
      nodes: ['statistics-basics', 'python-programming', 'data-visualization', 'machine-learning-intro'],
      prerequisites: ['math-algebra', 'programming-basics'],
      icon: <ChartBarIcon className="h-6 w-6" />,
      color: 'purple'
    },
    {
      id: 'calculus-mastery',
      name: 'Calculus Complete',
      description: 'Master differential and integral calculus from basics to advanced topics',
      category: 'mathematics',
      difficulty: 'advanced',
      estimatedHours: 80,
      nodes: ['limits', 'derivatives', 'integrals', 'multivariable-calculus'],
      prerequisites: ['algebra', 'trigonometry', 'pre-calculus'],
      icon: <AcademicCapIcon className="h-6 w-6" />,
      color: 'green'
    },
    {
      id: 'business-fundamentals',
      name: 'Business Essentials',
      description: 'Learn core business concepts including finance, marketing, and management',
      category: 'business',
      difficulty: 'beginner',
      estimatedHours: 35,
      nodes: ['accounting-basics', 'marketing-101', 'management-principles', 'business-strategy'],
      prerequisites: [],
      icon: <SparklesIcon className="h-6 w-6" />,
      color: 'gold'
    },
    {
      id: 'creative-writing',
      name: 'Creative Writing Journey',
      description: 'Develop your creative writing skills from story structure to publishing',
      category: 'arts',
      difficulty: 'intermediate',
      estimatedHours: 45,
      nodes: ['story-structure', 'character-development', 'dialogue-writing', 'editing-basics'],
      prerequisites: ['grammar', 'composition'],
      icon: <BookOpenIcon className="h-6 w-6" />,
      color: 'pink'
    },
    {
      id: 'physics-foundations',
      name: 'Physics Foundations',
      description: 'Understand the fundamental principles of physics from mechanics to electricity',
      category: 'science',
      difficulty: 'intermediate',
      estimatedHours: 55,
      nodes: ['mechanics', 'thermodynamics', 'waves-and-optics', 'electricity-magnetism'],
      prerequisites: ['algebra', 'trigonometry', 'basic-calculus'],
      icon: <SparklesIcon className="h-6 w-6" />,
      color: 'teal'
    }
  ]

  useEffect(() => {
    fetchUserProgress()
    fetchNodes()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const fetchUserProgress = async () => {
    if (!user) return

    try {
      // Fetch user's completed nodes
      const { data: progress } = await supabase
        .from('user_progress')
        .select('skill_id, status')
        .eq('user_id', user.id)
        .eq('status', 'completed')

      if (progress) {
        setUserProgress(new Set(progress.map(p => p.skill_id)))
      }

      // Calculate progress for each path
      const progressMap = new Map<string, PathProgress>()
      learningPaths.forEach(path => {
        const completed = path.nodes.filter(nodeId => 
          userProgress.has(nodeId)
        )
        
        progressMap.set(path.id, {
          pathId: path.id,
          completedNodes: completed,
          currentNode: path.nodes.find(n => !userProgress.has(n)) || null,
          percentComplete: (completed.length / path.nodes.length) * 100
        })
      })
      
      setPathProgress(progressMap)
    } catch (error) {
      console.error('Error fetching user progress:', error)
    }
  }

  const fetchNodes = async () => {
    setLoading(true)
    try {
      // Fetch all nodes to get their names
      const allNodes: SkillTreeNode[] = []
      const pageSize = 1000
      let offset = 0
      let hasMore = true

      while (hasMore) {
        const { data, error } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .range(offset, offset + pageSize - 1)
          .order('name')

        if (error) throw error
        if (data) {
          allNodes.push(...data)
          hasMore = data.length === pageSize
          offset += pageSize
        } else {
          hasMore = false
        }
      }

      const nodeMap = new Map<string, SkillTreeNode>()
      allNodes.forEach(node => {
        // Try to match by partial name for demonstration
        const simplifiedId = node.name.toLowerCase().replace(/\s+/g, '-')
        nodeMap.set(simplifiedId, node)
        nodeMap.set(node.id, node)
      })
      
      setNodes(nodeMap)
    } catch (error) {
      console.error('Error fetching nodes:', error)
    } finally {
      setLoading(false)
    }
  }

  const checkPrerequisites = (path: LearningPath): boolean => {
    if (!path.prerequisites.length) return true
    return path.prerequisites.every(prereq => userProgress.has(prereq))
  }

  const getNodeName = (nodeId: string): string => {
    const node = nodes.get(nodeId)
    if (node) return node.name
    // Fallback: Convert ID to readable name
    return nodeId.split('-').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ')
  }

  const handleStartPath = async (path: LearningPath) => {
    const progress = pathProgress.get(path.id)
    if (progress?.currentNode) {
      const node = nodes.get(progress.currentNode)
      if (node) {
        const categoryPath = await buildCategoryPath(node.id)
        navigate(categoryPath ? `/${categoryPath}` : `/learning/${node.id}`)
      }
    } else if (path.nodes.length > 0) {
      const firstNode = nodes.get(path.nodes[0])
      if (firstNode) {
        const categoryPath = await buildCategoryPath(firstNode.id)
        navigate(categoryPath ? `/${categoryPath}` : `/learning/${firstNode.id}`)
      }
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner':
        return 'text-green-600 bg-green-100 dark:bg-green-900/30'
      case 'intermediate':
        return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30'
      case 'advanced':
        return 'text-red-600 bg-red-100 dark:bg-red-900/30'
      default:
        return 'text-neutral-600 bg-neutral-100 dark:bg-neutral-900/30'
    }
  }

  const getColorClasses = (color: string) => {
    const colors: Record<string, string> = {
      blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
      purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
      green: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
      gold: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400',
      pink: 'bg-pink-100 dark:bg-pink-900/30 text-pink-700 dark:text-pink-400',
      teal: 'bg-teal-100 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400'
    }
    return colors[color] || colors.blue
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-primary-600 dark:text-primary-400">
          Learning Paths
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-3xl mx-auto">
          Follow structured learning paths to master new skills. Each path includes prerequisites
          and a recommended sequence of topics.
        </p>
      </div>

      {/* Path Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {learningPaths.map(path => {
          const progress = pathProgress.get(path.id)
          const prerequisitesMet = checkPrerequisites(path)
          const isCompleted = progress?.percentComplete === 100

          return (
            <div
              key={path.id}
              className={`bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-6 ${
                prerequisitesMet ? 'hover:shadow-xl transition-shadow cursor-pointer' : 'opacity-75'
              }`}
              onClick={() => prerequisitesMet && setSelectedPath(path)}
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`p-3 rounded-lg ${getColorClasses(path.color)}`}>
                  {path.icon}
                </div>
                {!prerequisitesMet && (
                  <LockClosedIcon className="h-5 w-5 text-neutral-400" />
                )}
                {isCompleted && (
                  <CheckCircleIcon className="h-5 w-5 text-green-600" />
                )}
              </div>

              <h3 className="text-xl font-bold mb-2">{path.name}</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
                {path.description}
              </p>

              <div className="space-y-2 mb-4">
                <div className="flex items-center gap-2">
                  <span className={`text-xs px-2 py-1 rounded-full ${getDifficultyColor(path.difficulty)}`}>
                    {path.difficulty}
                  </span>
                  <span className="text-xs text-neutral-500">
                    <ClockIcon className="h-3 w-3 inline mr-1" />
                    {path.estimatedHours} hours
                  </span>
                </div>

                {/* Progress Bar */}
                {user && progress && progress.percentComplete > 0 && (
                  <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full transition-all"
                      style={{ width: `${progress.percentComplete}%` }}
                    />
                  </div>
                )}

                {/* Prerequisites Warning */}
                {!prerequisitesMet && (
                  <div className="flex items-start gap-2 p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                    <ExclamationTriangleIcon className="h-4 w-4 text-yellow-600 mt-0.5" />
                    <div className="flex-1">
                      <p className="text-xs text-yellow-700 dark:text-yellow-400">
                        Prerequisites required:
                      </p>
                      <ul className="text-xs text-yellow-600 dark:text-yellow-500 mt-1">
                        {path.prerequisites.map(prereq => (
                          <li key={prereq}>• {getNodeName(prereq)}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}
              </div>

              {prerequisitesMet && (
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    handleStartPath(path)
                  }}
                  className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
                >
                  <span>
                    {progress && progress.percentComplete > 0
                      ? progress.percentComplete === 100
                        ? 'Review Path'
                        : 'Continue Learning'
                      : 'Start Path'}
                  </span>
                  <ArrowRightIcon className="h-4 w-4" />
                </button>
              )}
            </div>
          )
        })}
      </div>

      {/* Selected Path Details Modal */}
      {selectedPath && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-neutral-900 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6">
            <div className="flex items-start justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold mb-2">{selectedPath.name}</h2>
                <p className="text-neutral-600 dark:text-neutral-400">
                  {selectedPath.description}
                </p>
              </div>
              <button
                onClick={() => setSelectedPath(null)}
                className="text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300"
              >
                ✕
              </button>
            </div>

            <div className="mb-6">
              <h3 className="font-semibold mb-3">Learning Sequence:</h3>
              <div className="space-y-3">
                {selectedPath.nodes.map((nodeId, idx) => {
                  const isCompleted = userProgress.has(nodeId)
                  const progress = pathProgress.get(selectedPath.id)
                  const isCurrent = progress?.currentNode === nodeId

                  return (
                    <div
                      key={nodeId}
                      className={`flex items-center gap-3 p-3 rounded-lg ${
                        isCompleted
                          ? 'bg-green-50 dark:bg-green-900/20'
                          : isCurrent
                          ? 'bg-primary-50 dark:bg-primary-900/20 border-2 border-primary-500'
                          : 'bg-neutral-50 dark:bg-neutral-800'
                      }`}
                    >
                      <div className="flex-shrink-0">
                        {isCompleted ? (
                          <CheckCircleIcon className="h-6 w-6 text-green-600" />
                        ) : (
                          <div className={`w-6 h-6 rounded-full border-2 ${
                            isCurrent ? 'border-primary-600' : 'border-neutral-300'
                          } flex items-center justify-center`}>
                            <span className="text-xs font-semibold">{idx + 1}</span>
                          </div>
                        )}
                      </div>
                      <div className="flex-1">
                        <p className="font-medium">{getNodeName(nodeId)}</p>
                        {isCurrent && (
                          <p className="text-xs text-primary-600 dark:text-primary-400 mt-1">
                            Current topic
                          </p>
                        )}
                      </div>
                      {(isCompleted || isCurrent) && (
                        <button
                          onClick={async () => {
                            const node = nodes.get(nodeId)
                            if (node) {
                              const categoryPath = await buildCategoryPath(node.id)
                              navigate(categoryPath ? `/${categoryPath}` : `/learning/${node.id}`)
                            }
                          }}
                          className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
                        >
                          <ArrowRightIcon className="h-5 w-5" />
                        </button>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setSelectedPath(null)}
                className="flex-1 py-2 bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
              >
                Close
              </button>
              {checkPrerequisites(selectedPath) && (
                <button
                  onClick={() => handleStartPath(selectedPath)}
                  className="flex-1 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Start Learning
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default LearningPathsPage