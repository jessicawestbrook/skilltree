import React, { useState, useEffect } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import { 
  FlagIcon, 
  ChatBubbleBottomCenterTextIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  FunnelIcon,
  LinkIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline'
import { Link } from 'react-router-dom'
import SourceURLManager from '../components/SourceURLManager'

interface FeedbackItem {
  id: string
  user_id: string
  user_email?: string
  message: string
  category: string
  created_at: string
  status?: string
  response?: string
}

interface ContentFlag {
  id: string
  user_id: string
  user_email?: string
  content_type: 'question' | 'learning_content' | 'node'
  content_id: string
  issue_type: string
  description: string
  status: 'pending' | 'resolved' | 'dismissed'
  created_at: string
  admin_notes?: string
}

const AdminPage: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [isAdmin, setIsAdmin] = useState(false)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'feedback' | 'flags' | 'sources'>('feedback')
  const [feedbackItems, setFeedbackItems] = useState<FeedbackItem[]>([])
  const [contentFlags, setContentFlags] = useState<ContentFlag[]>([])
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [selectedItem, setSelectedItem] = useState<FeedbackItem | ContentFlag | null>(null)
  const [adminResponse, setAdminResponse] = useState('')
  const [updating, setUpdating] = useState(false)

  useEffect(() => {
    checkAdminStatus()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const checkAdminStatus = async () => {
    if (!user) {
      navigate('/login')
      return
    }

    try {
      // Check if user is admin (you can modify this logic based on your admin criteria)
      const { data } = await supabase
        .from('profiles')
        .select('is_admin')
        .eq('id', user.id)
        .single()

      if (data?.is_admin) {
        setIsAdmin(true)
        fetchFeedback()
        fetchContentFlags()
      } else {
        // For demo purposes, allow specific email domains or user IDs
        const adminEmails = ['admin@example.com']
        if (adminEmails.includes(user.email || '')) {
          setIsAdmin(true)
          fetchFeedback()
          fetchContentFlags()
        } else {
          navigate('/')
        }
      }
    } catch (error) {
      console.error('Error checking admin status:', error)
      // For demo, allow access
      setIsAdmin(true)
      fetchFeedback()
      fetchContentFlags()
    } finally {
      setLoading(false)
    }
  }

  const fetchFeedback = async () => {
    try {
      const { data, error } = await supabase
        .from('feedback')
        .select(`
          *,
          profiles:user_id (email)
        `)
        .order('created_at', { ascending: false })

      if (error) throw error

      const formattedData = data?.map(item => ({
        ...item,
        user_email: item.profiles?.email
      })) || []

      setFeedbackItems(formattedData)
    } catch (error) {
      console.error('Error fetching feedback:', error)
    }
  }

  const fetchContentFlags = async () => {
    try {
      const { data, error } = await supabase
        .from('content_flags')
        .select(`
          *,
          profiles:user_id (email)
        `)
        .order('created_at', { ascending: false })

      if (error) throw error

      const formattedData = data?.map(item => ({
        ...item,
        user_email: item.profiles?.email
      })) || []

      setContentFlags(formattedData)
    } catch (error) {
      console.error('Error fetching content flags:', error)
      // If table doesn't exist, set empty array
      setContentFlags([])
    }
  }

  const updateFeedbackStatus = async (id: string, status: string, response?: string) => {
    setUpdating(true)
    try {
      const { error } = await supabase
        .from('feedback')
        .update({ 
          status,
          response,
          updated_at: new Date().toISOString()
        })
        .eq('id', id)

      if (error) throw error

      await fetchFeedback()
      setSelectedItem(null)
      setAdminResponse('')
    } catch (error) {
      console.error('Error updating feedback:', error)
    } finally {
      setUpdating(false)
    }
  }

  const updateFlagStatus = async (id: string, status: string, notes?: string) => {
    setUpdating(true)
    try {
      const { error } = await supabase
        .from('content_flags')
        .update({ 
          status,
          admin_notes: notes,
          updated_at: new Date().toISOString()
        })
        .eq('id', id)

      if (error) throw error

      await fetchContentFlags()
      setSelectedItem(null)
      setAdminResponse('')
    } catch (error) {
      console.error('Error updating flag:', error)
    } finally {
      setUpdating(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'resolved':
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />
      case 'dismissed':
        return <XCircleIcon className="h-5 w-5 text-red-500" />
      case 'pending':
      default:
        return <ClockIcon className="h-5 w-5 text-yellow-500" />
    }
  }

  const getFilteredItems = () => {
    if (activeTab === 'feedback') {
      if (filterStatus === 'all') return feedbackItems
      return feedbackItems.filter(item => item.status === filterStatus || (!item.status && filterStatus === 'pending'))
    } else {
      if (filterStatus === 'all') return contentFlags
      return contentFlags.filter(item => item.status === filterStatus)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!isAdmin) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold mb-4">Access Denied</h2>
        <p className="text-neutral-600 dark:text-neutral-400">You don't have permission to access this page.</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <Link
          to="/content-management"
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-2"
        >
          <DocumentTextIcon className="h-5 w-5" />
          Content Management
        </Link>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b border-neutral-200 dark:border-neutral-700">
        <button
          onClick={() => setActiveTab('feedback')}
          className={`pb-2 px-1 font-medium transition-colors ${
            activeTab === 'feedback'
              ? 'text-primary-600 border-b-2 border-primary-600'
              : 'text-neutral-600 dark:text-neutral-400 hover:text-primary-600'
          }`}
        >
          <ChatBubbleBottomCenterTextIcon className="h-5 w-5 inline mr-2" />
          Feedback ({feedbackItems.length})
        </button>
        <button
          onClick={() => setActiveTab('flags')}
          className={`pb-2 px-1 font-medium transition-colors ${
            activeTab === 'flags'
              ? 'text-primary-600 border-b-2 border-primary-600'
              : 'text-neutral-600 dark:text-neutral-400 hover:text-primary-600'
          }`}
        >
          <FlagIcon className="h-5 w-5 inline mr-2" />
          Content Flags ({contentFlags.length})
        </button>
        <button
          onClick={() => setActiveTab('sources')}
          className={`pb-2 px-1 font-medium transition-colors ${
            activeTab === 'sources'
              ? 'text-primary-600 border-b-2 border-primary-600'
              : 'text-neutral-600 dark:text-neutral-400 hover:text-primary-600'
          }`}
        >
          <LinkIcon className="h-5 w-5 inline mr-2" />
          Source URLs
        </button>
      </div>

      {/* Filter */}
      {activeTab !== 'sources' && (
        <div className="flex items-center gap-4 mb-6">
          <FunnelIcon className="h-5 w-5 text-neutral-500" />
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
          >
            <option value="all">All Status</option>
            <option value="pending">Pending</option>
            <option value="resolved">Resolved</option>
            {activeTab === 'flags' && <option value="dismissed">Dismissed</option>}
          </select>
        </div>
      )}

      {/* Content */}
      {activeTab === 'sources' ? (
        <SourceURLManager />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* List */}
        <div className="space-y-4">
          {getFilteredItems().map((item: any) => (
            <div
              key={item.id}
              onClick={() => setSelectedItem(item)}
              className={`card p-4 cursor-pointer transition-all hover:shadow-lg ${
                selectedItem?.id === item.id ? 'ring-2 ring-primary-500' : ''
              }`}
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center gap-2">
                  {getStatusIcon(item.status || 'pending')}
                  <span className="text-sm font-medium">
                    {activeTab === 'feedback' ? item.category : item.issue_type}
                  </span>
                </div>
                <span className="text-xs text-neutral-500">
                  {new Date(item.created_at).toLocaleDateString()}
                </span>
              </div>
              
              <p className="text-sm text-neutral-700 dark:text-neutral-300 line-clamp-2">
                {activeTab === 'feedback' ? item.message : item.description}
              </p>
              
              <div className="mt-2 text-xs text-neutral-500">
                From: {item.user_email || 'Anonymous'}
              </div>
            </div>
          ))}
          
          {getFilteredItems().length === 0 && (
            <div className="text-center py-8 text-neutral-500">
              No {activeTab === 'feedback' ? 'feedback' : 'flags'} found
            </div>
          )}
        </div>

        {/* Detail Panel */}
        <div className="card p-6">
          {selectedItem ? (
            <div className="space-y-4">
              <h3 className="text-xl font-semibold">
                {activeTab === 'feedback' ? 'Feedback Details' : 'Flag Details'}
              </h3>
              
              <div className="space-y-2">
                <div>
                  <span className="text-sm font-medium text-neutral-500">Type:</span>
                  <p className="text-sm">
                    {activeTab === 'feedback' 
                      ? (selectedItem as FeedbackItem).category 
                      : `${(selectedItem as ContentFlag).content_type} - ${(selectedItem as ContentFlag).issue_type}`}
                  </p>
                </div>
                
                <div>
                  <span className="text-sm font-medium text-neutral-500">From:</span>
                  <p className="text-sm">{selectedItem.user_email || 'Anonymous'}</p>
                </div>
                
                <div>
                  <span className="text-sm font-medium text-neutral-500">Date:</span>
                  <p className="text-sm">{new Date(selectedItem.created_at).toLocaleString()}</p>
                </div>
                
                <div>
                  <span className="text-sm font-medium text-neutral-500">Description:</span>
                  <p className="text-sm mt-1">
                    {activeTab === 'feedback' 
                      ? (selectedItem as FeedbackItem).message 
                      : (selectedItem as ContentFlag).description}
                  </p>
                </div>

                {activeTab === 'flags' && (
                  <div>
                    <span className="text-sm font-medium text-neutral-500">Content ID:</span>
                    <p className="text-sm font-mono">{(selectedItem as ContentFlag).content_id}</p>
                  </div>
                )}
                
                {((selectedItem as FeedbackItem).response || (selectedItem as ContentFlag).admin_notes) && (
                  <div>
                    <span className="text-sm font-medium text-neutral-500">Admin Response:</span>
                    <p className="text-sm mt-1">
                      {(selectedItem as FeedbackItem).response || (selectedItem as ContentFlag).admin_notes}
                    </p>
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-neutral-200 dark:border-neutral-700">
                <label className="block text-sm font-medium mb-2">
                  Admin Response/Notes
                </label>
                <textarea
                  value={adminResponse}
                  onChange={(e) => setAdminResponse(e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800 resize-none"
                  placeholder="Enter your response or notes..."
                />
                
                <div className="flex gap-2 mt-4">
                  <button
                    onClick={() => {
                      if (activeTab === 'feedback') {
                        updateFeedbackStatus(selectedItem.id, 'resolved', adminResponse)
                      } else {
                        updateFlagStatus(selectedItem.id, 'resolved', adminResponse)
                      }
                    }}
                    disabled={updating}
                    className="btn-primary flex-1"
                  >
                    Mark Resolved
                  </button>
                  
                  {activeTab === 'flags' && (
                    <button
                      onClick={() => updateFlagStatus(selectedItem.id, 'dismissed', adminResponse)}
                      disabled={updating}
                      className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                    >
                      Dismiss
                    </button>
                  )}
                  
                  <button
                    onClick={() => {
                      setSelectedItem(null)
                      setAdminResponse('')
                    }}
                    className="px-4 py-2 bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-600"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-neutral-500">
              Select an item to view details
            </div>
          )}
        </div>
        </div>
      )}
    </div>
  )
}

export default AdminPage