import { Question } from '../types/database.types'

export interface AdaptiveQuestionSelection {
  preQuizQuestions: Question[]
  testQuestions: Question[]
}

export interface PerformanceTracker {
  correctAnswers: number
  totalAnswers: number
  currentDifficulty: string
  difficultyHistory: string[]
}

const DIFFICULTY_ORDER: Record<string, number> = {
  'easy': 1,
  'medium': 2,
  'hard': 3,
  'expert': 4
}

class AdaptiveLearningService {
  /**
   * Select questions for adaptive learning, starting with easy questions
   * and potentially progressing to harder ones based on performance
   */
  selectAdaptiveQuestions(
    allQuestions: Question[],
    preQuizCount: number = 3,
    testCount: number = 10
  ): AdaptiveQuestionSelection {
    // Group questions by difficulty
    const questionsByDifficulty = this.groupQuestionsByDifficulty(allQuestions)
    
    // Select pre-quiz questions (start with easy questions)
    const preQuizQuestions = this.selectPreQuizQuestions(questionsByDifficulty, preQuizCount)
    
    // Select test questions (adaptive based on pre-quiz performance)
    const remainingQuestions = allQuestions.filter(
      q => !preQuizQuestions.find(pq => pq.id === q.id)
    )
    const testQuestions = this.selectTestQuestions(remainingQuestions, testCount)
    
    return {
      preQuizQuestions,
      testQuestions
    }
  }

  /**
   * Group questions by difficulty level
   */
  private groupQuestionsByDifficulty(questions: Question[]): Record<string, Question[]> {
    const grouped: Record<string, Question[]> = {
      easy: [],
      medium: [],
      hard: [],
      expert: []
    }
    
    questions.forEach(question => {
      const difficulty = this.normalizeDifficulty(question.difficulty)
      if (grouped[difficulty]) {
        grouped[difficulty].push(question)
      } else {
        // Default to medium if difficulty is not recognized
        grouped.medium.push(question)
      }
    })
    
    return grouped
  }

  /**
   * Normalize difficulty strings to standard levels
   */
  private normalizeDifficulty(difficulty: string): string {
    const lower = difficulty.toLowerCase()
    
    // Map various difficulty naming conventions to our standard levels
    if (lower.includes('easy') || lower.includes('beginner') || lower === '1') {
      return 'easy'
    } else if (lower.includes('hard') || lower.includes('difficult') || lower === '3') {
      return 'hard'
    } else if (lower.includes('expert') || lower.includes('advanced') || lower === '4') {
      return 'expert'
    } else {
      // Default to medium for anything else
      return 'medium'
    }
  }

  /**
   * Select pre-quiz questions, prioritizing easier questions
   */
  private selectPreQuizQuestions(
    questionsByDifficulty: Record<string, Question[]>,
    count: number
  ): Question[] {
    const selected: Question[] = []
    
    // Start with easy questions
    const easyQuestions = this.shuffleArray([...questionsByDifficulty.easy])
    const mediumQuestions = this.shuffleArray([...questionsByDifficulty.medium])
    
    // Select 2 easy and 1 medium for pre-quiz (if available)
    if (count >= 3) {
      // Take up to 2 easy questions
      selected.push(...easyQuestions.slice(0, Math.min(2, easyQuestions.length)))
      
      // If we don't have enough easy questions, fill with medium
      if (selected.length < 2 && mediumQuestions.length > 0) {
        const needed = 2 - selected.length
        selected.push(...mediumQuestions.slice(0, needed))
      }
      
      // Add 1 medium question for the third question
      if (mediumQuestions.length > 0) {
        const remainingMedium = mediumQuestions.filter(
          q => !selected.find(s => s.id === q.id)
        )
        if (remainingMedium.length > 0) {
          selected.push(remainingMedium[0])
        }
      }
    } else {
      // For smaller pre-quiz counts, just take easy questions
      selected.push(...easyQuestions.slice(0, count))
      
      // Fill with medium if needed
      if (selected.length < count) {
        const needed = count - selected.length
        selected.push(...mediumQuestions.slice(0, needed))
      }
    }
    
    // If we still don't have enough questions, add from other difficulties
    if (selected.length < count) {
      const allRemaining = [
        ...questionsByDifficulty.hard,
        ...questionsByDifficulty.expert
      ].filter(q => !selected.find(s => s.id === q.id))
      
      const needed = count - selected.length
      selected.push(...this.shuffleArray(allRemaining).slice(0, needed))
    }
    
    return selected.slice(0, count)
  }

