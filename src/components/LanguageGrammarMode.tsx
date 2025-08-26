import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import {
  CheckCircleIcon,
  XCircleIcon,
  SpeakerWaveIcon,
  FlagIcon
} from '@heroicons/react/24/outline'
import SkipButton from './flashcards/SkipButton'
import StudyListActions from './StudyListActions'
import FlagContentModal from './FlagContentModal'

interface GrammarQuestion {
  id: string
  question_text: string
  options: string[]
  correct_answer: number
  explanation: string
  difficulty: string
}

interface LanguageGrammarModeProps {
  selectedLanguage: string
  languageName: string
  onBack?: () => void
}

const LanguageGrammarMode: React.FC<LanguageGrammarModeProps> = ({ selectedLanguage, languageName, onBack }) => {
  const { user } = useAuth()
  const [questions, setQuestions] = useState<GrammarQuestion[]>([])
  const [currentQuestion, setCurrentQuestion] = useState<GrammarQuestion | null>(null)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0 })
  const [loading, setLoading] = useState(true)
  const [showFlagModal, setShowFlagModal] = useState(false)

  // Load Spanish grammar questions
  const loadGrammarQuestions = useCallback(async () => {
    setLoading(true)
    try {
      // Load Spanish verb conjugation questions from the questions table
      const { data, error } = await supabase
        .from('questions')
        .select('*')
        .like('question_text', '%Fill in the blank%')
        .like('explanation', '%conjugation%')
        .order('created_at', { ascending: false })
        .limit(100)

      if (error) throw error

      if (data && data.length > 0) {
        // Shuffle questions for variety
        const shuffled = [...data].sort(() => Math.random() - 0.5)
        setQuestions(shuffled)
        setCurrentQuestion(shuffled[0])
        setCurrentIndex(0)
      }
    } catch (error) {
      console.error('Error loading grammar questions:', error)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (selectedLanguage === 'es') {
      loadGrammarQuestions()
    }
  }, [selectedLanguage, loadGrammarQuestions])

  const handleAnswerSelect = (answerIndex: number) => {
    if (showResult) return
    setSelectedAnswer(answerIndex)
    // Auto-submit after selection
    setTimeout(() => {
      handleSubmit(answerIndex)
    }, 100)
  }

  const handleSubmit = async (answerIndex?: number) => {
    if (!currentQuestion) return
    const answer = answerIndex !== undefined ? answerIndex : selectedAnswer
    if (answer === null) return

    const correct = answer === currentQuestion.correct_answer
    setIsCorrect(correct)
    setShowResult(true)

    // Update session stats
    setSessionStats(prev => ({
      correct: prev.correct + (correct ? 1 : 0),
      total: prev.total + 1
    }))

    // Record attempt if user is logged in
    if (user) {
      try {
        await supabase.from('user_question_attempts').insert({
          user_id: user.id,
          question_id: currentQuestion.id,
          selected_answer: answer,
          is_correct: correct,
          time_taken_seconds: 0
        })
      } catch (error) {
        console.error('Error recording attempt:', error)
      }
    }
  }

  const nextQuestion = () => {
    const nextIndex = (currentIndex + 1) % questions.length
    setCurrentIndex(nextIndex)
    setCurrentQuestion(questions[nextIndex])
    setSelectedAnswer(null)
    setShowResult(false)
  }

  const skipQuestion = () => {
    const nextIndex = (currentIndex + 1) % questions.length
    setCurrentIndex(nextIndex)
    setCurrentQuestion(questions[nextIndex])
    setSelectedAnswer(null)
    setShowResult(false)
  }

  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel()
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = selectedLanguage
      utterance.rate = 0.8
      window.speechSynthesis.speak(utterance)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!currentQuestion || questions.length === 0) {
    return (
      <div className="bg-white dark:bg-neutral-900 rounded-lg shadow p-6 text-center">
        <p className="text-gray-600 dark:text-gray-400">
          No grammar questions available for {languageName} yet.
        </p>
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-neutral-900 rounded-lg shadow-lg p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-neutral-800 dark:text-neutral-200">
          Grammar Practice
        </h2>
        <div className="flex gap-2">
          <button
            onClick={() => setShowFlagModal(true)}
            className="p-1.5 text-neutral-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
            title="Report an issue"
          >
            <FlagIcon className="h-4 w-4" />
          </button>
          <StudyListActions
            itemType="question"
            itemId={currentQuestion.id}
            itemData={currentQuestion}
            itemTitle={`${languageName} Grammar: ${currentQuestion.question_text.substring(0, 50)}...`}
            className="px-2 py-1"
          />
        </div>
      </div>

      {/* Stats */}
      <div className="flex justify-between items-center mb-4">
        <div className="text-xs text-neutral-600 dark:text-neutral-400">
          Question {currentIndex + 1} of {questions.length}
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
            <p className="text-lg font-medium text-neutral-800 dark:text-neutral-200 text-center">
              {currentQuestion.question_text}
            </p>
          </div>

          {/* Difficulty badge */}
          <div className="text-center mb-4">
            <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
              currentQuestion.difficulty === 'easy' 
                ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                : currentQuestion.difficulty === 'hard'
                ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
            }`}>
              {currentQuestion.difficulty}
            </span>
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
                {currentQuestion.options[currentQuestion.correct_answer]}
              </p>
              <button
                onClick={() => speakText(currentQuestion.options[currentQuestion.correct_answer])}
                className="mt-2 p-2 hover:bg-green-100 dark:hover:bg-green-800/20 rounded-md transition-colors"
                title="Hear pronunciation"
              >
                <SpeakerWaveIcon className="h-5 w-5 text-green-600 dark:text-green-400" />
              </button>
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

      {/* Flag Modal */}
      {showFlagModal && currentQuestion && (
        <FlagContentModal
          isOpen={showFlagModal}
          onClose={() => setShowFlagModal(false)}
          contentType="question"
          contentId={currentQuestion.id}
          contentTitle={`Grammar: ${currentQuestion.question_text}`}
        />
      )}
    </div>
  )
}

export default LanguageGrammarMode