import React, { useState, useEffect, useCallback } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { spacedRepetitionService, ReviewResponse } from '../services/spacedRepetitionService'
import { useAuth } from '../contexts/AuthContext'
import SpellingBeeCard from '../components/flashcards/SpellingBeeCard'
import VocabularyCard from '../components/flashcards/VocabularyCard'
import LanguageCard from '../components/flashcards/LanguageCard'
import {
  CheckCircleIcon,
  XCircleIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
  ChartBarIcon,
  ClockIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'

interface StudyItem {
  id: string
  type: string
  data: any
}

interface ReviewStats {
  total: number
  completed: number
  correct: number
  incorrect: number
  startTime: number
  totalTime: number
}

const StudyListReviewPage: React.FC = () => {
  const { user } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  
  const [items, setItems] = useState<StudyItem[]>([])
  const [currentIndex, setCurrentIndex] = useState(location.state?.startIndex || 0)
  const [loading, setLoading] = useState(true)
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [userAnswer, setUserAnswer] = useState<string>('')
  const [selectedOption, setSelectedOption] = useState<number | null>(null)
  const [stats, setStats] = useState<ReviewStats>({
    total: 0,
    completed: 0,
    correct: 0,
    incorrect: 0,
    startTime: Date.now(),
    totalTime: 0
  })

  // Load items from navigation state
  useEffect(() => {
    const loadItems = async () => {
      if (!location.state?.items) {
        console.error('No items provided to review')
        navigate('/study-lists')
        return
      }

      const reviewItems = location.state.items as StudyItem[]
      const listName = location.state.listName || 'Study List'
      
      // Load full data for each item based on type
      const fullItems = await Promise.all(
        reviewItems.map(async (item) => {
          let fullData = null
          
          switch (item.type) {
            case 'spelling_word':
            case 'vocabulary_word':
              const { data: word } = await supabase
                .from('spelling_words')
                .select('*')
                .eq('id', item.id)
                .single()
              fullData = word
              break
              
            case 'language_question':
              const { data: langQuestion } = await supabase
                .from('language_questions')
                .select('*')
                .eq('id', item.id)
                .single()
              fullData = langQuestion
              break
              
            case 'question':
              const { data: question } = await supabase
                .from('questions')
                .select('*')
                .eq('id', item.id)
                .single()
              fullData = question
              break
              
            case 'skill_node':
              // For skill nodes, we might want to load associated questions
              fullData = item.data
              break
              
            default:
              fullData = item.data
          }
          
          return {
            ...item,
            data: fullData || item.data
          }
        })
      )
      
      setItems(fullItems)
      setStats(prev => ({ ...prev, total: fullItems.length }))
      setLoading(false)
    }
    
    loadItems()
  }, [location.state, navigate])

  const currentItem = items[currentIndex] || null

  const handleAnswer = useCallback((answer: string | number) => {
    if (!currentItem) return
    
    let correct = false
    
    switch (currentItem.type) {
      case 'spelling_word':
        correct = answer.toString().toLowerCase() === currentItem.data.word?.toLowerCase()
        break
        
      case 'vocabulary_word':
        // For vocabulary, check if selected definition matches
        if (typeof answer === 'number') {
          const options = currentItem.data.options || []
          correct = options[answer] === currentItem.data.definition
        } else {
          correct = answer.toLowerCase() === currentItem.data.definition?.toLowerCase()
        }
        break
        
      case 'language_question':
        if (typeof answer === 'number') {
          correct = answer === currentItem.data.correct_answer_index
        }
        break
        
      case 'question':
        if (typeof answer === 'number' && currentItem.data.options) {
          correct = answer === currentItem.data.correct_answer_index
        } else {
          correct = answer.toString().toLowerCase() === currentItem.data.correct_answer?.toLowerCase()
        }
        break
    }
    
    setIsCorrect(correct)
    setShowResult(true)
    
    // Update stats
    setStats(prev => ({
      ...prev,
      completed: prev.completed + 1,
      correct: prev.correct + (correct ? 1 : 0),
      incorrect: prev.incorrect + (correct ? 0 : 1)
    }))
    
    // Record with spaced repetition service if user is logged in
    if (user) {
      const reviewResponse: ReviewResponse = {
        quality: correct ? 5 : 1, // 5 for perfect recall, 1 for incorrect
        time_taken: Math.floor((Date.now() - stats.startTime) / 1000), // in seconds
        hint_used: false
      }
      spacedRepetitionService.recordReview(
        user.id,
        currentItem.id,
        currentItem.type as any,
        reviewResponse
      ).catch(console.error)
    }
  }, [currentItem, user, stats.startTime])

  const handleNext = useCallback(() => {
    if (currentIndex < items.length - 1) {
      setCurrentIndex((prev: number) => prev + 1)
      setShowResult(false)
      setUserAnswer('')
      setSelectedOption(null)
    } else {
      // Session complete
      const totalTime = Date.now() - stats.startTime
      setStats(prev => ({ ...prev, totalTime }))
      // Could show a completion modal here
    }
  }, [currentIndex, items.length, stats.startTime])

  const handlePrevious = useCallback(() => {
    if (currentIndex > 0) {
      setCurrentIndex((prev: number) => prev - 1)
      setShowResult(false)
      setUserAnswer('')
      setSelectedOption(null)
    }
  }, [currentIndex])

  const handleExit = () => {
    if (window.confirm('Are you sure you want to exit this study session?')) {
      navigate('/study-lists')
    }
  }

  const renderCard = () => {
    if (!currentItem) return null
    
    switch (currentItem.type) {
      case 'spelling_word':
        return (
          <SpellingBeeCard
            word={currentItem.data?.word || ''}
            definition={currentItem.data?.definition}
            partOfSpeech={currentItem.data?.part_of_speech}
            difficulty={currentItem.data?.spelling_difficulty_id}
            userInput={userAnswer}
            showResult={showResult}
            isCorrect={isCorrect}
            onInputChange={setUserAnswer}
            onPlayAudio={() => {
              // Play audio implementation
              if ('speechSynthesis' in window && currentItem.data?.word) {
                const utterance = new SpeechSynthesisUtterance(currentItem.data.word)
                utterance.rate = 0.8
                window.speechSynthesis.speak(utterance)
              }
            }}
          />
        )
        
      case 'vocabulary_word':
        return (
          <VocabularyCard
            word={currentItem.data?.word || ''}
            definition={currentItem.data?.definition}
            partOfSpeech={currentItem.data?.part_of_speech}
            difficulty={currentItem.data?.vocabulary_difficulty_id}
            selectedOption={selectedOption}
            showResult={showResult}
            onSelectOption={(index: number) => {
              setSelectedOption(index)
              handleAnswer(index)
            }}
          />
        )
        
      case 'language_question':
        return (
          <LanguageCard
            language={currentItem.data?.language_id || 'Unknown'}
            questionText={currentItem.data?.question_text || ''}
            options={currentItem.data?.options || []}
            correctAnswer={currentItem.data?.options?.[currentItem.data?.correct_answer_index]}
            explanation={currentItem.data?.explanation}
            selectedOption={selectedOption}
            showResult={showResult}
            onSelectOption={(index: number) => {
              setSelectedOption(index)
              handleAnswer(index)
            }}
          />
        )
        
      case 'question':
        // For general questions, we can use a generic question card
        return (
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-2">
                {currentItem.data.question_text}
              </h3>
              {currentItem.data.options && (
                <div className="space-y-2 mt-4">
                  {currentItem.data.options.map((option: string, index: number) => (
                    <button
                      key={index}
                      onClick={() => {
                        setSelectedOption(index)
                        handleAnswer(index)
                      }}
                      disabled={showResult}
                      className={`w-full text-left p-3 rounded-lg border transition-all ${
                        showResult && index === currentItem.data.correct_answer_index
                          ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                          : showResult && index === selectedOption && !isCorrect
                          ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                          : selectedOption === index
                          ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                          : 'border-neutral-200 dark:border-neutral-700 hover:border-primary-400'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              )}
            </div>
            
            {showResult && (
              <div className={`p-4 rounded-lg ${isCorrect ? 'bg-green-100 dark:bg-green-900/30' : 'bg-red-100 dark:bg-red-900/30'}`}>
                <div className="flex items-center gap-2">
                  {isCorrect ? (
                    <CheckCircleIcon className="h-5 w-5 text-green-600" />
                  ) : (
                    <XCircleIcon className="h-5 w-5 text-red-600" />
                  )}
                  <span className={`font-medium ${isCorrect ? 'text-green-600' : 'text-red-600'}`}>
                    {isCorrect ? 'Correct!' : 'Incorrect'}
                  </span>
                </div>
                {currentItem.data.explanation && (
                  <p className="mt-2 text-sm text-neutral-600 dark:text-neutral-400">
                    {currentItem.data.explanation}
                  </p>
                )}
              </div>
            )}
          </div>
        )
        
      default:
        return (
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
            <p className="text-neutral-500">Unsupported item type: {currentItem.type}</p>
          </div>
        )
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const progress = (stats.completed / stats.total) * 100

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">
            {location.state?.listName || 'Study Session'}
          </h1>
          <button
            onClick={handleExit}
            className="p-2 text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
        
        {/* Progress bar */}
        <div className="bg-neutral-200 dark:bg-neutral-700 rounded-full h-2 overflow-hidden">
          <div
            className="bg-primary-500 h-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
        
        {/* Stats */}
        <div className="flex items-center justify-between mt-2 text-sm text-neutral-600 dark:text-neutral-400">
          <span>{currentIndex + 1} / {items.length}</span>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <CheckCircleIcon className="h-4 w-4 text-green-500" />
              {stats.correct}
            </span>
            <span className="flex items-center gap-1">
              <XCircleIcon className="h-4 w-4 text-red-500" />
              {stats.incorrect}
            </span>
          </div>
        </div>
      </div>

      {/* Card Content */}
      <div className="mb-6">
        {renderCard()}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <button
          onClick={handlePrevious}
          disabled={currentIndex === 0}
          className="flex items-center gap-2 px-4 py-2 text-neutral-600 dark:text-neutral-400 disabled:opacity-50 disabled:cursor-not-allowed hover:text-neutral-900 dark:hover:text-white"
        >
          <ArrowLeftIcon className="h-5 w-5" />
          Previous
        </button>
        
        {showResult && (
          <button
            onClick={handleNext}
            className="flex items-center gap-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            {currentIndex < items.length - 1 ? (
              <>
                Next
                <ArrowRightIcon className="h-5 w-5" />
              </>
            ) : (
              'Complete'
            )}
          </button>
        )}
      </div>

      {/* Completion Modal */}
      {stats.completed === stats.total && stats.total > 0 && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-xl p-8 max-w-md">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white mb-4">
              Session Complete!
            </h2>
            <div className="space-y-2 mb-6">
              <p className="text-neutral-600 dark:text-neutral-400">
                Total Questions: {stats.total}
              </p>
              <p className="text-green-600">
                Correct: {stats.correct} ({Math.round((stats.correct / stats.total) * 100)}%)
              </p>
              <p className="text-red-600">
                Incorrect: {stats.incorrect}
              </p>
              <p className="text-neutral-600 dark:text-neutral-400">
                Time: {Math.round(stats.totalTime / 1000)}s
              </p>
            </div>
            <button
              onClick={() => navigate('/study-lists')}
              className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Back to Study Lists
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default StudyListReviewPage