import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { DeckProgressionService, DeckStats } from '../services/deckProgressionService'
import LanguageVocabularyCard from './flashcards/LanguageVocabularyCard'
import {
  AcademicCapIcon,
  ChartBarIcon,
  BookOpenIcon,
  StarIcon,
  SparklesIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

interface VocabularyWord {
  id: string
  language: string
  word: string
  zipf_frequency: number
  difficulty_id: number
  difficulty_name?: string
  english_translation: string
  pronunciation_guide: string
  part_of_speech: string
  definition_english: string
  example_sentence?: string
  example_sentence_translation?: string
  memory_tips?: string
}

interface DeckVocabularyItem {
  id: string
  deck_status: 'learning' | 'review' | 'mastered'
  consecutive_correct: number
  total_reviews: number
  last_reviewed_at: string | null
  next_review_date: string
  vocabulary: VocabularyWord
}

interface VocabularyStudyList {
  id: string
  name: string
  description: string
  language: string
  difficulty_id: number | null
  min_zipf: number | null
  max_zipf: number | null
}

interface LanguageVocabularyModeProps {
  selectedLanguage: string
  onBack?: () => void
}

const LanguageVocabularyMode: React.FC<LanguageVocabularyModeProps> = ({
  selectedLanguage,
  onBack
}) => {
  const { user } = useAuth()
  const [, setVocabulary] = useState<VocabularyWord[]>([])
  const [deckItems, setDeckItems] = useState<DeckVocabularyItem[]>([])
  const [filteredVocabulary, setFilteredVocabulary] = useState<VocabularyWord[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deckStats, setDeckStats] = useState<DeckStats | null>(null)
  const [statusMessage, setStatusMessage] = useState<string>('')
  
  // Filter states
  const [selectedDifficulty, setSelectedDifficulty] = useState<number | null>(null)
  const [selectedStudyList, setSelectedStudyList] = useState<string | null>(null)
  const [studyLists, setStudyLists] = useState<VocabularyStudyList[]>([])
  const [deckFilter, setDeckFilter] = useState<'all' | 'learning' | 'review' | 'mastered' | 'due'>('due')
  
  // Stats
  const [sessionStats, setSessionStats] = useState({ 
    reviewed: 0, 
    easy: 0, 
    medium: 0, 
    hard: 0 
  })

  // Load deck statistics
  const loadDeckStats = useCallback(async () => {
    if (!user) return
    
    try {
      const stats = await DeckProgressionService.getDeckStats(user.id, selectedLanguage)
      setDeckStats(stats)
    } catch (error) {
      console.error('Error loading deck stats:', error)
    }
  }, [user, selectedLanguage])

  // Load study lists
  const loadStudyLists = useCallback(async () => {
    try {
      const { data, error } = await supabase
        .from('language_vocabulary_study_lists')
        .select('*')
        .eq('language', selectedLanguage)
        .order('difficulty_id')

      if (error) throw error
      setStudyLists(data || [])
      
      // Auto-select first study list
      if (data && data.length > 0 && !selectedStudyList) {
        setSelectedStudyList(data[0].id)
      }
    } catch (err) {
      console.error('Error loading study lists:', err)
    }
  }, [selectedLanguage, selectedStudyList])

  // Load vocabulary based on deck filter
  const loadVocabulary = useCallback(async () => {
    if (!user) {
      setError('Please sign in to use vocabulary cards')
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)
    
    try {
      if (deckFilter === 'all') {
        // Load all vocabulary (not in deck)
        let query = supabase
          .from('language_vocabulary_with_difficulty')
          .select('*')
          .eq('language', selectedLanguage)

        // Apply study list filter
        if (selectedStudyList) {
          const studyList = studyLists.find(s => s.id === selectedStudyList)
          if (studyList) {
            if (studyList.difficulty_id) {
              query = query.eq('difficulty_id', studyList.difficulty_id)
            }
            if (studyList.min_zipf !== null) {
              query = query.gte('zipf_frequency', studyList.min_zipf)
            }
            if (studyList.max_zipf !== null) {
              query = query.lte('zipf_frequency', studyList.max_zipf)
            }
          }
        }

        // Apply difficulty filter
        if (selectedDifficulty) {
          query = query.eq('difficulty_id', selectedDifficulty)
        }

        const { data, error } = await query
          .order('zipf_frequency', { ascending: false })
          .limit(100)

        if (error) throw error
        setVocabulary(data || [])
        setFilteredVocabulary(data || [])
      } else {
        // Load from deck
        const deckStatus = deckFilter === 'due' ? undefined : deckFilter
        const items = await DeckProgressionService.getVocabularyDeck(
          user.id,
          selectedLanguage,
          deckStatus || 'all'
        ) as DeckVocabularyItem[]

        setDeckItems(items)
        
        // Filter to only due items if needed
        let filteredItems = items
        if (deckFilter === 'due') {
          const today = new Date().toISOString().split('T')[0]
          filteredItems = items.filter(item => item.next_review_date <= today)
        }

        const vocabWords = filteredItems
          .map(item => item.vocabulary)
          .filter(Boolean)
        
        setFilteredVocabulary(vocabWords)
      }

      setCurrentIndex(0)
    } catch (err) {
      console.error('Error loading vocabulary:', err)
      setError('Failed to load vocabulary')
    } finally {
      setLoading(false)
    }
  }, [user, selectedLanguage, deckFilter, selectedDifficulty, selectedStudyList, studyLists])

  // Initialize
  useEffect(() => {
    loadStudyLists()
    loadDeckStats()
  }, [loadStudyLists, loadDeckStats])

  useEffect(() => {
    loadVocabulary()
  }, [loadVocabulary])

  const handleNext = () => {
    if (currentIndex < filteredVocabulary.length - 1) {
      setCurrentIndex(currentIndex + 1)
    } else {
      // Shuffle and restart
      const shuffled = [...filteredVocabulary].sort(() => Math.random() - 0.5)
      setFilteredVocabulary(shuffled)
      setCurrentIndex(0)
    }
  }

  const handleDifficulty = (difficulty: 'easy' | 'medium' | 'hard') => {
    setSessionStats(prev => ({
      reviewed: prev.reviewed + 1,
      easy: prev.easy + (difficulty === 'easy' ? 1 : 0),
      medium: prev.medium + (difficulty === 'medium' ? 1 : 0),
      hard: prev.hard + (difficulty === 'hard' ? 1 : 0)
    }))
    
    // Reload stats after review
    loadDeckStats()
  }

  const handleStatusChange = (newStatus: string, message: string) => {
    setStatusMessage(message)
    setTimeout(() => setStatusMessage(''), 3000)
    loadDeckStats() // Refresh stats when deck changes
  }

  const handleStudyListChange = (studyListId: string) => {
    setSelectedStudyList(studyListId)
    setSelectedDifficulty(null) // Clear difficulty filter when study list changes
  }

  const currentWord = filteredVocabulary[currentIndex]
  const currentDeckItem = deckItems[currentIndex]

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error || !currentWord) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6 text-center">
          <BookOpenIcon className="h-12 w-12 text-yellow-600 dark:text-yellow-400 mx-auto mb-3" />
          <p className="text-lg text-yellow-700 dark:text-yellow-400 mb-4">
            {error || 'No vocabulary available'}
          </p>
          <button
            onClick={onBack}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Back to Language Trainer
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Deck Filter Tabs */}
      <div className="mb-6">
        <div className="flex flex-wrap gap-2 justify-center mb-4">
          <button
            onClick={() => setDeckFilter('due')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              deckFilter === 'due' 
                ? 'bg-primary-600 text-white' 
                : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700'
            }`}
          >
            <ClockIcon className="h-5 w-5" />
            Due Today {deckStats && deckStats.dueToday > 0 && `(${deckStats.dueToday})`}
          </button>
          <button
            onClick={() => setDeckFilter('learning')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              deckFilter === 'learning' 
                ? 'bg-blue-600 text-white' 
                : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700'
            }`}
          >
            <AcademicCapIcon className="h-5 w-5" />
            Learning {deckStats && `(${deckStats.learning})`}
          </button>
          <button
            onClick={() => setDeckFilter('review')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              deckFilter === 'review' 
                ? 'bg-purple-600 text-white' 
                : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700'
            }`}
          >
            <StarIcon className="h-5 w-5" />
            Review {deckStats && `(${deckStats.review})`}
          </button>
          <button
            onClick={() => setDeckFilter('mastered')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              deckFilter === 'mastered' 
                ? 'bg-gold-600 text-white' 
                : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700'
            }`}
          >
            <SparklesIcon className="h-5 w-5" />
            Mastered {deckStats && `(${deckStats.mastered})`}
          </button>
          <button
            onClick={() => setDeckFilter('all')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              deckFilter === 'all' 
                ? 'bg-neutral-600 text-white' 
                : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700'
            }`}
          >
            <BookOpenIcon className="h-5 w-5" />
            Browse All
          </button>
        </div>

        {/* Study List and Difficulty filters (only for Browse All mode) */}
        {deckFilter === 'all' && (
          <div className="flex flex-wrap gap-3 justify-center">
            {/* Study Lists */}
            {studyLists.length > 0 && (
              <select
                value={selectedStudyList || ''}
                onChange={(e) => handleStudyListChange(e.target.value)}
                className="px-4 py-2 rounded-lg border border-neutral-300 dark:border-neutral-600 bg-white dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300"
              >
                {studyLists.map(list => (
                  <option key={list.id} value={list.id}>
                    {list.name}
                  </option>
                ))}
              </select>
            )}

            {/* Difficulty Filter */}
            <select
              value={selectedDifficulty || ''}
              onChange={(e) => setSelectedDifficulty(e.target.value ? parseInt(e.target.value) : null)}
              className="px-4 py-2 rounded-lg border border-neutral-300 dark:border-neutral-600 bg-white dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300"
            >
              <option value="">All Difficulties</option>
              <option value="1">Basic</option>
              <option value="2">Elementary</option>
              <option value="3">Intermediate</option>
              <option value="4">Advanced</option>
              <option value="5">Expert</option>
            </select>
          </div>
        )}
      </div>

      {/* Status Message */}
      {statusMessage && (
        <div className="mb-4 p-3 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-lg text-center animate-fade-in">
          {statusMessage}
        </div>
      )}

      {/* Progress indicator */}
      <div className="mb-4 flex items-center justify-between text-sm text-neutral-600 dark:text-neutral-400">
        <span>Card {currentIndex + 1} of {filteredVocabulary.length}</span>
        {sessionStats.reviewed > 0 && (
          <span>Reviewed: {sessionStats.reviewed} | Easy: {sessionStats.easy} | Medium: {sessionStats.medium} | Hard: {sessionStats.hard}</span>
        )}
      </div>

      {/* Vocabulary Card */}
      <LanguageVocabularyCard
        word={currentWord}
        onNext={handleNext}
        onDifficulty={handleDifficulty}
        isReviewMode={deckFilter !== 'all'}
        deckStatus={currentDeckItem?.deck_status}
        onStatusChange={handleStatusChange}
      />

      {/* Session Stats */}
      {sessionStats.reviewed > 0 && (
        <div className="mt-6 p-4 bg-neutral-100 dark:bg-neutral-800 rounded-lg">
          <h3 className="text-sm font-semibold mb-2 text-neutral-700 dark:text-neutral-300">
            Session Statistics
          </h3>
          <div className="grid grid-cols-4 gap-2 text-center">
            <div>
              <ChartBarIcon className="h-5 w-5 mx-auto mb-1 text-neutral-600 dark:text-neutral-400" />
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Total</p>
              <p className="text-lg font-bold text-neutral-800 dark:text-neutral-200">
                {sessionStats.reviewed}
              </p>
            </div>
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Easy</p>
              <p className="text-lg font-bold text-green-600 dark:text-green-400">
                {sessionStats.easy}
              </p>
              <p className="text-xs text-neutral-500">
                {sessionStats.reviewed > 0 ? Math.round((sessionStats.easy / sessionStats.reviewed) * 100) : 0}%
              </p>
            </div>
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Medium</p>
              <p className="text-lg font-bold text-yellow-600 dark:text-yellow-400">
                {sessionStats.medium}
              </p>
              <p className="text-xs text-neutral-500">
                {sessionStats.reviewed > 0 ? Math.round((sessionStats.medium / sessionStats.reviewed) * 100) : 0}%
              </p>
            </div>
            <div>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Hard</p>
              <p className="text-lg font-bold text-red-600 dark:text-red-400">
                {sessionStats.hard}
              </p>
              <p className="text-xs text-neutral-500">
                {sessionStats.reviewed > 0 ? Math.round((sessionStats.hard / sessionStats.reviewed) * 100) : 0}%
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Back button */}
      <div className="mt-6 text-center">
        <button
          onClick={onBack}
          className="px-4 py-2 text-neutral-600 dark:text-neutral-400 hover:text-neutral-800 dark:hover:text-neutral-200 transition-colors"
        >
          ← Back to Language Trainer
        </button>
      </div>
    </div>
  )
}

export default LanguageVocabularyMode