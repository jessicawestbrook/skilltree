import React, { useState, useEffect, useCallback } from 'react'
import { spacedRepetitionService, ReviewResponse } from '../services/spacedRepetitionService'
import { useAuth } from '../contexts/AuthContext'
import {
  CheckCircleIcon,
  XCircleIcon,
  SpeakerWaveIcon,
  ArrowRightIcon,
  LightBulbIcon,
  ChartBarIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

interface FlashcardData {
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
  // Spelling format
  audio_pronunciation?: string
  // Language format
  language?: string
  category?: string
  hint?: string
  // General
  difficulty?: string
  estimated_time_seconds?: number
}

interface InteractiveFlashcardReviewProps {
  flashcards: FlashcardData[]
  onComplete?: () => void
  onLoadMore?: () => void
  className?: string
}

const InteractiveFlashcardReview: React.FC<InteractiveFlashcardReviewProps> = ({
  flashcards,
  onComplete,
  onLoadMore,
  className = ''
}) => {
  const { user } = useAuth()
  const [currentIndex, setCurrentIndex] = useState(0)
  const [userAnswer, setUserAnswer] = useState<string>('')
  const [selectedOption, setSelectedOption] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [showHint, setShowHint] = useState(false)
  const [startTime, setStartTime] = useState<number>(Date.now())
  const [sessionStats, setSessionStats] = useState({
    reviewed: 0,
    correct: 0,
    incorrect: 0,
    averageTime: 0
  })

  const currentCard = flashcards[currentIndex] || null

  useEffect(() => {
    // Reset state when card changes
    setUserAnswer('')
    setSelectedOption(null)
    setShowResult(false)
    setShowHint(false)
    setStartTime(Date.now())
  }, [currentIndex])

  // Text-to-speech for pronunciation
  const speak = useCallback((text: string, lang: string = 'en-US') => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel()
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = lang
      utterance.rate = 0.9
      window.speechSynthesis.speak(utterance)
    }
  }, [])

  const checkAnswer = () => {
    if (!currentCard) return

    let correct = false

    switch (currentCard.type) {
      case 'spelling':
        correct = userAnswer.trim().toLowerCase() === currentCard.word?.toLowerCase()
        break
      
      case 'vocabulary':
        if (currentCard.options && selectedOption !== null) {
          correct = selectedOption === currentCard.correct_answer_index ||
                   currentCard.options[selectedOption] === currentCard.correct_answer
        }
        break
      
      case 'language':
        if (selectedOption !== null) {
          correct = selectedOption === currentCard.correct_answer_index
        }
        break
      
      case 'question':
      case 'skill_node':
        if (currentCard.options && selectedOption !== null) {
          correct = currentCard.options[selectedOption] === currentCard.correct_answer
        } else {
          correct = userAnswer.trim().toLowerCase() === currentCard.correct_answer?.toLowerCase()
        }
        break
    }

    setIsCorrect(correct)
    setShowResult(true)

    // Update session stats
    setSessionStats(prev => ({
      reviewed: prev.reviewed + 1,
      correct: correct ? prev.correct + 1 : prev.correct,
      incorrect: !correct ? prev.incorrect + 1 : prev.incorrect,
      averageTime: (prev.averageTime * prev.reviewed + (Date.now() - startTime) / 1000) / (prev.reviewed + 1)
    }))
  }

  const submitReview = async () => {
    if (!user || !currentCard) return

    const timeSpent = Math.floor((Date.now() - startTime) / 1000)
    
    // Calculate quality rating based on correctness and hints
    let quality = 0
    if (isCorrect) {
      if (showHint) {
        quality = 3 // Correct with hint
      } else if (timeSpent < 10) {
        quality = 5 // Perfect recall
      } else if (timeSpent < 30) {
        quality = 4 // Good recall
      } else {
        quality = 3 // Correct but slow
      }
    } else {
      quality = 1 // Failed
    }

    const response: ReviewResponse = {
      quality,
      time_taken: timeSpent,
      hint_used: showHint
    }

    // Record the review
    await spacedRepetitionService.recordReview(
      user.id,
      currentCard.id,
      currentCard.type,
      response
    )

    // Move to next card
    if (currentIndex < flashcards.length - 1) {
      setCurrentIndex(prev => prev + 1)
      
      // Load more cards when getting close to the end
      if (currentIndex >= flashcards.length - 5 && onLoadMore) {
        onLoadMore()
      }
    } else {
      // No more cards, try to load more or complete
      if (onLoadMore) {
        onLoadMore()
      } else if (onComplete) {
        onComplete()
      }
    }
  }

  const renderSpellingCard = () => {
    if (!currentCard) return null

    return (
      <div className="space-y-6">
        <div className="text-center">
          <h3 className="text-2xl font-semibold text-neutral-900 dark:text-white mb-4">
            Spell this word
          </h3>
          
          <button
            onClick={() => speak(currentCard.word || '')}
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary-100 hover:bg-primary-200 dark:bg-primary-900/30 dark:hover:bg-primary-900/50 text-primary-700 dark:text-primary-300 rounded-lg transition-colors"
          >
            <SpeakerWaveIcon className="h-6 w-6" />
            Play Audio
          </button>

          {currentCard.pronunciation && (
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-2">
              Pronunciation: {currentCard.pronunciation}
            </p>
          )}

          {currentCard.example_sentence && showHint && (
            <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <p className="text-sm text-blue-700 dark:text-blue-300">
                {currentCard.example_sentence}
              </p>
            </div>
          )}
        </div>

        <div>
          <input
            type="text"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !showResult) {
                checkAnswer()
              }
            }}
            placeholder="Type your answer..."
            disabled={showResult}
            className="w-full px-4 py-3 text-lg border border-neutral-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-800 dark:text-white"
            autoFocus
          />
        </div>

        {showResult && (
          <div className={`p-4 rounded-lg ${isCorrect ? 'bg-green-100 dark:bg-green-900/30' : 'bg-red-100 dark:bg-red-900/30'}`}>
            <div className="flex items-center gap-2">
              {isCorrect ? (
                <CheckCircleIcon className="h-6 w-6 text-green-600 dark:text-green-400" />
              ) : (
                <XCircleIcon className="h-6 w-6 text-red-600 dark:text-red-400" />
              )}
              <p className={`font-semibold ${isCorrect ? 'text-green-700 dark:text-green-300' : 'text-red-700 dark:text-red-300'}`}>
                {isCorrect ? 'Correct!' : `Incorrect. The answer is: ${currentCard.word}`}
              </p>
            </div>
            {currentCard.definition && (
              <p className="text-sm text-neutral-700 dark:text-neutral-300 mt-2">
                Definition: {currentCard.definition}
              </p>
            )}
          </div>
        )}
      </div>
    )
  }

  const renderVocabularyCard = () => {
    if (!currentCard) return null

    const isWordToDefinition = Math.random() > 0.5
    const question = isWordToDefinition ? currentCard.word : currentCard.definition
    const correctAnswer = isWordToDefinition ? currentCard.definition : currentCard.word

    return (
      <div className="space-y-6">
        <div>
          <h3 className="text-xl font-semibold text-neutral-900 dark:text-white mb-2">
            {isWordToDefinition ? 'What is the definition of:' : 'What word means:'}
          </h3>
          <p className="text-2xl font-bold text-primary-600 dark:text-primary-400">
            {question}
          </p>
          {currentCard.part_of_speech && isWordToDefinition && (
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-1">
              ({currentCard.part_of_speech})
            </p>
          )}
        </div>

        {currentCard.options && currentCard.options.length > 0 ? (
          <div className="space-y-3">
            {currentCard.options.map((option, index) => (
              <button
                key={index}
                onClick={() => {
                  if (!showResult) {
                    setSelectedOption(index)
                  }
                }}
                disabled={showResult}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                  showResult
                    ? index === currentCard.correct_answer_index
                      ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                      : selectedOption === index
                      ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                      : 'border-neutral-200 dark:border-neutral-700'
                    : selectedOption === index
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                    : 'border-neutral-200 dark:border-neutral-700 hover:border-primary-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-neutral-800 dark:text-neutral-200">
                    {option}
                  </span>
                  {showResult && (
                    <span>
                      {index === currentCard.correct_answer_index ? (
                        <CheckCircleIcon className="h-5 w-5 text-green-600" />
                      ) : selectedOption === index ? (
                        <XCircleIcon className="h-5 w-5 text-red-600" />
                      ) : null}
                    </span>
                  )}
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div>
            <input
              type="text"
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !showResult) {
                  checkAnswer()
                }
              }}
              placeholder="Type your answer..."
              disabled={showResult}
              className="w-full px-4 py-3 text-lg border border-neutral-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-800 dark:text-white"
              autoFocus
            />
            {showResult && (
              <div className={`mt-4 p-4 rounded-lg ${isCorrect ? 'bg-green-100 dark:bg-green-900/30' : 'bg-red-100 dark:bg-red-900/30'}`}>
                <p className={`font-semibold ${isCorrect ? 'text-green-700 dark:text-green-300' : 'text-red-700 dark:text-red-300'}`}>
                  {isCorrect ? 'Correct!' : `Incorrect. The answer is: ${correctAnswer}`}
                </p>
              </div>
            )}
          </div>
        )}

        {currentCard.example_sentence && showResult && (
          <div className="p-3 bg-neutral-100 dark:bg-neutral-800 rounded-lg">
            <p className="text-sm text-neutral-700 dark:text-neutral-300">
              <strong>Example:</strong> {currentCard.example_sentence}
            </p>
          </div>
        )}
      </div>
    )
  }

  const renderQuestionCard = () => {
    if (!currentCard) return null

    return (
      <div className="space-y-6">
        <div>
          <h3 className="text-xl font-medium text-neutral-900 dark:text-white leading-relaxed">
            {currentCard.question}
          </h3>
          {currentCard.category && (
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-2">
              Category: {currentCard.category}
            </p>
          )}
        </div>

        {currentCard.options && currentCard.options.length > 0 ? (
          <div className="space-y-3">
            {currentCard.options.map((option, index) => (
              <button
                key={index}
                onClick={() => {
                  if (!showResult) {
                    setSelectedOption(index)
                  }
                }}
                disabled={showResult}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                  showResult
                    ? option === currentCard.correct_answer
                      ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                      : selectedOption === index
                      ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                      : 'border-neutral-200 dark:border-neutral-700'
                    : selectedOption === index
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                    : 'border-neutral-200 dark:border-neutral-700 hover:border-primary-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-neutral-800 dark:text-neutral-200">
                    {option}
                  </span>
                  {showResult && (
                    <span>
                      {option === currentCard.correct_answer ? (
                        <CheckCircleIcon className="h-5 w-5 text-green-600" />
                      ) : selectedOption === index ? (
                        <XCircleIcon className="h-5 w-5 text-red-600" />
                      ) : null}
                    </span>
                  )}
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div>
            <textarea
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              placeholder="Type your answer..."
              disabled={showResult}
              className="w-full px-4 py-3 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-800 dark:text-white"
              rows={3}
              autoFocus
            />
          </div>
        )}

        {showResult && currentCard.explanation && (
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <p className="text-sm text-blue-700 dark:text-blue-300">
              <strong>Explanation:</strong> {currentCard.explanation}
            </p>
          </div>
        )}
      </div>
    )
  }

  const renderLanguageCard = () => {
    if (!currentCard) return null

    return (
      <div className="space-y-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="px-2 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded text-sm font-medium">
              {currentCard.language}
            </span>
            {currentCard.category && (
              <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded text-sm">
                {currentCard.category}
              </span>
            )}
          </div>
          <h3 className="text-xl font-medium text-neutral-900 dark:text-white">
            {currentCard.question}
          </h3>
          {currentCard.hint && showHint && (
            <div className="mt-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
              <p className="text-sm text-yellow-700 dark:text-yellow-300">
                Hint: {currentCard.hint}
              </p>
            </div>
          )}
        </div>

        {currentCard.options && currentCard.options.length > 0 && (
          <div className="space-y-3">
            {currentCard.options.map((option, index) => (
              <button
                key={index}
                onClick={() => {
                  if (!showResult) {
                    setSelectedOption(index)
                    // Auto-play pronunciation for language options
                    if (currentCard.language) {
                      const langCode = currentCard.language.toLowerCase().substring(0, 2)
                      speak(option, langCode)
                    }
                  }
                }}
                disabled={showResult}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                  showResult
                    ? index === currentCard.correct_answer_index
                      ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                      : selectedOption === index
                      ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                      : 'border-neutral-200 dark:border-neutral-700'
                    : selectedOption === index
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                    : 'border-neutral-200 dark:border-neutral-700 hover:border-primary-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-neutral-800 dark:text-neutral-200">
                      {option}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        if (currentCard.language) {
                          const langCode = currentCard.language.toLowerCase().substring(0, 2)
                          speak(option, langCode)
                        }
                      }}
                      className="p-1 hover:bg-neutral-200 dark:hover:bg-neutral-700 rounded"
                    >
                      <SpeakerWaveIcon className="h-4 w-4 text-neutral-600 dark:text-neutral-400" />
                    </button>
                  </div>
                  {showResult && (
                    <span>
                      {index === currentCard.correct_answer_index ? (
                        <CheckCircleIcon className="h-5 w-5 text-green-600" />
                      ) : selectedOption === index ? (
                        <XCircleIcon className="h-5 w-5 text-red-600" />
                      ) : null}
                    </span>
                  )}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    )
  }

  const renderCard = () => {
    if (!currentCard) return null

    switch (currentCard.type) {
      case 'spelling':
        return renderSpellingCard()
      case 'vocabulary':
        return renderVocabularyCard()
      case 'language':
        return renderLanguageCard()
      case 'question':
      case 'skill_node':
        return renderQuestionCard()
      default:
        return null
    }
  }

  if (!currentCard) {
    return (
      <div className={`bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 ${className}`}>
        <div className="text-center">
          <CheckCircleIcon className="h-12 w-12 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-2">
            Review Complete!
          </h3>
          <div className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
            <p>Cards reviewed: {sessionStats.reviewed}</p>
            <p>Correct: {sessionStats.correct} ({sessionStats.reviewed > 0 ? Math.round((sessionStats.correct / sessionStats.reviewed) * 100) : 0}%)</p>
            <p>Average time: {Math.round(sessionStats.averageTime)}s</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <span className="text-sm text-neutral-600 dark:text-neutral-400">
            Card {currentIndex + 1} of {flashcards.length}
          </span>
          {currentCard.difficulty && (
            <span className="px-2 py-1 bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 rounded text-xs">
              {currentCard.difficulty}
            </span>
          )}
          {currentCard.estimated_time_seconds && (
            <span className="flex items-center gap-1 text-xs text-neutral-500">
              <ClockIcon className="h-3 w-3" />
              ~{currentCard.estimated_time_seconds}s
            </span>
          )}
        </div>
        
        <div className="flex items-center gap-2">
          {currentCard.hint && !showHint && !showResult && (
            <button
              onClick={() => setShowHint(true)}
              className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
            >
              <LightBulbIcon className="h-4 w-4" />
              Hint
            </button>
          )}
          
          <div className="flex items-center gap-1 text-sm text-neutral-600 dark:text-neutral-400">
            <ChartBarIcon className="h-4 w-4" />
            {sessionStats.correct}/{sessionStats.reviewed}
          </div>
        </div>
      </div>

      {/* Card Content */}
      {renderCard()}

      {/* Action Buttons */}
      <div className="mt-6 flex justify-end gap-3">
        {!showResult ? (
          <button
            onClick={checkAnswer}
            disabled={
              (currentCard.type === 'spelling' && !userAnswer) ||
              ((currentCard.type === 'vocabulary' || currentCard.type === 'language' || 
                (currentCard.type === 'question' && currentCard.options)) && selectedOption === null) ||
              ((currentCard.type === 'question' && !currentCard.options) && !userAnswer)
            }
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-300 disabled:cursor-not-allowed transition-colors"
          >
            Check Answer
          </button>
        ) : (
          <button
            onClick={submitReview}
            className="inline-flex items-center gap-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Next
            <ArrowRightIcon className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Progress Bar */}
      <div className="mt-6 w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
        <div
          className="bg-primary-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${((currentIndex + 1) / flashcards.length) * 100}%` }}
        />
      </div>
    </div>
  )
}

export default InteractiveFlashcardReview