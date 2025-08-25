import React, { useState, useEffect, useCallback } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { 
  StarIcon, 
  FolderPlusIcon 
} from '@heroicons/react/24/outline'
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid'
import { useAuth } from '../contexts/AuthContext'
import { studyListService } from '../services/studyListService'
import { StudyList, StarredItem } from '../types/database.types'
import StudyListSelectionModal from './StudyListSelectionModal'

interface StudyListActionsProps {
  itemType: StarredItem['item_type']
  itemId: string
  itemData?: any
  itemTitle?: string
  className?: string
  showLabels?: boolean
}

const StudyListActions: React.FC<StudyListActionsProps> = ({
  itemType,
  itemId,
  itemData,
  itemTitle,
  className = '',
  showLabels = false
}) => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [isStarred, setIsStarred] = useState(false)
  const [showStudyListModal, setShowStudyListModal] = useState(false)
  const [userStudyLists, setUserStudyLists] = useState<StudyList[]>([])
  const [loading, setLoading] = useState(false)

  const checkIfStarred = useCallback(async () => {
    if (!user) return
    const starred = await studyListService.isItemStarred(user.id, itemType, itemId)
    setIsStarred(starred)
  }, [user, itemType, itemId])

  const fetchUserStudyLists = useCallback(async () => {
    if (!user) return
    const lists = await studyListService.getUserStudyLists(user.id)
    setUserStudyLists(lists)
  }, [user])

  useEffect(() => {
    if (user) {
      checkIfStarred()
      fetchUserStudyLists()
    }
  }, [user, checkIfStarred, fetchUserStudyLists])

  const handleStarToggle = async () => {
    if (!user) {
      // Navigate to login page with redirect
      const redirectTo = location.pathname + location.search
      navigate(`/login?redirect=${encodeURIComponent(redirectTo)}`)
      return
    }
    
    setLoading(true)
    try {
      if (isStarred) {
        const success = await studyListService.unstarItem(user.id, itemType, itemId)
        if (success) {
          setIsStarred(false)
        }
      } else {
        const success = await studyListService.starItem(user.id, itemType, itemId, itemData)
        if (success) {
          setIsStarred(true)
        }
      }
    } catch (error) {
      console.error('Error toggling star:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddToStudyList = () => {
    if (!user) {
      // Navigate to login page with redirect
      const redirectTo = location.pathname + location.search
      navigate(`/login?redirect=${encodeURIComponent(redirectTo)}`)
      return
    }
    setShowStudyListModal(true)
  }

  return (
    <>
      <div className={`flex items-center gap-2 ${className}`}>
        {/* Star Button */}
        <button
          onClick={handleStarToggle}
          disabled={loading}
          className="flex items-center gap-1 p-1.5 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors disabled:opacity-50"
          title={user ? (isStarred ? 'Remove from starred' : 'Add to starred') : 'Log in to star items'}
        >
          {user && isStarred ? (
            <StarIconSolid className="h-4 w-4 text-yellow-500" />
          ) : (
            <StarIcon className="h-4 w-4 text-neutral-400 hover:text-yellow-500" />
          )}
          {showLabels && (
            <span className="text-xs font-medium">
              {user && isStarred ? 'Starred' : 'Star'}
            </span>
          )}
        </button>

        {/* Add to Study List Button */}
        <button
          onClick={handleAddToStudyList}
          className="flex items-center gap-1 p-1.5 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
          title={user ? 'Add to study list' : 'Log in to create study lists'}
        >
          <FolderPlusIcon className="h-4 w-4 text-neutral-400 hover:text-primary-500" />
          {showLabels && (
            <span className="text-xs font-medium">Add to List</span>
          )}
        </button>
      </div>

      {/* Study List Selection Modal */}
      {showStudyListModal && (
        <StudyListSelectionModal
          isOpen={showStudyListModal}
          onClose={() => setShowStudyListModal(false)}
          itemType={itemType}
          itemId={itemId}
          itemData={itemData}
          itemTitle={itemTitle}
          userStudyLists={userStudyLists}
          onStudyListsUpdate={fetchUserStudyLists}
        />
      )}
    </>
  )
}

export default StudyListActions