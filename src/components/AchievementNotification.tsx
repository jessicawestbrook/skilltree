import React, { useEffect, useState } from 'react'
import { XMarkIcon } from '@heroicons/react/24/outline'

interface AchievementNotificationProps {
  achievement: {
    name: string
    description: string
    icon: string
    badge_color: string
    rarity: string
    points: number
  } | null
  onClose: () => void
}

export const AchievementNotification: React.FC<AchievementNotificationProps> = ({
  achievement,
  onClose
}) => {
  const [isVisible, setIsVisible] = useState(false)
  const [isLeaving, setIsLeaving] = useState(false)

  useEffect(() => {
    if (achievement) {
      setIsVisible(true)
      setIsLeaving(false)
      
      // Auto-close after 5 seconds
      const timer = setTimeout(() => {
        setIsLeaving(true)
        setTimeout(() => {
          setIsVisible(false)
          onClose()
        }, 300)
      }, 5000)
      
      return () => clearTimeout(timer)
    }
  }, [achievement, onClose])

  const handleClose = () => {
    setIsLeaving(true)
    setTimeout(() => {
      setIsVisible(false)
      onClose()
    }, 300)
  }

  if (!achievement || !isVisible) return null

  const getRarityColors = (rarity: string) => {
    switch (rarity) {
      case 'common':
        return 'from-gray-400 to-gray-600 border-gray-500'
      case 'uncommon':
        return 'from-green-400 to-green-600 border-green-500'
      case 'rare':
        return 'from-blue-400 to-blue-600 border-blue-500'
      case 'epic':
        return 'from-purple-400 to-purple-600 border-purple-500'
      case 'legendary':
        return 'from-yellow-400 to-yellow-600 border-yellow-500 animate-pulse'
      default:
        return 'from-gray-400 to-gray-600 border-gray-500'
    }
  }

  const rarityColors = getRarityColors(achievement.rarity)

  return (
    <div className={`fixed top-20 right-4 z-50 transition-all duration-300 ${
      isLeaving ? 'opacity-0 translate-x-full' : 'opacity-100 translate-x-0'
    }`}>
      <div className={`bg-gradient-to-br ${rarityColors} rounded-lg shadow-2xl p-1`}>
        <div className="bg-white dark:bg-gray-900 rounded-lg p-4 max-w-sm">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${rarityColors} 
                             flex items-center justify-center text-2xl shadow-lg
                             ${achievement.rarity === 'legendary' ? 'animate-bounce' : ''}`}>
                {achievement.icon}
              </div>
            </div>
            
            <div className="flex-1">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                    Achievement Unlocked!
                  </h3>
                  <p className="text-sm font-semibold text-gray-800 dark:text-gray-200 mt-1">
                    {achievement.name}
                  </p>
                  <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                    {achievement.description}
                  </p>
                  <div className="flex items-center mt-2 space-x-2">
                    <span className={`text-xs px-2 py-1 rounded-full bg-gradient-to-r ${rarityColors} text-white font-bold`}>
                      {achievement.rarity.toUpperCase()}
                    </span>
                    <span className="text-xs font-bold text-yellow-600 dark:text-yellow-400">
                      +{achievement.points} XP
                    </span>
                  </div>
                </div>
                
                <button
                  onClick={handleClose}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <XMarkIcon className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}