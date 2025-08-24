import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import { studyListService } from '../services/studyListService'
import { UserProgress, StudyList } from '../types/database.types'
import { recommendationService, RecommendationScore } from '../services/recommendationService'
import { spacedRepetitionService } from '../services/spacedRepetitionService'
import { buildCategoryPath } from '../utils/categoryPaths'
import { nameToSlug } from '../utils/studyListSlug'
import InteractiveFlashcardReview from '../components/InteractiveFlashcardReview'
import { 
  TrophyIcon, 
  ClockIcon, 
  BookOpenIcon,
  ChartBarIcon,
  RocketLaunchIcon,
  HeartIcon,
  ArrowRightIcon,
  QuestionMarkCircleIcon,
  CheckCircleIcon,
  XCircleIcon,
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
  type: 'vocabulary' | 'spelling' | 'language' | 'question' | 'skill_node'
  // Question/Assessment format
  question?: string
  options?: string[]
  correct_answer?: string
  correct_answer_index?: number
  explanation?: string
  // Vocabulary/Spelling format  
  word?: string
  definition?: string
  part_of_speech?: string
  pronunciation?: string
  example_sentence?: string
  // Language format
  language?: string
  hint?: string
  // General
  difficulty?: string
  category?: string
  estimated_time_seconds?: number
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
  const [dueFlashcards, setDueFlashcards] = useState<Flashcard[]>([])
  const [useSpacedRepetition, setUseSpacedRepetition] = useState(true)
  const [loadedCardIds, setLoadedCardIds] = useState<Set<string>>(new Set())
  const [stats, setStats] = useState<DashboardStats>({
    completedLessons: 0,
    averageRating: 0,
    totalTimeSpent: 0,
    starredItemsCount: 0,
    studyListsCount: 0,
    inProgressCount: 0
  })
  const [loading, setLoading] = useState(true)

  const fetchFlashcards = async (append: boolean = false) => {
    try {
      if (!user) return
      
      // Fetch due flashcards using spaced repetition
      if (useSpacedRepetition) {
        const dueSessions = await spacedRepetitionService.getDueFlashcards(
          user.id,
          100 // Get more cards for continuous review
        )
        
        // Filter out already loaded cards if appending
        const filteredSessions = append 
          ? dueSessions.filter(s => !loadedCardIds.has(s.flashcard?.id || ''))
          : dueSessions
        
        const dueCards: Flashcard[] = filteredSessions.map(session => {
          const card = session.flashcard
          let flashcard: Flashcard
          
          if (session.review?.flashcard_type === 'vocabulary' || session.review?.flashcard_type === 'spelling') {
            flashcard = {
              id: card.id,
              type: session.review.flashcard_type,
              word: card.word,
              definition: card.definition,
              part_of_speech: card.part_of_speech,
              pronunciation: card.pronunciation,
              example_sentence: card.example_sentence,
              difficulty: card.difficulty,
              category: session.review.flashcard_type === 'vocabulary' ? 'Vocabulary' : 'Spelling'
            }
          } else if (session.review?.flashcard_type === 'question') {
            flashcard = {
              id: card.id,
              type: 'question',
              question: card.question || card.question_text,
              options: card.options,
              correct_answer: card.correct_answer,
              explanation: card.explanation,
              difficulty: card.difficulty,
              estimated_time_seconds: card.estimated_time_seconds,
              category: 'Review Question'
            }
          } else if (session.review?.flashcard_type === 'language') {
            flashcard = {
              id: card.id,
              type: 'language',
              question: card.question || card.prompt,
              options: card.options,
              correct_answer_index: card.correct_answer_index,
              explanation: card.explanation,
              language: card.language,
              category: card.category || 'Language',
              hint: card.hint
            }
          } else {
            flashcard = {
              id: card.id || `${session.review?.flashcard_id}`,
              type: session.review?.flashcard_type || 'question',
              question: card.name || card.question || 'Review Card',
              correct_answer: card.description || card.answer || 'No content',
              category: session.review?.flashcard_type || 'Review'
            }
          }
          
          return flashcard
        })
        
        // Update loaded card IDs
        const newCardIds = new Set(loadedCardIds)
        dueCards.forEach(card => newCardIds.add(card.id))
        setLoadedCardIds(newCardIds)
        
        if (append) {
          setDueFlashcards(prev => [...prev, ...dueCards])
          setFlashcards(prev => [...prev, ...dueCards])
        } else {
          setDueFlashcards(dueCards)
          setFlashcards(dueCards)
        }
        
        // If no due cards, fall back to regular flashcards
        if (dueCards.length === 0 && !append) {
          await fetchRegularFlashcards(append)
        }
      } else {
        await fetchRegularFlashcards(append)
      }
    } catch (error) {
      console.error('Error fetching flashcards:', error)
      // Fall back to regular flashcards on error
      await fetchRegularFlashcards()
    }
  }
  
  const fetchRegularFlashcards = async (append: boolean = false) => {
    try {
      if (!user) return
      
      const flashcardsList: Flashcard[] = []
      
      // Fetch vocabulary words
      const { data: vocabWords, error: vocabError } = await supabase
        .from('spelling_words')
        .select('*')
        .not('definition', 'is', null)
        .limit(20)
        .order('created_at', { ascending: false })
      
      if (!vocabError && vocabWords) {
        vocabWords.forEach(word => {
          flashcardsList.push({
            id: `vocab-${word.id}`,
            type: 'vocabulary',
            word: word.word,
            definition: word.definition || 'No definition available',
            part_of_speech: word.part_of_speech,
            pronunciation: word.pronunciation,
            example_sentence: word.example_sentence,
            difficulty: word.difficulty,
            category: 'Vocabulary'
          })
        })
      }
      
      // Fetch spelling words  
      const { data: spellingWords, error: spellingError } = await supabase
        .from('spelling_words')
        .select('*')
        .is('definition', null)
        .limit(15)
        .order('created_at', { ascending: false })
      
      if (!spellingError && spellingWords) {
        spellingWords.forEach(word => {
          flashcardsList.push({
            id: `spelling-${word.id}`,
            type: 'spelling',
            word: word.word,
            definition: word.definition,
            pronunciation: word.pronunciation,
            difficulty: word.difficulty,
            category: 'Spelling'
          })
        })
      }
      
      // Fetch questions from user's progress
      if (recentProgress.length > 0) {
        const nodeIds = recentProgress.slice(0, 5).map(p => p.skill_id)
        const { data: questions, error: questionsError } = await supabase
          .from('questions')
          .select('*')
          .in('skill_id', nodeIds)
          .limit(15)
        
        if (!questionsError && questions) {
          questions.forEach(q => {
            flashcardsList.push({
              id: `question-${q.id}`,
              type: 'question',
              question: q.question,
              options: q.options,
              correct_answer: q.correct_answer,
              explanation: q.explanation,
              difficulty: q.difficulty,
              estimated_time_seconds: q.estimated_time_seconds,
              category: 'Review Question'
            })
          })
        }
      }
      
      // Update loaded card IDs
      const newCardIds = new Set(loadedCardIds)
      flashcardsList.forEach(card => newCardIds.add(card.id))
      setLoadedCardIds(newCardIds)
      
      if (append) {
        setFlashcards(prev => [...prev, ...flashcardsList])
      } else {
        setFlashcards(flashcardsList)
      }
    } catch (error) {
      console.error('Error fetching regular flashcards:', error)
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
    // Scroll to top when component mounts
    window.scrollTo(0, 0)
    
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

      // Fetch starred items - only skill_node types since flashcards are in study lists
      const starred = await studyListService.getStarredItems(user.id)
      
      // Filter to only show skill nodes (not flashcard types which are in study lists)
      const filteredStarred = starred.filter(item => 
        item.item_type === 'skill_node'
      )
      
      // Fetch details for skill node starred items
      const starredWithDetails = await Promise.all(
        filteredStarred.map(async (item) => {
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
          const fullPath = path ? `/${path}` : `/learning/${nodeId}`
          
          // Check for duplicate segments in the path
          const segments = fullPath.split('/').filter(s => s.length > 0)
          const uniqueSegments = Array.from(new Set(segments))
          if (segments.length !== uniqueSegments.length) {
            console.warn(`Duplicate segments detected in path for ${nodeId}: ${fullPath}`)
            // Use deduplicated path
            paths[nodeId] = '/' + uniqueSegments.join('/')
          } else {
            paths[nodeId] = fullPath
          }
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
  
  const loadMoreFlashcards = () => {
    fetchFlashcards(true) // Append more cards
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
      <div className="grid md:grid-cols-3 lg:grid-cols-5 gap-4">
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
                      Learning Module
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
        {/* Smart Review - moved to left with more space */}
        <div className="lg:col-span-2">
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 border border-neutral-200 dark:border-neutral-700">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">Smart Review</h3>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    setUseSpacedRepetition(!useSpacedRepetition)
                    fetchFlashcards()
                  }}
                  className={`text-xs px-2 py-1 rounded ${useSpacedRepetition ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400' : 'bg-neutral-100 text-neutral-600 dark:bg-neutral-700 dark:text-neutral-400'}`}
                >
                  {useSpacedRepetition ? 'Spaced' : 'Random'}
                </button>
                <span className="text-xs text-neutral-500">
                  {flashcards.length > 0 ? `${flashcards.length} cards` : '0 cards'}
                </span>
                <Link 
                  to="/review" 
                  className="text-primary-600 hover:text-primary-700 text-xs font-medium"
                >
                  Full Review
                </Link>
              </div>
            </div>
            
            {flashcards.length === 0 ? (
              <div className="text-center py-8">
                <BookOpenIcon className="h-8 w-8 text-neutral-400 mx-auto mb-2" />
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  {useSpacedRepetition ? 'No cards due for review' : 'No flashcards available yet'}
                </p>
                <p className="text-xs text-neutral-500 mt-1">
                  {useSpacedRepetition ? 'Great job! All caught up!' : 'Start learning to see review cards here'}
                </p>
                <Link
                  to="/review"
                  className="inline-flex items-center gap-2 mt-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm"
                >
                  <ArrowRightIcon className="h-4 w-4" />
                  Go to Full Review
                </Link>
              </div>
            ) : useSpacedRepetition && dueFlashcards.length > 0 ? (
              <InteractiveFlashcardReview
                flashcards={dueFlashcards}
                onComplete={() => {
                  fetchFlashcards() // Refresh after completion
                }}
                onLoadMore={loadMoreFlashcards}
                className="-m-4"
                disableAutoFocus={true}
              />
            ) : (
              <InteractiveFlashcardReview
                flashcards={flashcards}
                onComplete={() => {
                  fetchFlashcards() // Refresh after completion
                }}
                onLoadMore={loadMoreFlashcards}
                className="-m-4"
                disableAutoFocus={true}
              />
            )}
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Recent Activity - moved to right side */}
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 border border-neutral-200 dark:border-neutral-700">
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
              <div className="space-y-3 max-h-96 overflow-y-auto">
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
                  <Link
                    key={list.id}
                    to={`/study-lists/${nameToSlug(list.name)}`}
                    className="flex items-center gap-2 p-2 rounded-lg hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors cursor-pointer"
                  >
                    <div 
                      className="w-3 h-3 rounded-full flex-shrink-0"
                      style={{ backgroundColor: list.color }}
                    ></div>
                    <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300 truncate">
                      {list.name}
                    </span>
                  </Link>
                ))}
                {studyLists.length > 3 && (
                  <p className="text-xs text-neutral-500 mt-2">
                    +{studyLists.length - 3} more lists
                  </p>
                )}
              </div>
            )}
          </div>

        </div>
      </div>

      {/* Starred Learning Modules */}
      {starredItems.length > 0 && (
        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <StarSolidIcon className="h-5 w-5 text-gold-500" />
              <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">Your Starred Learning Modules</h2>
            </div>
            <span className="text-sm text-neutral-600 dark:text-neutral-400">
              {starredItems.length} item{starredItems.length !== 1 ? 's' : ''}
            </span>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {starredItems.slice(0, 6).map(item => {
              // All items are skill tree nodes now
              const node = item.nodeData
              if (!node) return null
              
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
                  {node.description && (
                    <p className="text-sm text-neutral-600 dark:text-neutral-400 line-clamp-3 mb-2">
                      {node.description}
                    </p>
                  )}
                  <div className="flex items-center justify-between mt-auto">
                    {node.has_learning_content && (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-full text-xs">
                        <BookOpenIcon className="h-3 w-3" />
                        Content
                      </span>
                    )}
                    <ArrowRightIcon className="h-4 w-4 text-primary-500 opacity-0 group-hover:opacity-100 transition-opacity ml-auto" />
                  </div>
                </Link>
              )
            })}
          </div>
          
          {starredItems.length > 6 && (
            <div className="mt-4 text-center">
              <Link 
                to="/starred-items" 
                className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium text-sm"
              >
                View all {starredItems.length} starred modules
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