import React, { useState } from 'react'
import { XMarkIcon, FlagIcon } from '@heroicons/react/24/outline'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'

interface FlagContentModalProps {
  isOpen: boolean
  onClose: () => void
  contentType: 'question' | 'learning_content' | 'node'
  contentId: string
  contentTitle?: string
}

const FlagContentModal: React.FC<FlagContentModalProps> = ({
  isOpen,
  onClose,
  contentType,
  contentId,
  contentTitle
}) => {
  const { user } = useAuth()
  const [issueType, setIssueType] = useState<string>('')
  const [description, setDescription] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  const issueTypes = {
    question: [
      'Incorrect answer',
      'Unclear question',
      'Grammatical error',
      'Missing information',
      'Technical issue',
      'Other'
    ],
    learning_content: [
      'Incorrect information',
      'Outdated content',
      'Grammatical error',
      'Missing images',
      'Too difficult',
      'Too easy',
      'Other'
    ],
    node: [
      'Wrong category',
      'Duplicate content',
      'Missing content',
      'Incorrect hierarchy',
      'Other'
    ]
  }

  const handleSubmit = async () => {
    if (!user) {
      alert('Please sign in to flag content')
      return
    }

    if (!issueType || !description.trim()) {
      alert('Please select an issue type and provide a description')
      return
    }

    setSubmitting(true)

    try {
      const { error } = await supabase
        .from('content_flags')
        .insert({
          user_id: user.id,
          content_type: contentType,
          content_id: contentId,
          issue_type: issueType,
          description: description.trim(),
          status: 'pending'
        })

      if (error) throw error

      setSubmitted(true)
      setTimeout(() => {
        onClose()
        // Reset state after closing
        setTimeout(() => {
          setIssueType('')
          setDescription('')
          setSubmitted(false)
        }, 300)
      }, 2000)
    } catch (error) {
      console.error('Error submitting flag:', error)
      alert('Failed to submit flag. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-2xl max-w-md w-full">
        <div className="flex justify-between items-center p-4 border-b border-neutral-200 dark:border-neutral-700">
          <div className="flex items-center gap-2">
            <FlagIcon className="h-5 w-5 text-red-500" />
            <h2 className="text-lg font-semibold">Report an Issue</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>

        <div className="p-4 space-y-4">
          {submitted ? (
            <div className="text-center py-8">
              <div className="text-green-600 dark:text-green-400 mb-2">
                <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-lg font-medium">Thank you for your feedback!</p>
              <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-1">
                We'll review your report and take appropriate action.
              </p>
            </div>
          ) : (
            <>
              {contentTitle && (
                <div className="text-sm text-neutral-600 dark:text-neutral-400">
                  Reporting issue with: <span className="font-medium">{contentTitle}</span>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium mb-2">
                  Issue Type
                </label>
                <select
                  value={issueType}
                  onChange={(e) => setIssueType(e.target.value)}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800 focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Select an issue type</option>
                  {issueTypes[contentType].map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Description
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Please describe the issue in detail..."
                  rows={4}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
                />
              </div>

              {!user && (
                <div className="text-sm text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-900/20 p-3 rounded-lg">
                  Please sign in to report issues
                </div>
              )}

              <div className="flex gap-2">
                <button
                  onClick={onClose}
                  className="flex-1 px-4 py-2 bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSubmit}
                  disabled={submitting || !user || !issueType || !description.trim()}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {submitting ? 'Submitting...' : 'Submit Report'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default FlagContentModal