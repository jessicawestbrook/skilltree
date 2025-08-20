import React, { useState } from 'react'
import { useNotifications } from '../contexts/NotificationContext'
import { Notification } from '../types/database.types'
import { 
  TrophyIcon,
  ChartBarIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  UserGroupIcon,
  XMarkIcon,
  CheckIcon,
  ArrowLeftIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline'
import { useNavigate } from 'react-router-dom'
// Simple date formatting functions instead of date-fns
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

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const NotificationsPage: React.FC = () => {
  const navigate = useNavigate()
  const { 
    notifications, 
    unreadCount, 
    loading, 
    markAsRead, 
    markAllAsRead, 
    deleteNotification 
  } = useNotifications()
  
  const [filter, setFilter] = useState<'all' | 'unread'>('all')
  const [typeFilter, setTypeFilter] = useState<string>('all')

  const getNotificationIcon = (type: Notification['type']) => {
    switch (type) {
      case 'achievement':
        return <TrophyIcon className="h-6 w-6 text-yellow-500" />
      case 'progress':
        return <ChartBarIcon className="h-6 w-6 text-blue-500" />
      case 'reminder':
        return <ClockIcon className="h-6 w-6 text-orange-500" />
      case 'system':
        return <ExclamationTriangleIcon className="h-6 w-6 text-red-500" />
      case 'social':
        return <UserGroupIcon className="h-6 w-6 text-green-500" />
      default:
        return <ExclamationTriangleIcon className="h-6 w-6 text-neutral-500" />
    }
  }

  const getTypeLabel = (type: Notification['type']) => {
    switch (type) {
      case 'achievement':
        return 'Achievement'
      case 'progress':
        return 'Progress'
      case 'reminder':
        return 'Reminder'
      case 'system':
        return 'System'
      case 'social':
        return 'Social'
      default:
        return 'Other'
    }
  }

  const filteredNotifications = notifications.filter(notification => {
    if (filter === 'unread' && notification.is_read) return false
    if (typeFilter !== 'all' && notification.type !== typeFilter) return false
    return true
  })

  const handleNotificationClick = async (notification: Notification) => {
    if (!notification.is_read) {
      await markAsRead(notification.id)
    }
    
    // Handle navigation based on notification data
    if (notification.data?.path) {
      navigate(notification.data.path)
    }
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-neutral-200 dark:bg-neutral-700 rounded w-1/3"></div>
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map(i => (
              <div key={i} className="h-20 bg-neutral-200 dark:bg-neutral-700 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center text-neutral-600 dark:text-neutral-400 hover:text-neutral-800 dark:hover:text-neutral-200 mb-4"
        >
          <ArrowLeftIcon className="h-4 w-4 mr-2" />
          Back
        </button>
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-neutral-900 dark:text-white">
              Notifications
            </h1>
            {unreadCount > 0 && (
              <p className="text-neutral-600 dark:text-neutral-400 mt-1">
                {unreadCount} unread notification{unreadCount !== 1 ? 's' : ''}
              </p>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors"
              >
                <CheckIcon className="h-4 w-4" />
                Mark All Read
              </button>
            )}
            
            <button
              onClick={() => navigate('/settings')}
              className="flex items-center gap-2 px-4 py-2 bg-neutral-200 dark:bg-neutral-700 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-700 dark:text-neutral-300 rounded-lg font-medium transition-colors"
            >
              <AdjustmentsHorizontalIcon className="h-4 w-4" />
              Settings
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300">
                Show:
              </span>
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value as 'all' | 'unread')}
                className="px-3 py-1 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">All notifications</option>
                <option value="unread">Unread only</option>
              </select>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300">
                Type:
              </span>
              <select
                value={typeFilter}
                onChange={(e) => setTypeFilter(e.target.value)}
                className="px-3 py-1 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">All types</option>
                <option value="achievement">Achievements</option>
                <option value="progress">Progress</option>
                <option value="reminder">Reminders</option>
                <option value="system">System</option>
                <option value="social">Social</option>
              </select>
            </div>
          </div>
          
          <div className="text-sm text-neutral-500">
            {filteredNotifications.length} notification{filteredNotifications.length !== 1 ? 's' : ''}
          </div>
        </div>
      </div>

      {/* Notifications */}
      <div className="space-y-2">
        {filteredNotifications.length === 0 ? (
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-12 text-center">
            <div className="text-neutral-400 mb-4">
              <ExclamationTriangleIcon className="h-16 w-16 mx-auto" />
            </div>
            <h3 className="text-xl font-semibold text-neutral-900 dark:text-white mb-2">
              No notifications found
            </h3>
            <p className="text-neutral-600 dark:text-neutral-400">
              {filter === 'unread' 
                ? "You're all caught up! No unread notifications."
                : "We'll notify you when something important happens."
              }
            </p>
          </div>
        ) : (
          filteredNotifications.map((notification) => (
            <div
              key={notification.id}
              className={`bg-white dark:bg-neutral-800 rounded-lg shadow-sm border transition-all cursor-pointer hover:shadow-md ${
                !notification.is_read 
                  ? 'border-primary-200 dark:border-primary-800 bg-primary-50 dark:bg-primary-900/10' 
                  : 'border-neutral-200 dark:border-neutral-700'
              }`}
              onClick={() => handleNotificationClick(notification)}
            >
              <div className="p-4">
                <div className="flex items-start gap-4">
                  {/* Icon */}
                  <div className="flex-shrink-0 mt-1">
                    {getNotificationIcon(notification.type)}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className={`font-semibold ${
                            !notification.is_read 
                              ? 'text-neutral-900 dark:text-white' 
                              : 'text-neutral-700 dark:text-neutral-300'
                          }`}>
                            {notification.title}
                          </h3>
                          <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${
                            notification.type === 'achievement' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' :
                            notification.type === 'progress' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400' :
                            notification.type === 'reminder' ? 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400' :
                            notification.type === 'system' ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' :
                            'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                          }`}>
                            {getTypeLabel(notification.type)}
                          </span>
                        </div>
                        
                        <p className={`text-sm mb-2 ${
                          !notification.is_read 
                            ? 'text-neutral-600 dark:text-neutral-300' 
                            : 'text-neutral-500 dark:text-neutral-400'
                        }`}>
                          {notification.message}
                        </p>
                        
                        <div className="flex items-center gap-4 text-xs text-neutral-400">
                          <span>
                            {formatTimeAgo(notification.created_at)}
                          </span>
                          <span>
                            {formatDate(notification.created_at)}
                          </span>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex items-center gap-1 ml-4">
                        {!notification.is_read && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation()
                              markAsRead(notification.id)
                            }}
                            className="p-2 text-neutral-400 hover:text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 rounded-lg transition-colors"
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
                          className="p-2 text-neutral-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                          title="Delete notification"
                        >
                          <XMarkIcon className="h-4 w-4" />
                        </button>
                      </div>
                    </div>

                    {/* Unread indicator */}
                    {!notification.is_read && (
                      <div className="absolute left-2 top-6 w-2 h-2 bg-primary-600 rounded-full"></div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default NotificationsPage