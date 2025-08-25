import { supabase } from './supabase'
import { notificationService } from './notificationService'

export interface StudyReminder {
  id: string
  user_id: string
  reminder_type: 'flashcard_review' | 'skill_practice' | 'custom'
  content_type?: string
  content_ids?: string[]
  scheduled_for: string
  reminder_sent: boolean
  reminder_sent_at?: string
  study_duration_minutes: number
  priority: 'low' | 'medium' | 'high'
  title?: string
  description?: string
  metadata?: any
  created_at: string
  updated_at: string
  completed_at?: string
  dismissed_at?: string
  is_recurring: boolean
  recurrence_pattern?: 'daily' | 'weekly' | 'custom'
  recurrence_days?: number[]
  recurrence_end_date?: string
}

export interface StudySchedule {
  id: string
  user_id: string
  schedule_name: string
  is_active: boolean
  preferred_days: number[]
  preferred_time: string
  timezone: string
  content_types?: string[]
  difficulty_levels?: string[]
  session_duration_minutes: number
  cards_per_session: number
  auto_schedule_reviews: boolean
  include_overdue: boolean
  created_at: string
  updated_at: string
}

export interface ReminderCreationData {
  type: 'flashcard_review' | 'skill_practice' | 'custom'
  contentType?: string
  contentIds?: string[]
  scheduledFor: Date
  title?: string
  description?: string
  duration?: number
  priority?: 'low' | 'medium' | 'high'
  isRecurring?: boolean
  recurrencePattern?: 'daily' | 'weekly' | 'custom'
  recurrenceDays?: number[]
  recurrenceEndDate?: Date
}

class StudyReminderService {
  /**
   * Create a new study reminder
   */
  async createReminder(
    userId: string,
    data: ReminderCreationData
  ): Promise<StudyReminder | null> {
    try {
      const reminderData = {
        user_id: userId,
        reminder_type: data.type,
        content_type: data.contentType,
        content_ids: data.contentIds,
        scheduled_for: data.scheduledFor.toISOString(),
        title: data.title || this.generateTitle(data),
        description: data.description || this.generateDescription(data),
        study_duration_minutes: data.duration || 15,
        priority: data.priority || 'medium',
        is_recurring: data.isRecurring || false,
        recurrence_pattern: data.recurrencePattern,
        recurrence_days: data.recurrenceDays,
        recurrence_end_date: data.recurrenceEndDate?.toISOString()
      }

      const { data: reminder, error } = await supabase
        .from('study_reminders')
        .insert(reminderData)
        .select()
        .single()

      if (error) throw error

      // Schedule notification for this reminder
      await this.scheduleNotification(reminder)

      return reminder
    } catch (error) {
      console.error('Error creating study reminder:', error)
      return null
    }
  }

  /**
   * Create reminder based on spaced repetition interval
   */
  async createSpacedRepetitionReminder(
    userId: string,
    contentType: string,
    contentIds: string[],
    intervalDays: number
  ): Promise<StudyReminder | null> {
    try {
      // Get user's preferred study schedule
      const schedule = await this.getUserActiveSchedule(userId)
      
      // Calculate scheduled time
      let scheduledFor = new Date()
      scheduledFor.setDate(scheduledFor.getDate() + intervalDays)
      
      // If user has a preferred time, use it
      if (schedule) {
        const [hours, minutes] = schedule.preferred_time.split(':').map(Number)
        scheduledFor.setHours(hours, minutes, 0, 0)
        
        // Find next available day based on preferred days
        if (schedule.preferred_days && schedule.preferred_days.length > 0) {
          while (!schedule.preferred_days.includes(scheduledFor.getDay())) {
            scheduledFor.setDate(scheduledFor.getDate() + 1)
          }
        }
      }

      return await this.createReminder(userId, {
        type: 'flashcard_review',
        contentType,
        contentIds,
        scheduledFor,
        title: `Review your ${contentType} flashcards`,
        description: `${contentIds.length} cards are due for spaced repetition review`,
        duration: Math.min(contentIds.length * 2, 30) // 2 min per card, max 30 min
      })
    } catch (error) {
      console.error('Error creating spaced repetition reminder:', error)
      return null
    }
  }

  /**
   * Get user's active reminders
   */
  async getUserReminders(
    userId: string,
    includeCompleted: boolean = false
  ): Promise<StudyReminder[]> {
    try {
      let query = supabase
        .from('study_reminders')
        .select('*')
        .eq('user_id', userId)
        .order('scheduled_for', { ascending: true })

      if (!includeCompleted) {
        query = query.is('completed_at', null).is('dismissed_at', null)
      }

      const { data, error } = await query

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching user reminders:', error)
      return []
    }
  }

