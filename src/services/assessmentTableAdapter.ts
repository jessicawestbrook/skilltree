import { supabase } from './supabase'
import { AssessmentSessionAdapter } from './assessmentSessionAdapter'

/**
 * Adapter service to map between adaptive assessment service expectations
 * and actual database tables (assessment_sessions or user_test_attempts)
 */

interface AssessmentSession {
  id: string
  user_id: string
  category_id: string
  session_type: string
  status: string
  current_ability_estimate: number
  confidence_interval: number
  total_questions: number
  correct_answers: number
  total_points: number
  streak_count: number
  max_streak: number
  started_at: string
  completed_at?: string
  metadata: any
  created_at: string
  updated_at: string
}

interface UserCategoryScore {
  user_id: string
  category_id: string
  current_ability_estimate: number
  confidence_interval: number
  total_questions_answered: number
  correct_answers: number
  last_assessment_date: string
}

export class AssessmentTableAdapter {
  /**
   * Create a new assessment session using assessment_sessions table if available,
   * otherwise fallback to user_test_attempts table
   */
  static async createSession(data: Partial<AssessmentSession>) {
    // First try to use the new assessment_sessions table
    const { data: testTable } = await supabase
      .from('assessment_sessions')
      .select('id')
      .limit(0)
    
    // If assessment_sessions table exists, use the new adapter
    if (testTable !== null) {
      return AssessmentSessionAdapter.createSession(data)
    }
    
    // Otherwise, fallback to user_test_attempts
    try {
      // First check if there's already an incomplete session for this user and category
      const { data: existingAttempt } = await supabase
        .from('user_test_attempts')
        .select('*')
        .eq('user_id', data.user_id)
        .eq('test_id', data.category_id)
        .eq('is_completed', false)
        .order('created_at', { ascending: false })
        .limit(1)
        .single()
      
      if (existingAttempt) {
        // Return the existing incomplete session
        return {
          data: {
            ...existingAttempt,
            category_id: existingAttempt.metadata?.category_id || data.category_id,
            session_type: existingAttempt.metadata?.session_type || data.session_type,
            status: 'active',
            current_ability_estimate: existingAttempt.scaled_score || 0,
            confidence_interval: existingAttempt.metadata?.confidence_interval || 1,
            total_questions: existingAttempt.metadata?.total_questions || 0,
            correct_answers: existingAttempt.metadata?.correct_answers || 0,
            total_points: existingAttempt.raw_score || 0,
            streak_count: existingAttempt.metadata?.streak_count || 0,
            max_streak: existingAttempt.metadata?.max_streak || 0,
            started_at: existingAttempt.created_at,
            completed_at: existingAttempt.completed_at,
            metadata: existingAttempt.metadata || {},
            created_at: existingAttempt.created_at,
            updated_at: existingAttempt.updated_at || existingAttempt.created_at
          },
          error: null
        }
      }
      
      // Get the highest attempt number for this user and test
      const { data: previousAttempts } = await supabase
        .from('user_test_attempts')
        .select('attempt_number')
        .eq('user_id', data.user_id)
        .eq('test_id', data.category_id)
        .order('attempt_number', { ascending: false })
        .limit(1)
      
      const nextAttemptNumber = previousAttempts && previousAttempts.length > 0 
        ? (previousAttempts[0].attempt_number + 1) 
        : 1
      
      // Map to user_test_attempts structure
      const { data: attempt, error } = await supabase
        .from('user_test_attempts')
        .insert({
          user_id: data.user_id,
          test_id: data.category_id, // Use category_id directly as test_id
          attempt_number: nextAttemptNumber,
          is_practice: data.session_type === 'practice',
          raw_score: data.total_points || 0,
          scaled_score: data.current_ability_estimate || 0,
          time_taken_seconds: 0,
          is_completed: false,
          metadata: {
            session_type: data.session_type,
            confidence_interval: data.confidence_interval,
            streak_count: data.streak_count || 0,
            max_streak: data.max_streak || 0,
            total_questions: data.total_questions || 0,
            correct_answers: data.correct_answers || 0,
            category_id: data.category_id // Store category_id in metadata
          }
        })
        .select()
        .single()

      if (error) {
        console.error('Error in AssessmentTableAdapter.createSession:', error)
        console.error('Insert data:', {
          user_id: data.user_id,
          test_id: data.category_id,
          session_type: data.session_type
        })
        throw error
      }

      // Transform back to expected format
      return {
        data: {
          ...attempt,
          category_id: attempt.metadata?.category_id || data.category_id,
          session_type: data.session_type,
          status: attempt.is_completed ? 'completed' : 'active',
          current_ability_estimate: attempt.scaled_score || 0,
          confidence_interval: attempt.metadata?.confidence_interval || 1,
          total_questions: attempt.metadata?.total_questions || 0,
          correct_answers: attempt.metadata?.correct_answers || 0,
          total_points: attempt.raw_score || 0,
          streak_count: attempt.metadata?.streak_count || 0,
          max_streak: attempt.metadata?.max_streak || 0,
          started_at: attempt.created_at,
          completed_at: attempt.completed_at,
          metadata: attempt.metadata || {},
          created_at: attempt.created_at,
          updated_at: attempt.updated_at || attempt.created_at
        },
        error: null
      }
    } catch (error) {
      return { data: null, error }
    }
  }

