import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { checkSpellingBeeTables, createSpellingBeeTables } from '../utils/createSpellingBeeTables'
import { 
  SpeakerWaveIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  ArrowPathIcon,
  InformationCircleIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline'

interface SpellingWord {
  id: string
  word: string
  definition: string
  example_sentence: string
  difficulty_level: number
  etymology?: string
  pronunciation_tips?: string
  common_misspellings?: string[]
  audio_url?: string
}


const SpellingBeePage: React.FC = () => {
  const { user } = useAuth()
  const [currentWord, setCurrentWord] = useState<SpellingWord | null>(null)
  const [userInput, setUserInput] = useState('')
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(true)
  const [wordBank, setWordBank] = useState<SpellingWord[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [stats, setStats] = useState({ correct: 0, total: 0 })
  const [showEtymology, setShowEtymology] = useState(false)

  const fetchWords = useCallback(async () => {
    try {
      const { data, error } = await supabase
        .from('spelling_words')
        .select('*')
        .order('difficulty_level')
        .limit(50)

      if (error) {
        console.error('Error fetching words:', error)
        setLoading(false)
        return
      }

      if (data && data.length > 0) {
        setWordBank(data)
        setCurrentWord(data[0])
      }
    } catch (error) {
      console.error('Error fetching words:', error)
    } finally {
      setLoading(false)
    }
  }, [])


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

  const playAudio = async () => {
    if (!currentWord) return

    // Use Web Speech API for text-to-speech
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(currentWord.word)
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
    } else {
      alert('Text-to-speech is not supported in your browser')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!currentWord || !userInput.trim()) return

    const correct = userInput.trim().toLowerCase() === currentWord.word.toLowerCase()
    setIsCorrect(correct)
    setShowResult(true)

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
    setShowEtymology(false)
  }

  const repeatWord = () => {
    playAudio()
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
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">
          <span className="bg-gradient-to-r from-primary-600 to-gold-500 bg-clip-text text-transparent">
            Spelling Bee Practice
          </span>
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400">
          Listen to the word, understand its meaning, and spell it correctly!
        </p>
      </div>

      {/* Stats Bar */}
      {user && stats.total > 0 && (
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-neutral-600 dark:text-neutral-400">
              Session Progress
            </span>
            <div className="flex items-center gap-4">
              <span className="text-sm">
                <CheckCircleIcon className="h-4 w-4 inline text-green-500 mr-1" />
                {stats.correct} correct
              </span>
              <span className="text-sm">
                <XCircleIcon className="h-4 w-4 inline text-red-500 mr-1" />
                {stats.total - stats.correct} incorrect
              </span>
              <span className="text-sm font-medium">
                {Math.round((stats.correct / stats.total) * 100)}% accuracy
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Main Spelling Card */}
      <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
        {!showResult ? (
          <>
            {/* Audio Controls */}
            <div className="text-center mb-8">
              <button
                onClick={playAudio}
                className="inline-flex items-center gap-3 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                <SpeakerWaveIcon className="h-6 w-6" />
                Play Word
              </button>
              <button
                onClick={repeatWord}
                className="ml-4 inline-flex items-center gap-2 px-4 py-3 bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
              >
                <ArrowPathIcon className="h-5 w-5" />
                Repeat
              </button>
            </div>

            {/* Context Information */}
            <div className="space-y-4 mb-8">
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
                <h3 className="font-semibold text-sm mb-2 flex items-center gap-2">
                  <InformationCircleIcon className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                  Definition
                </h3>
                <p className="text-sm text-neutral-700 dark:text-neutral-300">
                  {currentWord.definition}
                </p>
              </div>

              <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-4">
                <h3 className="font-semibold text-sm mb-2">Example Sentence</h3>
                <p className="text-sm text-neutral-700 dark:text-neutral-300 italic">
                  "{currentWord.example_sentence}"
                </p>
              </div>

              <div className="text-center text-sm text-neutral-500">
                Difficulty: {'⭐'.repeat(currentWord.difficulty_level)}
              </div>
            </div>

            {/* Input Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  Type your spelling:
                </label>
                <input
                  type="text"
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  className="w-full px-4 py-3 text-xl font-mono border-2 border-neutral-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-neutral-800"
                  placeholder="Enter spelling here..."
                  autoFocus
                />
              </div>
              <button
                type="submit"
                disabled={!userInput.trim()}
                className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors"
              >
                Submit Answer
              </button>
            </form>
          </>
        ) : (
          <>
            {/* Result Display */}
            <div className={`text-center mb-8 p-6 rounded-lg ${
              isCorrect 
                ? 'bg-green-50 dark:bg-green-900/20' 
                : 'bg-red-50 dark:bg-red-900/20'
            }`}>
              {isCorrect ? (
                <>
                  <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
                  <h2 className="text-2xl font-bold text-green-700 dark:text-green-400 mb-2">
                    Correct!
                  </h2>
                  <p className="text-lg">Great job spelling "{currentWord.word}"!</p>
                </>
              ) : (
                <>
                  <XCircleIcon className="h-16 w-16 text-red-500 mx-auto mb-4" />
                  <h2 className="text-2xl font-bold text-red-700 dark:text-red-400 mb-2">
                    Incorrect
                  </h2>
                  <div className="space-y-2">
                    <p className="text-lg">
                      Your spelling: <span className="font-mono text-red-600 dark:text-red-400">{userInput}</span>
                    </p>
                    <p className="text-lg">
                      Correct spelling: <span className="font-mono text-green-600 dark:text-green-400 font-bold">{currentWord.word}</span>
                    </p>
                  </div>
                </>
              )}
            </div>

            {/* Learning Tips */}
            <div className="space-y-4 mb-8">
              {currentWord.pronunciation_tips && (
                <div className="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-4">
                  <h3 className="font-semibold text-sm mb-2 flex items-center gap-2">
                    <AcademicCapIcon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
                    Memory Tip
                  </h3>
                  <p className="text-sm text-neutral-700 dark:text-neutral-300">
                    {currentWord.pronunciation_tips}
                  </p>
                </div>
              )}

              {/* Etymology Section */}
              {currentWord.etymology && (
                <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-4">
                  <button
                    onClick={() => setShowEtymology(!showEtymology)}
                    className="w-full text-left"
                  >
                    <h3 className="font-semibold text-sm mb-2 flex items-center justify-between">
                      <span>Word Origin & Etymology</span>
                      <span className="text-xs text-neutral-500">
                        {showEtymology ? 'Hide' : 'Show'}
                      </span>
                    </h3>
                  </button>
                  {showEtymology && (
                    <p className="text-sm text-neutral-700 dark:text-neutral-300 mt-2">
                      {currentWord.etymology}
                    </p>
                  )}
                </div>
              )}

              {currentWord.common_misspellings && currentWord.common_misspellings.length > 0 && (
                <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-4">
                  <h3 className="font-semibold text-sm mb-2">Common Misspellings to Avoid</h3>
                  <div className="flex flex-wrap gap-2">
                    {currentWord.common_misspellings.map((spelling, idx) => (
                      <span 
                        key={idx}
                        className="px-2 py-1 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 rounded text-sm font-mono line-through"
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
              className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Next Word →
            </button>
          </>
        )}
      </div>

      {/* Progress Indicator */}
      <div className="text-center text-sm text-neutral-500">
        Word {currentIndex + 1} of {wordBank.length}
      </div>
    </div>
  )
}

export default SpellingBeePage