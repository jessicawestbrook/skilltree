import React, { useState, useEffect, useCallback } from 'react'
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline'
import { interestsQuizService, QuizQuestion, QuizResponse } from '../services/interestsQuizService'
import { useAuth } from '../contexts/AuthContext'

interface QuizAnswer {
  questionId: string
  answer: string | string[] | number
  question: QuizQuestion
}

const DynamicInterestsQuiz: React.FC = () => {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [quizSession, setQuizSession] = useState<QuizResponse | null>(null)
  const [primaryQuestions, setPrimaryQuestions] = useState<QuizQuestion[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [currentQuestion, setCurrentQuestion] = useState<QuizQuestion | null>(null)
  const [answers, setAnswers] = useState<QuizAnswer[]>([])
  const [followUpQueue, setFollowUpQueue] = useState<QuizQuestion[]>([])
  const [currentAnswer, setCurrentAnswer] = useState<any>(null)
  const [, setSubmitting] = useState(false)
  const [completed, setCompleted] = useState(false)

  const initializeQuiz = useCallback(async () => {
    if (!user) return

    setLoading(true)
    try {
      // Get or create quiz session
      const sessionData = await interestsQuizService.getOrCreateQuizSession(user.id)
      if (!sessionData) {
        console.error('Failed to create quiz session')
        return
      }

      setQuizSession(sessionData.response)

      // Load primary questions
      const questions = await interestsQuizService.getPrimaryQuizQuestions()
      setPrimaryQuestions(questions)

      // If resuming, load previous answers
      if (!sessionData.isNew && sessionData.answers.length > 0) {
        // Convert saved answers to our format
        const savedAnswers: QuizAnswer[] = []
        for (const ans of sessionData.answers) {
          const question = questions.find(q => q.id === ans.question_id)
          if (question) {
            savedAnswers.push({
              questionId: ans.question_id,
              answer: JSON.parse(ans.answer_value),
              question
            })
          }
        }
        setAnswers(savedAnswers)
        setCurrentQuestionIndex(savedAnswers.length)
      }

      // Set first question
      if (questions.length > 0) {
        setCurrentQuestion(questions[0])
      }
    } catch (error) {
      console.error('Error initializing quiz:', error)
    } finally {
      setLoading(false)
    }
  }, [user])

  useEffect(() => {
    if (user) {
      initializeQuiz()
    }
  }, [user, initializeQuiz])

  const handleAnswer = async () => {
    if (!currentQuestion || currentAnswer === null || !quizSession) return

    // Save current answer
    const newAnswer: QuizAnswer = {
      questionId: currentQuestion.id,
      answer: currentAnswer,
      question: currentQuestion
    }
    
    const updatedAnswers = [...answers, newAnswer]
    setAnswers(updatedAnswers)

    // Save to database
    await interestsQuizService.saveAnswer(
      quizSession.id,
      currentQuestion.id,
      currentAnswer
    )

    // Check for follow-up questions
    const followUps = await interestsQuizService.getFollowUpQuestions(
      currentQuestion.id,
      currentAnswer
    )

    if (followUps.length > 0) {
      // Add follow-ups to queue
      setFollowUpQueue(prev => [...prev, ...followUps])
    }

    // Move to next question
    nextQuestion()
  }

  const nextQuestion = () => {
    // First check if there are follow-up questions in queue
    if (followUpQueue.length > 0) {
      const [nextFollowUp, ...remainingFollowUps] = followUpQueue
      setCurrentQuestion(nextFollowUp)
      setFollowUpQueue(remainingFollowUps)
      setCurrentAnswer(null)
      return
    }

    // Otherwise move to next primary question
    const nextIndex = currentQuestionIndex + 1
    if (nextIndex < primaryQuestions.length) {
      setCurrentQuestionIndex(nextIndex)
      setCurrentQuestion(primaryQuestions[nextIndex])
      setCurrentAnswer(null)
    } else {
      // Quiz completed
      completeQuiz()
    }
  }

  const completeQuiz = async () => {
    if (!quizSession) return

    setSubmitting(true)
    try {
      await interestsQuizService.completeQuizSession(quizSession.id)
      setCompleted(true)
    } catch (error) {
      console.error('Error completing quiz:', error)
    } finally {
      setSubmitting(false)
    }
  }

  const previousQuestion = () => {
    if (answers.length === 0) return

    // Remove last answer and go back
    const updatedAnswers = answers.slice(0, -1)
    setAnswers(updatedAnswers)

    // Find the previous question
    const lastAnswer = answers[answers.length - 1]
    setCurrentQuestion(lastAnswer.question)
    setCurrentAnswer(lastAnswer.answer)
    
    // Adjust index if it was a primary question
    const primaryIndex = primaryQuestions.findIndex(q => q.id === lastAnswer.question.id)
    if (primaryIndex !== -1) {
      setCurrentQuestionIndex(primaryIndex)
    }
  }

  const renderQuestionInput = () => {
    if (!currentQuestion) return null

    switch (currentQuestion.question_type) {
      case 'multiple_choice':
        return (
          <div className="space-y-3">
            {currentQuestion.options.map((option: string) => (
              <label
                key={option}
                className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
              >
                <input
                  type="radio"
                  name="answer"
                  value={option}
                  checked={currentAnswer === option}
                  onChange={(e) => setCurrentAnswer(e.target.value)}
                  className="mr-3"
                />
                <span className="text-neutral-700 dark:text-neutral-300">{option}</span>
              </label>
            ))}
          </div>
        )

      case 'multi_select':
        return (
          <div className="space-y-3">
            {currentQuestion.options.map((option: string) => (
              <label
                key={option}
                className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
              >
                <input
                  type="checkbox"
                  value={option}
                  checked={Array.isArray(currentAnswer) && currentAnswer.includes(option)}
                  onChange={(e) => {
                    const value = e.target.value
                    if (e.target.checked) {
                      setCurrentAnswer((prev: string | string[] | number | null) => 
                        Array.isArray(prev) ? [...prev, value] : [value]
                      )
                    } else {
                      setCurrentAnswer((prev: string | string[] | number | null) => 
                        Array.isArray(prev) ? prev.filter((v: string) => v !== value) : []
                      )
                    }
                  }}
                  className="mr-3"
                />
                <span className="text-neutral-700 dark:text-neutral-300">{option}</span>
              </label>
            ))}
          </div>
        )

      case 'scale':
        const scaleOptions = currentQuestion.options
        return (
          <div className="space-y-4">
            <div className="flex justify-between text-sm text-neutral-600 dark:text-neutral-400">
              <span>{scaleOptions.labels?.[0] || 'Min'}</span>
              <span>{scaleOptions.labels?.[scaleOptions.labels.length - 1] || 'Max'}</span>
            </div>
            <input
              type="range"
              min={scaleOptions.min || 1}
              max={scaleOptions.max || 5}
              value={currentAnswer || scaleOptions.min || 1}
              onChange={(e) => setCurrentAnswer(parseInt(e.target.value))}
              className="w-full"
            />
            <div className="text-center">
              <span className="text-2xl font-bold text-primary-600">
                {currentAnswer || scaleOptions.min || 1}
              </span>
              {scaleOptions.labels && (
                <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-1">
                  {scaleOptions.labels[currentAnswer - (scaleOptions.min || 1)]}
                </p>
              )}
            </div>
          </div>
        )

      case 'text':
        return (
          <textarea
            value={currentAnswer || ''}
            onChange={(e) => setCurrentAnswer(e.target.value)}
            className="w-full p-4 border rounded-lg dark:bg-neutral-800 dark:border-neutral-700"
            rows={4}
            placeholder="Type your answer here..."
          />
        )

      default:
        return null
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (completed) {
    return (
      <div className="text-center py-12">
        <div className="mb-6">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 dark:bg-green-900/30 rounded-full mb-4">
            <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
        <h2 className="text-3xl font-bold mb-4">Quiz Completed!</h2>
        <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-8">
          Thank you for completing the interests assessment. We're now personalizing your learning experience.
        </p>
        <button
          onClick={() => window.location.href = '/profile'}
          className="btn-primary"
        >
          View Your Personalized Recommendations
        </button>
      </div>
    )
  }

  if (!currentQuestion) {
    return <div>No questions available</div>
  }

  const progress = ((answers.length) / (primaryQuestions.length + followUpQueue.length)) * 100
  const isFollowUp = currentQuestion.is_follow_up

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress bar */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-neutral-600 dark:text-neutral-400 mb-2">
          <span>Question {answers.length + 1}</span>
          <span>{Math.round(progress)}% Complete</span>
        </div>
        <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
          <div
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question */}
      <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-lg p-8">
        {isFollowUp && (
          <div className="inline-block px-3 py-1 bg-secondary-100 dark:bg-secondary-900/30 text-secondary-700 dark:text-secondary-300 rounded-full text-sm font-medium mb-4">
            Follow-up Question
          </div>
        )}
        
        <h3 className="text-xl font-semibold mb-6">
          {currentQuestion.question_text}
        </h3>

        {renderQuestionInput()}

        {/* Navigation buttons */}
        <div className="flex justify-between mt-8">
          <button
            onClick={previousQuestion}
            disabled={answers.length === 0}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeftIcon className="h-5 w-5 mr-2" />
            Previous
          </button>

          <button
            onClick={handleAnswer}
            disabled={currentAnswer === null || (Array.isArray(currentAnswer) && currentAnswer.length === 0)}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {currentQuestionIndex === primaryQuestions.length - 1 && followUpQueue.length === 0
              ? 'Complete'
              : 'Next'}
            <ChevronRightIcon className="h-5 w-5 ml-2" />
          </button>
        </div>
      </div>

      {/* Skip button for follow-ups */}
      {isFollowUp && (
        <div className="text-center mt-4">
          <button
            onClick={nextQuestion}
            className="text-neutral-600 dark:text-neutral-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm"
          >
            Skip this question
          </button>
        </div>
      )}
    </div>
  )
}

export default DynamicInterestsQuiz