import React, { useState, useEffect } from 'react'
import { 
  BellIcon, 
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  CalendarDaysIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'
import { studyReminderService, StudyReminder } from '../services/studyReminderService'
import { StudyReminderModal } from './StudyReminderModal'

export const StudyRemindersPanel: React.FC = () => {
  const { user } = useAuth()
  const [reminders, setReminders] = useState<StudyReminder[]>([])
  const [overdueReminders, setOverdueReminders] = useState<StudyReminder[]>([])
  const [loading, setLoading] = useState(true)
  const [showReminderModal, setShowReminderModal] = useState(false)

  useEffect(() => {
    if (user) {
      loadReminders()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const loadReminders = async () => {
    if (!user) return
    
    setLoading(true)
    try {
      const [upcoming, overdue] = await Promise.all([
        studyReminderService.getUpcomingReminders(user.id),
        studyReminderService.getOverdueReminders(user.id)
      ])
      
      setReminders(upcoming)
      setOverdueReminders(overdue)
    } catch (error) {
      console.error('Error loading reminders:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleComplete = async (reminderId: string) => {
    const success = await studyReminderService.completeReminder(reminderId)
    if (success) {
      loadReminders()
    }
  }

  const handleDismiss = async (reminderId: string) => {
    const success = await studyReminderService.dismissReminder(reminderId)
    if (success) {
      loadReminders()
    }
  }

  const handleDelete = async (reminderId: string) => {
    if (window.confirm('Are you sure you want to delete this reminder?')) {
      const success = await studyReminderService.deleteReminder(reminderId)
      if (success) {
        loadReminders()
      }
    }
  }

  const formatDateTime = (dateStr: string) => {
    const date = new Date(dateStr)
    const today = new Date()
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    
    let dateLabel = ''
    if (date.toDateString() === today.toDateString()) {
      dateLabel = 'Today'
    } else if (date.toDateString() === tomorrow.toDateString()) {
      dateLabel = 'Tomorrow'
    } else {
      dateLabel = date.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' })
    }
    
    const timeStr = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    
    return `${dateLabel} at ${timeStr}`
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-red-600 dark:text-red-400'
      case 'medium':
        return 'text-yellow-600 dark:text-yellow-400'
      case 'low':
        return 'text-gray-600 dark:text-gray-400'
      default:
        return 'text-gray-600 dark:text-gray-400'
    }
  }

  if (loading) {
    return (
      <div className="p-4 text-center text-gray-500 dark:text-gray-400">
        Loading reminders...
      </div>
    )
  }

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <BellIcon className="h-5 w-5 mr-2 text-emerald-600" />
          Study Reminders
        </h3>
        <button
          onClick={() => setShowReminderModal(true)}
          className="px-3 py-1 bg-emerald-600 text-white text-sm rounded-md hover:bg-emerald-700 transition-colors"
        >
          Add Reminder
        </button>
      </div>

      {/* Overdue Reminders */}
      {overdueReminders.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-medium text-red-600 dark:text-red-400 mb-2 flex items-center">
            <ExclamationTriangleIcon className="h-4 w-4 mr-1" />
            Overdue ({overdueReminders.length})
          </h4>
          <div className="space-y-2">
            {overdueReminders.map((reminder) => (
              <ReminderCard
                key={reminder.id}
                reminder={reminder}
                isOverdue={true}
                onComplete={handleComplete}
                onDismiss={handleDismiss}
                onDelete={handleDelete}
                formatDateTime={formatDateTime}
                getPriorityColor={getPriorityColor}
              />
            ))}
          </div>
        </div>
      )}

      {/* Upcoming Reminders */}
      {reminders.length > 0 ? (
        <div>
          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Upcoming ({reminders.length})
          </h4>
          <div className="space-y-2">
            {reminders.map((reminder) => (
              <ReminderCard
                key={reminder.id}
                reminder={reminder}
                isOverdue={false}
                onComplete={handleComplete}
                onDismiss={handleDismiss}
                onDelete={handleDelete}
                formatDateTime={formatDateTime}
                getPriorityColor={getPriorityColor}
              />
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
          <CalendarDaysIcon className="h-12 w-12 mx-auto mb-2 opacity-50" />
          <p>No upcoming reminders</p>
          <p className="text-sm mt-1">Create a reminder to stay on track!</p>
        </div>
      )}

      {/* Reminder Modal */}
      <StudyReminderModal
        isOpen={showReminderModal}
        onClose={() => {
          setShowReminderModal(false)
          loadReminders()
        }}
      />
    </div>
  )
}

// Reminder Card Component
interface ReminderCardProps {
  reminder: StudyReminder
  isOverdue: boolean
  onComplete: (id: string) => void
  onDismiss: (id: string) => void
  onDelete: (id: string) => void
  formatDateTime: (date: string) => string
  getPriorityColor: (priority: string) => string
}

const ReminderCard: React.FC<ReminderCardProps> = ({
  reminder,
  isOverdue,
  onComplete,
  onDismiss,
  onDelete,
  formatDateTime,
  getPriorityColor
}) => {
  return (
    <div className={`p-3 rounded-lg border ${
      isOverdue 
        ? 'border-red-300 dark:border-red-700 bg-red-50 dark:bg-red-900/20' 
        : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800'
    }`}>
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <div className="flex items-center mb-1">
            <span className={`text-sm font-medium ${
              isOverdue ? 'text-red-700 dark:text-red-300' : 'text-gray-900 dark:text-white'
            }`}>
              {reminder.title}
            </span>
            {reminder.is_recurring && (
              <span className="ml-2 px-2 py-0.5 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 text-xs rounded-full">
                Recurring
              </span>
            )}
            <span className={`ml-2 text-xs ${getPriorityColor(reminder.priority)}`}>
              {reminder.priority}
            </span>
          </div>
          
          {reminder.description && (
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
              {reminder.description}
            </p>
          )}
          
          <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
            <ClockIcon className="h-3 w-3 mr-1" />
            {formatDateTime(reminder.scheduled_for)}
            {reminder.study_duration_minutes && (
              <span className="ml-2">• {reminder.study_duration_minutes} min</span>
            )}
          </div>
        </div>
        
        <div className="flex space-x-1 ml-2">
          <button
            onClick={() => onComplete(reminder.id)}
            className="p-1 text-green-600 hover:text-green-700 dark:text-green-400 dark:hover:text-green-300"
            title="Mark as complete"
          >
            <CheckCircleIcon className="h-5 w-5" />
          </button>
          <button
            onClick={() => onDismiss(reminder.id)}
            className="p-1 text-gray-600 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
            title="Dismiss"
          >
            <XCircleIcon className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  )
}