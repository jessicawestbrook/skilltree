import React from 'react'
import { Link } from 'react-router-dom'
import { 
  AcademicCapIcon, 
  SparklesIcon, 
  ChartBarIcon,
  UserGroupIcon,
  BookOpenIcon,
  TrophyIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline'
import MegaMenu from '../components/MegaMenu'
import SEO from '../components/SEO'
import { useAuth } from '../contexts/AuthContext'
import { createOrganizationStructuredData } from '../utils/structuredData'

const HomePage: React.FC = () => {
  const { user } = useAuth()
  
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

  return (
    <>
      <SEO
        structuredData={createOrganizationStructuredData()}
      />
      <div className="space-y-8">
      <section className="text-center pt-3 pb-1">
        <h1 className="text-3xl font-bold mb-2 text-primary-600 dark:text-primary-400">
          Welcome to SkillTree
        </h1>
        <p className="text-base text-neutral-600 dark:text-neutral-400 max-w-xl mx-auto">
          Your path to mastering everything you've ever dreamed of learning. 
          Navigate knowledge like a video game and level up your skills.
        </p>
      </section>

      <MegaMenu />

      <section className="py-8">
        <h2 className="text-3xl font-bold text-center mb-12">
          Learning That Feels Like Playing
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="card hover:shadow-xl transition-shadow">
              <div className="text-primary-600 dark:text-primary-400 mb-4">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-neutral-600 dark:text-neutral-400">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

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