import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { useSpellingBee } from '../contexts/SpellingBeeContext'
import { checkSpellingBeeTables, createSpellingBeeTables } from '../utils/createSpellingBeeTables'
import { replaceWordAndVariationsWithBlanks } from '../utils/vocabularyHelpers'
import { getVocabularyDifficultyLevels, getVocabularyDifficultyName } from '../services/difficultyLevels'
import { SpellingWordWithDifficulties, VocabularyDifficultyLevel } from '../types/difficultyLevels'
import { 
  CheckCircleIcon, 
  XCircleIcon,
  AcademicCapIcon,
  ClockIcon,
  FlagIcon,
  SpeakerWaveIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline'
import FlagContentModal from '../components/FlagContentModal'
import StudyListActions from '../components/StudyListActions'
import { studyListService } from '../services/studyListService'
import { StudyList } from '../types/database.types'

// Using the new type from difficultyLevels.ts
type SpellingWord = SpellingWordWithDifficulties;

interface VocabularyQuestion {
  word: SpellingWord
  options: string[]
  correctAnswer: string
}

const VocabularyTrainerPage: React.FC = () => {
  const { user } = useAuth()
  const { selectedDifficulties, setSelectedDifficulties, toggleDifficulty, useAdaptiveTesting, setUseAdaptiveTesting } = useSpellingBee()
  const [currentQuestion, setCurrentQuestion] = useState<VocabularyQuestion | null>(null)
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [difficultyLevels, setDifficultyLevels] = useState<VocabularyDifficultyLevel[]>([])
  const [selectedAnswer, setSelectedAnswer] = useState<string>('')
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(true)
  const [wordBank, setWordBank] = useState<SpellingWord[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [stats, setStats] = useState({ correct: 0, total: 0 })
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 })
  const [showFlagModal, setShowFlagModal] = useState(false)
  
  // Study list functionality
  const [studyLists, setStudyLists] = useState<StudyList[]>([])
  const [selectedStudyList, setSelectedStudyList] = useState<StudyList | null>(null)

  // Session storage keys
  const VOCAB_SESSION_KEY = 'vocabularyTrainerSession'

  // Helper function to organize and sort study lists
  const organizeStudyLists = (lists: StudyList[]) => {
    const vocabLists = lists.filter(list => list.name.includes('Vocab') && !list.name.includes('Grade'))
    const gradeLists = lists.filter(list => list.name.includes('Grade') && list.name.includes('Vocabulary'))
    
    // Sort existing vocab lists by name
    const sortedVocabLists = vocabLists.sort((a, b) => a.name.localeCompare(b.name))
    
    // Sort grade lists numerically (K, 1, 2, 3, etc.)
    const sortedGradeLists = gradeLists.sort((a, b) => {
      const extractGrade = (name: string) => {
        const match = name.match(/Grade\s+([K\d]+)/)
        if (!match) return 999
        return match[1] === 'K' ? 0 : parseInt(match[1])
      }
      return extractGrade(a.name) - extractGrade(b.name)
    })
    
    return { vocabLists: sortedVocabLists, gradeLists: sortedGradeLists }
  }

  // Load available study lists
  const loadStudyLists = useCallback(async () => {
    try {
      // Get public study lists for vocabulary (existing Vocab + Grade Level Vocabulary)
      const { data, error } = await supabase
        .from('study_lists')
        .select('*')
        .eq('is_public', true)
        .or('name.ilike.%Vocab%,name.ilike.%Vocabulary%')
        .order('name')

      if (error) {
        console.error('Error loading study lists:', error)
        return
      }

      // Also get user's personal study lists if logged in
      let userLists: StudyList[] = []
      if (user) {
        const userListsData = await studyListService.getUserStudyLists(user.id)
        userLists = userListsData.filter(list => 
          list.name.toLowerCase().includes('vocabulary') || 
          list.name.toLowerCase().includes('vocab')
        )
      }

      const allLists = [...(data || []), ...userLists]
      setStudyLists(allLists)
    } catch (error) {
      console.error('Error loading study lists:', error)
    }
  }, [user])

  // Save session state
  const saveSessionState = useCallback((question: VocabularyQuestion, index: number, selectedAnswer: string, showResult: boolean, isCorrect: boolean) => {
    const sessionState = {
      currentQuestion: question,
      currentIndex: index,
      selectedAnswer,
      showResult,
      isCorrect,
      timestamp: Date.now()
    }
    sessionStorage.setItem(VOCAB_SESSION_KEY, JSON.stringify(sessionState))
  }, [VOCAB_SESSION_KEY])

  // Load session state
  const loadSessionState = useCallback(() => {
    try {
      const saved = sessionStorage.getItem(VOCAB_SESSION_KEY)
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
  }, [VOCAB_SESSION_KEY])

  // Clear session state
  const clearSessionState = useCallback(() => {
    sessionStorage.removeItem(VOCAB_SESSION_KEY)
  }, [VOCAB_SESSION_KEY])

  const fetchWords = useCallback(async () => {
    try {
      // If a study list is selected, get words from the study list
      if (selectedStudyList) {
        const { data: studyListItems, error: studyListError } = await supabase
          .from('study_list_items')
          .select(`
            item_id,
            item_data,
            study_list:study_lists(name)
          `)
          .eq('study_list_id', selectedStudyList.id)
          .eq('item_type', 'spelling_word')

        if (studyListError) {
          console.error('Error fetching study list items:', studyListError)
          setLoading(false)
          return
        }

        if (studyListItems && studyListItems.length > 0) {
          const wordIds = studyListItems.map(item => item.item_id)
          
          const { data: words, error: wordsError } = await supabase
            .from('spelling_words')
            .select(`
              *,
              vocabulary_difficulty:vocabulary_difficulty_levels(id, name, description)
            `)
            .in('id', wordIds)

          if (wordsError) {
            console.error('Error fetching words from study list:', wordsError)
            setLoading(false)
            return
          }

          if (words && words.length > 0) {
            setWordBank(words)
            generateQuestion(words, 0)
            setCurrentIndex(0)
            setLoading(false)
            return
          }
        }
      }

      // Regular word fetching (existing logic)
      // Try to query with joins to the new difficulty tables first
      let query = supabase
        .from('spelling_words')
        .select(`
          *,
          vocabulary_difficulty:vocabulary_difficulty_levels(id, name, description)
        `)
        .order('vocabulary_difficulty_level')

      // Apply difficulty filter from selected difficulties
      if (selectedDifficulties.length > 0 && selectedDifficulties.length < 5) {
        // Try to filter by both new FK table and old name field for compatibility
        query = query.or(`vocabulary_difficulty.name.in.(${selectedDifficulties.join(',')}),vocabulary_difficulty_name.in.(${selectedDifficulties.join(',')})`)
      }

      let { data, error } = await query.limit(100)

      // If the join fails (tables don't exist yet), fall back to old structure
      if (error && error.message?.includes('vocabulary_difficulty_levels')) {
        console.log('New difficulty tables not found, using legacy structure...')
        
        query = supabase
          .from('spelling_words')
          .select('*')
          .order('vocabulary_difficulty_level')

        if (selectedDifficulties.length > 0 && selectedDifficulties.length < 5) {
          query = query.in('vocabulary_difficulty_name', selectedDifficulties)
        }

        const fallbackResult = await query.limit(100)
        data = fallbackResult.data
        error = fallbackResult.error
      }

      if (error) {
        console.error('Error fetching words:', error)
        setLoading(false)
        return
      }

      if (data && data.length > 0) {
        // For words that don't have difficulty names, try to get them from the service
        const wordsWithNames = await Promise.all(
          data.map(async (word) => {
            if (!word.vocabulary_difficulty_name && word.vocabulary_difficulty_level) {
              const difficultyName = await getVocabularyDifficultyName(word.vocabulary_difficulty_level)
              return { ...word, vocabulary_difficulty_name: difficultyName }
            }
            return word
          })
        )

        // Shuffle words for variety
        const shuffled = [...wordsWithNames].sort(() => Math.random() - 0.5)
        setWordBank(shuffled)
        
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
          if (savedSession.showResult) {
            setTimeout(() => {
              speakWord(savedSession.currentQuestion.word.word)
            }, 1000) // Longer delay for page restoration
          }
        } else {
          // Start fresh
          generateQuestion(shuffled, 0)
          setCurrentIndex(0)
        }
      }
    } catch (error) {
      console.error('Error fetching words:', error)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedDifficulties, selectedStudyList, loadSessionState])

  // Helper function to extract primary language origin from etymology
  const getLanguageOrigin = (etymology: string | undefined): string => {
    if (!etymology) return 'unknown'
    
    const lowerEtymology = etymology.toLowerCase()
    
    // Common language patterns in etymology
    const languagePatterns = [
      { pattern: /\b(japanese|japan)\b/, origin: 'japanese' },
      { pattern: /\b(chinese|china|mandarin|cantonese)\b/, origin: 'chinese' },
      { pattern: /\b(french|france|old french|middle french)\b/, origin: 'french' },
      { pattern: /\b(german|germanic|old german|middle german)\b/, origin: 'german' },
      { pattern: /\b(spanish|spain|castilian)\b/, origin: 'spanish' },
      { pattern: /\b(italian|italy)\b/, origin: 'italian' },
      { pattern: /\b(greek|ancient greek|modern greek)\b/, origin: 'greek' },
      { pattern: /\b(latin|roman)\b/, origin: 'latin' },
      { pattern: /\b(arabic|arab)\b/, origin: 'arabic' },
      { pattern: /\b(sanskrit|hindi|urdu|persian)\b/, origin: 'indo-iranian' },
      { pattern: /\b(dutch|netherlands|flemish)\b/, origin: 'dutch' },
      { pattern: /\b(russian|slavic|polish|czech)\b/, origin: 'slavic' },
      { pattern: /\b(portuguese|portugal)\b/, origin: 'portuguese' },
      { pattern: /\b(hebrew|yiddish)\b/, origin: 'hebrew' },
      { pattern: /\b(turkish|ottoman)\b/, origin: 'turkish' },
      { pattern: /\b(english|anglo|old english|middle english)\b/, origin: 'english' },
      { pattern: /\b(norse|norwegian|swedish|danish|iceland)\b/, origin: 'norse' },
    ]
    
    for (const { pattern, origin } of languagePatterns) {
      if (pattern.test(lowerEtymology)) {
        return origin
      }
    }
    
    return 'other'
  }

  const generateQuestion = (words: SpellingWord[], index: number) => {
    if (!words || words.length === 0) return

    const targetWord = words[index]
    const targetOrigin = getLanguageOrigin(targetWord.etymology)
    
    // First priority: words from same etymology/origin
    const sameOrigin = words.filter(w => 
      w.id !== targetWord.id && 
      getLanguageOrigin(w.etymology) === targetOrigin &&
      targetOrigin !== 'unknown' && targetOrigin !== 'other'
    )
    
    // Second priority: words from same difficulty level
    const sameLevel = words.filter(w => 
      w.id !== targetWord.id && 
      w.vocabulary_difficulty_name === targetWord.vocabulary_difficulty_name
    )
    
    // Third priority: all other words
    const allOthers = words.filter(w => w.id !== targetWord.id)
    
    let alternatives: SpellingWord[] = []
    
    // Try to get 3 alternatives from same origin first
    if (sameOrigin.length >= 3) {
      alternatives = [...sameOrigin].sort(() => Math.random() - 0.5).slice(0, 3)
    } 
    // If not enough same origin, mix same origin with same difficulty
    else if (sameOrigin.length > 0) {
      const remainingNeeded = 3 - sameOrigin.length
      const additionalOptions = sameLevel
        .filter(w => !sameOrigin.find(sw => sw.id === w.id))
        .sort(() => Math.random() - 0.5)
        .slice(0, remainingNeeded)
      alternatives = [...sameOrigin, ...additionalOptions]
    }
    // Fall back to same difficulty level
    else if (sameLevel.length >= 3) {
      alternatives = [...sameLevel].sort(() => Math.random() - 0.5).slice(0, 3)
    }
    // Final fallback to any words
    else {
      alternatives = [...allOthers].sort(() => Math.random() - 0.5).slice(0, 3)
    }
    
    const wrongOptions = alternatives.map(w => w.word)
    
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

  // Load difficulty levels on component mount
  useEffect(() => {
    const loadDifficultyLevels = async () => {
      try {
        const levels = await getVocabularyDifficultyLevels()
        setDifficultyLevels(levels)
      } catch (error) {
        console.error('Error loading vocabulary difficulty levels:', error)
      }
    }
    loadDifficultyLevels()
  }, [])

  // Load study lists on mount and when user changes
  useEffect(() => {
    loadStudyLists()
  }, [loadStudyLists])

  // Refetch words when selected difficulties or study list change
  useEffect(() => {
    setLoading(true)
    fetchWords()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedDifficulties, selectedStudyList])

  const handleAnswerSelect = (answer: string) => {
    if (showResult) return
    setSelectedAnswer(answer)
    // Save session state when answer is selected
    if (currentQuestion) {
      saveSessionState(currentQuestion, currentIndex, answer, showResult, isCorrect)
    }
  }

  const handleSubmit = async () => {
    if (!currentQuestion || !selectedAnswer) return

    const correct = selectedAnswer === currentQuestion.correctAnswer
    setIsCorrect(correct)
    setShowResult(true)

    // Save session state when result is shown
    saveSessionState(currentQuestion, currentIndex, selectedAnswer, true, correct)

    // Auto-play audio for the correct word when result is shown
    setTimeout(() => {
      speakWord(currentQuestion.word.word)
    }, 500) // Small delay to let UI update first

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
    // Clear session state when moving to next question
    clearSessionState()
    
    const nextIndex = (currentIndex + 1) % wordBank.length
    setCurrentIndex(nextIndex)
    generateQuestion(wordBank, nextIndex)
    setSelectedAnswer('')
    setShowResult(false)
  }

  const speakWord = (word: string) => {
    if ('speechSynthesis' in window) {
      // Cancel any previous speech
      window.speechSynthesis.cancel()
      
      const utterance = new SpeechSynthesisUtterance(word)
      utterance.rate = 0.8
      utterance.volume = 0.8
      utterance.pitch = 1.0
      
      window.speechSynthesis.speak(utterance)
    }
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

            {/* Study List Selection */}
            {studyLists.length > 0 && (
              <div className="flex items-center gap-1">
                <span className="text-xs font-medium text-neutral-700 dark:text-neutral-300">Study List:</span>
                <div className="relative">
                  <select
                    value={selectedStudyList?.id || ''}
                    onChange={(e) => {
                      const list = studyLists.find(l => l.id === e.target.value) || null
                      setSelectedStudyList(list)
                      setCurrentIndex(0)
                      setCurrentQuestion(null)
                      setSelectedAnswer('')
                      setShowResult(false)
                    }}
                    className="bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 px-2 py-1 rounded text-xs border-0 focus:ring-1 focus:ring-neutral-500 appearance-none pr-6"
                  >
                    <option value="">All Words</option>
                    {(() => {
                      const { vocabLists, gradeLists } = organizeStudyLists(studyLists)
                      return (
                        <>
                          {vocabLists.length > 0 && (
                            <optgroup label="Vocabulary Lists">
                              {vocabLists.map((list) => (
                                <option key={list.id} value={list.id}>
                                  {list.name}
                                </option>
                              ))}
                            </optgroup>
                          )}
                          {gradeLists.length > 0 && (
                            <optgroup label="Grade Level Lists">
                              {gradeLists.map((list) => (
                                <option key={list.id} value={list.id}>
                                  {list.name}
                                </option>
                              ))}
                            </optgroup>
                          )}
                        </>
                      )
                    })()}
                  </select>
                  <ChevronDownIcon className="absolute right-1 top-1/2 transform -translate-y-1/2 h-3 w-3 text-neutral-500 dark:text-neutral-400 pointer-events-none" />
                </div>
              </div>
            )}

            {/* Difficulty Selection */}
            {!useAdaptiveTesting && !selectedStudyList && (
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
                  "{replaceWordAndVariationsWithBlanks(currentQuestion.word.example_sentence, currentQuestion.word.word)}"
                </p>
              </div>
            </div>

            <div className="text-center mb-2 space-y-1">
              <div className="flex justify-center items-center gap-2 sm:gap-3 text-xs">
                {currentQuestion.word.vocabulary_difficulty_name && (
                  <span className={`px-1 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-medium ${
                    currentQuestion.word.vocabulary_difficulty_name === 'Beginner' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                    currentQuestion.word.vocabulary_difficulty_name === 'Elementary' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                    currentQuestion.word.vocabulary_difficulty_name === 'Intermediate' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                    currentQuestion.word.vocabulary_difficulty_name === 'Advanced' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' :
                    'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                  }`}>
                    {currentQuestion.word.vocabulary_difficulty_name}
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
              className="w-full py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 active:bg-primary-900 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors text-sm font-semibold shadow-md"
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
                <div className="flex flex-col items-center gap-3">
                  <div className="flex items-center gap-2">
                    <CheckCircleIcon className="h-5 w-5 text-green-500" />
                    <span className="text-sm font-bold text-green-700 dark:text-green-400">
                      Correct!
                    </span>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                      {replaceWordAndVariationsWithBlanks(currentQuestion.word.definition, currentQuestion.word.word)}
                    </p>
                  </div>
                  <div className="flex items-center justify-center gap-3">
                    <span className="text-5xl font-bold text-green-700 dark:text-green-400">
                      {currentQuestion.word.word}
                    </span>
                    <button
                      onClick={() => speakWord(currentQuestion.word.word)}
                      className="p-1 hover:bg-green-100 dark:hover:bg-green-800/20 rounded-md transition-colors"
                      title="Hear pronunciation"
                    >
                      <SpeakerWaveIcon className="h-4 w-4 text-green-600 dark:text-green-400" />
                    </button>
                  </div>
                </div>
              ) : (
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <XCircleIcon className="h-5 w-5 text-red-500" />
                    <span className="text-sm font-bold text-red-700 dark:text-red-400">Incorrect</span>
                  </div>
                  <div className="text-center mb-2">
                    <p className="text-sm text-neutral-600 dark:text-neutral-400">
                      {replaceWordAndVariationsWithBlanks(currentQuestion.word.definition, currentQuestion.word.word)}
                    </p>
                  </div>
                  <div className="flex items-center justify-center gap-3">
                    <div className="text-xl text-red-600 dark:text-red-400">{selectedAnswer}</div>
                    <div className="text-lg text-neutral-500">→</div>
                    <div className="text-3xl font-mono text-green-600 dark:text-green-400 font-bold">{currentQuestion.word.word}</div>
                    <button
                      onClick={() => speakWord(currentQuestion.word.word)}
                      className="p-1 hover:bg-green-100 dark:hover:bg-green-800/20 rounded-md transition-colors"
                      title="Hear pronunciation"
                    >
                      <SpeakerWaveIcon className="h-4 w-4 text-green-600 dark:text-green-400" />
                    </button>
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
              className="w-full py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 active:bg-primary-900 transition-colors text-sm font-semibold shadow-md"
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