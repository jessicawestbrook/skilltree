import React, { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import {
  AcademicCapIcon,
  ChartBarIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowRightIcon,
  ClockIcon,
  SparklesIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline'

interface AssessmentQuestion {
  id: string
  category: string
  subcategory: string
  difficulty: number
  question: string
  options: string[]
  correctIndex: number
  explanation: string
  skillNodeId?: string
}

interface CategoryScore {
  category: string
  correct: number
  total: number
  percentage: number
  difficulty: number
  recommendedNodes: string[]
}

interface AssessmentResult {
  overallScore: number
  strengths: string[]
  weaknesses: string[]
  recommendedPath: string[]
  categoryScores: CategoryScore[]
}

const IntroAssessmentPage: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [userAnswers, setUserAnswers] = useState<Array<{ questionId: string, selectedIndex: number, isCorrect: boolean }>>([])
  const [showExplanation, setShowExplanation] = useState(false)
  const [assessmentResult, setAssessmentResult] = useState<AssessmentResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [startTime] = useState(new Date())
  const [phase, setPhase] = useState<'intro' | 'assessment' | 'results'>('intro')

  const generateAssessmentQuestions = useCallback((): AssessmentQuestion[] => {
    // Generate a diverse set of assessment questions across different categories
    return [
      // Mathematics
      {
        id: '1',
        category: 'Mathematics',
        subcategory: 'Algebra',
        difficulty: 2,
        question: 'Solve for x: 2x + 5 = 13',
        options: ['x = 3', 'x = 4', 'x = 6', 'x = 9'],
        correctIndex: 1,
        explanation: 'Subtract 5 from both sides: 2x = 8, then divide by 2: x = 4',
        skillNodeId: 'algebra-basic'
      },
      {
        id: '2',
        category: 'Mathematics',
        subcategory: 'Geometry',
        difficulty: 2,
        question: 'What is the area of a triangle with base 6 and height 8?',
        options: ['24', '48', '14', '30'],
        correctIndex: 0,
        explanation: 'Area of triangle = (base × height) / 2 = (6 × 8) / 2 = 24',
        skillNodeId: 'geometry-area'
      },
      
      // Science
      {
        id: '3',
        category: 'Science',
        subcategory: 'Biology',
        difficulty: 2,
        question: 'What is the powerhouse of the cell?',
        options: ['Nucleus', 'Mitochondria', 'Ribosome', 'Chloroplast'],
        correctIndex: 1,
        explanation: 'Mitochondria are known as the powerhouse of the cell because they generate ATP (energy).',
        skillNodeId: 'cell-biology'
      },
      {
        id: '4',
        category: 'Science',
        subcategory: 'Physics',
        difficulty: 3,
        question: "According to Newton's second law, Force equals:",
        options: ['Mass × Velocity', 'Mass × Acceleration', 'Weight × Speed', 'Energy × Time'],
        correctIndex: 1,
        explanation: "Newton's second law states that Force = Mass × Acceleration (F = ma)",
        skillNodeId: 'physics-mechanics'
      },
      
      // Language Arts
      {
        id: '5',
        category: 'Language Arts',
        subcategory: 'Grammar',
        difficulty: 2,
        question: 'Which sentence uses correct grammar?',
        options: [
          'Me and him went to the store.',
          'Him and I went to the store.',
          'He and I went to the store.',
          'He and me went to the store.'
        ],
        correctIndex: 2,
        explanation: 'Use subject pronouns (He and I) when they are the subject of the sentence.',
        skillNodeId: 'grammar-pronouns'
      },
      {
        id: '6',
        category: 'Language Arts',
        subcategory: 'Vocabulary',
        difficulty: 3,
        question: 'What does "ubiquitous" mean?',
        options: ['Rare', 'Present everywhere', 'Mysterious', 'Ancient'],
        correctIndex: 1,
        explanation: 'Ubiquitous means present, appearing, or found everywhere.',
        skillNodeId: 'vocabulary-advanced'
      },
      
      // History
      {
        id: '7',
        category: 'History',
        subcategory: 'World History',
        difficulty: 2,
        question: 'In which year did World War II end?',
        options: ['1943', '1944', '1945', '1946'],
        correctIndex: 2,
        explanation: 'World War II ended in 1945 with the surrender of Japan in September.',
        skillNodeId: 'world-war-2'
      },
      {
        id: '8',
        category: 'History',
        subcategory: 'Ancient History',
        difficulty: 3,
        question: 'Which ancient civilization built Machu Picchu?',
        options: ['Aztec', 'Maya', 'Inca', 'Olmec'],
        correctIndex: 2,
        explanation: 'The Inca civilization built Machu Picchu in the 15th century in Peru.',
        skillNodeId: 'ancient-civilizations'
      },
      
      // Technology
      {
        id: '9',
        category: 'Technology',
        subcategory: 'Computer Science',
        difficulty: 2,
        question: 'What does HTML stand for?',
        options: [
          'Hyper Text Markup Language',
          'High Tech Modern Language',
          'Home Tool Markup Language',
          'Hyperlink and Text Markup Language'
        ],
        correctIndex: 0,
        explanation: 'HTML stands for Hyper Text Markup Language, used for creating web pages.',
        skillNodeId: 'web-development'
      },
      {
        id: '10',
        category: 'Technology',
        subcategory: 'Programming',
        difficulty: 3,
        question: 'Which of these is NOT a programming language?',
        options: ['Python', 'Java', 'HTML', 'C++'],
        correctIndex: 2,
        explanation: 'HTML is a markup language for structuring content, not a programming language.',
        skillNodeId: 'programming-basics'
      },
      
      // Critical Thinking
      {
        id: '11',
        category: 'Logic',
        subcategory: 'Pattern Recognition',
        difficulty: 3,
        question: 'What comes next in the sequence: 2, 6, 12, 20, 30, ?',
        options: ['40', '42', '44', '36'],
        correctIndex: 1,
        explanation: 'The pattern is n×(n+1): 1×2=2, 2×3=6, 3×4=12, 4×5=20, 5×6=30, 6×7=42',
        skillNodeId: 'pattern-recognition'
      },
      {
        id: '12',
        category: 'Logic',
        subcategory: 'Problem Solving',
        difficulty: 4,
        question: 'If all roses are flowers, and some flowers fade quickly, which must be true?',
        options: [
          'All roses fade quickly',
          'Some roses fade quickly',
          'No roses fade quickly',
          'Cannot be determined'
        ],
        correctIndex: 3,
        explanation: 'We cannot determine if roses fade quickly based on the given information.',
        skillNodeId: 'logical-reasoning'
      }
    ]
  }, [])

  useEffect(() => {
    const loadedQuestions = generateAssessmentQuestions()
    setQuestions(loadedQuestions)
    setLoading(false)
  }, [generateAssessmentQuestions])

  const handleStartAssessment = () => {
    setPhase('assessment')
    if (user) {
      // Log assessment start
      supabase.from('assessment_attempts').insert({
        user_id: user.id,
        type: 'intro',
        started_at: startTime
      })
    }
  }

  const handleAnswerSelect = (index: number) => {
    setSelectedAnswer(index)
  }

  const handleSubmitAnswer = () => {
    if (selectedAnswer === null) return

    const currentQuestion = questions[currentQuestionIndex]
    const isCorrect = selectedAnswer === currentQuestion.correctIndex

    setUserAnswers([...userAnswers, {
      questionId: currentQuestion.id,
      selectedIndex: selectedAnswer,
      isCorrect
    }])

    setShowExplanation(true)

    // Save answer if user is logged in
    if (user) {
      supabase.from('assessment_answers').insert({
        user_id: user.id,
        question_id: currentQuestion.id,
        selected_answer: selectedAnswer,
        is_correct: isCorrect,
        category: currentQuestion.category,
        difficulty: currentQuestion.difficulty
      })
    }
  }

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setSelectedAnswer(null)
      setShowExplanation(false)
    } else {
      calculateResults()
    }
  }

  const calculateResults = () => {
    const categoryMap = new Map<string, CategoryScore>()
    
    // Group answers by category
    questions.forEach((question, index) => {
      const answer = userAnswers[index]
      if (!answer) return

      if (!categoryMap.has(question.category)) {
        categoryMap.set(question.category, {
          category: question.category,
          correct: 0,
          total: 0,
          percentage: 0,
          difficulty: 0,
          recommendedNodes: []
        })
      }

      const categoryScore = categoryMap.get(question.category)!
      categoryScore.total++
      if (answer.isCorrect) {
        categoryScore.correct++
      }
      categoryScore.difficulty += question.difficulty
    })

    // Calculate percentages and identify strengths/weaknesses
    const categoryScores = Array.from(categoryMap.values())
    const strengths: string[] = []
    const weaknesses: string[] = []
    const recommendedPath: string[] = []

    categoryScores.forEach(score => {
      score.percentage = (score.correct / score.total) * 100
      score.difficulty = score.difficulty / score.total

      if (score.percentage >= 80) {
        strengths.push(score.category)
        // Recommend advanced topics in strong areas
        recommendedPath.push(`Advanced ${score.category}`)
      } else if (score.percentage <= 40) {
        weaknesses.push(score.category)
        // Recommend foundational topics in weak areas
        recommendedPath.push(`${score.category} Fundamentals`)
      } else {
        // Recommend intermediate topics
        recommendedPath.push(`${score.category} Practice`)
      }
    })

    const overallScore = (userAnswers.filter(a => a.isCorrect).length / questions.length) * 100

    const result: AssessmentResult = {
      overallScore,
      strengths,
      weaknesses,
      recommendedPath,
      categoryScores
    }

    setAssessmentResult(result)
    setPhase('results')

    // Save results if user is logged in
    if (user) {
      supabase.from('assessment_results').insert({
        user_id: user.id,
        type: 'intro',
        overall_score: overallScore,
        strengths,
        weaknesses,
        recommended_path: recommendedPath,
        category_scores: categoryScores,
        completed_at: new Date()
      })
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (phase === 'intro') {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
              <SparklesIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
            </div>
            <h1 className="text-4xl font-bold mb-4">
              <span className="text-primary-600 dark:text-primary-400">
                Skill Assessment Test
              </span>
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Discover your strengths and get personalized learning recommendations
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-full mb-3">
                <ClockIcon className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="font-semibold mb-1">15-20 Minutes</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Quick assessment across multiple subjects
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-full mb-3">
                <ChartBarIcon className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="font-semibold mb-1">Adaptive Difficulty</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Questions match your skill level
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-full mb-3">
                <LightBulbIcon className="h-6 w-6 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="font-semibold mb-1">Personalized Path</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Get custom learning recommendations
              </p>
            </div>
          </div>

          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
              What to Expect:
            </h3>
            <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-400">
              <li className="flex items-start gap-2">
                <span className="text-blue-600 dark:text-blue-500 mt-0.5">•</span>
                <span>Questions across Mathematics, Science, Language Arts, History, Technology, and Logic</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 dark:text-blue-500 mt-0.5">•</span>
                <span>No penalty for wrong answers - this helps us understand where to focus</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 dark:text-blue-500 mt-0.5">•</span>
                <span>Immediate feedback with explanations for each question</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 dark:text-blue-500 mt-0.5">•</span>
                <span>Detailed results showing your strengths and areas for improvement</span>
              </li>
            </ul>
          </div>

          <button
            onClick={handleStartAssessment}
            className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
          >
            Start Assessment
          </button>
        </div>
      </div>
    )
  }

  if (phase === 'results' && assessmentResult) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold mb-2">Assessment Complete!</h1>
            <p className="text-xl text-neutral-600 dark:text-neutral-400">
              Overall Score: {assessmentResult.overallScore.toFixed(0)}%
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            {/* Strengths */}
            <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6">
              <h3 className="font-semibold text-green-900 dark:text-green-300 mb-4 flex items-center gap-2">
                <CheckCircleIcon className="h-5 w-5" />
                Your Strengths
              </h3>
              {assessmentResult.strengths.length > 0 ? (
                <ul className="space-y-2">
                  {assessmentResult.strengths.map(strength => (
                    <li key={strength} className="flex items-center gap-2">
                      <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                      <span className="text-sm">{strength}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  Keep practicing to identify your strengths!
                </p>
              )}
            </div>

            {/* Areas for Improvement */}
            <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6">
              <h3 className="font-semibold text-yellow-900 dark:text-yellow-300 mb-4 flex items-center gap-2">
                <LightBulbIcon className="h-5 w-5" />
                Areas to Focus On
              </h3>
              {assessmentResult.weaknesses.length > 0 ? (
                <ul className="space-y-2">
                  {assessmentResult.weaknesses.map(weakness => (
                    <li key={weakness} className="flex items-center gap-2">
                      <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
                      <span className="text-sm">{weakness}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  Great job! Consider exploring advanced topics.
                </p>
              )}
            </div>
          </div>

          {/* Category Breakdown */}
          <div className="mb-8">
            <h3 className="font-semibold mb-4">Performance by Category</h3>
            <div className="space-y-3">
              {assessmentResult.categoryScores.map(score => (
                <div key={score.category} className="flex items-center gap-4">
                  <span className="w-32 text-sm font-medium">{score.category}</span>
                  <div className="flex-1 bg-neutral-200 dark:bg-neutral-700 rounded-full h-6 relative">
                    <div
                      className={`h-full rounded-full transition-all ${
                        score.percentage >= 80 ? 'bg-green-500' :
                        score.percentage >= 60 ? 'bg-yellow-500' :
                        score.percentage >= 40 ? 'bg-orange-500' :
                        'bg-red-500'
                      }`}
                      style={{ width: `${score.percentage}%` }}
                    />
                    <span className="absolute right-2 top-0 h-full flex items-center text-xs font-medium">
                      {score.correct}/{score.total}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recommended Learning Path */}
          <div className="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-6 mb-6">
            <h3 className="font-semibold text-primary-900 dark:text-primary-300 mb-4 flex items-center gap-2">
              <AcademicCapIcon className="h-5 w-5" />
              Recommended Learning Path
            </h3>
            <div className="flex flex-wrap gap-2">
              {assessmentResult.recommendedPath.map((path, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-white dark:bg-neutral-800 rounded-full text-sm font-medium"
                >
                  {path}
                </span>
              ))}
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => navigate('/learning-paths')}
              className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
            >
              Start Learning
            </button>
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-3 bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
            >
              Retake Test
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Assessment Phase
  const currentQuestion = questions[currentQuestionIndex]
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">
              Question {currentQuestionIndex + 1} of {questions.length}
            </span>
            <span className="text-sm text-neutral-500">
              {currentQuestion.category}
            </span>
          </div>
          <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Question */}
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-1">{currentQuestion.question}</h2>
          <div className="flex items-center gap-2 text-sm text-neutral-500">
            <span>Difficulty:</span>
            <div className="flex gap-1">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className={`w-2 h-2 rounded-full ${
                    i < currentQuestion.difficulty
                      ? 'bg-gold-500'
                      : 'bg-neutral-300 dark:bg-neutral-600'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Options */}
        <div className="space-y-3 mb-6">
          {currentQuestion.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswerSelect(index)}
              disabled={showExplanation}
              className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                showExplanation
                  ? index === currentQuestion.correctIndex
                    ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                    : index === selectedAnswer
                    ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                    : 'border-neutral-200 dark:border-neutral-700'
                  : selectedAnswer === index
                  ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                  : 'border-neutral-200 dark:border-neutral-700 hover:border-neutral-400'
              }`}
            >
              <div className="flex items-center justify-between">
                <span>{option}</span>
                {showExplanation && index === currentQuestion.correctIndex && (
                  <CheckCircleIcon className="h-5 w-5 text-green-500" />
                )}
                {showExplanation && index === selectedAnswer && index !== currentQuestion.correctIndex && (
                  <XCircleIcon className="h-5 w-5 text-red-500" />
                )}
              </div>
            </button>
          ))}
        </div>

        {/* Explanation */}
        {showExplanation && (
          <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <p className="text-sm">
              <span className="font-semibold">Explanation:</span> {currentQuestion.explanation}
            </p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-3">
          {!showExplanation ? (
            <button
              onClick={handleSubmitAnswer}
              disabled={selectedAnswer === null}
              className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors font-medium"
            >
              Submit Answer
            </button>
          ) : (
            <button
              onClick={handleNextQuestion}
              className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium flex items-center justify-center gap-2"
            >
              {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'View Results'}
              <ArrowRightIcon className="h-5 w-5" />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default IntroAssessmentPage