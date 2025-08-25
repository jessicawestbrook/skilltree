import React, { useState, useEffect } from 'react'
import { XMarkIcon, FlagIcon, SparklesIcon } from '@heroicons/react/24/outline'
import { supabase } from '../services/supabase'
import { Question } from '../types/database.types'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate, useLocation } from 'react-router-dom'
import FlagContentModal from './FlagContentModal'
import QuestionExplanation from './QuestionExplanation'
import { siteConfig } from '../config/site.config'

interface RandomQuestionBoxProps {
  onClose: () => void
}

const RandomQuestionBox: React.FC<RandomQuestionBoxProps> = ({ onClose }) => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [question, setQuestion] = useState<Question | null>(null)
  const [selectedOptionIndex, setSelectedOptionIndex] = useState<number | null>(null)
  const [showAnswer, setShowAnswer] = useState(false)
  const [loading, setLoading] = useState(true)
  const [questionCount, setQuestionCount] = useState(0)
  const [questionPath, setQuestionPath] = useState<string[]>([])
  const [seenQuestionIds, setSeenQuestionIds] = useState<Set<string>>(new Set())
  const [showFlagModal, setShowFlagModal] = useState(false)
  const [showLoginPrompt, setShowLoginPrompt] = useState(false)

  // Removed fetchQuestionPath - will implement differently if needed

  const fetchRandomQuestion = async () => {
    setLoading(true)
    setSelectedOptionIndex(null)
    setShowAnswer(false)
    setQuestionPath([])

    try {
      // First try to get user's question history if logged in
      let userSeenQuestions: string[] = []
      if (user) {
        const { data: attempts } = await supabase
          .from('user_question_responses')
          .select('question_id')
          .eq('user_id', user.id)
          .eq('context_type', 'practice')
        
        if (attempts) {
          userSeenQuestions = attempts.map(a => a.question_id)
        }
      }

      const { data: allQuestions, error } = await supabase
        .from('questions')
        .select('*')

      if (error) throw error

      if (allQuestions && allQuestions.length > 0) {
        // Separate unseen and seen questions
        const unseenQuestions = allQuestions.filter(
          q => !userSeenQuestions.includes(q.id) && !seenQuestionIds.has(q.id)
        )
        const seenQuestions = allQuestions.filter(
          q => userSeenQuestions.includes(q.id) || seenQuestionIds.has(q.id)
        )
        
        // Prioritize unseen questions
        const questionPool = unseenQuestions.length > 0 ? unseenQuestions : seenQuestions
        
        // Select a random question from the pool
        const randomIndex = Math.floor(Math.random() * questionPool.length)
        const selectedQuestion = questionPool[randomIndex]
        setQuestion(selectedQuestion)
        
        // Track this question as seen in the current session
        setSeenQuestionIds(prev => new Set(prev).add(selectedQuestion.id))
        
        // Knowledge path fetching will be implemented separately
      }
    } catch (error) {
      console.error('Error fetching question:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchRandomQuestion()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    const questionLimit = siteConfig.auth.randomQuestionsBeforeLogin
    if (!user && questionCount >= questionLimit) {
      setShowLoginPrompt(true)
    }
  }, [questionCount, user])

  const handleSubmit = async () => {
    if (selectedOptionIndex === null) return
    
    setShowAnswer(true)
    setQuestionCount(prev => prev + 1)

    if (user && question) {
      const isCorrect = selectedOptionIndex === question.correct_answer

      try {
        // Check if user has attempted this question before
        const { data: previousAttempts } = await supabase
          .from('user_question_responses')
          .select('id')
          .eq('user_id', user.id)
          .eq('question_id', question.id)
          .eq('context_type', 'practice')
        
        const attemptNumber = (previousAttempts?.length || 0) + 1
        
        // Save the attempt
        await supabase.from('user_question_responses').insert({
          user_id: user.id,
          question_id: question.id,
          is_correct: isCorrect,
          response_time_ms: 0,
          attempt_number: attemptNumber,
          context_type: 'practice',
          user_response: question.options[selectedOptionIndex]
        })
      } catch (error) {
        console.log('Could not save attempt:', error)
      }
    }
  }

  const handleNext = () => {
    fetchRandomQuestion()
  }

  if (loading) {
    return (
      <div className="card sticky top-4 p-3">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-sm font-semibold">Quick Practice</h3>
          <button onClick={onClose} className="p-0.5">
            <XMarkIcon className="h-4 w-4 text-neutral-500" />
          </button>
        </div>
        <div className="animate-pulse space-y-2">
          <div className="h-3 bg-neutral-200 dark:bg-neutral-700 rounded w-3/4"></div>
          <div className="h-3 bg-neutral-200 dark:bg-neutral-700 rounded w-1/2"></div>
        </div>
      </div>
    )
  }

  if (!question) {
    return (
      <div className="card sticky top-4 p-3">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-sm font-semibold">Quick Practice</h3>
          <button onClick={onClose} className="p-0.5">
            <XMarkIcon className="h-4 w-4 text-neutral-500" />
          </button>
        </div>
        <p className="text-xs text-neutral-600 dark:text-neutral-400">No questions available</p>
      </div>
    )
  }

  return (
    <>
      <div className="card sticky top-4 p-3">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-sm font-semibold flex items-center gap-2">
            <SparklesIcon className="h-4 w-4 text-gold-500" />
            <span>Quick Practice</span>
            <span className="text-xs text-neutral-500">#{questionCount + 1}</span>
          </h3>
          <div className="flex items-center gap-1">
            <button 
              onClick={() => setShowFlagModal(true)} 
              className="p-0.5 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded"
              title="Report an issue"
            >
              <FlagIcon className="h-4 w-4 text-neutral-500" />
            </button>
            <button onClick={onClose} className="p-0.5 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded">
              <XMarkIcon className="h-4 w-4 text-neutral-500" />
            </button>
          </div>
        </div>

        <div className="space-y-2">
        {questionPath.length > 0 && (
          <div className="text-xs text-neutral-500 truncate">
            {questionPath.join(' → ')}
          </div>
        )}
        <p className="text-sm font-medium leading-tight">{question.question_text}</p>
        
        {question.image_url && (
          <img 
            src={question.image_url} 
            alt="Question" 
            className="rounded max-h-32 object-contain"
          />
        )}

        <div className="space-y-1">
          {question.options.map((option, index) => {
            const isCorrect = index === question.correct_answer
            const isSelected = selectedOptionIndex === index
            
            return (
              <button
                key={index}
                onClick={() => !showAnswer && setSelectedOptionIndex(index)}
                disabled={showAnswer}
                className={`w-full text-left p-2 rounded border text-xs transition-colors ${
                  showAnswer
                    ? isCorrect
                      ? 'bg-green-50 dark:bg-green-900/20 border-green-500'
                      : isSelected
                      ? 'bg-red-50 dark:bg-red-900/20 border-red-500'
                      : 'border-neutral-200 dark:border-neutral-700'
                    : isSelected
                    ? 'bg-primary-50 dark:bg-primary-900/20 border-primary-500'
                    : 'border-neutral-200 dark:border-neutral-700 hover:bg-neutral-50 dark:hover:bg-neutral-800'
                }`}
              >
                {option}
              </button>
            )
          })}
        </div>

        {showAnswer && (
          <QuestionExplanation 
            explanation={question.explanation || 'No explanation available'}
            correctAnswer={question.options[question.correct_answer]}
            nodeType={questionPath[0]} // Use first path element as node type
          />
        )}

        <div className="flex gap-1.5">
          {!showAnswer ? (
            <button
              onClick={handleSubmit}
              disabled={selectedOptionIndex === null}
              className="btn-primary text-xs py-1.5 px-3 w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="btn-primary text-xs py-1.5 px-3 w-full"
            >
              Next →
            </button>
          )}
        </div>
      </div>
    </div>

    {showFlagModal && question && (
      <FlagContentModal
        isOpen={showFlagModal}
        onClose={() => setShowFlagModal(false)}
        contentType="question"
        contentId={question.id}
        contentTitle={question.question_text}
      />
    )}
    
    {showLoginPrompt && (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-2xl max-w-md w-full p-6">
          <h2 className="text-2xl font-bold mb-4">Keep Learning!</h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            You've answered {siteConfig.auth.randomQuestionsBeforeLogin} questions! Sign in to track your progress, see personalized recommendations, and unlock all features.
          </p>
          <div className="flex gap-3">
            <button
              onClick={() => {
                const redirectTo = location.pathname + location.search
                navigate(`/login?redirect=${encodeURIComponent(redirectTo)}`)
              }}
              className="btn-primary flex-1"
            >
              Sign In
            </button>
            <button
              onClick={() => navigate('/signup')}
              className="btn-secondary flex-1"
            >
              Sign Up
            </button>
          </div>
          <button
            onClick={() => {
              setShowLoginPrompt(false)
              setQuestionCount(0) // Reset counter
            }}
            className="w-full mt-3 text-sm text-neutral-500 hover:text-neutral-700"
          >
            Continue as guest (limited)
          </button>
        </div>
      </div>
    )}
    </>
  )
}

export default RandomQuestionBox