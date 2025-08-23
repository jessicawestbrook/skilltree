import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import CategoryLink from './CategoryLink'
import { recommendationService, RecommendationScore } from '../services/recommendationService'
import { 
  SparklesIcon, 
  ArrowRightIcon, 
  BookOpenIcon,
  TrophyIcon,
  FireIcon,
  LightBulbIcon,
  ClockIcon,
  AcademicCapIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'

const RecommendedContent: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [recommendations, setRecommendations] = useState<RecommendationScore[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  useEffect(() => {
    if (user) {
      fetchRecommendations()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, selectedCategory])

  const fetchRecommendations = async () => {
    if (!user) return

    setLoading(true)
    try {
      const recs = await recommendationService.getRecommendations(user.id, {
        maxRecommendations: 12,
        excludeCompleted: selectedCategory !== 'review',
        focusOnStarred: selectedCategory === 'interest'
      })
      
      // Filter by category if selected
      if (selectedCategory !== 'all') {
        setRecommendations(recs.filter(r => r.category === selectedCategory))
      } else {
        setRecommendations(recs)
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error)
    } finally {
      setLoading(false)
    }
  }

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'ready_to_learn':
        return <BookOpenIcon className="h-5 w-5" />
      case 'challenge':
        return <FireIcon className="h-5 w-5" />
      case 'review':
        return <ClockIcon className="h-5 w-5" />
      case 'interest':
        return <SparklesIcon className="h-5 w-5" />
      case 'skill_gap':
        return <ChartBarIcon className="h-5 w-5" />
      default:
        return <AcademicCapIcon className="h-5 w-5" />
    }
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'ready_to_learn':
        return 'text-green-600 bg-green-50 dark:bg-green-900/20'
      case 'challenge':
        return 'text-red-600 bg-red-50 dark:bg-red-900/20'
      case 'review':
        return 'text-blue-600 bg-blue-50 dark:bg-blue-900/20'
      case 'interest':
        return 'text-purple-600 bg-purple-50 dark:bg-purple-900/20'
      case 'skill_gap':
        return 'text-orange-600 bg-orange-50 dark:bg-orange-900/20'
      default:
        return 'text-neutral-600 bg-neutral-50 dark:bg-neutral-900/20'
    }
  }

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'ready_to_learn':
        return 'Ready to Learn'
      case 'challenge':
        return 'Challenge Yourself'
      case 'review':
        return 'Review & Strengthen'
      case 'interest':
        return 'Based on Interests'
      case 'skill_gap':
        return 'Fill Skill Gaps'
      default:
        return category
    }
  }


  if (!user) {
    return (
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
        <div className="flex items-center gap-2 mb-4">
          <LightBulbIcon className="h-6 w-6 text-primary-600" />
          <h2 className="text-xl font-bold">Recommended Learning</h2>
        </div>
        <p className="text-neutral-600 dark:text-neutral-400">
          Sign in to get personalized recommendations
        </p>
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <LightBulbIcon className="h-6 w-6 text-primary-600" />
          <h2 className="text-xl font-bold">Recommended for You</h2>
        </div>
        <TrophyIcon className="h-5 w-5 text-gold-500" />
      </div>

      {/* Category Filter Tabs - More compact */}
      <div className="grid grid-cols-3 gap-1.5 mb-6">
        <button
          onClick={() => setSelectedCategory('all')}
          className={`px-2 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            selectedCategory === 'all'
              ? 'bg-primary-600 text-white'
              : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setSelectedCategory('ready_to_learn')}
          className={`px-2 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            selectedCategory === 'ready_to_learn'
              ? 'bg-primary-600 text-white'
              : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
          }`}
          title="Ready to Learn"
        >
          <span className="flex items-center justify-center gap-1">
            <BookOpenIcon className="h-3.5 w-3.5" />
            <span className="hidden xl:inline">Ready</span>
          </span>
        </button>
        <button
          onClick={() => setSelectedCategory('challenge')}
          className={`px-2 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            selectedCategory === 'challenge'
              ? 'bg-primary-600 text-white'
              : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
          }`}
          title="Challenge Yourself"
        >
          <span className="flex items-center justify-center gap-1">
            <FireIcon className="h-3.5 w-3.5" />
            <span className="hidden xl:inline">Challenge</span>
          </span>
        </button>
        <button
          onClick={() => setSelectedCategory('review')}
          className={`px-2 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            selectedCategory === 'review'
              ? 'bg-primary-600 text-white'
              : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
          }`}
          title="Review & Strengthen"
        >
          <span className="flex items-center justify-center gap-1">
            <ClockIcon className="h-3.5 w-3.5" />
            <span className="hidden xl:inline">Review</span>
          </span>
        </button>
        <button
          onClick={() => setSelectedCategory('interest')}
          className={`px-2 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            selectedCategory === 'interest'
              ? 'bg-primary-600 text-white'
              : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
          }`}
          title="Based on Interests"
        >
          <span className="flex items-center justify-center gap-1">
            <SparklesIcon className="h-3.5 w-3.5" />
            <span className="hidden xl:inline">Interest</span>
          </span>
        </button>
        <button
          onClick={() => setSelectedCategory('skill_gap')}
          className={`px-2 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            selectedCategory === 'skill_gap'
              ? 'bg-primary-600 text-white'
              : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
          }`}
          title="Fill Skill Gaps"
        >
          <span className="flex items-center justify-center gap-1">
            <ChartBarIcon className="h-3.5 w-3.5" />
            <span className="hidden xl:inline">Gaps</span>
          </span>
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      ) : recommendations.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-neutral-600 dark:text-neutral-400">
            {selectedCategory === 'review' 
              ? 'No content needs review right now'
              : 'Complete some prerequisites to unlock new recommendations'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {recommendations.slice(0, 6).map((rec) => (
            <CategoryLink
              key={rec.node.id}
              categoryId={rec.node.id}
              className="group cursor-pointer bg-neutral-50 dark:bg-neutral-900 rounded-lg p-4 hover:shadow-md transition-all block"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`p-1 rounded ${getCategoryColor(rec.category)}`}>
                      {getCategoryIcon(rec.category)}
                    </span>
                    <span className="text-xs text-neutral-500 uppercase tracking-wider">
                      {getCategoryLabel(rec.category)}
                    </span>
                  </div>
                  
                  <h3 className="font-semibold text-neutral-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                    {rec.node.name}
                  </h3>
                  
                  {rec.node.learning_area && (
                    <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-1 line-clamp-2">
                      {rec.node.learning_area}
                    </p>
                  )}
                  
                  {/* Recommendation Reasons */}
                  <div className="flex flex-wrap gap-2 mt-3">
                    {rec.reasons.slice(0, 2).map((reason, idx) => (
                      <span
                        key={idx}
                        className="text-xs px-2 py-1 bg-white dark:bg-neutral-800 rounded-full text-neutral-600 dark:text-neutral-400"
                      >
                        {reason}
                      </span>
                    ))}
                  </div>

                  {/* Score Indicator */}
                  <div className="flex items-center gap-2 mt-3">
                    <div className="flex-1 bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all"
                        style={{ width: `${Math.round(rec.score * 100)}%` }}
                      />
                    </div>
                    <span className="text-xs text-neutral-500">
                      {Math.round(rec.score * 100)}% match
                    </span>
                  </div>
                </div>
                
                <ArrowRightIcon className="h-5 w-5 text-neutral-400 group-hover:text-primary-600 transition-colors ml-4 mt-4" />
              </div>
            </CategoryLink>
          ))}
        </div>
      )}

      {recommendations.length > 6 && (
        <button
          onClick={() => navigate('/recommendations')}
          className="w-full mt-4 py-2 text-center text-primary-600 hover:text-primary-700 font-medium"
        >
          View All Recommendations ({recommendations.length})
        </button>
      )}
    </div>
  )
}

export default RecommendedContent