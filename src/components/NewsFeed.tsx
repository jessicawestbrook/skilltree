import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  NewspaperIcon,
  SparklesIcon,
  BookOpenIcon,
  AcademicCapIcon,
  TrophyIcon,
  ChartBarIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline'
import { newsService, NewsItem } from '../services/newsService'

const NewsFeed: React.FC = () => {
  const [newsItems, setNewsItems] = useState<NewsItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadNews()
  }, [])

  const loadNews = async () => {
    try {
      const items = await newsService.getPublishedNews(5)
      setNewsItems(items)
    } catch (error) {
      console.error('Error loading news:', error)
      // Use fallback news items if database is not available
      setNewsItems([
        {
          id: 'spelling-bee',
          date_posted: '2025-08-01',
          icon_name: 'SparklesIcon',
          title: 'Scripps Spelling Bee Study Lists Added',
          description: 'Master spelling with official Scripps National Spelling Bee word lists, now available in our spelling and vocabulary flashcards.',
          link: '/spelling-bee?tab=spelling',
          link_text: 'Start Practicing',
          is_published: true,
          display_order: 1,
          created_at: '',
          updated_at: ''
        },
        {
          id: 'spanish-vocab',
          date_posted: '2025-08-01',
          icon_name: 'BookOpenIcon',
          title: '35,000 Spanish Vocabulary Words',
          description: 'Comprehensive Spanish vocabulary flashcards covering the most common words from beginner to advanced levels.',
          link: '/language-trainer?language=spanish&tab=vocabulary',
          link_text: 'Learn Spanish',
          is_published: true,
          display_order: 2,
          created_at: '',
          updated_at: ''
        },
        {
          id: 'latin-course',
          date_posted: '2025-08-01',
          icon_name: 'AcademicCapIcon',
          title: '4-Year Latin Learning Path',
          description: 'Complete Latin curriculum based on the Henle textbooks, digitized into an interactive online learning format with exercises and assessments.',
          link: '/learning-paths/complete-henle-latin-program',
          link_text: 'Explore Latin Path',
          is_published: true,
          display_order: 3,
          created_at: '',
          updated_at: ''
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const getIcon = (iconName?: string) => {
    const iconClass = "h-5 w-5"
    switch (iconName) {
      case 'SparklesIcon':
        return <SparklesIcon className={iconClass} />
      case 'BookOpenIcon':
        return <BookOpenIcon className={iconClass} />
      case 'AcademicCapIcon':
        return <AcademicCapIcon className={iconClass} />
      case 'TrophyIcon':
        return <TrophyIcon className={iconClass} />
      case 'ChartBarIcon':
        return <ChartBarIcon className={iconClass} />
      case 'LightBulbIcon':
        return <LightBulbIcon className={iconClass} />
      default:
        return <NewspaperIcon className={iconClass} />
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
  }

  if (loading) {
    return (
      <section className="bg-gradient-to-br from-primary-50/50 to-gold-50/50 dark:from-primary-900/10 dark:to-gold-900/10 rounded-xl p-6 border border-primary-200 dark:border-primary-800">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="bg-white dark:bg-neutral-900 rounded-lg p-4">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
              </div>
            ))}
          </div>
        </div>
      </section>
    )
  }

  if (newsItems.length === 0) {
    return null
  }

  return (
    <section className="bg-gradient-to-br from-primary-50/50 to-gold-50/50 dark:from-primary-900/10 dark:to-gold-900/10 rounded-xl p-6 border border-primary-200 dark:border-primary-800">
      <div className="flex items-center mb-4">
        <NewspaperIcon className="h-6 w-6 text-primary-600 dark:text-primary-400 mr-2" />
        <h2 className="text-2xl font-bold text-neutral-900 dark:text-neutral-100">
          What's New on SkillTree
        </h2>
      </div>
      
      <div className="space-y-4">
        {newsItems.map((item) => (
          <div 
            key={item.id}
            className="bg-white dark:bg-neutral-900 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 mt-1">
                <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg text-primary-600 dark:text-primary-400">
                  {getIcon(item.icon_name)}
                </div>
              </div>
              
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-1">
                  <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">
                    {item.title}
                  </h3>
                  <span className="text-xs text-neutral-500 dark:text-neutral-400 bg-neutral-100 dark:bg-neutral-800 px-2 py-1 rounded">
                    {formatDate(item.date_posted)}
                  </span>
                </div>
                
                <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                  {item.description}
                </p>
                
                {item.link && (
                  <Link 
                    to={item.link}
                    className="inline-flex items-center text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
                  >
                    {item.link_text || 'Learn More'}
                    <svg className="ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </Link>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 pt-4 border-t border-primary-200 dark:border-primary-700">
        <p className="text-xs text-center text-neutral-500 dark:text-neutral-400">
          Stay tuned for more updates and new learning content!
        </p>
      </div>
    </section>
  )
}

export default NewsFeed