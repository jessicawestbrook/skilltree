import React, { useState, useEffect, useCallback } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { checkReadingComprehensionTables, createReadingComprehensionTables } from '../utils/createReadingComprehensionTables'
import {
  BookOpenIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowRightIcon,
  ClockIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline'

interface ReadingPassage {
  id: string
  title: string
  passage_text: string
  difficulty_level: number
  category: string
  word_count: number
  source_url?: string
  source_attribution?: string
  created_at?: string
}

interface ComprehensionQuestion {
  id: string
  passage_id: string
  question_text: string
  options: string[]
  correct_answer_index: number
  explanation: string
  question_type: 'main_idea' | 'detail' | 'inference' | 'vocabulary' | 'author_purpose'
  order_index: number
}

interface UserAnswer {
  questionId: string
  selectedIndex: number
  isCorrect: boolean
}

const ReadingComprehensionPage: React.FC = () => {
  const { user } = useAuth()
  const [passages, setPassages] = useState<ReadingPassage[]>([])
  const [currentPassage, setCurrentPassage] = useState<ReadingPassage | null>(null)
  const [questions, setQuestions] = useState<ComprehensionQuestion[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [userAnswers, setUserAnswers] = useState<UserAnswer[]>([])
  const [showResult, setShowResult] = useState(false)
  const [showPassageComplete, setShowPassageComplete] = useState(false)
  const [loading, setLoading] = useState(true)
  const [readingStartTime, setReadingStartTime] = useState<Date | null>(null)
  const [readingTime, setReadingTime] = useState(0)

  const fetchPassages = useCallback(async () => {
    try {
      // Check if table exists, create if not
      await createTablesIfNeeded()

      const { data, error } = await supabase
        .from('reading_passages')
        .select('*')
        .order('difficulty_level')
        .limit(20)

      if (error) {
        console.error('Error fetching passages:', error)
        // Create sample data if tables are empty
        await createSampleData()
        return
      }

      if (data && data.length > 0) {
        setPassages(data)
        setCurrentPassage(data[0])
      } else {
        await createSampleData()
      }
    } catch (error) {
      console.error('Error in fetchPassages:', error)
    } finally {
      setLoading(false)
    }
  }, [])

  const createTablesIfNeeded = async () => {
    const tablesExist = await checkReadingComprehensionTables()
    if (!tablesExist) {
      console.log('Creating reading comprehension tables...')
      await createReadingComprehensionTables()
    }
  }

  const createSampleData = async () => {
    const samplePassages = [
      {
        title: "The Evolution of Computing",
        passage_text: `The history of computing can be traced back to ancient times when humans first began using tools to aid in calculation. The abacus, developed around 2400 BCE in Babylonia, represents one of the earliest computing devices. For thousands of years, such mechanical aids remained the primary means of computation.

The modern era of computing began in the 19th century with Charles Babbage's design of the Analytical Engine, a mechanical general-purpose computer. Although never fully built during his lifetime, Babbage's design contained all the fundamental principles of modern digital computers. His collaborator, Ada Lovelace, is often credited as the first computer programmer for her work on algorithms for the Analytical Engine.

The 20th century saw rapid advancement in computing technology. The 1940s brought the first electronic digital computers, such as ENIAC, which filled entire rooms and used vacuum tubes. The invention of the transistor in 1947 revolutionized computing, leading to smaller, more reliable machines. The integrated circuit, developed in the late 1950s, further miniaturized components and increased processing power.

The personal computer revolution of the 1970s and 1980s brought computing power to individuals and small businesses. Companies like Apple and IBM made computers accessible to the general public. The development of graphical user interfaces made computers easier to use for non-technical users.

Today, computing pervades every aspect of modern life. Smartphones, tablets, and wearable devices put immense computing power in our pockets. Cloud computing allows access to virtually unlimited processing power and storage. Artificial intelligence and quantum computing represent the cutting edge of computational technology, promising to solve problems previously thought impossible.`,
        difficulty_level: 3,
        category: "Technology",
        word_count: 268,
        source_attribution: "Educational excerpt on computing history"
      },
      {
        title: "The Water Cycle",
        passage_text: `The water cycle, also known as the hydrological cycle, describes the continuous movement of water on, above, and below Earth's surface. This process has been occurring for billions of years and is essential for all life on our planet.

The cycle begins with evaporation, where water from oceans, lakes, and rivers transforms from liquid to vapor due to solar energy. Plants also contribute through transpiration, releasing water vapor from their leaves. This water vapor rises into the atmosphere, where cooler temperatures cause it to condense into tiny droplets, forming clouds.

As water droplets in clouds combine and grow larger, they eventually become too heavy to remain suspended in the air. This leads to precipitation in the form of rain, snow, sleet, or hail. The type of precipitation depends on atmospheric conditions and temperature.

When precipitation reaches the ground, several things can happen. Some water infiltrates the soil, becoming groundwater that can feed underground aquifers. Some flows over the surface as runoff, eventually reaching streams, rivers, and oceans. Plants absorb water through their roots, using it for photosynthesis and growth.

The water cycle plays a crucial role in weather patterns, climate regulation, and the distribution of Earth's freshwater resources. Human activities, such as deforestation and urbanization, can significantly impact local and regional water cycles. Understanding this cycle is essential for managing water resources and predicting environmental changes.`,
        difficulty_level: 2,
        category: "Science",
        word_count: 234,
        source_attribution: "Earth Science Educational Material"
      }
    ]

    // Insert sample passages
    for (const passage of samplePassages) {
      const { data: passageData, error } = await supabase
        .from('reading_passages')
        .insert(passage)
        .select()
        .single()

      if (!error && passageData) {
        // Create questions for each passage
        await createQuestionsForPassage(passageData.id, passage.title)
      }
    }

    // Fetch the newly created data
    const { data } = await supabase
      .from('reading_passages')
      .select('*')
      .order('difficulty_level')

    if (data) {
      setPassages(data)
      setCurrentPassage(data[0])
    }
  }

  const createQuestionsForPassage = async (passageId: string, title: string) => {
    const questionsMap: Record<string, ComprehensionQuestion[]> = {
      "The Evolution of Computing": [
        {
          id: '',
          passage_id: passageId,
          question_text: "What is identified as one of the earliest computing devices?",
          options: ["The transistor", "The abacus", "The Analytical Engine", "ENIAC"],
          correct_answer_index: 1,
          explanation: "The passage states that the abacus, developed around 2400 BCE in Babylonia, represents one of the earliest computing devices.",
          question_type: 'detail' as const,
          order_index: 1
        },
        {
          id: '',
          passage_id: passageId,
          question_text: "Who is credited as the first computer programmer?",
          options: ["Charles Babbage", "Ada Lovelace", "Alan Turing", "Bill Gates"],
          correct_answer_index: 1,
          explanation: "According to the passage, Ada Lovelace is often credited as the first computer programmer for her work on algorithms for the Analytical Engine.",
          question_type: 'detail' as const,
          order_index: 2
        },
        {
          id: '',
          passage_id: passageId,
          question_text: "What was the main impact of the transistor invention in 1947?",
          options: [
            "It created the first computer",
            "It made computers fill entire rooms",
            "It led to smaller, more reliable machines",
            "It enabled cloud computing"
          ],
          correct_answer_index: 2,
          explanation: "The passage indicates that the invention of the transistor in 1947 revolutionized computing, leading to smaller, more reliable machines.",
          question_type: 'detail' as const,
          order_index: 3
        },
        {
          id: '',
          passage_id: passageId,
          question_text: "What is the main idea of this passage?",
          options: [
            "Computers are getting more expensive",
            "Computing has evolved from ancient tools to modern AI",
            "Charles Babbage invented the first computer",
            "Smartphones are the most important computers"
          ],
          correct_answer_index: 1,
          explanation: "The passage traces the evolution of computing from ancient calculation tools like the abacus through to modern AI and quantum computing.",
          question_type: 'main_idea' as const,
          order_index: 4
        },
        {
          id: '',
          passage_id: passageId,
          question_text: "Based on the passage, what can be inferred about the future of computing?",
          options: [
            "It will become less important in daily life",
            "It will continue to advance and solve new problems",
            "It will return to mechanical devices",
            "It will stop evolving"
          ],
          correct_answer_index: 1,
          explanation: "The passage ends by mentioning AI and quantum computing as cutting edge technologies 'promising to solve problems previously thought impossible,' suggesting continued advancement.",
          question_type: 'inference' as const,
          order_index: 5
        }
      ],
      "The Water Cycle": [
        {
          id: '',
          passage_id: passageId,
          question_text: "What is another name for the water cycle?",
          options: ["The rain cycle", "The hydrological cycle", "The evaporation cycle", "The cloud cycle"],
          correct_answer_index: 1,
          explanation: "The passage begins by stating that the water cycle is 'also known as the hydrological cycle.'",
          question_type: 'detail' as const,
          order_index: 1
        },
        {
          id: '',
          passage_id: passageId,
          question_text: "What process contributes water vapor from plants?",
          options: ["Evaporation", "Condensation", "Transpiration", "Precipitation"],
          correct_answer_index: 2,
          explanation: "The passage mentions that plants contribute through transpiration, releasing water vapor from their leaves.",
          question_type: 'vocabulary' as const,
          order_index: 2
        },
        {
          id: '',
          passage_id: passageId,
          question_text: "What determines the type of precipitation that falls?",
          options: [
            "The size of clouds",
            "The time of day",
            "Atmospheric conditions and temperature",
            "The amount of water vapor"
          ],
          correct_answer_index: 2,
          explanation: "The passage states that the type of precipitation depends on atmospheric conditions and temperature.",
          question_type: 'detail' as const,
          order_index: 3
        },
        {
          id: '',
          passage_id: passageId,
          question_text: "What is the author's purpose in the final paragraph?",
          options: [
            "To describe precipitation types",
            "To explain evaporation",
            "To emphasize the importance and human impact on the water cycle",
            "To define scientific terms"
          ],
          correct_answer_index: 2,
          explanation: "The final paragraph discusses the crucial role of the water cycle and how human activities impact it, emphasizing its importance for resource management.",
          question_type: 'author_purpose' as const,
          order_index: 4
        }
      ]
    }

    const questions = questionsMap[title] || []
    for (const question of questions) {
      await supabase.from('comprehension_questions').insert(question)
    }
  }

  const fetchQuestionsForPassage = useCallback(async (passageId: string) => {
    try {
      const { data, error } = await supabase
        .from('comprehension_questions')
        .select('*')
        .eq('passage_id', passageId)
        .order('order_index')

      if (error) throw error

      if (data && data.length > 0) {
        setQuestions(data)
        setCurrentQuestionIndex(0)
        setUserAnswers([])
        setShowPassageComplete(false)
      }
    } catch (error) {
      console.error('Error fetching questions:', error)
    }
  }, [])

  useEffect(() => {
    fetchPassages()
  }, [fetchPassages])

  useEffect(() => {
    if (currentPassage) {
      fetchQuestionsForPassage(currentPassage.id)
      setReadingStartTime(new Date())
    }
  }, [currentPassage, fetchQuestionsForPassage])

  const handleAnswerSelect = (index: number) => {
    setSelectedAnswer(index)
  }

  const handleSubmitAnswer = async () => {
    if (selectedAnswer === null || !questions[currentQuestionIndex]) return

    const currentQuestion = questions[currentQuestionIndex]
    const isCorrect = selectedAnswer === currentQuestion.correct_answer_index

    const answer: UserAnswer = {
      questionId: currentQuestion.id,
      selectedIndex: selectedAnswer,
      isCorrect
    }

    setUserAnswers([...userAnswers, answer])
    setShowResult(true)

    // Save to database if user is logged in
    if (user) {
      await supabase.from('reading_comprehension_attempts').insert({
        user_id: user.id,
        passage_id: currentPassage?.id,
        question_id: currentQuestion.id,
        selected_answer: selectedAnswer,
        is_correct: isCorrect,
        time_taken: readingTime
      })
    }
  }

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setSelectedAnswer(null)
      setShowResult(false)
    } else {
      // All questions answered
      setShowPassageComplete(true)
      if (readingStartTime) {
        setReadingTime(Math.floor((new Date().getTime() - readingStartTime.getTime()) / 1000))
      }
    }
  }

  const handleNextPassage = () => {
    const currentIndex = passages.findIndex(p => p.id === currentPassage?.id)
    if (currentIndex < passages.length - 1) {
      setCurrentPassage(passages[currentIndex + 1])
      setSelectedAnswer(null)
      setShowResult(false)
      setShowPassageComplete(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!currentPassage) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6 text-center">
          <p className="text-lg">No reading passages available. Please check back later!</p>
        </div>
      </div>
    )
  }

  const currentQuestion = questions[currentQuestionIndex]
  const score = userAnswers.filter(a => a.isCorrect).length

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4">
          <span className="bg-gradient-to-r from-primary-600 to-gold-500 bg-clip-text text-transparent">
            Reading Comprehension
          </span>
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400">
          Read carefully and answer questions about the passage
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Reading Passage */}
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-6 max-h-[600px] overflow-y-auto">
          <div className="mb-4">
            <h2 className="text-xl font-bold mb-2">{currentPassage.title}</h2>
            <div className="flex items-center gap-4 text-sm text-neutral-500">
              <span className="flex items-center gap-1">
                <BookOpenIcon className="h-4 w-4" />
                {currentPassage.word_count} words
              </span>
              <span className="flex items-center gap-1">
                <AcademicCapIcon className="h-4 w-4" />
                Level {currentPassage.difficulty_level}
              </span>
              {readingStartTime && !showPassageComplete && (
                <span className="flex items-center gap-1">
                  <ClockIcon className="h-4 w-4" />
                  Reading...
                </span>
              )}
            </div>
          </div>
          <div className="prose dark:prose-invert max-w-none">
            <p className="whitespace-pre-wrap text-sm leading-relaxed">
              {currentPassage.passage_text}
            </p>
          </div>
          {currentPassage.source_attribution && (
            <div className="mt-4 pt-4 border-t border-neutral-200 dark:border-neutral-700">
              <p className="text-xs text-neutral-500 italic">
                Source: {currentPassage.source_attribution}
              </p>
            </div>
          )}
        </div>

        {/* Questions Section */}
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-6">
          {!showPassageComplete ? (
            <>
              <div className="mb-4">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="text-lg font-semibold">
                    Question {currentQuestionIndex + 1} of {questions.length}
                  </h3>
                  <span className="text-sm text-neutral-500">
                    Type: {currentQuestion?.question_type.replace('_', ' ')}
                  </span>
                </div>
                <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                  <div 
                    className="bg-primary-600 h-2 rounded-full transition-all"
                    style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
                  />
                </div>
              </div>

              {currentQuestion && (
                <div className="space-y-4">
                  <p className="text-lg font-medium">{currentQuestion.question_text}</p>
                  
                  <div className="space-y-2">
                    {currentQuestion.options.map((option, index) => (
                      <button
                        key={index}
                        onClick={() => handleAnswerSelect(index)}
                        disabled={showResult}
                        className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                          showResult
                            ? index === currentQuestion.correct_answer_index
                              ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                              : index === selectedAnswer
                              ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                              : 'border-neutral-200 dark:border-neutral-700'
                            : selectedAnswer === index
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                            : 'border-neutral-200 dark:border-neutral-700 hover:border-neutral-400'
                        }`}
                      >
                        <div className="flex items-start gap-3">
                          <span className="font-semibold">{String.fromCharCode(65 + index)}.</span>
                          <span>{option}</span>
                          {showResult && index === currentQuestion.correct_answer_index && (
                            <CheckCircleIcon className="h-5 w-5 text-green-500 ml-auto" />
                          )}
                          {showResult && index === selectedAnswer && index !== currentQuestion.correct_answer_index && (
                            <XCircleIcon className="h-5 w-5 text-red-500 ml-auto" />
                          )}
                        </div>
                      </button>
                    ))}
                  </div>

                  {showResult && (
                    <div className={`p-4 rounded-lg ${
                      userAnswers[userAnswers.length - 1]?.isCorrect
                        ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
                        : 'bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800'
                    }`}>
                      <p className="font-semibold mb-2">Explanation:</p>
                      <p className="text-sm">{currentQuestion.explanation}</p>
                    </div>
                  )}

                  <div className="flex gap-3">
                    {!showResult ? (
                      <button
                        onClick={handleSubmitAnswer}
                        disabled={selectedAnswer === null}
                        className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors"
                      >
                        Submit Answer
                      </button>
                    ) : (
                      <button
                        onClick={handleNextQuestion}
                        className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
                      >
                        {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'View Results'}
                        <ArrowRightIcon className="h-5 w-5" />
                      </button>
                    )}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center space-y-6">
              <div className="py-8">
                <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
                <h3 className="text-2xl font-bold mb-2">Passage Complete!</h3>
                <p className="text-lg text-neutral-600 dark:text-neutral-400">
                  You scored {score} out of {questions.length}
                </p>
                <p className="text-sm text-neutral-500 mt-2">
                  {Math.round((score / questions.length) * 100)}% accuracy
                </p>
                {readingTime > 0 && (
                  <p className="text-sm text-neutral-500 mt-1">
                    Time taken: {Math.floor(readingTime / 60)}m {readingTime % 60}s
                  </p>
                )}
              </div>

              <div className="space-y-2">
                {userAnswers.map((answer, idx) => (
                  <div 
                    key={idx}
                    className={`p-3 rounded-lg text-left ${
                      answer.isCorrect 
                        ? 'bg-green-50 dark:bg-green-900/20' 
                        : 'bg-red-50 dark:bg-red-900/20'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Question {idx + 1}</span>
                      {answer.isCorrect ? (
                        <CheckCircleIcon className="h-5 w-5 text-green-500" />
                      ) : (
                        <XCircleIcon className="h-5 w-5 text-red-500" />
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <button
                onClick={handleNextPassage}
                className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Next Passage →
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ReadingComprehensionPage