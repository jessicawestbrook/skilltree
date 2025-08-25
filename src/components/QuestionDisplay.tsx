import React, { useState, useEffect } from 'react'
import {
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  TrophyIcon,
  LightBulbIcon,
  AcademicCapIcon,
  BookOpenIcon,
  BoltIcon,
  StarIcon,
  FlagIcon,
  FolderPlusIcon
} from '@heroicons/react/24/outline'
import { StarIcon as StarSolidIcon } from '@heroicons/react/24/solid'
import { useAuth } from '../contexts/AuthContext'
import { studyListService } from '../services/studyListService'
import FlagContentModal from './FlagContentModal'
import StudyListSelectionModal from './StudyListSelectionModal'
import { StudyList } from '../types/database.types'

export interface QuestionData {
  id: string
  question_text: string
  options: string[]
  correct_answer: string | number
  explanation?: string
  difficulty?: string
  image_url?: string
  estimated_time_seconds?: number
}

interface QuestionDisplayProps {
  question: QuestionData
  selectedAnswer: string | number | undefined
  onAnswerSelect: (answer: string | number) => void
  showExplanation: boolean
  isLoading?: boolean
  
  // Display options
  questionNumber?: number
  totalQuestions?: number
  questionType?: 'pre-quiz' | 'test' | 'assessment'
  
  // Scoring
  points?: number
  isCorrect?: boolean
  
  // Actions
  onNext?: () => void
  autoSubmit?: boolean
  
  // Custom styling
  className?: string
}

