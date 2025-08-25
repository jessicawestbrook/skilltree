import React from 'react'
import { SpeakerWaveIcon, LanguageIcon } from '@heroicons/react/24/outline'
import SkipButton from './SkipButton'

interface LanguageCardProps {
  language: string
  questionText: string
  questionType?: string
  options?: string[]
  selectedOption?: number | null
  correctAnswer?: string
  showResult?: boolean
  explanation?: string
  difficulty?: number
  onSelectOption?: (index: number) => void
  onPlayAudio?: () => void
  onSkip?: () => void
  className?: string
}

const LanguageCard: React.FC<LanguageCardProps> = ({
  language,
  questionText,
  questionType,
  options = [],
  selectedOption = null,
  correctAnswer,
  showResult = false,
  explanation,
  difficulty,
  onSelectOption,
  onPlayAudio,
  onSkip,
  className = ''
}) => {
  const getDifficultyLabel = (level?: number) => {
    if (!level) return 'Unknown'
    const labels = ['Beginner', 'Elementary', 'Intermediate', 'Advanced', 'Expert']
    return labels[Math.min(level - 1, labels.length - 1)]
  }

  const getDifficultyColor = (level?: number) => {
    if (!level) return 'text-neutral-500'
    const colors = [
      'text-green-600 dark:text-green-400',
      'text-blue-600 dark:text-blue-400',
      'text-yellow-600 dark:text-yellow-400',
      'text-orange-600 dark:text-orange-400',
      'text-red-600 dark:text-red-400'
    ]
    return colors[Math.min(level - 1, colors.length - 1)]
  }

  const getOptionStyle = (option: string, index: number) => {
    if (!showResult) {
      return selectedOption === index
        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400 dark:hover:border-primary-500'
    }

    const isCorrect = option === correctAnswer
    const isSelected = selectedOption === index

    if (isCorrect) {
      return 'border-green-500 bg-green-50 dark:bg-green-900/20'
    }
    if (isSelected && !isCorrect) {
      return 'border-red-500 bg-red-50 dark:bg-red-900/20'
    }
    return 'border-neutral-300 dark:border-neutral-600 opacity-50'
  }

  // Detect if question contains foreign language text for audio
  const hasForeignText = questionText && !questionText.match(/^[A-Za-z\s.,!?'"]+$/)

  return (
    <div className={`px-6 py-2 ${className}`}>
      {/* Skip link in top left */}
      {onSkip && !showResult && (
        <div className="flex justify-start mb-2">
          <SkipButton onSkip={onSkip} />
        </div>
      )}
      
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center gap-3">
          <LanguageIcon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
          <span className="text-sm font-medium text-primary-600 dark:text-primary-400">
            {language.charAt(0).toUpperCase() + language.slice(1)}
          </span>
          {difficulty && (
            <span className={`text-sm ${getDifficultyColor(difficulty)}`}>
              • {getDifficultyLabel(difficulty)}
            </span>
          )}
          {questionType && (
            <span className="text-sm text-neutral-600 dark:text-neutral-400">
              • {questionType}
            </span>
          )}
        </div>
        {onPlayAudio && hasForeignText && (
          <button
            onClick={onPlayAudio}
            className="p-2 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors"
            aria-label="Play pronunciation"
          >
            <SpeakerWaveIcon className="h-6 w-6" />
          </button>
        )}
      </div>

      {/* Question */}
      <div className="mb-6">
        <h3 className="text-lg font-medium text-neutral-900 dark:text-white">
          {questionText}
        </h3>
      </div>

      {/* Options */}
      {options.length > 0 && (
        <div className="space-y-3">
          {options.map((option, index) => (
            <button
              key={index}
              onClick={() => !showResult && onSelectOption?.(index)}
              disabled={showResult}
              className={`w-full text-left px-4 py-3 border-2 rounded-lg transition-all ${getOptionStyle(
                option,
                index
              )} ${!showResult ? 'cursor-pointer' : 'cursor-default'}`}
            >
              <div className="flex items-center justify-between">
                <span className="text-neutral-900 dark:text-white">{option}</span>
                {showResult && option === correctAnswer && (
                  <span className="text-xs text-green-600 dark:text-green-400 font-medium">
                    Correct
                  </span>
                )}
                {showResult && selectedOption === index && option !== correctAnswer && (
                  <span className="text-xs text-red-600 dark:text-red-400 font-medium">
                    Your answer
                  </span>
                )}
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Explanation */}
      {showResult && explanation && (
        <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
          <p className="text-sm text-blue-800 dark:text-blue-200">
            <span className="font-medium">Explanation:</span> {explanation}
          </p>
        </div>
      )}
    </div>
  )
}

export default LanguageCard