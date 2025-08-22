import React, { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import SimpleVisualMatrix from './SimpleVisualMatrix'

interface VisualRavensQuestion {
  id: string
  question_number: number
  set_name: 'A' | 'B' | 'C' | 'D' | 'E'
  difficulty: 'very_easy' | 'easy' | 'medium' | 'hard' | 'very_hard'
  pattern_type: string
  cognitive_area: string
  time_limit_seconds: number
  points_value: number
}

interface TestAttempt {
  id: string
  started_at: string
  responses: TestResponse[]
}

interface TestResponse {
  question_id: string
  selected_option: number
  is_correct: boolean
  time_taken: number
}

const VisualRavensTest: React.FC = () => {
  const { user } = useAuth()
  const [testPhase, setTestPhase] = useState<'intro' | 'test' | 'results'>('intro')
  const [questions, setQuestions] = useState<VisualRavensQuestion[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [testAttempt, setTestAttempt] = useState<TestAttempt | null>(null)
  const [responses, setResponses] = useState<TestResponse[]>([])
  const [timeRemaining, setTimeRemaining] = useState(0)
  const [, setTotalTime] = useState(0)
  const [loading, setLoading] = useState(false)

  // Load questions from database
  useEffect(() => {
    const loadQuestions = async () => {
      setLoading(true)
      try {
        const { data: testData } = await supabase
          .from('standardized_tests')
          .select('id')
          .eq('subtype', 'ravens_matrices')
          .single()

        if (testData) {
          const { data: questionsData, error } = await supabase
            .from('standardized_test_questions')
            .select(`
              id,
              question_number,
              difficulty,
              pattern_type,
              cognitive_area,
              time_limit_seconds,
              points_value,
              metadata
            `)
            .eq('test_id', testData.id)
            .order('question_number')

          if (error) {
            console.error('Error loading questions:', error)
          } else {
            const formattedQuestions = questionsData.map(q => ({
              ...q,
              set_name: getSetFromQuestionNumber(q.question_number)
            }))
            setQuestions(formattedQuestions)
          }
        }
      } catch (error) {
        console.error('Failed to load questions:', error)
      } finally {
        setLoading(false)
      }
    }

    loadQuestions()
  }, [])

  const getSetFromQuestionNumber = (num: number): 'A' | 'B' | 'C' | 'D' | 'E' => {
    if (num <= 4) return 'A'
    if (num <= 8) return 'B'
    if (num <= 12) return 'C'
    if (num <= 16) return 'D'
    return 'E'
  }

  const startTest = async () => {
    if (!user || questions.length === 0) return

    try {
      // Create test attempt
      const { data: attempt, error } = await supabase
        .from('user_test_attempts')
        .insert({
          user_id: user.id,
          test_id: questions[0]?.id, // This should be the test_id, not question id
          attempt_number: 1,
          is_practice: true
        })
        .select()
        .single()

      if (error) {
        console.error('Error creating test attempt:', error)
        return
      }

      setTestAttempt(attempt)
      setTestPhase('test')
      setCurrentQuestionIndex(0)
      setTimeRemaining(questions[0]?.time_limit_seconds || 60)
      setTotalTime(0)
      setResponses([])
    } catch (error) {
      console.error('Failed to start test:', error)
    }
  }

  const finishTest = useCallback(async () => {
    if (!testAttempt) return

    const totalTimeSpent = responses.reduce((sum, r) => sum + r.time_taken, 0)
    const correctAnswers = responses.filter(r => r.is_correct).length
    const rawScore = responses.reduce((sum, r, index) => {
      return sum + (r.is_correct ? questions[index]?.points_value || 1 : 0)
    }, 0)

    // Calculate IQ score (simplified)
    const percentCorrect = (correctAnswers / questions.length) * 100
    const iqScore = Math.round(85 + (percentCorrect / 100) * 30)

    try {
      await supabase
        .from('user_test_attempts')
        .update({
          completed_at: new Date().toISOString(),
          time_taken_seconds: totalTimeSpent,
          raw_score: rawScore,
          scaled_score: iqScore,
          is_completed: true
        })
        .eq('id', testAttempt.id)
    } catch (error) {
      console.error('Error updating test attempt:', error)
    }

    setTestPhase('results')
  }, [testAttempt, responses, questions])

  const handleAnswer = useCallback(async (selectedOption: number) => {
    if (!testAttempt || !questions[currentQuestionIndex]) return

    const currentQuestion = questions[currentQuestionIndex]
    const timeSpent = (currentQuestion.time_limit_seconds || 60) - timeRemaining
    
    // For this demo, we'll assume option 0 is always correct
    // In reality, this would come from the question data
    const isCorrect = selectedOption === 0
    
    const response: TestResponse = {
      question_id: currentQuestion.id,
      selected_option: selectedOption,
      is_correct: isCorrect,
      time_taken: timeSpent
    }

    setResponses(prev => [...prev, response])

    // Save response to database
    try {
      await supabase
        .from('user_test_responses')
        .insert({
          attempt_id: testAttempt.id,
          question_id: currentQuestion.id,
          user_answer: selectedOption,
          is_correct: isCorrect,
          points_earned: isCorrect ? currentQuestion.points_value : 0,
          time_taken_seconds: timeSpent
        })
    } catch (error) {
      console.error('Error saving response:', error)
    }

    // Move to next question or finish test
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1)
      setTimeRemaining(questions[currentQuestionIndex + 1]?.time_limit_seconds || 60)
    } else {
      finishTest()
    }
  }, [testAttempt, questions, currentQuestionIndex, timeRemaining, finishTest])

  // Timer effect
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null

    if (testPhase === 'test' && timeRemaining > 0) {
      interval = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            // Auto-advance when time runs out
            handleAnswer(-1) // -1 indicates no answer selected
            return 0
          }
          return prev - 1
        })
        setTotalTime(prev => prev + 1)
      }, 1000)
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [testPhase, timeRemaining, currentQuestionIndex, handleAnswer])

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-64">
        <div className="text-lg">Loading visual matrix test...</div>
      </div>
    )
  }

  if (testPhase === 'intro') {
    return (
      <div className="max-w-4xl mx-auto py-8">
        <div className="card">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold mb-2">Visual Raven's Progressive Matrices</h1>
            <p className="text-neutral-600 dark:text-neutral-400">
              Non-verbal intelligence test using visual pattern recognition
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-6">
              <h3 className="font-semibold mb-3">What to Expect</h3>
              <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  {questions.length} visual matrix puzzles
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Progressive difficulty (Sets A through E)
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Each question is timed individually
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Find the missing piece to complete the pattern
                </li>
              </ul>
            </div>

            <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-6">
              <h3 className="font-semibold mb-3">Instructions</h3>
              <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                <li className="flex items-start">
                  <span className="text-gold-600 mr-2">•</span>
                  Look at each visual pattern carefully
                </li>
                <li className="flex items-start">
                  <span className="text-gold-600 mr-2">•</span>
                  Find the logical rule or progression
                </li>
                <li className="flex items-start">
                  <span className="text-gold-600 mr-2">•</span>
                  Select the option that best completes the pattern
                </li>
                <li className="flex items-start">
                  <span className="text-gold-600 mr-2">•</span>
                  Work quickly but accurately
                </li>
              </ul>
            </div>
          </div>

          <div className="text-center">
            <button onClick={startTest} className="btn-primary">
              Start Visual Matrix Test
            </button>
            <p className="text-xs text-neutral-500 mt-4">
              Estimated time: 20-25 minutes
            </p>
          </div>
        </div>
      </div>
    )
  }

  if (testPhase === 'test' && questions.length > 0) {
    const currentQuestion = questions[currentQuestionIndex]
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100

    return (
      <div className="max-w-5xl mx-auto py-8">
        <div className="card">
          {/* Progress Bar */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium">
                Question {currentQuestionIndex + 1} of {questions.length}
              </span>
              <span className="text-sm text-neutral-600 dark:text-neutral-400">
                Set {currentQuestion.set_name} • {currentQuestion.difficulty}
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
              <span className={`font-mono text-lg ${
                timeRemaining <= 10 ? 'text-red-600' : 'text-neutral-700 dark:text-neutral-300'
              }`}>
                {formatTime(timeRemaining)}
              </span>
            </div>
            <div className="text-sm text-neutral-600 dark:text-neutral-400">
              Pattern: {currentQuestion.pattern_type.replace(/_/g, ' ')}
            </div>
          </div>

          {/* Visual Matrix */}
          <div className="mb-8">
            <SimpleVisualMatrix
              patternType={currentQuestion.pattern_type}
              difficulty={currentQuestion.difficulty}
              setName={currentQuestion.set_name}
              questionNumber={currentQuestion.question_number}
              onAnswer={handleAnswer}
            />
          </div>
        </div>
      </div>
    )
  }

  if (testPhase === 'results') {
    const correctAnswers = responses.filter(r => r.is_correct).length
    const percentCorrect = (correctAnswers / questions.length) * 100
    const iqScore = Math.round(85 + (percentCorrect / 100) * 30)

    return (
      <div className="max-w-4xl mx-auto py-8">
        <div className="card">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold mb-2">Test Complete!</h1>
            <p className="text-neutral-600 dark:text-neutral-400">
              Your visual pattern recognition results
            </p>
          </div>

          {/* IQ Score */}
          <div className="bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl p-8 mb-8 text-center">
            <h2 className="text-lg mb-2">Your IQ Score</h2>
            <div className="text-6xl font-bold mb-2">{iqScore}</div>
            <p className="text-primary-100">
              {correctAnswers}/{questions.length} correct ({Math.round(percentCorrect)}%)
            </p>
          </div>

          {/* Performance by Set */}
          <div className="mb-8">
            <h3 className="font-semibold mb-4">Performance by Difficulty Set</h3>
            <div className="space-y-3">
              {['A', 'B', 'C', 'D', 'E'].map(setName => {
                const setQuestions = questions.filter(q => q.set_name === setName)
                const setResponses = responses.filter((_, i) => questions[i]?.set_name === setName)
                const setCorrect = setResponses.filter(r => r.is_correct).length
                const setPercent = setQuestions.length > 0 ? (setCorrect / setQuestions.length) * 100 : 0

                return (
                  <div key={setName}>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-medium">
                        Set {setName} ({setQuestions[0]?.difficulty || 'N/A'})
                      </span>
                      <span className="text-sm text-neutral-600 dark:text-neutral-400">
                        {setCorrect}/{setQuestions.length} ({Math.round(setPercent)}%)
                      </span>
                    </div>
                    <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full transition-all ${
                          setPercent >= 80 ? 'bg-green-500' :
                          setPercent >= 60 ? 'bg-gold-500' :
                          setPercent >= 40 ? 'bg-orange-500' :
                          'bg-red-500'
                        }`}
                        style={{ width: `${setPercent}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          <div className="flex gap-3">
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

export default VisualRavensTest