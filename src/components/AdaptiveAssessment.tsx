import React, { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { 
  AdaptiveAssessmentService, 
  Question, 
  AssessmentSession, 
  QuestionResponse 
} from '../services/adaptiveAssessmentService'
import { spacedRepetitionService } from '../services/spacedRepetitionService'
import {
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  TrophyIcon,
  ChartBarIcon,
  ArrowRightIcon,
  XMarkIcon,
  LightBulbIcon,
  StarIcon
} from '@heroicons/react/24/outline'
import { CheckCircleIcon as CheckCircleSolid } from '@heroicons/react/24/solid'

interface AdaptiveAssessmentProps {
  categoryId: string
  categoryName: string
  onComplete?: (session: AssessmentSession) => void
  onExit?: () => void
  sessionType?: 'practice' | 'assessment' | 'quick_test'
}

interface AssessmentState {
  session: AssessmentSession | null
  currentQuestion: Question | null
  selectedAnswer: string
  responseTime: number
  startTime: number
  totalPoints: number
  questionsAnswered: number
  currentDifficulty: number
  abilityEstimate: number
  consecutiveCorrect: number
  isLoading: boolean
  showExplanation: boolean
  lastResponse: QuestionResponse | null
  responses: QuestionResponse[]
}

const AdaptiveAssessment: React.FC<AdaptiveAssessmentProps> = ({
  categoryId,
  categoryName,
  onComplete,
  onExit,
  sessionType = 'assessment'
}) => {
  const { user } = useAuth()
  const [state, setState] = useState<AssessmentState>({
    session: null,
    currentQuestion: null,
    selectedAnswer: '',
    responseTime: 0,
    startTime: Date.now(),
    totalPoints: 0,
    questionsAnswered: 0,
    currentDifficulty: 2,
    abilityEstimate: 2.0,
    consecutiveCorrect: 0,
    isLoading: true,
    showExplanation: false,
    lastResponse: null,
    responses: []
  })

  // Difficulty level names and colors
  const difficultyInfo = {
    1: { name: 'Beginner', color: 'bg-green-100 text-green-800', points: 10 },
    2: { name: 'Elementary', color: 'bg-blue-100 text-blue-800', points: 25 },
    3: { name: 'Intermediate', color: 'bg-yellow-100 text-yellow-800', points: 50 },
    4: { name: 'Advanced', color: 'bg-orange-100 text-orange-800', points: 100 },
    5: { name: 'Expert', color: 'bg-red-100 text-red-800', points: 200 }
  }

  const completeAssessment = useCallback(async () => {
    if (!state.session || !user) return

    try {
      const completedSession = await AdaptiveAssessmentService.completeAssessment(state.session.id)
      
      // Add all questions from this assessment to the user's flashcard review
      if (completedSession && state.responses.length > 0) {
        const flashcardsToAdd = state.responses.map(response => ({
          id: response.question_id,
          type: 'question' as const
        }))
        
        // Add questions to spaced repetition system
        await spacedRepetitionService.addFlashcardsToReview(user.id, flashcardsToAdd)
        
        console.log(`Added ${flashcardsToAdd.length} questions to flashcard review`)
      }
      
      if (completedSession && onComplete) {
        onComplete(completedSession)
      }
    } catch (error) {
      console.error('Error completing assessment:', error)
    }
  }, [state.session, state.responses, user, onComplete])

  const loadNextQuestion = useCallback(async (sessionId: string, onNoMoreQuestions?: () => Promise<void>) => {
    if (!user) return

    try {
      setState(prev => ({ ...prev, isLoading: true }))
      
      const question = await AdaptiveAssessmentService.getNextQuestion(
        sessionId,
        user.id,
        categoryId
      )
      
      if (question) {
        setState(prev => ({
          ...prev,
          currentQuestion: question,
          selectedAnswer: '',
          startTime: Date.now(),
          showExplanation: false,
          isLoading: false
        }))
      } else {
        // No more questions available - complete assessment
        if (onNoMoreQuestions) {
          await onNoMoreQuestions()
        }
      }
    } catch (error) {
      console.error('Error loading next question:', error)
      setState(prev => ({ ...prev, isLoading: false }))
    }
  }, [user, categoryId])

  // Initialize assessment session
  useEffect(() => {
    if (!user) return
    
    // Only initialize if we don't have a session yet
    if (state.session) return

    const initializeAssessment = async () => {
      try {
        setState(prev => ({ ...prev, isLoading: true }))
        
        const session = await AdaptiveAssessmentService.startAssessment(
          user.id,
          categoryId,
          sessionType
        )
        
        if (session) {
          setState(prev => ({
            ...prev,
            session,
            abilityEstimate: session.final_ability_estimate,
            currentDifficulty: Math.round(session.final_ability_estimate)
          }))
          
          // Load first question after setting session
          const question = await AdaptiveAssessmentService.getNextQuestion(
            session.id,
            user.id,
            categoryId
          )
          
          if (question) {
            setState(prev => ({
              ...prev,
              currentQuestion: question,
              selectedAnswer: '',
              startTime: Date.now(),
              showExplanation: false,
              isLoading: false
            }))
          } else {
            // No questions available
            setState(prev => ({ ...prev, isLoading: false }))
          }
        }
      } catch (error) {
        console.error('Error initializing assessment:', error)
        setState(prev => ({ ...prev, isLoading: false }))
      }
    }

    initializeAssessment()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, categoryId, sessionType]) // Intentionally omitting state.session to avoid re-initialization

  const submitAnswer = async () => {
    if (!state.session || !state.currentQuestion || !state.selectedAnswer) return

    const responseTime = Date.now() - state.startTime
    const isCorrect = state.selectedAnswer === state.currentQuestion.correct_answer

    try {
      setState(prev => ({ ...prev, isLoading: true }))
      
      const response = await AdaptiveAssessmentService.recordResponse(
        state.session.id,
        state.currentQuestion.id,
        state.selectedAnswer,
        isCorrect,
        responseTime
      )
      
      if (response) {
        const newConsecutiveCorrect = isCorrect ? state.consecutiveCorrect + 1 : 0
        
        setState(prev => ({
          ...prev,
          lastResponse: response,
          totalPoints: prev.totalPoints + response.points_earned,
          questionsAnswered: prev.questionsAnswered + 1,
          consecutiveCorrect: newConsecutiveCorrect,
          currentDifficulty: response.difficulty_level,
          responses: [...prev.responses, response],
          showExplanation: true,
          isLoading: false
        }))
      }
    } catch (error) {
      console.error('Error submitting answer:', error)
      setState(prev => ({ ...prev, isLoading: false }))
    }
  }

  const nextQuestion = async () => {
    if (state.session) {
      await loadNextQuestion(state.session.id, completeAssessment)
    }
  }

  const exitAssessment = () => {
    if (onExit) {
      onExit()
    }
  }

  // Loading state
  if (state.isLoading && !state.currentQuestion) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-neutral-200 dark:bg-neutral-700 rounded w-1/2"></div>
            <div className="space-y-4">
              <div className="h-4 bg-neutral-200 dark:bg-neutral-700 rounded"></div>
              <div className="h-4 bg-neutral-200 dark:bg-neutral-700 rounded w-3/4"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!state.currentQuestion) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8 text-center">
          <TrophyIcon className="h-16 w-16 text-gold-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-2">
            Assessment Complete!
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            You've completed the {categoryName} assessment. Great job!
          </p>
          <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-4 mb-6">
            <div className="text-3xl font-bold text-primary-600 dark:text-primary-400">
              {state.totalPoints} points
            </div>
            <div className="text-sm text-neutral-600 dark:text-neutral-400">
              {state.questionsAnswered} questions answered
            </div>
          </div>
          <button
            onClick={exitAssessment}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Continue
          </button>
        </div>
      </div>
    )
  }

  const currentDifficultyInfo = difficultyInfo[state.currentDifficulty as keyof typeof difficultyInfo] || difficultyInfo[2]

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header with progress and scoring */}
      <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg mb-6">
        <div className="p-6">
          {/* Top row: Title and Exit button */}
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-neutral-900 dark:text-neutral-100">
                {categoryName} Assessment
              </h1>
              <p className="text-neutral-600 dark:text-neutral-400">
                Computer Adaptive Testing
              </p>
            </div>
            <button
              onClick={exitAssessment}
              className="p-2 text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-200 transition-colors"
              title="Exit Assessment"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>

          {/* Progress indicators */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-3">
              <div className="flex items-center gap-2">
                <TrophyIcon className="h-5 w-5 text-gold-500" />
                <div>
                  <div className="text-lg font-bold text-neutral-900 dark:text-neutral-100">
                    {state.totalPoints}
                  </div>
                  <div className="text-xs text-neutral-600 dark:text-neutral-400">
                    Total Points
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-3">
              <div className="flex items-center gap-2">
                <ChartBarIcon className="h-5 w-5 text-blue-500" />
                <div>
                  <div className="text-lg font-bold text-neutral-900 dark:text-neutral-100">
                    {state.questionsAnswered}
                  </div>
                  <div className="text-xs text-neutral-600 dark:text-neutral-400">
                    Questions
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-3">
              <div className="flex items-center gap-2">
                <StarIcon className="h-5 w-5 text-purple-500" />
                <div>
                  <div className={`text-sm font-medium px-2 py-1 rounded ${currentDifficultyInfo.color}`}>
                    {currentDifficultyInfo.name}
                  </div>
                  <div className="text-xs text-neutral-600 dark:text-neutral-400 mt-1">
                    Current Level
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-3">
              <div className="flex items-center gap-2">
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <CheckCircleSolid
                      key={i}
                      className={`h-4 w-4 ${
                        i < state.consecutiveCorrect 
                          ? 'text-green-500' 
                          : 'text-neutral-300 dark:text-neutral-600'
                      }`}
                    />
                  ))}
                </div>
                <div>
                  <div className="text-xs text-neutral-600 dark:text-neutral-400">
                    Streak
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Question content */}
      <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg">
        <div className="p-6">
          {/* Question header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <span className="text-sm font-medium text-neutral-500 dark:text-neutral-400">
                Question {state.questionsAnswered + 1}
              </span>
              <span className={`text-xs font-medium px-2 py-1 rounded ${currentDifficultyInfo.color}`}>
                {currentDifficultyInfo.name} • {currentDifficultyInfo.points} pts
              </span>
            </div>
            <div className="flex items-center gap-2 text-sm text-neutral-500 dark:text-neutral-400">
              <ClockIcon className="h-4 w-4" />
              <span>~{state.currentQuestion.estimated_time_seconds}s</span>
            </div>
          </div>

          {/* Question text */}
          <div className="mb-8">
            <h3 className="text-xl font-medium text-neutral-900 dark:text-neutral-100 mb-4 leading-relaxed">
              {state.currentQuestion.question_text}
            </h3>
          </div>

          {/* Answer options */}
          <div className="space-y-3 mb-8">
            {state.currentQuestion.options.map((option, index) => {
              const isSelected = state.selectedAnswer === option
              const isCorrect = state.lastResponse && option === state.currentQuestion?.correct_answer
              const isIncorrect = state.lastResponse && isSelected && !isCorrect
              
              let optionClass = 'w-full text-left p-4 rounded-lg border-2 transition-all '
              
              if (state.showExplanation) {
                if (isCorrect) {
                  optionClass += 'border-green-500 bg-green-50 dark:bg-green-900/20 text-green-900 dark:text-green-100'
                } else if (isIncorrect) {
                  optionClass += 'border-red-500 bg-red-50 dark:bg-red-900/20 text-red-900 dark:text-red-100'
                } else {
                  optionClass += 'border-neutral-200 dark:border-neutral-700 bg-neutral-50 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400'
                }
              } else {
                if (isSelected) {
                  optionClass += 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-900 dark:text-primary-100'
                } else {
                  optionClass += 'border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 hover:border-primary-300 hover:bg-primary-25 dark:hover:bg-primary-900/10'
                }
              }

              return (
                <button
                  key={index}
                  onClick={() => !state.showExplanation && setState(prev => ({ ...prev, selectedAnswer: option }))}
                  disabled={state.showExplanation || state.isLoading}
                  className={optionClass}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">
                      {String.fromCharCode(65 + index)}. {option}
                    </span>
                    {state.showExplanation && isCorrect && (
                      <CheckCircleIcon className="h-5 w-5 text-green-600" />
                    )}
                    {state.showExplanation && isIncorrect && (
                      <XCircleIcon className="h-5 w-5 text-red-600" />
                    )}
                  </div>
                </button>
              )
            })}
          </div>

          {/* Explanation section */}
          {state.showExplanation && state.lastResponse && (
            <div className="mb-6 p-4 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
              <div className="flex items-start gap-3 mb-3">
                <LightBulbIcon className="h-5 w-5 text-gold-500 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <h4 className="font-medium text-neutral-900 dark:text-neutral-100 mb-2">
                    Explanation
                  </h4>
                  <p className="text-sm text-neutral-700 dark:text-neutral-300">
                    {state.currentQuestion.explanation}
                  </p>
                </div>
              </div>
              
              {/* Points earned display */}
              <div className="mt-3 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {state.lastResponse.is_correct ? (
                    <CheckCircleIcon className="h-5 w-5 text-green-500" />
                  ) : (
                    <XCircleIcon className="h-5 w-5 text-red-500" />
                  )}
                  <span className="text-sm font-medium text-neutral-900 dark:text-neutral-100">
                    {state.lastResponse.is_correct ? 'Correct!' : 'Incorrect'}
                  </span>
                </div>
                
                {state.lastResponse.points_earned > 0 && (
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-neutral-600 dark:text-neutral-400">
                      Points earned:
                    </span>
                    <span className="font-bold text-primary-600 dark:text-primary-400">
                      +{state.lastResponse.points_earned}
                    </span>
                    {Object.keys(state.lastResponse.point_multipliers).length > 0 && (
                      <span className="text-xs text-gold-600 dark:text-gold-400">
                        (with bonuses)
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Action buttons */}
          <div className="flex items-center justify-between">
            <button
              onClick={exitAssessment}
              className="px-4 py-2 text-neutral-600 dark:text-neutral-400 hover:text-neutral-800 dark:hover:text-neutral-200 transition-colors"
            >
              Stop Assessment
            </button>

            <div className="flex items-center gap-3">
              {!state.showExplanation ? (
                <button
                  onClick={submitAnswer}
                  disabled={!state.selectedAnswer || state.isLoading}
                  className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-300 disabled:text-neutral-500 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                >
                  {state.isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      Submitting...
                    </>
                  ) : (
                    <>
                      Submit Answer
                      <ArrowRightIcon className="h-4 w-4" />
                    </>
                  )}
                </button>
              ) : (
                <button
                  onClick={nextQuestion}
                  disabled={state.isLoading}
                  className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-300 disabled:text-neutral-500 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                >
                  {state.isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      Loading...
                    </>
                  ) : (
                    <>
                      Next Question
                      <ArrowRightIcon className="h-4 w-4" />
                    </>
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdaptiveAssessment