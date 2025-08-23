import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import { studyListService } from '../services/studyListService'
import { UserProgress, StudyList } from '../types/database.types'
import { recommendationService, RecommendationScore } from '../services/recommendationService'
import { buildCategoryPath } from '../utils/categoryPaths'
import { 
  TrophyIcon, 
  ClockIcon, 
  BookOpenIcon,
  ChartBarIcon,
  RocketLaunchIcon,
  HeartIcon,
  AcademicCapIcon,
  ArrowRightIcon,
  QuestionMarkCircleIcon,
  CheckCircleIcon,
  XCircleIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ArrowPathIcon
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

interface ReviewQuestion {
  id: string
  question: string
  options?: string[]
  correct_answer?: string
  explanation?: string
  skill_id?: string
  node_name?: string
  category?: string
  last_reviewed?: string
  times_reviewed?: number
  last_correct?: boolean
}

interface Flashcard {
  id: string
  type: 'vocabulary' | 'spelling' | 'language' | 'question'
  front: string
  back: string
  details?: string
  difficulty?: string
  category?: string
  isFlipped?: boolean
}

const ProfilePage: React.FC = () => {
  const { user } = useAuth()
  const [recentProgress, setRecentProgress] = useState<UserProgress[]>([])
  const [recommendedNodes, setRecommendedNodes] = useState<RecommendationScore[]>([])
  const [nodePaths, setNodePaths] = useState<Record<string, string>>({})
  const [studyLists, setStudyLists] = useState<StudyList[]>([])
  const [starredItems, setStarredItems] = useState<any[]>([])
  const [reviewQuestions, setReviewQuestions] = useState<ReviewQuestion[]>([])
  const [showingAnswer, setShowingAnswer] = useState<string | null>(null)
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({})
  const [flashcards, setFlashcards] = useState<Flashcard[]>([])
  const [currentFlashcardIndex, setCurrentFlashcardIndex] = useState(0)
  const [flippedCards, setFlippedCards] = useState<Set<string>>(new Set())
  const [stats, setStats] = useState<DashboardStats>({
    completedLessons: 0,
    averageRating: 0,
    totalTimeSpent: 0,
    starredItemsCount: 0,
    studyListsCount: 0,
    inProgressCount: 0
  })
  const [loading, setLoading] = useState(true)

  const fetchFlashcards = async () => {
    try {
      if (!user) return
      
      const flashcardsList: Flashcard[] = []
      
      // Fetch some vocabulary words
      const { data: vocabWords, error: vocabError } = await supabase
        .from('spelling_words')
        .select('*')
        .not('definition', 'is', null)
        .limit(3)
        .order('created_at', { ascending: false })
      
      if (!vocabError && vocabWords) {
        vocabWords.forEach(word => {
          flashcardsList.push({
            id: `vocab-${word.id}`,
            type: 'vocabulary',
            front: word.word,
            back: word.definition || 'No definition available',
            details: word.part_of_speech,
            difficulty: word.difficulty,
            category: 'Vocabulary'
          })
        })
      }
      
      // Fetch some spelling words  
      const { data: spellingWords, error: spellingError } = await supabase
        .from('spelling_words')
        .select('*')
        .is('definition', null)
        .limit(2)
        .order('created_at', { ascending: false })
      
      if (!spellingError && spellingWords) {
        spellingWords.forEach(word => {
          flashcardsList.push({
            id: `spelling-${word.id}`,
            type: 'spelling',
            front: 'Spell this word',
            back: word.word,
            difficulty: word.difficulty,
            category: 'Spelling'
          })
        })
      }
      
      // Fetch some questions from user's progress
      if (recentProgress.length > 0) {
        const nodeIds = recentProgress.slice(0, 2).map(p => p.skill_id)
        const { data: questions, error: questionsError } = await supabase
          .from('questions')
          .select('*')
          .in('skill_id', nodeIds)
          .limit(2)
        
        if (!questionsError && questions) {
          questions.forEach(q => {
            flashcardsList.push({
              id: `question-${q.id}`,
              type: 'question',
              front: q.question,
              back: q.correct_answer || 'No answer available',
              details: q.explanation,
              category: 'Review Question'
            })
          })
        }
      }
      
      setFlashcards(flashcardsList)
    } catch (error) {
      console.error('Error fetching flashcards:', error)
    }
  }

  const fetchReviewQuestions = async () => {
    try {
      if (!user) return

      // Get user's progress to find topics they've studied
      const { data: userProgress, error: progressError } = await supabase
        .from('user_progress')
        .select('skill_id')
        .eq('user_id', user.id)
        .in('status', ['completed', 'in_progress'])
        .limit(10)

      if (progressError) {
        console.error('Error fetching user progress for review:', progressError)
        return
      }

      if (!userProgress || userProgress.length === 0) {
        return
      }

      const nodeIds = userProgress.map(p => p.skill_id)

      // Fetch questions from these nodes
      const { data: questions, error: questionsError } = await supabase
        .from('questions')
        .select(`
          id,
          question,
          options,
          correct_answer,
          explanation
        `)
        .limit(5)
        .order('created_at', { ascending: false })

      if (questionsError) {
        console.error('Error fetching review questions:', questionsError)
        return
      }

      if (questions) {
        const reviewQuestions = questions.map((q: any) => ({
          id: q.id,
          question: q.question,
          options: q.options,
          correct_answer: q.correct_answer,
          explanation: q.explanation,
          skill_id: undefined,
          node_name: 'Review Question',
          category: 'General'
        }))
        setReviewQuestions(reviewQuestions)
      }
    } catch (error) {
      console.error('Error in fetchReviewQuestions:', error)
    }
  }

  useEffect(() => {
    if (user) {
      fetchUserData()
      fetchReviewQuestions()
      fetchFlashcards()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const fetchUserData = async () => {
    if (!user) return

    try {
      // Fetch user progress with node details
      const { data: progressData, error: progressError } = await supabase
        .from('user_progress')
        .select(`
          *,
          skill_tree_nodes!skill_id (
            id,
            name,
            learning_area,
            description
          )
        `)
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
      
      // Fetch details for different types of starred items
      const starredWithDetails = await Promise.all(
        starred.map(async (item) => {
          if (item.item_type === 'skill_node') {
            const { data: nodeData } = await supabase
              .from('skill_tree_nodes')
              .select('*')
              .eq('id', item.item_id)
              .single()
            
            return {
              ...item,
              nodeData,
              displayType: 'Learning Module'
            }
          } else if (item.item_type === 'spelling_word') {
            // For spelling words, the data might be stored in item_data
            if (item.item_data && item.item_data.word) {
              return {
                ...item,
                wordData: item.item_data,
                displayType: 'Spelling Word'
              }
            }
            // Fallback to fetching from spelling_words table
            const { data: wordData } = await supabase
              .from('spelling_words')
              .select('*')
              .eq('id', item.item_id)
              .maybeSingle()
            
            return {
              ...item,
              wordData: wordData || item.item_data,
              displayType: 'Spelling Word'
            }
          } else if (item.item_type === 'vocabulary_word') {
            // For vocabulary words, the data is stored in item_data
            if (item.item_data && item.item_data.word) {
              return {
                ...item,
                wordData: item.item_data,
                displayType: 'Vocabulary Word'
              }
            }
            // Fallback to fetching from spelling_words table
            const { data: wordData } = await supabase
              .from('spelling_words')
              .select('*')
              .eq('id', item.item_id)
              .maybeSingle()
            
            return {
              ...item,
              wordData: wordData || item.item_data,
              displayType: 'Vocabulary Word'
            }
          } else if (item.item_type === 'language_question') {
            // For language questions, check if data is in item_data first
            if (item.item_data && (item.item_data.question || item.item_data.text)) {
              return {
                ...item,
                questionData: item.item_data,
                displayType: 'Language Question'
              }
            }
            // Fallback to fetching from language_questions table
            const { data: questionData } = await supabase
              .from('language_questions')
              .select('*')
              .eq('id', item.item_id)
              .maybeSingle()
            
            return {
              ...item,
              questionData: questionData || item.item_data,
              displayType: 'Language Question'
            }
          }
          return {
            ...item,
            displayType: 'Other'
          }
        })
      )
      
      setStarredItems(starredWithDetails)
      
      // Fetch study lists
      const lists = await studyListService.getUserStudyLists(user.id)
      setStudyLists(lists)

      setStats(prev => ({
        ...prev,
        starredItemsCount: starred.length,
        studyListsCount: lists.length
      }))
      
      // Build paths for starred skill nodes and recent progress
      const allNodeIds = new Set<string>()
      
      // Collect node IDs from starred items
      starredWithDetails.forEach(item => {
        if ('nodeData' in item && item.nodeData && item.nodeData.id) {
          allNodeIds.add(item.nodeData.id)
        }
      })
      
      // Collect node IDs from recent progress
      if (progressData) {
        progressData.forEach(p => {
          if (p.skill_id) {
            allNodeIds.add(p.skill_id)
          }
        })
      }
      
      // Build all paths
      const paths: Record<string, string> = {}
      for (const nodeId of Array.from(allNodeIds)) {
        try {
          const path = await buildCategoryPath(nodeId)
          paths[nodeId] = path ? `/${path}` : `/learning/${nodeId}`
        } catch (err) {
          console.error(`Error building path for node ${nodeId}:`, err)
          paths[nodeId] = `/learning/${nodeId}`
        }
      }
      setNodePaths(prev => ({ ...prev, ...paths }))

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
      if (!user) return
      
      // Get personalized recommendations based on interest assessment and activity
      const recommendations = await recommendationService.getRecommendations(user.id, {
        maxRecommendations: 6,
        excludeCompleted: true
      })
      
      setRecommendedNodes(recommendations)
      
      // Build paths for all recommended nodes
      const paths: Record<string, string> = {}
      for (const rec of recommendations) {
        try {
          const path = await buildCategoryPath(rec.node.id)
          paths[rec.node.id] = path ? `/${path}` : `/learning/${rec.node.id}`
        } catch (err) {
          console.error(`Error building path for node ${rec.node.id}:`, err)
          // Fallback to learning page if path can't be built
          paths[rec.node.id] = `/learning/${rec.node.id}`
        }
      }
      setNodePaths(prev => ({ ...prev, ...paths }))
    } catch (error) {
      console.error('Error fetching recommendations:', error)
      // Fallback to basic recommendations
      try {
        const { data, error: fallbackError } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .not('learning_content_ids', 'eq', '{}')
          .limit(6)
          .order('updated_at', { ascending: false })

        if (fallbackError) throw fallbackError
        if (data) {
          const fallbackRecs = data.map(node => ({
            node,
            score: 0.5,
            category: 'ready_to_learn' as const,
            reasons: ['Explore this topic']
          }))
          setRecommendedNodes(fallbackRecs)
          
          // Build paths for fallback nodes
          const paths: Record<string, string> = {}
          for (const node of data) {
            try {
              const path = await buildCategoryPath(node.id)
              paths[node.id] = path ? `/${path}` : `/learning/${node.id}`
            } catch (err) {
              console.error(`Error building path for node ${node.id}:`, err)
              paths[node.id] = `/learning/${node.id}`
            }
          }
          setNodePaths(prev => ({ ...prev, ...paths }))
        }
      } catch (fallbackError) {
        console.error('Error fetching fallback recommendations:', fallbackError)
      }
    }
  }

  const handleAnswerSelect = (questionId: string, answer: string) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }))
  }

  const checkAnswer = (questionId: string) => {
    setShowingAnswer(showingAnswer === questionId ? null : questionId)
  }
  
  const flipCard = (cardId: string) => {
    setFlippedCards(prev => {
      const newSet = new Set(prev)
      if (newSet.has(cardId)) {
        newSet.delete(cardId)
      } else {
        newSet.add(cardId)
      }
      return newSet
    })
  }
  
  const nextFlashcard = () => {
    if (currentFlashcardIndex < flashcards.length - 1) {
      setCurrentFlashcardIndex(prev => prev + 1)
    } else {
      setCurrentFlashcardIndex(0) // Loop back to start
    }
  }
  
  const previousFlashcard = () => {
    if (currentFlashcardIndex > 0) {
      setCurrentFlashcardIndex(prev => prev - 1)
    } else {
      setCurrentFlashcardIndex(flashcards.length - 1) // Loop to end
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

      {/* Interest-Based Quick Recommendations */}
      {recommendedNodes.length > 0 && (
        <div className="bg-gradient-to-r from-purple-50 to-primary-50 dark:from-purple-900/20 dark:to-primary-900/20 rounded-xl p-6 border border-purple-200 dark:border-purple-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">Based on Your Interests</h2>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">Recommendations from your assessment results</p>
            </div>
            <div className="hidden md:block">
              <HeartIcon className="h-8 w-8 text-purple-500 opacity-70" />
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
            {recommendedNodes.slice(0, 3).map(recommendation => {
              const { node, reasons } = recommendation
              const nodePath = nodePaths[node.id] || `/learning/${node.id}`
              return (
                <Link
                  key={node.id}
                  to={nodePath}
                  className="p-3 rounded-lg bg-white/70 dark:bg-neutral-800/70 border border-white/50 dark:border-neutral-700/50 hover:bg-white dark:hover:bg-neutral-800 hover:shadow-md transition-all group"
                >
                  <h3 className="font-medium text-neutral-900 dark:text-white group-hover:text-primary-600 line-clamp-1 mb-1">
                    {node.name}
                  </h3>
                  {reasons.length > 0 && (
                    <p className="text-xs text-purple-600 dark:text-purple-400 mb-2">
                      {reasons[0]}
                    </p>
                  )}
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-neutral-500">
                      {node.learning_area}
                    </span>
                    <ArrowRightIcon className="h-3 w-3 text-primary-500" />
                  </div>
                </Link>
              )
            })}
          </div>
          
          {recommendedNodes.length > 3 && (
            <div className="mt-4 text-center">
              <Link 
                to="/learning-paths" 
                className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
              >
                <RocketLaunchIcon className="h-4 w-4" />
                See All Recommendations
              </Link>
            </div>
          )}
        </div>
      )}

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
              {recentProgress.map((item: any) => {
                const nodeName = item.skill_tree_nodes?.name || 'Learning Module'
                const nodeArea = item.skill_tree_nodes?.learning_area
                const nodePath = nodePaths[item.skill_id] || `/learning/${item.skill_id}`
                return (
                  <Link
                    to={nodePath}
                    key={item.id}
                    className="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-900 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors cursor-pointer"
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${item.status === 'completed' ? 'bg-green-500' : item.status === 'in_progress' ? 'bg-yellow-500' : 'bg-gray-400'}`}></div>
                      <div>
                        <h3 className="font-medium text-neutral-900 dark:text-white">{nodeName}</h3>
                        <p className="text-sm text-neutral-600 dark:text-neutral-400">
                          {nodeArea && <span className="text-xs mr-2">{nodeArea}</span>}
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
                  </Link>
                )
              })}
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

          {/* Flashcard Review Box */}
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 border border-neutral-200 dark:border-neutral-700">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">Quick Review</h3>
              <div className="flex items-center gap-2">
                <span className="text-xs text-neutral-500">
                  {flashcards.length > 0 ? `${currentFlashcardIndex + 1}/${flashcards.length}` : '0/0'}
                </span>
                <Link 
                  to="/vocabulary-trainer" 
                  className="text-primary-600 hover:text-primary-700 text-xs font-medium"
                >
                  Study All
                </Link>
              </div>
            </div>
            
            {flashcards.length === 0 ? (
              <div className="text-center py-8">
                <BookOpenIcon className="h-8 w-8 text-neutral-400 mx-auto mb-2" />
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  No flashcards available yet
                </p>
                <p className="text-xs text-neutral-500 mt-1">
                  Start learning to see review cards here
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {/* Current Flashcard */}
                <div 
                  className="relative h-48 cursor-pointer perspective-1000"
                  onClick={() => flipCard(flashcards[currentFlashcardIndex].id)}
                >
                  <div className={`absolute inset-0 w-full h-full transition-transform duration-500 transform-style-preserve-3d ${
                    flippedCards.has(flashcards[currentFlashcardIndex].id) ? 'rotate-y-180' : ''
                  }`}>
                    {/* Front of card */}
                    <div className="absolute inset-0 w-full h-full backface-hidden rounded-lg bg-gradient-to-br from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 border border-primary-200 dark:border-primary-700 p-4 flex flex-col justify-center items-center text-center">
                      <span className="text-xs text-primary-600 dark:text-primary-400 mb-2">
                        {flashcards[currentFlashcardIndex].category}
                      </span>
                      <p className="text-base font-medium text-neutral-800 dark:text-neutral-200">
                        {flashcards[currentFlashcardIndex].front}
                      </p>
                      {flashcards[currentFlashcardIndex].difficulty && (
                        <span className="text-xs text-neutral-500 mt-2">
                          Difficulty: {flashcards[currentFlashcardIndex].difficulty}
                        </span>
                      )}
                      <ArrowPathIcon className="h-4 w-4 text-neutral-400 mt-3" />
                    </div>
                    
                    {/* Back of card */}
                    <div className="absolute inset-0 w-full h-full backface-hidden rotate-y-180 rounded-lg bg-gradient-to-br from-gold-50 to-primary-50 dark:from-gold-900/20 dark:to-primary-900/20 border border-gold-200 dark:border-gold-700 p-4 flex flex-col justify-center items-center text-center">
                      <p className="text-lg font-semibold text-neutral-800 dark:text-neutral-200">
                        {flashcards[currentFlashcardIndex].back}
                      </p>
                      {flashcards[currentFlashcardIndex].details && (
                        <p className="text-xs text-neutral-600 dark:text-neutral-400 mt-2">
                          {flashcards[currentFlashcardIndex].details}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
                
                {/* Navigation Controls */}
                <div className="flex items-center justify-between">
                  <button
                    onClick={previousFlashcard}
                    className="p-2 rounded-lg bg-neutral-100 dark:bg-neutral-700 hover:bg-neutral-200 dark:hover:bg-neutral-600 transition-colors"
                    disabled={flashcards.length === 0}
                  >
                    <ChevronLeftIcon className="h-4 w-4 text-neutral-600 dark:text-neutral-300" />
                  </button>
                  
                  <div className="flex gap-1">
                    {flashcards.map((_, index) => (
                      <button
                        key={index}
                        onClick={() => setCurrentFlashcardIndex(index)}
                        className={`w-2 h-2 rounded-full transition-colors ${
                          index === currentFlashcardIndex 
                            ? 'bg-primary-600' 
                            : 'bg-neutral-300 dark:bg-neutral-600'
                        }`}
                      />
                    ))}
                  </div>
                  
                  <button
                    onClick={nextFlashcard}
                    className="p-2 rounded-lg bg-neutral-100 dark:bg-neutral-700 hover:bg-neutral-200 dark:hover:bg-neutral-600 transition-colors"
                    disabled={flashcards.length === 0}
                  >
                    <ChevronRightIcon className="h-4 w-4 text-neutral-600 dark:text-neutral-300" />
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Starred Learning Items */}
      {starredItems.length > 0 && (
        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <StarSolidIcon className="h-5 w-5 text-gold-500" />
              <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">Your Starred Learning Items</h2>
            </div>
            <span className="text-sm text-neutral-600 dark:text-neutral-400">
              {starredItems.length} item{starredItems.length !== 1 ? 's' : ''}
            </span>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {starredItems.slice(0, 6).map(item => {
              // Handle different types of starred items
              if (item.nodeData) {
                // Skill tree node
                const node = item.nodeData
                const nodePath = nodePaths[node.id] || `/learning/${node.id}`
                return (
                  <Link
                    key={item.id}
                    to={nodePath}
                    className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-700 hover:border-gold-300 dark:hover:border-gold-600 hover:shadow-md transition-all group bg-gradient-to-br from-white to-gold-50/30 dark:from-neutral-800 dark:to-gold-900/10"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-neutral-900 dark:text-white group-hover:text-primary-600 line-clamp-2">
                        {node.name}
                      </h3>
                      <StarSolidIcon className="h-4 w-4 text-gold-500 flex-shrink-0 ml-2" />
                    </div>
                    <p className="text-xs text-neutral-600 dark:text-neutral-400 mb-2">
                      {node.learning_area || 'General'}
                    </p>
                    {node.description && (
                      <p className="text-xs text-neutral-500 dark:text-neutral-400 line-clamp-2 mb-2">
                        {node.description}
                      </p>
                    )}
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-neutral-500">
                        Starred {new Date(item.created_at).toLocaleDateString()}
                      </span>
                      <ArrowRightIcon className="h-4 w-4 text-primary-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  </Link>
                )
              } else if (item.wordData) {
                // Spelling or vocabulary word
                const word = item.wordData
                const link = item.item_type === 'spelling_word' ? '/spelling-bee' : '/vocabulary-trainer'
                return (
                  <Link
                    key={item.id}
                    to={link}
                    className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-700 hover:border-gold-300 dark:hover:border-gold-600 hover:shadow-md transition-all group bg-gradient-to-br from-white to-gold-50/30 dark:from-neutral-800 dark:to-gold-900/10"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-neutral-900 dark:text-white group-hover:text-primary-600">
                        {word.word}
                      </h3>
                      <StarSolidIcon className="h-4 w-4 text-gold-500 flex-shrink-0 ml-2" />
                    </div>
                    <p className="text-xs text-neutral-600 dark:text-neutral-400 mb-2">
                      {item.displayType}
                    </p>
                    {word.definition && (
                      <p className="text-xs text-neutral-500 dark:text-neutral-400 line-clamp-2 mb-2">
                        {word.definition}
                      </p>
                    )}
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-neutral-500">
                        Difficulty: {word.difficulty || 'Not set'}
                      </span>
                      <ArrowRightIcon className="h-4 w-4 text-primary-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  </Link>
                )
              } else if (item.questionData) {
                // Language question
                const question = item.questionData
                const questionText = question.question || question.text || 'Language Question'
                const language = question.language || 'Unknown Language'
                const category = question.category || question.type || ''
                
                return (
                  <Link
                    key={item.id}
                    to="/language-trainer"
                    className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-700 hover:border-gold-300 dark:hover:border-gold-600 hover:shadow-md transition-all group bg-gradient-to-br from-white to-gold-50/30 dark:from-neutral-800 dark:to-gold-900/10"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-neutral-900 dark:text-white group-hover:text-primary-600 line-clamp-2">
                        {questionText}
                      </h3>
                      <StarSolidIcon className="h-4 w-4 text-gold-500 flex-shrink-0 ml-2" />
                    </div>
                    <p className="text-xs text-neutral-600 dark:text-neutral-400 mb-2">
                      {item.displayType} - {language}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-neutral-500">
                        {category}
                      </span>
                      <ArrowRightIcon className="h-4 w-4 text-primary-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  </Link>
                )
              } else {
                // Fallback for items without data - try to display stored item_data
                const displayName = item.item_data?.word || item.item_data?.name || item.item_data?.question || `Item ${item.item_id.slice(0, 8)}...`
                const displayDescription = item.item_data?.definition || item.item_data?.description || ''
                
                return (
                  <div
                    key={item.id}
                    className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-700 bg-gradient-to-br from-white to-gold-50/30 dark:from-neutral-800 dark:to-gold-900/10"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-neutral-900 dark:text-white">
                        {displayName}
                      </h3>
                      <StarSolidIcon className="h-4 w-4 text-gold-500 flex-shrink-0 ml-2" />
                    </div>
                    <p className="text-xs text-neutral-600 dark:text-neutral-400 mb-2">
                      {item.displayType}
                    </p>
                    {displayDescription && (
                      <p className="text-xs text-neutral-500 dark:text-neutral-400 line-clamp-2 mb-2">
                        {displayDescription}
                      </p>
                    )}
                    <div className="text-xs text-neutral-500">
                      Starred {new Date(item.created_at).toLocaleDateString()}
                    </div>
                  </div>
                )
              }
            })}
          </div>
          
          {starredItems.length > 6 && (
            <div className="mt-4 text-center">
              <Link 
                to="/starred-items" 
                className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium text-sm"
              >
                View all {starredItems.length} starred items
                <ArrowRightIcon className="h-4 w-4" />
              </Link>
            </div>
          )}
        </div>
      )}


      {/* Review Questions Section */}
      {reviewQuestions.length > 0 && (
        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <QuestionMarkCircleIcon className="h-5 w-5 text-blue-500" />
              <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">Review Questions</h2>
            </div>
            <span className="text-sm text-neutral-600 dark:text-neutral-400">
              Test your knowledge
            </span>
          </div>
          
          <div className="space-y-6">
            {reviewQuestions.slice(0, 3).map((q) => {
              const isAnswered = selectedAnswers[q.id] !== undefined
              const isCorrect = selectedAnswers[q.id] === q.correct_answer
              const showAnswer = showingAnswer === q.id
              
              return (
                <div key={q.id} className="border-l-4 border-blue-400 pl-4">
                  <div className="mb-2">
                    <span className="text-xs text-neutral-500 dark:text-neutral-400">
                      {q.category} • {q.node_name}
                    </span>
                  </div>
                  
                  <h3 className="font-medium text-neutral-900 dark:text-white mb-3">
                    {q.question}
                  </h3>
                  
                  {q.options && q.options.length > 0 && (
                    <div className="space-y-2 mb-3">
                      {q.options.map((option, idx) => {
                        const isSelected = selectedAnswers[q.id] === option
                        const isCorrectOption = option === q.correct_answer
                        
                        return (
                          <button
                            key={idx}
                            onClick={() => handleAnswerSelect(q.id, option)}
                            disabled={showAnswer}
                            className={`w-full text-left p-3 rounded-lg border transition-all ${
                              showAnswer
                                ? isCorrectOption
                                  ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                                  : isSelected
                                  ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                                  : 'border-neutral-200 dark:border-neutral-700'
                                : isSelected
                                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                                : 'border-neutral-200 dark:border-neutral-700 hover:border-blue-300 dark:hover:border-blue-600'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <span className="text-sm text-neutral-800 dark:text-neutral-200">
                                {option}
                              </span>
                              {showAnswer && (
                                <span>
                                  {isCorrectOption ? (
                                    <CheckCircleIcon className="h-5 w-5 text-green-600" />
                                  ) : isSelected ? (
                                    <XCircleIcon className="h-5 w-5 text-red-600" />
                                  ) : null}
                                </span>
                              )}
                            </div>
                          </button>
                        )
                      })}
                    </div>
                  )}
                  
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => checkAnswer(q.id)}
                      disabled={!isAnswered}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isAnswered
                          ? 'bg-blue-600 text-white hover:bg-blue-700'
                          : 'bg-neutral-200 text-neutral-400 cursor-not-allowed'
                      }`}
                    >
                      {showAnswer ? 'Hide Answer' : 'Check Answer'}
                    </button>
                    
                    {showAnswer && (
                      <span className={`text-sm font-medium ${
                        isCorrect ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {isCorrect ? '✓ Correct!' : '✗ Incorrect'}
                      </span>
                    )}
                  </div>
                  
                  {showAnswer && q.explanation && (
                    <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                      <p className="text-sm text-neutral-700 dark:text-neutral-300">
                        <strong>Explanation:</strong> {q.explanation}
                      </p>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
          
          {reviewQuestions.length > 3 && (
            <div className="mt-6 text-center">
              <Link 
                to="/practice" 
                className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                <QuestionMarkCircleIcon className="h-4 w-4" />
                Practice More Questions
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ProfilePage