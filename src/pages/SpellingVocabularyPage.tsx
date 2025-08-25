import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { 
  BookOpenIcon,
  LanguageIcon
} from '@heroicons/react/24/outline'

// Import the components directly
import SpellingPage from './SpellingPage'
import VocabularyTrainerPage from './VocabularyTrainerPage'

const SpellingVocabularyPage: React.FC = () => {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState<'vocabulary' | 'spelling'>('vocabulary')

  // Check if there's a tab preference in the location state
  useEffect(() => {
    if (location.state?.tab) {
      setActiveTab(location.state.tab)
    }
  }, [location.state])

  return (
    <div className="max-w-4xl mx-auto p-1 sm:p-2 pt-2 sm:pt-2">
      {/* Tab Navigation */}
      <div className="mb-4">
        <div className="border-b border-neutral-200 dark:border-neutral-700">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            <button
              onClick={() => setActiveTab('vocabulary')}
              className={`
                group inline-flex items-center py-2 px-1 border-b-2 font-medium text-sm transition-colors
                ${activeTab === 'vocabulary'
                  ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                  : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300 dark:text-neutral-400 dark:hover:text-neutral-300 dark:hover:border-neutral-600'
                }
              `}
            >
              <BookOpenIcon className={`
                -ml-0.5 mr-2 h-5 w-5
                ${activeTab === 'vocabulary'
                  ? 'text-primary-500 dark:text-primary-400'
                  : 'text-neutral-400 group-hover:text-neutral-500 dark:text-neutral-500 dark:group-hover:text-neutral-400'
                }
              `} />
              Vocabulary
            </button>

            <button
              onClick={() => setActiveTab('spelling')}
              className={`
                group inline-flex items-center py-2 px-1 border-b-2 font-medium text-sm transition-colors
                ${activeTab === 'spelling'
                  ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                  : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300 dark:text-neutral-400 dark:hover:text-neutral-300 dark:hover:border-neutral-600'
                }
              `}
            >
              <LanguageIcon className={`
                -ml-0.5 mr-2 h-5 w-5
                ${activeTab === 'spelling'
                  ? 'text-primary-500 dark:text-primary-400'
                  : 'text-neutral-400 group-hover:text-neutral-500 dark:text-neutral-500 dark:group-hover:text-neutral-400'
                }
              `} />
              Spelling
            </button>
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'vocabulary' ? (
          <VocabularyTrainerPage showTabs={false} onTabChange={setActiveTab} />
        ) : (
          <SpellingPage showTabs={false} onTabChange={setActiveTab} />
        )}
      </div>
    </div>
  )
}

export default SpellingVocabularyPage