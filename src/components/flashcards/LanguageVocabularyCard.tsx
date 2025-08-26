import React, { useState, useEffect } from 'react'
import { supabase } from '../../services/supabase'
import { useAuth } from '../../contexts/AuthContext'
import { DeckProgressionService } from '../../services/deckProgressionService'
import { StudyListService } from '../../services/studyListService'
import {
  SpeakerWaveIcon,
  EyeIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  StarIcon,
  AcademicCapIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid'

interface VocabularyWord {
  id: string
  language: string
  word: string
  zipf_frequency: number
  difficulty_id: number
  difficulty_name?: string
  english_translation: string
  pronunciation_guide: string
  part_of_speech: string
  definition_english: string
  example_sentence?: string
  example_sentence_translation?: string
  memory_tips?: string
}

interface LanguageVocabularyCardProps {
  word: VocabularyWord
  onNext: () => void
  onDifficulty: (difficulty: 'easy' | 'medium' | 'hard') => void
  isReviewMode?: boolean
  deckStatus?: 'learning' | 'review' | 'mastered'
  onStatusChange?: (newStatus: string, message: string) => void
}

const LanguageVocabularyCard: React.FC<LanguageVocabularyCardProps> = ({
  word,
  onNext,
  onDifficulty,
  isReviewMode = false,
  deckStatus,
  onStatusChange
}) => {
  const { user } = useAuth()
  const [showAnswer, setShowAnswer] = useState(false)
  const [flipped, setFlipped] = useState(false)
  const [hasVoice, setHasVoice] = useState(false)
  const [isInDeck, setIsInDeck] = useState(false)
  const [isStarring, setIsStarring] = useState(false)

  // Check if word is in deck
  useEffect(() => {
    const checkDeckStatus = async () => {
      if (user) {
        const inDeck = await DeckProgressionService.isVocabularyInDeck(user.id, word.id)
        setIsInDeck(inDeck)
      }
    }
    checkDeckStatus()
  }, [user, word.id])

  // Check for language voice availability
  useEffect(() => {
    if ('speechSynthesis' in window) {
      const checkVoices = () => {
        const voices = window.speechSynthesis.getVoices()
        const languageVoice = voices.find(voice => 
          voice.lang.toLowerCase().startsWith(word.language.toLowerCase())
        )
        setHasVoice(!!languageVoice)
      }

      if (window.speechSynthesis.getVoices().length === 0) {
        window.speechSynthesis.onvoiceschanged = checkVoices
      } else {
        checkVoices()
      }
    }
  }, [word.language])

  const speakWord = (text: string, language: string = word.language) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel()
      
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.8
      utterance.volume = 0.8
      utterance.lang = language === 'es' ? 'es-ES' : language
      
      const voices = window.speechSynthesis.getVoices()
      const languageVoice = voices.find(voice => 
        voice.lang.toLowerCase().startsWith(language.toLowerCase())
      )
      
      if (languageVoice) {
        utterance.voice = languageVoice
      }
      
      window.speechSynthesis.speak(utterance)
    }
  }

  const handleFlip = () => {
    setFlipped(!flipped)
    setShowAnswer(!showAnswer)
    
    // Auto-play pronunciation when flipping to answer
    if (!showAnswer && hasVoice && localStorage.getItem('audioAutoplay') !== 'false') {
      setTimeout(() => speakWord(word.word), 300)
    }
  }

  const handleStar = async () => {
    if (!user || isStarring) return
    
    setIsStarring(true)
    try {
      const studyListService = new StudyListService()
      
      if (!isInDeck) {
        // Star the item (which will auto-add to learning deck via trigger)
        const success = await studyListService.starItem(
          user.id,
          'vocabulary_word',
          word.id,
          {
            word: word.word,
            translation: word.english_translation,
            language: word.language
          }
        )
        
        if (success) {
          setIsInDeck(true)
          if (onStatusChange) {
            onStatusChange('learning', '⭐ Added to learning deck!')
          }
        }
      } else {
        // Remove from deck
        const result = await DeckProgressionService.removeFromDeck(user.id, 'vocabulary', word.id)
        if (result.success) {
          setIsInDeck(false)
          // Also unstar it
          await studyListService.unstarItem(user.id, 'vocabulary_word', word.id)
          if (onStatusChange) {
            onStatusChange('', 'Removed from deck')
          }
        }
      }
    } catch (error) {
      console.error('Error toggling star:', error)
    } finally {
      setIsStarring(false)
    }
  }

  const handleDifficulty = async (difficulty: 'easy' | 'medium' | 'hard') => {
    if (user) {
      
      // Update deck progression using the new service method
      const result = await DeckProgressionService.recordVocabularyReview(
        user.id,
        word.id,
        difficulty
      )
      
      if (result.message && onStatusChange) {
        onStatusChange(result.newStatus || deckStatus || 'learning', result.message)
      }
      
      // Also record the review in the progress table for spaced repetition
      try {
        const { data: existing } = await supabase
          .from('language_vocabulary_progress')
          .select('*')
          .eq('user_id', user.id)
          .eq('vocabulary_id', word.id)
          .single()

        const isCorrect = difficulty === 'easy'
        
        if (existing) {
          await supabase
            .from('language_vocabulary_progress')
            .update({
              times_reviewed: existing.times_reviewed + 1,
              times_correct: existing.times_correct + (isCorrect ? 1 : 0),
              last_reviewed: new Date().toISOString(),
              // Update spaced repetition intervals based on difficulty
              interval_days: difficulty === 'easy' ? existing.interval_days * 2.5 : 
                           difficulty === 'medium' ? existing.interval_days * 1.3 : 1,
              ease_factor: difficulty === 'easy' ? Math.min(existing.ease_factor + 0.1, 2.5) :
                          difficulty === 'hard' ? Math.max(existing.ease_factor - 0.2, 1.3) :
                          existing.ease_factor
            })
            .eq('id', existing.id)
        } else {
          await supabase
            .from('language_vocabulary_progress')
            .insert({
              user_id: user.id,
              vocabulary_id: word.id,
              times_reviewed: 1,
              times_correct: isCorrect ? 1 : 0,
              last_reviewed: new Date().toISOString(),
              interval_days: difficulty === 'easy' ? 4 : difficulty === 'medium' ? 2 : 1,
              ease_factor: 2.5
            })
        }
      } catch (error) {
        console.error('Error recording progress:', error)
      }
    }
    
    onDifficulty(difficulty)
    onNext()
  }

  // Get difficulty color
  const getDifficultyColor = () => {
    switch (word.difficulty_id) {
      case 1: return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' // Basic
      case 2: return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' // Elementary
      case 3: return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' // Intermediate
      case 4: return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' // Advanced
      case 5: return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' // Expert
      default: return 'bg-neutral-100 text-neutral-700 dark:bg-neutral-900/30 dark:text-neutral-400'
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Flashcard */}
      <div 
        className="relative h-64 sm:h-80 cursor-pointer perspective-1000"
        onClick={handleFlip}
      >
        <div className={`absolute inset-0 w-full h-full transition-transform duration-500 transform-style-preserve-3d ${
          flipped ? 'rotate-y-180' : ''
        }`}>
          {/* Front of card - Foreign word */}
          <div className="absolute inset-0 w-full h-full backface-hidden">
            <div className="h-full bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/20 rounded-xl p-6 border-2 border-primary-200 dark:border-primary-700 shadow-lg flex flex-col justify-center items-center">
              {/* Difficulty and deck status badges */}
              <div className="absolute top-4 right-4 flex flex-col gap-2">
                <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor()}`}>
                  {word.difficulty_name || `Level ${word.difficulty_id}`}
                </span>
                {deckStatus && (
                  <span className={`px-2 py-1 rounded text-xs font-medium flex items-center gap-1 ${
                    deckStatus === 'learning' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                    deckStatus === 'review' ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400' :
                    'bg-gold-100 text-gold-700 dark:bg-gold-900/30 dark:text-gold-400'
                  }`}>
                    {deckStatus === 'learning' && <AcademicCapIcon className="h-3 w-3" />}
                    {deckStatus === 'review' && <StarIcon className="h-3 w-3" />}
                    {deckStatus === 'mastered' && <SparklesIcon className="h-3 w-3" />}
                    {deckStatus === 'learning' ? 'Learning' : 
                     deckStatus === 'review' ? 'Review' : 'Mastered'}
                  </span>
                )}
              </div>
              
              {/* Language indicator and star button */}
              <div className="absolute top-4 left-4 flex items-center gap-2">
                <span className="px-2 py-1 rounded text-xs font-medium bg-neutral-100 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-300">
                  {word.language === 'es' ? '🇪🇸 Spanish' : word.language.toUpperCase()}
                </span>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    handleStar()
                  }}
                  disabled={isStarring}
                  className="p-1.5 rounded-lg bg-white dark:bg-neutral-800 shadow-md hover:shadow-lg transition-all disabled:opacity-50"
                  title={isInDeck ? 'Remove from deck' : 'Add to learning deck'}
                >
                  {isInDeck ? (
                    <StarIconSolid className="h-5 w-5 text-gold-500" />
                  ) : (
                    <StarIcon className="h-5 w-5 text-neutral-400 hover:text-gold-500" />
                  )}
                </button>
              </div>
              
              {/* Main word */}
              <div className="text-center">
                <h2 className="text-4xl sm:text-5xl font-bold text-neutral-800 dark:text-neutral-100 mb-4">
                  {word.word}
                </h2>
                
                {/* Part of speech */}
                {word.part_of_speech && (
                  <p className="text-sm text-neutral-600 dark:text-neutral-400 italic">
                    {word.part_of_speech}
                  </p>
                )}
                
                {/* Pronunciation guide */}
                {word.pronunciation_guide && (
                  <p className="text-lg text-neutral-700 dark:text-neutral-300 mt-2">
                    [{word.pronunciation_guide}]
                  </p>
                )}
              </div>
              
              {/* Audio button */}
              {hasVoice && (
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    speakWord(word.word)
                  }}
                  className="absolute bottom-4 right-4 p-2 bg-white dark:bg-neutral-800 rounded-lg shadow-md hover:shadow-lg transition-shadow"
                  title="Hear pronunciation"
                >
                  <SpeakerWaveIcon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
                </button>
              )}
              
              {/* Flip hint */}
              <div className="absolute bottom-4 left-4 flex items-center gap-2 text-xs text-neutral-500 dark:text-neutral-400">
                <EyeIcon className="h-4 w-4" />
                <span>Click to reveal</span>
              </div>
            </div>
          </div>
          
          {/* Back of card - Translation and details */}
          <div className="absolute inset-0 w-full h-full backface-hidden rotate-y-180">
            <div className="h-full bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/30 dark:to-green-800/20 rounded-xl p-6 border-2 border-green-200 dark:border-green-700 shadow-lg overflow-y-auto">
              {/* Translation */}
              <div className="text-center mb-4">
                <h3 className="text-3xl sm:text-4xl font-bold text-green-700 dark:text-green-400 mb-2">
                  {word.english_translation}
                </h3>
                
                {/* Definition if different from translation */}
                {word.definition_english && word.definition_english !== word.english_translation && (
                  <p className="text-sm text-neutral-700 dark:text-neutral-300">
                    {word.definition_english}
                  </p>
                )}
              </div>
              
              {/* Example sentence */}
              {word.example_sentence && (
                <div className="mb-4 p-3 bg-white/50 dark:bg-neutral-800/50 rounded-lg">
                  <p className="text-sm font-medium text-neutral-800 dark:text-neutral-200 mb-1">
                    {word.example_sentence}
                  </p>
                  {word.example_sentence_translation && (
                    <p className="text-xs text-neutral-600 dark:text-neutral-400 italic">
                      {word.example_sentence_translation}
                    </p>
                  )}
                </div>
              )}
              
              {/* Memory tips */}
              {word.memory_tips && (
                <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <p className="text-xs text-blue-700 dark:text-blue-400">
                    💡 {word.memory_tips}
                  </p>
                </div>
              )}
              
              {/* Frequency info */}
              <div className="absolute bottom-4 left-4 text-xs text-neutral-500 dark:text-neutral-400">
                Frequency: {word.zipf_frequency.toFixed(1)}
              </div>
              
              {/* Flip back hint */}
              <div className="absolute bottom-4 right-4 flex items-center gap-2 text-xs text-neutral-500 dark:text-neutral-400">
                <ArrowPathIcon className="h-4 w-4" />
                <span>Click to flip back</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Action buttons (only show after revealing answer) */}
      {showAnswer && isReviewMode && (
        <div className="mt-6 grid grid-cols-3 gap-3">
          <button
            onClick={() => handleDifficulty('hard')}
            className="py-3 px-4 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 rounded-lg hover:bg-red-200 dark:hover:bg-red-900/40 transition-colors font-medium text-sm"
          >
            <XCircleIcon className="h-5 w-5 mx-auto mb-1" />
            Hard
          </button>
          <button
            onClick={() => handleDifficulty('medium')}
            className="py-3 px-4 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 rounded-lg hover:bg-yellow-200 dark:hover:bg-yellow-900/40 transition-colors font-medium text-sm"
          >
            <ArrowPathIcon className="h-5 w-5 mx-auto mb-1" />
            Medium
          </button>
          <button
            onClick={() => handleDifficulty('easy')}
            className="py-3 px-4 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-lg hover:bg-green-200 dark:hover:bg-green-900/40 transition-colors font-medium text-sm"
          >
            <CheckCircleIcon className="h-5 w-5 mx-auto mb-1" />
            Easy
          </button>
        </div>
      )}
      
      {/* Simple next button for practice mode */}
      {showAnswer && !isReviewMode && (
        <div className="mt-6">
          <button
            onClick={onNext}
            className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
          >
            Next Word →
          </button>
        </div>
      )}
    </div>
  )
}

export default LanguageVocabularyCard