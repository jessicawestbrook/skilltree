import React, { useState, useEffect } from 'react'
import { Dialog } from '@headlessui/react'
import { 
  XMarkIcon, 
  ClockIcon, 
  CalendarIcon,
  BellIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'
import { studyReminderService, ReminderCreationData } from '../services/studyReminderService'
import { useNotifications } from '../contexts/NotificationContext'

interface StudyReminderModalProps {
  isOpen: boolean
  onClose: () => void
  contentType?: string
  contentIds?: string[]
  suggestedInterval?: number // Days until next review (from spaced repetition)
}

export const StudyReminderModal: React.FC<StudyReminderModalProps> = ({
  isOpen,
  onClose,
  contentType,
  contentIds,
  suggestedInterval
}) => {
  const { user } = useAuth()
  const { createNotification } = useNotifications()
  
  // Form state
  const [reminderType, setReminderType] = useState<'once' | 'recurring'>('once')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [duration, setDuration] = useState(15)
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium')
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  
  // Recurring options
  const [recurrencePattern, setRecurrencePattern] = useState<'daily' | 'weekly' | 'custom'>('daily')
  const [recurrenceDays, setRecurrenceDays] = useState<number[]>([])
  const [recurrenceEndDate, setRecurrenceEndDate] = useState('')
  
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Set default values based on props
  useEffect(() => {
    if (isOpen) {
      // Set default date based on suggested interval
      const defaultDate = new Date()
      if (suggestedInterval) {
        defaultDate.setDate(defaultDate.getDate() + suggestedInterval)
      } else {
        defaultDate.setDate(defaultDate.getDate() + 1) // Tomorrow by default
      }
      
      // Format date for input
      const dateStr = defaultDate.toISOString().split('T')[0]
      setDate(dateStr)
      
      // Set default time to 9 AM
      setTime('09:00')
      
      // Set default title
      if (contentType) {
        setTitle(`Review ${contentType} flashcards`)
        
        if (contentIds && contentIds.length > 0) {
          setDescription(`${contentIds.length} cards ready for review`)
          // Estimate duration based on card count (2 min per card, max 30 min)
          setDuration(Math.min(contentIds.length * 2, 30))
        }
      }
    }
  }, [isOpen, contentType, contentIds, suggestedInterval])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!user) return
    
    setLoading(true)
    setError('')
    
    try {
      // Combine date and time
      const scheduledFor = new Date(`${date}T${time}`)
      
      // Validate scheduled time is in the future
      if (scheduledFor <= new Date()) {
        throw new Error('Please select a future date and time')
      }
      
      const reminderData: ReminderCreationData = {
        type: contentType ? 'flashcard_review' : 'custom',
        contentType,
        contentIds,
        scheduledFor,
        title: title || undefined,
        description: description || undefined,
        duration,
        priority,
        isRecurring: reminderType === 'recurring',
        recurrencePattern: reminderType === 'recurring' ? recurrencePattern : undefined,
        recurrenceDays: reminderType === 'recurring' && recurrencePattern === 'custom' ? recurrenceDays : undefined,
        recurrenceEndDate: reminderType === 'recurring' && recurrenceEndDate ? new Date(recurrenceEndDate) : undefined
      }
      
      const reminder = await studyReminderService.createReminder(user.id, reminderData)
      
      if (reminder) {
        // Show success notification
        await createNotification(
          'system',
          'Reminder Set',
          `Study reminder scheduled for ${scheduledFor.toLocaleDateString()} at ${scheduledFor.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
        )
        
        onClose()
        resetForm()
      } else {
        throw new Error('Failed to create reminder')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create reminder')
    } finally {
      setLoading(false)
    }
  }
  
  const resetForm = () => {
    setReminderType('once')
    setDate('')
    setTime('')
    setDuration(15)
    setPriority('medium')
    setTitle('')
    setDescription('')
    setRecurrencePattern('daily')
    setRecurrenceDays([])
    setRecurrenceEndDate('')
    setError('')
  }
  
  const toggleDay = (day: number) => {
    setRecurrenceDays(prev =>
      prev.includes(day)
        ? prev.filter(d => d !== day)
        : [...prev, day].sort()
    )
  }
  
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

  return (
    <Dialog open={isOpen} onClose={onClose} className="relative z-50">
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
      
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <Dialog.Panel className="mx-auto max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-xl">
          <div className="p-6">
            <div className="flex justify-between items-center mb-4">
              <Dialog.Title className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <BellIcon className="h-5 w-5 mr-2 text-emerald-600" />
                Set Study Reminder
              </Dialog.Title>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
              >
                <XMarkIcon className="h-5 w-5" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Reminder Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Reminder Type
                </label>
                <div className="flex space-x-4">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      value="once"
                      checked={reminderType === 'once'}
                      onChange={(e) => setReminderType(e.target.value as 'once')}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700 dark:text-gray-300">One-time</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      value="recurring"
                      checked={reminderType === 'recurring'}
                      onChange={(e) => setReminderType(e.target.value as 'recurring')}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700 dark:text-gray-300">Recurring</span>
                  </label>
                </div>
              </div>
              
              {/* Date and Time */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    <CalendarIcon className="inline h-4 w-4 mr-1" />
                    Date
                  </label>
                  <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    required
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                             bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                             focus:ring-emerald-500 focus:border-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    <ClockIcon className="inline h-4 w-4 mr-1" />
                    Time
                  </label>
                  <input
                    type="time"
                    value={time}
                    onChange={(e) => setTime(e.target.value)}
                    required
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                             bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                             focus:ring-emerald-500 focus:border-emerald-500"
                  />
                </div>
              </div>
              
              {/* Recurring Options */}
              {reminderType === 'recurring' && (
                <div className="space-y-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      <ArrowPathIcon className="inline h-4 w-4 mr-1" />
                      Repeat
                    </label>
                    <select
                      value={recurrencePattern}
                      onChange={(e) => setRecurrencePattern(e.target.value as 'daily' | 'weekly' | 'custom')}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                               bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                               focus:ring-emerald-500 focus:border-emerald-500"
                    >
                      <option value="daily">Daily</option>
                      <option value="weekly">Weekly</option>
                      <option value="custom">Custom Days</option>
                    </select>
                  </div>
                  
                  {recurrencePattern === 'custom' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Select Days
                      </label>
                      <div className="flex space-x-1">
                        {dayNames.map((day, index) => (
                          <button
                            key={index}
                            type="button"
                            onClick={() => toggleDay(index)}
                            className={`px-2 py-1 text-xs rounded ${
                              recurrenceDays.includes(index)
                                ? 'bg-emerald-600 text-white'
                                : 'bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300'
                            }`}
                          >
                            {day}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      End Date (Optional)
                    </label>
                    <input
                      type="date"
                      value={recurrenceEndDate}
                      onChange={(e) => setRecurrenceEndDate(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                               bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                               focus:ring-emerald-500 focus:border-emerald-500"
                    />
                  </div>
                </div>
              )}
              
              {/* Title and Description */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Title
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g., Review Spanish vocabulary"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                           focus:ring-emerald-500 focus:border-emerald-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Description (Optional)
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Add notes about what to study..."
                  rows={2}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                           focus:ring-emerald-500 focus:border-emerald-500"
                />
              </div>
              
              {/* Duration and Priority */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Duration (minutes)
                  </label>
                  <input
                    type="number"
                    value={duration}
                    onChange={(e) => setDuration(Number(e.target.value))}
                    min="5"
                    max="120"
                    step="5"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                             bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                             focus:ring-emerald-500 focus:border-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Priority
                  </label>
                  <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                             bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                             focus:ring-emerald-500 focus:border-emerald-500"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>
              
              {/* Error Message */}
              {error && (
                <div className="text-red-600 dark:text-red-400 text-sm">
                  {error}
                </div>
              )}
              
              {/* Buttons */}
              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 
                           dark:hover:bg-gray-700 rounded-md transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-4 py-2 bg-emerald-600 text-white rounded-md 
                           hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed
                           transition-colors"
                >
                  {loading ? 'Setting...' : 'Set Reminder'}
                </button>
              </div>
            </form>
          </div>
        </Dialog.Panel>
      </div>
    </Dialog>
  )
}