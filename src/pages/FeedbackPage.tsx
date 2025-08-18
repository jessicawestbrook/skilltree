import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import { Feedback } from '../types/database.types'
import { ChatBubbleBottomCenterTextIcon } from '@heroicons/react/24/outline'

const FeedbackPage: React.FC = () => {
  const { user } = useAuth()
  const [category, setCategory] = useState<Feedback['category']>('general')
  const [message, setMessage] = useState('')
  const [feedbackList, setFeedbackList] = useState<Feedback[]>([])
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (user) {
      fetchUserFeedback()
    }
  }, [user])

  const fetchUserFeedback = async () => {
    if (!user) return

    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('feedback')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })

      if (error) throw error
      setFeedbackList(data || [])
    } catch (error) {
      console.error('Error fetching feedback:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!user || !message.trim()) return

    setSubmitting(true)
    try {
      const { error } = await supabase
        .from('feedback')
        .insert({
          user_id: user.id,
          category,
          message,
          status: 'open'
        })

      if (error) throw error

      setMessage('')
      alert('Feedback submitted successfully!')
      fetchUserFeedback()
    } catch (error) {
      console.error('Error submitting feedback:', error)
      alert('Failed to submit feedback')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Feedback & Support</h1>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Submit Feedback</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value as Feedback['category'])}
              className="input-field"
            >
              <option value="general">General Feedback</option>
              <option value="bug">Bug Report</option>
              <option value="content_request">Content Request</option>
              <option value="question_issue">Question Issue</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Message</label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={5}
              className="input-field resize-none"
              placeholder="Describe your feedback or issue..."
              required
            />
          </div>

          <button
            type="submit"
            disabled={submitting || !message.trim()}
            className="btn-primary disabled:opacity-50"
          >
            {submitting ? 'Submitting...' : 'Submit Feedback'}
          </button>
        </form>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Your Feedback History</h2>
        
        {loading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
        ) : feedbackList.length === 0 ? (
          <p className="text-neutral-600 dark:text-neutral-400">
            No feedback submitted yet
          </p>
        ) : (
          <div className="space-y-4">
            {feedbackList.map((feedback) => (
              <div 
                key={feedback.id}
                className="border border-neutral-200 dark:border-neutral-700 rounded-lg p-4"
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <ChatBubbleBottomCenterTextIcon className="h-5 w-5 text-primary-600" />
                    <span className="text-sm font-medium capitalize">
                      {feedback.category.replace('_', ' ')}
                    </span>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded ${
                    feedback.status === 'resolved' 
                      ? 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
                      : feedback.status === 'in_progress'
                      ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400'
                      : 'bg-neutral-100 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-400'
                  }`}>
                    {feedback.status}
                  </span>
                </div>
                
                <p className="text-sm mb-2">{feedback.message}</p>
                
                {feedback.admin_response && (
                  <div className="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded">
                    <p className="text-xs font-medium text-blue-700 dark:text-blue-400 mb-1">
                      Admin Response:
                    </p>
                    <p className="text-sm">{feedback.admin_response}</p>
                  </div>
                )}
                
                <p className="text-xs text-neutral-500 mt-2">
                  {new Date(feedback.created_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default FeedbackPage