import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { Notification, NotificationPreferences } from '../types/database.types'
import { notificationService } from '../services/notificationService'
import { useAuth } from './AuthContext'

interface NotificationContextType {
  notifications: Notification[]
  unreadCount: number
  preferences: NotificationPreferences | null
  loading: boolean
  fetchNotifications: () => Promise<void>
  markAsRead: (notificationId: string) => Promise<void>
  markAllAsRead: () => Promise<void>
  deleteNotification: (notificationId: string) => Promise<void>
  updatePreferences: (prefs: Partial<NotificationPreferences>) => Promise<void>
  createNotification: (
    type: Notification['type'],
    title: string,
    message: string,
    data?: any
  ) => Promise<void>
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined)

export const useNotifications = () => {
  const context = useContext(NotificationContext)
  if (context === undefined) {
    throw new Error('useNotifications must be used within a NotificationProvider')
  }
  return context
}

interface NotificationProviderProps {
  children: ReactNode
}

export const NotificationProvider: React.FC<NotificationProviderProps> = ({ children }) => {
  const { user } = useAuth()
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [preferences, setPreferences] = useState<NotificationPreferences | null>(null)
  const [loading, setLoading] = useState(false)

  // Fetch notifications when user changes
  useEffect(() => {
    if (user) {
      fetchNotifications()
      fetchPreferences()
      // Set up periodic refresh for notifications
      const interval = setInterval(fetchNotifications, 30000) // Every 30 seconds
      return () => clearInterval(interval)
    } else {
      setNotifications([])
      setUnreadCount(0)
      setPreferences(null)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const fetchNotifications = async () => {
    if (!user) return

    setLoading(true)
    try {
      const [notifs, count] = await Promise.all([
        notificationService.getUserNotifications(user.id, 50),
        notificationService.getUnreadCount(user.id)
      ])
      
      setNotifications(notifs)
      setUnreadCount(count)
    } catch (error) {
      console.error('Error fetching notifications:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPreferences = async () => {
    if (!user) return

    try {
      const prefs = await notificationService.getNotificationPreferences(user.id)
      setPreferences(prefs)
    } catch (error) {
      console.error('Error fetching notification preferences:', error)
    }
  }

  const markAsRead = async (notificationId: string) => {
    if (!user) return

    const success = await notificationService.markAsRead(notificationId)
    if (success) {
      setNotifications(prev =>
        prev.map(notif =>
          notif.id === notificationId ? { ...notif, is_read: true } : notif
        )
      )
      setUnreadCount(prev => Math.max(0, prev - 1))
    }
  }

  const markAllAsRead = async () => {
    if (!user) return

    const success = await notificationService.markAllAsRead(user.id)
    if (success) {
      setNotifications(prev =>
        prev.map(notif => ({ ...notif, is_read: true }))
      )
      setUnreadCount(0)
    }
  }

  const deleteNotification = async (notificationId: string) => {
    if (!user) return

    const success = await notificationService.deleteNotification(notificationId)
    if (success) {
      const deletedNotif = notifications.find(n => n.id === notificationId)
      setNotifications(prev => prev.filter(notif => notif.id !== notificationId))
      
      if (deletedNotif && !deletedNotif.is_read) {
        setUnreadCount(prev => Math.max(0, prev - 1))
      }
    }
  }

  const updatePreferences = async (prefs: Partial<NotificationPreferences>) => {
    if (!user) return

    const success = await notificationService.updateNotificationPreferences(user.id, prefs)
    if (success) {
      setPreferences(prev => prev ? { ...prev, ...prefs } : null)
    }
  }

  const createNotification = async (
    type: Notification['type'],
    title: string,
    message: string,
    data?: any
  ) => {
    if (!user) return

    const notification = await notificationService.createNotification(
      user.id,
      type,
      title,
      message,
      data
    )
    
    if (notification) {
      setNotifications(prev => [notification, ...prev])
      setUnreadCount(prev => prev + 1)
    }
  }

  const value: NotificationContextType = {
    notifications,
    unreadCount,
    preferences,
    loading,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    updatePreferences,
    createNotification
  }

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  )
}