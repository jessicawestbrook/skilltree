import React, { useState, useEffect } from 'react'
import { 
  BellIcon, 
  DevicePhoneMobileIcon,
  EnvelopeIcon,
  CalendarDaysIcon,
  ClockIcon,
  CheckIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'
import { useNotifications } from '../contexts/NotificationContext'
import { pushNotificationService } from '../services/pushNotificationService'
import { studyReminderService, StudySchedule } from '../services/studyReminderService'
import { StudyRemindersPanel } from '../components/StudyRemindersPanel'

export const NotificationSettingsPage: React.FC = () => {
  const { user } = useAuth()
  const { preferences, updatePreferences } = useNotifications()
  
  // Notification preferences
  const [emailNotifications, setEmailNotifications] = useState(true)
  const [pushEnabled, setPushEnabled] = useState(false)
  const [achievementNotifications, setAchievementNotifications] = useState(true)
  const [progressNotifications, setProgressNotifications] = useState(true)
  const [reminderNotifications, setReminderNotifications] = useState(true)
  const [systemNotifications, setSystemNotifications] = useState(true)
  
  // Study schedule settings
  const [scheduleName, setScheduleName] = useState('Daily Study')
  const [preferredTime, setPreferredTime] = useState('09:00')
  const [preferredDays, setPreferredDays] = useState<number[]>([1, 2, 3, 4, 5]) // Mon-Fri
  const [sessionDuration, setSessionDuration] = useState(15)
  const [cardsPerSession, setCardsPerSession] = useState(20)
  const [autoScheduleReviews, setAutoScheduleReviews] = useState(true)
  const [includeOverdue, setIncludeOverdue] = useState(true)
  
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    loadSettings()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const loadSettings = async () => {
    if (!user) return
    
    setLoading(true)
    try {
      // Load notification preferences
      if (preferences) {
        setEmailNotifications(preferences.email_notifications ?? true)
        setAchievementNotifications(preferences.achievement_notifications ?? true)
        setProgressNotifications(preferences.progress_notifications ?? true)
        setReminderNotifications(preferences.reminder_notifications ?? true)
        setSystemNotifications(preferences.system_notifications ?? true)
      }
      
      // Check push notification status
      const pushStatus = await pushNotificationService.isPushEnabled()
      setPushEnabled(pushStatus)
      
      // Load study schedule
      const activeSchedule = await studyReminderService.getUserActiveSchedule(user.id)
      if (activeSchedule) {
        setScheduleName(activeSchedule.schedule_name)
        setPreferredTime(activeSchedule.preferred_time)
        setPreferredDays(activeSchedule.preferred_days || [])
        setSessionDuration(activeSchedule.session_duration_minutes)
        setCardsPerSession(activeSchedule.cards_per_session)
        setAutoScheduleReviews(activeSchedule.auto_schedule_reviews)
        setIncludeOverdue(activeSchedule.include_overdue)
      }
    } catch (error) {
      console.error('Error loading settings:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSavePreferences = async () => {
    if (!user) return
    
    setSaving(true)
    setMessage('')
    
    try {
      // Update notification preferences
      await updatePreferences({
        email_notifications: emailNotifications,
        push_notifications: pushEnabled,
        achievement_notifications: achievementNotifications,
        progress_notifications: progressNotifications,
        reminder_notifications: reminderNotifications,
        system_notifications: systemNotifications
      })
      
      // Update or create study schedule
      const scheduleData: Partial<StudySchedule> = {
        schedule_name: scheduleName,
        is_active: true,
        preferred_days: preferredDays,
        preferred_time: preferredTime,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        session_duration_minutes: sessionDuration,
        cards_per_session: cardsPerSession,
        auto_schedule_reviews: autoScheduleReviews,
        include_overdue: includeOverdue
      }
      
      await studyReminderService.upsertSchedule(user.id, scheduleData)
      
      setMessage('Settings saved successfully!')
      setTimeout(() => setMessage(''), 3000)
    } catch (error) {
      console.error('Error saving preferences:', error)
      setMessage('Error saving settings')
    } finally {
      setSaving(false)
    }
  }

  const handleTogglePush = async () => {
    if (pushEnabled) {
      // Disable push notifications
      const success = await pushNotificationService.unsubscribe()
      if (success) {
        setPushEnabled(false)
      }
    } else {
      // Enable push notifications
      const permission = await pushNotificationService.requestPermission()
      if (permission === 'granted') {
        await pushNotificationService.initialize()
        const subscription = await pushNotificationService.subscribeToPush()
        if (subscription) {
          setPushEnabled(true)
          
          // Show test notification
          await pushNotificationService.showNotification(
            'Push Notifications Enabled',
            {
              body: 'You will now receive study reminders!',
              icon: '/icon-192x192.png'
            }
          )
        }
      }
    }
  }

  const toggleDay = (day: number) => {
    setPreferredDays(prev =>
      prev.includes(day)
        ? prev.filter(d => d !== day)
        : [...prev, day].sort()
    )
  }

  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center py-12">Loading settings...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 flex items-center">
          <BellIcon className="h-8 w-8 mr-3 text-emerald-600" />
          Notification Settings
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Notification Preferences */}
          <div className="space-y-6">
            {/* Notification Types */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Notification Types
              </h2>
              
              <div className="space-y-4">
                {/* Push Notifications */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <DevicePhoneMobileIcon className="h-5 w-5 mr-3 text-gray-600 dark:text-gray-400" />
                    <div>
                      <label className="text-sm font-medium text-gray-900 dark:text-white">
                        Push Notifications
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Browser notifications for reminders
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={handleTogglePush}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      pushEnabled ? 'bg-emerald-600' : 'bg-gray-300 dark:bg-gray-600'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        pushEnabled ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>

                {/* Email Notifications */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <EnvelopeIcon className="h-5 w-5 mr-3 text-gray-600 dark:text-gray-400" />
                    <div>
                      <label className="text-sm font-medium text-gray-900 dark:text-white">
                        Email Notifications
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Daily digest and important updates
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => setEmailNotifications(!emailNotifications)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      emailNotifications ? 'bg-emerald-600' : 'bg-gray-300 dark:bg-gray-600'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        emailNotifications ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>

                <hr className="border-gray-200 dark:border-gray-700" />

                {/* Achievement Notifications */}
                <label className="flex items-center justify-between">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Achievement Notifications</span>
                  <input
                    type="checkbox"
                    checked={achievementNotifications}
                    onChange={(e) => setAchievementNotifications(e.target.checked)}
                    className="h-4 w-4 text-emerald-600 rounded"
                  />
                </label>

                {/* Progress Notifications */}
                <label className="flex items-center justify-between">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Progress Updates</span>
                  <input
                    type="checkbox"
                    checked={progressNotifications}
                    onChange={(e) => setProgressNotifications(e.target.checked)}
                    className="h-4 w-4 text-emerald-600 rounded"
                  />
                </label>

                {/* Reminder Notifications */}
                <label className="flex items-center justify-between">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Study Reminders</span>
                  <input
                    type="checkbox"
                    checked={reminderNotifications}
                    onChange={(e) => setReminderNotifications(e.target.checked)}
                    className="h-4 w-4 text-emerald-600 rounded"
                  />
                </label>

                {/* System Notifications */}
                <label className="flex items-center justify-between">
                  <span className="text-sm text-gray-700 dark:text-gray-300">System Notifications</span>
                  <input
                    type="checkbox"
                    checked={systemNotifications}
                    onChange={(e) => setSystemNotifications(e.target.checked)}
                    className="h-4 w-4 text-emerald-600 rounded"
                  />
                </label>
              </div>
            </div>

            {/* Study Schedule */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <CalendarDaysIcon className="h-5 w-5 mr-2 text-emerald-600" />
                Study Schedule
              </h2>

              <div className="space-y-4">
                {/* Schedule Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Schedule Name
                  </label>
                  <input
                    type="text"
                    value={scheduleName}
                    onChange={(e) => setScheduleName(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                             bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  />
                </div>

                {/* Preferred Time */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    <ClockIcon className="inline h-4 w-4 mr-1" />
                    Preferred Study Time
                  </label>
                  <input
                    type="time"
                    value={preferredTime}
                    onChange={(e) => setPreferredTime(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                             bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  />
                </div>

                {/* Preferred Days */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Study Days
                  </label>
                  <div className="flex space-x-1">
                    {dayNames.map((day, index) => (
                      <button
                        key={index}
                        type="button"
                        onClick={() => toggleDay(index)}
                        className={`px-3 py-1 text-xs rounded ${
                          preferredDays.includes(index)
                            ? 'bg-emerald-600 text-white'
                            : 'bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300'
                        }`}
                      >
                        {day}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Session Settings */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Session Duration (min)
                    </label>
                    <input
                      type="number"
                      value={sessionDuration}
                      onChange={(e) => setSessionDuration(Number(e.target.value))}
                      min="5"
                      max="60"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                               bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Cards per Session
                    </label>
                    <input
                      type="number"
                      value={cardsPerSession}
                      onChange={(e) => setCardsPerSession(Number(e.target.value))}
                      min="5"
                      max="100"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                               bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                  </div>
                </div>

                {/* Auto-scheduling Options */}
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={autoScheduleReviews}
                      onChange={(e) => setAutoScheduleReviews(e.target.checked)}
                      className="h-4 w-4 text-emerald-600 rounded mr-2"
                    />
                    <span className="text-sm text-gray-700 dark:text-gray-300">
                      Automatically schedule spaced repetition reviews
                    </span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={includeOverdue}
                      onChange={(e) => setIncludeOverdue(e.target.checked)}
                      className="h-4 w-4 text-emerald-600 rounded mr-2"
                    />
                    <span className="text-sm text-gray-700 dark:text-gray-300">
                      Include overdue cards in sessions
                    </span>
                  </label>
                </div>
              </div>
            </div>

            {/* Save Button */}
            <div className="flex items-center space-x-4">
              <button
                onClick={handleSavePreferences}
                disabled={saving}
                className="px-6 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 
                         disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {saving ? 'Saving...' : 'Save Settings'}
              </button>
              {message && (
                <div className={`text-sm flex items-center ${
                  message.includes('Error') ? 'text-red-600' : 'text-green-600'
                }`}>
                  {!message.includes('Error') && <CheckIcon className="h-4 w-4 mr-1" />}
                  {message}
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Active Reminders */}
          <div>
            <StudyRemindersPanel />
          </div>
        </div>
      </div>
    </div>
  )
}