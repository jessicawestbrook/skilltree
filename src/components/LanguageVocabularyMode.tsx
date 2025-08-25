import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import LanguageVocabularyCard from './flashcards/LanguageVocabularyCard'
import {
  AcademicCapIcon,
  ChartBarIcon,
  ArrowPathIcon,
  BookOpenIcon
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
  const [filteredVocabulary, setFilteredVocabulary] = useState<VocabularyWord[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Filter states
  const [selectedDifficulty, setSelectedDifficulty] = useState<number | null>(null)
  const [selectedStudyList, setSelectedStudyList] = useState<string | null>(null)
  const [studyLists, setStudyLists] = useState<VocabularyStudyList[]>([])
  const [isReviewMode, setIsReviewMode] = useState(false)
  
  // Stats
  const [sessionStats, setSessionStats] = useState({ 
    reviewed: 0, 
    easy: 0, 
    medium: 0, 
    hard: 0 
  })

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

  // Load vocabulary
  const loadVocabulary = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      // Build query
      let query = supabase
        .from('language_vocabulary_with_difficulty')
        .select('*')
        .eq('language', selectedLanguage)
        .order('zipf_frequency', { ascending: false })

      // Apply filters
      if (selectedDifficulty) {
        query = query.eq('difficulty_id', selectedDifficulty)
      }
      
      if (selectedStudyList) {
        const studyList = studyLists.find(sl => sl.id === selectedStudyList)
        if (studyList) {
          if (studyList.difficulty_id) {
            query = query.eq('difficulty_id', studyList.difficulty_id)
          }
          if (studyList.min_zipf !== null) {
            query = query.gte('zipf_frequency', studyList.min_zipf)
          }
          if (studyList.max_zipf !== null) {
            query = query.lt('zipf_frequency', studyList.max_zipf)
          }
        }
      }

      const { data, error } = await query

      if (error) throw error
      
      if (!data || data.length === 0) {
        setError('No vocabulary available for the selected filters')
        setVocabulary([])
        setFilteredVocabulary([])
      } else {
        // Shuffle for variety
        const shuffled = [...data].sort(() => Math.random() - 0.5)
        setVocabulary(data)
        setFilteredVocabulary(shuffled)
        setCurrentIndex(0)
      }
    } catch (err) {
      console.error('Error loading vocabulary:', err)
      setError('Failed to load vocabulary')
    } finally {
      setLoading(false)
    }
  }, [selectedLanguage, selectedDifficulty, selectedStudyList, studyLists])

  // Load due reviews if in review mode
  const loadDueReviews = useCallback(async () => {
    if (!user || !isReviewMode) return
    
    setLoading(true)
    try {
      // Get vocabulary items that are due for review
      const { data: progressData, error: progressError } = await supabase
        .from('language_vocabulary_progress')
        .select('vocabulary_id, next_review')
        .eq('user_id', user.id)
        .lte('next_review', new Date().toISOString())

      if (progressError) throw progressError

      if (progressData && progressData.length > 0) {
        const vocabularyIds = progressData.map(p => p.vocabulary_id)
        
        const { data: vocabData, error: vocabError } = await supabase
          .from('language_vocabulary_with_difficulty')
          .select('*')
          .in('id', vocabularyIds)
          .eq('language', selectedLanguage)

        if (vocabError) throw vocabError
        
        if (vocabData && vocabData.length > 0) {
          setFilteredVocabulary(vocabData)
          setCurrentIndex(0)
        } else {
          setError('No vocabulary items due for review')
        }
      } else {
        setError('No vocabulary items due for review. Great job!')
      }
    } catch (err) {
      console.error('Error loading due reviews:', err)
      setError('Failed to load review items')
    } finally {
      setLoading(false)
    }
  }, [user, isReviewMode, selectedLanguage])

  // Initialize
  useEffect(() => {
    loadStudyLists()
  }, [loadStudyLists])

  useEffect(() => {
    if (isReviewMode) {
      loadDueReviews()
    } else {
      loadVocabulary()
    }
  }, [isReviewMode, loadVocabulary, loadDueReviews])

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
  }

  const handleStudyListChange = (studyListId: string) => {
    setSelectedStudyList(studyListId)
    setSelectedDifficulty(null) // Clear difficulty filter when study list changes
  }

  const currentWord = filteredVocabulary[currentIndex]

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
            Back to Questions
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-4">
      {/* Header and Controls */}
      <div className="bg-white dark:bg-neutral-900 rounded-lg shadow-lg p-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-neutral-800 dark:text-neutral-200 flex items-center gap-2">
            <AcademicCapIcon className="h-6 w-6 text-primary-600" />
            Vocabulary Flashcards
          </h2>
          
          {onBack && (
            <button
              onClick={onBack}
              className="text-sm text-neutral-600 dark:text-neutral-400 hover:text-primary-600 dark:hover:text-primary-400"
            >
              ← Back to Questions
            </button>
          )}
        </div>
        
        {/* Filters */}
        <div className="flex flex-wrap gap-3 mb-4">
          {/* Study List Filter */}
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Study List
            </label>
            <select
              value={selectedStudyList || ''}
              onChange={(e) => handleStudyListChange(e.target.value)}
              className="w-full px-3 py-2 bg-white dark:bg-neutral-800 border border-neutral-300 dark:border-neutral-600 rounded-lg text-sm"
            >
              <option value="">All Vocabulary</option>
              {studyLists.map(list => (
                <option key={list.id} value={list.id}>
                  {list.name}
                </option>
              ))}
            </select>
          </div>
          
          {/* Difficulty Filter */}
          <div className="flex-1 min-w-[150px]">
            <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Difficulty
            </label>
            <select
              value={selectedDifficulty || ''}
              onChange={(e) => setSelectedDifficulty(e.target.value ? parseInt(e.target.value) : null)}
              className="w-full px-3 py-2 bg-white dark:bg-neutral-800 border border-neutral-300 dark:border-neutral-600 rounded-lg text-sm"
              disabled={!!selectedStudyList} // Disable if study list is selected
            >
              <option value="">All Levels</option>
              <option value="1">Basic</option>
              <option value="2">Elementary</option>
              <option value="3">Intermediate</option>
              <option value="4">Advanced</option>
              <option value="5">Expert</option>
            </select>
          </div>
          
          {/* Review Mode Toggle */}
          {user && (
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsReviewMode(!isReviewMode)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isReviewMode 
                    ? 'bg-primary-600 text-white' 
                    : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300'
                }`}
              >
                <ArrowPathIcon className="h-4 w-4 inline mr-1" />
                Review Mode
              </button>
            </div>
          )}
        </div>
        
        {/* Stats */}
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-4">
            <span className="text-neutral-600 dark:text-neutral-400">
              Word {currentIndex + 1} of {filteredVocabulary.length}
            </span>
            <span className="text-neutral-600 dark:text-neutral-400">
              Language: {selectedLanguage === 'es' ? 'Spanish' : selectedLanguage.toUpperCase()}
            </span>
          </div>
          
          {sessionStats.reviewed > 0 && (
            <div className="flex items-center gap-2">
              <ChartBarIcon className="h-4 w-4 text-neutral-500" />
              <span className="text-neutral-600 dark:text-neutral-400">
                Reviewed: {sessionStats.reviewed}
              </span>
              <span className="text-green-600 dark:text-green-400">
                Easy: {sessionStats.easy}
              </span>
              <span className="text-yellow-600 dark:text-yellow-400">
                Medium: {sessionStats.medium}
              </span>
              <span className="text-red-600 dark:text-red-400">
                Hard: {sessionStats.hard}
              </span>
            </div>
          )}
        </div>
      </div>
      
      {/* Vocabulary Card */}
      <LanguageVocabularyCard
        word={currentWord}
        onNext={handleNext}
        onDifficulty={handleDifficulty}
        isReviewMode={isReviewMode}
      />
    </div>
  )
}

export default LanguageVocabularyMode