import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { spacedRepetitionService } from '../services/spacedRepetitionService'
import { supabase } from '../services/supabase'
import InteractiveFlashcardReview from '../components/InteractiveFlashcardReview'
import { Link } from 'react-router-dom'
import {
  ArrowLeftIcon,
  AcademicCapIcon,
  ClockIcon,
  StarIcon,
  ChartBarIcon,
  CogIcon,
  ArrowPathIcon,
  BookOpenIcon
} from '@heroicons/react/24/outline'

interface Flashcard {
  id: string
  type: 'vocabulary' | 'spelling' | 'language' | 'question' | 'skill_node'
  // Question/Assessment format
  question?: string
  options?: string[]
  correct_answer?: string
  correct_answer_index?: number
  explanation?: string
  // Vocabulary format
  word?: string
  definition?: string
  part_of_speech?: string
  pronunciation?: string
  example_sentence?: string
  // Language format
  language?: string
  category?: string
  hint?: string
  // General
  difficulty?: string
  estimated_time_seconds?: number
}

interface ReviewStats {
  dueToday: number
  newCards: number
  learningCards: number
  matureCards: number
  totalCards: number
  averageEasiness: number
  averageSuccessRate: number
}

const ReviewFlashcardsPage: React.FC = () => {
  const { user } = useAuth()
  const [flashcards, setFlashcards] = useState<Flashcard[]>([])
  const [stats, setStats] = useState<ReviewStats>({
    dueToday: 0,
    newCards: 0,
    learningCards: 0,
    matureCards: 0,
    totalCards: 0,
    averageEasiness: 0,
    averageSuccessRate: 0
  })
  const [loading, setLoading] = useState(true)
  const [settings, setSettings] = useState({
    cardTypes: ['vocabulary', 'spelling', 'question'],
    maxCards: 50,
    prioritizeDue: true
  })
  const [showSettings, setShowSettings] = useState(false)
  const [loadedCardIds, setLoadedCardIds] = useState<Set<string>>(new Set())

  useEffect(() => {
    if (user) {
      fetchStats()
      fetchFlashcards()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, settings])

  const fetchStats = async () => {
    if (!user) return
    
    try {
      const userStats = await spacedRepetitionService.getUserStatistics(user.id)
      if (userStats) {
        setStats({
          dueToday: userStats.dueToday || 0,
          newCards: userStats.newCards || 0,
          learningCards: userStats.learningCards || 0,
          matureCards: userStats.matureCards || 0,
          totalCards: userStats.totalCards || 0,
          averageEasiness: userStats.averageEasiness || 2.5,
          averageSuccessRate: userStats.averageSuccessRate || 0
        })
      }
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const fetchFlashcards = async (append: boolean = false) => {
    if (!user) return
    
    try {
      setLoading(true)
      
      // Fetch due flashcards using spaced repetition
      const dueSessions = await spacedRepetitionService.getDueFlashcards(
        user.id,
        settings.maxCards,
        settings.cardTypes
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
            category: card.category,
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
        setFlashcards(prev => [...prev, ...dueCards])
      } else {
        setFlashcards(dueCards)
      }
      
      // If no due cards, fetch some random cards
      if (dueCards.length === 0 && !append) {
        await fetchRandomFlashcards()
      }
      
    } catch (error) {
      console.error('Error fetching flashcards:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchRandomFlashcards = async () => {
    if (!user) return
    
    try {
      const flashcardsList: Flashcard[] = []
      
      // Fetch vocabulary words
      if (settings.cardTypes.includes('vocabulary')) {
        const { data: vocabWords } = await supabase
          .from('spelling_words')
          .select('*')
          .not('definition', 'is', null)
          .limit(20)
          .order('created_at', { ascending: false })
        
        if (vocabWords) {
          vocabWords.forEach(word => {
            if (!loadedCardIds.has(`vocab-${word.id}`)) {
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
            }
          })
        }
      }
      
      // Fetch spelling words
      if (settings.cardTypes.includes('spelling')) {
        const { data: spellingWords } = await supabase
          .from('spelling_words')
          .select('*')
          .is('definition', null)
          .limit(20)
          .order('created_at', { ascending: false })
        
        if (spellingWords) {
          spellingWords.forEach(word => {
            if (!loadedCardIds.has(`spelling-${word.id}`)) {
              flashcardsList.push({
                id: `spelling-${word.id}`,
                type: 'spelling',
                word: word.word,
                definition: word.definition,
                pronunciation: word.pronunciation,
                difficulty: word.difficulty,
                category: 'Spelling'
              })
            }
          })
        }
      }
      
      // Fetch language questions
      if (settings.cardTypes.includes('language')) {
        const { data: languageQuestions } = await supabase
          .from('language_questions')
          .select('*')
          .limit(20)
          .order('created_at', { ascending: false })
        
        if (languageQuestions) {
          languageQuestions.forEach(q => {
            if (!loadedCardIds.has(`language-${q.id}`)) {
              flashcardsList.push({
                id: `language-${q.id}`,
                type: 'language',
                question: q.question || 'Language Question',
                options: q.options,
                correct_answer_index: q.correct_answer_index,
                explanation: q.explanation,
                language: q.language,
                category: q.category || 'Language',
                hint: q.hint
              })
            }
          })
        }
      }
      
      // Update loaded card IDs
      const newCardIds = new Set(loadedCardIds)
      flashcardsList.forEach(card => newCardIds.add(card.id))
      setLoadedCardIds(newCardIds)
      
      setFlashcards(flashcardsList)
    } catch (error) {
      console.error('Error fetching random flashcards:', error)
    }
  }

  const loadMoreFlashcards = () => {
    fetchFlashcards(true)
  }

  const handleReset = () => {
    setLoadedCardIds(new Set())
    fetchFlashcards()
  }

  const toggleCardType = (type: string) => {
    setSettings(prev => ({
      ...prev,
      cardTypes: prev.cardTypes.includes(type)
        ? prev.cardTypes.filter(t => t !== type)
        : [...prev.cardTypes, type]
    }))
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              to="/profile"
              className="p-2 rounded-lg bg-neutral-100 hover:bg-neutral-200 dark:bg-neutral-800 dark:hover:bg-neutral-700 transition-colors"
            >
              <ArrowLeftIcon className="h-5 w-5 text-neutral-600 dark:text-neutral-300" />
            </Link>
            <div>
              <h1 className="text-3xl font-bold text-neutral-900 dark:text-white">
                Review Flashcards
              </h1>
              <p className="text-neutral-600 dark:text-neutral-400 mt-1">
                Practice with spaced repetition for optimal memory retention
              </p>
            </div>
          </div>
          
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-3 rounded-lg bg-neutral-100 hover:bg-neutral-200 dark:bg-neutral-800 dark:hover:bg-neutral-700 transition-colors"
          >
            <CogIcon className="h-5 w-5 text-neutral-600 dark:text-neutral-300" />
          </button>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="mb-6 p-4 bg-white dark:bg-neutral-800 rounded-xl shadow-lg border border-neutral-200 dark:border-neutral-700">
          <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">
            Review Settings
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2 block">
                Card Types
              </label>
              <div className="flex flex-wrap gap-2">
                {['vocabulary', 'spelling', 'question', 'language', 'skill_node'].map(type => (
                  <button
                    key={type}
                    onClick={() => toggleCardType(type)}
                    className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                      settings.cardTypes.includes(type)
                        ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400'
                        : 'bg-neutral-100 text-neutral-600 dark:bg-neutral-700 dark:text-neutral-400'
                    }`}
                  >
                    {type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>
            
            <div>
              <label className="text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2 block">
                Max Cards per Session: {settings.maxCards}
              </label>
              <input
                type="range"
                min="10"
                max="100"
                step="10"
                value={settings.maxCards}
                onChange={(e) => setSettings(prev => ({ ...prev, maxCards: parseInt(e.target.value) }))}
                className="w-full"
              />
            </div>
            
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="prioritizeDue"
                checked={settings.prioritizeDue}
                onChange={(e) => setSettings(prev => ({ ...prev, prioritizeDue: e.target.checked }))}
                className="rounded border-neutral-300 text-primary-600 focus:ring-primary-500"
              />
              <label htmlFor="prioritizeDue" className="text-sm text-neutral-700 dark:text-neutral-300">
                Prioritize due cards (spaced repetition)
              </label>
            </div>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-6">
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-3 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center gap-2">
            <ClockIcon className="h-5 w-5 text-blue-500" />
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Due Today</p>
              <p className="text-xl font-bold text-neutral-900 dark:text-white">{stats.dueToday}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-3 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center gap-2">
            <StarIcon className="h-5 w-5 text-green-500" />
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">New</p>
              <p className="text-xl font-bold text-neutral-900 dark:text-white">{stats.newCards}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-3 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center gap-2">
            <AcademicCapIcon className="h-5 w-5 text-yellow-500" />
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Learning</p>
              <p className="text-xl font-bold text-neutral-900 dark:text-white">{stats.learningCards}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-3 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center gap-2">
            <ChartBarIcon className="h-5 w-5 text-purple-500" />
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Mature</p>
              <p className="text-xl font-bold text-neutral-900 dark:text-white">{stats.matureCards}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-3 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center gap-2">
            <BookOpenIcon className="h-5 w-5 text-primary-500" />
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Total</p>
              <p className="text-xl font-bold text-neutral-900 dark:text-white">{stats.totalCards}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-3 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center gap-2">
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Success Rate</p>
              <p className="text-xl font-bold text-neutral-900 dark:text-white">
                {Math.round(stats.averageSuccessRate)}%
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-3 border border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center gap-2">
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Avg Easiness</p>
              <p className="text-xl font-bold text-neutral-900 dark:text-white">
                {stats.averageEasiness.toFixed(1)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg border border-neutral-200 dark:border-neutral-700">
        {flashcards.length === 0 ? (
          <div className="p-12 text-center">
            <BookOpenIcon className="h-16 w-16 text-neutral-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-neutral-900 dark:text-white mb-2">
              No flashcards available
            </h2>
            <p className="text-neutral-600 dark:text-neutral-400 mb-6">
              {stats.dueToday > 0 
                ? "Loading your due cards..." 
                : "Great job! You're all caught up. Check back later for more reviews."}
            </p>
            <button
              onClick={handleReset}
              className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <ArrowPathIcon className="h-4 w-4" />
              Load New Cards
            </button>
          </div>
        ) : (
          <div className="p-6">
            <InteractiveFlashcardReview
              flashcards={flashcards}
              onComplete={() => {
                setLoadedCardIds(new Set())
                fetchFlashcards()
              }}
              onLoadMore={loadMoreFlashcards}
            />
          </div>
        )}
      </div>
      
      {/* Footer Actions */}
      <div className="mt-6 flex items-center justify-between">
        <div className="text-sm text-neutral-600 dark:text-neutral-400">
          {flashcards.length > 0 && (
            <span>
              {flashcards.length} cards loaded • {loadedCardIds.size} unique cards seen
            </span>
          )}
        </div>
        
        <div className="flex items-center gap-3">
          <button
            onClick={handleReset}
            className="inline-flex items-center gap-2 px-4 py-2 bg-neutral-200 text-neutral-700 rounded-lg hover:bg-neutral-300 dark:bg-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-600 transition-colors"
          >
            <ArrowPathIcon className="h-4 w-4" />
            Reset Session
          </button>
        </div>
      </div>
    </div>
  )
}

export default ReviewFlashcardsPage