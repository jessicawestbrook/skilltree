import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import { studyListService } from '../services/studyListService'
import { UserProgress, SkillTreeNode, StudyList } from '../types/database.types'
import { 
  TrophyIcon, 
  ClockIcon, 
  BookOpenIcon,
  ChartBarIcon,
  RocketLaunchIcon,
  HeartIcon,
  AcademicCapIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'
import { StarIcon as StarSolidIcon } from '@heroicons/react/24/solid'

interface DashboardStats {
  completedLessons: number
  averageRating: number
  totalTimeSpent: number
  starredItemsCount: number
  studyListsCount: number
  inProgressCount: number
}

const ProfilePage: React.FC = () => {
  const { user } = useAuth()
  const [recentProgress, setRecentProgress] = useState<UserProgress[]>([])
  const [recommendedNodes, setRecommendedNodes] = useState<SkillTreeNode[]>([])
  const [studyLists, setStudyLists] = useState<StudyList[]>([])
  const [stats, setStats] = useState<DashboardStats>({
    completedLessons: 0,
    averageRating: 0,
    totalTimeSpent: 0,
    starredItemsCount: 0,
    studyListsCount: 0,
    inProgressCount: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user) {
      fetchUserData()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const fetchUserData = async () => {
    if (!user) return

    try {
      // Fetch user progress
      const { data: progressData, error: progressError } = await supabase
        .from('user_progress')
        .select('*')
        .eq('user_id', user.id)
        .order('last_accessed', { ascending: false })

      if (progressError) throw progressError

      if (progressData) {
        setRecentProgress(progressData.slice(0, 5)) // Show 5 most recent

        // Calculate stats
        const completed = progressData.filter(p => p.status === 'completed')
        const inProgress = progressData.filter(p => p.status === 'in_progress')
        const avgRating = completed.length > 0
          ? completed.reduce((acc, p) => acc + p.rating, 0) / completed.length
          : 0

        setStats(prev => ({
          ...prev,
          completedLessons: completed.length,
          averageRating: Math.round(avgRating),
          inProgressCount: inProgress.length
        }))
      }

      // Fetch starred items
      const starred = await studyListService.getStarredItems(user.id)
      
      // Fetch study lists
      const lists = await studyListService.getUserStudyLists(user.id)
      setStudyLists(lists)

      setStats(prev => ({
        ...prev,
        starredItemsCount: starred.length,
        studyListsCount: lists.length
      }))

      // Fetch recommended content
      await fetchRecommendedContent()

    } catch (error) {
      console.error('Error fetching user data:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchRecommendedContent = async () => {
    try {
      // Get recommended content based on learning areas the user hasn't explored much
      const { data, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('type', 'category')
        .eq('has_learning_content', true)
        .limit(6)
        .order('updated_at', { ascending: false })

      if (error) throw error
      if (data) {
        setRecommendedNodes(data)
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error)
    }
  }

  const getProgressColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100 dark:bg-green-900/30'
      case 'in_progress': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30'
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-900/30'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 rounded-xl p-6 border border-primary-200 dark:border-primary-800">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-neutral-900 dark:text-white">
              Welcome back! 🌟
            </h1>
            <p className="text-neutral-600 dark:text-neutral-400 mt-1">
              Continue your learning journey and explore new topics
            </p>
          </div>
          <div className="hidden md:block">
            <RocketLaunchIcon className="h-16 w-16 text-primary-500 opacity-50" />
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">Completed</p>
              <p className="text-2xl font-bold text-green-600">{stats.completedLessons}</p>
            </div>
            <TrophyIcon className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">In Progress</p>
              <p className="text-2xl font-bold text-yellow-600">{stats.inProgressCount}</p>
            </div>
            <ClockIcon className="h-8 w-8 text-yellow-600" />
          </div>
        </div>

        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">Avg Score</p>
              <p className="text-2xl font-bold text-gold-600">{stats.averageRating}%</p>
            </div>
            <ChartBarIcon className="h-8 w-8 text-gold-600" />
          </div>
        </div>

        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">Starred</p>
              <p className="text-2xl font-bold text-purple-600">{stats.starredItemsCount}</p>
            </div>
            <StarSolidIcon className="h-8 w-8 text-purple-600" />
          </div>
        </div>

        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">Study Lists</p>
              <p className="text-2xl font-bold text-blue-600">{stats.studyListsCount}</p>
            </div>
            <BookOpenIcon className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">Email</p>
              <p className="text-xs font-medium truncate text-neutral-700 dark:text-neutral-300">
                {user?.email?.split('@')[0]}
              </p>
            </div>
            <AcademicCapIcon className="h-8 w-8 text-primary-600" />
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Recent Progress */}
        <div className="lg:col-span-2 bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">Recent Activity</h2>
            <Link 
              to="/learning-paths" 
              className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center gap-1"
            >
              View All <ArrowRightIcon className="h-4 w-4" />
            </Link>
          </div>
          
          {recentProgress.length === 0 ? (
            <div className="text-center py-8">
              <BookOpenIcon className="h-12 w-12 text-neutral-400 mx-auto mb-4" />
              <p className="text-neutral-600 dark:text-neutral-400 mb-4">
                No learning progress yet. Start exploring!
              </p>
              <Link 
                to="/learning-paths"
                className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                <RocketLaunchIcon className="h-4 w-4" />
                Explore Skill Tree
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {recentProgress.map((item, index) => (
                <div 
                  key={item.id}
                  className="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-900 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${item.status === 'completed' ? 'bg-green-500' : item.status === 'in_progress' ? 'bg-yellow-500' : 'bg-gray-400'}`}></div>
                    <div>
                      <h3 className="font-medium text-neutral-900 dark:text-white">Learning Module</h3>
                      <p className="text-sm text-neutral-600 dark:text-neutral-400">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium mr-2 ${getProgressColor(item.status)}`}>
                          {item.status.replace('_', ' ')}
                        </span>
                        {item.status === 'completed' && `Score: ${item.rating}%`}
                      </p>
                    </div>
                  </div>
                  <span className="text-xs text-neutral-500">
                    {new Date(item.last_accessed).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="space-y-6">
          {/* Study Lists Quick Access */}
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 border border-neutral-200 dark:border-neutral-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">Study Lists</h3>
              <Link 
                to="/study-lists" 
                className="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                View All
              </Link>
            </div>
            
            {studyLists.length === 0 ? (
              <div className="text-center py-4">
                <HeartIcon className="h-8 w-8 text-neutral-400 mx-auto mb-2" />
                <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
                  No study lists yet
                </p>
                <Link 
                  to="/study-lists"
                  className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                >
                  Create your first list
                </Link>
              </div>
            ) : (
              <div className="space-y-2">
                {studyLists.slice(0, 3).map(list => (
                  <div key={list.id} className="flex items-center gap-2 p-2 rounded-lg hover:bg-neutral-50 dark:hover:bg-neutral-700">
                    <div 
                      className="w-3 h-3 rounded-full flex-shrink-0"
                      style={{ backgroundColor: list.color }}
                    ></div>
                    <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300 truncate">
                      {list.name}
                    </span>
                  </div>
                ))}
                {studyLists.length > 3 && (
                  <p className="text-xs text-neutral-500 mt-2">
                    +{studyLists.length - 3} more lists
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Quick Navigation */}
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 border border-neutral-200 dark:border-neutral-700">
            <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Quick Access</h3>
            <div className="space-y-2">
              <Link 
                to="/spelling-bee"
                className="flex items-center gap-3 p-3 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors group"
              >
                <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                  <span className="text-blue-600 text-sm font-bold">Aa</span>
                </div>
                <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300 group-hover:text-primary-600">
                  Spelling Bee
                </span>
              </Link>
              
              <Link 
                to="/vocabulary-trainer"
                className="flex items-center gap-3 p-3 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors group"
              >
                <div className="w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                  <BookOpenIcon className="h-4 w-4 text-green-600" />
                </div>
                <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300 group-hover:text-primary-600">
                  Vocabulary
                </span>
              </Link>
              
              <Link 
                to="/language-trainer"
                className="flex items-center gap-3 p-3 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors group"
              >
                <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                  <span className="text-purple-600 text-sm">🌍</span>
                </div>
                <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300 group-hover:text-primary-600">
                  Languages
                </span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Recommended Content */}
      {recommendedNodes.length > 0 && (
        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">Recommended for You</h2>
            <Link 
              to="/learning-paths" 
              className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center gap-1"
            >
              Explore More <ArrowRightIcon className="h-4 w-4" />
            </Link>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recommendedNodes.map(node => (
              <Link
                key={node.id}
                to={`/category/${node.id}`}
                className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-md transition-all group"
              >
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-neutral-900 dark:text-white group-hover:text-primary-600 line-clamp-2">
                    {node.name}
                  </h3>
                  <ArrowRightIcon className="h-4 w-4 text-neutral-400 group-hover:text-primary-500 flex-shrink-0 ml-2" />
                </div>
                <p className="text-xs text-neutral-600 dark:text-neutral-400 mb-2">
                  {node.learning_area || 'General'}
                </p>
                <div className="text-xs text-primary-600 font-medium">
                  Start Learning →
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ProfilePage