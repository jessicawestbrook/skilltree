import React from 'react'
import { Link } from 'react-router-dom'
import { 
  AcademicCapIcon, 
  SparklesIcon, 
  ChartBarIcon,
  UserGroupIcon,
  BookOpenIcon,
  TrophyIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline'
import SearchBar from '../components/SearchBar'
import MegaMenu from '../components/MegaMenu'
import { useAuth } from '../contexts/AuthContext'

const HomePage: React.FC = () => {
  const { user } = useAuth()
  
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
    <div className="space-y-12">
      <section className="text-center py-12">
        <h1 className="text-5xl font-bold mb-4">
          <span className="bg-gradient-to-r from-primary-600 to-gold-500 bg-clip-text text-transparent">
            Welcome to SkillTree
          </span>
        </h1>
        <p className="text-xl text-neutral-600 dark:text-neutral-400 max-w-3xl mx-auto mb-8">
          Your path to mastering everything you've ever dreamed of learning. 
          Navigate knowledge like a video game and level up your skills.
        </p>
        <div className="flex gap-4 justify-center mb-8">
          <Link to="/skill-tree" className="btn-primary text-lg px-8 py-3">
            Explore Skill Tree
          </Link>
          <Link to="/signup" className="btn-secondary text-lg px-8 py-3">
            Get Started Free
          </Link>
        </div>
        
        {/* Search Bar */}
        <div className="max-w-2xl mx-auto">
          <SearchBar placeholder="Search for any topic you want to learn..." />
          <div className="mt-3 text-center">
            <Link 
              to="/search" 
              className="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 flex items-center justify-center gap-1"
            >
              <MagnifyingGlassIcon className="h-4 w-4" />
              Advanced Search
            </Link>
          </div>
        </div>
      </section>

      {/* Mega Menu - Top 3 Skill Tree Categories */}
      <MegaMenu />

      <section>
        <h2 className="text-3xl font-bold text-center mb-8">
          Learning That Feels Like Playing
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
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
            <Link to="/skill-tree" className="btn-primary text-lg px-8 py-3">
              Explore Skill Tree
            </Link>
          )}
        </div>
      </section>
    </div>
  )
}

export default HomePage