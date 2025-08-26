import { supabase } from './supabase'

export interface DeckItem {
  id: string
  user_id: string
  vocabulary_id?: string
  question_id?: string
  language?: string
  language_id?: string
  deck_status: 'learning' | 'review' | 'mastered'
  consecutive_correct: number
  total_reviews: number
  times_incorrect: number
  last_reviewed_at: string | null
  promoted_to_review_at: string | null
  mastered_at: string | null
  ease_factor: number
  interval_days: number
  next_review_date: string
}

export interface DeckStats {
  learning: number
  review: number
  mastered: number
  dueToday: number
}

// Note: Thresholds for progression are handled by database triggers
// Learning -> Review: 3 consecutive correct
// Review -> Mastered: 5 consecutive correct

export class DeckProgressionService {
  /**
   * Add a vocabulary word to the learning deck
   */
  static async addVocabularyToDeck(
    userId: string,
    vocabularyId: string,
    language: string
  ): Promise<{ success: boolean; message?: string }> {
    try {
      const { error } = await supabase
        .from('user_vocabulary_decks')
        .insert({
          user_id: userId,
          vocabulary_id: vocabularyId,
          language: language,
          deck_status: 'learning',
          consecutive_correct: 0,
          total_reviews: 0,
          times_incorrect: 0
        })
        .single()

      if (error) {
        if (error.code === '23505') { // Duplicate key error
          return { success: true, message: 'Already in your learning deck' }
        }
        throw error
      }

      return { success: true, message: 'Added to learning deck!' }
    } catch (error) {
      console.error('Error adding to deck:', error)
      return { success: false, message: 'Failed to add to deck' }
    }
  }

  /**
   * Add a grammar question to the learning deck
   */
  static async addGrammarToDeck(
    userId: string,
    questionId: string,
    languageId: string
  ): Promise<{ success: boolean; message?: string }> {
    try {
      const { error } = await supabase
        .from('user_grammar_decks')
        .insert({
          user_id: userId,
          question_id: questionId,
          language_id: languageId,
          deck_status: 'learning',
          consecutive_correct: 0,
          total_reviews: 0,
          times_incorrect: 0
        })
        .single()

      if (error) {
        if (error.code === '23505') { // Duplicate key error
          return { success: true, message: 'Already in your learning deck' }
        }
        throw error
      }

      return { success: true, message: 'Added to learning deck!' }
    } catch (error) {
      console.error('Error adding to deck:', error)
      return { success: false, message: 'Failed to add to deck' }
    }
  }

  /**
   * Record a review result for vocabulary and update deck status
   */
  static async recordVocabularyReview(
    userId: string,
    vocabularyId: string,
    difficulty: 'easy' | 'medium' | 'hard'
  ): Promise<{ success: boolean; newStatus?: string; message?: string }> {
    try {
      // Get current item
      const { data: item, error: fetchError } = await supabase
        .from('user_vocabulary_decks')
        .select('*')
        .eq('user_id', userId)
        .eq('vocabulary_id', vocabularyId)
        .single()

      if (fetchError || !item) {
        return { success: false, message: 'Item not found in deck' }
      }

      const isCorrect = difficulty === 'easy' || difficulty === 'medium'
      const consecutiveCorrect = isCorrect 
        ? item.consecutive_correct + 1 
        : 0
      const totalReviews = item.total_reviews + 1
      const timesIncorrect = !isCorrect ? item.times_incorrect + 1 : item.times_incorrect

      // Calculate new ease factor and interval for spaced repetition
      let easeFactor = item.ease_factor
      let intervalDays = item.interval_days

      if (difficulty === 'easy') {
        easeFactor = Math.min(easeFactor + 0.15, 2.5)
        intervalDays = Math.ceil(intervalDays * easeFactor)
      } else if (difficulty === 'medium') {
        intervalDays = Math.ceil(intervalDays * 1.3)
      } else { // hard
        easeFactor = Math.max(easeFactor - 0.2, 1.3)
        intervalDays = 1
      }

      // Calculate next review date
      const nextReviewDate = new Date()
      nextReviewDate.setDate(nextReviewDate.getDate() + intervalDays)

      // Update the item
      const { data: updatedItem, error: updateError } = await supabase
        .from('user_vocabulary_decks')
        .update({
          consecutive_correct: consecutiveCorrect,
          total_reviews: totalReviews,
          times_incorrect: timesIncorrect,
          last_reviewed_at: new Date().toISOString(),
          ease_factor: easeFactor,
          interval_days: intervalDays,
          next_review_date: nextReviewDate.toISOString().split('T')[0]
        })
        .eq('user_id', userId)
        .eq('vocabulary_id', vocabularyId)
        .select()
        .single()

      if (updateError) {
        return { success: false, message: 'Failed to update progress' }
      }

      // Check if status changed (handled by database trigger)
      let message = ''
      if (updatedItem.deck_status !== item.deck_status) {
        if (updatedItem.deck_status === 'review') {
          message = '🎉 Card promoted to Review deck!'
        } else if (updatedItem.deck_status === 'mastered') {
          message = '🌟 Card mastered! Excellent work!'
        } else if (updatedItem.deck_status === 'learning') {
          message = '📚 Card moved back to Learning deck for more practice'
        }
      }

      return { success: true, newStatus: updatedItem.deck_status, message }
    } catch (error) {
      console.error('Error recording review:', error)
      return { success: false, message: 'An error occurred' }
    }
  }

