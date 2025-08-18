import { supabase } from './supabase'

export interface QuestionAttempt {
  id: string
  user_id: string
  question_id: string
  is_correct: boolean
  time_taken_seconds: number
  attempt_number: number
  created_at: string
}

export interface QuestionHistory {
  question_id: string
  view_count: number
  correct_count: number
  incorrect_count: number
  last_seen: string
  last_correct: string | null
  last_incorrect: string | null
  average_time: number
}

export interface QuestionPriority {
  question_id: string
  priority: number
  reason: string
}

class QuestionTrackingService {
  /**
   * Track when a user views a question
   */
  async trackQuestionView(userId: string, questionId: string): Promise<void> {
    try {
      // Check if tracking record exists
      const { data: existing } = await supabase
        .from('user_question_tracking')
        .select('*')
        .eq('user_id', userId)
        .eq('question_id', questionId)
        .single()

      if (existing) {
        // Update existing record
        await supabase
          .from('user_question_tracking')
          .update({
            view_count: existing.view_count + 1,
            last_seen: new Date().toISOString()
          })
          .eq('user_id', userId)
          .eq('question_id', questionId)
      } else {
        // Create new tracking record
        await supabase
          .from('user_question_tracking')
          .insert({
            user_id: userId,
            question_id: questionId,
            view_count: 1,
            correct_count: 0,
            incorrect_count: 0,
            last_seen: new Date().toISOString()
          })
      }
    } catch (error) {
      console.error('Error tracking question view:', error)
    }
  }

  /**
   * Track a user's answer to a question
   */
  async trackQuestionAttempt(
    userId: string,
    questionId: string,
    isCorrect: boolean,
    timeTaken: number
  ): Promise<void> {
    try {
      // Get current attempt number
      const { count } = await supabase
        .from('user_question_attempts')
        .select('*', { count: 'exact' })
        .eq('user_id', userId)
        .eq('question_id', questionId)

      const attemptNumber = (count || 0) + 1

      // Record the attempt
      await supabase
        .from('user_question_attempts')
        .insert({
          user_id: userId,
          question_id: questionId,
          is_correct: isCorrect,
          time_taken_seconds: timeTaken,
          attempt_number: attemptNumber,
          created_at: new Date().toISOString()
        })

      // Update tracking summary
      const { data: tracking } = await supabase
        .from('user_question_tracking')
        .select('*')
        .eq('user_id', userId)
        .eq('question_id', questionId)
        .single()

      if (tracking) {
        const updates: any = {
          last_seen: new Date().toISOString()
        }

        if (isCorrect) {
          updates.correct_count = tracking.correct_count + 1
          updates.last_correct = new Date().toISOString()
        } else {
          updates.incorrect_count = tracking.incorrect_count + 1
          updates.last_incorrect = new Date().toISOString()
        }

        // Update average time
        const totalAttempts = tracking.correct_count + tracking.incorrect_count + 1
        updates.average_time = 
          (tracking.average_time * (totalAttempts - 1) + timeTaken) / totalAttempts

        await supabase
          .from('user_question_tracking')
          .update(updates)
          .eq('user_id', userId)
          .eq('question_id', questionId)
      }
    } catch (error) {
      console.error('Error tracking question attempt:', error)
    }
  }

  /**
   * Get user's history with specific questions
   */
  async getUserQuestionHistory(
    userId: string,
    questionIds: string[]
  ): Promise<Map<string, QuestionHistory>> {
    try {
      const { data, error } = await supabase
        .from('user_question_tracking')
        .select('*')
        .eq('user_id', userId)
        .in('question_id', questionIds)

      if (error) throw error

      const historyMap = new Map<string, QuestionHistory>()
      
      data?.forEach(record => {
        historyMap.set(record.question_id, {
          question_id: record.question_id,
          view_count: record.view_count || 0,
          correct_count: record.correct_count || 0,
          incorrect_count: record.incorrect_count || 0,
          last_seen: record.last_seen,
          last_correct: record.last_correct,
          last_incorrect: record.last_incorrect,
          average_time: record.average_time || 0
        })
      })

      return historyMap
    } catch (error) {
      console.error('Error fetching question history:', error)
      return new Map()
    }
  }

