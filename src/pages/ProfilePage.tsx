import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import { UserProgress } from '../types/database.types'
import { TrophyIcon, ClockIcon, StarIcon } from '@heroicons/react/24/outline'

const ProfilePage: React.FC = () => {
  const { user } = useAuth()
  const [progress, setProgress] = useState<UserProgress[]>([])
  const [stats, setStats] = useState({
    completedLessons: 0,
    averageRating: 0,
    totalTimeSpent: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user) {
      fetchUserProgress()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const fetchUserProgress = async () => {
    if (!user) return

    try {
      const { data, error } = await supabase
        .from('user_progress')
        .select('*')
        .eq('user_id', user.id)

      if (error) throw error

      if (data) {
        setProgress(data as any)
        
        const completed = data.filter(p => p.status === 'completed')
        const avgRating = completed.length > 0
          ? completed.reduce((acc, p) => acc + p.rating, 0) / completed.length
          : 0

        setStats({
          completedLessons: completed.length,
          averageRating: Math.round(avgRating),
          totalTimeSpent: 0
        })
      }
    } catch (error) {
      console.error('Error fetching progress:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">My Profile</h1>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">Completed Lessons</p>
              <p className="text-3xl font-bold">{stats.completedLessons}</p>
            </div>
            <TrophyIcon className="h-10 w-10 text-primary-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">Average Rating</p>
              <p className="text-3xl font-bold">{stats.averageRating}%</p>
            </div>
            <StarIcon className="h-10 w-10 text-yellow-500" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">Email</p>
              <p className="text-sm font-medium truncate">{user?.email}</p>
            </div>
            <ClockIcon className="h-10 w-10 text-secondary-600" />
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Recent Progress</h2>
        
        {progress.length === 0 ? (
          <p className="text-neutral-600 dark:text-neutral-400">
            No learning progress yet. Start exploring the skill tree!
          </p>
        ) : (
          <div className="space-y-3">
            {progress.map((item) => (
              <div 
                key={item.id}
                className="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-900 rounded-lg"
              >
                <div>
                  <h3 className="font-medium">Learning Progress</h3>
                  <p className="text-sm text-neutral-600 dark:text-neutral-400">
                    Status: {item.status} | Rating: {item.rating}%
                  </p>
                </div>
                <span className="text-xs text-neutral-500">
                  {new Date(item.last_accessed).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ProfilePage