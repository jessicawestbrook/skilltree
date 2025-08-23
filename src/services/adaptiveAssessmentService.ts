import { supabase } from './supabase'

// Types for the adaptive assessment system
export interface Question {
  id: string
  question_text: string
  options: string[]
  correct_answer: string
  explanation: string
  difficulty_level: number
  estimated_time_seconds: number
  cognitive_load_rating: number
  skill_id: string
  last_used_at?: string
  usage_count: number
}

export interface AssessmentSession {
  id: string
  user_id: string
  category_id: string
  started_at: string
  ended_at?: string
  total_points: number
  questions_answered: number
  highest_difficulty_reached: number
  final_ability_estimate: number
  session_type: 'practice' | 'assessment' | 'quick_test'
  is_completed: boolean
}

export interface QuestionResponse {
  id: string
  session_id: string
  question_id: string
  user_response: string
  is_correct: boolean
  response_time_ms: number
  difficulty_level: number
  points_earned: number
  question_sequence: number
  point_multipliers: Record<string, number>
  answered_at: string
}

export interface UserCategoryScore {
  id: string
  user_id: string
  category_id: string
  current_ability_estimate: number
  total_points: number
  best_session_points: number
  questions_answered_total: number
  sessions_completed: number
  last_assessment_date?: string
  mastery_level: number
  achievement_badges: string[]
}

// Point calculation system
export class PointCalculator {
  // Base points for each difficulty level
  private static readonly DIFFICULTY_BASE_POINTS = {
    1: 10,   // Beginner
    2: 25,   // Elementary
    3: 50,   // Intermediate
    4: 100,  // Advanced
    5: 200   // Expert
  }

  // Multiplier factors
  private static readonly CONSECUTIVE_BONUS = 1.1  // 3+ consecutive correct
  private static readonly QUICK_RESPONSE_BONUS = 1.05  // Under 15 seconds
  private static readonly FIRST_ATTEMPT_BONUS = 1.2   // Never seen this question
  private static readonly MAX_MULTIPLIER = 2.0        // Cap total multipliers

  /**
   * Calculate points for a single question response
   */
  static calculateQuestionPoints(
    difficultyLevel: number,
    isCorrect: boolean,
    responseTimeMs: number,
    consecutiveCorrect: number,
    isFirstAttempt: boolean,
    questionTimeLimit: number = 60000 // Default 60 seconds
  ): { points: number; multipliers: Record<string, number> } {
    
    if (!isCorrect) {
      return { points: 0, multipliers: {} }
    }

    const basePoints = this.DIFFICULTY_BASE_POINTS[difficultyLevel as keyof typeof this.DIFFICULTY_BASE_POINTS] || 25
    const multipliers: Record<string, number> = {}
    let totalMultiplier = 1.0

    // Consecutive correct bonus
    if (consecutiveCorrect >= 3) {
      multipliers.consecutive = this.CONSECUTIVE_BONUS
      totalMultiplier *= this.CONSECUTIVE_BONUS
    }

    // Quick response bonus (within 25% of estimated time)
    const quickThreshold = Math.min(15000, questionTimeLimit * 0.25)
    if (responseTimeMs <= quickThreshold) {
      multipliers.quick_response = this.QUICK_RESPONSE_BONUS
      totalMultiplier *= this.QUICK_RESPONSE_BONUS
    }

    // First attempt bonus
    if (isFirstAttempt) {
      multipliers.first_attempt = this.FIRST_ATTEMPT_BONUS
      totalMultiplier *= this.FIRST_ATTEMPT_BONUS
    }

    // Cap the total multiplier
    totalMultiplier = Math.min(totalMultiplier, this.MAX_MULTIPLIER)

    const finalPoints = Math.round(basePoints * totalMultiplier)
    
    return { points: finalPoints, multipliers }
  }

  /**
   * Calculate mastery level based on ability estimate
   */
  static calculateMasteryLevel(abilityEstimate: number): number {
    if (abilityEstimate >= 4.0) return 5  // Expert
    if (abilityEstimate >= 3.0) return 4  // Advanced
    if (abilityEstimate >= 2.0) return 3  // Intermediate
    if (abilityEstimate >= 1.0) return 2  // Elementary
    return 1  // Beginner
  }

