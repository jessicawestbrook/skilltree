import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { achievementService, Achievement, UserAchievement } from '../services/achievementService'
import { useAuth } from './AuthContext'
import { useNotifications } from './NotificationContext'
import { AchievementNotification } from '../components/AchievementNotification'

interface AchievementContextType {
  userAchievements: UserAchievement[]
  totalPoints: number
  loading: boolean
  refreshAchievements: () => Promise<void>
  checkForNewAchievements: () => Promise<void>
}

const AchievementContext = createContext<AchievementContextType | undefined>(undefined)

export const useAchievements = () => {
  const context = useContext(AchievementContext)
  if (context === undefined) {
    throw new Error('useAchievements must be used within an AchievementProvider')
  }
  return context
}

interface AchievementProviderProps {
  children: ReactNode
}

export const AchievementProvider: React.FC<AchievementProviderProps> = ({ children }) => {
  const { user } = useAuth()
  const { notifications, markAsRead } = useNotifications()
  const [userAchievements, setUserAchievements] = useState<UserAchievement[]>([])
  const [totalPoints, setTotalPoints] = useState(0)
  const [loading, setLoading] = useState(false)
  const [displayAchievement, setDisplayAchievement] = useState<Achievement | null>(null)

  useEffect(() => {
    if (user) {
      refreshAchievements()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])


  // Listen for new achievement notifications
  useEffect(() => {
    if (notifications && notifications.length > 0) {
      const latestNotification = notifications[0]
      
      // Check if we've already displayed this notification (persisted across page loads)
      const displayedIds = JSON.parse(localStorage.getItem('displayedAchievementNotifications') || '[]') as string[]
      
      if (
        latestNotification.type === 'achievement' &&
        !displayedIds.includes(latestNotification.id) &&
        !latestNotification.is_read
      ) {
        // Extract achievement data from notification
        const achievementData = latestNotification.data as any
        if (achievementData) {
          setDisplayAchievement({
            id: achievementData.achievement_id,
            code: achievementData.achievement_code,
            name: latestNotification.title.replace('Achievement Unlocked: ', '').replace('!', ''),
            description: latestNotification.message,
            icon: achievementData.icon || '🏆',
            badge_color: achievementData.badge_color || 'gold',
            rarity: achievementData.rarity || 'common',
            points: achievementData.points || 10,
            category: 'special',
            requirement_type: 'special',
            requirement_value: 1,
            is_active: true,
            is_secret: false
          })
          
          // Store this ID in localStorage to prevent re-display
          const updatedIds = [...displayedIds, latestNotification.id].slice(-50) // Keep only last 50
          localStorage.setItem('displayedAchievementNotifications', JSON.stringify(updatedIds))
          
          // Mark the notification as read after displaying it
          markAsRead(latestNotification.id)
        }
      }
    }
  }, [notifications, markAsRead])

  const refreshAchievements = async () => {
    if (!user) return

    setLoading(true)
    try {
      const achievements = await achievementService.getUserAchievements(user.id)
      setUserAchievements(achievements)
      
      // Calculate total points
      const points = achievements
        .filter(ua => ua.unlocked_at)
        .reduce((sum, ua) => sum + (ua.achievement?.points || 0), 0)
      setTotalPoints(points)
    } catch (error) {
      console.error('Error fetching achievements:', error)
    } finally {
      setLoading(false)
    }
  }

  const checkForNewAchievements = async () => {
    if (!user) return
    
    // This would be called after certain actions to check for new achievements
    await achievementService.checkAchievements(user.id, 'manual_check')
    await refreshAchievements()
  }

  const value: AchievementContextType = {
    userAchievements,
    totalPoints,
    loading,
    refreshAchievements,
    checkForNewAchievements
  }

  return (
    <AchievementContext.Provider value={value}>
      {children}
      <AchievementNotification
        achievement={displayAchievement}
        onClose={() => setDisplayAchievement(null)}
      />
    </AchievementContext.Provider>
  )
}