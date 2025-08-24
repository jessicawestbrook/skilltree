import { supabase } from './supabase'

export interface QuizQuestion {
  id: string
  question_text: string
  question_type: 'multiple_choice' | 'scale' | 'text' | 'multi_select'
  category: string | null
  options: any
  display_order: number
  parent_question_id?: string | null
  condition_type?: 'contains' | 'equals' | 'greater_than' | 'selected' | null
  condition_value?: any
  is_follow_up?: boolean
}

export interface QuizResponse {
  id: string
  user_id: string
  quiz_version: number
  started_at: string
  completed_at: string | null
  is_complete: boolean
  metadata?: any
}

export interface QuizAnswer {
  id: string
  response_id: string
  question_id: string
  answer_value: string
  answer_metadata?: any
  answered_at: string
}

export interface UserInterest {
  id: string
  user_id: string
  interest_category: string
  interest_level: number
  confidence_score: number
  source: string
}

class InterestsQuizService {
  /**
   * Get primary quiz questions (not follow-ups)
   */
  async getPrimaryQuizQuestions(): Promise<QuizQuestion[]> {
    const { data, error } = await supabase
      .from('interests_quiz_questions')
      .select('*')
      .eq('is_active', true)
      .or('is_follow_up.is.false,is_follow_up.is.null')
      .order('display_order', { ascending: true })

    if (error) {
      console.error('Error fetching quiz questions:', error)
      return []
    }

    return data || []
  }

  /**
   * Get all active quiz questions including follow-ups
   */
  async getAllQuizQuestions(): Promise<QuizQuestion[]> {
    const { data, error } = await supabase
      .from('interests_quiz_questions')
      .select('*')
      .eq('is_active', true)
      .order('display_order', { ascending: true })

    if (error) {
      console.error('Error fetching quiz questions:', error)
      return []
    }

    return data || []
  }

  /**
   * Get follow-up questions based on an answer
   */
  async getFollowUpQuestions(
    parentQuestionId: string,
    answerValue: string | string[] | number
  ): Promise<QuizQuestion[]> {
    // Convert answer to string for database function
    let answerString: string
    if (Array.isArray(answerValue)) {
      answerString = JSON.stringify(answerValue)
    } else {
      answerString = String(answerValue)
    }

    const { data, error } = await supabase
      .rpc('get_follow_up_questions', {
        p_parent_id: parentQuestionId,
        p_answer_value: answerString
      })

    if (error) {
      console.error('Error fetching follow-up questions:', error)
      return []
    }

    return data || []
  }

  /**
   * Check if an answer triggers follow-up questions
   */
  async hasFollowUpQuestions(
    parentQuestionId: string,
    answerValue: string | string[] | number
  ): Promise<boolean> {
    const followUps = await this.getFollowUpQuestions(parentQuestionId, answerValue)
    return followUps.length > 0
  }

  /**
   * Start a new quiz session for a user
   */
  async startQuizSession(userId: string): Promise<QuizResponse | null> {
    const { data, error } = await supabase
      .from('interests_quiz_responses')
      .insert({
        user_id: userId,
        started_at: new Date().toISOString()
      })
      .select()
      .single()

    if (error) {
      console.error('Error starting quiz session:', error)
      return null
    }

    return data
  }

  /**
   * Save an answer for a quiz question
   */
  async saveAnswer(
    responseId: string,
    questionId: string,
    answerValue: string | string[],
    metadata?: any
  ): Promise<boolean> {
    // Convert array answers to JSON string for multi-select
    const value = Array.isArray(answerValue) 
      ? JSON.stringify(answerValue) 
      : answerValue

    const { error } = await supabase
      .from('interests_quiz_answers')
      .upsert({
        response_id: responseId,
        question_id: questionId,
        answer_value: value,
        answer_metadata: metadata,
        answered_at: new Date().toISOString()
      })

    if (error) {
      console.error('Error saving answer:', error)
      return false
    }

    return true
  }