  /**
   * Determine achievement badges based on performance
   */
  static calculateAchievementBadges(
    session: AssessmentSession,
    categoryScore: UserCategoryScore
  ): string[] {
    const badges: string[] = []

    // Difficulty achievement badges
    if (session.highest_difficulty_reached >= 5) badges.push('expert_reached')
    if (session.highest_difficulty_reached >= 4) badges.push('advanced_reached')
    if (session.highest_difficulty_reached >= 3) badges.push('intermediate_reached')

    // Endurance badges
    if (session.questions_answered >= 50) badges.push('marathon_session')
    if (session.questions_answered >= 25) badges.push('extended_session')
    if (session.questions_answered >= 10) badges.push('dedicated_learner')

    // Point achievement badges
    if (session.total_points >= 1000) badges.push('thousand_points')
    if (session.total_points >= 500) badges.push('five_hundred_points')

    // Consistency badges
    if (categoryScore.sessions_completed >= 10) badges.push('persistent_learner')
    if (categoryScore.sessions_completed >= 5) badges.push('regular_assessor')

    // Performance badges
    const accuracy = categoryScore.questions_answered_total > 0 
      ? categoryScore.total_points / (categoryScore.questions_answered_total * 25) // Assuming average question worth 25 points
      : 0
    
    if (accuracy >= 0.9) badges.push('accuracy_master')
    if (accuracy >= 0.8) badges.push('high_achiever')

    return badges
  }
}

// Adaptive Question Selection Algorithm
export class AdaptiveQuestionSelector {
  /**
   * Select the next question based on user's current ability and response history
   */
  static async selectNextQuestion(
    userId: string,
    categoryId: string,
    currentAbilityEstimate: number,
    sessionId: string,
    questionSequence: number
  ): Promise<Question | null> {
    try {
      // Determine target difficulty level based on ability estimate
      const targetDifficulty = this.getTargetDifficulty(currentAbilityEstimate)
      
      // Get recently answered questions to avoid repetition
      const recentQuestions = await this.getRecentQuestions(userId, categoryId, 30)
      
      // First try: Get unasked questions at target difficulty
      let question = await this.getQuestionAtDifficulty(
        categoryId, 
        targetDifficulty, 
        recentQuestions,
        userId
      )
      
      // Fallback: Try adjacent difficulty levels
      if (!question) {
        const fallbackDifficulties = this.getFallbackDifficulties(targetDifficulty)
        for (const difficulty of fallbackDifficulties) {
          question = await this.getQuestionAtDifficulty(
            categoryId, 
            difficulty, 
            recentQuestions,
            userId
          )
          if (question) break
        }
      }
      
      // Update question usage tracking
      if (question) {
        await this.updateQuestionUsage(question.id, userId, categoryId)
      }
      
      return question
      
    } catch (error) {
      console.error('Error selecting next question:', error)
      return null
    }
  }

  /**
   * Determine target difficulty based on current ability estimate
   */
  private static getTargetDifficulty(abilityEstimate: number): number {
    // Round ability estimate to nearest difficulty level
    return Math.max(1, Math.min(5, Math.round(abilityEstimate)))
  }

  /**
   * Get fallback difficulty levels in order of preference
   */
  private static getFallbackDifficulties(targetDifficulty: number): number[] {
    const fallbacks: number[] = []
    
    // Add adjacent levels
    if (targetDifficulty > 1) fallbacks.push(targetDifficulty - 1)
    if (targetDifficulty < 5) fallbacks.push(targetDifficulty + 1)
    
    // Add more distant levels
    if (targetDifficulty > 2) fallbacks.push(targetDifficulty - 2)
    if (targetDifficulty < 4) fallbacks.push(targetDifficulty + 2)
    
    // Add remaining levels
    for (let i = 1; i <= 5; i++) {
      if (i !== targetDifficulty && !fallbacks.includes(i)) {
        fallbacks.push(i)
      }
    }
    
    return fallbacks
  }

