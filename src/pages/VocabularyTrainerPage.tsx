import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { useSpellingBee } from '../contexts/SpellingBeeContext'
import { checkSpellingBeeTables, createSpellingBeeTables } from '../utils/createSpellingBeeTables'
import { replaceWordAndVariationsWithBlanks } from '../utils/vocabularyHelpers'
import { 
  CheckCircleIcon, 
  XCircleIcon,
  AcademicCapIcon,
  ClockIcon,
  FlagIcon
} from '@heroicons/react/24/outline'
import FlagContentModal from '../components/FlagContentModal'
import StudyListActions from '../components/StudyListActions'

interface SpellingWord {
  id: string
  word: string
  definition: string
  example_sentence: string
  difficulty_level: number
  difficulty_name?: string
  source_difficulty?: string
  ai_difficulty_level?: number
  ai_difficulty_name?: string
  etymology?: string
  etymology_source?: string
  pronunciation_guide?: string
  part_of_speech?: string
  memory_tips?: string
  pronunciation_tips?: string
  common_misspellings?: string[]
  phonetic_transparency_score?: number
  word_frequency_score?: number
  morphology_score?: number
  etymology_score?: number
  source_names?: string[]
  source_difficulties?: string[]
  original_source?: string
  audio_url?: string
}

interface VocabularyQuestion {
  word: SpellingWord
  options: string[]
  correctAnswer: string
}

