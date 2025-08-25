import React from 'react'
import { SpeakerWaveIcon, InformationCircleIcon } from '@heroicons/react/24/outline'
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid'
import { replaceWordAndVariationsWithBlanks } from '../../utils/vocabularyHelpers'
import SkipButton from './SkipButton'

interface SpellingCardProps {
  word: string
  definition?: string
  exampleSentence?: string
  partOfSpeech?: string
  difficulty?: number
  difficultyName?: string
  userInput?: string
  showResult?: boolean
  isCorrect?: boolean
  onPlayAudio?: () => void
  onInputChange?: (value: string) => void
  onSubmit?: () => void
  onSkip?: () => void
  hideInput?: boolean
  className?: string
}

const SpellingCard: React.FC<SpellingCardProps> = ({
  word,
  definition,
  exampleSentence,
  partOfSpeech,
  difficulty,
  difficultyName,
  userInput = '',
  showResult = false,
  isCorrect = false,
  onPlayAudio,
  onInputChange,
  onSubmit,
  onSkip,
  hideInput = false,
  className = ''
}) => {
  const getDifficultyLabel = (level?: number, name?: string) => {
    if (name) return name
    if (!level) return 'Unknown'
    const labels = ['Beginner', 'Elementary', 'Intermediate', 'Advanced', 'Expert']
    return labels[Math.min(level - 1, labels.length - 1)]
  }

  const getDifficultyColor = (name?: string) => {
    switch(name || getDifficultyLabel(difficulty)) {
      case 'Beginner': return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
      case 'Elementary': return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
      case 'Intermediate': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
      case 'Advanced': return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
      case 'Expert': return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
      default: return 'bg-neutral-100 text-neutral-700 dark:bg-neutral-900/30 dark:text-neutral-400'
    }
  }

  return (
    <div className={`px-6 py-2 ${className}`}>
      {/* Skip link in top left */}
      {onSkip && !showResult && (
        <div className="flex justify-start mb-2">
          <SkipButton onSkip={onSkip} />
        </div>
      )}
      
      {!showResult && (
        <>
          {/* Audio Play Button - Prominent */}
          {onPlayAudio && (
            <div className="text-center mb-4">
              <button
                onClick={onPlayAudio}
                className="inline-flex items-center gap-3 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-lg font-medium"
                aria-label="Play word pronunciation"
              >
                <SpeakerWaveIcon className="h-6 w-6" />
                Play Word
              </button>
            </div>
          )}

          {/* Context Information */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
            {definition && (
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                <h3 className="font-semibold text-sm mb-1 flex items-center gap-1">
                  <InformationCircleIcon className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                  Definition
                </h3>
                <p className="text-sm text-neutral-700 dark:text-neutral-300">
                  {replaceWordAndVariationsWithBlanks(definition, word)}
                </p>
              </div>
            )}

            {exampleSentence && (
              <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-3">
                <h3 className="font-semibold text-sm mb-1">Example</h3>
                <p className="text-sm text-neutral-700 dark:text-neutral-300 italic">
                  "{replaceWordAndVariationsWithBlanks(exampleSentence, word)}"
                </p>
              </div>
            )}
          </div>

          {/* Difficulty and Part of Speech */}
          <div className="text-center mb-4">
            <div className="flex justify-center items-center gap-3">
              {difficultyName && (
                <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(difficultyName)}`}>
                  {difficultyName}
                </span>
              )}
              {partOfSpeech && (
                <span className="text-sm text-neutral-600 dark:text-neutral-400 italic">
                  {partOfSpeech}
                </span>
              )}
            </div>
          </div>
        </>
      )}

      {/* Input Field */}
      {!hideInput && !showResult && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Type your spelling:
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={userInput}
                onChange={(e) => onInputChange?.(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && userInput.trim() && onSubmit) {
                    onSubmit()
                  }
                }}
                className="flex-1 px-3 py-2 text-lg font-mono border-2 border-neutral-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-neutral-800"
                placeholder=""
                autoFocus
              />
              <button
                onClick={() => {
                  if (onSubmit && userInput.trim()) {
                    onSubmit()
                  }
                }}
                disabled={!userInput.trim()}
                className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-300 dark:disabled:bg-neutral-600 disabled:text-neutral-500 dark:disabled:text-neutral-400 disabled:cursor-not-allowed transition-colors font-medium"
                type="button"
              >
                Check
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Result Display */}
      {showResult && (
        <div className={`text-center p-4 rounded-lg ${
          isCorrect
            ? 'bg-green-50 dark:bg-green-900/20'
            : 'bg-red-50 dark:bg-red-900/20'
        }`}>
          <div className="flex items-center justify-center gap-2 mb-3">
            {isCorrect ? (
              <>
                <CheckCircleIcon className="h-6 w-6 text-green-500" />
                <span className="text-lg font-bold text-green-700 dark:text-green-400">
                  Correct!
                </span>
              </>
            ) : (
              <>
                <XCircleIcon className="h-6 w-6 text-red-500" />
                <span className="text-lg font-bold text-red-700 dark:text-red-400">
                  Incorrect
                </span>
              </>
            )}
          </div>
          
          <div className={`text-3xl font-bold mb-2 ${
            isCorrect ? 'text-green-700 dark:text-green-400' : 'text-neutral-700 dark:text-neutral-300'
          }`}>
            {word}
          </div>
          
          {!isCorrect && userInput && (
            <div className="text-sm text-red-600 dark:text-red-400 line-through mb-2">
              Your answer: {userInput}
            </div>
          )}
          
          {definition && (
            <div className="mt-3 text-sm text-neutral-600 dark:text-neutral-400">
              {definition}
            </div>
          )}
          
          {onPlayAudio && (
            <button
              onClick={onPlayAudio}
              className="mt-3 inline-flex items-center gap-2 px-4 py-2 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors"
            >
              <SpeakerWaveIcon className="h-5 w-5" />
              Hear pronunciation
            </button>
          )}
        </div>
      )}
    </div>
  )
}

export default SpellingCard