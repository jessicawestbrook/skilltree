import { supabase } from './supabase'
import { notificationService } from './notificationService'

export interface Achievement {
  id: string
  code: string
  name: string
  description: string
  category: 'learning' | 'streak' | 'mastery' | 'collection' | 'social' | 'special'
  requirement_type: 'count' | 'streak' | 'score' | 'collection' | 'special'
  requirement_value: number
  requirement_data?: any
  icon: string
  badge_color: string
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary'
  points: number
  is_active: boolean
  is_secret: boolean
}

export interface UserAchievement {
  id: string
  user_id: string
  achievement_id: string
  current_progress: number
  target_progress: number
  progress_data?: any
  unlocked_at?: string
  notification_sent: boolean
  achievement?: Achievement
}

export interface UserStats {
  user_id: string
  total_lessons_completed: number
  total_flashcards_reviewed: number
  total_correct_answers: number
  total_study_time_minutes: number
  total_modules_completed: number
  current_streak_days: number
  longest_streak_days: number
  last_activity_date: string
  average_accuracy: number
  perfect_scores_count: number
  total_achievements_unlocked: number
  total_achievement_points: number
}

class AchievementService {
  /**
   * Get all achievements
   */
  async getAllAchievements(): Promise<Achievement[]> {
    try {
      const { data, error } = await supabase
        .from('achievements')
        .select('*')
        .eq('is_active', true)
        .order('category')
        .order('requirement_value')

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching achievements:', error)
      return []
    }
  }

  /**
   * Get user's achievements
   */
  async getUserAchievements(userId: string): Promise<UserAchievement[]> {
    try {
      const { data, error } = await supabase
        .from('user_achievements')
        .select(`
          *,
          achievement:achievements(*)
        `)
        .eq('user_id', userId)
        .order('unlocked_at', { ascending: false })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching user achievements:', error)
      return []
    }
  }

  /**
   * Get or create user stats
   */
  async getUserStats(userId: string): Promise<UserStats | null> {
    try {
      let { data, error } = await supabase
        .from('user_stats')
        .select('*')
        .eq('user_id', userId)
        .single()

      if (error && error.code === 'PGRST116') {
        // Stats don't exist, create them
        const { data: newStats, error: createError } = await supabase
          .from('user_stats')
          .insert({ user_id: userId })
          .select()
          .single()

        if (createError) throw createError
        return newStats
      }

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error fetching user stats:', error)
      return null
    }
  }

  /**
   * Update user stats
   */
  async updateUserStats(userId: string, updates: Partial<UserStats>): Promise<void> {
    try {
      const { error } = await supabase
        .from('user_stats')
        .upsert({
          user_id: userId,
          ...updates,
          updated_at: new Date().toISOString()
        })

      if (error) throw error
    } catch (error) {
      console.error('Error updating user stats:', error)
    }
  }

  /**
   * Check and unlock achievements based on current stats
   */
  async checkAchievements(userId: string, triggerType: string, additionalData?: any): Promise<UserAchievement[]> {
    const unlockedAchievements: UserAchievement[] = []

    try {
      // Get user stats
      const stats = await this.getUserStats(userId)
      if (!stats) return []

      // Get all achievements that might be relevant
      const { data: achievements, error: achError } = await supabase
        .from('achievements')
        .select('*')
        .eq('is_active', true)

      if (achError || !achievements) return []

      // Get user's current achievement progress
      const { data: userAchievements, error: userAchError } = await supabase
        .from('user_achievements')
        .select('*')
        .eq('user_id', userId)

      if (userAchError) return []

      const userAchMap = new Map(
        (userAchievements || []).map(ua => [ua.achievement_id, ua])
      )

      // Check each achievement
      for (const achievement of achievements) {
        const userAch = userAchMap.get(achievement.id)
        
        // Skip if already unlocked
        if (userAch?.unlocked_at) continue

        // Check if achievement should be unlocked
        const shouldUnlock = await this.checkAchievementCriteria(
          achievement,
          stats,
          triggerType,
          additionalData
        )

        if (shouldUnlock) {
          const unlocked = await this.unlockAchievement(userId, achievement)
          if (unlocked) {
            unlockedAchievements.push(unlocked)
          }
        }
      }

      return unlockedAchievements
    } catch (error) {
      console.error('Error checking achievements:', error)
      return []
    }
  }