const QuestionDisplay: React.FC<QuestionDisplayProps> = ({
  question,
  selectedAnswer,
  onAnswerSelect,
  showExplanation,
  isLoading = false,
  questionNumber,
  totalQuestions,
  questionType = 'test',
  points,
  isCorrect,
  onNext,
  autoSubmit = false,
  className = ''
}) => {
  const { user } = useAuth()
  const [isStarred, setIsStarred] = useState(false)
  const [isLoadingStudyList, setIsLoadingStudyList] = useState(false)
  const [showFlagModal, setShowFlagModal] = useState(false)
  const [showStudyListModal, setShowStudyListModal] = useState(false)
  const [userStudyLists, setUserStudyLists] = useState<StudyList[]>([])
  const [hasSubmitted, setHasSubmitted] = useState(false)
  // Get the correct answer as string for comparison
  const correctAnswerString = typeof question.correct_answer === 'number' 
    ? question.options[question.correct_answer]
    : question.correct_answer

  // Check if current answer is correct
  const isAnswerCorrect = isCorrect !== undefined 
    ? isCorrect 
    : selectedAnswer === correctAnswerString

  // Check if question is starred on mount
  useEffect(() => {
    const checkStarred = async () => {
      if (user && question.id) {
        const starred = await studyListService.isItemStarred(
          user.id,
          'question',
          question.id
        )
        setIsStarred(starred)
      }
    }
    checkStarred()
  }, [user, question.id])

  // Reset submission state when question changes
  useEffect(() => {
    setHasSubmitted(false)
  }, [question.id])

  // Fetch user's study lists
  useEffect(() => {
    const fetchStudyLists = async () => {
      if (user) {
        const lists = await studyListService.getUserStudyLists(user.id)
        setUserStudyLists(lists)
      }
    }
    fetchStudyLists()
  }, [user])

  // Toggle star status
  const toggleStar = async () => {
    if (!user || isLoadingStudyList) return
    
    setIsLoadingStudyList(true)
    try {
      if (isStarred) {
        await studyListService.unstarItem(
          user.id,
          'question',
          question.id
        )
      } else {
        await studyListService.starItem(
          user.id,
          'question',
          question.id,
          {
            question_text: question.question_text,
            options: question.options,
            correct_answer: question.correct_answer,
            difficulty: question.difficulty
          }
        )
      }
      setIsStarred(!isStarred)
    } catch (error) {
      console.error('Error toggling study list:', error)
    } finally {
      setIsLoadingStudyList(false)
    }
  }

  // Get difficulty display info
  const getDifficultyInfo = (difficulty?: string) => {
    const normalized = difficulty?.toLowerCase() || 'medium'
    
    if (normalized.includes('easy') || normalized === '1') {
      return { 
        label: 'Easy', 
        color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
        borderColor: 'border-green-400',
        gradient: 'from-green-400 to-green-600'
      }
    } else if (normalized.includes('hard') || normalized === '3') {
      return { 
        label: 'Hard', 
        color: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300',
        borderColor: 'border-orange-400',
        gradient: 'from-orange-400 to-orange-600'
      }
    } else if (normalized.includes('expert') || normalized === '4' || normalized === '5') {
      return { 
        label: 'Expert', 
        color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
        borderColor: 'border-red-400',
        gradient: 'from-red-400 to-red-600'
      }
    } else {
      return { 
        label: 'Medium', 
        color: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
        borderColor: 'border-blue-400',
        gradient: 'from-blue-400 to-blue-600'
      }
    }
  }

  const difficulty = getDifficultyInfo(question.difficulty)

  // Progress percentage
  const progressPercentage = questionNumber && totalQuestions && !isNaN(totalQuestions)
    ? (questionNumber / totalQuestions) * 100 
    : 0

  // Get question type icon
  const getQuestionTypeIcon = () => {
    switch (questionType) {
      case 'pre-quiz':
        return <AcademicCapIcon className="h-4 w-4 text-primary-600" />
      case 'assessment':
        return <BoltIcon className="h-4 w-4 text-gold-500" />
      default:
        return <BookOpenIcon className="h-4 w-4 text-primary-600" />
    }
  }

  // Handle answer click
  const handleAnswerClick = (answer: string) => {
    if (!showExplanation && !isLoading && !hasSubmitted) {
      onAnswerSelect(answer)
      setHasSubmitted(true)
      
      // Auto-submit if enabled - this should trigger parent to show explanation
      // We don't call onNext here - that's for when user clicks Next button
    }
  }

  return (
    <div className={`flex flex-col bg-white dark:bg-neutral-900 ${className}`}>
      {/* Header with progress */}
      {(questionNumber || totalQuestions) && (
        <div className="bg-white dark:bg-neutral-900 pb-2">
          {/* Progress bar */}
          {progressPercentage > 0 && (
            <div className="h-1 bg-neutral-200 dark:bg-neutral-700 rounded-full overflow-hidden mb-3">
              <div 
                className="h-full bg-gradient-to-r from-primary-400 to-primary-600 transition-all duration-500 ease-out"
                style={{ width: `${progressPercentage}%` }}
              />
            </div>
          )}
          
          {/* Question header */}
          <div className="flex justify-between items-center px-2">
            <div className="flex items-center gap-3">
              {getQuestionTypeIcon()}
              <h3 className="text-sm font-semibold text-neutral-800 dark:text-neutral-100">
                {questionType === 'pre-quiz' ? 'Pre-Quiz' : 
                 questionType === 'assessment' ? 'Assessment' : 'Test'}
              </h3>
              {questionNumber && totalQuestions && !isNaN(totalQuestions) && (
                <span className="text-xs text-neutral-500 dark:text-neutral-400">
                  Q{questionNumber}/{totalQuestions}
                </span>
              )}
              {questionNumber && !totalQuestions && (
                <span className="text-xs text-neutral-500 dark:text-neutral-400">
                  Q{questionNumber}
                </span>
              )}
              
              {/* Flag button - moved to left side */}
              {user && (
                <button
                  onClick={() => setShowFlagModal(true)}
                  className="p-1.5 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
                  title="Report an issue"
                >
                  <FlagIcon className="h-5 w-5 text-neutral-400 dark:text-neutral-500 hover:text-red-500" />
                </button>
              )}
            </div>
            
            <div className="flex items-center gap-2">
              {/* Star button */}
              {user && (
                <button
                  onClick={toggleStar}
                  disabled={isLoadingStudyList}
                  className="p-1.5 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
                  title={isStarred ? "Remove from starred" : "Add to starred"}
                >
                  {isStarred ? (
                    <StarSolidIcon className="h-5 w-5 text-gold-500" />
                  ) : (
                    <StarIcon className="h-5 w-5 text-neutral-400 dark:text-neutral-500 hover:text-gold-500" />
                  )}
                </button>
              )}
              
              {/* Add to study list button */}
              {user && (
                <button
                  onClick={() => setShowStudyListModal(true)}
                  className="p-1.5 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
                  title="Add to study list"
                >
                  <FolderPlusIcon className="h-5 w-5 text-neutral-400 dark:text-neutral-500 hover:text-primary-500" />
                </button>
              )}
              
              {/* Timer if provided */}
              {question.estimated_time_seconds && !showExplanation && (
                <div className="flex items-center gap-1 px-2 py-1 rounded-full bg-neutral-100 dark:bg-neutral-800 text-xs">
                  <ClockIcon className="h-3 w-3 text-neutral-500" />
                  <span className="text-neutral-600 dark:text-neutral-400">
                    {question.estimated_time_seconds}s
                  </span>
                </div>
              )}
              
              {/* Difficulty badge */}
              {question.difficulty && (
                <div className={`px-2 py-1 rounded-full text-xs font-medium ${difficulty.color}`}>
                  {difficulty.label}
                  {points && <span> • {points} pts</span>}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Question content */}
      <div className={`transition-all duration-300 rounded-xl ${questionType === 'assessment' ? 'p-2' : 'p-4'} ${questionType === 'assessment' ? 'mt-1' : 'mt-2'}
        ${showExplanation 
          ? isAnswerCorrect
            ? 'bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20' 
            : 'bg-gradient-to-br from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20'
          : 'bg-white dark:bg-neutral-800'
        }`}>
        
        {/* Question text */}
        <div className={questionType === 'assessment' ? 'mb-3' : 'mb-4'}>
          <p className={`${questionType === 'assessment' ? 'text-base' : 'text-base md:text-lg'} leading-relaxed text-neutral-800 dark:text-neutral-100 font-medium`}>
            {question.question_text}
          </p>
        </div>

        {/* Question image if present */}
        {question.image_url && (
          <div className="mb-4 flex justify-center">
            <img 
              src={question.image_url} 
              alt="Question illustration" 
              className="max-w-full h-auto rounded-lg shadow-md"
              style={{ maxHeight: '300px' }}
            />
          </div>
        )}

        {/* Answer options */}
        <div className={`${questionType === 'assessment' ? 'space-y-1.5' : 'space-y-2'} mb-4`}>
          {question.options.map((option, index) => {
            const isSelected = selectedAnswer === option
            const isThisCorrect = option === correctAnswerString
            const isIncorrect = isSelected && !isThisCorrect && showExplanation
            
            // More compact padding for assessments
            const paddingClass = questionType === 'assessment' ? 'p-2' : 'p-3'
            let optionClass = `w-full text-left ${paddingClass} rounded-xl border-2 transition-all duration-200 `
            
            if (!autoSubmit) {
              // Standard quiz style (hover effects)
              optionClass += 'transform hover:scale-[1.02] '
            }
            
            if (showExplanation) {
              if (isThisCorrect) {
                optionClass += 'border-green-400 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 shadow-lg'
              } else if (isIncorrect) {
                optionClass += 'border-red-400 bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/30 dark:to-pink-900/30 shadow-lg'
              } else {
                optionClass += 'border-neutral-200 dark:border-neutral-700 bg-neutral-50 dark:bg-neutral-800/50 opacity-60'
              }
            } else {
              if (isSelected) {
                optionClass += 'border-primary-400 bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/30 dark:to-blue-900/30 shadow-lg scale-[1.02]'
              } else {
                optionClass += 'border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 hover:border-primary-300 hover:shadow-md cursor-pointer'
              }
            }

            // Smaller option letters for assessments
            const letterSize = questionType === 'assessment' ? 'w-7 h-7 text-xs' : 'w-8 h-8 text-sm'
            const optionTextSize = questionType === 'assessment' ? 'text-sm' : 'text-sm'

            return (
              <button
                key={index}
                onClick={() => handleAnswerClick(option)}
                disabled={showExplanation || isLoading}
                className={optionClass}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <span className={`flex-shrink-0 ${letterSize} bg-neutral-100 dark:bg-neutral-700 rounded-lg flex items-center justify-center font-bold text-neutral-600 dark:text-neutral-300`}>
                      {String.fromCharCode(65 + index)}
                    </span>
                    <span className={`${optionTextSize} font-medium text-neutral-800 dark:text-neutral-100`}>
                      {option}
                    </span>
                  </div>
                  {showExplanation && isThisCorrect && (
                    <CheckCircleIcon className="h-5 w-5 text-green-500 flex-shrink-0" />
                  )}
                  {showExplanation && isIncorrect && (
                    <XCircleIcon className="h-5 w-5 text-red-500 flex-shrink-0" />
                  )}
                </div>
              </button>
            )
          })}
        </div>

        {/* Explanation section */}
        {showExplanation && question.explanation && (
          <div className={`${questionType === 'assessment' ? 'mt-2 p-2' : 'mt-4 p-4'} bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl border border-blue-200 dark:border-blue-800`}>
            <div className={`flex items-start ${questionType === 'assessment' ? 'gap-2' : 'gap-3'}`}>
              <LightBulbIcon className={`${questionType === 'assessment' ? 'h-4 w-4' : 'h-5 w-5'} text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0`} />
              <div className="flex-1">
                <h4 className={`font-semibold text-blue-900 dark:text-blue-100 ${questionType === 'assessment' ? 'mb-1 text-xs' : 'mb-2'}`}>
                  Explanation
                </h4>
                <p className={`${questionType === 'assessment' ? 'text-xs' : 'text-sm'} text-blue-800 dark:text-blue-200 leading-relaxed`}>
                  {question.explanation}
                </p>
              </div>
            </div>
            
            {/* Result display */}
            <div className={`${questionType === 'assessment' ? 'mt-2 pt-2' : 'mt-4 pt-3'} border-t border-blue-200 dark:border-blue-700 flex items-center justify-between`}>
              <div className="flex items-center gap-2">
                {isAnswerCorrect ? (
                  <>
                    <CheckCircleIcon className="h-5 w-5 text-green-500" />
                    <span className="text-sm font-semibold text-green-700 dark:text-green-300">
                      Correct Answer!
                    </span>
                  </>
                ) : (
                  <>
                    <XCircleIcon className="h-5 w-5 text-red-500" />
                    <span className="text-sm font-semibold text-red-700 dark:text-red-300">
                      Not Quite Right
                    </span>
                  </>
                )}
              </div>
              
              {points && isAnswerCorrect && (
                <div className="flex items-center gap-2">
                  <TrophyIcon className="h-4 w-4 text-gold-500" />
                  <span className="text-sm font-bold text-gold-700 dark:text-gold-300">
                    +{points} pts
                  </span>
                </div>
              )}
            </div>
          </div>
        )}


        {/* Loading state */}
        {isLoading && (
          <div className="mt-4 flex justify-center">
            <div className="px-5 py-2.5 bg-neutral-200 dark:bg-neutral-700 rounded-xl flex items-center gap-2">
              <div className="animate-spin h-4 w-4 border-2 border-neutral-400 border-t-transparent rounded-full"></div>
              <span className="text-sm font-medium text-neutral-600 dark:text-neutral-400">Processing...</span>
            </div>
          </div>
        )}
      </div>
      
      {/* Flag Modal */}
      {showFlagModal && (
        <FlagContentModal
          isOpen={showFlagModal}
          onClose={() => setShowFlagModal(false)}
          contentType="question"
          contentId={question.id}
          contentTitle={question.question_text}
        />
      )}
      
      {/* Study List Selection Modal */}
      {showStudyListModal && (
        <StudyListSelectionModal
          isOpen={showStudyListModal}
          onClose={() => setShowStudyListModal(false)}
          itemType="question"
          itemId={question.id}
          itemData={{
            question_text: question.question_text,
            options: question.options,
            correct_answer: question.correct_answer,
            explanation: question.explanation,
            difficulty: question.difficulty
          }}
          itemTitle={question.question_text}
          userStudyLists={userStudyLists}
          onStudyListsUpdate={async () => {
            // Refresh study lists
            if (user) {
              const lists = await studyListService.getUserStudyLists(user.id)
              setUserStudyLists(lists)
            }
          }}
        />
      )}
    </div>
  )
}

export default QuestionDisplay