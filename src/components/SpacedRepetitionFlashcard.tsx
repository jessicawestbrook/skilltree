import React, { useState, useEffect } from 'react'
import { spacedRepetitionService, ReviewResponse } from '../services/spacedRepetitionService'
import { useAuth } from '../contexts/AuthContext'
import {
  ArrowPathIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  AcademicCapIcon,
  StarIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline'

interface FlashcardData {
  id: string
  type: 'vocabulary' | 'spelling' | 'language' | 'question' | 'skill_node'
  front: string
  back: string
  details?: string
  difficulty?: string
  category?: string
  hint?: string
}

interface SpacedRepetitionFlashcardProps {
  flashcards: FlashcardData[]
  onComplete?: () => void
  onLoadMore?: () => void
  className?: string
}

const SpacedRepetitionFlashcard: React.FC<SpacedRepetitionFlashcardProps> = ({
  flashcards,
  onComplete,
  onLoadMore,
  className = ''
}) => {
  const { user } = useAuth()
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)
  const [showHint, setShowHint] = useState(false)
  const [startTime, setStartTime] = useState<number>(Date.now())
  const [stats, setStats] = useState({
    dueToday: 0,
    newCards: 0,
    learningCards: 0,
    matureCards: 0
  })
  const [sessionStats, setSessionStats] = useState({
    reviewed: 0,
    correct: 0,
    incorrect: 0,
    averageTime: 0
  })
  
  const currentCard = flashcards[currentIndex] || null

  useEffect(() => {
    const loadStats = async () => {
      if (user) {
        const userStats = await spacedRepetitionService.getUserStatistics(user.id)
        if (userStats) {
          setStats({
            dueToday: userStats.dueToday,
            newCards: userStats.newCards,
            learningCards: userStats.learningCards,
            matureCards: userStats.matureCards
          })
        }
      }
    }
    loadStats()
  }, [user])

  useEffect(() => {
    // Reset state when card changes
    setIsFlipped(false)
    setShowHint(false)
    setStartTime(Date.now())
  }, [currentIndex])


  const handleQualityRating = async (quality: number) => {
    if (!user || !currentCard) return

    const timeSpent = Math.floor((Date.now() - startTime) / 1000)
    
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

    // Update session stats
    setSessionStats(prev => ({
      reviewed: prev.reviewed + 1,
      correct: quality >= 3 ? prev.correct + 1 : prev.correct,
      incorrect: quality < 3 ? prev.incorrect + 1 : prev.incorrect,
      averageTime: (prev.averageTime * prev.reviewed + timeSpent) / (prev.reviewed + 1)
    }))

    // Move to next card
    if (currentIndex < flashcards.length - 1) {
      setCurrentIndex(prev => prev + 1)
      
      // Load more cards when we're getting close to the end
      if (currentIndex >= flashcards.length - 5 && onLoadMore) {
        onLoadMore()
      }
    } else {
      // No more cards, try to load more
      if (onLoadMore) {
        onLoadMore()
      } else if (onComplete) {
        onComplete()
      }
    }
  }

  const getQualityButtonStyle = (quality: number) => {
    const baseStyle = "px-3 py-2 rounded-lg font-medium text-sm transition-all"
    switch (quality) {
      case 0:
      case 1:
        return `${baseStyle} bg-red-100 hover:bg-red-200 text-red-700 dark:bg-red-900/30 dark:hover:bg-red-900/50 dark:text-red-400`
      case 2:
        return `${baseStyle} bg-orange-100 hover:bg-orange-200 text-orange-700 dark:bg-orange-900/30 dark:hover:bg-orange-900/50 dark:text-orange-400`
      case 3:
        return `${baseStyle} bg-yellow-100 hover:bg-yellow-200 text-yellow-700 dark:bg-yellow-900/30 dark:hover:bg-yellow-900/50 dark:text-yellow-400`
      case 4:
        return `${baseStyle} bg-blue-100 hover:bg-blue-200 text-blue-700 dark:bg-blue-900/30 dark:hover:bg-blue-900/50 dark:text-blue-400`
      case 5:
        return `${baseStyle} bg-green-100 hover:bg-green-200 text-green-700 dark:bg-green-900/30 dark:hover:bg-green-900/50 dark:text-green-400`
      default:
        return baseStyle
    }
  }

  const getQualityLabel = (quality: number) => {
    switch (quality) {
      case 0: return 'Blackout'
      case 1: return 'Failed'
      case 2: return 'Hard'
      case 3: return 'Good'
      case 4: return 'Easy'
      case 5: return 'Perfect'
      default: return ''
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
      {/* Header Stats */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-4 text-xs text-neutral-600 dark:text-neutral-400">
          <span className="flex items-center gap-1">
            <ClockIcon className="h-4 w-4" />
            Due: {stats.dueToday}
          </span>
          <span className="flex items-center gap-1">
            <StarIcon className="h-4 w-4" />
            New: {stats.newCards}
          </span>
          <span className="flex items-center gap-1">
            <AcademicCapIcon className="h-4 w-4" />
            Learning: {stats.learningCards}
          </span>
        </div>
        <span className="text-sm text-neutral-500">
          {currentIndex + 1} / {flashcards.length}
        </span>
      </div>

      {/* Flashcard */}
      <div 
        className="relative h-64 cursor-pointer perspective-1000 mb-6"
        onClick={() => setIsFlipped(!isFlipped)}
      >
        <div className={`absolute inset-0 w-full h-full transition-transform duration-500 transform-style-preserve-3d ${
          isFlipped ? 'rotate-y-180' : ''
        }`}>
          {/* Front of card */}
          <div className="absolute inset-0 w-full h-full backface-hidden rounded-lg bg-gradient-to-br from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 border border-primary-200 dark:border-primary-700 p-6 flex flex-col justify-center items-center text-center">
            <span className="text-sm text-primary-600 dark:text-primary-400 mb-3">
              {currentCard.category || currentCard.type}
            </span>
            <p className="text-lg font-medium text-neutral-800 dark:text-neutral-200">
              {currentCard.front}
            </p>
            {currentCard.difficulty && (
              <span className="text-xs text-neutral-500 mt-3">
                Difficulty: {currentCard.difficulty}
              </span>
            )}
            <ArrowPathIcon className="h-5 w-5 text-neutral-400 mt-4" />
            <span className="text-xs text-neutral-500 mt-2">Click to reveal</span>
          </div>
          
          {/* Back of card */}
          <div className="absolute inset-0 w-full h-full backface-hidden rotate-y-180 rounded-lg bg-gradient-to-br from-gold-50 to-primary-50 dark:from-gold-900/20 dark:to-primary-900/20 border border-gold-200 dark:border-gold-700 p-6 flex flex-col justify-center items-center text-center">
            <p className="text-xl font-semibold text-neutral-800 dark:text-neutral-200">
              {currentCard.back}
            </p>
            {currentCard.details && (
              <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-3">
                {currentCard.details}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Hint Section */}
      {currentCard.hint && !isFlipped && (
        <div className="mb-4">
          {!showHint ? (
            <button
              onClick={() => setShowHint(true)}
              className="flex items-center gap-2 text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
            >
              <LightBulbIcon className="h-4 w-4" />
              Show hint
            </button>
          ) : (
            <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <p className="text-sm text-blue-700 dark:text-blue-300">
                <span className="font-medium">Hint:</span> {currentCard.hint}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Rating Buttons (shown after flip) */}
      {isFlipped && (
        <div className="space-y-3">
          <p className="text-sm text-neutral-600 dark:text-neutral-400 text-center">
            How well did you know this?
          </p>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => handleQualityRating(1)}
              className={getQualityButtonStyle(1)}
            >
              <XCircleIcon className="h-4 w-4 inline mr-1" />
              {getQualityLabel(1)}
            </button>
            <button
              onClick={() => handleQualityRating(3)}
              className={getQualityButtonStyle(3)}
            >
              {getQualityLabel(3)}
            </button>
            <button
              onClick={() => handleQualityRating(5)}
              className={getQualityButtonStyle(5)}
            >
              <CheckCircleIcon className="h-4 w-4 inline mr-1" />
              {getQualityLabel(5)}
            </button>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => handleQualityRating(0)}
              className={`${getQualityButtonStyle(0)} text-xs`}
            >
              {getQualityLabel(0)}
            </button>
            <button
              onClick={() => handleQualityRating(2)}
              className={`${getQualityButtonStyle(2)} text-xs`}
            >
              {getQualityLabel(2)}
            </button>
            <button
              onClick={() => handleQualityRating(4)}
              className={`${getQualityButtonStyle(4)} text-xs`}
            >
              {getQualityLabel(4)}
            </button>
          </div>
        </div>
      )}

      {/* Progress Dots */}
      <div className="flex justify-center gap-1 mt-6">
        {flashcards.slice(0, 10).map((_, index) => (
          <div
            key={index}
            className={`w-2 h-2 rounded-full transition-colors ${
              index === currentIndex 
                ? 'bg-primary-600' 
                : index < currentIndex
                ? 'bg-green-500'
                : 'bg-neutral-300 dark:bg-neutral-600'
            }`}
          />
        ))}
        {flashcards.length > 10 && (
          <span className="text-xs text-neutral-500 ml-2">
            +{flashcards.length - 10}
          </span>
        )}
      </div>
    </div>
  )
}

export default SpacedRepetitionFlashcard