  /**
   * Check if achievement criteria is met
   */
  private async checkAchievementCriteria(
    achievement: Achievement,
    stats: UserStats,
    triggerType: string,
    additionalData?: any
  ): Promise<boolean> {
    switch (achievement.requirement_type) {
      case 'count':
        return this.checkCountCriteria(achievement, stats)
      
      case 'streak':
        return stats.current_streak_days >= (achievement.requirement_value || 0)
      
      case 'special':
        return this.checkSpecialCriteria(achievement.code, triggerType, additionalData)
      
      case 'collection':
        return this.checkCollectionCriteria(achievement, additionalData)
      
      default:
        return false
    }
  }

  /**
   * Check count-based criteria
   */
  private checkCountCriteria(achievement: Achievement, stats: UserStats): boolean {
    const target = achievement.requirement_value || 0

    switch (achievement.code) {
      case 'first_lesson':
      case 'lessons_10':
      case 'lessons_50':
      case 'lessons_100':
      case 'lessons_500':
      case 'lessons_1000':
        return stats.total_lessons_completed >= target

      case 'flashcards_10':
      case 'flashcards_100':
      case 'flashcards_1000':
        return stats.total_flashcards_reviewed >= target

      case 'module_first':
      case 'module_5':
      case 'module_25':
      case 'module_100':
        return stats.total_modules_completed >= target

      case 'perfectionist':
        return stats.perfect_scores_count >= target

      default:
        return false
    }
  }

  /**
   * Check special achievements
   */
  private checkSpecialCriteria(code: string, triggerType: string, data?: any): boolean {
    const now = new Date()
    const hour = now.getHours()
    const day = now.getDay()

    switch (code) {
      case 'night_owl':
        return triggerType === 'study_session' && (hour >= 0 && hour < 5)

      case 'early_bird':
        return triggerType === 'study_session' && hour < 6

      case 'weekend_warrior':
        return triggerType === 'study_session' && (day === 0 || day === 6)

      case 'speed_demon':
        return triggerType === 'flashcard_speed' && data?.cardsCompleted >= 10 && data?.timeSeconds < 60

      case 'comeback_kid':
        return triggerType === 'comeback' && data?.daysAway >= 7

      case 'perfect_10':
      case 'perfect_25':
      case 'perfect_50':
        return triggerType === 'perfect_streak' && data?.streak >= (
          code === 'perfect_10' ? 10 :
          code === 'perfect_25' ? 25 : 50
        )

      default:
        return false
    }
  }

  /**
   * Check collection-based criteria
   */
  private async checkCollectionCriteria(achievement: Achievement, data?: any): Promise<boolean> {
    if (!data?.userId) return false

    try {
      // Get unique categories the user has studied
      const { data: studiedCategories, error } = await supabase
        .from('user_progress')
        .select('node_id')
        .eq('user_id', data.userId)
        .eq('status', 'completed')

      if (error || !studiedCategories) return false

      // Get the categories from skill_tree_nodes
      const nodeIds = studiedCategories.map(sc => sc.node_id)
      const { data: nodes, error: nodeError } = await supabase
        .from('skill_tree_nodes')
        .select('parent_id')
        .in('id', nodeIds)

      if (nodeError || !nodes) return false

      // Count unique top-level categories
      const uniqueCategories = new Set(nodes.map(n => n.parent_id).filter(Boolean))
      
      return uniqueCategories.size >= (achievement.requirement_value || 0)
    } catch (error) {
      console.error('Error checking collection criteria:', error)
      return false
    }
  }

  /**
   * Unlock an achievement for a user
   */
  private async unlockAchievement(userId: string, achievement: Achievement): Promise<UserAchievement | null> {
    try {
      const now = new Date().toISOString()

      // Create or update user achievement record
      const { data, error } = await supabase
        .from('user_achievements')
        .upsert({
          user_id: userId,
          achievement_id: achievement.id,
          current_progress: achievement.requirement_value || 1,
          target_progress: achievement.requirement_value || 1,
          unlocked_at: now,
          notification_sent: false
        }, {
          onConflict: 'user_id,achievement_id'
        })
        .select()
        .single()

      if (error) throw error

      // Update user stats
      const currentStats = await this.getUserStats(userId)
      if (currentStats) {
        await this.updateUserStats(userId, {
          total_achievements_unlocked: currentStats.total_achievements_unlocked + 1,
          total_achievement_points: currentStats.total_achievement_points + achievement.points
        })
      }

      // Send notification
      await notificationService.notifyAchievement(
        userId,
        `Achievement Unlocked: ${achievement.name}!`,
        achievement.description,
        {
          achievement_id: achievement.id,
          achievement_code: achievement.code,
          points: achievement.points,
          rarity: achievement.rarity
        }
      )

      // Mark notification as sent
      await supabase
        .from('user_achievements')
        .update({ notification_sent: true })
        .eq('id', data.id)

      return { ...data, achievement }
    } catch (error) {
      console.error('Error unlocking achievement:', error)
      return null
    }
  }

