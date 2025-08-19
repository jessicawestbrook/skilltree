import React, { useState, useEffect } from 'react'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import { 
  ChartBarIcon
} from '@heroicons/react/24/outline'

interface SpellingStats {
  totalWords: number
  wordsAttempted: number
  correctWords: number
  byDifficulty: {
    [key: string]: {
      total: number
      attempted: number
      correct: number
    }
  }
}

const SpellingBeeMenu: React.FC = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState<SpellingStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const fetchStats = async () => {
    try {
      // Get total words count
      const { count: totalWords } = await supabase
        .from('spelling_words')
        .select('*', { count: 'exact', head: true })

      if (user) {
        // Get user's attempts
        const { data: attempts } = await supabase
          .from('user_spelling_attempts')
          .select(`
            correct,
            word_id,
            spelling_words (
              difficulty_name
            )
          `)
          .eq('user_id', user.id)

        // Calculate stats
        const uniqueWordIds = new Set(attempts?.map(a => a.word_id))
        const wordsAttempted = uniqueWordIds.size
        const correctWords = attempts?.filter(a => a.correct).length || 0

        // Group by difficulty
        const byDifficulty: any = {}
        const difficulties = ['Beginner', 'Elementary', 'Intermediate', 'Advanced', 'Expert']
        
        for (const diff of difficulties) {
          const { count } = await supabase
            .from('spelling_words')
            .select('*', { count: 'exact', head: true })
            .eq('difficulty_name', diff)

          const diffAttempts = attempts?.filter((a: any) => a.spelling_words?.difficulty_name === diff) || []
          const diffCorrect = diffAttempts.filter((a: any) => a.correct).length

          byDifficulty[diff] = {
            total: count || 0,
            attempted: diffAttempts.length,
            correct: diffCorrect
          }
        }

        setStats({
          totalWords: totalWords || 0,
          wordsAttempted,
          correctWords,
          byDifficulty
        })
      } else {
        setStats({
          totalWords: totalWords || 0,
          wordsAttempted: 0,
          correctWords: 0,
          byDifficulty: {}
        })
      }
    } catch (error) {
      console.error('Error fetching spelling bee stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const difficultyColors = {
    Beginner: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
    Elementary: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
    Intermediate: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
    Advanced: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400',
    Expert: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
  }

  if (loading) {
    return (
      <div className="bg-white dark:bg-neutral-900 rounded-lg shadow-md p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-neutral-200 dark:bg-neutral-700 rounded w-3/4"></div>
          <div className="h-4 bg-neutral-200 dark:bg-neutral-700 rounded w-1/2"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-neutral-900 rounded-lg shadow-md p-4 space-y-4">

      {/* Progress Overview */}
      {user && stats && (
        <div>
          <h3 className="text-sm font-bold mb-3 flex items-center gap-1">
            <ChartBarIcon className="h-4 w-4 text-primary-600" />
            Progress Overview
          </h3>
          
          <div className="space-y-3">
            {/* Overall Progress */}
            <div className="bg-neutral-50 dark:bg-neutral-800 rounded p-3">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-medium">Overall Progress</span>
                <span className="text-xs text-neutral-600 dark:text-neutral-400">
                  {stats.wordsAttempted}/{stats.totalWords}
                </span>
              </div>
              <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                <div 
                  className="bg-primary-600 h-2 rounded-full transition-all"
                  style={{ width: `${(stats.wordsAttempted / stats.totalWords) * 100}%` }}
                />
              </div>
              {stats.wordsAttempted > 0 && (
                <div className="mt-1 text-xs text-neutral-600 dark:text-neutral-400">
                  Accuracy: {Math.round((stats.correctWords / stats.wordsAttempted) * 100)}%
                </div>
              )}
            </div>

            {/* Progress by Difficulty */}
            <div className="space-y-2">
              <div className="text-xs font-medium text-neutral-700 dark:text-neutral-300">By Difficulty</div>
              <div className="space-y-1">
                {Object.entries(stats.byDifficulty).map(([level, data]) => {
                  if (data.total === 0) return null
                  const shortLevel = level.substring(0, 3) // Beg, Ele, Int, Adv, Exp
                  
                  return (
                    <div key={level} className="flex items-center gap-2 text-xs">
                      <span className={`px-1.5 py-0.5 rounded font-medium min-w-[2.5rem] text-center ${difficultyColors[level as keyof typeof difficultyColors]}`}>
                        {shortLevel}
                      </span>
                      <div className="flex-1 bg-neutral-200 dark:bg-neutral-700 rounded-full h-1.5">
                        <div 
                          className="bg-primary-600 h-1.5 rounded-full"
                          style={{ width: `${(data.attempted / data.total) * 100}%` }}
                        />
                      </div>
                      <span className="text-xs text-neutral-500 min-w-[2rem] text-right">
                        {data.attempted}/{data.total}
                      </span>
                    </div>
                  )
                })}
              </div>
            </div>

          </div>
        </div>
      )}

    </div>
  )
}

export default SpellingBeeMenu