import React, { useState, useEffect } from 'react'
import { 
  SpeakerWaveIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline'
import { replaceWordAndVariationsWithBlanks } from '../../utils/vocabularyHelpers'
import SkipButton from './SkipButton'

interface VocabularyCardProps {
  word: any // Full word object from database
  isWordToDefinition?: boolean
  options?: string[]
  correctAnswer?: string
  selectedAnswer?: string
  showResult?: boolean
  isCorrect?: boolean
  onAnswerSelect?: (answer: string) => void
  onNext?: () => void
  onSkip?: () => void
  className?: string
}

const VocabularyCard: React.FC<VocabularyCardProps> = ({
  word,
  isWordToDefinition = true,
  options = [],
  correctAnswer = '',
  selectedAnswer = '',
  showResult = false,
  isCorrect = false,
  onAnswerSelect,
  onNext,
  onSkip,
  className = ''
}) => {
  const [localSelectedAnswer, setLocalSelectedAnswer] = useState(selectedAnswer)

  useEffect(() => {
    setLocalSelectedAnswer(selectedAnswer)
  }, [selectedAnswer])

  const speakWord = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel()
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.8
      utterance.volume = 0.8
      utterance.pitch = 1.0
      window.speechSynthesis.speak(utterance)
    }
  }

  const handleAnswerSelect = (answer: string) => {
    if (showResult) return
    setLocalSelectedAnswer(answer)
    onAnswerSelect?.(answer)
  }

  const getDifficultyColor = (difficultyName?: string) => {
    switch(difficultyName) {
      case 'Foundation': return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
      case 'Academic': return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
      case 'Sophisticated': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
      case 'Specialized': return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
      case 'Scholarly': return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
      default: return 'bg-neutral-100 text-neutral-700 dark:bg-neutral-900/30 dark:text-neutral-400'
    }
  }

  // Auto-play audio when result is shown (if enabled)
  useEffect(() => {
    if (!showResult || !word) return
    
    const autoplayEnabled = localStorage.getItem('audioAutoplay') !== 'false'
    if (!autoplayEnabled) return
    
    // Try different word properties as fallback
    const wordText = word.word || word.term || word.answer || ''
    if (!wordText) return
    
    const timer = setTimeout(() => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel()
        const utterance = new SpeechSynthesisUtterance(wordText)
        utterance.rate = 0.8
        utterance.volume = 0.8
        utterance.pitch = 1.0
        window.speechSynthesis.speak(utterance)
      }
    }, 200) // Shorter delay for quicker audio playback
    
    return () => clearTimeout(timer)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showResult]) // Only trigger when showResult changes

  if (!word) return null

  return (
    <div className={`px-6 py-2 ${className}`}>
      {/* Skip link in top left */}
      {onSkip && !showResult && (
        <div className="flex justify-start mb-2">
          <SkipButton onSkip={onSkip} />
        </div>
      )}
      
      {!showResult ? (
        <>
          {/* Question Content */}
          <div className="space-y-2 mb-2">
            {isWordToDefinition ? (
              // Word-to-definition mode: Display the word prominently
              <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/20 rounded-lg p-3 sm:p-4 border-2 border-primary-200 dark:border-primary-700 shadow-lg">
                <div className="text-center">
                  <p className="text-3xl sm:text-4xl font-bold text-primary-700 dark:text-primary-400 mb-2">
                    {word.word}
                  </p>
                  {word.part_of_speech && (
                    <span className="text-sm text-neutral-600 dark:text-neutral-400 italic">
                      ({word.part_of_speech})
                    </span>
                  )}
                </div>
              </div>
            ) : (
              // Definition-to-word mode: Display the definition
              <>
                <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/20 rounded-lg p-3 sm:p-4 border-2 border-primary-200 dark:border-primary-700 shadow-lg">
                  <p className="text-base sm:text-lg font-medium text-neutral-800 dark:text-neutral-200 leading-snug text-center">
                    {replaceWordAndVariationsWithBlanks(word.definition, word.word)}
                  </p>
                </div>

                {word.example_sentence && (
                  <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-2 text-center border border-gold-200 dark:border-gold-800">
                    <h3 className="font-semibold text-sm mb-2 text-gold-700 dark:text-gold-400">Example</h3>
                    <p className="text-sm text-neutral-700 dark:text-neutral-300 italic">
                      "{replaceWordAndVariationsWithBlanks(word.example_sentence, word.word)}"
                    </p>
                  </div>
                )}
              </>
            )}
          </div>

          {/* Difficulty and Part of Speech */}
          <div className="text-center mb-2 space-y-1">
            <div className="flex justify-center items-center gap-2 sm:gap-3 text-xs">
              {word.vocabulary_difficulty_levels?.name && (
                <span className={`px-1 sm:px-2 py-0.5 sm:py-1 rounded text-xs font-medium ${getDifficultyColor(word.vocabulary_difficulty_levels.name)}`}>
                  {word.vocabulary_difficulty_levels.name}
                </span>
              )}
              {word.part_of_speech && !isWordToDefinition && (
                <span className="text-neutral-600 dark:text-neutral-400 italic">
                  {word.part_of_speech}
                </span>
              )}
            </div>
          </div>

          {/* Multiple Choice Options */}
          <div className="space-y-1.5 mb-2">
            <h3 className="font-semibold text-sm">
              {isWordToDefinition 
                ? "Which definition matches the word above?" 
                : "Which word matches the definition above?"}
            </h3>
            <div className={`grid gap-1.5 ${isWordToDefinition ? 'grid-cols-1' : 'grid-cols-1 sm:grid-cols-2'}`}>
              {options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleAnswerSelect(option)}
                  className={`${isWordToDefinition ? 'p-2' : 'p-1.5'} text-left border-2 rounded-lg transition-colors ${
                    localSelectedAnswer === option
                      ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20'
                      : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/10 bg-white dark:bg-neutral-800'
                  }`}
                >
                  <span className={`text-sm ${isWordToDefinition ? 'line-clamp-2' : ''}`}>
                    {isWordToDefinition 
                      ? replaceWordAndVariationsWithBlanks(option, word.word)
                      : option}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </>
      ) : (
        <>
          {/* Result Display */}
          <div className={`mb-2 p-2 rounded-lg ${
            isCorrect 
              ? 'bg-green-50 dark:bg-green-900/20' 
              : 'bg-red-50 dark:bg-red-900/20'
          }`}>
            {isCorrect ? (
              <div className="flex flex-col items-center gap-3">
                <div className="flex items-center gap-2">
                  <CheckCircleIcon className="h-5 w-5 text-green-500" />
                  <span className="text-sm font-bold text-green-700 dark:text-green-400">
                    Correct!
                  </span>
                </div>
                <div className="text-center">
                  {isWordToDefinition ? (
                    <>
                      <p className="text-2xl font-bold text-green-700 dark:text-green-400 mb-2">
                        {word.word}
                      </p>
                      <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                        {word.definition}
                      </p>
                      {word.example_sentence && (
                        <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-2 text-center border border-gold-200 dark:border-gold-800 mt-2">
                          <h3 className="font-semibold text-xs mb-1 text-gold-700 dark:text-gold-400">Example:</h3>
                          <p className="text-xs text-neutral-700 dark:text-neutral-300 italic">
                            "{replaceWordAndVariationsWithBlanks(word.example_sentence, word.word)}"
                          </p>
                        </div>
                      )}
                    </>
                  ) : (
                    <>
                      <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                        {replaceWordAndVariationsWithBlanks(word.definition, word.word)}
                      </p>
                      <span className="text-5xl font-bold text-green-700 dark:text-green-400">
                        {word.word}
                      </span>
                    </>
                  )}
                </div>
                <div className="flex items-center justify-center gap-3">
                  <button
                    onClick={() => speakWord(word.word)}
                    className="p-1 hover:bg-green-100 dark:hover:bg-green-800/20 rounded-md transition-colors"
                    title="Hear pronunciation"
                  >
                    <SpeakerWaveIcon className="h-4 w-4 text-green-600 dark:text-green-400" />
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <XCircleIcon className="h-5 w-5 text-red-500" />
                  <span className="text-sm font-bold text-red-700 dark:text-red-400">Incorrect</span>
                </div>
                <div className="text-center mb-2">
                  <p className="text-sm text-neutral-600 dark:text-neutral-400">
                    {isWordToDefinition 
                      ? `The word "${word.word}" means:`
                      : replaceWordAndVariationsWithBlanks(word.definition, word.word)}
                  </p>
                </div>
                <div className="flex flex-col items-center justify-center gap-3">
                  {isWordToDefinition ? (
                    <>
                      <div className="text-sm text-red-600 dark:text-red-400 max-w-md text-center line-clamp-2">
                        Your answer: {replaceWordAndVariationsWithBlanks(localSelectedAnswer, word.word)}
                      </div>
                      <div className="text-sm text-green-600 dark:text-green-400 max-w-md text-center">
                        <span className="font-semibold">Correct answer:</span> {replaceWordAndVariationsWithBlanks(word.definition, word.word)}
                      </div>
                      {word.example_sentence && (
                        <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-2 text-center border border-gold-200 dark:border-gold-800 mt-1 max-w-md">
                          <h3 className="font-semibold text-xs mb-1 text-gold-700 dark:text-gold-400">Example:</h3>
                          <p className="text-xs text-neutral-700 dark:text-neutral-300 italic">
                            "{replaceWordAndVariationsWithBlanks(word.example_sentence, word.word)}"
                          </p>
                        </div>
                      )}
                    </>
                  ) : (
                    <div className="flex items-center gap-3">
                      <div className="text-xl text-red-600 dark:text-red-400">{localSelectedAnswer}</div>
                      <div className="text-lg text-neutral-500">→</div>
                      <div className="text-3xl font-mono text-green-600 dark:text-green-400 font-bold">{word.word}</div>
                    </div>
                  )}
                  <button
                    onClick={() => speakWord(word.word)}
                    className="p-1 hover:bg-green-100 dark:hover:bg-green-800/20 rounded-md transition-colors"
                    title="Hear pronunciation"
                  >
                    <SpeakerWaveIcon className="h-4 w-4 text-green-600 dark:text-green-400" />
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Learning Information */}
          <div className="space-y-1.5 mb-2">
            {(word.memory_tips || word.pronunciation_tips) && (
              <div className="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-3">
                <h3 className="font-semibold text-xs mb-1 flex items-center gap-1">
                  <AcademicCapIcon className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                  Memory Tips
                </h3>
                <p className="text-xs text-neutral-700 dark:text-neutral-300">
                  {word.memory_tips || word.pronunciation_tips}
                </p>
              </div>
            )}

            {word.etymology && (
              <div className="bg-neutral-50 dark:bg-neutral-800 rounded-lg p-3">
                <h3 className="font-semibold text-xs mb-1">
                  Word Origin & Etymology
                </h3>
                <p className="text-xs text-neutral-700 dark:text-neutral-300">
                  {word.etymology}
                </p>
              </div>
            )}
          </div>

          {onNext && (
            <button
              onClick={onNext}
              className="w-full py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 active:bg-primary-900 transition-colors text-sm font-semibold shadow-md"
            >
              Next Word →
            </button>
          )}
        </>
      )}
    </div>
  )
}

export default VocabularyCard