import React, { useState, useEffect } from 'react'
import { Question } from '../types/database.types'
import { 
  CheckCircleIcon, 
  XCircleIcon, 
  LightBulbIcon, 
  BookOpenIcon,
  AcademicCapIcon,
  SparklesIcon,
  TrophyIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import { CheckCircleIcon as CheckCircleSolidIcon, XCircleIcon as XCircleSolidIcon } from '@heroicons/react/24/solid'

interface EnhancedQuestionDisplayProps {
  question: Question
  questionNumber: number
  totalQuestions: number
  onAnswerSelect: (optionIndex: number) => void
  onSubmit: () => void
  onNext: () => void
  selectedAnswer?: number
  showExplanation: boolean
  isPreQuiz?: boolean
  timeLimit?: number // in seconds
}

const EnhancedQuestionDisplay: React.FC<EnhancedQuestionDisplayProps> = ({
  question,
  questionNumber,
  totalQuestions,
  onAnswerSelect,
  onSubmit,
  onNext,
  selectedAnswer,
  showExplanation,
  isPreQuiz = false,
  timeLimit
}) => {
  const [timeRemaining, setTimeRemaining] = useState(timeLimit || 0)
  const [animateCorrect, setAnimateCorrect] = useState(false)
  const [animateIncorrect, setAnimateIncorrect] = useState(false)
  const [isScrolled, setIsScrolled] = useState(false)

  // Timer effect
  useEffect(() => {
    if (timeLimit && timeRemaining > 0 && !showExplanation) {
      const timer = setTimeout(() => {
        setTimeRemaining(timeRemaining - 1)
      }, 1000)
      
      // Auto-submit when time runs out
      if (timeRemaining === 1) {
        onSubmit()
      }
      
      return () => clearTimeout(timer)
    }
  }, [timeRemaining, timeLimit, showExplanation, onSubmit])

  // Reset timer when question changes
  useEffect(() => {
    setTimeRemaining(timeLimit || 0)
    setAnimateCorrect(false)
    setAnimateIncorrect(false)
  }, [question.id, timeLimit])

  // Trigger animations when showing explanation
  useEffect(() => {
    if (showExplanation) {
      const isCorrect = selectedAnswer === question.correct_answer
      if (isCorrect) {
        setAnimateCorrect(true)
      } else {
        setAnimateIncorrect(true)
      }
    }
  }, [showExplanation, selectedAnswer, question.correct_answer])

  const getDifficultyInfo = (difficulty: string) => {
    const normalized = difficulty.toLowerCase()
    
    if (normalized.includes('easy') || normalized === '1') {
      return { 
        label: 'Easy', 
        color: 'from-green-400 to-green-600',
        bgColor: 'bg-green-50 dark:bg-green-900/20',
        borderColor: 'border-green-200 dark:border-green-800',
        icon: '🌱'
      }
    } else if (normalized.includes('hard') || normalized === '3') {
      return { 
        label: 'Hard', 
        color: 'from-orange-400 to-orange-600',
        bgColor: 'bg-orange-50 dark:bg-orange-900/20',
        borderColor: 'border-orange-200 dark:border-orange-800',
        icon: '🔥'
      }
    } else if (normalized.includes('expert') || normalized === '4') {
      return { 
        label: 'Expert', 
        color: 'from-red-400 to-red-600',
        bgColor: 'bg-red-50 dark:bg-red-900/20',
        borderColor: 'border-red-200 dark:border-red-800',
        icon: '⚡'
      }
    } else {
      return { 
        label: 'Medium', 
        color: 'from-blue-400 to-blue-600',
        bgColor: 'bg-blue-50 dark:bg-blue-900/20',
        borderColor: 'border-blue-200 dark:border-blue-800',
        icon: '💫'
      }
    }
  }

  const difficulty = getDifficultyInfo(question.difficulty)
  const isCorrect = selectedAnswer === question.correct_answer

  // Calculate progress percentage
  const progressPercentage = (questionNumber / totalQuestions) * 100

  return (
    <div className="flex flex-col bg-white dark:bg-neutral-900">
      {/* Header with progress - More compact */}
      <div className={`bg-white dark:bg-neutral-900 pb-1 transition-shadow duration-200 ${isScrolled ? 'shadow-md' : ''}`}>
        {/* Progress bar at the very top */}
        <div className="h-1 bg-neutral-200 dark:bg-neutral-700 rounded-full overflow-hidden mb-2">
          <div 
            className="h-full bg-gradient-to-r from-primary-400 to-primary-600 transition-all duration-500 ease-out"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
        
        {/* Question header with background - Compact */}
        <div className="flex justify-between items-center bg-white dark:bg-neutral-900 px-2">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              {isPreQuiz ? (
                <AcademicCapIcon className="h-4 w-4 text-primary-600" />
              ) : (
                <BookOpenIcon className="h-4 w-4 text-primary-600" />
              )}
              <h3 className="text-sm sm:text-base font-semibold text-neutral-800 dark:text-neutral-100">
                {isPreQuiz ? 'Pre-Quiz' : 'Test'}
              </h3>
            </div>
            <span className="text-xs sm:text-sm text-neutral-500 dark:text-neutral-400">
              Q{questionNumber}/{totalQuestions}
            </span>
          </div>
          
          <div className="flex items-center gap-3">
            {/* Timer - More compact */}
            {timeLimit && timeRemaining > 0 && !showExplanation && (
              <div className={`flex items-center gap-1 px-2 py-0.5 rounded-full text-xs sm:text-sm font-medium
                ${timeRemaining <= 10 
                  ? 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 animate-pulse' 
                  : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400'
                }`}>
                <ClockIcon className="h-4 w-4" />
                <span>{timeRemaining}s</span>
              </div>
            )}
            
            {/* Difficulty badge - Compact */}
            <div className={`px-2 py-0.5 rounded-full ${difficulty.bgColor} border ${difficulty.borderColor}`}>
              <span className={`text-xs font-bold bg-gradient-to-r ${difficulty.color} bg-clip-text text-transparent`}>
                {difficulty.icon}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Question card - No scrolling needed */}
      <div className={`transition-all duration-300 pt-4
        ${showExplanation 
          ? isCorrect 
            ? 'bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20' 
            : 'bg-gradient-to-br from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20'
          : 'bg-white dark:bg-neutral-800'
        }`}>
        
        <div className="relative p-3 sm:p-4">
          {/* Decorative corner gradient */}
          <div className="absolute top-0 right-0 w-24 h-24 opacity-10 pointer-events-none">
            <div className={`w-full h-full bg-gradient-to-br ${difficulty.color} rounded-bl-full`} />
          </div>
          {/* Question text */}
          <div className="mb-3">
            <p className="text-sm sm:text-base leading-relaxed text-neutral-800 dark:text-neutral-100 font-medium">
              {question.question_text}
            </p>
          </div>

          {/* Question image if present */}
          {question.image_url && (
            <div className="mb-3 rounded-lg overflow-hidden shadow-md">
              <img 
                src={question.image_url} 
                alt="Question visual"
                className="w-full h-auto max-h-32 sm:max-h-40 object-contain bg-neutral-50 dark:bg-neutral-900"
              />
            </div>
          )}

          {/* Answer options - More compact */}
          <div className="space-y-1.5 sm:space-y-2">
            {question.options.map((option, index) => {
              const isSelected = selectedAnswer === index
              const isCorrectOption = index === question.correct_answer
              const showCorrect = showExplanation && isCorrectOption
              const showIncorrect = showExplanation && isSelected && !isCorrectOption
              
              return (
                <button
                  key={index}
                  onClick={() => {
                    if (!showExplanation) {
                      onAnswerSelect(index)
                      // Automatically submit after a brief delay for visual feedback
                      setTimeout(() => onSubmit(), 300)
                    }
                  }}
                  disabled={showExplanation}
                  className={`
                    relative w-full text-left p-2.5 sm:p-3 rounded-lg border-2 transition-all duration-300
                    ${showCorrect
                      ? 'bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 border-green-500 shadow-lg shadow-green-200 dark:shadow-green-900/50 scale-[1.02]'
                      : showIncorrect
                      ? 'bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/30 dark:to-pink-900/30 border-red-500 shadow-md shadow-red-200 dark:shadow-red-900/50'
                      : showExplanation
                      ? 'border-neutral-200 dark:border-neutral-700 opacity-50'
                      : isSelected
                      ? 'bg-gradient-to-r from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-900/50 border-primary-500 shadow-md shadow-primary-200 dark:shadow-primary-900/50'
                      : 'border-neutral-200 dark:border-neutral-700 hover:border-primary-300 dark:hover:border-primary-700 hover:bg-neutral-50 dark:hover:bg-neutral-800/50'
                    }
                    ${!showExplanation && 'transform hover:translate-x-1'}
                  `}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {/* Option letter */}
                      <div className={`
                        w-6 h-6 sm:w-7 sm:h-7 rounded-full flex items-center justify-center text-xs sm:text-sm font-bold
                        ${showCorrect
                          ? 'bg-green-500 text-white'
                          : showIncorrect
                          ? 'bg-red-500 text-white'
                          : isSelected
                          ? 'bg-primary-500 text-white'
                          : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-400'
                        }
                      `}>
                        {String.fromCharCode(65 + index)}
                      </div>
                      
                      {/* Option text */}
                      <span className={`
                        text-sm sm:text-base
                        ${showCorrect || showIncorrect || isSelected
                          ? 'font-medium text-neutral-800 dark:text-neutral-100'
                          : 'text-neutral-700 dark:text-neutral-300'
                        }
                      `}>
                        {option}
                      </span>
                    </div>
                    
                    {/* Result icon */}
                    {showCorrect && (
                      <CheckCircleSolidIcon className={`h-5 w-5 sm:h-6 sm:w-6 text-green-500 ${animateCorrect ? 'animate-bounce' : ''}`} />
                    )}
                    {showIncorrect && (
                      <XCircleSolidIcon className={`h-5 w-5 sm:h-6 sm:w-6 text-red-500 ${animateIncorrect ? 'animate-pulse' : ''}`} />
                    )}
                  </div>
                </button>
              )
            })}
          </div>

          {/* Explanation box - Compact */}
          {showExplanation && (
            <div className={`
              mt-3 p-2.5 sm:p-3 rounded-lg border-2 animate-slideIn text-sm
              ${isCorrect
                ? 'bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-green-300 dark:border-green-700'
                : 'bg-gradient-to-r from-amber-50 to-yellow-50 dark:from-amber-900/20 dark:to-yellow-900/20 border-amber-300 dark:border-amber-700'
              }
            `}>
              <div className="flex items-start gap-2">
                <LightBulbIcon className={`h-4 w-4 sm:h-5 sm:w-5 mt-0.5 flex-shrink-0 ${
                  isCorrect ? 'text-green-600 dark:text-green-400' : 'text-amber-600 dark:text-amber-400'
                }`} />
                <div>
                  <p className="font-semibold text-neutral-800 dark:text-neutral-100 mb-0.5 text-sm">
                    {isCorrect ? 'Excellent!' : 'Explanation'}
                  </p>
                  <p className="text-xs sm:text-sm text-neutral-700 dark:text-neutral-300 leading-relaxed">
                    {question.explanation || 'No explanation available for this question.'}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Result message - Ultra compact or removed */}
        </div>
      </div>

      {/* Action buttons - Fixed at bottom with opaque background */}
      {showExplanation && (
        <div className="flex-shrink-0 bg-white dark:bg-neutral-900 border-t border-neutral-200 dark:border-neutral-700 pt-3 mt-2">
          <div className="flex justify-end">
            <button
              onClick={onNext}
              className="px-4 sm:px-6 py-2.5 sm:py-3 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl font-medium shadow-lg hover:shadow-xl hover:scale-105 active:scale-100 transition-all text-sm sm:text-base"
            >
              {questionNumber === totalQuestions ? 'View Results' : 'Next Question →'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default EnhancedQuestionDisplay