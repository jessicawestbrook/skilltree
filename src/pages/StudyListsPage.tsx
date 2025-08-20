import React, { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { studyListService } from '../services/studyListService'
import { checkStudyListTables, createStudyListTables } from '../utils/createStudyListTables'
import { StudyList, StarredItem, StudyListItem } from '../types/database.types'
import {
  PlusIcon,
  TrashIcon,
  PencilIcon,
  PlayIcon
} from '@heroicons/react/24/outline'
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid'

const StudyListsPage: React.FC = () => {
  const { user } = useAuth()
  const [studyLists, setStudyLists] = useState<StudyList[]>([])
  const [starredItems, setStarredItems] = useState<StarredItem[]>([])
  const [loading, setLoading] = useState(true)
  const [tablesExist, setTablesExist] = useState<boolean | null>(null)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [editingList, setEditingList] = useState<StudyList | null>(null)
  const [selectedList, setSelectedList] = useState<StudyList | null>(null)
  const [listItems, setListItems] = useState<StudyListItem[]>([])
  const [newListData, setNewListData] = useState({
    name: '',
    description: '',
    color: '#3B82F6'
  })

  const colors = [
    '#3B82F6', // Blue
    '#10B981', // Green
    '#F59E0B', // Amber
    '#EF4444', // Red
    '#8B5CF6', // Purple
    '#F97316', // Orange
    '#06B6D4', // Cyan
    '#84CC16'  // Lime
  ]

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
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }, [user])

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

  const fetchListItems = async (listId: string) => {
    const items = await studyListService.getStudyListItems(listId)
    setListItems(items)
  }

  const handleCreateList = async () => {
    if (!user || !newListData.name.trim()) return

    const newList = await studyListService.createStudyList(
      user.id,
      newListData.name.trim(),
      newListData.description.trim() || undefined,
      newListData.color
    )

    if (newList) {
      setStudyLists([newList, ...studyLists])
      setNewListData({ name: '', description: '', color: '#3B82F6' })
      setShowCreateForm(false)
    }
  }

  const handleUpdateList = async () => {
    if (!editingList || !newListData.name.trim()) return

    const success = await studyListService.updateStudyList(editingList.id, {
      name: newListData.name.trim(),
      description: newListData.description.trim() || undefined,
      color: newListData.color
    })

    if (success) {
      setStudyLists(studyLists.map(list => 
        list.id === editingList.id 
          ? { ...list, ...newListData, name: newListData.name.trim() }
          : list
      ))
      setEditingList(null)
      setNewListData({ name: '', description: '', color: '#3B82F6' })
    }
  }

  const handleDeleteList = async (listId: string) => {
    if (!window.confirm('Are you sure you want to delete this study list?')) return

    const success = await studyListService.deleteStudyList(listId)
    if (success) {
      setStudyLists(studyLists.filter(list => list.id !== listId))
      if (selectedList?.id === listId) {
        setSelectedList(null)
        setListItems([])
      }
    }
  }

  const handleEditList = (list: StudyList) => {
    setEditingList(list)
    setNewListData({
      name: list.name,
      description: list.description || '',
      color: list.color || '#3B82F6'
    })
    setShowCreateForm(true)
  }

  const handleViewList = (list: StudyList) => {
    setSelectedList(list)
    fetchListItems(list.id)
  }

  const handleRemoveFromList = async (item: StudyListItem) => {
    if (!selectedList) return

    const success = await studyListService.removeItemFromStudyList(
      selectedList.id,
      item.item_type,
      item.item_id
    )

    if (success) {
      setListItems(listItems.filter(i => i.id !== item.id))
    }
  }

  const renderItemPreview = (item: StarredItem | StudyListItem) => {
    const data = item.item_data || {}
    
    switch (item.item_type) {
      case 'spelling_word':
      case 'vocabulary_word':
        return (
          <div className="flex-1">
            <span className="font-medium">{data.word || 'Unknown word'}</span>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 line-clamp-2">
              {data.definition || 'No definition available'}
            </p>
          </div>
        )
      case 'language_question':
        return (
          <div className="flex-1">
            <span className="font-medium">Language Question</span>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 line-clamp-2">
              {data.question_text || 'No question text available'}
            </p>
          </div>
        )
      case 'question':
        return (
          <div className="flex-1">
            <span className="font-medium">General Question</span>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 line-clamp-2">
              {data.question_text || 'No question text available'}
            </p>
          </div>
        )
      case 'skill_node':
        return (
          <div className="flex-1">
            <span className="font-medium">{data.name || 'Skill Node'}</span>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 line-clamp-2">
              {data.learning_area || 'No description available'}
            </p>
          </div>
        )
      default:
        return (
          <div className="flex-1">
            <span className="font-medium">Unknown Item</span>
          </div>
        )
    }
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
        <h1 className="text-3xl font-bold text-neutral-900 dark:text-white mb-2">
          Study Lists & Starred Items
        </h1>
        <p className="text-neutral-600 dark:text-neutral-400">
          Organize your learning materials and track your progress
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Panel - Study Lists */}
        <div className="lg:col-span-1">
          {/* Create List Button */}
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 mb-4">
            {!showCreateForm ? (
              <button
                onClick={() => setShowCreateForm(true)}
                className="w-full flex items-center justify-center gap-2 p-3 border-2 border-dashed border-neutral-300 dark:border-neutral-600 rounded-lg hover:border-primary-400 dark:hover:border-primary-500 transition-colors"
              >
                <PlusIcon className="h-5 w-5 text-neutral-400" />
                <span className="font-medium text-neutral-600 dark:text-neutral-400">
                  Create Study List
                </span>
              </button>
            ) : (
              <div className="space-y-3">
                <h3 className="font-semibold text-neutral-900 dark:text-white">
                  {editingList ? 'Edit Study List' : 'Create New Study List'}
                </h3>
                <input
                  type="text"
                  placeholder="List name"
                  value={newListData.name}
                  onChange={(e) => setNewListData({ ...newListData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
                />
                <textarea
                  placeholder="Description (optional)"
                  value={newListData.description}
                  onChange={(e) => setNewListData({ ...newListData, description: e.target.value })}
                  rows={2}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white resize-none"
                />
                
                {/* Color Picker */}
                <div>
                  <label className="text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-2 block">
                    Color
                  </label>
                  <div className="flex gap-2 flex-wrap">
                    {colors.map(color => (
                      <button
                        key={color}
                        onClick={() => setNewListData({ ...newListData, color })}
                        className={`w-6 h-6 rounded-full border-2 transition-all ${
                          newListData.color === color
                            ? 'border-neutral-400 scale-110'
                            : 'border-neutral-200 dark:border-neutral-600'
                        }`}
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={editingList ? handleUpdateList : handleCreateList}
                    disabled={!newListData.name.trim()}
                    className="flex-1 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors text-sm font-medium"
                  >
                    {editingList ? 'Update' : 'Create'}
                  </button>
                  <button
                    onClick={() => {
                      setShowCreateForm(false)
                      setEditingList(null)
                      setNewListData({ name: '', description: '', color: '#3B82F6' })
                    }}
                    className="px-4 py-2 bg-neutral-200 dark:bg-neutral-600 text-neutral-700 dark:text-neutral-300 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-500 transition-colors text-sm"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Study Lists */}
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4">
            <h2 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">
              Your Study Lists ({studyLists.length})
            </h2>
            <div className="space-y-2">
              {studyLists.map(list => (
                <div
                  key={list.id}
                  className={`p-3 rounded-lg border transition-colors cursor-pointer ${
                    selectedList?.id === list.id
                      ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                      : 'border-neutral-200 dark:border-neutral-700 hover:border-neutral-300'
                  }`}
                  onClick={() => handleViewList(list)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3 flex-1">
                      <div
                        className="w-4 h-4 rounded-full"
                        style={{ backgroundColor: list.color }}
                      />
                      <div className="flex-1 min-w-0">
                        <span className="font-medium text-neutral-900 dark:text-white block truncate">
                          {list.name}
                        </span>
                        {list.description && (
                          <p className="text-xs text-neutral-500 dark:text-neutral-400 truncate">
                            {list.description}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-1">
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleEditList(list)
                        }}
                        className="p-1 hover:bg-neutral-200 dark:hover:bg-neutral-600 rounded transition-colors"
                      >
                        <PencilIcon className="h-4 w-4 text-neutral-500" />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleDeleteList(list.id)
                        }}
                        className="p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded transition-colors"
                      >
                        <TrashIcon className="h-4 w-4 text-red-500" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
              {studyLists.length === 0 && (
                <p className="text-neutral-500 dark:text-neutral-400 text-center py-4 text-sm">
                  No study lists yet. Create your first one!
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Right Panel - Content */}
        <div className="lg:col-span-2">
          {selectedList ? (
            /* Study List Items */
            <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div
                    className="w-6 h-6 rounded-full"
                    style={{ backgroundColor: selectedList.color }}
                  />
                  <div>
                    <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">
                      {selectedList.name}
                    </h2>
                    {selectedList.description && (
                      <p className="text-sm text-neutral-600 dark:text-neutral-400">
                        {selectedList.description}
                      </p>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-neutral-500 dark:text-neutral-400">
                    {listItems.length} items
                  </span>
                  <button className="p-2 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors">
                    <PlayIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>

              <div className="space-y-3">
                {listItems.map(item => (
                  <div
                    key={item.id}
                    className="flex items-center gap-3 p-4 border border-neutral-200 dark:border-neutral-700 rounded-lg"
                  >
                    <div className="w-2 h-2 bg-neutral-400 rounded-full flex-shrink-0" />
                    {renderItemPreview(item)}
                    <div className="flex items-center gap-2">
                      <span className="text-xs bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-400 px-2 py-1 rounded">
                        {item.item_type.replace('_', ' ')}
                      </span>
                      <button
                        onClick={() => handleRemoveFromList(item)}
                        className="p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded transition-colors"
                      >
                        <TrashIcon className="h-4 w-4 text-red-500" />
                      </button>
                    </div>
                  </div>
                ))}
                {listItems.length === 0 && (
                  <p className="text-neutral-500 dark:text-neutral-400 text-center py-8">
                    This study list is empty. Add items using the star/bookmark buttons when practicing.
                  </p>
                )}
              </div>
            </div>
          ) : (
            /* Starred Items */
            <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-3 mb-6">
                <StarIconSolid className="h-6 w-6 text-yellow-500" />
                <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">
                  Starred Items ({starredItems.length})
                </h2>
              </div>

              <div className="space-y-3">
                {starredItems.map(item => (
                  <div
                    key={item.id}
                    className="flex items-center gap-3 p-4 border border-neutral-200 dark:border-neutral-700 rounded-lg"
                  >
                    <StarIconSolid className="h-4 w-4 text-yellow-500 flex-shrink-0" />
                    {renderItemPreview(item)}
                    <span className="text-xs bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-400 px-2 py-1 rounded">
                      {item.item_type.replace('_', ' ')}
                    </span>
                  </div>
                ))}
                {starredItems.length === 0 && (
                  <p className="text-neutral-500 dark:text-neutral-400 text-center py-8">
                    No starred items yet. Star questions and flashcards to save them here.
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default StudyListsPage