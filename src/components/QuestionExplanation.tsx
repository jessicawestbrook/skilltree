import React from 'react'
import { 
  ArrowTopRightOnSquareIcon,
  CheckCircleIcon,
  XCircleIcon,
  LightBulbIcon,
  AcademicCapIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

interface ExternalLink {
  url: string
  title: string
  description?: string
}

interface QuestionExplanationProps {
  explanation: string
  nodeType?: string
  externalLinks?: ExternalLink[]
  correctAnswer?: string
  incorrectAnswers?: string[]
  allOptions?: string[]
  correctAnswerIndex?: number
  selectedAnswerIndex?: number
  optionExplanations?: Record<number, string>
}

const QuestionExplanation: React.FC<QuestionExplanationProps> = ({
  explanation,
  nodeType,
  externalLinks,
  correctAnswer,
  incorrectAnswers,
  allOptions,
  correctAnswerIndex,
  selectedAnswerIndex,
  optionExplanations
}) => {
  // Determine if external links should be shown based on node type
  const shouldShowLinks = nodeType && ['humanities', 'science', 'social_science', 'history', 'geography', 'biology', 'chemistry', 'physics'].includes(nodeType.toLowerCase())


  // Enhanced explanation parser with special markers
  const parseExplanation = (text: string) => {
    if (!text) return null

    let currentText = text

    // Process special markers
    const markers = [
      { pattern: /\[CORRECT\]/g, component: (key: number) => (
        <span key={key} className="inline-flex items-center gap-1 text-green-600 dark:text-green-400 font-semibold">
          <CheckCircleIcon className="h-4 w-4" />
          Correct Answer
        </span>
      )},
      { pattern: /\[INCORRECT:(\d+)\]/g, component: (key: number, match: RegExpMatchArray) => (
        <span key={key} className="inline-flex items-center gap-1 text-red-600 dark:text-red-400 font-semibold">
          <XCircleIcon className="h-4 w-4" />
          Option {match[1]} is Incorrect
        </span>
      )},
      { pattern: /\[CONCEPT\]/g, component: (key: number) => (
        <span key={key} className="inline-flex items-center gap-1 text-primary-600 dark:text-primary-400 font-semibold">
          <AcademicCapIcon className="h-4 w-4" />
          Key Concept
        </span>
      )},
      { pattern: /\[TIP\]/g, component: (key: number) => (
        <span key={key} className="inline-flex items-center gap-1 text-amber-600 dark:text-amber-400 font-semibold">
          <LightBulbIcon className="h-4 w-4" />
          Tip
        </span>
      )},
      { pattern: /\[WARNING\]/g, component: (key: number) => (
        <span key={key} className="inline-flex items-center gap-1 text-orange-600 dark:text-orange-400 font-semibold">
          <ExclamationTriangleIcon className="h-4 w-4" />
          Common Mistake
        </span>
      )}
    ]

    // Process links (format: [text](url))
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g
    const processedParts: React.ReactNode[] = []
    let lastIndex = 0
    let match

    while ((match = linkRegex.exec(currentText)) !== null) {
      // Add text before the link
      if (match.index > lastIndex) {
        processedParts.push(currentText.substring(lastIndex, match.index))
      }
      // Add the link
      processedParts.push(
        <a
          key={`link-${match.index}`}
          href={match[2]}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 underline inline-flex items-center gap-1"
        >
          {match[1]}
          <ArrowTopRightOnSquareIcon className="h-3 w-3" />
        </a>
      )
      lastIndex = match.index + match[0].length
    }

    // Add remaining text
    if (lastIndex < currentText.length) {
      processedParts.push(currentText.substring(lastIndex))
    }

    // If no links were found, use the original text
    if (processedParts.length === 0) {
      processedParts.push(currentText)
    }

    // Now process the parts for special markers
    const finalElements: React.ReactNode[] = []
    let keyCounter = 0

    processedParts.forEach((part, partIndex) => {
      if (typeof part === 'string') {
        let processedText = part
        let lastProcessedIndex = 0
        const tempElements: React.ReactNode[] = []

        markers.forEach(({ pattern, component }) => {
          const regex = new RegExp(pattern)
          let markerMatch
          
          while ((markerMatch = regex.exec(processedText)) !== null) {
            // Add text before marker
            if (markerMatch.index > lastProcessedIndex) {
              tempElements.push(processedText.substring(lastProcessedIndex, markerMatch.index))
            }
            // Add marker component
            tempElements.push(component(keyCounter++, markerMatch))
            lastProcessedIndex = markerMatch.index + markerMatch[0].length
          }
        })

        // Add remaining text
        if (lastProcessedIndex < processedText.length) {
          tempElements.push(processedText.substring(lastProcessedIndex))
        }

        if (tempElements.length > 0) {
          finalElements.push(...tempElements)
        } else {
          finalElements.push(part)
        }
      } else {
        finalElements.push(part)
      }
    })

    return finalElements.length > 0 ? finalElements : text
  }

  return (
    <div className="bg-gold-50 dark:bg-gold-900/20 rounded-lg p-4 space-y-3">
      {/* Main Explanation */}
      <div>
        <h4 className="font-semibold text-sm mb-2 text-neutral-900 dark:text-white">
          Explanation
        </h4>
        <div className="text-sm text-neutral-700 dark:text-neutral-300 leading-relaxed">
          {parseExplanation(explanation)}
        </div>
      </div>

      {/* Correct Answer Highlight */}
      {correctAnswer && (
        <div className="border-l-4 border-green-500 pl-3 py-1">
          <p className="text-sm text-green-700 dark:text-green-400">
            <span className="font-semibold">Correct: </span>
            {correctAnswer}
          </p>
        </div>
      )}

      {/* Incorrect Answers Explanation */}
      {incorrectAnswers && incorrectAnswers.length > 0 && (
        <div className="space-y-2">
          <h5 className="font-semibold text-xs text-neutral-600 dark:text-neutral-400 uppercase tracking-wider">
            Why other options are incorrect:
          </h5>
          {incorrectAnswers.map((answer, index) => (
            <div key={index} className="border-l-4 border-red-300 dark:border-red-800 pl-3 py-1">
              <p className="text-xs text-neutral-600 dark:text-neutral-400">
                {answer}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* External Learning Resources */}
      {shouldShowLinks && externalLinks && externalLinks.length > 0 && (
        <div className="border-t border-neutral-200 dark:border-neutral-700 pt-3">
          <h5 className="font-semibold text-xs text-neutral-600 dark:text-neutral-400 uppercase tracking-wider mb-2">
            Learn More
          </h5>
          <div className="space-y-2">
            {externalLinks.map((link, index) => (
              <a
                key={index}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block p-2 rounded-lg bg-white dark:bg-neutral-800 hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors group"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-primary-600 dark:text-primary-400 group-hover:text-primary-700 dark:group-hover:text-primary-300">
                      {link.title}
                    </p>
                    {link.description && (
                      <p className="text-xs text-neutral-600 dark:text-neutral-400 mt-0.5">
                        {link.description}
                      </p>
                    )}
                  </div>
                  <ArrowTopRightOnSquareIcon className="h-4 w-4 text-neutral-400 ml-2 flex-shrink-0" />
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Auto-generated links for certain subjects */}
      {shouldShowLinks && !externalLinks && (
        <div className="border-t border-neutral-200 dark:border-neutral-700 pt-3">
          <p className="text-xs text-neutral-500 italic">
            💡 Tip: Search for more information about this topic on educational websites like Khan Academy, Wikipedia, or Britannica.
          </p>
        </div>
      )}
    </div>
  )
}

export default QuestionExplanation