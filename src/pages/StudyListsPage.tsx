import React, { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { studyListService } from '../services/studyListService'
import { checkStudyListTables, createStudyListTables } from '../utils/createStudyListTables'
import { StudyList, StarredItem, StudyListItem } from '../types/database.types'
import { nameToSlug } from '../utils/studyListSlug'
import {
  PlayIcon,
  CloudArrowUpIcon
} from '@heroicons/react/24/outline'
import CustomQuestionUploader from '../components/CustomQuestionUploader'
import StudyListsDragDrop from '../components/StudyListsDragDrop'

const StudyListsPage: React.FC = () => {
  const { user } = useAuth()
  const { listSlug } = useParams<{ listSlug?: string }>()
  const navigate = useNavigate()
  const [studyLists, setStudyLists] = useState<StudyList[]>([])
  const [starredItems, setStarredItems] = useState<StarredItem[]>([])
  const [loading, setLoading] = useState(true)
  const [tablesExist, setTablesExist] = useState<boolean | null>(null)
  const [selectedList, setSelectedList] = useState<StudyList | null>(null)
  const [showBatchSettings, setShowBatchSettings] = useState(false)
  const [batchSize, setBatchSize] = useState(() => {
    // Load saved batch size from localStorage or default to 20
    const saved = localStorage.getItem('preferredBatchSize')
    return saved ? Number(saved) : 20
  })
  const [pendingReviewItems, setPendingReviewItems] = useState<(StarredItem | StudyListItem)[]>([])
  const [pendingListName, setPendingListName] = useState<string>('')
  const [showUploader, setShowUploader] = useState(false)



  const fetchData = useCallback(async () => {
    if (!user) return

    setLoading(true)
    try {
      const [lists, starred] = await Promise.all([
        studyListService.getUserStudyLists(user.id),
        studyListService.getStarredItems(user.id)
      ])
      
      setStudyLists(lists)
      setStarredItems(starred)
      
      // If there's a listSlug in the URL, select that list
      if (listSlug && lists.length > 0) {
        const targetList = lists.find(list => nameToSlug(list.name) === listSlug)
        if (targetList) {
          setSelectedList(targetList)
        }
      }
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }, [user, listSlug])

  const initializeStudyLists = useCallback(async () => {
    // Check if tables exist
    const exists = await checkStudyListTables()
    setTablesExist(exists)
    
    if (!exists) {
      console.log('Study list tables do not exist. Manual database setup required.')
      await createStudyListTables() // This will show instructions
      setLoading(false)
      return
    }
    
    await fetchData()
  }, [fetchData])

  useEffect(() => {
    if (user) {
      initializeStudyLists()
    }
  }, [user, initializeStudyLists])




  const handleDeleteList = async (listId: string) => {
    if (!window.confirm('Are you sure you want to delete this study list?')) return

    const success = await studyListService.deleteStudyList(listId)
    if (success) {
      setStudyLists(studyLists.filter(list => list.id !== listId))
      if (selectedList?.id === listId) {
        setSelectedList(null)
      }
    }
  }

  const handleEditList = (list: StudyList) => {
    // Handled in drag-drop component
  }



  const handlePlayAllItems = (items: (StarredItem | StudyListItem)[], listName?: string) => {
    if (items.length === 0) return
    
    // If there are more items than the default batch size, show settings modal
    if (items.length > 10) {
      setPendingReviewItems(items)
      setPendingListName(listName || 'Study Session')
      setShowBatchSettings(true)
    } else {
      // Navigate directly for small lists
      navigate('/study-list-review', {
        state: {
          items: items.map(item => ({
            id: item.item_id,
            type: item.item_type,
            data: item.item_data
          })),
          listName: listName || 'Study Session'
        }
      })
    }
  }

  const updateBatchSize = (size: number) => {
    setBatchSize(size)
    // Save preference to localStorage
    localStorage.setItem('preferredBatchSize', size.toString())
  }

  const startReviewWithBatchSize = () => {
    if (pendingReviewItems.length === 0) return
    
    // Save the batch size preference
    localStorage.setItem('preferredBatchSize', batchSize.toString())
    
    // Get the selected batch of items
    const reviewBatch = pendingReviewItems.slice(0, batchSize)
    
    navigate('/study-list-review', {
      state: {
        items: reviewBatch.map(item => ({
          id: item.item_id,
          type: item.item_type,
          data: item.item_data
        })),
        listName: pendingListName,
        totalItems: pendingReviewItems.length,
        batchSize: batchSize
      }
    })
    
    // Reset modal state
    setShowBatchSettings(false)
    setPendingReviewItems([])
    setPendingListName('')
  }



  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  // Show setup instructions if tables don't exist
  if (tablesExist === false) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl p-6">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                Database Setup Required
              </h3>
              <div className="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
                <p className="mb-3">
                  The study list feature requires additional database tables. Please create these tables in your Supabase SQL Editor:
                </p>
                <div className="bg-neutral-900 text-green-400 p-4 rounded-lg font-mono text-xs overflow-x-auto">
                  <pre>
{`-- Create study_lists table
CREATE TABLE IF NOT EXISTS study_lists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR(200) NOT NULL,
  description TEXT,
  color VARCHAR(7) DEFAULT '#3B82F6',
  is_public BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create starred_items table
CREATE TABLE IF NOT EXISTS starred_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  item_type VARCHAR(50) NOT NULL,
  item_id VARCHAR(200) NOT NULL,
  item_data JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, item_type, item_id)
);

-- Create study_list_items table
CREATE TABLE IF NOT EXISTS study_list_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  study_list_id UUID NOT NULL REFERENCES study_lists(id) ON DELETE CASCADE,
  item_type VARCHAR(50) NOT NULL,
  item_id VARCHAR(200) NOT NULL,
  item_data JSONB,
  notes TEXT,
  added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(study_list_id, item_type, item_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_study_lists_user_id ON study_lists(user_id);
CREATE INDEX IF NOT EXISTS idx_starred_items_user_id ON starred_items(user_id);
CREATE INDEX IF NOT EXISTS idx_study_list_items_study_list_id ON study_list_items(study_list_id);`}
                  </pre>
                </div>
                <p className="mt-3">
                  After running these commands in your Supabase dashboard, refresh this page to use the study list features.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-neutral-900 dark:text-white mb-2">
              Study Lists
            </h1>
            <p className="text-neutral-600 dark:text-neutral-400">
              Organize your learning materials and track your progress
            </p>
          </div>
          <button
            onClick={() => setShowUploader(true)}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <CloudArrowUpIcon className="h-5 w-5" />
            Upload Questions
          </button>
        </div>
      </div>

      <StudyListsDragDrop
        studyLists={studyLists}
        starredItems={starredItems}
        onListUpdate={fetchData}
        onPlayItems={handlePlayAllItems}
        onEditList={handleEditList}
        onDeleteList={handleDeleteList}
        onShowCreateForm={() => {}}
        userId={user?.id || ''}
      />

      {/* Batch Size Settings Modal */}
      {showBatchSettings && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-xl p-6 max-w-md w-full">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-neutral-900 dark:text-white">
                Study Session Settings
              </h3>
              <button
                onClick={() => {
                  setShowBatchSettings(false)
                  setPendingReviewItems([])
                  setPendingListName('')
                }}
                className="p-1 text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-200"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="mb-6">
              <p className="text-neutral-600 dark:text-neutral-400 mb-4">
                You have {pendingReviewItems.length} items in this list. How many would you like to study in this session?
              </p>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                    Number of flashcards
                  </label>
                  <div className="flex items-center gap-4">
                    <input
                      type="range"
                      min="5"
                      max={Math.min(pendingReviewItems.length, 100)}
                      step="5"
                      value={batchSize}
                      onChange={(e) => updateBatchSize(Number(e.target.value))}
                      className="flex-1"
                    />
                    <input
                      type="number"
                      min="5"
                      max={Math.min(pendingReviewItems.length, 100)}
                      value={batchSize}
                      onChange={(e) => updateBatchSize(Math.min(Math.max(5, Number(e.target.value)), pendingReviewItems.length))}
                      className="w-20 px-2 py-1 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white text-center"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2">
                  <button
                    onClick={() => updateBatchSize(10)}
                    className={`px-3 py-2 rounded-lg border ${
                      batchSize === 10
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400'
                    }`}
                  >
                    10
                  </button>
                  <button
                    onClick={() => updateBatchSize(20)}
                    className={`px-3 py-2 rounded-lg border ${
                      batchSize === 20
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400'
                    }`}
                  >
                    20
                  </button>
                  <button
                    onClick={() => updateBatchSize(30)}
                    className={`px-3 py-2 rounded-lg border ${
                      batchSize === 30
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400'
                    }`}
                  >
                    30
                  </button>
                  <button
                    onClick={() => updateBatchSize(50)}
                    className={`px-3 py-2 rounded-lg border ${
                      batchSize === 50
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400'
                    }`}
                  >
                    50
                  </button>
                  <button
                    onClick={() => updateBatchSize(Math.min(pendingReviewItems.length, 100))}
                    className={`px-3 py-2 rounded-lg border ${
                      batchSize === Math.min(pendingReviewItems.length, 100)
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                        : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400'
                    }`}
                  >
                    All
                  </button>
                  <button
                    onClick={() => {
                      const customSize = prompt(`Enter custom batch size (5-${pendingReviewItems.length}):`)
                      if (customSize) {
                        const size = Number(customSize)
                        if (!isNaN(size)) {
                          updateBatchSize(Math.min(Math.max(5, size), pendingReviewItems.length))
                        }
                      }
                    }}
                    className="px-3 py-2 rounded-lg border border-neutral-300 dark:border-neutral-600 hover:border-primary-400"
                  >
                    Custom
                  </button>
                </div>

                <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-3 text-sm text-neutral-600 dark:text-neutral-400">
                  <p>
                    <span className="font-medium">Estimated time:</span> {Math.round(batchSize * 0.5)}-{Math.round(batchSize * 1.5)} minutes
                  </p>
                  <p className="text-xs mt-1">
                    Based on ~30-90 seconds per flashcard
                  </p>
                </div>

                <div className="text-xs text-neutral-500 dark:text-neutral-400 text-center">
                  Your preference will be saved for future sessions
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={() => {
                  setShowBatchSettings(false)
                  setPendingReviewItems([])
                  setPendingListName('')
                }}
                className="flex-1 px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={startReviewWithBatchSize}
                className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
              >
                <PlayIcon className="h-5 w-5" />
                Start Session
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Custom Question Uploader Modal */}
      {showUploader && (
        <CustomQuestionUploader
          studyListId={selectedList?.id}
          onClose={() => setShowUploader(false)}
          onSuccess={() => {
            setShowUploader(false)
            // Refresh data to show new questions
            fetchData()
          }}
        />
      )}
    </div>
  )
}

export default StudyListsPage