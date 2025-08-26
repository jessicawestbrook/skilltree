import { supabase } from './supabase'

// Spaced Repetition Algorithm based on SM-2 with modifications for educational context
// References:
// - Ebbinghaus Forgetting Curve (1885)
// - SuperMemo SM-2 Algorithm (Wozniak, 1987)
// - Leitner System principles

export interface FlashcardReview {
  id: string
  user_id: string
  flashcard_id: string
  flashcard_type: 'vocabulary' | 'spelling' | 'language' | 'question' | 'skill_node'
  last_reviewed: string
  next_review: string
  review_count: number
  easiness_factor: number // 1.3 to 2.5, where 2.5 is easiest
  interval_days: number // Days until next review
  consecutive_correct: number
  total_correct: number
  total_attempts: number
  created_at: string
  updated_at: string
}

export interface ReviewSession {
  flashcard: any
  review: FlashcardReview | null
  priority: number
  reason: string
}

export interface ReviewResponse {
  quality: number // 0-5 scale (0=complete blackout, 5=perfect recall)
  time_taken: number // seconds
  hint_used: boolean
}

class SpacedRepetitionService {
  // Default intervals in days based on Leitner system
  private readonly DEFAULT_INTERVALS = [1, 3, 7, 14, 30, 90]
  
  // Minimum easiness factor to prevent infinite difficulty
  private readonly MIN_EASINESS = 1.3
  
  // Maximum easiness factor for very easy items
  private readonly MAX_EASINESS = 2.5
  
  // Hours before a card is considered "due"
  private readonly GRACE_PERIOD_HOURS = 4

  /**
   * Calculate the next review interval using modified SM-2 algorithm
   */
  private calculateNextInterval(
    quality: number, // 0-5 rating
    easinessFactor: number,
    currentInterval: number,
    consecutiveCorrect: number
  ): { interval: number; easiness: number } {
    // Adjust easiness factor based on quality
    // EF' = EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    let newEasiness = easinessFactor
    
    if (quality < 3) {
      // Reset interval for incorrect answers
      return {
        interval: 1,
        easiness: Math.max(this.MIN_EASINESS, easinessFactor - 0.2)
      }
    }
    
    // Calculate new easiness factor for correct answers
    newEasiness = easinessFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    newEasiness = Math.max(this.MIN_EASINESS, Math.min(this.MAX_EASINESS, newEasiness))
    
    // Calculate next interval
    let nextInterval: number
    
    if (consecutiveCorrect === 0) {
      nextInterval = 1
    } else if (consecutiveCorrect === 1) {
      nextInterval = 6
    } else {
      // I(n) = I(n-1) * EF
      nextInterval = Math.round(currentInterval * newEasiness)
    }
    
    // Apply maximum interval cap (6 months)
    nextInterval = Math.min(nextInterval, 180)
    
    return {
      interval: nextInterval,
      easiness: newEasiness
    }
  }

  /**
   * Initialize or get review record for a flashcard
   */
  async getOrCreateReview(
    userId: string,
    flashcardId: string,
    flashcardType: 'vocabulary' | 'spelling' | 'language' | 'question' | 'skill_node'
  ): Promise<FlashcardReview | null> {
    try {
      // Check if review record exists
      const { data: existing, error: fetchError } = await supabase
        .from('user_flashcard_reviews')
        .select('*')
        .eq('user_id', userId)
        .eq('flashcard_id', flashcardId)
        .eq('flashcard_type', flashcardType)
        .single()
      
      // If table doesn't exist, return null gracefully
      if (fetchError?.code === '42P01') {
        console.warn('user_flashcard_reviews table not found. Please run the migration script.')
        return null
      }
      
      if (existing) {
        return existing as FlashcardReview
      }
      
      // Create new review record with all columns
      const now = new Date().toISOString()
      const newReview: Partial<FlashcardReview> = {
        user_id: userId,
        flashcard_id: flashcardId,
        flashcard_type: flashcardType,
        last_reviewed: now,
        next_review: now, // Due immediately for new cards
        review_count: 0,
        easiness_factor: 2.5, // Start with default easiness
        interval_days: 0,
        consecutive_correct: 0,
        total_correct: 0,
        total_attempts: 0,
        created_at: now,
        updated_at: now
      }
      
      const { data, error } = await supabase
        .from('user_flashcard_reviews')
        .insert(newReview)
        .select()
        .single()
      
      if (error) {
        // If table doesn't exist, log warning instead of error
        if (error.code === '42P01') {
          console.warn('user_flashcard_reviews table not found. Please run the migration script.')
        } else {
          console.error('Error creating review record:', error)
        }
        return null
      }
      
      return data as FlashcardReview
    } catch (error) {
      console.error('Error in getOrCreateReview:', error)
      return null
    }
  }

