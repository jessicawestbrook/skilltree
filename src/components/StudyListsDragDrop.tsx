import React, { useState, useCallback, DragEvent } from 'react'
import { StudyList, StarredItem, StudyListItem } from '../types/database.types'
import { studyListService } from '../services/studyListService'
import {
  PlusIcon,
  TrashIcon,
  PlayIcon,
  PencilIcon
} from '@heroicons/react/24/outline'
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid'

interface Props {
  studyLists: StudyList[]
  starredItems: StarredItem[]
  onListUpdate: () => void
  onPlayItems: (items: (StarredItem | StudyListItem)[], listName?: string) => void
  onEditList?: (list: StudyList) => void
  onDeleteList?: (listId: string) => void
  onShowCreateForm?: () => void
  userId: string
}

type ItemType = 'spelling_word' | 'vocabulary_word' | 'language_question' | 'question' | 'skill_node' | 'custom_question' | 'custom_flashcard'

interface DraggableCard {
  id: string
  type: ItemType
  data: any
  sourceList?: string
}

const StudyListsDragDrop: React.FC<Props> = ({
  studyLists,
  starredItems,
  onListUpdate,
  onPlayItems,
  onEditList,
  onDeleteList,
  onShowCreateForm,
  userId
}) => {
  const [draggedCard, setDraggedCard] = useState<DraggableCard | null>(null)
  const [dragOverList, setDragOverList] = useState<string | null>(null)
  const [listItems, setListItems] = useState<Record<string, StudyListItem[]>>({})
  const [loadingLists, setLoadingLists] = useState<Set<string>>(new Set())
  const [expandedLists, setExpandedLists] = useState<Set<string>>(new Set())

  // Load items for a specific list
  const loadListItems = useCallback(async (listId: string) => {
    if (listItems[listId] || loadingLists.has(listId)) return

    setLoadingLists(prev => new Set(Array.from(prev).concat(listId)))
    try {
      const items = await studyListService.getStudyListItems(listId)
      setListItems(prev => ({ ...prev, [listId]: items }))
      // Auto-expand when loaded
      setExpandedLists(prev => new Set(Array.from(prev).concat(listId)))
    } catch (error) {
      console.error('Error loading list items:', error)
    } finally {
      setLoadingLists(prev => {
        const next = new Set(prev)
        next.delete(listId)
        return next
      })
    }
  }, [listItems, loadingLists])

  // Toggle list expansion
  const toggleList = (listId: string) => {
    if (expandedLists.has(listId)) {
      setExpandedLists(prev => {
        const next = new Set(prev)
        next.delete(listId)
        return next
      })
    } else {
      loadListItems(listId)
    }
  }

  // Drag handlers for cards
  const handleDragStart = (e: DragEvent<HTMLDivElement>, card: DraggableCard) => {
    setDraggedCard(card)
    e.dataTransfer.effectAllowed = 'move'
    // Add dragging class to the element
    const element = e.currentTarget as HTMLDivElement
    element.classList.add('opacity-50')
  }

  const handleDragEnd = (e: DragEvent<HTMLDivElement>) => {
    // Remove dragging class
    const element = e.currentTarget as HTMLDivElement
    element.classList.remove('opacity-50')
    setDraggedCard(null)
    setDragOverList(null)
  }

  // Drag handlers for lists
  const handleListDragOver = (e: DragEvent<HTMLDivElement>, listId: string) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
    setDragOverList(listId)
  }

  const handleListDragLeave = () => {
    setDragOverList(null)
  }

  const handleListDrop = async (e: DragEvent<HTMLDivElement>, targetListId: string) => {
    e.preventDefault()
    setDragOverList(null)

    if (!draggedCard) return

    // Don't drop on the same list
    if (draggedCard.sourceList === targetListId) return

    try {
      // Add item to the target list
      const success = await studyListService.addItemToStudyList(
        targetListId,
        draggedCard.type as ItemType,
        draggedCard.id,
        draggedCard.data
      )

      if (success) {
        // If moving from another list, remove from source
        if (draggedCard.sourceList) {
          await studyListService.removeItemFromStudyList(
            draggedCard.sourceList,
            draggedCard.type as ItemType,
            draggedCard.id
          )
          // Reload source list
          const sourceItems = await studyListService.getStudyListItems(draggedCard.sourceList)
          setListItems(prev => ({ ...prev, [draggedCard.sourceList!]: sourceItems }))
        }

        // Reload target list
        const targetItems = await studyListService.getStudyListItems(targetListId)
        setListItems(prev => ({ ...prev, [targetListId]: targetItems }))
        onListUpdate()
      }
    } catch (error) {
      console.error('Error moving item:', error)
    }
  }

  // Remove item from list
  const handleRemoveItem = async (listId: string, itemType: ItemType, itemId: string) => {
    const success = await studyListService.removeItemFromStudyList(listId, itemType as ItemType, itemId)
    if (success) {
      const items = await studyListService.getStudyListItems(listId)
      setListItems(prev => ({ ...prev, [listId]: items }))
      onListUpdate()
    }
  }

  // Render card content
  const renderItemPreview = (item: StarredItem | StudyListItem) => {
    const data = item.item_data || {}
    
    switch (item.item_type) {
      case 'spelling_word':
      case 'vocabulary_word':
        return (
          <div className="flex-1">
            <span className="font-medium">{data.word || 'Unknown word'}</span>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 line-clamp-2">
              {data.definition || data.translation || 'No definition available'}
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
      case 'custom_question':
        return (
          <div className="flex-1">
            <span className="font-medium">Custom Question</span>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 line-clamp-2">
              {data.question_text || 'No question text available'}
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

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      {/* Left Panel - Study Lists */}
      <div className="lg:col-span-1">
        {/* Create List Button */}
        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-4 mb-4">
          <button
            onClick={onShowCreateForm}
            className="w-full flex items-center justify-center gap-2 p-3 border-2 border-dashed border-neutral-300 dark:border-neutral-600 rounded-lg hover:border-primary-400 dark:hover:border-primary-500 transition-colors"
          >
            <PlusIcon className="h-5 w-5 text-neutral-400" />
            <span className="font-medium text-neutral-600 dark:text-neutral-400">
              Create Study List
            </span>
          </button>
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
                  dragOverList === list.id
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                    : expandedLists.has(list.id)
                    ? 'border-neutral-300 dark:border-neutral-600 bg-neutral-50 dark:bg-neutral-700/50'
                    : 'border-neutral-200 dark:border-neutral-700 hover:border-neutral-300'
                }`}
                onClick={() => toggleList(list.id)}
                onDragOver={(e) => {
                  e.stopPropagation()
                  handleListDragOver(e, list.id)
                }}
                onDragLeave={handleListDragLeave}
                onDrop={(e) => {
                  e.stopPropagation()
                  handleListDrop(e, list.id)
                }}
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
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    {onEditList && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          onEditList(list)
                        }}
                        className="p-1 hover:bg-neutral-200 dark:hover:bg-neutral-600 rounded transition-colors"
                      >
                        <PencilIcon className="h-4 w-4 text-neutral-500 dark:text-neutral-400" />
                      </button>
                    )}
                    {onDeleteList && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          onDeleteList(list.id)
                        }}
                        className="p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded transition-colors"
                      >
                        <TrashIcon className="h-4 w-4 text-red-500" />
                      </button>
                    )}
                  </div>
                </div>

                {/* Drop zone indicator when dragging */}
                {dragOverList === list.id && (
                  <div className="mt-2 p-2 border-2 border-dashed border-primary-400 rounded-lg text-center text-xs text-primary-600 dark:text-primary-400">
                    Drop here to add to {list.name}
                  </div>
                )}
              </div>
            ))}
            {studyLists.length === 0 && (
              <p className="text-neutral-500 dark:text-neutral-400 text-center py-4">
                No study lists yet
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Right Panel - Items */}
      <div className="lg:col-span-2">
        {/* Show expanded list items or starred items */}
        {Array.from(expandedLists).map(listId => {
          const list = studyLists.find(l => l.id === listId)
          const items = listItems[listId] || []
          if (!list) return null

          return (
            <div key={listId} className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6 mb-4">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div
                    className="w-6 h-6 rounded-full"
                    style={{ backgroundColor: list.color }}
                  />
                  <div>
                    <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">
                      {list.name}
                    </h2>
                    {list.description && (
                      <p className="text-sm text-neutral-600 dark:text-neutral-400">
                        {list.description}
                      </p>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-neutral-500 dark:text-neutral-400">
                    {items.length} items
                  </span>
                  {items.length > 0 && (
                    <button 
                      onClick={() => onPlayItems(items, list.name)}
                      className="p-2 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors"
                      title="Study all items in this list"
                    >
                      <PlayIcon className="h-5 w-5" />
                    </button>
                  )}
                </div>
              </div>

              <div className="space-y-3">
                {loadingLists.has(listId) ? (
                  <div className="text-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                  </div>
                ) : items.length > 0 ? (
                  items.map((item) => (
                    <div
                      key={item.id}
                      draggable
                      onDragStart={(e) => handleDragStart(e, {
                        id: item.item_id,
                        type: item.item_type as ItemType,
                        data: item.item_data,
                        sourceList: listId
                      })}
                      onDragEnd={handleDragEnd}
                      className="flex items-center gap-3 p-4 border border-neutral-200 dark:border-neutral-700 rounded-lg hover:border-primary-400 dark:hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/10 transition-all cursor-move group"
                    >
                      <div className="w-2 h-2 bg-neutral-400 group-hover:bg-primary-500 rounded-full flex-shrink-0 transition-colors" />
                      {renderItemPreview(item)}
                      <div className="flex items-center gap-2">
                        <span className="text-xs bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-400 px-2 py-1 rounded">
                          {item.item_type.replace('_', ' ')}
                        </span>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            handleRemoveItem(listId, item.item_type as ItemType, item.item_id)
                          }}
                          className="p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded transition-colors"
                        >
                          <TrashIcon className="h-4 w-4 text-red-500" />
                        </button>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-neutral-500 dark:text-neutral-400 text-center py-8">
                    This study list is empty. Drag items here to add them.
                  </p>
                )}
              </div>
            </div>
          )
        })}

        {/* Starred Items - Always visible */}
        {expandedLists.size === 0 && (
          <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <StarIconSolid className="h-6 w-6 text-yellow-500" />
                <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">
                  Starred Items ({starredItems.length})
                </h2>
              </div>
              {starredItems.length > 0 && (
                <button 
                  onClick={() => onPlayItems(starredItems, 'Starred Items')}
                  className="p-2 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors"
                  title="Study all starred items"
                >
                  <PlayIcon className="h-5 w-5" />
                </button>
              )}
            </div>

            <div className="space-y-3">
              {starredItems.map((item) => (
                <div
                  key={`${item.item_type}-${item.item_id}`}
                  draggable
                  onDragStart={(e) => handleDragStart(e, {
                    id: item.item_id,
                    type: item.item_type as ItemType,
                    data: item.item_data
                  })}
                  onDragEnd={handleDragEnd}
                  className="flex items-center gap-3 p-4 border border-neutral-200 dark:border-neutral-700 rounded-lg hover:border-primary-400 dark:hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/10 transition-all cursor-move group"
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
  )
}

export default StudyListsDragDrop