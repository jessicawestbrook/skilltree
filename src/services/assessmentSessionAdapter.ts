import { supabase } from './supabase'

/**
 * Adapter service for the new assessment_sessions table
 * This replaces the assessmentTableAdapter when assessment_sessions table is available
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
  highest_difficulty_reached: number
  started_at: string
  completed_at?: string
  metadata: any
  created_at: string
  updated_at: string
}

interface QuestionResponse {
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

export class AssessmentSessionAdapter {
  /**
   * Create a new assessment session
   */
  static async createSession(data: Partial<AssessmentSession>) {
    try {
      // First check if there's already an incomplete session for this user and category
      const { data: existingSession } = await supabase
        .from('assessment_sessions')
        .select('*')
        .eq('user_id', data.user_id)
        .eq('category_id', data.category_id)
        .eq('status', 'active')
        .order('created_at', { ascending: false })
        .limit(1)
        .single()
      
      if (existingSession) {
        // Return the existing incomplete session
        return { data: existingSession, error: null }
      }
      
      // Create new session
      const { data: session, error } = await supabase
        .from('assessment_sessions')
        .insert({
          user_id: data.user_id,
          category_id: data.category_id,
          session_type: data.session_type || 'assessment',
          status: 'active',
          current_ability_estimate: data.current_ability_estimate || 0,
          confidence_interval: data.confidence_interval || 1,
          total_questions: 0,
          correct_answers: 0,
          total_points: 0,
          streak_count: 0,
          max_streak: 0,
          highest_difficulty_reached: 0,
          metadata: data.metadata || {}
        })
        .select()
        .single()

      if (error) {
        console.error('Error creating assessment session:', error)
        throw error
      }

      return { data: session, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  /**
   * Get assessment session by ID
   */
  static async getSession(sessionId: string) {
    try {
      const { data: session, error } = await supabase
        .from('assessment_sessions')
        .select('*')
        .eq('id', sessionId)
        .single()

      if (error) throw error
      return { data: session, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  /**
   * Update assessment session
   */
  static async updateSession(sessionId: string, updates: Partial<AssessmentSession>) {
    try {
      const { data: session, error } = await supabase
        .from('assessment_sessions')
        .update({
          ...updates,
          updated_at: new Date().toISOString()
        })
        .eq('id', sessionId)
        .select()
        .single()

      if (error) throw error
      return { data: session, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  /**
   * Complete an assessment session
   */
  static async completeSession(sessionId: string) {
    try {
      const { data: session, error } = await supabase
        .from('assessment_sessions')
        .update({
          status: 'completed',
          completed_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        })
        .eq('id', sessionId)
        .select()
        .single()

      if (error) throw error
      return { data: session, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  /**
   * Record a question response
   */
  static async recordResponse(response: Partial<QuestionResponse>) {
    try {
      // Get the session to get user_id
      const { data: session } = await supabase
        .from('assessment_sessions')
        .select('user_id')
        .eq('id', response.session_id)
        .single()
      
      if (!session) throw new Error('Session not found')

      const { data: questionResponse, error } = await supabase
        .from('user_question_responses')
        .insert({
          user_id: session.user_id,
          session_id: response.session_id,
          question_id: response.question_id,
          selected_answer: response.user_response,
          is_correct: response.is_correct,
          time_spent_seconds: Math.round((response.response_time_ms || 0) / 1000),
          question_sequence: response.question_sequence,
          context_type: 'assessment',
          response_metadata: {
            difficulty_level: response.difficulty_level,
            points_earned: response.points_earned || 0,
            point_multipliers: response.point_multipliers || {}
          }
        })
        .select()
        .single()

      if (error) throw error
      return { data: questionResponse, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  /**
   * Get all responses for a session
   */
  static async getSessionResponses(sessionId: string) {
    try {
      const { data: responses, error } = await supabase
        .from('user_question_responses')
        .select('*')
        .eq('session_id', sessionId)
        .eq('context_type', 'assessment')
        .order('question_sequence', { ascending: true })

      if (error) throw error
      return { data: responses || [], error: null }
    } catch (error) {
      return { data: [], error }
    }
  }

  /**
   * Get user category scores (aggregated from completed sessions)
   */
  static async getUserCategoryScore(userId: string, categoryId: string) {
    try {
      // Get all completed sessions for this user and category
      const { data: sessions, error } = await supabase
        .from('assessment_sessions')
        .select('*')
        .eq('user_id', userId)
        .eq('category_id', categoryId)
        .eq('status', 'completed')
        .order('completed_at', { ascending: false })

      if (error) throw error

      if (!sessions || sessions.length === 0) {
        // No completed sessions yet
        return {
          data: {
            user_id: userId,
            category_id: categoryId,
            current_ability_estimate: 0,
            confidence_interval: 1,
            total_questions_answered: 0,
            correct_answers: 0,
            total_points: 0,
            best_session_points: 0,
            sessions_completed: 0,
            last_assessment_date: null,
            mastery_level: 0,
            achievement_badges: []
          },
          error: null
        }
      }

      // Calculate aggregate scores
      const latestSession = sessions[0]
      const totalQuestions = sessions.reduce((sum, s) => sum + s.total_questions, 0)
      const correctAnswers = sessions.reduce((sum, s) => sum + s.correct_answers, 0)
      const totalPoints = sessions.reduce((sum, s) => sum + s.total_points, 0)
      const bestPoints = Math.max(...sessions.map(s => s.total_points))

      return {
        data: {
          user_id: userId,
          category_id: categoryId,
          current_ability_estimate: latestSession.current_ability_estimate,
          confidence_interval: latestSession.confidence_interval,
          total_questions_answered: totalQuestions,
          correct_answers: correctAnswers,
          total_points: totalPoints,
          best_session_points: bestPoints,
          sessions_completed: sessions.length,
          last_assessment_date: latestSession.completed_at,
          mastery_level: Math.min(5, Math.ceil(latestSession.current_ability_estimate)),
          achievement_badges: []
        },
        error: null
      }
    } catch (error) {
      return { data: null, error }
    }
  }
}