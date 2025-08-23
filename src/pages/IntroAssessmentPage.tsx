import React, { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import {
  ChartBarIcon,
  CheckCircleIcon,
  ClockIcon,
  SparklesIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline'

interface InterestQuestion {
  id: string
  category: string
  question: string
  options: string[]
  type: 'single' | 'multiple' | 'scale'
  weights: { [key: string]: number }
}

// Removed unused InterestScore interface

// Removed unused InterestResult interface

const IntroAssessmentPage: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [questions, setQuestions] = useState<InterestQuestion[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | number[] | null>(null)
  const [userAnswers, setUserAnswers] = useState<Array<{ questionId: string, selectedAnswer: number | number[], category: string }>>([])
  // Remove unused state variable
  // const [interestResult, setInterestResult] = useState<InterestResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [startTime] = useState(new Date())
  const [phase, setPhase] = useState<'intro' | 'assessment' | 'login_required' | 'redirect_to_user'>('intro')

  const generateInterestQuestions = useCallback((): InterestQuestion[] => {
    return [
      {
        id: '1',
        category: 'general',
        question: 'What is your primary learning goal?',
        options: [
          'Homeschool curriculum support',
          'Supplement traditional education',
          'Personal skill development',
          'Career advancement',
          'Test preparation (SAT, ACT, etc.)',
          'Lifelong learning and curiosity'
        ],
        type: 'single',
        weights: {}
      },
      {
        id: '2',
        category: 'general',
        question: 'What age group best describes you?',
        options: [
          'Elementary (6-10 years)',
          'Middle School (11-13 years)',
          'High School (14-18 years)',
          'College/University (18-25 years)',
          'Adult Learner (25+ years)'
        ],
        type: 'single',
        weights: {}
      },
      {
        id: '3',
        category: 'Mathematics',
        question: 'How interested are you in mathematics and problem-solving?',
        options: [
          'Very interested - I love working with numbers and solving complex problems',
          'Somewhat interested - Math is useful and I enjoy some topics',
          'Neutral - I see math as necessary but not exciting',
          'Not very interested - I find math challenging or boring',
          'Not interested at all - I avoid math whenever possible'
        ],
        type: 'scale',
        weights: { Mathematics: 5 }
      },
      {
        id: '4',
        category: 'Science',
        question: 'Which science topics interest you most? (Select all that apply)',
        options: [
          'Biology and Life Sciences',
          'Chemistry and Chemical Reactions',
          'Physics and How Things Work',
          'Earth Sciences and Environment',
          'Space and Astronomy',
          'Medicine and Human Body',
          'None of these interest me'
        ],
        type: 'multiple',
        weights: { Science: 3 }
      },
      {
        id: '5',
        category: 'Language Arts',
        question: 'How do you feel about reading, writing, and language skills?',
        options: [
          'I love reading, writing, and exploring language',
          'I enjoy most language activities and reading',
          'I see language skills as important but not my favorite',
          'I find reading and writing somewhat difficult',
          'I prefer other subjects over language arts'
        ],
        type: 'scale',
        weights: { 'Language Arts': 5 }
      },
      {
        id: '6',
        category: 'History',
        question: 'What aspects of history and social studies appeal to you?',
        options: [
          'Learning about past civilizations and cultures',
          'Understanding how historical events shaped today',
          'Studying government and political systems',
          'Exploring geography and world cultures',
          'I find history interesting but not a top priority',
          'History is not particularly interesting to me'
        ],
        type: 'multiple',
        weights: { History: 3 }
      },
      {
        id: '7',
        category: 'Technology',
        question: 'How interested are you in technology and computer skills?',
        options: [
          'Very interested - I love learning about computers and programming',
          'Interested - Technology is important for the future',
          'Somewhat interested - I use technology but don\'t study it deeply',
          'Not very interested - I use basic technology but prefer other subjects',
          'Not interested - I avoid technical topics when possible'
        ],
        type: 'scale',
        weights: { Technology: 5 }
      },
      {
        id: '8',
        category: 'Arts',
        question: 'Which creative and artistic areas interest you?',
        options: [
          'Visual Arts (Drawing, Painting, Design)',
          'Music and Sound',
          'Creative Writing and Storytelling',
          'Theater and Performance',
          'Digital Art and Media',
          'I appreciate art but don\'t create it',
          'Arts are not a priority for me'
        ],
        type: 'multiple',
        weights: { Arts: 3 }
      },
      {
        id: '9',
        category: 'Languages',
        question: 'How interested are you in learning foreign languages?',
        options: [
          'Very interested - I love learning new languages',
          'Interested - Languages open doors to new cultures',
          'Somewhat interested - Might be useful for travel or career',
          'Not very interested - English is enough for me',
          'Not interested - I find languages difficult to learn'
        ],
        type: 'scale',
        weights: { Languages: 5 }
      },
      {
        id: '10',
        category: 'Life Skills',
        question: 'Which practical life skills would you like to develop?',
        options: [
          'Personal Finance and Money Management',
          'Health and Nutrition',
          'Communication and Social Skills',
          'Critical Thinking and Problem Solving',
          'Time Management and Organization',
          'Career Planning and Professional Skills',
          'I\'m satisfied with my current life skills'
        ],
        type: 'multiple',
        weights: { 'Life Skills': 3 }
      }
    ]
  }, [])

  useEffect(() => {
    const loadedQuestions = generateInterestQuestions()
    setQuestions(loadedQuestions)
    setLoading(false)
  }, [generateInterestQuestions])

  const handleStartAssessment = () => {
    setPhase('assessment')
    if (user) {
      // Log interest assessment start
      supabase.from('assessment_attempts').insert({
        user_id: user.id,
        type: 'interests',
        started_at: startTime
      })
    }
  }

  const handleAnswerSelect = (index: number | number[]) => {
    setSelectedAnswer(index)
  }

  const handleMultipleSelect = (index: number) => {
    const currentAnswers = Array.isArray(selectedAnswer) ? selectedAnswer : []
    if (currentAnswers.includes(index)) {
      setSelectedAnswer(currentAnswers.filter(i => i !== index))
    } else {
      setSelectedAnswer([...currentAnswers, index])
    }
  }

  const handleSubmitAnswer = () => {
    if (selectedAnswer === null || (Array.isArray(selectedAnswer) && selectedAnswer.length === 0)) return

    const currentQuestion = questions[currentQuestionIndex]

    setUserAnswers([...userAnswers, {
      questionId: currentQuestion.id,
      selectedAnswer: selectedAnswer,
      category: currentQuestion.category
    }])

    // Save answer if user is logged in
    if (user) {
      supabase.from('interest_responses').insert({
        user_id: user.id,
        question_id: currentQuestion.id,
        selected_answer: selectedAnswer,
        category: currentQuestion.category,
        created_at: new Date()
      })
    }

    // Move to next question immediately for interest assessment
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setSelectedAnswer(null)
    } else {
      calculateResults()
    }
  }

  // Removed handleNextQuestion as it's handled in handleSubmitAnswer now

  const calculateResults = async () => {
    // Check if user is logged in before proceeding
    if (!user) {
      // Show login prompt instead of results
      setPhase('login_required')
      return
    }

    const interestMap = new Map<string, number>()
    let learningGoal = ''
    let ageGroup = ''
    
    // Process answers and calculate interest scores
    questions.forEach((question, index) => {
      const answer = userAnswers[index]
      if (!answer) return

      // Handle demographic questions
      if (question.id === '1' && typeof answer.selectedAnswer === 'number') {
        learningGoal = question.options[answer.selectedAnswer]
      }
      if (question.id === '2' && typeof answer.selectedAnswer === 'number') {
        ageGroup = question.options[answer.selectedAnswer]
      }

      // Calculate interest scores based on question type (normalize to 1-10 scale)
      if (question.type === 'scale' && typeof answer.selectedAnswer === 'number') {
        const scaleValue = 5 - answer.selectedAnswer // Reverse scale (0=highest interest)
        const normalizedValue = Math.max(1, Math.min(10, scaleValue * 2)) // Convert to 1-10 scale
        Object.entries(question.weights).forEach(([category]) => {
          interestMap.set(category, normalizedValue)
        })
      } else if (question.type === 'multiple' && Array.isArray(answer.selectedAnswer)) {
        Object.entries(question.weights).forEach(([category]) => {
          const answerArray = answer.selectedAnswer as number[]
          const selections = answerArray.length
          // Convert selections to 1-10 scale based on number of options selected
          const maxSelections = question.options.length - 1 // Exclude "None" option usually
          const normalizedValue = selections > 0 
            ? Math.max(1, Math.min(10, Math.round((selections / maxSelections) * 10)))
            : 1
          interestMap.set(category, normalizedValue)
        })
      }
    })

    // Save numeric interest levels to database
    const interestLevels: { [key: string]: number } = {}
    interestMap.forEach((value, key) => {
      interestLevels[key] = value
    })

    // Save to database
    // Use row-based approach for flexibility as categories may change over time
    const interestRecords = Object.entries(interestLevels).map(([category, level]) => ({
      user_id: user.id,
      category: category,
      interest_level: level,
      updated_at: new Date()
    }))

    // Delete existing interest levels for this user first
    await supabase
      .from('user_interest_levels')
      .delete()
      .eq('user_id', user.id)

    // Insert new interest levels
    if (interestRecords.length > 0) {
      await supabase.from('user_interest_levels').insert(interestRecords)
    }

    // Save user profile data separately
    await supabase.from('user_profiles').upsert({
      user_id: user.id,
      learning_goal: learningGoal,
      age_group: ageGroup,
      updated_at: new Date()
    }, { onConflict: 'user_id' })

    // Set phase to redirect to user page
    setPhase('redirect_to_user')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (phase === 'intro') {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
              <SparklesIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
            </div>
            <h1 className="text-4xl font-bold mb-4">
              <span className="text-primary-600 dark:text-primary-400">
                Learning Interests Survey
              </span>
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Tell us about your interests to get personalized learning recommendations
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-full mb-3">
                <ClockIcon className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="font-semibold mb-1">10-15 Minutes</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Quick survey about your learning interests
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-full mb-3">
                <ChartBarIcon className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="font-semibold mb-1">Interest-Based</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Questions about what you enjoy learning
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-full mb-3">
                <LightBulbIcon className="h-6 w-6 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="font-semibold mb-1">Personalized Path</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Get custom learning recommendations
              </p>
            </div>
          </div>

          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
              What to Expect:
            </h3>
            <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-400">
              <li className="flex items-start gap-2">
                <span className="text-blue-600 dark:text-blue-500 mt-0.5">•</span>
                <span>Questions about your interests in Mathematics, Science, Language Arts, History, Technology, Arts, and more</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 dark:text-blue-500 mt-0.5">•</span>
                <span>No right or wrong answers - we want to know what genuinely interests you</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 dark:text-blue-500 mt-0.5">•</span>
                <span>Help us understand your learning goals and preferences</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 dark:text-blue-500 mt-0.5">•</span>
                <span>Get a personalized learning path based on your interests</span>
              </li>
            </ul>
          </div>

          <button
            onClick={handleStartAssessment}
            className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
          >
            Start Interest Survey
          </button>
        </div>
      </div>
    )
  }

  if (phase === 'login_required') {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <LightBulbIcon className="h-16 w-16 text-primary-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold mb-4">Survey Complete!</h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-6">
              Please log in to see your personalized learning recommendations
            </p>
          </div>
          
          <div className="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-6 mb-6">
            <h3 className="font-semibold text-primary-900 dark:text-primary-300 mb-3">
              What happens after you log in:
            </h3>
            <ul className="space-y-2 text-sm text-primary-800 dark:text-primary-400">
              <li className="flex items-start gap-2">
                <span className="text-primary-600 dark:text-primary-500 mt-0.5">•</span>
                <span>View your personalized interest profile</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary-600 dark:text-primary-500 mt-0.5">•</span>
                <span>Get course recommendations based on your interests</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary-600 dark:text-primary-500 mt-0.5">•</span>
                <span>Update your interests anytime from your user page</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary-600 dark:text-primary-500 mt-0.5">•</span>
                <span>Track your learning progress across subjects</span>
              </li>
            </ul>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={() => navigate('/auth/login', { 
                state: { redirectTo: '/user/profile', message: 'Complete your interest survey setup!' } 
              })}
              className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
            >
              Log In to See Results
            </button>
            <button
              onClick={() => navigate('/auth/signup', { 
                state: { redirectTo: '/user/profile', message: 'Complete your interest survey setup!' } 
              })}
              className="flex-1 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
            >
              Sign Up
            </button>
          </div>
          
          <button
            onClick={() => navigate('/')}
            className="w-full mt-3 py-2 text-neutral-600 dark:text-neutral-400 hover:text-neutral-800 dark:hover:text-neutral-200 transition-colors"
          >
            Return to Home
          </button>
        </div>
      </div>
    )
  }

  if (phase === 'redirect_to_user') {
    // Redirect to user page
    navigate('/user/profile', { 
      state: { message: 'Your interest profile has been updated! Here are your personalized recommendations.' } 
    })
    return null
  }

  // Results phase is no longer used - survey redirects to user page after completion

  // Interest Survey Phase
  const currentQuestion = questions[currentQuestionIndex]
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100

  const renderQuestionOptions = () => {
    if (currentQuestion.type === 'multiple') {
      return (
        <div className="space-y-3 mb-6">
          <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
            Select all that apply:
          </p>
          {currentQuestion.options.map((option, index) => {
            const isSelected = Array.isArray(selectedAnswer) && selectedAnswer.includes(index)
            return (
              <button
                key={index}
                onClick={() => handleMultipleSelect(index)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                  isSelected
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                    : 'border-neutral-200 dark:border-neutral-700 hover:border-neutral-400'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
                    isSelected 
                      ? 'border-primary-500 bg-primary-500' 
                      : 'border-neutral-300 dark:border-neutral-600'
                  }`}>
                    {isSelected && (
                      <CheckCircleIcon className="h-3 w-3 text-white" />
                    )}
                  </div>
                  <span>{option}</span>
                </div>
              </button>
            )
          })}
        </div>
      )
    }

    return (
      <div className="space-y-3 mb-6">
        {currentQuestion.options.map((option, index) => (
          <button
            key={index}
            onClick={() => handleAnswerSelect(index)}
            className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
              selectedAnswer === index
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-neutral-200 dark:border-neutral-700 hover:border-neutral-400'
            }`}
          >
            <div className="flex items-center gap-3">
              <div className={`w-4 h-4 rounded-full border-2 ${
                selectedAnswer === index 
                  ? 'border-primary-500 bg-primary-500' 
                  : 'border-neutral-300 dark:border-neutral-600'
              }`} />
              <span>{option}</span>
            </div>
          </button>
        ))}
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">
              Question {currentQuestionIndex + 1} of {questions.length}
            </span>
            <span className="text-sm text-neutral-500 capitalize">
              {currentQuestion.category === 'general' ? 'About You' : currentQuestion.category}
            </span>
          </div>
          <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Question */}
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">{currentQuestion.question}</h2>
        </div>

        {/* Options */}
        {renderQuestionOptions()}

        {/* Action Button */}
        <div className="flex gap-3">
          <button
            onClick={handleSubmitAnswer}
            disabled={selectedAnswer === null || (Array.isArray(selectedAnswer) && selectedAnswer.length === 0)}
            className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'Complete Survey'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default IntroAssessmentPage