  /**
   * Select test questions with adaptive difficulty progression
   */
  private selectTestQuestions(questions: Question[], count: number): Question[] {
    const grouped = this.groupQuestionsByDifficulty(questions)
    const selected: Question[] = []
    
    // Create a difficulty distribution for the test
    // Start with easier questions and progress to harder ones
    const distribution = this.createAdaptiveDistribution(count)
    
    distribution.forEach(({ difficulty, count: diffCount }) => {
      const available = this.shuffleArray(grouped[difficulty] || [])
      selected.push(...available.slice(0, diffCount))
    })
    
    // If we don't have enough questions from the planned distribution,
    // fill with any remaining questions
    if (selected.length < count) {
      const remaining = questions.filter(q => !selected.find(s => s.id === q.id))
      const needed = count - selected.length
      selected.push(...this.shuffleArray(remaining).slice(0, needed))
    }
    
    return selected.slice(0, count)
  }

  /**
   * Create an adaptive distribution of difficulties for the test
   */
  private createAdaptiveDistribution(totalCount: number): { difficulty: string; count: number }[] {
    if (totalCount <= 5) {
      // For small tests, mostly easy and medium
      return [
        { difficulty: 'easy', count: Math.ceil(totalCount * 0.6) },
        { difficulty: 'medium', count: Math.floor(totalCount * 0.4) }
      ]
    } else if (totalCount <= 10) {
      // For medium tests, progressive difficulty
      return [
        { difficulty: 'easy', count: Math.ceil(totalCount * 0.4) },
        { difficulty: 'medium', count: Math.ceil(totalCount * 0.4) },
        { difficulty: 'hard', count: Math.floor(totalCount * 0.2) }
      ]
    } else {
      // For larger tests, full range of difficulties
      return [
        { difficulty: 'easy', count: Math.ceil(totalCount * 0.3) },
        { difficulty: 'medium', count: Math.ceil(totalCount * 0.35) },
        { difficulty: 'hard', count: Math.ceil(totalCount * 0.25) },
        { difficulty: 'expert', count: Math.floor(totalCount * 0.1) }
      ]
    }
  }

  /**
   * Get next question difficulty based on performance
   */
  getNextDifficulty(
    currentDifficulty: string,
    isCorrect: boolean,
    consecutiveCorrect: number,
    consecutiveIncorrect: number
  ): string {
    const currentLevel = DIFFICULTY_ORDER[currentDifficulty] || 2
    
    // Progress to harder difficulty after 2 consecutive correct answers
    if (isCorrect && consecutiveCorrect >= 2) {
      const nextLevel = Math.min(currentLevel + 1, 4)
      return Object.keys(DIFFICULTY_ORDER).find(
        key => DIFFICULTY_ORDER[key] === nextLevel
      ) || currentDifficulty
    }
    
    // Drop to easier difficulty after 2 consecutive incorrect answers
    if (!isCorrect && consecutiveIncorrect >= 2) {
      const nextLevel = Math.max(currentLevel - 1, 1)
      return Object.keys(DIFFICULTY_ORDER).find(
        key => DIFFICULTY_ORDER[key] === nextLevel
      ) || currentDifficulty
    }
    
    // Stay at current difficulty
    return currentDifficulty
  }

  /**
   * Sort questions by difficulty (easy to hard)
   */
  sortQuestionsByDifficulty(questions: Question[]): Question[] {
    return questions.sort((a, b) => {
      const aDiff = DIFFICULTY_ORDER[this.normalizeDifficulty(a.difficulty)] || 2
      const bDiff = DIFFICULTY_ORDER[this.normalizeDifficulty(b.difficulty)] || 2
      return aDiff - bDiff
    })
  }

  /**
   * Shuffle array using Fisher-Yates algorithm
   */
  private shuffleArray<T>(array: T[]): T[] {
    const shuffled = [...array]
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    return shuffled
  }

  /**
   * Calculate performance score based on difficulty and correctness
   */
  calculatePerformanceScore(
    questions: Question[],
    answers: Record<number, { correct: boolean; timeSpent: number }>
  ): number {
    let totalScore = 0
    let maxScore = 0
    
    questions.forEach((question, index) => {
      const answer = answers[index]
      if (!answer) return
      
      const difficultyMultiplier = DIFFICULTY_ORDER[this.normalizeDifficulty(question.difficulty)] || 2
      const basePoints = 10 * difficultyMultiplier
      
      maxScore += basePoints
      
      if (answer.correct) {
        // Award points based on difficulty
        let points = basePoints
        
        // Bonus for quick answers (under 30 seconds)
        if (answer.timeSpent < 30) {
          points *= 1.2
        }
        
        totalScore += points
      }
    })
    
    return maxScore > 0 ? Math.round((totalScore / maxScore) * 100) : 0
  }
}

export const adaptiveLearningService = new AdaptiveLearningService()