  /**
   * Calculate priority for question selection (Spaced Repetition + Smart Selection)
   */
  calculateQuestionPriority(
    questionId: string,
    history: QuestionHistory | undefined,
    phase: 'pre-quiz' | 'test'
  ): QuestionPriority {
    let priority = 100
    let reason = 'new'

    if (!history) {
      // Never seen - highest priority
      return { question_id: questionId, priority: 100, reason: 'never_seen' }
    }

    // Reduce priority based on view count (prefer unviewed)
    priority -= history.view_count * 20
    
    // Calculate days since last seen
    const daysSinceSeen = history.last_seen 
      ? (Date.now() - new Date(history.last_seen).getTime()) / (1000 * 60 * 60 * 24)
      : 999

    // Spaced repetition for incorrect answers
    if (history.incorrect_count > 0 && phase === 'test') {
      const daysSinceIncorrect = history.last_incorrect
        ? (Date.now() - new Date(history.last_incorrect).getTime()) / (1000 * 60 * 60 * 24)
        : 0

      // Optimal review intervals: 1, 3, 7, 14, 30 days
      const optimalIntervals = [1, 3, 7, 14, 30]
      const nearOptimal = optimalIntervals.some(
        interval => Math.abs(daysSinceIncorrect - interval) < 1
      )

      if (nearOptimal) {
        priority += 40
        reason = 'spaced_repetition'
      }
    }

    // Avoid recent questions (within 24 hours)
    if (daysSinceSeen < 1) {
      priority -= 50
      reason = 'too_recent'
    } else if (daysSinceSeen > 7) {
      // Boost older questions for review
      priority += 10
      reason = 'review'
    }

    // Adjust for success rate
    const totalAttempts = history.correct_count + history.incorrect_count
    if (totalAttempts > 0) {
      const successRate = history.correct_count / totalAttempts
      if (successRate < 0.5 && phase === 'test') {
        // Boost difficult questions for practice
        priority += 20
        reason = 'needs_practice'
      }
    }

    return { question_id: questionId, priority, reason }
  }

  /**
   * Select optimal questions for a quiz/test
   */
  async selectOptimalQuestions(
    userId: string,
    availableQuestions: any[],
    count: number,
    phase: 'pre-quiz' | 'test'
  ): Promise<any[]> {
    // Get user's history with all available questions
    const questionIds = availableQuestions.map(q => q.id)
    const historyMap = await this.getUserQuestionHistory(userId, questionIds)

    // Calculate priorities
    const prioritizedQuestions = availableQuestions.map(question => {
      const history = historyMap.get(question.id)
      const priority = this.calculateQuestionPriority(question.id, history, phase)
      
      return {
        question,
        ...priority
      }
    })

    // Sort by priority (highest first) and select top N
    prioritizedQuestions.sort((a, b) => b.priority - a.priority)
    
    // Log selection reasoning (for debugging)
    console.log('Question selection:', prioritizedQuestions.slice(0, count).map(q => ({
      id: q.question.id,
      priority: q.priority,
      reason: q.reason
    })))

    return prioritizedQuestions.slice(0, count).map(p => p.question)
  }

  /**
   * Get learning analytics for a user
   */
  async getUserLearningAnalytics(userId: string): Promise<any> {
    try {
      const { data: attempts, error: attemptsError } = await supabase
        .from('user_question_attempts')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false })
        .limit(100)

      if (attemptsError) throw attemptsError

      // Calculate analytics
      const totalAttempts = attempts?.length || 0
      const correctAttempts = attempts?.filter(a => a.is_correct).length || 0
      const averageTime = attempts?.reduce((sum, a) => sum + a.time_taken_seconds, 0) / totalAttempts || 0

      // Calculate improvement trend (compare first 25% to last 25%)
      const quarterSize = Math.floor(totalAttempts / 4)
      const earlyAttempts = attempts?.slice(-quarterSize) || []
      const recentAttempts = attempts?.slice(0, quarterSize) || []
      
      const earlyAccuracy = earlyAttempts.filter(a => a.is_correct).length / earlyAttempts.length || 0
      const recentAccuracy = recentAttempts.filter(a => a.is_correct).length / recentAttempts.length || 0
      const improvementTrend = recentAccuracy - earlyAccuracy

      // Identify problem areas (questions frequently answered incorrectly)
      const { data: tracking } = await supabase
        .from('user_question_tracking')
        .select('*')
        .eq('user_id', userId)
        .gt('incorrect_count', 0)
        .order('incorrect_count', { ascending: false })
        .limit(10)

      return {
        totalAttempts,
        accuracy: totalAttempts > 0 ? (correctAttempts / totalAttempts) * 100 : 0,
        averageTimePerQuestion: averageTime,
        improvementTrend: improvementTrend * 100,
        problemAreas: tracking || [],
        recentActivity: attempts?.slice(0, 10) || []
      }
    } catch (error) {
      console.error('Error fetching analytics:', error)
      return null
    }
  }
}

export const questionTrackingService = new QuestionTrackingService()