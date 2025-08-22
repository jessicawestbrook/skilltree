import React, { useState, useEffect } from 'react'

interface SimpleMatrixProps {
  patternType: string
  difficulty: string
  setName: string
  questionNumber: number
  onAnswer?: (selectedOption: number) => void
}

const SimpleVisualMatrix: React.FC<SimpleMatrixProps> = ({
  patternType,
  difficulty,
  setName,
  questionNumber,
  onAnswer
}) => {
  const [selectedOption, setSelectedOption] = useState<number | null>(null)

  // Reset selected option when question changes
  useEffect(() => {
    setSelectedOption(null)
  }, [patternType, difficulty, setName, questionNumber])

  // Generate simple visual patterns based on difficulty
  const generatePattern = () => {
    switch (difficulty) {
      case 'very_easy':
        return generateVeryEasyPattern()
      case 'easy':
        return generateEasyPattern()
      case 'medium':
        return generateMediumPattern()
      case 'hard':
        return generateHardPattern()
      case 'very_hard':
        return generateVeryHardPattern()
      default:
        return generateVeryEasyPattern()
    }
  }

  // Very Easy: Simple counting patterns
  const generateVeryEasyPattern = () => {
    const correctAnswer = 0
    
    return {
      matrix: (
        <div className="grid grid-cols-3 gap-4 p-8 border-2 border-gray-600 bg-white max-w-2xl mx-auto">
          {/* Row 1 */}
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="w-8 h-8 bg-black rounded-full"></div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="flex gap-3 items-center">
              <div className="w-8 h-8 bg-black rounded-full"></div>
              <div className="w-8 h-8 bg-black rounded-full"></div>
            </div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="flex gap-2 items-center">
              <div className="w-8 h-8 bg-black rounded-full"></div>
              <div className="w-8 h-8 bg-black rounded-full"></div>
              <div className="w-8 h-8 bg-black rounded-full"></div>
            </div>
          </div>
          
          {/* Row 2 */}
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="grid grid-cols-2 gap-3 items-center justify-items-center">
              <div className="w-8 h-8 bg-black rounded-full"></div>
              <div className="w-8 h-8 bg-black rounded-full"></div>
              <div className="w-8 h-8 bg-black rounded-full"></div>
              <div className="w-8 h-8 bg-black rounded-full"></div>
            </div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="grid grid-cols-3 gap-2 items-center justify-items-center">
              {Array.from({length: 5}).map((_, i) => (
                <div key={i} className="w-6 h-6 bg-black rounded-full"></div>
              ))}
            </div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-gray-100">
            <span className="text-6xl text-gray-500 font-bold">?</span>
          </div>
        </div>
      ),
      options: [
        // Option A: 6 dots (correct)
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="grid grid-cols-3 gap-2 items-center justify-items-center">
            {Array.from({length: 6}).map((_, i) => (
              <div key={i} className="w-4 h-4 bg-black rounded-full"></div>
            ))}
          </div>
        </div>,
        // Option B: 5 dots
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="grid grid-cols-3 gap-2 items-center justify-items-center">
            {Array.from({length: 5}).map((_, i) => (
              <div key={i} className="w-4 h-4 bg-black rounded-full"></div>
            ))}
          </div>
        </div>,
        // Option C: 4 dots
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="grid grid-cols-2 gap-2 items-center justify-items-center">
            {Array.from({length: 4}).map((_, i) => (
              <div key={i} className="w-4 h-4 bg-black rounded-full"></div>
            ))}
          </div>
        </div>,
        // Option D: 7 dots
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="grid grid-cols-3 gap-2 items-center justify-items-center">
            {Array.from({length: 7}).map((_, i) => (
              <div key={i} className="w-4 h-4 bg-black rounded-full"></div>
            ))}
          </div>
        </div>
      ],
      correctAnswer,
      explanation: "The pattern increases by 1 each step: 1, 2, 3, 4, 5, so the missing piece should have 6 dots."
    }
  }

  // Easy: Shape alternation
  const generateEasyPattern = () => {
    const correctAnswer = 0
    
    return {
      matrix: (
        <div className="grid grid-cols-2 gap-4 p-8 border-2 border-gray-600 bg-white max-w-xl mx-auto">
          {/* Row 1 */}
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="w-16 h-16 bg-black rounded-full"></div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="w-16 h-16 border-4 border-black rounded-full bg-white"></div>
          </div>
          
          {/* Row 2 */}
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="w-16 h-16 border-4 border-black rounded-full bg-white"></div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-gray-100">
            <span className="text-6xl text-gray-500 font-bold">?</span>
          </div>
        </div>
      ),
      options: [
        // Option A: Filled circle (correct)
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="w-12 h-12 bg-black rounded-full"></div>
        </div>,
        // Option B: Empty circle
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="w-12 h-12 border-4 border-black rounded-full bg-white"></div>
        </div>,
        // Option C: Filled square
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="w-12 h-12 bg-black"></div>
        </div>,
        // Option D: Empty square
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="w-12 h-12 border-4 border-black bg-white"></div>
        </div>
      ],
      correctAnswer,
      explanation: "The pattern alternates between filled and empty shapes. Following the diagonal pattern: filled→empty→empty→filled."
    }
  }

  // Medium: Shape transformation
  const generateMediumPattern = () => {
    const correctAnswer = 2
    
    return {
      matrix: (
        <div className="grid grid-cols-3 gap-4 p-8 border-2 border-gray-600 bg-white max-w-2xl mx-auto">
          {/* Row 1 */}
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="w-16 h-16 bg-black rounded-full"></div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="w-16 h-16 bg-gray-400 rounded-full"></div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="w-16 h-16 border-4 border-black rounded-full bg-white"></div>
          </div>
          
          {/* Row 2 */}
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="w-16 h-16 bg-black transform rotate-45"></div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="w-16 h-16 bg-gray-400 transform rotate-45"></div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-gray-100">
            <span className="text-6xl text-gray-500 font-bold">?</span>
          </div>
        </div>
      ),
      options: [
        // Option A: Black square
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="w-12 h-12 bg-black transform rotate-45"></div>
        </div>,
        // Option B: Gray square
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="w-12 h-12 bg-gray-400 transform rotate-45"></div>
        </div>,
        // Option C: Empty square (correct)
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="w-12 h-12 border-4 border-black bg-white transform rotate-45"></div>
        </div>,
        // Option D: Circle
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="w-12 h-12 border-4 border-black rounded-full bg-white"></div>
        </div>
      ],
      correctAnswer,
      explanation: "Each row shows the same transformation pattern: black→gray→empty. Row 2 follows the same pattern but with squares instead of circles."
    }
  }

  // Hard: Multiple rules
  const generateHardPattern = () => {
    const correctAnswer = 1
    
    return {
      matrix: (
        <div className="grid grid-cols-3 gap-4 p-8 border-2 border-gray-600 bg-white max-w-2xl mx-auto">
          {/* Row 1 */}
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-black rounded-full"></div>
              <div className="w-6 h-6 bg-gray-300"></div>
            </div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-black transform rotate-45"></div>
              <div className="w-6 h-6 bg-gray-300 rounded-full"></div>
            </div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="flex items-center gap-2">
              <div className="w-0 h-0 border-l-5 border-r-5 border-b-10 border-l-transparent border-r-transparent border-b-black"></div>
              <div className="w-6 h-6 bg-gray-300 transform rotate-45"></div>
            </div>
          </div>
          
          {/* Row 2 */}
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 border-3 border-black rounded-full bg-white"></div>
              <div className="w-6 h-6 bg-black"></div>
            </div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 border-3 border-black bg-white transform rotate-45"></div>
              <div className="w-6 h-6 bg-black rounded-full"></div>
            </div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-gray-100">
            <span className="text-6xl text-gray-500 font-bold">?</span>
          </div>
        </div>
      ),
      options: [
        // Option A: Wrong combination
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="flex items-center gap-1">
            <div className="w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-transparent border-r-transparent border-b-black"></div>
            <div className="w-4 h-4 bg-gray-300"></div>
          </div>
        </div>,
        // Option B: Correct - empty triangle with black square
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="flex items-center gap-1">
            <div className="w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-black border-r-black border-b-transparent"></div>
            <div className="w-4 h-4 bg-black transform rotate-45"></div>
          </div>
        </div>,
        // Option C: Wrong shape
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="flex items-center gap-1">
            <div className="w-8 h-8 border-3 border-black rounded-full bg-white"></div>
            <div className="w-4 h-4 bg-black transform rotate-45"></div>
          </div>
        </div>,
        // Option D: Wrong inner shape
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="flex items-center gap-1">
            <div className="w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-black border-r-black border-b-transparent"></div>
            <div className="w-4 h-4 bg-black rounded-full"></div>
          </div>
        </div>
      ],
      correctAnswer,
      explanation: "Two rules apply: 1) Outer shapes cycle (circle→square→triangle), 2) Fill inverts between rows (filled→empty), 3) Inner shapes cycle and invert fill."
    }
  }

  // Very Hard: Complex transformations
  const generateVeryHardPattern = () => {
    const correctAnswer = 3
    
    return {
      matrix: (
        <div className="grid grid-cols-3 gap-4 p-8 border-2 border-gray-600 bg-white max-w-2xl mx-auto">
          {/* Complex overlapping patterns */}
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="relative">
              <div className="w-12 h-12 bg-black rounded-full"></div>
              <div className="w-6 h-6 border-2 border-black bg-white transform rotate-45 absolute -top-1 -right-1"></div>
              <div className="w-3 h-3 bg-gray-400 absolute bottom-1 left-1"></div>
            </div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-white">
            <div className="relative">
              <div className="w-12 h-12 bg-black transform rotate-45"></div>
              <div className="w-6 h-6 border-2 border-black bg-white rounded-full absolute -top-1 -right-1"></div>
              <div className="w-3 h-3 bg-gray-400 rounded-full absolute bottom-1 left-1"></div>
            </div>
          </div>
          <div className="w-36 h-36 border border-gray-400 flex items-center justify-center bg-gray-100">
            <span className="text-6xl text-gray-500 font-bold">?</span>
          </div>
        </div>
      ),
      options: [
        // Option A
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="relative">
            <div className="w-0 h-0 border-l-6 border-r-6 border-b-12 border-l-transparent border-r-transparent border-b-black"></div>
            <div className="w-5 h-5 border-2 border-black bg-white rounded-full absolute -top-1 -right-1"></div>
          </div>
        </div>,
        // Option B
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="relative">
            <div className="w-0 h-0 border-l-6 border-r-6 border-b-12 border-l-transparent border-r-transparent border-b-black"></div>
            <div className="w-5 h-5 border-2 border-black bg-white transform rotate-45 absolute -top-1 -right-1"></div>
          </div>
        </div>,
        // Option C
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="relative">
            <div className="w-10 h-10 bg-black rounded-full"></div>
            <div className="w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-black border-r-black border-b-transparent absolute -top-1 -right-1"></div>
          </div>
        </div>,
        // Option D (correct)
        <div className="w-28 h-28 border border-gray-400 flex items-center justify-center bg-white">
          <div className="relative">
            <div className="w-0 h-0 border-l-6 border-r-6 border-b-12 border-l-transparent border-r-transparent border-b-black"></div>
            <div className="w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-black border-r-black border-b-transparent absolute -top-1 -right-1"></div>
            <div className="w-3 h-3 bg-gray-400 transform rotate-45 absolute bottom-0 left-0"></div>
          </div>
        </div>
      ],
      correctAnswer,
      explanation: "Complex pattern: Main shape cycles (circle→square→triangle), overlay shape cycles inversely, small accent follows both rules with position rotation."
    }
  }

  const { matrix, options, correctAnswer, explanation } = generatePattern()

  const handleOptionClick = (index: number) => {
    setSelectedOption(index)
    if (onAnswer) {
      onAnswer(index)
    }
  }

  return (
    <div className="space-y-6">
      {/* Matrix Display */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">Complete the visual pattern:</h3>
        <div className="flex justify-center">
          {matrix}
        </div>
      </div>

      {/* Options Display */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">Choose the missing piece:</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {options.map((option, index) => (
            <button
              key={index}
              className={`p-3 border-2 transition-colors ${
                selectedOption === index
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-300 hover:border-primary-400 hover:bg-primary-25'
              }`}
              onClick={() => handleOptionClick(index)}
            >
              <div className="flex justify-center">
                {option}
              </div>
              <div className="text-sm mt-2 text-center font-medium">
                {String.fromCharCode(65 + index)}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Show result if answer selected */}
      {selectedOption !== null && (
        <div className={`p-4 rounded-lg border ${
          selectedOption === correctAnswer
            ? 'bg-green-50 border-green-200 text-green-800'
            : 'bg-red-50 border-red-200 text-red-800'
        }`}>
          <p className="font-semibold mb-2">
            {selectedOption === correctAnswer ? '✓ Correct!' : '✗ Incorrect'}
          </p>
          <p className="text-sm">{explanation}</p>
        </div>
      )}

    </div>
  )
}

export default SimpleVisualMatrix