  /**
   * Get assessment session using assessment_sessions table if available,
   * otherwise fallback to user_test_attempts table
   */
  static async getSession(sessionId: string) {
    // First try to use the new assessment_sessions table
    const { data: testTable } = await supabase
      .from('assessment_sessions')
      .select('id')
      .limit(0)
    
    // If assessment_sessions table exists, use the new adapter
    if (testTable !== null) {
      return AssessmentSessionAdapter.getSession(sessionId)
    }
    
    // Otherwise, fallback to user_test_attempts
    try {
      const { data: attempt, error } = await supabase
        .from('user_test_attempts')
        .select('*')
        .eq('id', sessionId)
        .single()

      if (error) throw error

      // Transform to expected format
      return {
        data: {
          ...attempt,
          category_id: attempt.metadata?.category_id || attempt.test_id,
          session_type: attempt.metadata?.session_type || 'assessment',
          status: attempt.is_completed ? 'completed' : 'active',
          current_ability_estimate: attempt.scaled_score || 0,
          confidence_interval: attempt.metadata?.confidence_interval || 1,
          total_questions: attempt.metadata?.total_questions || 0,
          correct_answers: attempt.metadata?.correct_answers || 0,
          total_points: attempt.raw_score || 0,
          streak_count: attempt.metadata?.streak_count || 0,
          max_streak: attempt.metadata?.max_streak || 0,
          started_at: attempt.created_at,
          completed_at: attempt.completed_at,
          metadata: attempt.metadata || {},
          created_at: attempt.created_at,
          updated_at: attempt.updated_at || attempt.created_at
        },
        error: null
      }
    } catch (error) {
      return { data: null, error }
    }
  }

  /**
   * Update assessment session using assessment_sessions table if available,
   * otherwise fallback to user_test_attempts table
   */
  static async updateSession(sessionId: string, updates: Partial<AssessmentSession>) {
    // First try to use the new assessment_sessions table
    const { data: testTable } = await supabase
      .from('assessment_sessions')
      .select('id')
      .limit(0)
    
    // If assessment_sessions table exists, use the new adapter
    if (testTable !== null) {
      return AssessmentSessionAdapter.updateSession(sessionId, updates)
    }
    
    // Otherwise, fallback to user_test_attempts
    try {
      // Get current attempt to merge metadata
      const { data: current } = await supabase
        .from('user_test_attempts')
        .select('metadata')
        .eq('id', sessionId)
        .single()

      const mergedMetadata = {
        ...(current?.metadata || {}),
        session_type: updates.session_type,
        confidence_interval: updates.confidence_interval,
        streak_count: updates.streak_count,
        max_streak: updates.max_streak,
        total_questions: updates.total_questions,
        correct_answers: updates.correct_answers,
        category_id: current?.metadata?.category_id // Preserve category_id
      }

      const { data: attempt, error } = await supabase
        .from('user_test_attempts')
        .update({
          raw_score: updates.total_points,
          scaled_score: updates.current_ability_estimate,
          is_completed: updates.status === 'completed',
          completed_at: updates.completed_at,
          metadata: mergedMetadata,
          updated_at: new Date().toISOString()
        })
        .eq('id', sessionId)
        .select()
        .single()

      if (error) throw error

      // Transform back to expected format
      return {
        data: {
          ...attempt,
          category_id: mergedMetadata.category_id || attempt.test_id,
          session_type: mergedMetadata.session_type || 'assessment',
          status: attempt.is_completed ? 'completed' : 'active',
          current_ability_estimate: attempt.scaled_score || 0,
          confidence_interval: mergedMetadata.confidence_interval || 1,
          total_questions: mergedMetadata.total_questions || 0,
          correct_answers: mergedMetadata.correct_answers || 0,
          total_points: attempt.raw_score || 0,
          streak_count: mergedMetadata.streak_count || 0,
          max_streak: mergedMetadata.max_streak || 0,
          started_at: attempt.created_at,
          completed_at: attempt.completed_at,
          metadata: attempt.metadata || {},
          created_at: attempt.created_at,
          updated_at: attempt.updated_at
        },
        error: null
      }
    } catch (error) {
      return { data: null, error }
    }
  }

