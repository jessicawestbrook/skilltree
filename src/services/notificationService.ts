import { supabase } from './supabase'
import { Notification, NotificationPreferences } from '../types/database.types'

export class NotificationService {
  // Create a new notification
  static async createNotification(
    userId: string, 
    type: Notification['type'],
    title: string,
    message: string,
    data?: any,
    expiresAt?: string
  ): Promise<Notification | null> {
    try {
      const { data: notification, error } = await supabase
        .from('notifications')
        .insert({
          user_id: userId,
          type,
          title,
          message,
          data,
          expires_at: expiresAt,
          is_read: false,
          created_at: new Date().toISOString()
        })
        .select()
        .single()

      if (error) throw error
      return notification
    } catch (error) {
      console.error('Error creating notification:', error)
      return null
    }
  }

  // Get user notifications
  static async getUserNotifications(
    userId: string, 
    limit: number = 20,
    unreadOnly: boolean = false
  ): Promise<Notification[]> {
    try {
      let query = supabase
        .from('notifications')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false })
        .limit(limit)

      if (unreadOnly) {
        query = query.eq('is_read', false)
      }

      // Filter out expired notifications
      query = query.or(`expires_at.is.null,expires_at.gt.${new Date().toISOString()}`)

      const { data, error } = await query

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching notifications:', error)
      return []
    }
  }

  // Mark notification as read
  static async markAsRead(notificationId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('notifications')
        .update({ is_read: true })
        .eq('id', notificationId)

      if (error) throw error
      return true
    } catch (error) {
      console.error('Error marking notification as read:', error)
      return false
    }
  }

  // Mark all notifications as read for user
  static async markAllAsRead(userId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('notifications')
        .update({ is_read: true })
        .eq('user_id', userId)
        .eq('is_read', false)

      if (error) throw error
      return true
    } catch (error) {
      console.error('Error marking all notifications as read:', error)
      return false
    }
  }

  // Delete notification
  static async deleteNotification(notificationId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('notifications')
        .delete()
        .eq('id', notificationId)

      if (error) throw error
      return true
    } catch (error) {
      console.error('Error deleting notification:', error)
      return false
    }
  }

  // Get unread count
  static async getUnreadCount(userId: string): Promise<number> {
    try {
      const { count, error } = await supabase
        .from('notifications')
        .select('*', { count: 'exact', head: true })
        .eq('user_id', userId)
        .eq('is_read', false)
        .or(`expires_at.is.null,expires_at.gt.${new Date().toISOString()}`)

      if (error) throw error
      return count || 0
    } catch (error) {
      console.error('Error getting unread count:', error)
      return 0
    }
  }

  // Get or create notification preferences
  static async getNotificationPreferences(userId: string): Promise<NotificationPreferences> {
    try {
      const { data, error } = await supabase
        .from('notification_preferences')
        .select('*')
        .eq('user_id', userId)
        .single()

      if (error && error.code === 'PGRST116') {
        // Create default preferences if they don't exist
        const defaultPrefs = {
          user_id: userId,
          email_notifications: true,
          push_notifications: true,
          achievement_notifications: true,
          progress_notifications: true,
          reminder_notifications: true,
          system_notifications: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }

        const { data: newPrefs, error: createError } = await supabase
          .from('notification_preferences')
          .insert(defaultPrefs)
          .select()
          .single()

        if (createError) throw createError
        return newPrefs
      }

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error getting notification preferences:', error)
      // Return default preferences if there's an error
      return {
        user_id: userId,
        email_notifications: true,
        push_notifications: false,
        achievement_notifications: true,
        progress_notifications: true,
        reminder_notifications: true,
        system_notifications: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    }
  }

  // Update notification preferences
  static async updateNotificationPreferences(
    userId: string, 
    preferences: Partial<NotificationPreferences>
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('notification_preferences')
        .upsert({
          user_id: userId,
          ...preferences,
          updated_at: new Date().toISOString()
        })

      if (error) throw error
      return true
    } catch (error) {
      console.error('Error updating notification preferences:', error)
      return false
    }
  }

  // Helper methods for common notification types
  static async notifyAchievement(userId: string, title: string, message: string, data?: any) {
    const prefs = await this.getNotificationPreferences(userId)
    if (prefs.achievement_notifications) {
      return await this.createNotification(userId, 'achievement', title, message, data)
    }
    return null
  }

  static async notifyProgress(userId: string, title: string, message: string, data?: any) {
    const prefs = await this.getNotificationPreferences(userId)
    if (prefs.progress_notifications) {
      return await this.createNotification(userId, 'progress', title, message, data)
    }
    return null
  }

  static async notifyReminder(userId: string, title: string, message: string, data?: any) {
    const prefs = await this.getNotificationPreferences(userId)
    if (prefs.reminder_notifications) {
      return await this.createNotification(userId, 'reminder', title, message, data)
    }
    return null
  }

  static async notifySystem(userId: string, title: string, message: string, data?: any) {
    const prefs = await this.getNotificationPreferences(userId)
    if (prefs.system_notifications) {
      return await this.createNotification(userId, 'system', title, message, data)
    }
    return null
  }
}

export { NotificationService as notificationService }