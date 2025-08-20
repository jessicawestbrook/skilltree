import React from 'react'
import { useNotifications } from '../contexts/NotificationContext'
import { Notification } from '../types/database.types'
import { 
  TrophyIcon,
  ChartBarIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  UserGroupIcon,
  XMarkIcon,
  CheckIcon
} from '@heroicons/react/24/outline'
// Simple date formatting function instead of date-fns
const formatTimeAgo = (date: string) => {
  const now = new Date()
  const notifDate = new Date(date)
  const diffInMinutes = Math.floor((now.getTime() - notifDate.getTime()) / (1000 * 60))
  
  if (diffInMinutes < 1) return 'Just now'
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`
  
  const diffInHours = Math.floor(diffInMinutes / 60)
  if (diffInHours < 24) return `${diffInHours}h ago`
  
  const diffInDays = Math.floor(diffInHours / 24)
  if (diffInDays < 7) return `${diffInDays}d ago`
  
  return notifDate.toLocaleDateString()
}

interface NotificationDropdownProps {
  onClose: () => void
}

const NotificationDropdown: React.FC<NotificationDropdownProps> = ({ onClose }) => {
  const { 
    notifications, 
    unreadCount, 
    loading, 
    markAsRead, 
    markAllAsRead, 
    deleteNotification 
  } = useNotifications()

  const getNotificationIcon = (type: Notification['type']) => {
    switch (type) {
      case 'achievement':
        return <TrophyIcon className="h-5 w-5 text-yellow-500" />
      case 'progress':
        return <ChartBarIcon className="h-5 w-5 text-blue-500" />
      case 'reminder':
        return <ClockIcon className="h-5 w-5 text-orange-500" />
      case 'system':
        return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
      case 'social':
        return <UserGroupIcon className="h-5 w-5 text-green-500" />
      default:
        return <ExclamationTriangleIcon className="h-5 w-5 text-neutral-500" />
    }
  }

  const handleNotificationClick = async (notification: Notification) => {
    if (!notification.is_read) {
      await markAsRead(notification.id)
    }
    
    // Handle navigation based on notification data
    if (notification.data?.path) {
      window.location.href = notification.data.path
    }
  }

  if (loading) {
    return (
      <div className="p-4">
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-neutral-200 dark:bg-neutral-700 rounded w-1/2"></div>
          <div className="h-12 bg-neutral-200 dark:bg-neutral-700 rounded"></div>
          <div className="h-12 bg-neutral-200 dark:bg-neutral-700 rounded"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-h-96 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-neutral-200 dark:border-neutral-700">
        <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">
          Notifications
        </h3>
        <div className="flex items-center gap-2">
          {unreadCount > 0 && (
            <button
              onClick={markAllAsRead}
              className="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
            >
              Mark all read
            </button>
          )}
          <button
            onClick={onClose}
            className="p-1 text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Notifications list */}
      <div className="max-h-64 overflow-y-auto">
        {notifications.length === 0 ? (
          <div className="p-8 text-center">
            <div className="text-neutral-400 mb-2">
              <ExclamationTriangleIcon className="h-12 w-12 mx-auto" />
            </div>
            <p className="text-neutral-600 dark:text-neutral-400">
              No notifications yet
            </p>
            <p className="text-sm text-neutral-500 mt-1">
              We'll notify you when something important happens
            </p>
          </div>
        ) : (
          <div className="py-2">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className={`relative p-3 hover:bg-neutral-50 dark:hover:bg-neutral-700 cursor-pointer group ${
                  !notification.is_read ? 'bg-primary-50 dark:bg-primary-900/20' : ''
                }`}
                onClick={() => handleNotificationClick(notification)}
              >
                <div className="flex items-start gap-3">
                  {/* Icon */}
                  <div className="flex-shrink-0 mt-0.5">
                    {getNotificationIcon(notification.type)}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className={`text-sm font-medium ${
                          !notification.is_read 
                            ? 'text-neutral-900 dark:text-white' 
                            : 'text-neutral-700 dark:text-neutral-300'
                        }`}>
                          {notification.title}
                        </h4>
                        <p className={`text-sm mt-1 ${
                          !notification.is_read 
                            ? 'text-neutral-600 dark:text-neutral-300' 
                            : 'text-neutral-500 dark:text-neutral-400'
                        }`}>
                          {notification.message}
                        </p>
                        <p className="text-xs text-neutral-400 mt-1">
                          {formatTimeAgo(notification.created_at)}
                        </p>
                      </div>

                      {/* Actions */}
                      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        {!notification.is_read && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation()
                              markAsRead(notification.id)
                            }}
                            className="p-1 text-neutral-400 hover:text-green-600"
                            title="Mark as read"
                          >
                            <CheckIcon className="h-4 w-4" />
                          </button>
                        )}
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            deleteNotification(notification.id)
                          }}
                          className="p-1 text-neutral-400 hover:text-red-600"
                          title="Delete"
                        >
                          <XMarkIcon className="h-4 w-4" />
                        </button>
                      </div>
                    </div>

                    {/* Unread indicator */}
                    {!notification.is_read && (
                      <div className="absolute left-1 top-1/2 w-2 h-2 bg-primary-600 rounded-full transform -translate-y-1/2"></div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      {notifications.length > 0 && (
        <div className="p-3 border-t border-neutral-200 dark:border-neutral-700">
          <button
            onClick={() => {
              // Navigate to full notifications page
              window.location.href = '/notifications'
              onClose()
            }}
            className="w-full text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-center"
          >
            View all notifications
          </button>
        </div>
      )}
    </div>
  )
}

export default NotificationDropdown