import React, { useState, useEffect, useCallback } from 'react'
import { spacedRepetitionService, ReviewResponse } from '../services/spacedRepetitionService'
import { achievementService } from '../services/achievementService'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import {
  CheckCircleIcon,
  XCircleIcon,
  ArrowRightIcon,
  LightBulbIcon,
  ChartBarIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import SpellingCard from './flashcards/SpellingCard'
import VocabularyCard from './flashcards/VocabularyCard'
import LanguageCard from './flashcards/LanguageCard'

interface FlashcardData {
  id: string
  type: 'vocabulary' | 'spelling' | 'language' | 'question'
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
  disableAutoFocus?: boolean
}

const InteractiveFlashcardReview: React.FC<InteractiveFlashcardReviewProps> = ({
  flashcards,
  onComplete,
  onLoadMore,
  className = '',
  disableAutoFocus = false
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
    averageTime: 0,
    correctStreak: 0,
    bestStreak: 0
  })
  const [vocabOptionsPool, setVocabOptionsPool] = useState<{words: string[], definitions: string[]}>({
    words: [],
    definitions: []
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

  // Fetch vocabulary options pool on mount
  useEffect(() => {
    const fetchVocabOptions = async () => {
      const { data: vocabWords } = await supabase
        .from('spelling_words')
        .select('word, definition')
        .not('definition', 'is', null)
        .limit(50)
      
      if (vocabWords) {
        setVocabOptionsPool({
          words: vocabWords.map(w => w.word).filter(Boolean),
          definitions: vocabWords.map(w => w.definition).filter(Boolean)
        })
      }
    }
    
    fetchVocabOptions()
  }, [])

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
      averageTime: (prev.averageTime * prev.reviewed + (Date.now() - startTime) / 1000) / (prev.reviewed + 1),
      correctStreak: correct ? prev.correctStreak + 1 : 0,
      bestStreak: correct ? Math.max(prev.correctStreak + 1, prev.bestStreak) : prev.bestStreak
    }))
  }

  const skipCard = async () => {
    if (!currentCard) return

    // Don't record any review for skipped cards - they won't be added to review queue
    // Just move to the next card
    
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
    
    // Track achievements
    await achievementService.trackFlashcardReview(user.id, isCorrect)
    await achievementService.trackDailyActivity(user.id)
    
    // Update and check streak achievements
    const newStreak = isCorrect 
      ? sessionStats.correctStreak + 1 
      : 0
    
    if (newStreak > 0) {
      await achievementService.trackFlashcardStreak(user.id, newStreak)
    }
    
    // Update session stats with new streak
    setSessionStats(prev => ({
      ...prev,
      correctStreak: newStreak,
      bestStreak: Math.max(newStreak, prev.bestStreak)
    }))
    
    // Check for speed demon achievement (10 cards in under 60 seconds)
    if (sessionStats.reviewed === 9 && isCorrect) { // This will be the 10th card
      const totalCards = sessionStats.reviewed + 1
      const sessionTime = Math.floor((Date.now() - startTime) / 1000)
      if (totalCards >= 10 && sessionTime < 60) {
        await achievementService.trackSpeedAchievement(user.id, totalCards, sessionTime)
      }
    }

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
      <SpellingCard
        word={currentCard.word || ''}
        definition={currentCard.definition}
        exampleSentence={currentCard.example_sentence}
        partOfSpeech={currentCard.part_of_speech}
        difficulty={parseInt(currentCard.difficulty || '1')}
        difficultyName={currentCard.difficulty}
        userInput={userAnswer}
        showResult={showResult}
        isCorrect={isCorrect}
        onPlayAudio={() => speak(currentCard.word || '')}
        onInputChange={(value) => {
          setUserAnswer(value)
        }}
        onSubmit={() => {
          if (userAnswer.trim()) {
            checkAnswer()
          }
        }}
        onSkip={skipCard}
      />
    )
  }

  const renderVocabularyCard = () => {
    if (!currentCard) return null

    const isWordToDefinition = Math.random() > 0.5
    
    // Generate options if they don't exist
    let options = currentCard.options || []
    let correctAnswer = currentCard.correct_answer || ''
    
    if (options.length === 0 && currentCard.definition) {
      // Generate options from real vocabulary pool
      if (isWordToDefinition) {
        // Get random definitions for word-to-definition mode
        const availableDefinitions = vocabOptionsPool.definitions
          .filter(def => def !== currentCard.definition)
        
        // Get 3 random wrong definitions
        const wrongOptions = availableDefinitions.length >= 3
          ? [...availableDefinitions].sort(() => Math.random() - 0.5).slice(0, 3)
          : [
              "A type of object or concept",
              "An action or process", 
              "A quality or characteristic"
            ]
        
        options = [currentCard.definition, ...wrongOptions].sort(() => Math.random() - 0.5)
        correctAnswer = currentCard.definition
      } else {
        // Get random words for definition-to-word mode
        const availableWords = vocabOptionsPool.words
          .filter(word => word !== currentCard.word)
        
        // Get 3 random wrong words
        const wrongOptions = availableWords.length >= 3
          ? [...availableWords].sort(() => Math.random() - 0.5).slice(0, 3)
          : ["option", "choice", "alternative"]
        
        const currentWord = currentCard.word || "word"
        options = [currentWord, ...wrongOptions].sort(() => Math.random() - 0.5)
        correctAnswer = currentWord
      }
    } else if (currentCard.correct_answer_index !== undefined && currentCard.options) {
      correctAnswer = currentCard.options[currentCard.correct_answer_index]
    }

    return (
      <VocabularyCard
        word={currentCard}
        isWordToDefinition={isWordToDefinition}
        options={options}
        correctAnswer={correctAnswer}
        selectedAnswer={selectedOption !== null && options ? options[selectedOption] : ''}
        showResult={showResult}
        isCorrect={isCorrect}
        onAnswerSelect={(answer: string) => {
          if (!showResult) {
            const index = options.indexOf(answer)
            setSelectedOption(index)
            // Immediately check answer when option is selected
            setTimeout(() => {
              const correct = answer === correctAnswer
              setIsCorrect(correct)
              setShowResult(true)
              // Update session stats
              setSessionStats(prev => ({
                reviewed: prev.reviewed + 1,
                correct: correct ? prev.correct + 1 : prev.correct,
                incorrect: !correct ? prev.incorrect + 1 : prev.incorrect,
                averageTime: (prev.averageTime * prev.reviewed + (Date.now() - startTime) / 1000) / (prev.reviewed + 1),
                correctStreak: correct ? prev.correctStreak + 1 : 0,
                bestStreak: correct ? Math.max(prev.correctStreak + 1, prev.bestStreak) : prev.bestStreak
              }))
            }, 100)
          }
        }}
        onSkip={skipCard}
      />
    )
  }

  const renderLanguageCard = () => {
    if (!currentCard) return null

    return (
      <LanguageCard
        language={currentCard.language || currentCard.category || 'Language'}
        questionText={currentCard.question || ''}
        questionType={currentCard.category}
        options={currentCard.options || []}
        selectedOption={selectedOption}
        correctAnswer={currentCard.correct_answer || (currentCard.correct_answer_index !== undefined && currentCard.options ? currentCard.options[currentCard.correct_answer_index] : '')}
        showResult={showResult}
        explanation={currentCard.explanation}
        difficulty={parseInt(currentCard.difficulty || '1')}
        onSelectOption={(index) => {
          if (!showResult) {
            setSelectedOption(index)
            // Immediately check answer when option is selected
            setTimeout(() => {
              const correct = index === currentCard.correct_answer_index ||
                             currentCard.options![index] === currentCard.correct_answer
              setIsCorrect(correct)
              setShowResult(true)
              // Update session stats
              setSessionStats(prev => ({
                reviewed: prev.reviewed + 1,
                correct: correct ? prev.correct + 1 : prev.correct,
                incorrect: !correct ? prev.incorrect + 1 : prev.incorrect,
                averageTime: (prev.averageTime * prev.reviewed + (Date.now() - startTime) / 1000) / (prev.reviewed + 1),
                correctStreak: correct ? prev.correctStreak + 1 : 0,
                bestStreak: correct ? Math.max(prev.correctStreak + 1, prev.bestStreak) : prev.bestStreak
              }))
            }, 100)
          }
        }}
        onSkip={skipCard}
      />
    )
  }

  const renderQuestionCard = () => {
    if (!currentCard) return null

    return (
      <div className="px-6 py-2 space-y-6">
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
                    // Immediately check answer when option is selected
                    setTimeout(() => {
                      const correct = option === currentCard.correct_answer
                      setIsCorrect(correct)
                      setShowResult(true)
                      // Update session stats
                      setSessionStats(prev => ({
                        reviewed: prev.reviewed + 1,
                        correct: correct ? prev.correct + 1 : prev.correct,
                        incorrect: !correct ? prev.incorrect + 1 : prev.incorrect,
                        averageTime: (prev.averageTime * prev.reviewed + (Date.now() - startTime) / 1000) / (prev.reviewed + 1),
                        correctStreak: correct ? prev.correctStreak + 1 : 0,
                        bestStreak: correct ? Math.max(prev.correctStreak + 1, prev.bestStreak) : prev.bestStreak
                      }))
                    }, 100)
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
              autoFocus={!disableAutoFocus}
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
    <div className={`bg-white dark:bg-neutral-800 rounded-xl shadow-lg ${className}`}>
      {/* Header */}
      <div className="px-6 pt-4 pb-2">
        <div className="flex items-center justify-between">
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
      </div>

      {/* Card Content */}
      {renderCard()}

      {/* Footer with Action Buttons and Progress Bar */}
      <div className="px-6 pt-2 pb-4">
        {/* Action Buttons */}
        <div className="flex justify-end gap-3 mb-4">
          {showResult ? (
            <button
              onClick={submitReview}
              className="inline-flex items-center gap-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Next
              <ArrowRightIcon className="h-4 w-4" />
            </button>
          ) : (
            // Only show Check Answer button for free-form questions (not spelling, which has its own button)
            (currentCard.type === 'question' && !currentCard.options) && (
              <button
                onClick={checkAnswer}
                disabled={!userAnswer}
                className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-300 disabled:cursor-not-allowed transition-colors"
              >
                Check Answer
              </button>
            )
          )}
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
          <div
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentIndex + 1) / flashcards.length) * 100}%` }}
          />
        </div>
      </div>
    </div>
  )
}

export default InteractiveFlashcardReview