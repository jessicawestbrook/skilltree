import React, { useState } from 'react'
import SimpleVisualMatrix from '../components/SimpleVisualMatrix'

const VisualMatrixDemoPage: React.FC = () => {
  const [currentDemo, setCurrentDemo] = useState(0)

  const demoQuestions = [
    {
      setName: 'A',
      difficulty: 'very_easy',
      patternType: 'simple_counting',
      questionNumber: 1,
      title: 'Set A - Very Easy: Counting Pattern'
    },
    {
      setName: 'B',
      difficulty: 'easy',
      patternType: 'simple_alternation',
      questionNumber: 5,
      title: 'Set B - Easy: Alternation Pattern'
    },
    {
      setName: 'C',
      difficulty: 'medium',
      patternType: 'fill_progression',
      questionNumber: 9,
      title: 'Set C - Medium: Fill Progression'
    },
    {
      setName: 'D',
      difficulty: 'hard',
      patternType: 'multiple_rule_system',
      questionNumber: 13,
      title: 'Set D - Hard: Multiple Rules'
    },
    {
      setName: 'E',
      difficulty: 'very_hard',
      patternType: 'complex_transformation',
      questionNumber: 17,
      title: 'Set E - Very Hard: Complex Transformations'
    }
  ]

  const currentQuestion = demoQuestions[currentDemo]

  const handleAnswer = (selectedOption: number) => {
    console.log(`Selected option: ${selectedOption}`)
    // Auto-advance after 3 seconds
    setTimeout(() => {
      if (currentDemo < demoQuestions.length - 1) {
        setCurrentDemo(prev => prev + 1)
      }
    }, 3000)
  }

  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-neutral-900 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-4">Visual Raven's Progressive Matrices</h1>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-6">
            Interactive demo of visual pattern recognition questions
          </p>
          
          {/* Navigation */}
          <div className="flex justify-center gap-2 mb-8">
            {demoQuestions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentDemo(index)}
                className={`px-4 py-2 rounded-lg border-2 transition-colors ${
                  currentDemo === index
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-300 hover:border-primary-300 text-gray-600'
                }`}
              >
                Set {demoQuestions[index].setName}
              </button>
            ))}
          </div>
        </div>

        {/* Current Question */}
        <div className="card">
          <div className="mb-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">{currentQuestion.title}</h2>
              <div className="text-sm text-neutral-600 dark:text-neutral-400">
                Question {currentDemo + 1} of {demoQuestions.length}
              </div>
            </div>
            
            <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2 mb-6">
              <div 
                className="bg-primary-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${((currentDemo + 1) / demoQuestions.length) * 100}%` }}
              />
            </div>
          </div>

          <SimpleVisualMatrix
            setName={currentQuestion.setName}
            difficulty={currentQuestion.difficulty}
            patternType={currentQuestion.patternType}
            questionNumber={currentQuestion.questionNumber}
            onAnswer={handleAnswer}
          />

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8">
            <button
              onClick={() => setCurrentDemo(prev => Math.max(0, prev - 1))}
              disabled={currentDemo === 0}
              className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            <button
              onClick={() => setCurrentDemo(prev => Math.min(demoQuestions.length - 1, prev + 1))}
              disabled={currentDemo === demoQuestions.length - 1}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>

        {/* Explanation */}
        <div className="mt-8 card">
          <h3 className="text-lg font-semibold mb-4">About Visual Pattern Recognition</h3>
          <div className="space-y-4 text-sm text-neutral-600 dark:text-neutral-400">
            <p>
              <strong>Real Raven's Progressive Matrices</strong> use visual patterns instead of text descriptions. 
              This demo shows how actual matrix puzzles work with progressive difficulty levels.
            </p>
            
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold text-neutral-800 dark:text-neutral-200 mb-2">Difficulty Progression:</h4>
                <ul className="space-y-1">
                  <li><strong>Set A:</strong> Simple counting, basic patterns</li>
                  <li><strong>Set B:</strong> Shape relationships, analogies</li>
                  <li><strong>Set C:</strong> Complex transformations</li>
                  <li><strong>Set D:</strong> Multiple simultaneous rules</li>
                  <li><strong>Set E:</strong> Abstract reasoning, meta-patterns</li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold text-neutral-800 dark:text-neutral-200 mb-2">Cognitive Skills Tested:</h4>
                <ul className="space-y-1">
                  <li>• Pattern completion</li>
                  <li>• Analogical reasoning</li>
                  <li>• Visual-spatial processing</li>
                  <li>• Working memory</li>
                  <li>• Abstract reasoning</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VisualMatrixDemoPage