  /**
   * Save multiple answers at once
   */
  async saveAnswers(
    responseId: string,
    answers: Array<{
      questionId: string
      answerValue: string | string[]
      metadata?: any
    }>
  ): Promise<boolean> {
    const formattedAnswers = answers.map(answer => ({
      response_id: responseId,
      question_id: answer.questionId,
      answer_value: Array.isArray(answer.answerValue) 
        ? JSON.stringify(answer.answerValue) 
        : answer.answerValue,
      answer_metadata: answer.metadata,
      answered_at: new Date().toISOString()
    }))

    const { error } = await supabase
      .from('interests_quiz_answers')
      .upsert(formattedAnswers)

    if (error) {
      console.error('Error saving answers:', error)
      return false
    }

    return true
  }

  /**
   * Complete a quiz session
   */
  async completeQuizSession(responseId: string): Promise<boolean> {
    const { error } = await supabase
      .from('interests_quiz_responses')
      .update({
        completed_at: new Date().toISOString(),
        is_complete: true
      })
      .eq('id', responseId)

    if (error) {
      console.error('Error completing quiz session:', error)
      return false
    }

    // The trigger will automatically compute interests
    return true
  }

  /**
   * Get user's latest quiz response
   */
  async getLatestUserResponse(userId: string): Promise<QuizResponse | null> {
    const { data, error } = await supabase
      .from('interests_quiz_responses')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(1)
      .single()

    if (error) {
      console.error('Error fetching user response:', error)
      return null
    }

    return data
  }

  /**
   * Get answers for a quiz response
   */
  async getResponseAnswers(responseId: string): Promise<QuizAnswer[]> {
    const { data, error } = await supabase
      .from('interests_quiz_answers')
      .select('*')
      .eq('response_id', responseId)

    if (error) {
      console.error('Error fetching answers:', error)
      return []
    }

    return data || []
  }

  /**
   * Get user's interests
   */
  async getUserInterests(userId: string): Promise<UserInterest[]> {
    const { data, error } = await supabase
      .from('user_interests')
      .select('*')
      .eq('user_id', userId)
      .order('interest_level', { ascending: false })

    if (error) {
      console.error('Error fetching user interests:', error)
      return []
    }

    return data || []
  }

  /**
   * Check if user has completed interests quiz
   */
  async hasCompletedQuiz(userId: string): Promise<boolean> {
    const { data, error } = await supabase
      .from('interests_quiz_responses')
      .select('id')
      .eq('user_id', userId)
      .eq('is_complete', true)
      .limit(1)

    if (error) {
      console.error('Error checking quiz completion:', error)
      return false
    }

    return data && data.length > 0
  }

  /**
   * Get or resume quiz session
   */
  async getOrCreateQuizSession(userId: string): Promise<{
    response: QuizResponse
    answers: QuizAnswer[]
    isNew: boolean
  } | null> {
    // Check for incomplete session
    const { data: incompleteSession } = await supabase
      .from('interests_quiz_responses')
      .select('*')
      .eq('user_id', userId)
      .eq('is_complete', false)
      .order('created_at', { ascending: false })
      .limit(1)
      .single()

    if (incompleteSession) {
      const answers = await this.getResponseAnswers(incompleteSession.id)
      return {
        response: incompleteSession,
        answers,
        isNew: false
      }
    }

    // Create new session
    const newSession = await this.startQuizSession(userId)
    if (!newSession) return null

    return {
      response: newSession,
      answers: [],
      isNew: true
    }
  }

  /**
   * Update user interests based on behavior (not quiz)
   */
  async updateInterestFromBehavior(
    userId: string,
    category: string,
    delta: number,
    source: string = 'behavior'
  ): Promise<boolean> {
    // Get current interest level
    const { data: currentInterest } = await supabase
      .from('user_interests')
      .select('interest_level, confidence_score')
      .eq('user_id', userId)
      .eq('interest_category', category)
      .eq('source', source)
      .single()

    const currentLevel = (currentInterest as any)?.interest_level || 0.5
    const currentConfidence = (currentInterest as any)?.confidence_score || 0.5
    const newLevel = Math.max(0, Math.min(1, currentLevel + delta))

    const { error } = await supabase
      .from('user_interests')
      .upsert({
        user_id: userId,
        interest_category: category,
        interest_level: newLevel,
        confidence_score: Math.min(1, currentConfidence + 0.05),
        source,
        updated_at: new Date().toISOString()
      })

    if (error) {
      console.error('Error updating interest:', error)
      return false
    }

    return true
  }
}

export const interestsQuizService = new InterestsQuizService()