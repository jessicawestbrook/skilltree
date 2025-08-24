import React from 'react'
import { SpeakerWaveIcon } from '@heroicons/react/24/outline'
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid'

interface SpellingBeeCardProps {
  word: string
  definition?: string
  partOfSpeech?: string
  difficulty?: number
  userInput?: string
  showResult?: boolean
  isCorrect?: boolean
  onPlayAudio?: () => void
  onInputChange?: (value: string) => void
  hideInput?: boolean
  className?: string
}

const SpellingBeeCard: React.FC<SpellingBeeCardProps> = ({
  word,
  definition,
  partOfSpeech,
  difficulty,
  userInput = '',
  showResult = false,
  isCorrect = false,
  onPlayAudio,
  onInputChange,
  hideInput = false,
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

  return (
    <div className={`bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 ${className}`}>
      {/* Header with difficulty */}
      <div className="flex justify-between items-center mb-4">
        <span className={`text-sm font-medium ${getDifficultyColor(difficulty)}`}>
          {getDifficultyLabel(difficulty)} Level
        </span>
        {onPlayAudio && (
          <button
            onClick={onPlayAudio}
            className="p-2 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors"
            aria-label="Play word pronunciation"
          >
            <SpeakerWaveIcon className="h-6 w-6" />
          </button>
        )}
      </div>

      {/* Definition and Part of Speech */}
      {(definition || partOfSpeech) && (
        <div className="mb-6 p-4 bg-neutral-50 dark:bg-neutral-700/50 rounded-lg">
          {partOfSpeech && (
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-1">
              <span className="font-medium">Part of Speech:</span> {partOfSpeech}
            </p>
          )}
          {definition && (
            <p className="text-neutral-700 dark:text-neutral-300">
              <span className="font-medium">Definition:</span> {definition}
            </p>
          )}
        </div>
      )}

      {/* Input Field or Result */}
      {!hideInput && (
        <div className="space-y-4">
          <div className="relative">
            <input
              type="text"
              value={userInput}
              onChange={(e) => onInputChange?.(e.target.value)}
              placeholder="Type the word you hear..."
              disabled={showResult}
              className={`w-full px-4 py-3 text-lg border-2 rounded-lg transition-colors ${
                showResult
                  ? isCorrect
                    ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                    : 'border-red-500 bg-red-50 dark:bg-red-900/20'
                  : 'border-neutral-300 dark:border-neutral-600 bg-white dark:bg-neutral-700'
              } text-neutral-900 dark:text-white`}
            />
            {showResult && (
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                {isCorrect ? (
                  <CheckCircleIcon className="h-6 w-6 text-green-500" />
                ) : (
                  <XCircleIcon className="h-6 w-6 text-red-500" />
                )}
              </div>
            )}
          </div>

          {/* Show correct answer if wrong */}
          {showResult && !isCorrect && (
            <div className="p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
              <p className="text-sm text-blue-800 dark:text-blue-200">
                Correct spelling: <span className="font-bold">{word}</span>
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default SpellingBeeCard