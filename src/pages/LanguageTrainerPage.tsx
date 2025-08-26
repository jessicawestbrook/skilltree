import React, { useState, useEffect, useCallback } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { spacedRepetitionService } from '../services/spacedRepetitionService'
import { useAuth } from '../contexts/AuthContext'
import { 
  CheckCircleIcon, 
  XCircleIcon,
  FlagIcon,
  SpeakerWaveIcon,
  BookOpenIcon,
  PencilSquareIcon,
  DocumentTextIcon,
  BeakerIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import FlagContentModal from '../components/FlagContentModal'
import StudyListActions from '../components/StudyListActions'
import SkipButton from '../components/flashcards/SkipButton'
import LanguageVocabularyMode from '../components/LanguageVocabularyMode'
import LanguageMixedMode from '../components/LanguageMixedMode'

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

interface Course {
  id: string
  language_id: string
  name: string
  description: string
  level: string
  estimated_hours: number
  is_active: boolean
}

// Language configuration with available features
const LANGUAGE_CONFIG: Record<string, {
  name: string
  code: string
  flag: string
  hasVocabulary: boolean
  hasGrammar: boolean
  hasCharacters?: boolean
  hasListening?: boolean
  hasReading?: boolean
}> = {
  spanish: {
    name: 'Spanish',
    code: 'es',
    flag: '🇪🇸',
    hasVocabulary: true,
    hasGrammar: true,
    hasListening: true,
    hasReading: true
  },
  chinese: {
    name: 'Chinese',
    code: 'zh',
    flag: '🇨🇳',
    hasVocabulary: false,  // Chinese uses Characters tab instead
    hasGrammar: false,
    hasCharacters: true,
    hasListening: false,
    hasReading: false
  },
  french: {
    name: 'French',
    code: 'fr',
    flag: '🇫🇷',
    hasVocabulary: false,
    hasGrammar: false,
    hasListening: false,
    hasReading: false
  },
  german: {
    name: 'German',
    code: 'de',
    flag: '🇩🇪',
    hasVocabulary: false,
    hasGrammar: false,
    hasListening: false,
    hasReading: false
  },
  italian: {
    name: 'Italian',
    code: 'it',
    flag: '🇮🇹',
    hasVocabulary: false,
    hasGrammar: false,
    hasListening: false,
    hasReading: false
  },
  portuguese: {
    name: 'Portuguese',
    code: 'pt',
    flag: '🇵🇹',
    hasVocabulary: false,
    hasGrammar: false,
    hasListening: false,
    hasReading: false
  },
  latin: {
    name: 'Latin',
    code: 'la',
    flag: '🏛️',
    hasVocabulary: false,
    hasGrammar: false,
    hasListening: false,
    hasReading: false
  }
}


const LanguageTrainerPage: React.FC = () => {
  const { user } = useAuth()
  const location = useLocation()
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const navigate = useNavigate()
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [languages, setLanguages] = useState<Language[]>([])
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [categories, setCategories] = useState<Category[]>([])
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [courses, setCourses] = useState<Course[]>([])
  const [questionBank, setQuestionBank] = useState<Question[]>([])
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(true)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 })
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [overallStats, setOverallStats] = useState({ correct: 0, total: 0 })
  const [showFlagModal, setShowFlagModal] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  
  const [selectedLanguage, setSelectedLanguage] = useState<string>('spanish')
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(null)
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [userProgress, setUserProgress] = useState<UserProgress[]>([])
  const [hasLanguageVoice, setHasLanguageVoice] = useState<boolean>(false)
  
  const [error, setError] = useState<string | null>(null)
  const [mode, setMode] = useState<'characters' | 'vocabulary' | 'grammar' | 'listening' | 'reading' | 'mixed'>('vocabulary')

  // Session storage keys
  const LANG_SESSION_KEY = 'languageTrainerSession'

  // Get current language config
  const currentLangConfig = LANGUAGE_CONFIG[selectedLanguage]

  // Update mode when language changes
  useEffect(() => {
    if (currentLangConfig) {
      // Set to the first available mode for this language
      if (currentLangConfig.hasCharacters) {
        setMode('characters')
      } else if (currentLangConfig.hasVocabulary) {
        setMode('vocabulary')
      } else if (currentLangConfig.hasGrammar) {
        setMode('grammar')
      } else {
        setMode('vocabulary')
      }
    }
  }, [selectedLanguage, currentLangConfig])

  // Save session state
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const saveSessionState = useCallback((question: Question, index: number, selectedAnswer: number | null, showResult: boolean, isCorrect: boolean, languageId: string, categoryId: string) => {
    const sessionState = {
      currentQuestion: question,
      currentIndex: index,
      selectedAnswer,
      showResult,
      isCorrect,
      languageId,
      categoryId,
      timestamp: Date.now()
    }
    sessionStorage.setItem(LANG_SESSION_KEY, JSON.stringify(sessionState))
  }, [LANG_SESSION_KEY])

  // Load session state
  const loadSessionState = useCallback(() => {
    try {
      const saved = sessionStorage.getItem(LANG_SESSION_KEY)
      if (saved) {
        const sessionState = JSON.parse(saved)
        // Only restore if saved within last 30 minutes
        if (Date.now() - sessionState.timestamp < 30 * 60 * 1000) {
          return sessionState
        }
      }
    } catch (error) {
      console.error('Error loading session state:', error)
    }
    return null
  }, [LANG_SESSION_KEY])

  // Clear session state
  const clearSessionState = useCallback(() => {
    sessionStorage.removeItem(LANG_SESSION_KEY)
  }, [LANG_SESSION_KEY])

  // Dynamic tab configuration based on language
  const getTabs = () => {
    const tabs = []
    
    if (currentLangConfig?.hasCharacters) {
      tabs.push({ id: 'characters', label: 'Characters', icon: PencilSquareIcon })
    }
    if (currentLangConfig?.hasVocabulary) {
      tabs.push({ id: 'vocabulary', label: 'Vocabulary', icon: BookOpenIcon })
    }
    if (currentLangConfig?.hasGrammar) {
      tabs.push({ id: 'grammar', label: 'Grammar', icon: PencilSquareIcon })
    }
    if (currentLangConfig?.hasListening) {
      tabs.push({ id: 'listening', label: 'Listening', icon: SpeakerWaveIcon })
    }
    if (currentLangConfig?.hasReading) {
      tabs.push({ id: 'reading', label: 'Reading', icon: DocumentTextIcon })
    }
    
    // Add mixed mode only if there are multiple content types
    const hasMultipleTypes = [
      currentLangConfig?.hasCharacters,
      currentLangConfig?.hasVocabulary,
      currentLangConfig?.hasGrammar,
      currentLangConfig?.hasListening,
      currentLangConfig?.hasReading
    ].filter(Boolean).length > 1
    
    if (hasMultipleTypes) {
      tabs.push({ id: 'mixed', label: 'Mixed', icon: BeakerIcon })
    }
    
    return tabs
  }

  const tabs = getTabs()

  // Check if a language-specific voice is available
  const checkLanguageVoiceAvailability = useCallback(() => {
    if (!currentLangConfig || !('speechSynthesis' in window)) {
      setHasLanguageVoice(false)
      return
    }

    const checkVoices = () => {
      const voices = window.speechSynthesis.getVoices()
      const languageVoice = voices.find(voice => 
        voice.lang.toLowerCase().startsWith(currentLangConfig.code.toLowerCase())
      )
      setHasLanguageVoice(!!languageVoice)
    }

    // If voices are not loaded yet, wait for them
    if (window.speechSynthesis.getVoices().length === 0) {
      window.speechSynthesis.onvoiceschanged = () => {
        checkVoices()
        window.speechSynthesis.onvoiceschanged = null
      }
    } else {
      checkVoices()
    }
  }, [currentLangConfig])

  // Check voice availability when language changes
  useEffect(() => {
    checkLanguageVoiceAvailability()
  }, [selectedLanguage, checkLanguageVoiceAvailability])

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
    } catch (err) {
      console.error('Error loading languages:', err)
      setError('Failed to load languages')
    }
  }, [])

  // Load categories when language is selected
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const loadCategories = useCallback(async (languageId: string) => {
    try {
      const { data, error } = await supabase
        .from('language_categories')
        .select('*')
        .eq('language_id', languageId)
        .order('display_order')

      if (error) throw error
      setCategories(data || [])
      
      // Load courses for this language
      const { data: coursesData, error: coursesError } = await supabase
        .from('language_courses')
        .select('*')
        .eq('language_id', languageId)
        .eq('is_active', true)
        .order('display_order')
      
      if (coursesError) {
        console.error('Error loading courses:', coursesError)
      } else {
        setCourses(coursesData || [])
      }
      
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
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
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
        
        // Check for saved session state first
        const savedSession = loadSessionState()
        if (savedSession && savedSession.currentQuestion) {
          // Restore saved session
          setCurrentQuestion(savedSession.currentQuestion)
          setCurrentIndex(savedSession.currentIndex)
          setSelectedAnswer(savedSession.selectedAnswer)
          setShowResult(savedSession.showResult)
          setIsCorrect(savedSession.isCorrect)
          
          // Auto-play audio if restoring a result state
          const autoplayEnabled = localStorage.getItem('audioAutoplay') !== 'false'
          if (savedSession.showResult && hasLanguageVoice && autoplayEnabled) {
            setTimeout(() => {
              speakWord(savedSession.currentQuestion.options[savedSession.currentQuestion.correct_answer_index])
            }, 1000)
          }
        } else {
          // Start fresh
          setCurrentQuestion(shuffled[0])
          setCurrentIndex(0)
        }
      } else {
        setCurrentQuestion(null)
      }
    } catch (err) {
      console.error('Error loading questions:', err)
      setError('Failed to load questions')
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hasLanguageVoice, loadSessionState])

  // Load user progress
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
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

  // Load questions based on mode (grammar, reading, listening)
  useEffect(() => {
    if ((mode === 'grammar' || mode === 'reading' || mode === 'listening') && selectedLanguage === 'spanish') {
      const loadModeQuestions = async () => {
        setLoading(true)
        try {
          // Map mode to category (reading and listening use same content)
          const category = (mode === 'listening' || mode === 'reading') ? 'reading/listening' : 'grammar';
          
          // Get Spanish language ID
          const { data: spanishLang } = await supabase
            .from('languages')
            .select('id')
            .eq('code', 'es')
            .single()
          
          if (!spanishLang) {
            throw new Error('Spanish language not found')
          }
          
          // Load Spanish questions for the selected category
          const { data: questions, error } = await supabase
            .from('language_questions')
            .select('*')
            .eq('language_id', spanishLang.id) // Use actual Spanish UUID
            .eq('category', category) // Filter by category
            .order('difficulty_level')
            .limit(50)
          
          if (error) {
            console.error(`Error loading ${mode} questions:`, error)
            setError(`Failed to load ${mode} questions`)
          } else if (questions && questions.length > 0) {
            // Shuffle questions for variety
            const shuffled = [...questions].sort(() => Math.random() - 0.5)
            setQuestionBank(shuffled)
            setCurrentQuestion(shuffled[0])
            setCurrentIndex(0)
            setSelectedAnswer(null)
            setShowResult(false)
          } else {
            setQuestionBank([])
            setCurrentQuestion(null)
          }
        } catch (err) {
          console.error(`Error loading ${mode} questions:`, err)
          setError(`Failed to load ${mode} questions`)
        } finally {
          setLoading(false)
        }
      }
      
      loadModeQuestions()
    }
  }, [mode, selectedLanguage])

  // Handle navigation from study list page
  useEffect(() => {
    if (location.state) {
      const state = location.state as any
      if (state.studyListQuestions && state.studyListQuestions.length > 0) {
        // Load questions from the study list navigation
        const loadStudyListQuestions = async () => {
          setLoading(true)
          const questionIds = state.studyListQuestions.map((q: any) => q.id)
          const startIndex = state.startIndex || 0
          
          const { data: questions, error } = await supabase
            .from('language_questions')
            .select('*')
            .in('id', questionIds)
          
          if (error) {
            console.error('Error fetching study list questions:', error)
            setLoading(false)
            return
          }
          
          if (questions && questions.length > 0) {
            // Sort questions to match the order from study list
            const sortedQuestions = questionIds.map((id: string) => 
              questions.find((q: Question) => q.id === id)
            ).filter(Boolean) as Question[]
            
            setQuestionBank(sortedQuestions)
            setCurrentIndex(startIndex)
            setCurrentQuestion(sortedQuestions[startIndex])
            setLoading(false)
          }
        }
        
        loadStudyListQuestions()
        return
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state])

  const handleAnswerSelect = (answerIndex: number) => {
    if (showResult) return
    setSelectedAnswer(answerIndex)
    // Auto-submit the answer after a brief delay
    setTimeout(() => {
      handleSubmit(answerIndex)
    }, 100)
  }

  const handleSubmit = async (answerIndex?: number) => {
    if (!currentQuestion) return
    const answer = answerIndex !== undefined ? answerIndex : selectedAnswer
    if (answer === null) return

    const correct = answer === currentQuestion.correct_answer_index
    setIsCorrect(correct)
    setShowResult(true)

    // Auto-play audio for the correct answer
    const autoplayEnabled = localStorage.getItem('audioAutoplay') !== 'false'
    if (hasLanguageVoice && autoplayEnabled) {
      setTimeout(() => {
        speakWord(currentQuestion.options[currentQuestion.correct_answer_index])
      }, 500)
    }

    // Update session stats
    setSessionStats(prev => ({
      correct: prev.correct + (correct ? 1 : 0),
      total: prev.total + 1
    }))

    // Record the attempt if user is logged in
    if (user) {
      // Add this language question to flashcard review
      try {
        await spacedRepetitionService.addFlashcardsToReview(user.id, [{
          id: currentQuestion.id,
          type: 'language'
        }])
      } catch (error) {
        console.error('Error adding language question to flashcard review:', error)
      }
      
      await recordAttempt(currentQuestion.id, answer, correct)
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

      // Update overall stats
      setOverallStats(prev => ({
        correct: prev.correct + (isCorrect ? 1 : 0),
        total: prev.total + 1
      }))
    } catch (err) {
      console.error('Error recording attempt:', err)
    }
  }

  const speakWord = (text: string) => {
    if ('speechSynthesis' in window && currentLangConfig) {
      // Cancel any previous speech
      window.speechSynthesis.cancel()
      
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.8
      utterance.volume = 0.8
      utterance.pitch = 1.0
      
      // Set language based on the selected language code
      utterance.lang = currentLangConfig.code
      
      const speakWithLanguage = () => {
        // Try to find a voice that matches the language
        const voices = window.speechSynthesis.getVoices()
        const languageVoice = voices.find(voice => 
          voice.lang.toLowerCase().startsWith(currentLangConfig.code.toLowerCase())
        )
        
        if (languageVoice) {
          utterance.voice = languageVoice
        }
        
        window.speechSynthesis.speak(utterance)
      }
      
      // If voices are not loaded yet, wait for them
      if (window.speechSynthesis.getVoices().length === 0) {
        window.speechSynthesis.onvoiceschanged = () => {
          speakWithLanguage()
          window.speechSynthesis.onvoiceschanged = null
        }
      } else {
        speakWithLanguage()
      }
    }
  }

  const nextQuestion = () => {
    // Clear session state when moving to next question
    clearSessionState()
    
    const nextIndex = (currentIndex + 1) % questionBank.length
    setCurrentIndex(nextIndex)
    setCurrentQuestion(questionBank[nextIndex])
    setSelectedAnswer(null)
    setShowResult(false)
    setIsPlaying(false) // Reset audio playing state
  }

  const skipQuestion = () => {
    // Clear session state when skipping
    clearSessionState()
    
    // Move to next question without recording stats
    const nextIndex = (currentIndex + 1) % questionBank.length
    setCurrentIndex(nextIndex)
    setCurrentQuestion(questionBank[nextIndex])
    setSelectedAnswer(null)
    setShowResult(false)
    setIsPlaying(false) // Reset audio playing state
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

  // Render language menu
  const renderLanguageMenu = () => (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold text-neutral-600 dark:text-neutral-400 uppercase tracking-wider mb-3">
        Languages
      </h3>
      {Object.entries(LANGUAGE_CONFIG).map(([key, config]) => {
        const isActive = selectedLanguage === key
        const hasContent = config.hasVocabulary || config.hasGrammar || config.hasCharacters
        
        return (
          <button
            key={key}
            onClick={() => {
              setSelectedLanguage(key)
              setMobileMenuOpen(false)
            }}
            disabled={!hasContent}
            className={`
              w-full text-left px-3 py-2 rounded-lg transition-all flex items-center justify-between
              ${isActive 
                ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 font-medium' 
                : hasContent
                  ? 'hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-700 dark:text-neutral-300'
                  : 'text-neutral-400 dark:text-neutral-600 cursor-not-allowed opacity-60'
              }
            `}
          >
            <span className="flex items-center gap-2">
              <span className="text-lg">{config.flag}</span>
              <span>{config.name}</span>
            </span>
            {!hasContent && (
              <span className="text-xs text-neutral-400">Coming soon</span>
            )}
          </button>
        )
      })}
    </div>
  )

  // Render tab navigation
  const renderTabNavigation = () => (
    <div className="mb-4">
      <div className="border-b border-neutral-200 dark:border-neutral-700">
        <nav className="-mb-px flex flex-wrap gap-2 sm:gap-4" aria-label="Tabs">
          {tabs.map(tab => {
            const Icon = tab.icon
            const isActive = mode === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => setMode(tab.id as typeof mode)}
                className={`
                  group inline-flex items-center py-2 px-1 border-b-2 font-medium text-xs sm:text-sm transition-colors whitespace-nowrap
                  ${isActive
                    ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                    : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300 dark:text-neutral-400 dark:hover:text-neutral-300 dark:hover:border-neutral-600'
                  }
                `}
              >
                <Icon
                  className={`
                    -ml-0.5 mr-1 sm:mr-2 h-4 w-4 sm:h-5 sm:w-5
                    ${isActive
                      ? 'text-primary-500 dark:text-primary-400'
                      : 'text-neutral-400 group-hover:text-neutral-500 dark:text-neutral-500 dark:group-hover:text-neutral-400'
                    }
                  `}
                />
                <span>{tab.label}</span>
              </button>
            )
          })}
        </nav>
      </div>
    </div>
  )

  // Show vocabulary mode if selected
  if (mode === 'vocabulary' && currentLangConfig?.hasVocabulary) {
    return (
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Desktop Language Menu */}
        <aside className="hidden lg:block w-64 flex-shrink-0">
          <div className="bg-white dark:bg-neutral-900 rounded-lg shadow p-4">
            {renderLanguageMenu()}
          </div>
        </aside>

        {/* Mobile Language Selector */}
        <div className="lg:hidden mb-4">
          <div className="relative">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="w-full flex items-center justify-between px-4 py-2 bg-white dark:bg-neutral-900 rounded-lg shadow border border-neutral-200 dark:border-neutral-700"
            >
              <span className="flex items-center gap-2">
                <span className="text-lg">{currentLangConfig.flag}</span>
                <span className="font-medium">{currentLangConfig.name}</span>
              </span>
              {mobileMenuOpen ? (
                <XMarkIcon className="h-5 w-5 text-neutral-400" />
              ) : (
                <Bars3Icon className="h-5 w-5 text-neutral-400" />
              )}
            </button>
            
            {mobileMenuOpen && (
              <div className="absolute z-10 w-full mt-2 bg-white dark:bg-neutral-900 rounded-lg shadow-lg border border-neutral-200 dark:border-neutral-700 p-2">
                {renderLanguageMenu()}
              </div>
            )}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {renderTabNavigation()}
          <LanguageVocabularyMode 
            selectedLanguage={currentLangConfig.code} 
            onBack={() => setMode('grammar')}
          />
        </div>
      </div>
    )
  }

  // Show mixed mode if selected
  if (mode === 'mixed' && tabs.length > 1) {
    const languageObj: Language = {
      id: selectedLanguage,
      name: currentLangConfig.name,
      code: currentLangConfig.code,
      flag_emoji: currentLangConfig.flag
    }
    
    return (
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Desktop Language Menu */}
        <aside className="hidden lg:block w-64 flex-shrink-0">
          <div className="bg-white dark:bg-neutral-900 rounded-lg shadow p-4">
            {renderLanguageMenu()}
          </div>
        </aside>

        {/* Mobile Language Selector */}
        <div className="lg:hidden mb-4">
          <div className="relative">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="w-full flex items-center justify-between px-4 py-2 bg-white dark:bg-neutral-900 rounded-lg shadow border border-neutral-200 dark:border-neutral-700"
            >
              <span className="flex items-center gap-2">
                <span className="text-lg">{currentLangConfig.flag}</span>
                <span className="font-medium">{currentLangConfig.name}</span>
              </span>
              {mobileMenuOpen ? (
                <XMarkIcon className="h-5 w-5 text-neutral-400" />
              ) : (
                <Bars3Icon className="h-5 w-5 text-neutral-400" />
              )}
            </button>
            
            {mobileMenuOpen && (
              <div className="absolute z-10 w-full mt-2 bg-white dark:bg-neutral-900 rounded-lg shadow-lg border border-neutral-200 dark:border-neutral-700 p-2">
                {renderLanguageMenu()}
              </div>
            )}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {renderTabNavigation()}
          <LanguageMixedMode 
            selectedLanguage={languageObj}
            onBack={() => setMode('vocabulary')}
          />
        </div>
      </div>
    )
  }

  // Placeholder for other modes
  const renderPlaceholder = (title: string, icon: React.ComponentType<{ className?: string }>) => {
    const Icon = icon
    return (
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Desktop Language Menu */}
        <aside className="hidden lg:block w-64 flex-shrink-0">
          <div className="bg-white dark:bg-neutral-900 rounded-lg shadow p-4">
            {renderLanguageMenu()}
          </div>
        </aside>

        {/* Mobile Language Selector */}
        <div className="lg:hidden mb-4">
          <div className="relative">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="w-full flex items-center justify-between px-4 py-2 bg-white dark:bg-neutral-900 rounded-lg shadow border border-neutral-200 dark:border-neutral-700"
            >
              <span className="flex items-center gap-2">
                <span className="text-lg">{currentLangConfig.flag}</span>
                <span className="font-medium">{currentLangConfig.name}</span>
              </span>
              {mobileMenuOpen ? (
                <XMarkIcon className="h-5 w-5 text-neutral-400" />
              ) : (
                <Bars3Icon className="h-5 w-5 text-neutral-400" />
              )}
            </button>
            
            {mobileMenuOpen && (
              <div className="absolute z-10 w-full mt-2 bg-white dark:bg-neutral-900 rounded-lg shadow-lg border border-neutral-200 dark:border-neutral-700 p-2">
                {renderLanguageMenu()}
              </div>
            )}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {renderTabNavigation()}
          <div className="bg-white dark:bg-neutral-800 rounded-lg shadow p-6 text-center">
            <Icon className="h-12 w-12 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-semibold mb-2">{title}</h3>
            <p className="text-gray-600 dark:text-gray-400">
              {title} for {currentLangConfig.name} will be available soon.
            </p>
          </div>
        </div>
      </div>
    )
  }

  if (mode === 'characters' && currentLangConfig?.hasCharacters) {
    // Show characters using the same vocabulary component, but for character type
    return (
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Desktop Language Menu */}
        <aside className="hidden lg:block w-64 flex-shrink-0">
          <div className="bg-white dark:bg-neutral-900 rounded-lg shadow p-4">
            {renderLanguageMenu()}
          </div>
        </aside>

        {/* Mobile Language Selector */}
        <div className="lg:hidden mb-4">
          <div className="relative">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="w-full flex items-center justify-between px-4 py-2 bg-white dark:bg-neutral-900 rounded-lg shadow border border-neutral-200 dark:border-neutral-700"
            >
              <span className="flex items-center gap-2">
                <span className="text-lg">{currentLangConfig.flag}</span>
                <span className="font-medium">{currentLangConfig.name}</span>
              </span>
              {mobileMenuOpen ? (
                <XMarkIcon className="h-5 w-5 text-neutral-400" />
              ) : (
                <Bars3Icon className="h-5 w-5 text-neutral-400" />
              )}
            </button>
            
            {mobileMenuOpen && (
              <div className="absolute z-10 w-full mt-2 bg-white dark:bg-neutral-900 rounded-lg shadow-lg border border-neutral-200 dark:border-neutral-700 p-2">
                {renderLanguageMenu()}
              </div>
            )}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {renderTabNavigation()}
          <LanguageVocabularyMode 
            selectedLanguage={currentLangConfig.code} 
            onBack={() => setMode('vocabulary')}
          />
        </div>
      </div>
    )
  }

  // Note: Listening and reading modes will now show questions like grammar mode
  // They fall through to the main question display below

  if (mode === 'grammar') {
    // Show coming soon for languages without grammar content
    if (!currentLangConfig?.hasGrammar) {
      return renderPlaceholder('Grammar Practice', PencilSquareIcon)
    }
    // Otherwise continue to show the grammar questions below
  }

  // Show questions for grammar, reading, and listening modes
  if (!currentQuestion || (mode !== 'grammar' && mode !== 'reading' && mode !== 'listening')) {
    return (
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Desktop Language Menu */}
        <aside className="hidden lg:block w-64 flex-shrink-0">
          <div className="bg-white dark:bg-neutral-900 rounded-lg shadow p-4">
            {renderLanguageMenu()}
          </div>
        </aside>

        {/* Mobile Language Selector */}
        <div className="lg:hidden mb-4">
          <div className="relative">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="w-full flex items-center justify-between px-4 py-2 bg-white dark:bg-neutral-900 rounded-lg shadow border border-neutral-200 dark:border-neutral-700"
            >
              <span className="flex items-center gap-2">
                <span className="text-lg">{currentLangConfig.flag}</span>
                <span className="font-medium">{currentLangConfig.name}</span>
              </span>
              {mobileMenuOpen ? (
                <XMarkIcon className="h-5 w-5 text-neutral-400" />
              ) : (
                <Bars3Icon className="h-5 w-5 text-neutral-400" />
              )}
            </button>
            
            {mobileMenuOpen && (
              <div className="absolute z-10 w-full mt-2 bg-white dark:bg-neutral-900 rounded-lg shadow-lg border border-neutral-200 dark:border-neutral-700 p-2">
                {renderLanguageMenu()}
              </div>
            )}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {renderTabNavigation()}
          <div className="bg-white dark:bg-neutral-800 rounded-lg shadow p-6 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Loading grammar questions...
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col lg:flex-row gap-6">
      {/* Desktop Language Menu */}
      <aside className="hidden lg:block w-64 flex-shrink-0">
        <div className="bg-white dark:bg-neutral-900 rounded-lg shadow p-4">
          {renderLanguageMenu()}
        </div>
      </aside>

      {/* Mobile Language Selector */}
      <div className="lg:hidden mb-4">
        <div className="relative">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="w-full flex items-center justify-between px-4 py-2 bg-white dark:bg-neutral-900 rounded-lg shadow border border-neutral-200 dark:border-neutral-700"
          >
            <span className="flex items-center gap-2">
              <span className="text-lg">{currentLangConfig.flag}</span>
              <span className="font-medium">{currentLangConfig.name}</span>
            </span>
            {mobileMenuOpen ? (
              <XMarkIcon className="h-5 w-5 text-neutral-400" />
            ) : (
              <Bars3Icon className="h-5 w-5 text-neutral-400" />
            )}
          </button>
          
          {mobileMenuOpen && (
            <div className="absolute z-10 w-full mt-2 bg-white dark:bg-neutral-900 rounded-lg shadow-lg border border-neutral-200 dark:border-neutral-700 p-2">
              {renderLanguageMenu()}
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        {renderTabNavigation()}

        {/* Grammar Question Card */}
        <div className="bg-white dark:bg-neutral-900 rounded-lg shadow-lg p-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-neutral-800 dark:text-neutral-200">
              {mode === 'listening' ? 'Listening Practice' : mode === 'reading' ? 'Reading Comprehension' : 'Grammar Practice'}
            </h2>
            <div className="flex gap-2">
              {currentQuestion && (
                <>
                  <button
                    onClick={() => setShowFlagModal(true)}
                    className="p-1.5 text-neutral-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                    title="Report an issue"
                  >
                    <FlagIcon className="h-4 w-4" />
                  </button>
                  <StudyListActions
                    itemType="language_question"
                    itemId={currentQuestion.id}
                    itemData={currentQuestion}
                    itemTitle={`${currentLangConfig.name}: ${currentQuestion.question_text.substring(0, 50)}...`}
                    className="px-2 py-1"
                  />
                </>
              )}
            </div>
          </div>

          {/* Stats */}
          <div className="flex justify-between items-center mb-4">
            <div className="text-xs text-neutral-600 dark:text-neutral-400">
              Question {currentIndex + 1} of {questionBank.length}
            </div>
            <div className="flex gap-2 text-xs">
              <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-2 py-1">
                <span className="font-bold text-primary-600">{sessionStats.total}</span>
                <span className="text-neutral-500 ml-1">today</span>
              </div>
              <div className="bg-neutral-50 dark:bg-neutral-800 rounded px-2 py-1">
                <span className="font-bold text-green-600">
                  {sessionStats.total > 0 ? Math.round((sessionStats.correct / sessionStats.total) * 100) : 0}%
                </span>
                <span className="text-neutral-500 ml-1">correct</span>
              </div>
            </div>
          </div>

          {!showResult ? (
            <>
              {/* Skip button */}
              <div className="flex justify-end mb-2">
                <SkipButton onSkip={skipQuestion} />
              </div>

              {/* Question */}
              <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/20 rounded-xl p-6 mb-4">
                {mode === 'listening' ? (
                  // For listening mode, show only play button for the passage
                  <div className="text-center">
                    <button
                      onClick={() => {
                        if (isPlaying) return // Prevent multiple plays
                        
                        // Extract the passage from the question text (it's in quotes)
                        const match = currentQuestion.question_text.match(/"([^"]+)"/)
                        const passage = match ? match[1] : ''
                        const questionPart = currentQuestion.question_text.split('\n\n').pop() || ''
                        
                        // Speak the passage first, then the question
                        if (hasLanguageVoice && passage) {
                          setIsPlaying(true)
                          speakWord(passage)
                          // After a delay, speak the question
                          const passageTime = passage.length * 50 // Rough estimate of speaking time
                          setTimeout(() => {
                            speakWord(questionPart)
                            // Reset playing state after both are done
                            setTimeout(() => {
                              setIsPlaying(false)
                            }, questionPart.length * 50)
                          }, passageTime)
                        }
                      }}
                      disabled={isPlaying}
                      className={`mx-auto p-6 rounded-full transition-all group ${
                        isPlaying 
                          ? 'bg-primary-400 cursor-not-allowed animate-pulse' 
                          : 'bg-primary-600 hover:bg-primary-700 hover:scale-105'
                      }`}
                      aria-label={isPlaying ? "Audio playing..." : "Play audio"}
                    >
                      <SpeakerWaveIcon className={`h-10 w-10 text-white transition-transform ${
                        isPlaying ? 'animate-pulse' : 'group-hover:scale-110'
                      }`} />
                    </button>
                    <p className="mt-4 text-lg font-medium text-neutral-800 dark:text-neutral-200">
                      {/* Show only the question part, not the passage */}
                      {currentQuestion.question_text.split('\n\n').pop()}
                    </p>
                    {isPlaying && (
                      <p className="mt-2 text-sm text-primary-600 dark:text-primary-400 animate-pulse">
                        Playing audio...
                      </p>
                    )}
                  </div>
                ) : (
                  // For reading and grammar modes, show the full text
                  <p className="text-lg font-medium text-neutral-800 dark:text-neutral-200 text-center">
                    {currentQuestion.question_text}
                  </p>
                )}
              </div>

              {/* Options */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {currentQuestion.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleAnswerSelect(index)}
                    className={`p-3 text-left border-2 rounded-lg transition-colors ${
                      selectedAnswer === index
                        ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20'
                        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/10'
                    }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </>
          ) : (
            <>
              {/* Result */}
              <div className={`mb-4 p-4 rounded-lg ${
                isCorrect 
                  ? 'bg-green-50 dark:bg-green-900/20' 
                  : 'bg-red-50 dark:bg-red-900/20'
              }`}>
                <div className="flex items-center justify-center gap-2 mb-2">
                  {isCorrect ? (
                    <CheckCircleIcon className="h-5 w-5 text-green-500" />
                  ) : (
                    <XCircleIcon className="h-5 w-5 text-red-500" />
                  )}
                  <span className="font-bold">
                    {isCorrect ? 'Correct!' : 'Incorrect'}
                  </span>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {currentQuestion.options[currentQuestion.correct_answer_index]}
                  </p>
                  {hasLanguageVoice && (
                    <button
                      onClick={() => speakWord(currentQuestion.options[currentQuestion.correct_answer_index])}
                      className="mt-2 p-2 hover:bg-green-100 dark:hover:bg-green-800/20 rounded-md transition-colors"
                    >
                      <SpeakerWaveIcon className="h-5 w-5 text-green-600 dark:text-green-400" />
                    </button>
                  )}
                </div>
              </div>

              {/* Explanation */}
              {currentQuestion.explanation && (
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 mb-4">
                  <p className="text-sm text-neutral-700 dark:text-neutral-300">
                    {currentQuestion.explanation}
                  </p>
                </div>
              )}

              <button
                onClick={nextQuestion}
                className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
              >
                Next Question →
              </button>
            </>
          )}
        </div>
      </div>

      {/* Flag Modal */}
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