  /**
   * Record a review result for grammar and update deck status
   */
  static async recordGrammarReview(
    userId: string,
    questionId: string,
    isCorrect: boolean
  ): Promise<{ success: boolean; newStatus?: string; message?: string }> {
    try {
      // Get current item
      const { data: item, error: fetchError } = await supabase
        .from('user_grammar_decks')
        .select('*')
        .eq('user_id', userId)
        .eq('question_id', questionId)
        .single()

      if (fetchError || !item) {
        return { success: false, message: 'Item not found in deck' }
      }

      const consecutiveCorrect = isCorrect 
        ? item.consecutive_correct + 1 
        : 0
      const totalReviews = item.total_reviews + 1
      const timesIncorrect = !isCorrect ? item.times_incorrect + 1 : item.times_incorrect

      // Calculate new ease factor and interval
      let easeFactor = item.ease_factor
      let intervalDays = item.interval_days

      if (isCorrect) {
        easeFactor = Math.min(easeFactor + 0.15, 2.5)
        intervalDays = Math.ceil(intervalDays * easeFactor)
      } else {
        easeFactor = Math.max(easeFactor - 0.2, 1.3)
        intervalDays = 1
      }

      // Calculate next review date
      const nextReviewDate = new Date()
      nextReviewDate.setDate(nextReviewDate.getDate() + intervalDays)

      // Update the item
      const { data: updatedItem, error: updateError } = await supabase
        .from('user_grammar_decks')
        .update({
          consecutive_correct: consecutiveCorrect,
          total_reviews: totalReviews,
          times_incorrect: timesIncorrect,
          last_reviewed_at: new Date().toISOString(),
          ease_factor: easeFactor,
          interval_days: intervalDays,
          next_review_date: nextReviewDate.toISOString().split('T')[0]
        })
        .eq('user_id', userId)
        .eq('question_id', questionId)
        .select()
        .single()

      if (updateError) {
        return { success: false, message: 'Failed to update progress' }
      }

      // Check if status changed
      let message = ''
      if (updatedItem.deck_status !== item.deck_status) {
        if (updatedItem.deck_status === 'review') {
          message = '🎉 Card promoted to Review deck!'
        } else if (updatedItem.deck_status === 'mastered') {
          message = '🌟 Card mastered! Excellent work!'
        } else if (updatedItem.deck_status === 'learning') {
          message = '📚 Card moved back to Learning deck for more practice'
        }
      }

      return { success: true, newStatus: updatedItem.deck_status, message }
    } catch (error) {
      console.error('Error recording review:', error)
      return { success: false, message: 'An error occurred' }
    }
  }