  /**
   * Get recently answered questions to avoid repetition
   */
  private static async getRecentQuestions(
    userId: string, 
    categoryId: string, 
    dayLimit: number
  ): Promise<string[]> {
    const { data, error } = await supabase
      .from('user_question_history')
      .select('question_id')
      .eq('user_id', userId)
      .eq('category_id', categoryId)
      .gte('last_seen_at', new Date(Date.now() - dayLimit * 24 * 60 * 60 * 1000).toISOString())
    
    if (error) {
      console.error('Error fetching recent questions:', error)
      return []
    }
    
    return data?.map(row => row.question_id) || []
  }

  /**
   * Get a question at specific difficulty level
   */
  private static async getQuestionAtDifficulty(
    categoryId: string,
    difficulty: number,
    excludeQuestions: string[],
    userId: string
  ): Promise<Question | null> {
    let query = supabase
      .from('questions')
      .select('*')
      .eq('skill_id', categoryId)
      .eq('difficulty_level', difficulty)
      .order('usage_count', { ascending: true })  // Prefer less-used questions
      .order('last_used_at', { ascending: true, nullsFirst: true })  // Prefer never/old questions
      .limit(10)  // Get multiple options for randomization
    
    // Exclude recently seen questions
    if (excludeQuestions.length > 0) {
      query = query.not('id', 'in', `(${excludeQuestions.map(q => `'${q}'`).join(',')})`)
    }
    
    const { data, error } = await query
    
    if (error) {
      console.error('Error fetching questions:', error)
      return null
    }
    
    if (!data || data.length === 0) {
      return null
    }
    
    // Randomly select from available questions to add variety
    const randomIndex = Math.floor(Math.random() * data.length)
    return data[randomIndex] as Question
  }

  /**
   * Update question usage tracking
   */
  private static async updateQuestionUsage(
    questionId: string, 
    userId: string, 
    categoryId: string
  ): Promise<void> {
    try {
      // Update question usage count
      await supabase
        .from('questions')
        .update({ 
          usage_count: supabase.rpc('increment_usage_count', { question_id: questionId }),
          last_used_at: new Date().toISOString()
        })
        .eq('id', questionId)
      
      // Update or insert user question history
      await supabase
        .from('user_question_history')
        .upsert({
          user_id: userId,
          question_id: questionId,
          category_id: categoryId,
          times_seen: supabase.rpc('increment_times_seen', { 
            p_user_id: userId, 
            p_question_id: questionId 
          }),
          last_seen_at: new Date().toISOString()
        })
        
    } catch (error) {
      console.error('Error updating question usage:', error)
    }
  }
}

// Ability Estimation Algorithm (simplified IRT-based)
export class AbilityEstimator {
  /**
   * Update ability estimate based on question response
   */
  static updateAbilityEstimate(
    currentEstimate: number,
    questionDifficulty: number,
    isCorrect: boolean,
    consecutivePattern: number[] // Recent response pattern
  ): number {
    const difficultyWeight = 0.1
    const baseAdjustment = questionDifficulty * difficultyWeight
    
    let adjustment = 0
    
    if (isCorrect) {
      // Positive adjustment for correct answer
      adjustment = baseAdjustment
      
      // Bonus for consistent performance
      const recentAccuracy = this.calculateRecentAccuracy(consecutivePattern)
      if (recentAccuracy >= 0.8) {
        adjustment *= 1.2  // 20% bonus for high accuracy
      }
    } else {
      // Negative adjustment for incorrect answer
      adjustment = -baseAdjustment * 1.5  // Slightly larger penalty
      
      // Additional penalty for consecutive mistakes
      const consecutiveIncorrect = this.countConsecutiveIncorrect(consecutivePattern)
      if (consecutiveIncorrect >= 2) {
        adjustment *= 1.3  // 30% additional penalty
      }
    }
    
    // Apply adjustment with bounds checking
    const newEstimate = currentEstimate + adjustment
    return Math.max(0.1, Math.min(5.0, newEstimate))  // Keep within valid range
  }

  /**
   * Calculate accuracy from recent response pattern
   */
  private static calculateRecentAccuracy(pattern: number[]): number {
    if (pattern.length === 0) return 0
    const correct = pattern.filter(response => response === 1).length
    return correct / pattern.length
  }

  /**
   * Count consecutive incorrect responses at the end of pattern
   */
  private static countConsecutiveIncorrect(pattern: number[]): number {
    let count = 0
    for (let i = pattern.length - 1; i >= 0; i--) {
      if (pattern[i] === 0) {
        count++
      } else {
        break
      }
    }
    return count
  }
}