  /**
   * Track lesson completion
   */
  async trackLessonCompletion(userId: string): Promise<void> {
    const stats = await this.getUserStats(userId)
    if (!stats) return

    await this.updateUserStats(userId, {
      total_lessons_completed: stats.total_lessons_completed + 1
    })

    await this.checkAchievements(userId, 'lesson_complete')
  }

  /**
   * Track flashcard review
   */
  async trackFlashcardReview(userId: string, correct: boolean): Promise<void> {
    const stats = await this.getUserStats(userId)
    if (!stats) return

    await this.updateUserStats(userId, {
      total_flashcards_reviewed: stats.total_flashcards_reviewed + 1,
      total_correct_answers: correct ? stats.total_correct_answers + 1 : stats.total_correct_answers
    })

    await this.checkAchievements(userId, 'flashcard_review')
  }

  /**
   * Track module completion
   */
  async trackModuleCompletion(userId: string, moduleId: string): Promise<void> {
    const stats = await this.getUserStats(userId)
    if (!stats) return

    await this.updateUserStats(userId, {
      total_modules_completed: stats.total_modules_completed + 1
    })

    await this.checkAchievements(userId, 'module_complete', { moduleId })
  }

  /**
   * Track study streak
   */
  async trackDailyActivity(userId: string): Promise<void> {
    const stats = await this.getUserStats(userId)
    if (!stats) return

    const today = new Date().toISOString().split('T')[0]
    const lastActivity = stats.last_activity_date

    let newStreak = stats.current_streak_days
    
    if (lastActivity) {
      const lastDate = new Date(lastActivity)
      const todayDate = new Date(today)
      const daysDiff = Math.floor((todayDate.getTime() - lastDate.getTime()) / (1000 * 60 * 60 * 24))

      if (daysDiff === 1) {
        // Consecutive day
        newStreak = stats.current_streak_days + 1
      } else if (daysDiff > 1) {
        // Streak broken
        if (daysDiff >= 7) {
          // Check comeback kid achievement
          await this.checkAchievements(userId, 'comeback', { daysAway: daysDiff })
        }
        newStreak = 1
      }
      // If daysDiff === 0, it's the same day, don't update streak
    } else {
      newStreak = 1
    }

    const longestStreak = Math.max(newStreak, stats.longest_streak_days)

    await this.updateUserStats(userId, {
      current_streak_days: newStreak,
      longest_streak_days: longestStreak,
      last_activity_date: today
    })

    // Check time-based achievements
    await this.checkAchievements(userId, 'study_session')
    
    // Check streak achievements
    if (newStreak > stats.current_streak_days) {
      await this.checkAchievements(userId, 'streak_update')
    }
  }

  /**
   * Track perfect score
   */
  async trackPerfectScore(userId: string, assessmentType: string): Promise<void> {
    const stats = await this.getUserStats(userId)
    if (!stats) return

    await this.updateUserStats(userId, {
      perfect_scores_count: stats.perfect_scores_count + 1
    })

    await this.checkAchievements(userId, 'perfect_score', { assessmentType })
  }

  /**
   * Track flashcard streak
   */
  async trackFlashcardStreak(userId: string, streak: number): Promise<void> {
    await this.checkAchievements(userId, 'perfect_streak', { streak })
  }

  /**
   * Track speed achievement
   */
  async trackSpeedAchievement(userId: string, cardsCompleted: number, timeSeconds: number): Promise<void> {
    await this.checkAchievements(userId, 'flashcard_speed', { cardsCompleted, timeSeconds })
  }
}

export const achievementService = new AchievementService()