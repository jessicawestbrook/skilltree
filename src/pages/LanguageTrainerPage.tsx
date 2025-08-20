import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { 
  CheckCircleIcon, 
  XCircleIcon,
  LanguageIcon,
  ClockIcon,
  FlagIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline'
import FlagContentModal from '../components/FlagContentModal'

interface Language {
  id: string
  name: string
  code: string
  flag_emoji?: string
}

interface Category {
  id: string
  language_id: string
  name: string
  description: string
  display_order: number
}

interface Question {
  id: string
  language_id: string
  category_id: string
  question_text: string
  question_type: string
  options: string[]
  correct_answer_index: number
  explanation: string
  difficulty_level: number
  image_url?: string
  audio_url?: string
}

interface UserProgress {
  language_id: string
  category_id: string
  questions_attempted: number
  questions_correct: number
  accuracy_percentage: number
}

const LanguageTrainerPage: React.FC = () => {
  const { user } = useAuth()
  const [languages, setLanguages] = useState<Language[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [questionBank, setQuestionBank] = useState<Question[]>([])
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(true)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 })
  const [overallStats, setOverallStats] = useState({ correct: 0, total: 0 })
  const [showFlagModal, setShowFlagModal] = useState(false)
  
  const [selectedLanguage, setSelectedLanguage] = useState<Language | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(null)
  const [userProgress, setUserProgress] = useState<UserProgress[]>([])
  
  const [error, setError] = useState<string | null>(null)

  // Load languages on component mount
  const loadLanguages = useCallback(async () => {
    try {
      const { data, error } = await supabase
        .from('languages')
        .select('*')
        .order('name')

      if (error) throw error
      
      // Sort languages with Spanish first, then alphabetically
      const sortedLanguages = (data || []).sort((a, b) => {
        if (a.code === 'es') return -1
        if (b.code === 'es') return 1
        return a.name.localeCompare(b.name)
      })
      
      setLanguages(sortedLanguages)
      
      // Auto-select first language if none selected (Spanish will be first)
      if (sortedLanguages.length > 0 && !selectedLanguage) {
        setSelectedLanguage(sortedLanguages[0])
      }
    } catch (err) {
      console.error('Error loading languages:', err)
      setError('Failed to load languages')
    }
  }, [selectedLanguage])

  // Load categories when language is selected
  const loadCategories = useCallback(async (languageId: string) => {
    try {
      const { data, error } = await supabase
        .from('language_categories')
        .select('*')
        .eq('language_id', languageId)
        .order('display_order')

      if (error) throw error
      setCategories(data || [])
      
      // Auto-select first category if none selected
      if (data && data.length > 0 && !selectedCategory) {
        setSelectedCategory(data[0])
      }
    } catch (err) {
      console.error('Error loading categories:', err)
      setError('Failed to load categories')
    }
  }, [selectedCategory])

  // Load questions when category is selected
  const loadQuestions = useCallback(async (categoryId: string) => {
    try {
      const { data, error } = await supabase
        .from('language_questions')
        .select('*')
        .eq('category_id', categoryId)
        .order('difficulty_level')

      if (error) throw error
      
      const questions = data || []
      setQuestionBank(questions)
      
      if (questions.length > 0) {
        // Shuffle questions for variety
        const shuffled = [...questions].sort(() => Math.random() - 0.5)
        setQuestionBank(shuffled)
        setCurrentQuestion(shuffled[0])
        setCurrentIndex(0)
      } else {
        setCurrentQuestion(null)
      }
    } catch (err) {
      console.error('Error loading questions:', err)
      setError('Failed to load questions')
    }
  }, [])

  // Load user progress
  const loadUserProgress = useCallback(async (languageId: string) => {
    if (!user) return

    try {
      const { data, error } = await supabase
        .from('user_language_progress')
        .select('*')
        .eq('user_id', user.id)
        .eq('language_id', languageId)

      if (error) throw error
      setUserProgress(data || [])
    } catch (err) {
      console.error('Error loading user progress:', err)
    }
  }, [user])

  // Load overall user stats
  const loadOverallStats = useCallback(async () => {
    if (!user) return

    try {
      const { data, error } = await supabase
        .from('user_language_attempts')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })

      if (!error && data) {
        const correct = data.filter(a => a.is_correct).length
        setOverallStats({ correct, total: data.length })
      }
    } catch (error) {
      console.error('Error fetching overall stats:', error)
    }
  }, [user])

  // Initialize the trainer
  const initializeTrainer = useCallback(async () => {
    setLoading(true)
    await loadLanguages()
    if (user) {
      await loadOverallStats()
    }
    setLoading(false)
  }, [loadLanguages, loadOverallStats, user])

  useEffect(() => {
    initializeTrainer()
  }, [initializeTrainer])

  // Load categories when language changes
  useEffect(() => {
    if (selectedLanguage) {
      loadCategories(selectedLanguage.id)
      if (user) {
        loadUserProgress(selectedLanguage.id)
      }
    }
  }, [selectedLanguage, loadCategories, loadUserProgress, user])

  // Load questions when category changes
  useEffect(() => {
    if (selectedCategory) {
      loadQuestions(selectedCategory.id)
    }
  }, [selectedCategory, loadQuestions])

  const handleAnswerSelect = (answerIndex: number) => {
    if (showResult) return
    setSelectedAnswer(answerIndex)
  }

  const handleSubmit = async () => {
    if (!currentQuestion || selectedAnswer === null) return

    const correct = selectedAnswer === currentQuestion.correct_answer_index
    setIsCorrect(correct)
    setShowResult(true)

    // Update session stats
    setSessionStats(prev => ({
      correct: prev.correct + (correct ? 1 : 0),
      total: prev.total + 1
    }))

    // Record the attempt if user is logged in
    if (user) {
      await recordAttempt(currentQuestion.id, selectedAnswer, correct)
    }
  }

  const recordAttempt = async (questionId: string, selectedIndex: number, isCorrect: boolean) => {
    if (!user) return

    try {
      const { error } = await supabase
        .from('user_language_attempts')
        .insert({
          user_id: user.id,
          question_id: questionId,
          selected_option_index: selectedIndex,
          is_correct: isCorrect,
          time_taken_seconds: 0
        })

      if (error) throw error

      // Update user progress
      if (selectedLanguage && selectedCategory) {
        await updateUserProgress(selectedLanguage.id, selectedCategory.id, isCorrect)
      }

      // Update overall stats
      setOverallStats(prev => ({
        correct: prev.correct + (isCorrect ? 1 : 0),
        total: prev.total + 1
      }))
    } catch (err) {
      console.error('Error recording attempt:', err)
    }
  }

  const updateUserProgress = async (languageId: string, categoryId: string, isCorrect: boolean) => {
    if (!user) return

    try {
      const { data: existingProgress } = await supabase
        .from('user_language_progress')
        .select('*')
        .eq('user_id', user.id)
        .eq('language_id', languageId)
        .eq('category_id', categoryId)
        .single()

      if (existingProgress) {
        const newQuestionsAttempted = existingProgress.questions_attempted + 1
        const newQuestionsCorrect = existingProgress.questions_correct + (isCorrect ? 1 : 0)
        const newAccuracy = (newQuestionsCorrect / newQuestionsAttempted) * 100

        await supabase
          .from('user_language_progress')
          .update({
            questions_attempted: newQuestionsAttempted,
            questions_correct: newQuestionsCorrect,
            accuracy_percentage: newAccuracy,
            last_practiced: new Date().toISOString(),
            updated_at: new Date().toISOString()
          })
          .eq('id', existingProgress.id)
      } else {
        await supabase
          .from('user_language_progress')
          .insert({
            user_id: user.id,
            language_id: languageId,
            category_id: categoryId,
            questions_attempted: 1,
            questions_correct: isCorrect ? 1 : 0,
            accuracy_percentage: isCorrect ? 100 : 0
          })
      }

      // Refresh progress data
      if (selectedLanguage) {
        loadUserProgress(selectedLanguage.id)
      }
    } catch (err) {
      console.error('Error updating progress:', err)
    }
  }

  const nextQuestion = () => {
    const nextIndex = (currentIndex + 1) % questionBank.length
    setCurrentIndex(nextIndex)
    setCurrentQuestion(questionBank[nextIndex])
    setSelectedAnswer(null)
    setShowResult(false)
  }

  const getCategoryProgress = (categoryId: string): UserProgress | null => {
    return userProgress.find(p => p.category_id === categoryId) || null
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-6 text-center">
          <p className="text-lg text-red-700 dark:text-red-400">{error}</p>
        </div>
      </div>
    )
  }

  if (!currentQuestion) {
    return (
      <div className="max-w-4xl mx-auto p-1 sm:p-4 space-y-2 sm:space-y-6">
        {/* Page Title */}
        <div className="text-center py-1 sm:py-0">
          <h1 className="text-xl sm:text-3xl font-bold">Language Trainer</h1>
        </div>

        {/* Setup Card */}
        <div className="bg-white dark:bg-neutral-900 rounded-lg sm:rounded-xl shadow-lg p-4 sm:p-6">
          <div className="space-y-4">
            {/* Language Selection */}
            <div>
              <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                Select a Language:
              </label>
              <div className="relative">
                <select
                  value={selectedLanguage?.id || ''}
                  onChange={(e) => {
                    const language = languages.find(l => l.id === e.target.value) || null
                    setSelectedLanguage(language)
                    setSelectedCategory(null) // Reset category when language changes
                  }}
                  className="w-full px-3 py-2 bg-white dark:bg-neutral-800 border border-neutral-300 dark:border-neutral-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 appearance-none"
                >
                  <option value="">Choose a language...</option>
                  {languages.map(language => (
                    <option key={language.id} value={language.id}>
                      {language.flag_emoji} {language.name}
                    </option>
                  ))}
                </select>
                <ChevronDownIcon className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400 pointer-events-none" />
              </div>
            </div>

            {/* Category Selection */}
            {selectedLanguage && categories.length > 0 && (
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Select a Category:
                </label>
                <div className="space-y-2">
                  {categories.map(category => {
                    const progress = getCategoryProgress(category.id)
                    return (
                      <div
                        key={category.id}
                        onClick={() => setSelectedCategory(category)}
                        className={`p-3 border rounded-lg cursor-pointer transition-all hover:shadow-sm ${
                          selectedCategory?.id === category.id
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                            : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-300 bg-white dark:bg-neutral-800'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <h3 className="font-medium text-sm text-neutral-900 dark:text-white">
                              {category.name}
                            </h3>
                            <p className="text-xs text-neutral-600 dark:text-neutral-400 mt-1">
                              {category.description}
                            </p>
                          </div>
                          {progress && (
                            <div className="text-right">
                              <div className="text-xs font-medium text-primary-600 dark:text-primary-400">
                                {progress.accuracy_percentage.toFixed(0)}% accuracy
                              </div>
                              <div className="text-xs text-neutral-500 dark:text-neutral-400">
                                {progress.questions_correct}/{progress.questions_attempted} correct
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {selectedLanguage && categories.length === 0 && (
              <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-4 text-center">
                <p className="text-sm text-yellow-700 dark:text-yellow-400">
                  No categories available for {selectedLanguage.name} yet. Please check back later!
                </p>
              </div>
            )}

            {selectedCategory && questionBank.length === 0 && (
              <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-4 text-center">
                <p className="text-sm text-yellow-700 dark:text-yellow-400">
                  No questions available for {selectedCategory.name} yet. Please try a different category!
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-1 sm:p-4 space-y-2 sm:space-y-6">
      {/* Page Title */}
      <div className="text-center py-1 sm:py-0">
        <h1 className="text-xl sm:text-3xl font-bold">Language Trainer</h1>
      </div>

      {/* Combined Language Practice Card */}
      <div className="bg-white dark:bg-neutral-900 rounded-lg sm:rounded-xl shadow-lg p-2 sm:p-6 relative">
        {/* Flag Button */}
        {currentQuestion && (
          <button
            onClick={() => setShowFlagModal(true)}
            className="absolute top-2 right-2 p-1.5 text-neutral-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors z-10"
            title="Report an issue with this question"
          >
            <FlagIcon className="h-4 w-4" />
          </button>
        )}
        
        {/* Settings and Stats Row */}
        <div className="flex justify-between items-start mb-1 sm:mb-2">
          {/* Practice Settings */}
          <div className="flex flex-col lg:flex-row gap-1 sm:gap-2 items-start lg:items-center flex-1 mr-2 sm:mr-0">
            {/* Language and Category Display */}
            <div className="flex flex-wrap items-center gap-1 text-xs">
              {selectedLanguage && (
                <span className="bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 px-2 py-1 rounded font-medium">
                  {selectedLanguage.flag_emoji} {selectedLanguage.name}
                </span>
              )}
              {selectedCategory && (
                <span className="bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 px-2 py-1 rounded">
                  {selectedCategory.name}
                </span>
              )}
            </div>

            {/* Question Progress */}
            <div className="text-xs text-neutral-600 dark:text-neutral-400">
              Question {currentIndex + 1} of {questionBank.length}
            </div>
          </div>

          {/* Unified Stats Section */}
          <div className="flex-shrink-0">
            <h4 className="text-xs font-medium mb-1 flex items-center gap-0.5">
              <ClockIcon className="h-3 w-3 text-neutral-600" />
              Statistics
            </h4>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-1 text-xs">
              {/* Session Questions */}
              <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                <span className="font-bold text-primary-600">{sessionStats.total}</span>
                <span className="text-neutral-500 ml-0.5">today</span>
              </div>
              
              {/* Session Accuracy */}
              <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                <span className="font-bold text-green-600">
                  {sessionStats.total > 0 ? Math.round((sessionStats.correct / sessionStats.total) * 100) : 0}%
                </span>
                <span className="text-neutral-500 ml-0.5">session</span>
              </div>
              
              {/* Overall Correct */}
              {user && overallStats.total > 0 && (
                <>
                  <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                    <span className="font-bold text-green-500">{overallStats.correct}</span>
                    <span className="text-neutral-500 ml-0.5">✓</span>
                  </div>
                  
                  {/* Overall Percentage */}
                  <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-1.5 py-0.5 text-center">
                    <span className="font-bold text-primary-600">
                      {Math.round((overallStats.correct / overallStats.total) * 100)}%
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
            <div className="space-y-3 mb-4">
              <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/20 rounded-xl p-4 sm:p-6 border-2 border-primary-200 dark:border-primary-700 shadow-lg">
                <p className="text-lg sm:text-xl font-medium text-neutral-800 dark:text-neutral-200 leading-relaxed text-center">
                  {currentQuestion.question_text}
                </p>
              </div>

              <div className="text-center mb-4 space-y-1">
                <div className="flex justify-center items-center gap-2 sm:gap-3 text-xs">
                  <span className={`px-1 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-medium ${
                    currentQuestion.difficulty_level === 1 ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                    currentQuestion.difficulty_level === 2 ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                    currentQuestion.difficulty_level === 3 ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                    currentQuestion.difficulty_level === 4 ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' :
                    'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                  }`}>
                    Level {currentQuestion.difficulty_level}
                  </span>
                </div>
              </div>
            </div>

            {/* Multiple Choice Options */}
            <div className="space-y-2 mb-3">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {currentQuestion.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleAnswerSelect(index)}
                    className={`p-3 text-left border-2 rounded-lg transition-colors ${
                      selectedAnswer === index
                        ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20'
                        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/10 bg-white dark:bg-neutral-800'
                    }`}
                  >
                    <span className="text-base">{option}</span>
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={handleSubmit}
              disabled={selectedAnswer === null}
              className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 active:bg-primary-800 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors text-sm"
            >
              Submit
            </button>
          </>
        ) : (
          <>
            {/* Result Display */}
            <div className={`mb-3 p-2 rounded-lg ${
              isCorrect 
                ? 'bg-green-50 dark:bg-green-900/20' 
                : 'bg-red-50 dark:bg-red-900/20'
            }`}>
              {isCorrect ? (
                <div className="flex items-center justify-center gap-2">
                  <CheckCircleIcon className="h-5 w-5 text-green-500" />
                  <span className="text-sm font-bold text-green-700 dark:text-green-400">
                    Correct!
                  </span>
                </div>
              ) : (
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <XCircleIcon className="h-5 w-5 text-red-500" />
                    <span className="text-sm font-bold text-red-700 dark:text-red-400">Incorrect</span>
                  </div>
                  <div className="text-xs">
                    <span className="text-red-600 dark:text-red-400">
                      {currentQuestion.options[selectedAnswer!]}
                    </span>
                    <span className="mx-2">→</span>
                    <span className="font-bold text-green-600 dark:text-green-400">
                      {currentQuestion.options[currentQuestion.correct_answer_index]}
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Explanation */}
            {currentQuestion.explanation && (
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 mb-4">
                <h3 className="font-semibold text-xs mb-1 flex items-center gap-1">
                  <LanguageIcon className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                  Explanation
                </h3>
                <p className="text-xs text-neutral-700 dark:text-neutral-300">
                  {currentQuestion.explanation}
                </p>
              </div>
            )}

            <button
              onClick={nextQuestion}
              className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 active:bg-primary-800 transition-colors text-sm"
            >
              Next Question →
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
          contentId={currentQuestion.id}
          contentTitle={`Language: ${currentQuestion.question_text}`}
        />
      )}
    </div>
  )
}

export default LanguageTrainerPage