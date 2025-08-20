import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import { 
  ClockIcon, 
  AcademicCapIcon,
  ChartBarIcon,
  PlayIcon,
  PauseIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'

interface IQQuestion {
  id: string
  question_text: string
  image_url?: string
  options: string[]
  correct_answer: number
  difficulty: 'easy' | 'medium' | 'hard'
  category: 'pattern' | 'spatial' | 'verbal' | 'numerical' | 'logical'
  time_limit: number // seconds
  source_url?: string
}

interface TestResult {
  score: number
  percentile: number
  category_scores: Record<string, number>
  time_taken: number
  date: Date
}

const IQTestPage: React.FC = () => {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [testPhase, setTestPhase] = useState<'intro' | 'test' | 'results'>('intro')
  const [questions, setQuestions] = useState<IQQuestion[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState<(number | null)[]>([])
  const [timeRemaining, setTimeRemaining] = useState(0)
  const [totalTimeElapsed, setTotalTimeElapsed] = useState(0)
  const [isPaused, setIsPaused] = useState(false)
  const [testResult, setTestResult] = useState<TestResult | null>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  // Sample IQ test questions (in production, these would come from the database)
  const sampleQuestions: IQQuestion[] = [
    {
      id: '1',
      question_text: 'Which number should come next in the pattern? 2, 4, 8, 16, ?',
      options: ['24', '32', '48', '64'],
      correct_answer: 1,
      difficulty: 'easy',
      category: 'numerical',
      time_limit: 30
    },
    {
      id: '2',
      question_text: 'Complete the pattern: A, C, F, J, ?',
      options: ['M', 'N', 'O', 'P'],
      correct_answer: 2,
      difficulty: 'medium',
      category: 'pattern',
      time_limit: 45
    },
    {
      id: '3',
      question_text: 'If all roses are flowers and some flowers fade quickly, which statement must be true?',
      options: [
        'All roses fade quickly',
        'Some roses fade quickly',
        'No roses fade quickly',
        'Some roses might fade quickly'
      ],
      correct_answer: 3,
      difficulty: 'hard',
      category: 'logical',
      time_limit: 60
    },
    {
      id: '4',
      question_text: 'Which word does not belong in the group? Apple, Orange, Banana, Carrot, Grape',
      options: ['Apple', 'Orange', 'Carrot', 'Grape'],
      correct_answer: 2,
      difficulty: 'easy',
      category: 'verbal',
      time_limit: 30
    },
    {
      id: '5',
      question_text: 'If a cube is painted red on all sides and then cut into 27 equal smaller cubes, how many smaller cubes will have exactly 2 red faces?',
      options: ['6', '8', '12', '16'],
      correct_answer: 2,
      difficulty: 'hard',
      category: 'spatial',
      time_limit: 90
    }
  ]

  useEffect(() => {
    // Initialize with sample questions
    setQuestions(sampleQuestions)
    setSelectedAnswers(new Array(sampleQuestions.length).fill(null))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (testPhase === 'test' && !isPaused && timeRemaining > 0) {
      intervalRef.current = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            handleNextQuestion()
            return 0
          }
          return prev - 1
        })
        setTotalTimeElapsed(prev => prev + 1)
      }, 1000)
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [testPhase, isPaused, timeRemaining])

  const startTest = () => {
    setTestPhase('test')
    setCurrentQuestionIndex(0)
    setTimeRemaining(questions[0]?.time_limit || 30)
    setTotalTimeElapsed(0)
    setSelectedAnswers(new Array(questions.length).fill(null))
  }

  const handleSelectAnswer = (optionIndex: number) => {
    const newAnswers = [...selectedAnswers]
    newAnswers[currentQuestionIndex] = optionIndex
    setSelectedAnswers(newAnswers)
  }

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1)
      setTimeRemaining(questions[currentQuestionIndex + 1].time_limit)
    } else {
      finishTest()
    }
  }

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1)
      setTimeRemaining(questions[currentQuestionIndex - 1].time_limit)
    }
  }

  const finishTest = async () => {
    setTestPhase('results')
    
    // Calculate scores
    let correctCount = 0
    const categoryScores: Record<string, { correct: number; total: number }> = {}
    
    questions.forEach((q, index) => {
      if (!categoryScores[q.category]) {
        categoryScores[q.category] = { correct: 0, total: 0 }
      }
      categoryScores[q.category].total++
      
      if (selectedAnswers[index] === q.correct_answer) {
        correctCount++
        categoryScores[q.category].correct++
      }
    })
    
    const overallScore = Math.round((correctCount / questions.length) * 100)
    const iqScore = Math.round(85 + (overallScore / 100) * 30) // Simplified IQ calculation
    
    // Calculate category percentages
    const categoryPercentages: Record<string, number> = {}
    Object.keys(categoryScores).forEach(cat => {
      categoryPercentages[cat] = Math.round(
        (categoryScores[cat].correct / categoryScores[cat].total) * 100
      )
    })
    
    const result: TestResult = {
      score: iqScore,
      percentile: calculatePercentile(iqScore),
      category_scores: categoryPercentages,
      time_taken: totalTimeElapsed,
      date: new Date()
    }
    
    setTestResult(result)
    
    // Save result to database if user is logged in
    if (user) {
      try {
        await supabase.from('iq_test_results').insert({
          user_id: user.id,
          score: iqScore,
          percentile: result.percentile,
          category_scores: categoryPercentages,
          time_taken: totalTimeElapsed,
          questions_answered: selectedAnswers.filter(a => a !== null).length,
          total_questions: questions.length
        })
      } catch (error) {
        console.error('Error saving test result:', error)
      }
    }
  }

  const calculatePercentile = (iqScore: number): number => {
    // Simplified percentile calculation based on normal distribution
    if (iqScore >= 130) return 98
    if (iqScore >= 120) return 91
    if (iqScore >= 110) return 75
    if (iqScore >= 100) return 50
    if (iqScore >= 90) return 25
    if (iqScore >= 80) return 9
    return 2
  }

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (testPhase === 'intro') {
    return (
      <div className="max-w-4xl mx-auto py-8">
        <div className="card">
          <div className="text-center mb-8">
            <AcademicCapIcon className="h-16 w-16 text-primary-600 mx-auto mb-4" />
            <h1 className="text-3xl font-bold mb-2">IQ Test</h1>
            <p className="text-neutral-600 dark:text-neutral-400">
              Test your cognitive abilities across multiple dimensions
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-6">
              <h3 className="font-semibold mb-3">What to Expect</h3>
              <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  {questions.length} carefully designed questions
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Timed questions with varying difficulty
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Categories: Pattern Recognition, Spatial, Verbal, Numerical, Logical
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Detailed results with category breakdown
                </li>
              </ul>
            </div>

            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-6">
              <h3 className="font-semibold mb-3">Test Rules</h3>
              <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                <li className="flex items-start">
                  <span className="text-gold-600 mr-2">•</span>
                  Each question has a time limit
                </li>
                <li className="flex items-start">
                  <span className="text-gold-600 mr-2">•</span>
                  You can navigate between questions
                </li>
                <li className="flex items-start">
                  <span className="text-gold-600 mr-2">•</span>
                  No external help or calculators
                </li>
                <li className="flex items-start">
                  <span className="text-gold-600 mr-2">•</span>
                  Results are calculated immediately
                </li>
              </ul>
            </div>
          </div>

          <div className="text-center">
            <button onClick={startTest} className="btn-primary">
              <PlayIcon className="h-5 w-5 mr-2" />
              Start IQ Test
            </button>
            <p className="text-xs text-neutral-500 mt-4">
              Estimated time: 10-15 minutes
            </p>
          </div>
        </div>
      </div>
    )
  }

  if (testPhase === 'test') {
    const currentQuestion = questions[currentQuestionIndex]
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100

    return (
      <div className="max-w-3xl mx-auto py-8">
        <div className="card">
          {/* Progress Bar */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium">
                Question {currentQuestionIndex + 1} of {questions.length}
              </span>
              <span className="text-sm text-neutral-600 dark:text-neutral-400">
                {currentQuestion.category} • {currentQuestion.difficulty}
              </span>
            </div>
            <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
              <div 
                className="bg-primary-600 h-2 rounded-full transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Timer */}
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center gap-2">
              <ClockIcon className="h-5 w-5 text-neutral-500" />
              <span className={`font-mono text-lg ${
                timeRemaining <= 10 ? 'text-red-600' : 'text-neutral-700 dark:text-neutral-300'
              }`}>
                {formatTime(timeRemaining)}
              </span>
            </div>
            <button
              onClick={() => setIsPaused(!isPaused)}
              className="p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700"
            >
              {isPaused ? <PlayIcon className="h-5 w-5" /> : <PauseIcon className="h-5 w-5" />}
            </button>
          </div>

          {/* Question */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-4">{currentQuestion.question_text}</h2>
            {currentQuestion.image_url && (
              <img 
                src={currentQuestion.image_url} 
                alt="Question visual"
                className="w-full max-w-md mx-auto rounded-lg mb-4"
              />
            )}
          </div>

          {/* Options */}
          <div className="space-y-3 mb-8">
            {currentQuestion.options.map((option, index) => (
              <button
                key={index}
                onClick={() => handleSelectAnswer(index)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                  selectedAnswers[currentQuestionIndex] === index
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                    : 'border-neutral-200 dark:border-neutral-600 hover:border-neutral-300 dark:hover:border-neutral-500'
                }`}
              >
                <div className="flex items-center">
                  <span className="w-8 h-8 rounded-full border-2 mr-3 flex items-center justify-center text-sm font-medium">
                    {String.fromCharCode(65 + index)}
                  </span>
                  <span>{option}</span>
                </div>
              </button>
            ))}
          </div>

          {/* Source URL Display */}
          {currentQuestion.source_url && (
            <div className="bg-neutral-50 dark:bg-neutral-900 p-3 rounded-lg border-l-4 border-primary-500 mb-6">
              <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-1">Source:</p>
              <a 
                href={currentQuestion.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-primary-600 dark:text-primary-400 hover:underline break-all"
              >
                {currentQuestion.source_url}
              </a>
            </div>
          )}

          {/* Navigation */}
          <div className="flex justify-between">
            <button
              onClick={handlePreviousQuestion}
              disabled={currentQuestionIndex === 0}
              className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            {currentQuestionIndex === questions.length - 1 ? (
              <button onClick={finishTest} className="btn-primary">
                Finish Test
              </button>
            ) : (
              <button onClick={handleNextQuestion} className="btn-primary">
                Next Question
              </button>
            )}
          </div>
        </div>
      </div>
    )
  }

  // Results phase
  if (testResult) {
    return (
      <div className="max-w-4xl mx-auto py-8">
        <div className="card">
          <div className="text-center mb-8">
            <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold mb-2">Test Complete!</h1>
            <p className="text-neutral-600 dark:text-neutral-400">
              Here are your results
            </p>
          </div>

          {/* IQ Score */}
          <div className="bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl p-8 mb-8 text-center">
            <h2 className="text-lg mb-2">Your IQ Score</h2>
            <div className="text-6xl font-bold mb-2">{testResult.score}</div>
            <p className="text-primary-100">
              {testResult.percentile}th Percentile
            </p>
          </div>

          {/* Category Breakdown */}
          <div className="mb-8">
            <h3 className="font-semibold mb-4">Performance by Category</h3>
            <div className="space-y-3">
              {Object.entries(testResult.category_scores).map(([category, score]) => (
                <div key={category}>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium capitalize">
                      {category.replace('_', ' ')}
                    </span>
                    <span className="text-sm text-neutral-600 dark:text-neutral-400">
                      {score}%
                    </span>
                  </div>
                  <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full transition-all ${
                        score >= 80 ? 'bg-green-500' :
                        score >= 60 ? 'bg-gold-500' :
                        score >= 40 ? 'bg-orange-500' :
                        'bg-red-500'
                      }`}
                      style={{ width: `${score}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Statistics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-4 text-center">
              <ChartBarIcon className="h-8 w-8 text-primary-600 mx-auto mb-2" />
              <p className="text-2xl font-bold">{testResult.score}</p>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">IQ Score</p>
            </div>
            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-4 text-center">
              <ClockIcon className="h-8 w-8 text-gold-600 mx-auto mb-2" />
              <p className="text-2xl font-bold">{formatTime(testResult.time_taken)}</p>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Time Taken</p>
            </div>
            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-4 text-center">
              <CheckCircleIcon className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <p className="text-2xl font-bold">
                {selectedAnswers.filter(a => a !== null).length}/{questions.length}
              </p>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Answered</p>
            </div>
            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-4 text-center">
              <AcademicCapIcon className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <p className="text-2xl font-bold">{testResult.percentile}%</p>
              <p className="text-xs text-neutral-600 dark:text-neutral-400">Percentile</p>
            </div>
          </div>

          {/* Interpretation */}
          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 mb-8">
            <h3 className="font-semibold mb-2">Score Interpretation</h3>
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
              {testResult.score >= 130 ? 'Exceptional! Your score indicates very superior intelligence.' :
               testResult.score >= 120 ? 'Excellent! Your score indicates superior intelligence.' :
               testResult.score >= 110 ? 'Great! Your score indicates above average intelligence.' :
               testResult.score >= 90 ? 'Good! Your score indicates average intelligence.' :
               'Your score indicates room for improvement. Keep practicing!'}
            </p>
            <p className="text-xs text-neutral-500">
              Note: This is a simplified IQ test for practice. Professional assessments provide more comprehensive evaluations.
            </p>
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <button onClick={() => navigate('/skill-tree')} className="btn-secondary flex-1">
              Back to Skill Tree
            </button>
            <button onClick={() => window.location.reload()} className="btn-primary flex-1">
              Take Another Test
            </button>
          </div>
        </div>
      </div>
    )
  }

  return null
}

export default IQTestPage