const VocabularyTrainerPage: React.FC = () => {
  const { user } = useAuth()
  const { selectedDifficulties, setSelectedDifficulties, toggleDifficulty, useAdaptiveTesting, setUseAdaptiveTesting } = useSpellingBee()
  const [currentQuestion, setCurrentQuestion] = useState<VocabularyQuestion | null>(null)
  const [selectedAnswer, setSelectedAnswer] = useState<string>('')
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(true)
  const [wordBank, setWordBank] = useState<SpellingWord[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [stats, setStats] = useState({ correct: 0, total: 0 })
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 })
  const [showFlagModal, setShowFlagModal] = useState(false)

  const fetchWords = useCallback(async () => {
    try {
      let query = supabase
        .from('spelling_words')
        .select('*')
        .order('difficulty_level')

      // Apply difficulty filter from selected difficulties
      if (selectedDifficulties.length > 0 && selectedDifficulties.length < 5) {
        query = query.in('difficulty_name', selectedDifficulties)
      }

      const { data, error } = await query.limit(100)

      if (error) {
        console.error('Error fetching words:', error)
        setLoading(false)
        return
      }

      if (data && data.length > 0) {
        // Shuffle words for variety
        const shuffled = [...data].sort(() => Math.random() - 0.5)
        setWordBank(shuffled)
        generateQuestion(shuffled, 0)
        setCurrentIndex(0)
      }
    } catch (error) {
      console.error('Error fetching words:', error)
    } finally {
      setLoading(false)
    }
  }, [selectedDifficulties])

  const generateQuestion = (words: SpellingWord[], index: number) => {
    if (!words || words.length === 0) return

    const targetWord = words[index]
    
    // Generate plausible alternatives from same difficulty level
    const sameLevel = words.filter(w => 
      w.id !== targetWord.id && 
      w.difficulty_name === targetWord.difficulty_name
    )
    
    // If not enough same level words, use all other words
    const alternatives = sameLevel.length >= 3 ? sameLevel : words.filter(w => w.id !== targetWord.id)
    
    // Randomly select 3 alternatives
    const shuffledAlternatives = [...alternatives].sort(() => Math.random() - 0.5)
    const wrongOptions = shuffledAlternatives.slice(0, 3).map(w => w.word)
    
    // Create options array with correct answer
    const allOptions = [targetWord.word, ...wrongOptions]
    const shuffledOptions = [...allOptions].sort(() => Math.random() - 0.5)

    setCurrentQuestion({
      word: targetWord,
      options: shuffledOptions,
      correctAnswer: targetWord.word
    })
  }

  const fetchUserStats = useCallback(async () => {
    if (!user) return

    try {
      const { data, error } = await supabase
        .from('user_vocabulary_attempts')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })

      if (!error && data) {
        const correct = data.filter(a => a.correct).length
        setStats({ correct, total: data.length })
      }
    } catch (error) {
      console.error('Error fetching user stats:', error)
    }
  }, [user])

  const initializeVocabularyTrainer = useCallback(async () => {
    // Check if tables exist, create if not
    const tablesExist = await checkSpellingBeeTables()
    if (!tablesExist) {
      console.log('Creating spelling bee tables...')
      await createSpellingBeeTables()
    }
    
    await fetchWords()
    if (user) {
      await fetchUserStats()
    }
  }, [user, fetchWords, fetchUserStats])

  useEffect(() => {
    initializeVocabularyTrainer()
  }, [initializeVocabularyTrainer])

  // Refetch words when selected difficulties change
  useEffect(() => {
    setLoading(true)
    fetchWords()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedDifficulties])

  const handleAnswerSelect = (answer: string) => {
    if (showResult) return
    setSelectedAnswer(answer)
  }

  const handleSubmit = async () => {
    if (!currentQuestion || !selectedAnswer) return

    const correct = selectedAnswer === currentQuestion.correctAnswer
    setIsCorrect(correct)
    setShowResult(true)

    // Update session stats
    setSessionStats(prev => ({
      correct: prev.correct + (correct ? 1 : 0),
      total: prev.total + 1
    }))

    // Save attempt if user is logged in
    if (user) {
      // First create vocabulary attempts table if it doesn't exist
      await supabase.rpc('exec_sql', {
        sql: `
          CREATE TABLE IF NOT EXISTS user_vocabulary_attempts (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
            word_id UUID NOT NULL REFERENCES spelling_words(id) ON DELETE CASCADE,
            correct BOOLEAN NOT NULL,
            selected_answer VARCHAR(200) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
          );
          
          CREATE INDEX IF NOT EXISTS idx_user_vocabulary_attempts_user ON user_vocabulary_attempts(user_id);
          CREATE INDEX IF NOT EXISTS idx_user_vocabulary_attempts_word ON user_vocabulary_attempts(word_id);
        `
      })

      await supabase.from('user_vocabulary_attempts').insert({
        user_id: user.id,
        word_id: currentQuestion.word.id,
        correct,
        selected_answer: selectedAnswer
      })

      setStats(prev => ({
        correct: prev.correct + (correct ? 1 : 0),
        total: prev.total + 1
      }))
    }
  }

  const nextQuestion = () => {
    const nextIndex = (currentIndex + 1) % wordBank.length
    setCurrentIndex(nextIndex)
    generateQuestion(wordBank, nextIndex)
    setSelectedAnswer('')
    setShowResult(false)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!currentQuestion) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6 text-center">
          <p className="text-lg">No vocabulary words available. Please check back later!</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-1 sm:p-2 pt-2 sm:pt-2 space-y-1 sm:space-y-2">
      {/* Combined Vocabulary Practice Card */}
      <div className="bg-white dark:bg-neutral-900 rounded-lg sm:rounded-xl shadow-lg p-2 sm:p-3 pt-14 sm:pt-12 relative">
        {/* Page Title */}
        <div className="text-center mb-1 sm:mb-2">
          <h1 className="text-lg sm:text-xl font-bold text-neutral-800 dark:text-neutral-200">Vocabulary Trainer</h1>
        </div>
        {/* Action Buttons */}
        {currentQuestion && (
          <div className="absolute top-2 right-2 flex items-center gap-1 z-10">
            <StudyListActions
              itemType="vocabulary_word"
              itemId={currentQuestion.word.id}
              itemData={currentQuestion.word}
              itemTitle={`Vocabulary: ${currentQuestion.word.word}`}
              className="bg-white dark:bg-neutral-800 rounded-lg shadow-sm border border-neutral-200 dark:border-neutral-700 px-2 py-1"
            />
            <button
              onClick={() => setShowFlagModal(true)}
              className="p-1.5 text-neutral-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700"
              title="Report an issue with this question"
            >
              <FlagIcon className="h-4 w-4" />
            </button>
          </div>
        )}
        
        {/* Settings and Stats Row */}
        <div className="flex justify-between items-start mb-1">
          {/* Practice Settings */}
          <div className="flex flex-col lg:flex-row gap-1 sm:gap-2 items-start lg:items-center flex-1 mr-2 sm:mr-0">
            {/* Adaptive Learning Toggle */}
            <div className="flex items-center gap-1">
              <label className="flex items-center gap-1 cursor-pointer">
                <input
                  type="checkbox"
                  checked={useAdaptiveTesting}
                  onChange={(e) => setUseAdaptiveTesting(e.target.checked)}
                  className="rounded border-neutral-300 text-primary-600 focus:ring-primary-500 h-3 w-3"
                />
                <span className="text-xs font-medium">Adaptive Learning</span>
              </label>
              {useAdaptiveTesting && (
                <span className="text-xs text-neutral-500">Auto-adjusts</span>
              )}
            </div>

            {/* Difficulty Selection */}
            {!useAdaptiveTesting && (
              <div className="flex items-center gap-1 flex-wrap">
                <span className="text-xs font-medium text-neutral-700 dark:text-neutral-300">Difficulty:</span>
                <div className="flex flex-wrap gap-0.5">
                  {['Beginner', 'Elementary', 'Intermediate', 'Advanced', 'Expert'].map((level) => (
                    <label key={level} className="flex items-center gap-0.5 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={selectedDifficulties.includes(level)}
                        onChange={() => toggleDifficulty(level)}
                        className="rounded border-neutral-300 text-primary-600 focus:ring-primary-500 h-3 w-3"
                      />
                      <span className="text-xs">{level.substring(0, 3)}</span>
                    </label>
                  ))}
                </div>
                <div className="flex gap-0.5">
                  <button
                    type="button"
                    onClick={() => setSelectedDifficulties(['Beginner', 'Elementary', 'Intermediate', 'Advanced', 'Expert'])}
                    className="text-xs text-primary-600 hover:text-primary-700 font-medium px-1 py-0.5 rounded hover:bg-primary-50"
                  >
                    All
                  </button>
                  <button
                    type="button"
                    onClick={() => setSelectedDifficulties(['Beginner'])}
                    className="text-xs text-neutral-500 hover:text-neutral-700 px-1 py-0.5 rounded hover:bg-neutral-100"
                  >
                    Clear
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Unified Stats Section */}
          <div className="flex-shrink-0">
            <h4 className="text-xs font-medium mb-1 flex items-center gap-0.5">
              <ClockIcon className="h-3 w-3 text-neutral-600" />
              Statistics
            </h4>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-1 text-xs">
              {/* Session Words */}
              <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                <span className="font-bold text-primary-600">{sessionStats.total}</span>
                <span className="text-neutral-500 ml-0.5">words</span>
              </div>
              
              {/* Session Accuracy */}
              <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                <span className="font-bold text-green-600">
                  {sessionStats.total > 0 ? Math.round((sessionStats.correct / sessionStats.total) * 100) : 0}%
                </span>
                <span className="text-neutral-500 ml-0.5">today</span>
              </div>
              
              {/* Overall Correct */}
              {user && stats.total > 0 && (
                <>
                  <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                    <span className="font-bold text-green-500">{stats.correct}</span>
                    <span className="text-neutral-500 ml-0.5">✓</span>
                  </div>
                  
                  {/* Overall Percentage */}
                  <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                    <span className="font-bold text-primary-600">
                      {Math.round((stats.correct / stats.total) * 100)}%
                    </span>
                    <span className="text-neutral-500 ml-0.5">total</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        {!showResult ? (
          <>
            {/* Question Content */}
            <div className="space-y-2 mb-2">
              <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/20 rounded-lg p-3 sm:p-4 border-2 border-primary-200 dark:border-primary-700 shadow-lg">
                <p className="text-base sm:text-lg font-medium text-neutral-800 dark:text-neutral-200 leading-snug text-center">
                  {replaceWordAndVariationsWithBlanks(currentQuestion.word.definition, currentQuestion.word.word)}
                </p>
              </div>

              <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-2 text-center border border-gold-200 dark:border-gold-800">
                <h3 className="font-semibold text-sm mb-2 text-gold-700 dark:text-gold-400">Example</h3>
                <p className="text-sm text-neutral-700 dark:text-neutral-300 italic">
                  "{currentQuestion.word.example_sentence}"
                </p>
              </div>
            </div>

            <div className="text-center mb-2 space-y-1">
              <div className="flex justify-center items-center gap-2 sm:gap-3 text-xs">
                {currentQuestion.word.difficulty_name && (
                  <span className={`px-1 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-medium ${
                    currentQuestion.word.difficulty_name === 'Beginner' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                    currentQuestion.word.difficulty_name === 'Elementary' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                    currentQuestion.word.difficulty_name === 'Intermediate' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                    currentQuestion.word.difficulty_name === 'Advanced' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' :
                    'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                  }`}>
                    {currentQuestion.word.difficulty_name}
                  </span>
                )}
                {currentQuestion.word.part_of_speech && (
                  <span className="text-neutral-600 dark:text-neutral-400 italic">
                    {currentQuestion.word.part_of_speech}
                  </span>
                )}
              </div>
            </div>

            {/* Multiple Choice Options */}
            <div className="space-y-1.5 mb-2">
              <h3 className="font-semibold text-sm">Which word matches the definition above?</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                {currentQuestion.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleAnswerSelect(option)}
                    className={`p-1.5 text-left border-2 rounded-lg transition-colors ${
                      selectedAnswer === option
                        ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20'
                        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/10 bg-white dark:bg-neutral-800'
                    }`}
                  >
                    <span className="text-sm">{option}</span>
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={handleSubmit}
              disabled={!selectedAnswer}
              className="w-full py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 active:bg-primary-800 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors text-sm"
            >
              Submit
            </button>
          </>
        ) : (
          <>
            {/* Result Display */}
            <div className={`mb-2 p-2 rounded-lg ${
              isCorrect 
                ? 'bg-green-50 dark:bg-green-900/20' 
                : 'bg-red-50 dark:bg-red-900/20'
            }`}>
              {isCorrect ? (
                <div className="flex items-center justify-center gap-2">
                  <CheckCircleIcon className="h-5 w-5 text-green-500" />
                  <span className="text-sm font-bold text-green-700 dark:text-green-400">
                    Correct! "{currentQuestion.word.word}"
                  </span>
                </div>
              ) : (
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <XCircleIcon className="h-5 w-5 text-red-500" />
                    <span className="text-sm font-bold text-red-700 dark:text-red-400">Incorrect</span>
                  </div>
                  <div className="text-xs">
                    <span className="text-red-600 dark:text-red-400">{selectedAnswer}</span>
                    <span className="mx-2">→</span>
                    <span className="font-mono text-green-600 dark:text-green-400 font-bold">{currentQuestion.word.word}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Learning Information */}
            <div className="space-y-1.5 mb-2">
              {(currentQuestion.word.memory_tips || currentQuestion.word.pronunciation_tips) && (
                <div className="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-3">
                  <h3 className="font-semibold text-xs mb-1 flex items-center gap-1">
                    <AcademicCapIcon className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    Memory Tips
                  </h3>
                  <p className="text-xs text-neutral-700 dark:text-neutral-300">
                    {currentQuestion.word.memory_tips || currentQuestion.word.pronunciation_tips}
                  </p>
                </div>
              )}

              {currentQuestion.word.etymology && (
                <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-3">
                  <h3 className="font-semibold text-xs mb-1">
                    Word Origin & Etymology
                  </h3>
                  <p className="text-xs text-neutral-700 dark:text-neutral-300">
                    {currentQuestion.word.etymology}
                  </p>
                </div>
              )}
            </div>

            <button
              onClick={nextQuestion}
              className="w-full py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 active:bg-primary-800 transition-colors text-sm"
            >
              Next Word →
            </button>
          </>
        )}
      </div>

      {/* Flag Content Modal */}
      {showFlagModal && currentQuestion && (
        <FlagContentModal
          isOpen={showFlagModal}
          onClose={() => setShowFlagModal(false)}
          contentType="question"
          contentId={currentQuestion.word.id}
          contentTitle={`Vocabulary: ${currentQuestion.word.word}`}
        />
      )}
    </div>
  )
}

export default VocabularyTrainerPage