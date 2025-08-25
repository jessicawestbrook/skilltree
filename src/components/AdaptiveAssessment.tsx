import React, { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { 
  AdaptiveAssessmentService, 
  Question, 
  AssessmentSession, 
  QuestionResponse 
} from '../services/adaptiveAssessmentService'
import { spacedRepetitionService } from '../services/spacedRepetitionService'
import QuestionDisplay from './QuestionDisplay'
import {
  TrophyIcon,
  ArrowRightIcon,
  LightBulbIcon,
  BoltIcon
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

  const handleAnswerSubmit = async (answer: string) => {
    if (!state.session || !state.currentQuestion) return

    const responseTime = Date.now() - state.startTime
    const isCorrect = answer === state.currentQuestion.correct_answer

    try {
      setState(prev => ({ ...prev, isLoading: true }))
      
      const response = await AdaptiveAssessmentService.recordResponse(
        state.session.id,
        state.currentQuestion.id,
        answer,
        isCorrect,
        responseTime
      )
      
      if (response) {
        const newConsecutiveCorrect = isCorrect ? state.consecutiveCorrect + 1 : 0
        
        setState(prev => ({
          ...prev,
          lastResponse: response,
          totalPoints: prev.totalPoints + (response.points_earned || 0),
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
    // Check if this is a completion or no questions available
    if (state.questionsAnswered > 0) {
      // Assessment completed
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
    } else {
      // No questions available
      return (
        <div className="max-w-4xl mx-auto p-6">
          <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-neutral-900 dark:text-neutral-100">
                {categoryName} Assessment
              </h2>
            </div>
            <div className="text-center py-8">
              <LightBulbIcon className="h-16 w-16 text-neutral-400 mx-auto mb-4" />
              <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-2">
                No assessment questions available yet
              </p>
              <p className="text-sm text-neutral-500 dark:text-neutral-500">
                Assessment questions for this category are being developed and will be available soon.
              </p>
            </div>
          </div>
        </div>
      )
    }
  }

  const currentDifficultyInfo = difficultyInfo[state.currentDifficulty as keyof typeof difficultyInfo] || difficultyInfo[2]

  return (
    <div className="flex flex-col bg-white dark:bg-neutral-800">
      {/* Header with stats */}
      <div className="bg-white dark:bg-neutral-900 border-b border-neutral-200 dark:border-neutral-700 p-2 flex-shrink-0">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <BoltIcon className="h-4 w-4 text-gold-500" />
            <div>
              <h1 className="text-sm font-bold text-neutral-900 dark:text-neutral-100">
                {categoryName} Assessment
              </h1>
            </div>
          </div>

          {/* Compact stats */}
          <div className="flex items-center gap-2">
            {/* Points */}
            <div className="flex items-center gap-1 px-2 py-0.5 bg-gold-50 dark:bg-gold-900/20 rounded-full">
              <TrophyIcon className="h-3.5 w-3.5 text-gold-600 dark:text-gold-400" />
              <span className="text-xs font-bold text-gold-700 dark:text-gold-300">
                {state.totalPoints}
              </span>
            </div>
            
            {/* Streak */}
            {state.consecutiveCorrect > 0 && (
              <div className="flex items-center gap-0.5">
                {[...Array(Math.min(state.consecutiveCorrect, 3))].map((_, i) => (
                  <CheckCircleSolid
                    key={i}
                    className="h-3.5 w-3.5 text-green-500"
                  />
                ))}
                {state.consecutiveCorrect > 3 && (
                  <span className="text-xs font-bold text-green-600 dark:text-green-400">
                    +{state.consecutiveCorrect - 3}
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Question content area - removed overflow-y-auto to let parent handle scrolling */}
      <div className="flex-1 p-3">
        <QuestionDisplay
          question={{
            id: state.currentQuestion.id,
            question_text: state.currentQuestion.question_text,
            options: state.currentQuestion.options,
            correct_answer: state.currentQuestion.correct_answer,
            explanation: state.currentQuestion.explanation,
            difficulty: currentDifficultyInfo.name.toLowerCase(),
            estimated_time_seconds: state.currentQuestion.estimated_time_seconds
          }}
          selectedAnswer={state.selectedAnswer}
          onAnswerSelect={(answer) => {
            setState(prev => ({ ...prev, selectedAnswer: answer as string }))
            // Auto-submit after selection
            setTimeout(() => {
              handleAnswerSubmit(answer as string)
            }, 100)
          }}
          showExplanation={state.showExplanation}
          isLoading={state.isLoading}
          questionNumber={state.questionsAnswered + 1}
          totalQuestions={undefined} // Don't show total for adaptive assessment
          questionType="assessment"
          points={state.lastResponse?.points_earned || currentDifficultyInfo.points}
          isCorrect={state.lastResponse?.is_correct}
          autoSubmit={true}
        />
        
        {/* Action buttons */}
        <div className="mt-3 flex items-center justify-between px-3 pb-3">
          <button
            onClick={exitAssessment}
            className="px-4 py-2 text-sm text-neutral-500 dark:text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 transition-colors"
          >
            Exit Assessment
          </button>

          {state.showExplanation && (
            <button
              onClick={nextQuestion}
              disabled={state.isLoading}
              className="px-5 py-2.5 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-xl hover:from-primary-700 hover:to-primary-800 disabled:from-neutral-300 disabled:to-neutral-400 disabled:text-neutral-500 disabled:cursor-not-allowed transition-all transform hover:scale-105 shadow-lg flex items-center gap-2 font-medium"
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
  )
}

export default AdaptiveAssessment