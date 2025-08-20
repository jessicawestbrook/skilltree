import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { useSpellingBee } from '../contexts/SpellingBeeContext'
import { checkSpellingBeeTables, createSpellingBeeTables } from '../utils/createSpellingBeeTables'
import { replaceWordAndVariationsWithBlanks } from '../utils/vocabularyHelpers'
import { 
  SpeakerWaveIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  InformationCircleIcon,
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


const SpellingBeePage: React.FC = () => {
  const { user } = useAuth()
  const { selectedDifficulties, setSelectedDifficulties, toggleDifficulty, useAdaptiveTesting, setUseAdaptiveTesting } = useSpellingBee()
  const [currentWord, setCurrentWord] = useState<SpellingWord | null>(null)
  const [userInput, setUserInput] = useState('')
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
        setCurrentWord(shuffled[0])
        setCurrentIndex(0)
      }
    } catch (error) {
      console.error('Error fetching words:', error)
    } finally {
      setLoading(false)
    }
  }, [selectedDifficulties])


  const fetchUserStats = useCallback(async () => {
    if (!user) return

    try {
      const { data, error } = await supabase
        .from('user_spelling_attempts')
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

  const initializeSpellingBee = useCallback(async () => {
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
    initializeSpellingBee()
  }, [initializeSpellingBee])

  // Refetch words when selected difficulties change
  useEffect(() => {
    setLoading(true)
    fetchWords()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedDifficulties])

  // Play word when it changes (including initial load)
  useEffect(() => {
    if (currentWord && !showResult) {
      // Small delay to ensure page is ready
      const timer = setTimeout(() => {
        playAudioForWord(currentWord)
      }, 1000)
      return () => clearTimeout(timer)
    }
  }, [currentWord, showResult])

  const playAudio = async () => {
    if (!currentWord) return
    playAudioForWord(currentWord)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!currentWord || !userInput.trim()) return

    const correct = userInput.trim().toLowerCase() === currentWord.word.toLowerCase()
    setIsCorrect(correct)
    setShowResult(true)

    // Update session stats
    setSessionStats(prev => ({
      correct: prev.correct + (correct ? 1 : 0),
      total: prev.total + 1
    }))

    // Save attempt if user is logged in
    if (user) {
      await supabase.from('user_spelling_attempts').insert({
        user_id: user.id,
        word_id: currentWord.id,
        correct,
        user_spelling: userInput.trim()
      })

      setStats(prev => ({
        correct: prev.correct + (correct ? 1 : 0),
        total: prev.total + 1
      }))
    }
  }

  const nextWord = () => {
    const nextIndex = (currentIndex + 1) % wordBank.length
    setCurrentIndex(nextIndex)
    setCurrentWord(wordBank[nextIndex])
    setUserInput('')
    setShowResult(false)
    
    // Automatically play the next word
    setTimeout(() => {
      if (wordBank[nextIndex]) {
        playAudioForWord(wordBank[nextIndex])
      }
    }, 500) // Small delay for better UX
  }
  
  const playAudioForWord = (word: SpellingWord) => {
    if (!word) return

    // Use Web Speech API for text-to-speech
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(word.word)
      utterance.rate = 0.8 // Slower for spelling
      utterance.pitch = 1
      utterance.volume = 1
      
      // Try to use a clearer voice if available
      const voices = speechSynthesis.getVoices()
      const englishVoice = voices.find(voice => 
        voice.lang.startsWith('en-') && voice.name.includes('Google')
      ) || voices.find(voice => voice.lang.startsWith('en-'))
      
      if (englishVoice) {
        utterance.voice = englishVoice
      }
      
      speechSynthesis.speak(utterance)
    }
  }


  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!currentWord) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6 text-center">
          <p className="text-lg">No spelling words available. Please check back later!</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-1 sm:p-4 space-y-2 sm:space-y-6">
      {/* Page Title */}
      <div className="text-center py-1 sm:py-0">
        <h1 className="text-xl sm:text-3xl font-bold">Spelling Bee Practice</h1>
      </div>

      {/* Combined Spelling Practice Card */}
      <div className="bg-white dark:bg-neutral-900 rounded-lg sm:rounded-xl shadow-lg p-2 sm:p-6 relative">
        {/* Action Buttons */}
        {currentWord && (
          <div className="absolute top-2 right-2 flex items-center gap-1 z-10">
            <StudyListActions
              itemType="spelling_word"
              itemId={currentWord.id}
              itemData={currentWord}
              itemTitle={`Spelling: ${currentWord.word}`}
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
        <div className="flex justify-between items-start mb-1 sm:mb-2">
          {/* Practice Settings */}
          <div className="flex flex-col lg:flex-row gap-1 sm:gap-2 items-start lg:items-center flex-1 mr-2 sm:mr-0">
            {/* Adaptive Testing Toggle */}
            <div className="flex items-center gap-1">
              <label className="flex items-center gap-1 cursor-pointer">
                <input
                  type="checkbox"
                  checked={useAdaptiveTesting}
                  onChange={(e) => setUseAdaptiveTesting(e.target.checked)}
                  className="rounded border-neutral-300 text-primary-600 focus:ring-primary-500 h-3 w-3"
                />
                <span className="text-xs font-medium">Adaptive Testing</span>
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
            {/* Audio Controls */}
            <div className="text-center mb-2 sm:mb-4">
              <button
                onClick={playAudio}
                className="inline-flex items-center gap-3 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-lg font-medium"
              >
                <SpeakerWaveIcon className="h-6 w-6" />
                Play Word
              </button>
            </div>

            {/* Context Information - More Compact */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 sm:gap-3 mb-2 sm:mb-4">
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded p-1.5 sm:p-3">
                <h3 className="font-semibold text-xs mb-0.5 sm:mb-1 flex items-center gap-1">
                  <InformationCircleIcon className="h-3 w-3 sm:h-4 sm:w-4 text-blue-600 dark:text-blue-400" />
                  Definition
                </h3>
                <p className="text-xs text-neutral-700 dark:text-neutral-300">
                  {replaceWordAndVariationsWithBlanks(currentWord.definition, currentWord.word)}
                </p>
              </div>

              <div className="bg-gold-50 dark:bg-gold-900/20 rounded p-1.5 sm:p-3">
                <h3 className="font-semibold text-xs mb-0.5 sm:mb-1">Example</h3>
                <p className="text-xs text-neutral-700 dark:text-neutral-300 italic">
                  "{currentWord.example_sentence}"
                </p>
              </div>
            </div>

            <div className="text-center mb-1 sm:mb-4 space-y-1">
              <div className="flex justify-center items-center gap-2 sm:gap-3 text-xs">
                {currentWord.difficulty_name && (
                  <span className={`px-1 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-medium ${
                    currentWord.difficulty_name === 'Beginner' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                    currentWord.difficulty_name === 'Elementary' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                    currentWord.difficulty_name === 'Intermediate' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                    currentWord.difficulty_name === 'Advanced' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' :
                    'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                  }`}>
                    {currentWord.difficulty_name}
                  </span>
                )}
                {currentWord.part_of_speech && (
                  <span className="text-neutral-600 dark:text-neutral-400 italic">
                    {currentWord.part_of_speech}
                  </span>
                )}
              </div>
            </div>

            {/* Input Form */}
            <form onSubmit={handleSubmit} className="space-y-1.5 sm:space-y-3">
              <div>
                <label className="block text-xs font-medium mb-0.5 sm:mb-1">
                  Type your spelling:
                </label>
                <input
                  type="text"
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  className="w-full px-2 sm:px-3 py-1.5 sm:py-2 text-base sm:text-lg font-mono border-2 border-neutral-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-neutral-800"
                  placeholder=""
                  autoFocus
                />
              </div>
              <button
                type="submit"
                disabled={!userInput.trim()}
                className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors text-sm"
              >
                Submit
              </button>
            </form>
          </>
        ) : (
          <>
            {/* Result Display - More Compact */}
            <div className={`mb-3 p-2 rounded-lg ${
              isCorrect 
                ? 'bg-green-50 dark:bg-green-900/20' 
                : 'bg-red-50 dark:bg-red-900/20'
            }`}>
              {isCorrect ? (
                <div className="flex items-center justify-center gap-2">
                  <CheckCircleIcon className="h-5 w-5 text-green-500" />
                  <span className="text-sm font-bold text-green-700 dark:text-green-400">
                    Correct! "{currentWord.word}"
                  </span>
                </div>
              ) : (
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <XCircleIcon className="h-5 w-5 text-red-500" />
                    <span className="text-sm font-bold text-red-700 dark:text-red-400">Incorrect</span>
                  </div>
                  <div className="text-xs">
                    <span className="text-red-600 dark:text-red-400">{userInput}</span>
                    <span className="mx-2">→</span>
                    <span className="font-mono text-green-600 dark:text-green-400 font-bold">{currentWord.word}</span>
                  </div>
                </div>
              )}
              {currentWord.pronunciation_guide && (
                <div className="text-center mt-2 pt-2 border-t border-neutral-200 dark:border-neutral-700">
                  <div className="text-xs text-neutral-600 dark:text-neutral-400">
                    Pronunciation: <span className="font-mono">{currentWord.pronunciation_guide}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Learning Tips - Compact */}
            <div className="space-y-2 mb-4">
              {(currentWord.memory_tips || currentWord.pronunciation_tips) && (
                <div className="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-3">
                  <h3 className="font-semibold text-xs mb-1 flex items-center gap-1">
                    <AcademicCapIcon className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    Memory Tips
                  </h3>
                  <p className="text-xs text-neutral-700 dark:text-neutral-300">
                    {currentWord.memory_tips || currentWord.pronunciation_tips}
                  </p>
                </div>
              )}

              {/* Etymology Section - Always Open */}
              {currentWord.etymology && (
                <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-3">
                  <h3 className="font-semibold text-xs mb-1">
                    Word Origin & Etymology
                    {currentWord.etymology_source && (
                      <span className="ml-2 text-neutral-500 font-normal">
                        (Source: {currentWord.etymology_source})
                      </span>
                    )}
                  </h3>
                  <p className="text-xs text-neutral-700 dark:text-neutral-300">
                    {currentWord.etymology}
                  </p>
                </div>
              )}


              {currentWord.common_misspellings && currentWord.common_misspellings.length > 0 && (
                <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-3">
                  <h3 className="font-semibold text-xs mb-1">Common Misspellings</h3>
                  <div className="flex flex-wrap gap-1">
                    {currentWord.common_misspellings.map((spelling, idx) => (
                      <span 
                        key={idx}
                        className="px-1 py-0.5 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 rounded text-xs font-mono line-through"
                      >
                        {spelling}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <button
              onClick={nextWord}
              className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm"
            >
              Next Word →
            </button>
          </>
        )}
      </div>

      {/* Flag Content Modal */}
      {showFlagModal && currentWord && (
        <FlagContentModal
          isOpen={showFlagModal}
          onClose={() => setShowFlagModal(false)}
          contentType="question"
          contentId={currentWord.id}
          contentTitle={`Spelling: ${currentWord.word}`}
        />
      )}
    </div>
  )
}

export default SpellingBeePage