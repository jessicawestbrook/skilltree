import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  AcademicCapIcon, 
  SparklesIcon, 
  ChartBarIcon,
  UserGroupIcon,
  BookOpenIcon,
  TrophyIcon,
  LightBulbIcon,
  ChatBubbleBottomCenterTextIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline'
import MegaMenu from '../components/MegaMenu'
import SEO from '../components/SEO'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../services/supabase'
import { createOrganizationStructuredData } from '../utils/structuredData'

const HomePage: React.FC = () => {
  const { user } = useAuth()
  const [hasCompletedAssessment, setHasCompletedAssessment] = useState(false)
  const [checkingAssessment, setCheckingAssessment] = useState(true)
  
  const learningFacts = [
    {
      fact: "Each year of education increases cognitive abilities",
      source: "American Psychological Association",
      url: "https://www.apa.org/science/about/psa/2017/10/education-cognitive"
    },
    {
      fact: "Adult brains can form new neural connections throughout life",
      source: "Harvard Health Publishing",
      url: "https://www.health.harvard.edu/mind-and-mood/the-science-of-neuroplasticity"
    },
    {
      fact: "Continuous learning may help prevent cognitive decline",
      source: "Mayo Clinic",
      url: "https://www.mayoclinic.org/healthy-lifestyle/healthy-aging/in-depth/memory-loss/art-20046326"
    },
    {
      fact: "Learning multiple languages enhances cognitive flexibility",
      source: "National Institute of Health",
      url: "https://www.nih.gov/news-events/nih-research-matters/learning-second-language-protects-against-alzheimers"
    },
    {
      fact: "Mental exercises can strengthen brain structure",
      source: "National Institute on Aging",
      url: "https://www.nia.nih.gov/health/brain-health/cognitive-training-research"
    },
    {
      fact: "Mathematical thinking improves problem-solving abilities",
      source: "Stanford Education",
      url: "https://ed.stanford.edu/news/math-learning-difference"
    }
  ]
  
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const features = [
    {
      icon: <AcademicCapIcon className="h-8 w-8" />,
      title: 'Interactive Skill Tree',
      description: 'Navigate through knowledge like a video game skill tree'
    },
    {
      icon: <SparklesIcon className="h-8 w-8" />,
      title: 'Gamified Learning',
      description: 'Earn ratings and track progress as you master new skills'
    },
    {
      icon: <ChartBarIcon className="h-8 w-8" />,
      title: 'Personalized Path',
      description: 'Get recommendations based on your interests and progress'
    },
    {
      icon: <UserGroupIcon className="h-8 w-8" />,
      title: 'All Ages Welcome',
      description: 'Content for homeschooling, supplemental, and lifelong learning'
    },
    {
      icon: <BookOpenIcon className="h-8 w-8" />,
      title: 'Comprehensive Content',
      description: 'From basic skills to advanced topics across all subjects'
    },
    {
      icon: <TrophyIcon className="h-8 w-8" />,
      title: 'Track Achievement',
      description: 'Monitor your learning journey and celebrate milestones'
    }
  ]

  useEffect(() => {
    const checkAssessmentCompletion = async () => {
      if (!user) {
        setCheckingAssessment(false)
        setHasCompletedAssessment(false)
        return
      }

      try {
        const { data, error } = await supabase
          .from('user_interest_levels')
          .select('id')
          .eq('user_id', user.id)
          .limit(1)

        if (error) {
          console.error('Error checking assessment completion:', error)
          setHasCompletedAssessment(false)
        } else {
          setHasCompletedAssessment(data && data.length > 0)
        }
      } catch (error) {
        console.error('Error checking assessment completion:', error)
        setHasCompletedAssessment(false)
      } finally {
        setCheckingAssessment(false)
      }
    }

    checkAssessmentCompletion()
  }, [user])

  return (
    <>
      <SEO
        structuredData={createOrganizationStructuredData()}
      />
      <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-primary-600 dark:text-primary-400">
          Welcome to SkillTree
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-3xl mx-auto mb-6">
          Your personal memory palace for lifelong learning. Build lasting knowledge 
          through interactive skill trees and science-backed learning methods.
        </p>
        
        {!user ? (
          <div className="bg-gradient-to-r from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 rounded-lg p-4 max-w-md mx-auto border border-primary-200 dark:border-primary-800">
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
              Get personalized learning recommendations based on your interests
            </p>
            <Link 
              to="/intro-assessment" 
              className="btn-primary inline-block px-6 py-2 text-sm"
            >
              Take Interests Quiz
            </Link>
          </div>
        ) : !checkingAssessment ? (
          !hasCompletedAssessment ? (
            <div className="bg-gradient-to-r from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 rounded-lg p-4 max-w-md mx-auto border border-primary-200 dark:border-primary-800">
              <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
                Get personalized learning recommendations based on your interests
              </p>
              <Link 
                to="/intro-assessment" 
                className="btn-primary inline-block px-6 py-2 text-sm"
              >
                Take Interests Quiz
              </Link>
            </div>
          ) : (
            <div className="bg-gradient-to-r from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 rounded-lg p-4 max-w-md mx-auto border border-primary-200 dark:border-primary-800">
              <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
                Update your learning interests to get fresh recommendations
              </p>
              <Link 
                to="/intro-assessment" 
                className="btn-secondary inline-block px-6 py-2 text-sm"
              >
                Update Interests
              </Link>
            </div>
          )
        ) : null}
      </div>

      {/* Flashcard Practice Section */}
      <section className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold text-center mb-4 text-neutral-900 dark:text-neutral-100">
          Practice with Flashcards
        </h2>
        <div className="grid md:grid-cols-3 gap-4">
          <Link 
            to="/spelling-bee"
            className="group bg-gradient-to-br from-green-50 to-primary-50 dark:from-green-900/10 dark:to-primary-900/10 rounded-lg p-4 border border-green-200 dark:border-green-800 hover:shadow-lg transition-all hover:scale-105"
          >
            <div className="text-center">
              <ChatBubbleBottomCenterTextIcon className="h-8 w-8 text-green-600 dark:text-green-400 mx-auto mb-2 group-hover:scale-110 transition-transform" />
              <h3 className="text-lg font-semibold mb-1 text-neutral-900 dark:text-white">
                Spelling Bee Trainer
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Master spelling with audio pronunciation and etymology tips
              </p>
            </div>
          </Link>
          
          <Link 
            to="/vocabulary-trainer"
            className="group bg-gradient-to-br from-blue-50 to-primary-50 dark:from-blue-900/10 dark:to-primary-900/10 rounded-lg p-4 border border-blue-200 dark:border-blue-800 hover:shadow-lg transition-all hover:scale-105"
          >
            <div className="text-center">
              <BookOpenIcon className="h-8 w-8 text-blue-600 dark:text-blue-400 mx-auto mb-2 group-hover:scale-110 transition-transform" />
              <h3 className="text-lg font-semibold mb-1 text-neutral-900 dark:text-white">
                Vocabulary Trainer
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Expand your vocabulary with contextual definitions and examples
              </p>
            </div>
          </Link>
          
          <Link 
            to="/language-trainer"
            className="group bg-gradient-to-br from-purple-50 to-primary-50 dark:from-purple-900/10 dark:to-primary-900/10 rounded-lg p-4 border border-purple-200 dark:border-purple-800 hover:shadow-lg transition-all hover:scale-105"
          >
            <div className="text-center">
              <GlobeAltIcon className="h-8 w-8 text-purple-600 dark:text-purple-400 mx-auto mb-2 group-hover:scale-110 transition-transform" />
              <h3 className="text-lg font-semibold mb-1 text-neutral-900 dark:text-white">
                Language Trainer
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Learn foreign languages with interactive flashcards
              </p>
            </div>
          </Link>
        </div>
      </section>

      <MegaMenu />

      <section className="py-8">
        <div className="text-center mb-8">
          <LightBulbIcon className="h-12 w-12 text-gold-500 mx-auto mb-4" />
          <h2 className="text-3xl font-bold mb-4">The Science of Learning</h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
            Research shows that continuous learning transforms your brain and enhances your life
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {learningFacts.map((item, index) => (
            <div key={index} className="bg-gradient-to-br from-gold-50 to-primary-50 dark:from-gold-900/10 dark:to-primary-900/10 rounded-lg p-6 border border-gold-200 dark:border-gold-800">
              <p className="text-lg font-semibold text-neutral-800 dark:text-neutral-200 mb-2">
                {item.fact}
              </p>
              <p className="text-sm text-neutral-600 dark:text-neutral-400 italic">
                — <a 
                    href={item.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 hover:underline transition-colors"
                  >
                    {item.source}
                  </a>
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-gradient-to-r from-primary-100 to-gold-100 dark:from-primary-900/20 dark:to-gold-900/20 rounded-2xl p-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Your Journey?</h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-6">
            Join thousands of learners who are leveling up their knowledge every day
          </p>
          {!user ? (
            <Link to="/signup" className="btn-primary text-lg px-8 py-3">
              Create Free Account
            </Link>
          ) : (
            <Link to="/learning-paths" className="btn-primary text-lg px-8 py-3">
              Explore Learning Paths
            </Link>
          )}
        </div>
      </section>
    </div>
    </>
  )
}

export default HomePage