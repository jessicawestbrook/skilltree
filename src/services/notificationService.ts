import { supabase } from './supabase'
import { Notification, NotificationPreferences } from '../types/database.types'

// Retry configuration
const MAX_RETRIES = 3
const RETRY_DELAY = 1000 // 1 second
const RETRY_MULTIPLIER = 2 // Exponential backoff

// Helper function to check if error is retryable
function isRetryableError(error: any): boolean {
  // Connection errors, timeout errors, and 5xx server errors are retryable
  if (!error) return false
  
  const errorMessage = error.message?.toLowerCase() || ''
  const errorCode = error.code?.toLowerCase() || ''
  
  return (
    errorMessage.includes('connection') ||
    errorMessage.includes('timeout') ||
    errorMessage.includes('network') ||
    errorCode === 'err_connection_closed' ||
    errorCode === 'err_network' ||
    (error.status >= 500 && error.status < 600)
  )
}

// Helper function to retry failed requests
async function retryRequest<T>(
  fn: () => Promise<T>,
  retries = MAX_RETRIES,
  delay = RETRY_DELAY
): Promise<T | null> {
  try {
    return await fn()
  } catch (error) {
    if (retries > 0 && isRetryableError(error)) {
      console.warn(`Request failed, retrying in ${delay}ms... (${retries} retries left)`, error)
      await new Promise(resolve => setTimeout(resolve, delay))
      return retryRequest(fn, retries - 1, delay * RETRY_MULTIPLIER)
    }
    throw error
  }
}

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
      const result = await retryRequest(async () => {
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
        
        // Cache successful results
        if (typeof window !== 'undefined' && window.localStorage && data) {
          try {
            localStorage.setItem(`notifications_${userId}`, JSON.stringify({
              data: data || [],
              timestamp: Date.now()
            }))
          } catch (cacheError) {
            console.error('Error caching notifications:', cacheError)
          }
        }
        
        return data || []
      })
      
      return result || []
    } catch (error) {
      console.error('Error fetching notifications:', error)
      // Return cached notifications if available
      if (typeof window !== 'undefined' && window.localStorage) {
        try {
          const cached = localStorage.getItem(`notifications_${userId}`)
          if (cached) {
            const { data, timestamp } = JSON.parse(cached)
            // Use cache if less than 5 minutes old
            if (Date.now() - timestamp < 5 * 60 * 1000) {
              console.log('Using cached notifications due to connection error')
              return data
            }
          }
        } catch (cacheError) {
          console.error('Error reading cached notifications:', cacheError)
        }
      }
      return []
    }
  }

  // Mark notification as read
  static async markAsRead(notificationId: string): Promise<boolean> {
    try {
      const result = await retryRequest(async () => {
        const { error } = await supabase
          .from('notifications')
          .update({ is_read: true })
          .eq('id', notificationId)

        if (error) throw error
        return true
      })
      
      return result || false
    } catch (error) {
      console.error('Error marking notification as read:', error)
      // Store locally to retry later
      if (typeof window !== 'undefined' && window.localStorage) {
        try {
          const pendingUpdates = JSON.parse(localStorage.getItem('pending_notification_updates') || '[]')
          pendingUpdates.push({ id: notificationId, action: 'markAsRead', timestamp: Date.now() })
          localStorage.setItem('pending_notification_updates', JSON.stringify(pendingUpdates))
        } catch (cacheError) {
          console.error('Error storing pending update:', cacheError)
        }
      }
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
      const result = await retryRequest(async () => {
        const { count, error } = await supabase
          .from('notifications')
          .select('*', { count: 'exact', head: true })
          .eq('user_id', userId)
          .eq('is_read', false)
          .or(`expires_at.is.null,expires_at.gt.${new Date().toISOString()}`)

        if (error) throw error
        return count || 0
      })
      
      return result || 0
    } catch (error) {
      console.error('Error getting unread count:', error)
      // Try to calculate from cached notifications if available
      if (typeof window !== 'undefined' && window.localStorage) {
        try {
          const cached = localStorage.getItem(`notifications_${userId}`)
          if (cached) {
            const { data } = JSON.parse(cached)
            const unreadCount = data.filter((n: Notification) => !n.is_read).length
            console.log('Using cached unread count due to connection error')
            return unreadCount
          }
        } catch (cacheError) {
          console.error('Error calculating cached unread count:', cacheError)
        }
      }
      return 0
    }
  }

  // Get or create notification preferences
  static async getNotificationPreferences(userId: string): Promise<NotificationPreferences> {
    try {
      const result = await retryRequest(async () => {
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
      })
      
      return result || this.getDefaultPreferences(userId)
    } catch (error) {
      console.error('Error getting notification preferences:', error)
      return this.getDefaultPreferences(userId)
    }
  }

  // Helper to get default preferences
  private static getDefaultPreferences(userId: string): NotificationPreferences {
    // Check localStorage for cached preferences
    if (typeof window !== 'undefined' && window.localStorage) {
      try {
        const cached = localStorage.getItem(`notification_prefs_${userId}`)
        if (cached) {
          return JSON.parse(cached)
        }
      } catch (cacheError) {
        console.error('Error reading cached preferences:', cacheError)
      }
    }
    
    // Return default preferences
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

  // Process any pending updates that were stored locally due to connection errors
  static async processPendingUpdates(userId: string): Promise<void> {
    if (typeof window === 'undefined' || !window.localStorage) return

    try {
      const pendingUpdates = JSON.parse(localStorage.getItem('pending_notification_updates') || '[]')
      const failedUpdates: any[] = []

      for (const update of pendingUpdates) {
        // Skip updates older than 24 hours
        if (Date.now() - update.timestamp > 24 * 60 * 60 * 1000) continue

        try {
          if (update.action === 'markAsRead') {
            const success = await this.markAsRead(update.id)
            if (!success) failedUpdates.push(update)
          }
        } catch (error) {
          console.error('Error processing pending update:', error)
          failedUpdates.push(update)
        }
      }

      // Store only the updates that failed
      if (failedUpdates.length > 0) {
        localStorage.setItem('pending_notification_updates', JSON.stringify(failedUpdates))
      } else {
        localStorage.removeItem('pending_notification_updates')
      }
    } catch (error) {
      console.error('Error processing pending notification updates:', error)
    }
  }

  // Check connection status and process pending updates if online
  static async checkConnectionAndSync(userId: string): Promise<boolean> {
    try {
      // Try a simple query to check if connection is working
      const { error } = await supabase
        .from('notifications')
        .select('id')
        .limit(1)

      if (!error) {
        // Connection is good, process any pending updates
        await this.processPendingUpdates(userId)
        return true
      }
      return false
    } catch (error) {
      console.error('Connection check failed:', error)
      return false
    }
  }
}

export { NotificationService as notificationService }