  /**
   * Get vocabulary cards filtered by deck status
   */
  static async getVocabularyDeck(
    userId: string,
    language: string,
    deckStatus?: 'learning' | 'review' | 'mastered' | 'all'
  ) {
    try {
      let query = supabase
        .from('user_vocabulary_decks')
        .select(`
          *,
          vocabulary:language_vocabulary!user_vocabulary_decks_vocabulary_id_fkey (
            id,
            language,
            word,
            english_translation,
            pronunciation_guide,
            part_of_speech,
            definition_english,
            example_sentence,
            example_sentence_translation,
            memory_tips,
            difficulty_id,
            zipf_frequency
          )
        `)
        .eq('user_id', userId)
        .eq('language', language)

      if (deckStatus && deckStatus !== 'all') {
        query = query.eq('deck_status', deckStatus)
      }

      // Prioritize cards due for review
      const { data, error } = await query
        .lte('next_review_date', new Date().toISOString().split('T')[0])
        .order('next_review_date', { ascending: true })
        .order('last_reviewed_at', { ascending: true, nullsFirst: true })
        .limit(50)

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching vocabulary deck:', error)
      return []
    }
  }

  /**
   * Get grammar cards filtered by deck status
   */
  static async getGrammarDeck(
    userId: string,
    languageId: string,
    deckStatus?: 'learning' | 'review' | 'mastered' | 'all'
  ) {
    try {
      let query = supabase
        .from('user_grammar_decks')
        .select(`
          *,
          question:language_questions!user_grammar_decks_question_id_fkey (
            id,
            language_id,
            question_text,
            question_type,
            options,
            correct_answer,
            correct_answer_index,
            explanation,
            difficulty_level
          )
        `)
        .eq('user_id', userId)
        .eq('language_id', languageId)

      if (deckStatus && deckStatus !== 'all') {
        query = query.eq('deck_status', deckStatus)
      }

      // Prioritize cards due for review
      const { data, error } = await query
        .lte('next_review_date', new Date().toISOString().split('T')[0])
        .order('next_review_date', { ascending: true })
        .order('last_reviewed_at', { ascending: true, nullsFirst: true })
        .limit(50)

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching grammar deck:', error)
      return []
    }
  }

  /**
   * Get deck statistics for a user
   */
  static async getDeckStats(userId: string, language?: string): Promise<DeckStats> {
    try {
      const { data, error } = await supabase
        .rpc('get_user_deck_stats', { 
          p_user_id: userId,
          p_language: language || null
        })

      if (error) throw error

      const stats: DeckStats = {
        learning: 0,
        review: 0,
        mastered: 0,
        dueToday: 0
      }

      if (data) {
        data.forEach((row: any) => {
          switch (row.deck_status) {
            case 'learning':
              stats.learning = row.item_count
              stats.dueToday += row.due_today
              break
            case 'review':
              stats.review = row.item_count
              stats.dueToday += row.due_today
              break
            case 'mastered':
              stats.mastered = row.item_count
              break
          }
        })
      }

      return stats
    } catch (error) {
      console.error('Error fetching deck stats:', error)
      return {
        learning: 0,
        review: 0,
        mastered: 0,
        dueToday: 0
      }
    }
  }

  /**
   * Check if a vocabulary word is in the user's deck
   */
  static async isVocabularyInDeck(
    userId: string,
    vocabularyId: string
  ): Promise<boolean> {
    try {
      const { data, error } = await supabase
        .from('user_vocabulary_decks')
        .select('id')
        .eq('user_id', userId)
        .eq('vocabulary_id', vocabularyId)
        .single()

      return !error && !!data
    } catch (error) {
      return false
    }
  }

  /**
   * Check if a grammar question is in the user's deck
   */
  static async isGrammarInDeck(
    userId: string,
    questionId: string
  ): Promise<boolean> {
    try {
      const { data, error } = await supabase
        .from('user_grammar_decks')
        .select('id')
        .eq('user_id', userId)
        .eq('question_id', questionId)
        .single()

      return !error && !!data
    } catch (error) {
      return false
    }
  }

  /**
   * Remove from deck
   */
  static async removeFromDeck(
    userId: string,
    itemType: 'vocabulary' | 'grammar',
    itemId: string
  ): Promise<{ success: boolean }> {
    try {
      const table = itemType === 'vocabulary' ? 'user_vocabulary_decks' : 'user_grammar_decks'
      const column = itemType === 'vocabulary' ? 'vocabulary_id' : 'question_id'
      
      const { error } = await supabase
        .from(table)
        .delete()
        .eq('user_id', userId)
        .eq(column, itemId)

      return { success: !error }
    } catch (error) {
      console.error('Error removing from deck:', error)
      return { success: false }
    }
  }
}