  /**
   * Record a review and update scheduling
   */
  async recordReview(
    userId: string,
    flashcardId: string,
    flashcardType: 'vocabulary' | 'spelling' | 'language' | 'question' | 'skill_node',
    response: ReviewResponse
  ): Promise<FlashcardReview | null> {
    try {
      // Get or create review record
      const review = await this.getOrCreateReview(userId, flashcardId, flashcardType)
      if (!review) return null
      
      // Calculate next interval and easiness
      const { interval, easiness } = this.calculateNextInterval(
        response.quality,
        review.easiness_factor,
        review.interval_days,
        review.consecutive_correct
      )
      
      // Calculate next review date
      const nextReviewDate = new Date()
      nextReviewDate.setDate(nextReviewDate.getDate() + interval)
      
      // Update review record with all columns
      const updates: Partial<FlashcardReview> = {
        last_reviewed: new Date().toISOString(),
        next_review: nextReviewDate.toISOString(),
        review_count: review.review_count + 1,
        easiness_factor: easiness,
        interval_days: interval,
        consecutive_correct: response.quality >= 3 
          ? review.consecutive_correct + 1 
          : 0,
        total_correct: response.quality >= 3 
          ? review.total_correct + 1 
          : review.total_correct,
        total_attempts: review.total_attempts + 1,
        updated_at: new Date().toISOString()
      }
      
      const { data, error } = await supabase
        .from('user_flashcard_reviews')
        .update(updates)
        .eq('id', review.id)
        .select()
        .single()
      
      if (error) {
        console.error('Error updating review record:', error)
        return null
      }
      
      // Also record in review history for analytics
      await this.recordReviewHistory(userId, flashcardId, flashcardType, response, interval)
      
      // Create automatic reminder for next review if enabled
      if (response.quality >= 3) { // Only for correct answers
        await this.createNextReviewReminder(userId, flashcardId, flashcardType, interval)
      }
      
      return data as FlashcardReview
    } catch (error) {
      console.error('Error recording review:', error)
      return null
    }
  }

  /**
   * Record review history for analytics
   */
  private async recordReviewHistory(
    userId: string,
    flashcardId: string,
    flashcardType: 'vocabulary' | 'spelling' | 'language' | 'question' | 'skill_node',
    response: ReviewResponse,
    nextInterval: number
  ): Promise<void> {
    try {
      const { error } = await supabase
        .from('flashcard_review_history')
        .insert({
          user_id: userId,
          flashcard_id: flashcardId,
          flashcard_type: flashcardType,
          quality_rating: response.quality,
          time_taken_seconds: response.time_taken,
          hint_used: response.hint_used,
          next_interval_days: nextInterval,
          reviewed_at: new Date().toISOString()
        })
      
      if (error) {
        // Silently fail if table doesn't exist - it's optional for analytics
        if (error.code !== 'PGRST205') {
          console.warn('Error recording review history (non-critical):', error.message)
        }
      }
    } catch (error) {
      // Silently fail - history table is optional
      console.warn('Error recording review history (non-critical):', error)
    }
  }

  /**
   * Get flashcards due for review
   */
  async getDueFlashcards(
    userId: string,
    limit: number = 20,
    flashcardTypes?: string[],
    offset: number = 0
  ): Promise<ReviewSession[]> {
    try {
      const now = new Date()
      const graceTime = new Date(now.getTime() + this.GRACE_PERIOD_HOURS * 60 * 60 * 1000)
      
      // Build query
      let query = supabase
        .from('user_flashcard_reviews')
        .select('*')
        .eq('user_id', userId)
        .lte('next_review', graceTime.toISOString())
        .order('next_review', { ascending: true })
        .range(offset, offset + limit - 1)
      
      if (flashcardTypes && flashcardTypes.length > 0) {
        query = query.in('flashcard_type', flashcardTypes)
      }
      
      const { data: dueReviews, error } = await query
      
      if (error) {
        // If table doesn't exist, return empty array gracefully
        if (error.code === '42P01') {
          console.warn('user_flashcard_reviews table not found. Please run the migration script.')
          return []
        }
        console.error('Error fetching due reviews:', error)
        return []
      }
      
      // Calculate priority and fetch flashcard content
      const sessions: ReviewSession[] = []
      
      for (const review of dueReviews || []) {
        const priority = this.calculateReviewPriority(review, now)
        const flashcard = await this.fetchFlashcardContent(
          review.flashcard_id,
          review.flashcard_type
        )
        
        if (flashcard) {
          sessions.push({
            flashcard,
            review,
            priority,
            reason: this.getReviewReason(review, now)
          })
        }
      }
      
      // Sort by priority (highest first)
      sessions.sort((a, b) => b.priority - a.priority)
      
      return sessions
    } catch (error) {
      console.error('Error getting due flashcards:', error)
      return []
    }
  }

