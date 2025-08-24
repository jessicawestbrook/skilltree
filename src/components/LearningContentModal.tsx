import React, { useState, useEffect, useRef } from 'react'
import { XMarkIcon, FlagIcon, ClockIcon } from '@heroicons/react/24/outline'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { questionTrackingService } from '../services/questionTrackingService'
import { adaptiveLearningService } from '../services/adaptiveLearningService'
import { SkillTreeNode, LearningContent, Question } from '../types/database.types'
import FlagContentModal from './FlagContentModal'
import LearningContentViewer from './LearningContentViewer'
import EnhancedQuestionDisplay from './EnhancedQuestionDisplay'
import '../styles/learningContent.css'

interface LearningContentModalProps {
  node: SkillTreeNode
  isOpen: boolean
  onClose: () => void
  onComplete?: (passed: boolean) => void
}

type LearningPhase = 'pre-quiz' | 'content' | 'test' | 'results'

const LearningContentModal: React.FC<LearningContentModalProps> = ({ 
  node, 
  isOpen, 
  onClose,
  onComplete 
}) => {
  const { user } = useAuth()
  const [phase, setPhase] = useState<LearningPhase>('pre-quiz')
  const [learningContent, setLearningContent] = useState<LearningContent | null>(null)
  const [questions, setQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({})
  const [showExplanation, setShowExplanation] = useState(false)
  const [preQuizScore, setPreQuizScore] = useState(0)
  const [testScore, setTestScore] = useState(0)
  const [loading, setLoading] = useState(true)
  const [showFlagModal, setShowFlagModal] = useState(false)
  const [flagType, setFlagType] = useState<'question' | 'learning_content'>('learning_content')
  const [flagContentId, setFlagContentId] = useState<string>('')
  const [flagContentTitle, setFlagContentTitle] = useState<string>('')
  const [questionStartTime, setQuestionStartTime] = useState<number>(Date.now())
  const [contentViewTime, setContentViewTime] = useState<number>(0)
  const [minContentViewTime] = useState<number>(30) // Minimum 30 seconds to view content
  const timeRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    if (isOpen && node.learning_content_ids?.length) {
      fetchLearningContent()
    }
    
    // Cleanup timer on unmount or close
    return () => {
      if (timeRef.current) {
        clearInterval(timeRef.current)
        timeRef.current = null
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen, node])

  const fetchLearningContent = async () => {
    if (!node.learning_content_ids?.length) {
      setLoading(false)
      return
    }

    try {
      // Fetch the first learning content for this node
      const { data: content, error: contentError } = await supabase
        .from('learning_content')
        .select('*')
        .eq('id', node.learning_content_ids[0])
        .single()

      if (contentError) throw contentError
      setLearningContent(content)

      // Fetch all available questions
      if (content.question_ids?.length) {
        const { data: allQuestions, error: questionsError } = await supabase
          .from('questions')
          .select('*')
          .in('id', content.question_ids)

        if (questionsError) throw questionsError
        
        if (allQuestions && allQuestions.length > 0) {
          // Use adaptive learning to select questions
          const { preQuizQuestions, testQuestions } = adaptiveLearningService.selectAdaptiveQuestions(
            allQuestions,
            Math.min(3, allQuestions.length),
            Math.min(Math.max(5, allQuestions.length - 3), 20)
          )
          
          // Track question views if user is logged in
          if (user) {
            // Track all selected questions
            const allSelectedQuestions = [...preQuizQuestions, ...testQuestions]
            for (const question of allSelectedQuestions) {
              await questionTrackingService.trackQuestionView(user.id, question.id)
            }
          }
          
          // Sort test questions by difficulty (easy to hard) for adaptive progression
          const sortedTestQuestions = adaptiveLearningService.sortQuestionsByDifficulty(testQuestions)
          
          // Combine questions (pre-quiz first, then sorted test questions)
          setQuestions([...preQuizQuestions, ...sortedTestQuestions])
        } else {
          // Fallback for no questions
          setQuestions([])
        }
      } else {
        // No questions available - skip directly to content
        setPhase('content')
        setQuestions([])
        
        // Start content timer
        timeRef.current = setInterval(() => {
          setContentViewTime(prev => prev + 1)
        }, 1000)
      }
    } catch (error) {
      console.error('Error fetching learning content:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerSelect = (questionIndex: number, optionIndex: number) => {
    setSelectedAnswers(prev => ({ ...prev, [questionIndex]: optionIndex }))
  }

  const handleQuestionSubmit = async () => {
    setShowExplanation(true)
    
    // Track the question attempt
    if (user && questions[currentQuestionIndex]) {
      const timeTaken = (Date.now() - questionStartTime) / 1000 // Convert to seconds
      const isCorrect = selectedAnswers[currentQuestionIndex] === questions[currentQuestionIndex].correct_answer
      
      await questionTrackingService.trackQuestionView(user.id, questions[currentQuestionIndex].id)
      await questionTrackingService.trackQuestionAttempt(
        user.id,
        questions[currentQuestionIndex].id,
        isCorrect,
        timeTaken
      )
    }
  }

  const handleNextQuestion = () => {
    setShowExplanation(false)
    setQuestionStartTime(Date.now()) // Reset timer for next question
    
    if (phase === 'pre-quiz' && currentQuestionIndex === 2) {
      // End of pre-quiz, calculate score and move to content
      const score = calculateScore(0, 3)
      setPreQuizScore(score)
      setPhase('content')
      setContentViewTime(0)
      // Start content timer
      if (timeRef.current) clearInterval(timeRef.current)
      timeRef.current = setInterval(() => {
        setContentViewTime(prev => prev + 1)
      }, 1000)
      setCurrentQuestionIndex(3) // Skip first 3 questions for test
    } else if (phase === 'test' && currentQuestionIndex === questions.length - 1) {
      // End of test, calculate score and show results
      const score = calculateScore(3, questions.length)
      setTestScore(score)
      setPhase('results')
      const passed = score === questions.length - 3 // Pass if 100% on test
      saveProgress(passed)
    } else {
      setCurrentQuestionIndex(prev => prev + 1)
    }
  }

  const calculateScore = (startIndex: number, endIndex: number) => {
    let correct = 0
    for (let i = startIndex; i < endIndex && i < questions.length; i++) {
      if (selectedAnswers[i] === questions[i].correct_answer) {
        correct++
      }
    }
    return correct
  }

  const saveProgress = async (passed: boolean) => {
    if (!user) return

    try {
      // Calculate enhanced rating based on theoretical foundations
      const totalTestQuestions = questions.length - 3 // Excluding pre-quiz
      const accuracy = totalTestQuestions > 0 
        ? (testScore / totalTestQuestions) * 100 
        : 0
      
      // Calculate time efficiency
      const estimatedTime = (learningContent?.estimated_time_minutes || 15) * 60 // in seconds
      const actualTime = contentViewTime + (totalTestQuestions * 30) // content + avg question time
      const timeEfficiency = Math.min(100, (estimatedTime / actualTime) * 100)
      
      // Calculate consistency (higher if passed with 100%, lower otherwise)
      const consistency = passed ? 100 : Math.max(0, 100 - Math.abs(accuracy - 70))
      
      // Estimate difficulty (should come from question difficulty levels)
      const avgDifficulty = 5 // Default medium difficulty (scale 1-10)
      
      // Multi-dimensional rating calculation
      // Based on: (0.4 × Accuracy) + (0.3 × Consistency) + (0.2 × Difficulty) + (0.1 × Speed)
      const rating = Math.round(
        (accuracy * 0.4) + 
        (consistency * 0.3) + 
        (avgDifficulty * 10 * 0.2) + 
        (timeEfficiency * 0.1)
      )
      
      // Update user progress with enhanced metrics
      const { error } = await supabase
        .from('user_progress')
        .upsert({
          user_id: user.id,
          skill_id: node.id,
          status: passed ? 'completed' : 'in_progress',
          rating: rating,
          last_accessed: new Date().toISOString(),
          test_score: testScore,
          total_questions: totalTestQuestions,
          pre_quiz_score: preQuizScore
        })

      if (error) throw error
      
      // Update user's overall rating/level
      await updateUserRating(rating, passed)
      
      if (onComplete) {
        onComplete(passed)
      }
    } catch (error) {
      console.error('Error saving progress:', error)
    }
  }
  
  const updateUserRating = async (nodeRating: number, passed: boolean) => {
    if (!user) return
    
    try {
      // Fetch user's current profile
      const { data: profile } = await supabase
        .from('profiles')
        .select('overall_rating, total_completed, total_attempted')
        .eq('id', user.id)
        .single()
      
      const currentRating = profile?.overall_rating || 0
      const totalCompleted = (profile?.total_completed || 0) + (passed ? 1 : 0)
      const totalAttempted = (profile?.total_attempted || 0) + 1
      
      // Calculate new overall rating (weighted average)
      const newOverallRating = Math.round(
        ((currentRating * (totalAttempted - 1)) + nodeRating) / totalAttempted
      )
      
      // Update profile with new rating
      await supabase
        .from('profiles')
        .update({
          overall_rating: newOverallRating,
          total_completed: totalCompleted,
          total_attempted: totalAttempted,
          last_activity: new Date().toISOString()
        })
        .eq('id', user.id)
        
    } catch (error) {
      console.error('Error updating user rating:', error)
    }
  }

  const startTest = () => {
    // Stop content timer
    if (timeRef.current) {
      clearInterval(timeRef.current)
      timeRef.current = null
    }
    setPhase('test')
    setCurrentQuestionIndex(3) // Start with questions after pre-quiz
    setQuestionStartTime(Date.now()) // Start timing first test question
  }

  if (!isOpen) return null

  const currentQuestion = questions[currentQuestionIndex]
  const isPreQuiz = phase === 'pre-quiz'
  const questionsInPhase = isPreQuiz ? 3 : questions.length - 3
  const questionNumber = isPreQuiz 
    ? currentQuestionIndex + 1 
    : currentQuestionIndex - 2

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-2xl max-w-5xl w-full max-h-[90vh] flex flex-col border border-neutral-200 dark:border-neutral-700 overflow-hidden">
        <div className="bg-white dark:bg-neutral-800 border-b border-neutral-200 dark:border-neutral-700 p-4 flex justify-between items-center flex-shrink-0">
          <div className="flex items-center gap-2">
            {(phase === 'pre-quiz' || phase === 'test') && currentQuestion && (
              <button 
                onClick={() => {
                  setFlagType('question')
                  setFlagContentId(questions[currentQuestionIndex].id)
                  setFlagContentTitle(questions[currentQuestionIndex].question_text)
                  setShowFlagModal(true)
                }}
                className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg"
                title="Report an issue with this question"
              >
                <FlagIcon className="h-5 w-5 text-neutral-500" />
              </button>
            )}
            {phase === 'content' && learningContent && (
              <button 
                onClick={() => {
                  setFlagType('learning_content')
                  setFlagContentId(learningContent.id)
                  setFlagContentTitle(learningContent.title)
                  setShowFlagModal(true)
                }}
                className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg"
                title="Report an issue with this content"
              >
                <FlagIcon className="h-5 w-5 text-neutral-500" />
              </button>
            )}
            <h2 className="text-xl font-bold ml-2">{node.name}</h2>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg">
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          ) : !learningContent ? (
            <div className="text-center py-8">
              <p className="text-neutral-600 dark:text-neutral-400">No learning content available for this module yet.</p>
            </div>
          ) : (
            <>
              {/* Pre-Quiz Phase */}
              {phase === 'pre-quiz' && currentQuestion && (
                <EnhancedQuestionDisplay
                  question={currentQuestion}
                  questionNumber={questionNumber}
                  totalQuestions={3}
                  onAnswerSelect={(optionIndex) => handleAnswerSelect(currentQuestionIndex, optionIndex)}
                  onSubmit={handleQuestionSubmit}
                  onNext={handleNextQuestion}
                  selectedAnswer={selectedAnswers[currentQuestionIndex]}
                  showExplanation={showExplanation}
                  isPreQuiz={true}
                />
              )}

              {/* Learning Content Phase */}
              {phase === 'content' && (
                <div className="relative">
                  {/* Flag button overlay for enhanced viewer */}
                  <div className="absolute top-4 left-4 z-10">
                    <button 
                      onClick={() => {
                        setFlagType('learning_content')
                        setFlagContentId(learningContent.id)
                        setFlagContentTitle(learningContent.title)
                        setShowFlagModal(true)
                      }}
                      className="p-2 bg-white dark:bg-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg shadow-md"
                      title="Report an issue with this content"
                    >
                      <FlagIcon className="h-5 w-5 text-neutral-500" />
                    </button>
                  </div>
                  
                  {questions.length > 0 && preQuizScore > 0 && (
                    <div className="bg-gradient-to-r from-gold-50 to-primary-50 dark:from-gold-900/20 dark:to-primary-900/20 p-4 rounded-xl border border-gold-200 dark:border-gold-800 mb-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-gold-700 dark:text-gold-300">Pre-Quiz Performance</p>
                          <p className="text-2xl font-bold text-gold-900 dark:text-gold-100">
                            {preQuizScore} / 3 correct
                          </p>
                        </div>
                        <div className="text-4xl">
                          {preQuizScore === 3 ? '🌟' : preQuizScore === 2 ? '⭐' : preQuizScore === 1 ? '✨' : '💫'}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Use enhanced viewer for HTML content */}
                  {learningContent.content && learningContent.content.includes('<') ? (
                    <LearningContentViewer
                      htmlContent={learningContent.content}
                      nodeId={learningContent.id}
                      nodeName={learningContent.title}
                      onComplete={() => {
                        if (questions.length > 0) {
                          startTest()
                        } else {
                          onClose()
                        }
                      }}
                      onProgress={(progress) => {
                        console.log(`Content progress: ${progress}%`)
                      }}
                    />
                  ) : learningContent.content_sections && learningContent.content_sections.length > 0 ? (
                    // Modern format with content_sections
                    learningContent.content_sections.map((section, index) => (
                      <div key={index} className="space-y-4">
                        {section.title && (
                          <h4 className="text-xl font-semibold">{section.title}</h4>
                        )}
                        <div className="prose dark:prose-invert max-w-none">
                          {section.content.split('\n').map((paragraph, pIndex) => (
                            <p key={pIndex} className="mb-4">{paragraph}</p>
                          ))}
                        </div>
                        {section.image && (
                          <figure>
                            <img src={section.image.url} alt="" className="rounded-lg max-w-full" />
                            {section.image.caption && (
                              <figcaption className="text-sm text-neutral-600 dark:text-neutral-400 mt-2">
                                {section.image.caption}
                              </figcaption>
                            )}
                          </figure>
                        )}
                      </div>
                    ))
                  ) : learningContent.content ? (
                    // Legacy format with HTML content or plain text
                    learningContent.content.includes('<') ? (
                      // HTML content - render directly (CSS is embedded in the content)
                      <div 
                        className="learning-content-container"
                        dangerouslySetInnerHTML={{ __html: learningContent.content }} 
                      />
                    ) : (
                      // Plain text content - split into paragraphs
                      <div className="prose dark:prose-invert max-w-none">
                        {learningContent.content.split('\n').map((paragraph, index) => (
                          <p key={index} className="mb-4">{paragraph}</p>
                        ))}
                      </div>
                    )
                  ) : (
                    // No content available
                    <p className="text-neutral-600 dark:text-neutral-400">No content available.</p>
                  )}

                  {/* Handle images array if present */}
                  {learningContent.images?.map((image, index) => (
                    <div key={index} className="my-4">
                      {typeof image === 'string' ? (
                        <img src={image} alt="" className="rounded-lg max-w-full" />
                      ) : (
                        <figure>
                          <img src={image.url} alt="" className="rounded-lg max-w-full" />
                          {image.caption && (
                            <figcaption className="text-sm text-neutral-600 dark:text-neutral-400 mt-2">
                              {image.caption}
                            </figcaption>
                          )}
                        </figure>
                      )}
                    </div>
                  ))}

                  {/* Source URL Display */}
                  {learningContent.source_url && (
                    <div className="bg-neutral-50 dark:bg-neutral-900 p-3 rounded-lg border-l-4 border-primary-500 mt-6">
                      <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-1">Source:</p>
                      <a 
                        href={learningContent.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-primary-600 dark:text-primary-400 hover:underline break-all"
                      >
                        {learningContent.source_url}
                      </a>
                    </div>
                  )}

                  <div className="flex justify-between items-center pt-6">
                    <div>
                      <p className="text-sm text-neutral-500">
                        Estimated time: {learningContent.estimated_time_minutes} minutes
                      </p>
                      {questions.length > 0 && contentViewTime < minContentViewTime && (
                        <p className="text-xs text-amber-600 dark:text-amber-400 mt-1">
                          <ClockIcon className="h-3 w-3 inline mr-1" />
                          Review content for {minContentViewTime - contentViewTime} more seconds to continue
                        </p>
                      )}
                    </div>
                    {questions.length > 0 ? (
                      <button 
                        onClick={startTest} 
                        disabled={contentViewTime < minContentViewTime}
                        className={`btn-primary ${
                          contentViewTime < minContentViewTime 
                            ? 'opacity-50 cursor-not-allowed' 
                            : ''
                        }`}
                        title={contentViewTime < minContentViewTime 
                          ? `Please review content for ${minContentViewTime - contentViewTime} more seconds` 
                          : 'Start the test'}
                      >
                        Take Test
                      </button>
                    ) : (
                      <button 
                        onClick={onClose} 
                        className="btn-primary"
                      >
                        Finish Reading
                      </button>
                    )}
                  </div>
                </div>
              )}

              {/* Test Phase */}
              {phase === 'test' && currentQuestion && (
                <EnhancedQuestionDisplay
                  question={currentQuestion}
                  questionNumber={questionNumber}
                  totalQuestions={questionsInPhase}
                  onAnswerSelect={(optionIndex) => handleAnswerSelect(currentQuestionIndex, optionIndex)}
                  onSubmit={handleQuestionSubmit}
                  onNext={handleNextQuestion}
                  selectedAnswer={selectedAnswers[currentQuestionIndex]}
                  showExplanation={showExplanation}
                  isPreQuiz={false}
                  timeLimit={90} // 90 seconds per question for test
                />
              )}

              {/* Results Phase */}
              {phase === 'results' && (
                <div className="space-y-6 text-center">
                  <h3 className="text-2xl font-bold">Test Complete!</h3>
                  
                  <div className="space-y-4">
                    <div className="bg-gradient-to-br from-neutral-100 to-neutral-50 dark:from-neutral-700 dark:to-neutral-800 p-6 rounded-xl">
                      <p className="text-3xl font-bold mb-2">
                        {testScore} / {questionsInPhase}
                      </p>
                      <p className="text-lg text-neutral-600 dark:text-neutral-400">
                        {testScore === questionsInPhase 
                          ? '🎉 Perfect Score!' 
                          : testScore >= questionsInPhase * 0.8
                          ? '🌟 Great Job!'
                          : testScore >= questionsInPhase * 0.6
                          ? '⭐ Good Progress!'
                          : '💪 Keep Practicing!'}
                      </p>
                      
                      {testScore === questionsInPhase && (
                        <div className="mt-4 p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
                          <p className="text-green-700 dark:text-green-300 font-semibold">
                            ✅ You passed this module with 100%!
                          </p>
                        </div>
                      )}
                    </div>

                    {preQuizScore > 0 && (
                      <div className="bg-gold-50 dark:bg-gold-900/20 p-3 rounded-lg">
                        <p className="text-sm font-medium text-gold-700 dark:text-gold-300">
                          Pre-Quiz Performance: {preQuizScore} / 3
                        </p>
                        <p className="text-xs text-neutral-600 dark:text-neutral-400 mt-1">
                          {preQuizScore === 3 
                            ? 'Excellent foundation knowledge!'
                            : preQuizScore === 2
                            ? 'Good starting point!'
                            : 'You learned a lot from the content!'}
                        </p>
                      </div>
                    )}
                    
                    <div className="text-xs text-neutral-500 dark:text-neutral-400">
                      Questions were adaptively selected from easy to harder difficulties
                    </div>
                  </div>

                  <button onClick={onClose} className="btn-primary">
                    Continue Learning
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
      
      {showFlagModal && (
        <FlagContentModal
          isOpen={showFlagModal}
          onClose={() => setShowFlagModal(false)}
          contentType={flagType}
          contentId={flagContentId}
          contentTitle={flagContentTitle}
        />
      )}
    </div>
  )
}

// Helper function to get difficulty color and label
const getDifficultyDisplay = (difficulty: string) => {
  const normalized = difficulty.toLowerCase()
  
  if (normalized.includes('easy') || normalized === '1') {
    return { label: 'Easy', color: 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30' }
  } else if (normalized.includes('hard') || normalized === '3') {
    return { label: 'Hard', color: 'text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/30' }
  } else if (normalized.includes('expert') || normalized === '4') {
    return { label: 'Expert', color: 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30' }
  } else {
    return { label: 'Medium', color: 'text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30' }
  }
}

// Separate component for displaying questions
const QuestionDisplay: React.FC<{
  question: Question
  selectedAnswer?: number
  onAnswerSelect: (index: number) => void
  showExplanation: boolean
}> = ({ question, selectedAnswer, onAnswerSelect, showExplanation }) => {
  const difficulty = getDifficultyDisplay(question.difficulty)
  
  return (
    <div className="space-y-4">
      <div className="flex items-start justify-between gap-4">
        <p className="text-lg flex-1">{question.question_text}</p>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${difficulty.color}`}>
          {difficulty.label}
        </span>
      </div>
      
      {question.image_url && (
        <img src={question.image_url} alt="" className="rounded-lg max-w-full" />
      )}

      <div className="space-y-2">
        {question.options.map((option, index) => {
          const isSelected = selectedAnswer === index
          const isCorrect = index === question.correct_answer
          
          return (
            <button
              key={index}
              onClick={() => !showExplanation && onAnswerSelect(index)}
              disabled={showExplanation}
              className={`w-full text-left p-3 rounded-lg border-2 transition-colors ${
                showExplanation
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

      {showExplanation && (
        <div className="p-4 bg-gold-50 dark:bg-gold-900/20 rounded-lg">
          <p className="font-semibold mb-2">Explanation:</p>
          <p className="text-sm">{question.explanation || 'No explanation available.'}</p>
        </div>
      )}
      
      {/* Question Source URL Display */}
      {question.source_url && (
        <div className="bg-neutral-50 dark:bg-neutral-900 p-3 rounded-lg border-l-4 border-primary-500">
          <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-1">Source:</p>
          <a 
            href={question.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary-600 dark:text-primary-400 hover:underline break-all"
          >
            {question.source_url}
          </a>
        </div>
      )}
    </div>
  )
}

export default LearningContentModal