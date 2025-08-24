import React, { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { spacedRepetitionService } from '../services/spacedRepetitionService'
import { useAuth } from '../contexts/AuthContext'
import { LearningContent, Question } from '../types/database.types'
import { TrophyIcon, StarIcon } from '@heroicons/react/24/outline'
import { CheckCircleIcon as CheckCircleSolidIcon } from '@heroicons/react/24/solid'
import LearningContentViewer from '../components/LearningContentViewer'
import EnhancedQuestionDisplay from '../components/EnhancedQuestionDisplay'
import '../styles/learningContent.css'

const SimpleLearningPage: React.FC = () => {
  const { contentId } = useParams<{ contentId?: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [content, setContent] = useState<LearningContent | null>(null)
  const [questions, setQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedOptionIndex, setSelectedOptionIndex] = useState<number | null>(null)
  const [showAnswer, setShowAnswer] = useState(false)
  const [phase, setPhase] = useState<'content' | 'test' | 'complete'>('content')
  const [score, setScore] = useState(0)
  const [loading, setLoading] = useState(true)
  const [currentSkillId, setCurrentSkillId] = useState<string | null>(null)

  const fetchContent = useCallback(async () => {
    try {
      let contentData = null
      let skillId = null
      
      if (contentId) {
        // First, try to fetch as a learning content ID
        const { data: directContent, error: directError } = await supabase
          .from('learning_content')
          .select('*')
          .eq('id', contentId)
          .single()
        
        if (!directError && directContent) {
          contentData = directContent
          // Find the skill node that contains this content
          const { data: node } = await supabase
            .from('skill_tree_nodes')
            .select('id')
            .contains('learning_content_ids', [parseInt(contentId)])
            .single()
          skillId = node?.id
        } else {
          // If not found as content ID, try as skill node ID
          const { data: nodeData, error: nodeError } = await supabase
            .from('skill_tree_nodes')
            .select('id, learning_content_ids')
            .eq('id', contentId)
            .single()
          
          if (!nodeError && nodeData && nodeData.learning_content_ids?.length > 0) {
            skillId = nodeData.id
            // Fetch the first learning content for this node
            const { data: nodeContent } = await supabase
              .from('learning_content')
              .select('*')
              .eq('id', nodeData.learning_content_ids[0])
              .single()
            contentData = nodeContent
          }
        }
      } else {
        // No contentId provided, get the first available content
        const { data: firstContent } = await supabase
          .from('learning_content')
          .select('*')
          .limit(1)
          .single()
        contentData = firstContent
      }

      if (!contentData) {
        throw new Error('No learning content found')
      }
      
      setContent(contentData)
      setCurrentSkillId(skillId)
      
      // Track user progress if we have a skill
      if (user && skillId) {
        try {
          // Check if progress record exists
          const { data: existingProgress } = await supabase
            .from('user_progress')
            .select('*')
            .eq('user_id', user.id)
            .eq('skill_id', skillId)
            .single()
          
          if (existingProgress) {
            // Update existing progress
            await supabase
              .from('user_progress')
              .update({
                last_accessed: new Date().toISOString(),
                status: existingProgress.status === 'not_started' ? 'in_progress' : existingProgress.status
              })
              .eq('id', existingProgress.id)
          } else {
            // Create new progress record
            await supabase
              .from('user_progress')
              .insert({
                user_id: user.id,
                skill_id: skillId,
                status: 'in_progress',
                last_accessed: new Date().toISOString(),
                rating: 0
              })
          }
        } catch (error) {
          console.error('Error tracking user progress:', error)
        }
      }
      
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
    } catch (error) {
      console.error('Error fetching content:', error)
    } finally {
      setLoading(false)
    }
  }, [contentId, user])

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

  const handleNext = async () => {
    setSelectedOptionIndex(null)
    setShowAnswer(false)
    
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1)
    } else {
      // Test complete - add questions to flashcard review and update progress
      if (user) {
        // Add questions to flashcard review
        if (questions.length > 0) {
          try {
            const flashcardsToAdd = questions.map(q => ({
              id: q.id,
              type: 'question' as const
            }))
            
            await spacedRepetitionService.addFlashcardsToReview(user.id, flashcardsToAdd)
            console.log(`Added ${flashcardsToAdd.length} questions to flashcard review`)
          } catch (error) {
            console.error('Error adding questions to flashcard review:', error)
          }
        }
        
        // Update user progress to completed
        if (currentSkillId) {
          try {
            const percentage = questions.length > 0 ? Math.round((score / questions.length) * 100) : 100
            
            await supabase
              .from('user_progress')
              .update({
                status: 'completed',
                rating: percentage,
                last_accessed: new Date().toISOString()
              })
              .eq('user_id', user.id)
              .eq('skill_id', currentSkillId)
          } catch (error) {
            console.error('Error updating progress to completed:', error)
          }
        }
      }
      
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
      <LearningContentViewer
        htmlContent={content.content}
        skillId={content.id}
        skillName={content.title}
        onComplete={() => {
          if (questions.length > 0) {
            startTest()
          } else {
            setPhase('complete')
          }
        }}
        onProgress={(progress) => {
          console.log(`Learning progress: ${progress}%`)
        }}
      />
    )
  }

  if (phase === 'complete') {
    const percentage = Math.round((score / questions.length) * 100)
    const isPerfect = score === questions.length
    const isGreat = percentage >= 80
    const isGood = percentage >= 60
    
    return (
      <div className="max-w-2xl mx-auto px-4">
        <div className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl shadow-2xl overflow-hidden">
          {/* Confetti effect for perfect score */}
          {isPerfect && (
            <div className="absolute inset-0 pointer-events-none">
              <div className="animate-bounce absolute top-10 left-10">🎉</div>
              <div className="animate-bounce absolute top-10 right-10" style={{ animationDelay: '0.2s' }}>🎊</div>
              <div className="animate-bounce absolute bottom-10 left-20" style={{ animationDelay: '0.4s' }}>✨</div>
              <div className="animate-bounce absolute bottom-10 right-20" style={{ animationDelay: '0.6s' }}>🌟</div>
            </div>
          )}
          
          <div className="relative p-8 text-center">
            {/* Icon */}
            <div className="mb-6">
              {isPerfect ? (
                <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 shadow-lg">
                  <TrophyIcon className="h-12 w-12 text-white" />
                </div>
              ) : (
                <div className={`inline-flex items-center justify-center w-24 h-24 rounded-full shadow-lg
                  ${isGreat 
                    ? 'bg-gradient-to-br from-green-400 to-green-600' 
                    : isGood
                    ? 'bg-gradient-to-br from-blue-400 to-blue-600'
                    : 'bg-gradient-to-br from-purple-400 to-purple-600'
                  }`}>
                  <CheckCircleSolidIcon className="h-12 w-12 text-white" />
                </div>
              )}
            </div>
            
            {/* Title */}
            <h2 className="text-3xl font-bold mb-2 bg-gradient-to-r from-primary-600 to-secondary-600 dark:from-primary-400 dark:to-secondary-400 bg-clip-text text-transparent">
              {isPerfect ? 'Perfect Score!' : isGreat ? 'Excellent Work!' : isGood ? 'Good Job!' : 'Keep Learning!'}
            </h2>
            
            {/* Score */}
            <div className="mb-6">
              <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-2">
                You answered correctly:
              </p>
              <div className="flex items-center justify-center gap-4">
                <div className="text-5xl font-bold text-neutral-800 dark:text-neutral-100">
                  {score}
                </div>
                <div className="text-2xl text-neutral-500 dark:text-neutral-400">
                  /
                </div>
                <div className="text-3xl font-semibold text-neutral-600 dark:text-neutral-300">
                  {questions.length}
                </div>
              </div>
            </div>
            
            {/* Percentage with visual indicator */}
            <div className="mb-8">
              <div className="relative h-6 bg-neutral-200 dark:bg-neutral-700 rounded-full overflow-hidden mb-2">
                <div 
                  className={`h-full transition-all duration-1000 ease-out
                    ${isPerfect
                      ? 'bg-gradient-to-r from-yellow-400 to-yellow-600'
                      : isGreat
                      ? 'bg-gradient-to-r from-green-400 to-green-600'
                      : isGood
                      ? 'bg-gradient-to-r from-blue-400 to-blue-600'
                      : 'bg-gradient-to-r from-purple-400 to-purple-600'
                    }`}
                  style={{ width: `${percentage}%` }}
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-sm font-bold text-white drop-shadow">
                    {percentage}%
                  </span>
                </div>
              </div>
              
              {/* Stars rating */}
              <div className="flex justify-center gap-1">
                {[1, 2, 3, 4, 5].map((star) => (
                  <StarIcon
                    key={star}
                    className={`h-6 w-6 transition-all ${
                      star <= Math.ceil(percentage / 20)
                        ? 'text-yellow-400 fill-yellow-400'
                        : 'text-neutral-300 dark:text-neutral-600'
                    }`}
                  />
                ))}
              </div>
            </div>
            
            {/* Motivational message */}
            <p className="text-neutral-600 dark:text-neutral-400 mb-8">
              {isPerfect 
                ? "Outstanding! You've mastered this content!" 
                : isGreat
                ? "Great job! You're well on your way to mastery!"
                : isGood
                ? "Good progress! Keep practicing to improve!"
                : "Every attempt is a step forward. Keep going!"}
            </p>
            
            {/* Action button */}
            <button 
              onClick={() => navigate('/learning-paths')} 
              className="px-8 py-3 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl font-medium shadow-lg hover:shadow-xl hover:scale-105 active:scale-100 transition-all"
            >
              Continue Learning →
            </button>
          </div>
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
    <div className="max-w-3xl mx-auto px-4 py-4 h-screen">
      <EnhancedQuestionDisplay
        question={currentQuestion}
        questionNumber={currentQuestionIndex + 1}
        totalQuestions={questions.length}
        onAnswerSelect={(index) => setSelectedOptionIndex(index)}
        onSubmit={handleAnswer}
        onNext={handleNext}
        selectedAnswer={selectedOptionIndex ?? undefined}
        showExplanation={showAnswer}
        isPreQuiz={false}
        timeLimit={60} // 60 seconds per question
      />
    </div>
  )
}

export default SimpleLearningPage