  /**
   * Calculate priority for review scheduling
   */
  private calculateReviewPriority(review: FlashcardReview, now: Date): number {
    const nextReview = new Date(review.next_review)
    const daysPastDue = (now.getTime() - nextReview.getTime()) / (1000 * 60 * 60 * 24)
    
    let priority = 100
    
    // Increase priority for overdue cards
    if (daysPastDue > 0) {
      priority += Math.min(daysPastDue * 10, 50) // Cap at +50
    }
    
    // Prioritize cards with low success rate
    const successRate = review.total_attempts > 0 
      ? review.total_correct / review.total_attempts 
      : 0.5
    priority += (1 - successRate) * 30
    
    // Prioritize cards with lower easiness (harder cards)
    priority += (this.MAX_EASINESS - review.easiness_factor) * 20
    
    // Slight boost for cards reviewed fewer times
    if (review.review_count < 5) {
      priority += (5 - review.review_count) * 5
    }
    
    return priority
  }

  /**
   * Get reason for review
   */
  private getReviewReason(review: FlashcardReview, now: Date): string {
    const nextReview = new Date(review.next_review)
    const daysPastDue = (now.getTime() - nextReview.getTime()) / (1000 * 60 * 60 * 24)
    
    if (daysPastDue > 7) {
      return 'Overdue for review'
    } else if (daysPastDue > 0) {
      return 'Due for review'
    } else if (review.consecutive_correct === 0 && review.review_count > 0) {
      return 'Needs practice'
    } else if (review.review_count === 0) {
      return 'New card'
    } else if (review.interval_days <= 3) {
      return 'Recently learned'
    } else {
      return 'Scheduled review'
    }
  }

  /**
   * Fetch flashcard content based on type
   */
  private async fetchFlashcardContent(
    flashcardId: string,
    flashcardType: 'vocabulary' | 'spelling' | 'language' | 'question' | 'skill_node'
  ): Promise<any> {
    try {
      // Strip prefixes from flashcard IDs if present (e.g., "vocab-uuid" -> "uuid")
      const cleanId = flashcardId.replace(/^(vocab|spelling|question|language|skill)-/, '')
      
      switch (flashcardType) {
        case 'vocabulary':
        case 'spelling':
          const { data: word } = await supabase
            .from('spelling_words')
            .select('*')
            .eq('id', cleanId)
            .single()
          return word
          
        case 'question':
          const { data: question } = await supabase
            .from('questions')
            .select('*')
            .eq('id', cleanId)
            .single()
          return question
          
        case 'language':
          const { data: langQuestion } = await supabase
            .from('language_questions')
            .select(`
              *,
              languages (
                name
              )
            `)
            .eq('id', cleanId)
            .single()
          
          // Transform to include language name
          if (langQuestion) {
            return {
              ...langQuestion,
              language: langQuestion.languages?.name || 'Language',
              question: langQuestion.question_text || langQuestion.question
            }
          }
          return langQuestion
          
        case 'skill_node':
          const { data: node } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('id', cleanId)
            .single()
          return node
          
        default:
          return null
      }
    } catch (error) {
      console.error(`Error fetching flashcard content for ${flashcardType}:`, error)
      return null
    }
  }