// Main Assessment Service
export class AdaptiveAssessmentService {
  /**
   * Start a new adaptive assessment session
   */
  static async startAssessment(
    userId: string,
    categoryId: string,
    sessionType: 'practice' | 'assessment' | 'quick_test' = 'assessment'
  ): Promise<AssessmentSession | null> {
    try {
      // Get user's current ability estimate for this category
      const abilityEstimate = await this.getUserAbilityEstimate(userId, categoryId)
      
      // Create new assessment session
      const { data, error } = await supabase
        .from('assessment_sessions')
        .insert({
          user_id: userId,
          category_id: categoryId,
          session_type: sessionType,
          final_ability_estimate: abilityEstimate
        })
        .select()
        .single()
      
      if (error) throw error
      
      return data as AssessmentSession
      
    } catch (error) {
      console.error('Error starting assessment:', error)
      return null
    }
  }

  /**
   * Get the next question for an assessment session
   */
  static async getNextQuestion(
    sessionId: string,
    userId: string,
    categoryId: string
  ): Promise<Question | null> {
    try {
      // Get current session state
      const session = await this.getSessionById(sessionId)
      if (!session) return null
      
      // Get user's current ability estimate
      const abilityEstimate = session.final_ability_estimate
      
      // Select next question
      return await AdaptiveQuestionSelector.selectNextQuestion(
        userId,
        categoryId,
        abilityEstimate,
        sessionId,
        session.questions_answered + 1
      )
      
    } catch (error) {
      console.error('Error getting next question:', error)
      return null
    }
  }

  /**
   * Record a question response and update session
   */
  static async recordResponse(
    sessionId: string,
    questionId: string,
    userResponse: string,
    isCorrect: boolean,
    responseTimeMs: number
  ): Promise<QuestionResponse | null> {
    try {
      // Get session and question details
      const [session, question] = await Promise.all([
        this.getSessionById(sessionId),
        this.getQuestionById(questionId)
      ])
      
      if (!session || !question) return null
      
      // Get recent response pattern for ability estimation
      const recentResponses = await this.getRecentResponses(sessionId, 5)
      const consecutiveCorrect = this.countConsecutiveCorrect(recentResponses)
      
      // Check if this is first time seeing this question
      const isFirstAttempt = await this.isFirstAttempt(session.user_id, questionId)
      
      // Calculate points
      const { points, multipliers } = PointCalculator.calculateQuestionPoints(
        question.difficulty_level,
        isCorrect,
        responseTimeMs,
        consecutiveCorrect,
        isFirstAttempt,
        question.estimated_time_seconds * 1000
      )
      
      // Record the response
      const { data: response, error: responseError } = await supabase
        .from('question_responses')
        .insert({
          session_id: sessionId,
          question_id: questionId,
          user_response: userResponse,
          is_correct: isCorrect,
          response_time_ms: responseTimeMs,
          difficulty_level: question.difficulty_level,
          points_earned: points,
          question_sequence: session.questions_answered + 1,
          point_multipliers: multipliers
        })
        .select()
        .single()
      
      if (responseError) throw responseError
      
      // Update ability estimate
      const responsePattern = [...recentResponses.map(r => r.is_correct ? 1 : 0), isCorrect ? 1 : 0]
      const newAbilityEstimate = AbilityEstimator.updateAbilityEstimate(
        session.final_ability_estimate,
        question.difficulty_level,
        isCorrect,
        responsePattern
      )
      
      // Update session
      await this.updateSession(sessionId, {
        total_points: session.total_points + points,
        questions_answered: session.questions_answered + 1,
        highest_difficulty_reached: Math.max(session.highest_difficulty_reached, question.difficulty_level),
        final_ability_estimate: newAbilityEstimate
      })
      
      // Update user category scores
      await this.updateUserCategoryScore(session.user_id, session.category_id, points, newAbilityEstimate)
      
      return response as QuestionResponse
      
    } catch (error) {
      console.error('Error recording response:', error)
      return null
    }
  }