  /**
   * Get upcoming reminders (next 7 days)
   */
  async getUpcomingReminders(userId: string): Promise<StudyReminder[]> {
    try {
      const now = new Date()
      const weekFromNow = new Date()
      weekFromNow.setDate(weekFromNow.getDate() + 7)

      const { data, error } = await supabase
        .from('study_reminders')
        .select('*')
        .eq('user_id', userId)
        .gte('scheduled_for', now.toISOString())
        .lte('scheduled_for', weekFromNow.toISOString())
        .eq('reminder_sent', false)
        .is('completed_at', null)
        .is('dismissed_at', null)
        .order('scheduled_for', { ascending: true })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching upcoming reminders:', error)
      return []
    }
  }

  /**
   * Get overdue reminders
   */
  async getOverdueReminders(userId: string): Promise<StudyReminder[]> {
    try {
      const now = new Date()

      const { data, error } = await supabase
        .from('study_reminders')
        .select('*')
        .eq('user_id', userId)
        .lt('scheduled_for', now.toISOString())
        .is('completed_at', null)
        .is('dismissed_at', null)
        .order('scheduled_for', { ascending: true })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching overdue reminders:', error)
      return []
    }
  }

  /**
   * Mark reminder as completed
   */
  async completeReminder(reminderId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('study_reminders')
        .update({ 
          completed_at: new Date().toISOString() 
        })
        .eq('id', reminderId)

      if (error) throw error

      // Check if this is a recurring reminder and create next occurrence
      const { data: reminder } = await supabase
        .from('study_reminders')
        .select('*')
        .eq('id', reminderId)
        .single()

      if (reminder && reminder.is_recurring) {
        await this.createNextRecurrence(reminder)
      }

      return true
    } catch (error) {
      console.error('Error completing reminder:', error)
      return false
    }
  }

  /**
   * Dismiss reminder
   */
  async dismissReminder(reminderId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('study_reminders')
        .update({ 
          dismissed_at: new Date().toISOString() 
        })
        .eq('id', reminderId)

      if (error) throw error
      return true
    } catch (error) {
      console.error('Error dismissing reminder:', error)
      return false
    }
  }

  /**
   * Update reminder
   */
  async updateReminder(
    reminderId: string,
    updates: Partial<StudyReminder>
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('study_reminders')
        .update(updates)
        .eq('id', reminderId)

      if (error) throw error

      // Reschedule notification if scheduled_for changed
      if (updates.scheduled_for) {
        const { data: reminder } = await supabase
          .from('study_reminders')
          .select('*')
          .eq('id', reminderId)
          .single()

        if (reminder) {
          await this.scheduleNotification(reminder)
        }
      }

      return true
    } catch (error) {
      console.error('Error updating reminder:', error)
      return false
    }
  }

  /**
   * Delete reminder
   */
  async deleteReminder(reminderId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('study_reminders')
        .delete()
        .eq('id', reminderId)

      if (error) throw error
      return true
    } catch (error) {
      console.error('Error deleting reminder:', error)
      return false
    }
  }

  /**
   * Get or create user's study schedule
   */
  async getUserSchedules(userId: string): Promise<StudySchedule[]> {
    try {
      const { data, error } = await supabase
        .from('study_schedules')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching user schedules:', error)
      return []
    }
  }

  /**
   * Get user's active study schedule
   */
  async getUserActiveSchedule(userId: string): Promise<StudySchedule | null> {
    try {
      const { data, error } = await supabase
        .from('study_schedules')
        .select('*')
        .eq('user_id', userId)
        .eq('is_active', true)
        .single()

      if (error && error.code !== 'PGRST116') throw error
      return data
    } catch (error) {
      console.error('Error fetching active schedule:', error)
      return null
    }
  }

  /**
   * Create or update study schedule
   */
  async upsertSchedule(
    userId: string,
    schedule: Partial<StudySchedule>
  ): Promise<StudySchedule | null> {
    try {
      // Deactivate other schedules if this one is active
      if (schedule.is_active) {
        await supabase
          .from('study_schedules')
          .update({ is_active: false })
          .eq('user_id', userId)
      }

      const { data, error } = await supabase
        .from('study_schedules')
        .upsert({
          user_id: userId,
          ...schedule
        })
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error upserting schedule:', error)
      return null
    }
  }

  /**
   * Schedule a notification for a reminder
   */
  private async scheduleNotification(reminder: StudyReminder): Promise<void> {
    try {
      // Create notification to be sent at scheduled time
      const notification = await notificationService.createNotification(
        reminder.user_id,
        'reminder',
        reminder.title || 'Study Reminder',
        reminder.description || 'Time for your study session!',
        {
          reminder_id: reminder.id,
          content_type: reminder.content_type,
          content_ids: reminder.content_ids,
          duration_minutes: reminder.study_duration_minutes
        },
        reminder.scheduled_for
      )

      if (notification) {
        // Add to notification queue for processing
        await supabase
          .from('notification_queue')
          .insert({
            notification_id: notification.id,
            reminder_id: reminder.id,
            scheduled_for: reminder.scheduled_for,
            status: 'pending'
          })
      }
    } catch (error) {
      console.error('Error scheduling notification:', error)
    }
  }

  /**
   * Create next occurrence of a recurring reminder
   */
  private async createNextRecurrence(reminder: StudyReminder): Promise<void> {
    if (!reminder.is_recurring || !reminder.recurrence_pattern) return

    const scheduledFor = new Date(reminder.scheduled_for)
    
    // Check if we've reached the end date
    if (reminder.recurrence_end_date) {
      const endDate = new Date(reminder.recurrence_end_date)
      if (scheduledFor >= endDate) return
    }

    // Calculate next occurrence
    switch (reminder.recurrence_pattern) {
      case 'daily':
        scheduledFor.setDate(scheduledFor.getDate() + 1)
        break
      
      case 'weekly':
        scheduledFor.setDate(scheduledFor.getDate() + 7)
        break
      
      case 'custom':
        if (reminder.recurrence_days && reminder.recurrence_days.length > 0) {
          // Find next day in recurrence_days
          let daysToAdd = 1
          const currentDay = scheduledFor.getDay()
          
          for (let i = 1; i <= 7; i++) {
            const nextDay = (currentDay + i) % 7
            if (reminder.recurrence_days.includes(nextDay)) {
              daysToAdd = i
              break
            }
          }
          
          scheduledFor.setDate(scheduledFor.getDate() + daysToAdd)
        }
        break
    }

    // Create new reminder
    await this.createReminder(reminder.user_id, {
      type: reminder.reminder_type,
      contentType: reminder.content_type,
      contentIds: reminder.content_ids,
      scheduledFor,
      title: reminder.title,
      description: reminder.description,
      duration: reminder.study_duration_minutes,
      priority: reminder.priority as 'low' | 'medium' | 'high',
      isRecurring: true,
      recurrencePattern: reminder.recurrence_pattern,
      recurrenceDays: reminder.recurrence_days,
      recurrenceEndDate: reminder.recurrence_end_date ? new Date(reminder.recurrence_end_date) : undefined
    })
  }

  /**
   * Generate title for reminder
   */
  private generateTitle(data: ReminderCreationData): string {
    switch (data.type) {
      case 'flashcard_review':
        return `Review ${data.contentType || 'flashcards'}`
      case 'skill_practice':
        return 'Practice session'
      case 'custom':
        return 'Study reminder'
      default:
        return 'Study time!'
    }
  }

  /**
   * Generate description for reminder
   */
  private generateDescription(data: ReminderCreationData): string {
    const duration = data.duration || 15
    const cardCount = data.contentIds?.length || 0
    
    switch (data.type) {
      case 'flashcard_review':
        return cardCount > 0 
          ? `${cardCount} cards ready for review (${duration} min)`
          : `${duration}-minute review session`
      case 'skill_practice':
        return `${duration}-minute practice session`
      case 'custom':
        return `${duration}-minute study session`
      default:
        return `Time to study for ${duration} minutes`
    }
  }

  /**
   * Process due reminders and send notifications
   * This should be called periodically (e.g., every minute) by a cron job or Edge Function
   */
  async processDueReminders(): Promise<void> {
    try {
      const now = new Date()
      
      // Get pending reminders that are due
      const { data: dueReminders, error } = await supabase
        .from('study_reminders')
        .select('*')
        .lte('scheduled_for', now.toISOString())
        .eq('reminder_sent', false)
        .is('completed_at', null)
        .is('dismissed_at', null)

      if (error) throw error
      if (!dueReminders || dueReminders.length === 0) return

      // Process each due reminder
      for (const reminder of dueReminders) {
        try {
          // Send notification
          await notificationService.notifyReminder(
            reminder.user_id,
            reminder.title || 'Study Reminder',
            reminder.description || 'Time for your study session!',
            {
              reminder_id: reminder.id,
              content_type: reminder.content_type,
              content_ids: reminder.content_ids,
              duration_minutes: reminder.study_duration_minutes
            }
          )

          // Mark reminder as sent
          await supabase
            .from('study_reminders')
            .update({
              reminder_sent: true,
              reminder_sent_at: now.toISOString()
            })
            .eq('id', reminder.id)

        } catch (error) {
          console.error(`Error processing reminder ${reminder.id}:`, error)
        }
      }
    } catch (error) {
      console.error('Error processing due reminders:', error)
    }
  }
}

export const studyReminderService = new StudyReminderService()