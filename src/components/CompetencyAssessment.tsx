import React, { useState } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { questionTrackingService } from '../services/questionTrackingService'
import { Question } from '../types/database.types'
import {
  CheckCircleIcon,
  XCircleIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline'

interface CompetencyAssessmentProps {
  categoryId: string
  categoryName: string
  onComplete?: (score: number, passed: boolean) => void
}

const CompetencyAssessment: React.FC<CompetencyAssessmentProps> = ({
  categoryId,
  categoryName,
  onComplete
}) => {
  const { user } = useAuth()
  const [questions, setQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({})
  const [showResults, setShowResults] = useState(false)
  const [loading, setLoading] = useState(false)
  const [score, setScore] = useState(0)
  const [questionStartTime, setQuestionStartTime] = useState<number>(Date.now())

  const fetchAllDescendants = async (nodeId: string): Promise<any[]> => {
    const descendants: any[] = []
    
    const { data: children } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('parent_id', nodeId)

    if (children) {
      for (const child of children) {
        descendants.push(child)
        const childDescendants = await fetchAllDescendants(child.id)
        descendants.push(...childDescendants)
      }
    }

    return descendants
  }

  const fetchAssessmentQuestions = async () => {
    if (!user) return

    setLoading(true)
    try {
      // Get all descendant nodes with learning content
      const descendants = await fetchAllDescendants(categoryId)

      // Collect question IDs from all learning content in the category
      const allQuestionIds: string[] = []
      
      for (const node of descendants) {
        if (node.learning_content_ids?.length) {
          for (const contentId of node.learning_content_ids) {
            const { data: content } = await supabase
              .from('learning_content')
              .select('question_ids')
              .eq('id', contentId)
              .single()
            
            if (content?.question_ids) {
              allQuestionIds.push(...content.question_ids)
            }
          }
        }
      }

      if (allQuestionIds.length === 0) {
        setLoading(false)
        return
      }

      // Get unique question IDs
      const uniqueQuestionIds = Array.from(new Set(allQuestionIds))

      // Fetch all questions
      const { data: allQuestions, error: questionsError } = await supabase
        .from('questions')
        .select('*')
        .in('id', uniqueQuestionIds)

      if (questionsError) throw questionsError

      if (allQuestions && allQuestions.length > 0) {
        // Select optimal questions for assessment (5-10 questions)
        const assessmentQuestions = await questionTrackingService.selectOptimalQuestions(
          user.id,
          allQuestions,
          Math.min(10, allQuestions.length),
          'test'
        )
        
        setQuestions(assessmentQuestions)
        setQuestionStartTime(Date.now())
      }
    } catch (error) {
      console.error('Error fetching assessment questions:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerSelect = (questionIndex: number, answerIndex: number) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionIndex]: answerIndex
    }))
  }

  const handleNextQuestion = async () => {
    const currentQuestion = questions[currentQuestionIndex]
    const selectedAnswer = selectedAnswers[currentQuestionIndex]
    const isCorrect = selectedAnswer === currentQuestion.correct_answer

    if (user) {
      // Track the question attempt
      const timeTaken = (Date.now() - questionStartTime) / 1000
      await questionTrackingService.trackQuestionAttempt(
        user.id,
        currentQuestion.id,
        isCorrect,
        timeTaken
      )
    }

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1)
      setQuestionStartTime(Date.now())
    } else {
      // Calculate final score
      const correctCount = questions.reduce((count, question, index) => {
        return count + (selectedAnswers[index] === question.correct_answer ? 1 : 0)
      }, 0)
      
      const finalScore = Math.round((correctCount / questions.length) * 100)
      const passed = finalScore >= 70 // 70% pass rate
      
      setScore(finalScore)
      setShowResults(true)
      
      if (onComplete) {
        onComplete(finalScore, passed)
      }
    }
  }

  const resetAssessment = () => {
    setCurrentQuestionIndex(0)
    setSelectedAnswers({})
    setShowResults(false)
    setScore(0)
    setQuestions([])
  }

  if (loading) {
    return (
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
            <AcademicCapIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
          </div>
          <h2 className="text-xl font-bold text-neutral-900 dark:text-white">
            Competency Assessment
          </h2>
        </div>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-neutral-200 dark:bg-neutral-700 rounded w-3/4"></div>
          <div className="h-32 bg-neutral-200 dark:bg-neutral-700 rounded"></div>
        </div>
      </div>
    )
  }

  if (questions.length === 0) {
    return (
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
            <AcademicCapIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
          </div>
          <h2 className="text-xl font-bold text-neutral-900 dark:text-white">
            Competency Assessment
          </h2>
        </div>
        <p className="text-neutral-600 dark:text-neutral-400 mb-4">
          Test your knowledge of {categoryName} concepts
        </p>
        <button
          onClick={fetchAssessmentQuestions}
          className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium"
        >
          Start Assessment
        </button>
      </div>
    )
  }

  if (showResults) {
    const passed = score >= 70
    return (
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
        <div className="text-center">
          <div className={`mx-auto w-16 h-16 rounded-full flex items-center justify-center mb-4 ${
            passed ? 'bg-green-100 dark:bg-green-900/30' : 'bg-red-100 dark:bg-red-900/30'
          }`}>
            {passed ? (
              <CheckCircleIcon className="h-8 w-8 text-green-600 dark:text-green-400" />
            ) : (
              <XCircleIcon className="h-8 w-8 text-red-600 dark:text-red-400" />
            )}
          </div>
          <h3 className="text-2xl font-bold text-neutral-900 dark:text-white mb-2">
            Assessment {passed ? 'Passed' : 'Not Passed'}
          </h3>
          <p className="text-4xl font-bold mb-2">
            <span className={passed ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}>
              {score}%
            </span>
          </p>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            You answered {questions.reduce((count, question, index) => {
              return count + (selectedAnswers[index] === question.correct_answer ? 1 : 0)
            }, 0)} out of {questions.length} questions correctly
          </p>
          <div className="flex gap-3 justify-center">
            <button
              onClick={resetAssessment}
              className="bg-neutral-200 dark:bg-neutral-700 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-700 dark:text-neutral-300 px-4 py-2 rounded-lg font-medium"
            >
              Try Again
            </button>
            <button
              onClick={() => window.history.back()}
              className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium"
            >
              Continue Learning
            </button>
          </div>
        </div>
      </div>
    )
  }

  const currentQuestion = questions[currentQuestionIndex]
  const selectedAnswer = selectedAnswers[currentQuestionIndex]

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
            <AcademicCapIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
          </div>
          <h2 className="text-xl font-bold text-neutral-900 dark:text-white">
            Competency Assessment
          </h2>
        </div>
        <span className="text-sm text-neutral-500 dark:text-neutral-400">
          Question {currentQuestionIndex + 1} of {questions.length}
        </span>
      </div>

      <div className="mb-6">
        <div className="bg-neutral-100 dark:bg-neutral-700 rounded-full h-2 mb-4">
          <div 
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
          />
        </div>
      </div>

      <div className="space-y-6">
        <h3 className="text-lg font-medium text-neutral-900 dark:text-white">
          {currentQuestion.question_text}
        </h3>

        {currentQuestion.image_url && (
          <img 
            src={currentQuestion.image_url} 
            alt="Question illustration"
            className="max-w-full h-auto rounded-lg mx-auto"
          />
        )}

        <div className="space-y-3">
          {currentQuestion.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswerSelect(currentQuestionIndex, index)}
              className={`w-full text-left p-4 rounded-lg border transition-all ${
                selectedAnswer === index
                  ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                  : 'border-neutral-200 dark:border-neutral-700 hover:border-primary-300 hover:bg-neutral-50 dark:hover:bg-neutral-700'
              }`}
            >
              <span className="font-medium text-neutral-900 dark:text-white">
                {String.fromCharCode(65 + index)}. {option}
              </span>
            </button>
          ))}
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleNextQuestion}
            disabled={selectedAnswer === undefined}
            className="bg-primary-600 hover:bg-primary-700 disabled:bg-neutral-300 dark:disabled:bg-neutral-700 disabled:cursor-not-allowed text-white px-6 py-2 rounded-lg font-medium"
          >
            {currentQuestionIndex === questions.length - 1 ? 'Finish Assessment' : 'Next Question'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default CompetencyAssessment