  /**
   * Add multiple flashcards to review system at once
   */
  async addFlashcardsToReview(
    userId: string,
    flashcards: Array<{
      id: string
      type: 'vocabulary' | 'spelling' | 'language' | 'question' | 'skill_node'
    }>
  ): Promise<boolean> {
    try {
      // Create review records for each flashcard
      const now = new Date()
      const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000) // 1 day from now
      
      // Now we can use all columns since they've been added
      const reviewRecords = flashcards.map(card => ({
        user_id: userId,
        flashcard_id: card.id,
        flashcard_type: card.type,
        last_reviewed: now.toISOString(), // Considered "reviewed" when added from assessment
        next_review: tomorrow.toISOString(), // Due in 1 day (initial interval)
        review_count: 0, // Still 0 since this isn't a formal review
        easiness_factor: 2.5,
        interval_days: 1, // Start with 1 day interval
        consecutive_correct: 0,
        total_correct: 0,
        total_attempts: 0,
        created_at: now.toISOString(),
        updated_at: now.toISOString()
      }))
      
      // Insert all records, ignoring duplicates
      const { error } = await supabase
        .from('user_flashcard_reviews')
        .upsert(reviewRecords, {
          onConflict: 'user_id,flashcard_id,flashcard_type',
          ignoreDuplicates: true
        })
      
      if (error) {
        // If table doesn't exist, log warning instead of error
        if (error.code === '42P01') {
          console.warn('user_flashcard_reviews table not found. Please run the migration script.')
        } else {
          console.error('Error adding flashcards to review:', error)
        }
        return false
      }
      
      return true
    } catch (error) {
      console.error('Error in addFlashcardsToReview:', error)
      return false
    }
  }

  /**
   * Create a reminder for the next review
   */
  private async createNextReviewReminder(
    userId: string,
    flashcardId: string,
    flashcardType: string,
    intervalDays: number
  ): Promise<void> {
    try {
      // Import dynamically to avoid circular dependency
      const { studyReminderService } = await import('./studyReminderService')
      
      // Check if user has auto-scheduling enabled
      const schedule = await studyReminderService.getUserActiveSchedule(userId)
      if (schedule && schedule.auto_schedule_reviews) {
        await studyReminderService.createSpacedRepetitionReminder(
          userId,
          flashcardType,
          [flashcardId],
          intervalDays
        )
      }
    } catch (error) {
      console.error('Error creating review reminder:', error)
    }
  }

  /**
   * Get learning statistics for a user
   */
  async getUserStatistics(userId: string): Promise<any> {
    try {
      const { data: reviews, error } = await supabase
        .from('user_flashcard_reviews')
        .select('*')
        .eq('user_id', userId)
      
      if (error) {
        // If table doesn't exist, return default stats
        if (error.code === '42P01') {
          console.warn('user_flashcard_reviews table not found. Please run the migration script.')
          return {
            totalCards: 0,
            dueToday: 0,
            newCards: 0,
            learningCards: 0,
            matureCards: 0,
            averageEasiness: 0,
            averageSuccessRate: 0,
            totalReviews: 0
          }
        }
        throw error
      }
      
      const stats = {
        totalCards: reviews?.length || 0,
        dueToday: 0,
        newCards: 0,
        learningCards: 0,
        matureCards: 0,
        averageEasiness: 0,
        averageSuccessRate: 0,
        totalReviews: 0
      }
      
      if (!reviews || reviews.length === 0) return stats
      
      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      
      reviews.forEach(review => {
        const nextReview = new Date(review.next_review)
        
        // Count due today
        if (nextReview <= tomorrow) {
          stats.dueToday++
        }
        
        // Categorize cards
        if (review.review_count === 0) {
          stats.newCards++
        } else if (review.interval_days < 21) {
          stats.learningCards++
        } else {
          stats.matureCards++
        }
        
        // Calculate averages
        stats.averageEasiness += review.easiness_factor
        if (review.total_attempts > 0) {
          stats.averageSuccessRate += review.total_correct / review.total_attempts
        }
        stats.totalReviews += review.review_count
      })
      
      // Finalize averages
      stats.averageEasiness /= reviews.length
      stats.averageSuccessRate = (stats.averageSuccessRate / reviews.length) * 100
      
      return stats
    } catch (error) {
      console.error('Error getting user statistics:', error)
      return null
    }
  }

  /**
   * Get optimal review schedule for next 30 days
   */
  async getReviewForecast(userId: string, days: number = 30): Promise<any> {
    try {
      const { data: reviews, error } = await supabase
        .from('user_flashcard_reviews')
        .select('next_review, flashcard_type')
        .eq('user_id', userId)
      
      if (error) {
        // If table doesn't exist, return empty forecast
        if (error.code === '42P01') {
          console.warn('user_flashcard_reviews table not found. Please run the migration script.')
          return {}
        }
        throw error
      }
      
      const forecast: Record<string, number> = {}
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      for (let i = 0; i < days; i++) {
        const date = new Date(today)
        date.setDate(date.getDate() + i)
        const dateStr = date.toISOString().split('T')[0]
        forecast[dateStr] = 0
      }
      
      reviews?.forEach(review => {
        const reviewDate = new Date(review.next_review)
        reviewDate.setHours(0, 0, 0, 0)
        const dateStr = reviewDate.toISOString().split('T')[0]
        
        if (forecast.hasOwnProperty(dateStr)) {
          forecast[dateStr]++
        }
      })
      
      return forecast
    } catch (error) {
      console.error('Error getting review forecast:', error)
      return {}
    }
  }
}

export const spacedRepetitionService = new SpacedRepetitionService()