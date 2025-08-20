import React, { useState, useEffect, useCallback } from 'react'
import {
  XMarkIcon,
  PlusIcon,
  CheckIcon,
  BookOpenIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'
import { studyListService } from '../services/studyListService'
import { StudyList, StarredItem, StudyListItem } from '../types/database.types'

interface StudyListSelectionModalProps {
  isOpen: boolean
  onClose: () => void
  itemType: StarredItem['item_type']
  itemId: string
  itemData?: any
  itemTitle?: string
  userStudyLists: StudyList[]
  onStudyListsUpdate: () => void
}

const StudyListSelectionModal: React.FC<StudyListSelectionModalProps> = ({
  isOpen,
  onClose,
  itemType,
  itemId,
  itemData,
  itemTitle,
  userStudyLists,
  onStudyListsUpdate
}) => {
  const { user } = useAuth()
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newListName, setNewListName] = useState('')
  const [newListDescription, setNewListDescription] = useState('')
  const [newListColor, setNewListColor] = useState('#3B82F6')
  const [itemInLists, setItemInLists] = useState<Set<string>>(new Set())
  const [loading, setLoading] = useState(false)

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

  const checkItemInLists = useCallback(async () => {
    if (!user) return
    
    const listsWithItem = new Set<string>()
    
    for (const list of userStudyLists) {
      const inList = await studyListService.isItemInStudyList(
        list.id,
        itemType as StudyListItem['item_type'],
        itemId
      )
      if (inList) {
        listsWithItem.add(list.id)
      }
    }
    
    setItemInLists(listsWithItem)
  }, [user, userStudyLists, itemType, itemId])

  useEffect(() => {
    if (isOpen) {
      checkItemInLists()
    }
  }, [isOpen, checkItemInLists])

  const handleCreateList = async () => {
    if (!user || !newListName.trim()) return

    setLoading(true)
    try {
      const newList = await studyListService.createStudyList(
        user.id,
        newListName.trim(),
        newListDescription.trim() || undefined,
        newListColor
      )

      if (newList) {
        // Add item to the new list
        await studyListService.addItemToStudyList(
          newList.id,
          itemType as StudyListItem['item_type'],
          itemId,
          itemData
        )

        // Reset form
        setNewListName('')
        setNewListDescription('')
        setNewListColor('#3B82F6')
        setShowCreateForm(false)
        
        // Update parent component
        onStudyListsUpdate()
        
        // Show success message or close modal
        onClose()
      }
    } catch (error) {
      console.error('Error creating study list:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleToggleItemInList = async (listId: string) => {
    if (!user) return

    setLoading(true)
    try {
      const isInList = itemInLists.has(listId)
      
      if (isInList) {
        const success = await studyListService.removeItemFromStudyList(
          listId,
          itemType as StudyListItem['item_type'],
          itemId
        )
        if (success) {
          setItemInLists(prev => {
            const newSet = new Set(prev)
            newSet.delete(listId)
            return newSet
          })
        }
      } else {
        const success = await studyListService.addItemToStudyList(
          listId,
          itemType as StudyListItem['item_type'],
          itemId,
          itemData
        )
        if (success) {
          setItemInLists(prev => new Set(prev).add(listId))
        }
      }
    } catch (error) {
      console.error('Error toggling item in list:', error)
    } finally {
      setLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-xl max-w-md w-full max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-neutral-200 dark:border-neutral-700">
          <h2 className="text-lg font-semibold text-neutral-900 dark:text-white">
            Add to Study List
          </h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg transition-colors"
          >
            <XMarkIcon className="h-5 w-5 text-neutral-500" />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 overflow-y-auto max-h-[60vh]">
          {/* Item Info */}
          {itemTitle && (
            <div className="mb-4 p-3 bg-neutral-50 dark:bg-neutral-900 rounded-lg">
              <div className="flex items-center gap-2">
                <BookOpenIcon className="h-4 w-4 text-neutral-500" />
                <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300">
                  {itemTitle}
                </span>
              </div>
            </div>
          )}

          {/* Existing Study Lists */}
          <div className="space-y-2 mb-4">
            {userStudyLists.length > 0 ? (
              userStudyLists.map(list => (
                <div
                  key={list.id}
                  className="flex items-center justify-between p-3 border border-neutral-200 dark:border-neutral-700 rounded-lg hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: list.color }}
                    />
                    <div>
                      <span className="font-medium text-neutral-900 dark:text-white">
                        {list.name}
                      </span>
                      {list.description && (
                        <p className="text-xs text-neutral-500 dark:text-neutral-400">
                          {list.description}
                        </p>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => handleToggleItemInList(list.id)}
                    disabled={loading}
                    className={`p-1.5 rounded-lg transition-colors ${
                      itemInLists.has(list.id)
                        ? 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400'
                        : 'bg-neutral-100 text-neutral-400 hover:bg-neutral-200 dark:bg-neutral-600 dark:hover:bg-neutral-500'
                    }`}
                  >
                    <CheckIcon className="h-4 w-4" />
                  </button>
                </div>
              ))
            ) : (
              <p className="text-sm text-neutral-500 dark:text-neutral-400 text-center py-4">
                No study lists yet. Create your first one below!
              </p>
            )}
          </div>

          {/* Create New List */}
          {!showCreateForm ? (
            <button
              onClick={() => setShowCreateForm(true)}
              className="w-full flex items-center justify-center gap-2 p-3 border-2 border-dashed border-neutral-300 dark:border-neutral-600 rounded-lg hover:border-primary-400 dark:hover:border-primary-500 transition-colors"
            >
              <PlusIcon className="h-4 w-4 text-neutral-400" />
              <span className="text-sm font-medium text-neutral-600 dark:text-neutral-400">
                Create New Study List
              </span>
            </button>
          ) : (
            <div className="space-y-3 p-3 border border-neutral-200 dark:border-neutral-700 rounded-lg">
              <input
                type="text"
                placeholder="List name"
                value={newListName}
                onChange={(e) => setNewListName(e.target.value)}
                className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white"
              />
              <textarea
                placeholder="Description (optional)"
                value={newListDescription}
                onChange={(e) => setNewListDescription(e.target.value)}
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
                      onClick={() => setNewListColor(color)}
                      className={`w-6 h-6 rounded-full border-2 transition-all ${
                        newListColor === color
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
                  onClick={handleCreateList}
                  disabled={!newListName.trim() || loading}
                  className="flex-1 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors text-sm font-medium"
                >
                  Create & Add
                </button>
                <button
                  onClick={() => setShowCreateForm(false)}
                  className="px-4 py-2 bg-neutral-200 dark:bg-neutral-600 text-neutral-700 dark:text-neutral-300 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-500 transition-colors text-sm"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default StudyListSelectionModal