  /**
   * Complete an assessment session
   */
  static async completeAssessment(sessionId: string): Promise<AssessmentSession | null> {
    try {
      const { data, error } = await supabase
        .from('assessment_sessions')
        .update({
          ended_at: new Date().toISOString(),
          is_completed: true
        })
        .eq('id', sessionId)
        .select()
        .single()
      
      if (error) throw error
      
      // Update user category scores with session completion
      const session = data as AssessmentSession
      await this.recordSessionCompletion(session)
      
      return session
      
    } catch (error) {
      console.error('Error completing assessment:', error)
      return null
    }
  }

  // Helper methods
  private static async getUserAbilityEstimate(userId: string, categoryId: string): Promise<number> {
    const { data, error } = await supabase
      .from('user_category_scores')
      .select('current_ability_estimate')
      .eq('user_id', userId)
      .eq('category_id', categoryId)
      .single()
    
    if (error || !data) {
      return 2.0  // Default to elementary level
    }
    
    return data.current_ability_estimate || 2.0
  }

  private static async getSessionById(sessionId: string): Promise<AssessmentSession | null> {
    const { data, error } = await supabase
      .from('assessment_sessions')
      .select('*')
      .eq('id', sessionId)
      .single()
    
    return error ? null : data as AssessmentSession
  }

  private static async getQuestionById(questionId: string): Promise<Question | null> {
    const { data, error } = await supabase
      .from('questions')
      .select('*')
      .eq('id', questionId)
      .single()
    
    return error ? null : data as Question
  }

  private static async getRecentResponses(sessionId: string, limit: number): Promise<QuestionResponse[]> {
    const { data, error } = await supabase
      .from('question_responses')
      .select('*')
      .eq('session_id', sessionId)
      .order('question_sequence', { ascending: false })
      .limit(limit)
    
    return error ? [] : data as QuestionResponse[]
  }

  private static countConsecutiveCorrect(responses: QuestionResponse[]): number {
    let count = 0
    for (const response of responses) {
      if (response.is_correct) {
        count++
      } else {
        break
      }
    }
    return count
  }

  private static async isFirstAttempt(userId: string, questionId: string): Promise<boolean> {
    const { data, error } = await supabase
      .from('user_question_history')
      .select('times_seen')
      .eq('user_id', userId)
      .eq('question_id', questionId)
      .single()
    
    return !!error || !data || data.times_seen === 0
  }

  private static async updateSession(sessionId: string, updates: Partial<AssessmentSession>): Promise<void> {
    await supabase
      .from('assessment_sessions')
      .update(updates)
      .eq('id', sessionId)
  }

  private static async updateUserCategoryScore(
    userId: string, 
    categoryId: string, 
    pointsEarned: number, 
    abilityEstimate: number
  ): Promise<void> {
    await supabase
      .from('user_category_scores')
      .upsert({
        user_id: userId,
        category_id: categoryId,
        current_ability_estimate: abilityEstimate,
        total_points: supabase.rpc('add_points', { user_id: userId, category_id: categoryId, points: pointsEarned }),
        questions_answered_total: supabase.rpc('increment_questions_answered', { user_id: userId, category_id: categoryId }),
        mastery_level: PointCalculator.calculateMasteryLevel(abilityEstimate),
        last_assessment_date: new Date().toISOString()
      })
  }

  private static async recordSessionCompletion(session: AssessmentSession): Promise<void> {
    // Get current category score
    const { data: categoryScore } = await supabase
      .from('user_category_scores')
      .select('*')
      .eq('user_id', session.user_id)
      .eq('category_id', session.category_id)
      .single()
    
    if (categoryScore) {
      // Calculate achievement badges
      const newBadges = PointCalculator.calculateAchievementBadges(session, categoryScore as UserCategoryScore)
      const existingBadges = categoryScore.achievement_badges || []
      const badgeSet = new Set([...existingBadges, ...newBadges])
      const updatedBadges = Array.from(badgeSet)
      
      // Update category score with session completion data
      await supabase
        .from('user_category_scores')
        .update({
          sessions_completed: (categoryScore.sessions_completed || 0) + 1,
          best_session_points: Math.max(categoryScore.best_session_points || 0, session.total_points),
          achievement_badges: updatedBadges
        })
        .eq('user_id', session.user_id)
        .eq('category_id', session.category_id)
    }
  }
}