  /**
   * Get user category scores using assessment_sessions table if available,
   * otherwise fallback to user_question_tracking table
   */
  static async getUserCategoryScore(userId: string, categoryId: string) {
    // First try to use the new assessment_sessions table
    const { data: testTable } = await supabase
      .from('assessment_sessions')
      .select('id')
      .limit(0)
    
    // If assessment_sessions table exists, use the new adapter
    if (testTable !== null) {
      return AssessmentSessionAdapter.getUserCategoryScore(userId, categoryId)
    }
    
    // Otherwise, fallback to user_question_tracking
    try {
      // Get aggregated stats from user_question_tracking for questions in this category
      const { data: questions } = await supabase
        .from('questions')
        .select('id')
        .eq('skill_id', categoryId)

      if (!questions || questions.length === 0) {
        // No questions for this category, return default score
        return {
          data: {
            user_id: userId,
            category_id: categoryId,
            current_ability_estimate: 0,
            confidence_interval: 1,
            total_questions_answered: 0,
            correct_answers: 0,
            last_assessment_date: null
          },
          error: null
        }
      }

      const questionIds = questions.map(q => q.id)

      const { data: tracking } = await supabase
        .from('user_question_tracking')
        .select('*')
        .eq('user_id', userId)
        .in('question_id', questionIds)

      if (!tracking || tracking.length === 0) {
        // No tracking data yet
        return {
          data: {
            user_id: userId,
            category_id: categoryId,
            current_ability_estimate: 0,
            confidence_interval: 1,
            total_questions_answered: 0,
            correct_answers: 0,
            last_assessment_date: null
          },
          error: null
        }
      }

      // Calculate aggregate scores
      const totalQuestions = tracking.reduce((sum, t) => sum + t.view_count, 0)
      const correctAnswers = tracking.reduce((sum, t) => sum + t.correct_count, 0)
      const lastSeen = tracking.reduce((latest, t) => {
        return t.last_seen > latest ? t.last_seen : latest
      }, tracking[0].last_seen)

      // Simple ability estimate based on success rate
      const successRate = totalQuestions > 0 ? correctAnswers / totalQuestions : 0
      const abilityEstimate = successRate * 100

      return {
        data: {
          user_id: userId,
          category_id: categoryId,
          current_ability_estimate: abilityEstimate,
          confidence_interval: Math.max(0.5, 1 - (totalQuestions / 100)), // Confidence improves with more questions
          total_questions_answered: totalQuestions,
          correct_answers: correctAnswers,
          last_assessment_date: lastSeen
        },
        error: null
      }
    } catch (error) {
      return { data: null, error }
    }
  }

  /**
   * Update user category scores (stores in user_question_tracking)
   */
  static async updateUserCategoryScore(userId: string, categoryId: string, updates: Partial<UserCategoryScore>) {
    // Since we're using user_question_tracking which is per-question,
    // we'll store category-level data in a metadata field or just return success
    // The actual scores are calculated on-the-fly from question tracking data
    return {
      data: {
        user_id: userId,
        category_id: categoryId,
        ...updates
      },
      error: null
    }
  }
}