import React, { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { LearningContent, Question } from '../types/database.types'
import { ClockIcon, CheckCircleIcon } from '@heroicons/react/24/outline'

const SimpleLearningPage: React.FC = () => {
  const { contentId } = useParams<{ contentId?: string }>()
  const navigate = useNavigate()
  // const { user } = useAuth()
  const [content, setContent] = useState<LearningContent | null>(null)
  const [questions, setQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedOptionIndex, setSelectedOptionIndex] = useState<number | null>(null)
  const [showAnswer, setShowAnswer] = useState(false)
  const [phase, setPhase] = useState<'content' | 'test' | 'complete'>('content')
  const [score, setScore] = useState(0)
  const [loading, setLoading] = useState(true)

  const fetchContent = useCallback(async () => {
    try {
      // If no contentId, get the first available content
      const query = contentId 
        ? supabase.from('learning_content').select('*').eq('id', contentId).single()
        : supabase.from('learning_content').select('*').limit(1).single()
      
      const { data: contentData, error: contentError } = await query

      if (contentError) throw contentError
      
      if (contentData) {
        setContent(contentData)
        
        // Fetch questions if they exist
        if (contentData.question_ids && contentData.question_ids.length > 0) {
          const { data: questionsData, error: questionsError } = await supabase
            .from('questions')
            .select('*')
            .in('id', contentData.question_ids)
          
          if (!questionsError && questionsData) {
            setQuestions(questionsData)
          }
        }
      }
    } catch (error) {
      console.error('Error fetching content:', error)
    } finally {
      setLoading(false)
    }
  }, [contentId])

  useEffect(() => {
    fetchContent()
  }, [fetchContent])

  const handleAnswer = () => {
    if (selectedOptionIndex === null || !questions[currentQuestionIndex]) return
    
    setShowAnswer(true)
    const currentQuestion = questions[currentQuestionIndex]
    const isCorrect = selectedOptionIndex === currentQuestion.correct_answer
    
    if (isCorrect) {
      setScore(prev => prev + 1)
    }
  }

  const handleNext = () => {
    setSelectedOptionIndex(null)
    setShowAnswer(false)
    
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1)
    } else {
      setPhase('complete')
    }
  }

  const startTest = () => {
    setPhase('test')
    setCurrentQuestionIndex(0)
    setScore(0)
    setSelectedOptionIndex(null)
    setShowAnswer(false)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!content) {
    return (
      <div className="text-center py-12">
        <p className="text-xl text-neutral-600">No learning content available</p>
        <button onClick={() => navigate('/learning-paths')} className="btn-primary mt-4">
          Back to Skill Tree
        </button>
      </div>
    )
  }

  if (phase === 'content') {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card">
          <h1 className="text-3xl font-bold mb-4">{content.title}</h1>
          
          <div className="flex items-center gap-4 mb-6 text-sm text-neutral-600 dark:text-neutral-400">
            <span className="flex items-center gap-1">
              <ClockIcon className="h-4 w-4" />
              {content.estimated_time_minutes} minutes
            </span>
            <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 rounded">
              {content.difficulty_level}
            </span>
          </div>

          {content.images && content.images.length > 0 && (
            <div className="mb-6">
              {content.images.map((img, index) => (
                <div key={index} className="mb-4">
                  <img 
                    src={typeof img === 'string' ? img : img.url}
                    alt={typeof img === 'string' ? `Image ${index + 1}` : img.caption || `Image ${index + 1}`}
                    className="w-full rounded-lg"
                  />
                  {typeof img === 'object' && img.caption && (
                    <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-2 text-center">
                      {img.caption}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}

          <div 
            className="prose dark:prose-invert max-w-none mb-8"
            dangerouslySetInnerHTML={{ __html: content.content }}
          />

          {questions.length > 0 && (
            <button onClick={startTest} className="btn-primary">
              Take Test ({questions.length} questions)
            </button>
          )}
        </div>
      </div>
    )
  }

  if (phase === 'complete') {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="card text-center">
          <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-4">Test Complete!</h2>
          <p className="text-lg mb-6">
            You scored {score} out of {questions.length} questions correctly
          </p>
          <div className="text-3xl font-bold text-primary-600">
            {Math.round((score / questions.length) * 100)}%
          </div>
          <button 
            onClick={() => navigate('/learning-paths')} 
            className="btn-primary mt-6"
          >
            Back to Skill Tree
          </button>
        </div>
      </div>
    )
  }

  // Test phase
  const currentQuestion = questions[currentQuestionIndex]
  
  if (!currentQuestion) {
    return <div>No questions available</div>
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <div className="mb-4">
          <span className="text-sm text-neutral-600 dark:text-neutral-400">
            Question {currentQuestionIndex + 1} of {questions.length}
          </span>
        </div>

        <h2 className="text-xl font-semibold mb-4">{currentQuestion.question_text}</h2>

        {currentQuestion.image_url && (
          <img 
            src={currentQuestion.image_url} 
            alt="Question"
            className="w-full rounded-lg mb-4"
          />
        )}

        <div className="space-y-3 mb-6">
          {currentQuestion.options.map((option, index) => {
            const isCorrect = index === currentQuestion.correct_answer
            const isSelected = selectedOptionIndex === index
            
            return (
              <button
                key={index}
                onClick={() => !showAnswer && setSelectedOptionIndex(index)}
                disabled={showAnswer}
                className={`w-full text-left p-4 rounded-lg border transition-colors ${
                  showAnswer
                    ? isCorrect
                      ? 'bg-green-50 dark:bg-green-900/20 border-green-500'
                      : isSelected
                      ? 'bg-red-50 dark:bg-red-900/20 border-red-500'
                      : 'border-neutral-300 dark:border-neutral-600'
                    : isSelected
                    ? 'bg-primary-50 dark:bg-primary-900/20 border-primary-500'
                    : 'border-neutral-300 dark:border-neutral-600 hover:bg-neutral-50 dark:hover:bg-neutral-800'
                }`}
              >
                {option}
              </button>
            )
          })}
        </div>

        {showAnswer && (
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg mb-6">
            <p className="font-medium mb-2">Explanation:</p>
            <p className="text-sm">
              {currentQuestion.explanation || 'No explanation available'}
            </p>
          </div>
        )}

        <div className="flex gap-3">
          {!showAnswer ? (
            <button
              onClick={handleAnswer}
              disabled={selectedOptionIndex === null}
              className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit Answer
            </button>
          ) : (
            <button onClick={handleNext} className="btn-primary flex-1">
              {currentQuestionIndex === questions.length - 1 ? 'View Results' : 'Next Question'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default SimpleLearningPage