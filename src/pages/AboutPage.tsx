import React from 'react'
import { Link } from 'react-router-dom'
import {
  AcademicCapIcon,
  BookOpenIcon,
  LightBulbIcon,
  SparklesIcon,
  UserGroupIcon,
  BeakerIcon,
  ChartBarIcon,
  BuildingLibraryIcon,
  EnvelopeIcon,
  HeartIcon
} from '@heroicons/react/24/outline'

const AboutPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl md:text-5xl font-bold text-primary-600 dark:text-primary-400">
          About SkillTree
        </h1>
        <p className="text-xl text-neutral-600 dark:text-neutral-400 max-w-3xl mx-auto">
          Your personal memory palace for lifelong learning
        </p>
      </div>

      {/* Vision Section */}
      <section className="bg-gradient-to-r from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3 mb-4">
          <BuildingLibraryIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
          <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">
            Our Vision: A Modern Memory Palace
          </h2>
        </div>
        <p className="text-neutral-700 dark:text-neutral-300 leading-relaxed">
          SkillTree reimagines the ancient technique of the memory palace for the digital age. 
          Just as scholars once organized knowledge in imagined architectural spaces, we provide 
          a visual, interactive tree structure where you can build, organize, and retain knowledge 
          across all domains of learning.
        </p>
        <p className="text-neutral-700 dark:text-neutral-300 leading-relaxed">
          Whether you're homeschooling, supplementing traditional education, or pursuing lifelong 
          learning, SkillTree creates a personalized pathway through human knowledge—making learning 
          feel like an adventure rather than a chore.
        </p>
      </section>

      {/* Learning Theory Section */}
      <section className="space-y-6">
        <div className="flex items-center gap-3 mb-4">
          <BeakerIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
          <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">
            Built on Proven Learning Science
          </h2>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-neutral-800 rounded-xl p-6 border border-neutral-200 dark:border-neutral-700">
            <div className="flex items-center gap-2 mb-3">
              <LightBulbIcon className="h-6 w-6 text-gold-500" />
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">
                Constructivist Learning
              </h3>
            </div>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              You build knowledge actively through engagement, not passive reception. 
              Pre-quizzes activate prior knowledge, while interactive modules and immediate 
              feedback reinforce understanding.
            </p>
          </div>

          <div className="bg-white dark:bg-neutral-800 rounded-xl p-6 border border-neutral-200 dark:border-neutral-700">
            <div className="flex items-center gap-2 mb-3">
              <ChartBarIcon className="h-6 w-6 text-gold-500" />
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">
                Mastery-Based Progression
              </h3>
            </div>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Following Bloom's Mastery Learning model, we ensure complete understanding 
              before advancement. Learn at your own pace with multiple attempts to achieve 
              100% comprehension.
            </p>
          </div>

          <div className="bg-white dark:bg-neutral-800 rounded-xl p-6 border border-neutral-200 dark:border-neutral-700">
            <div className="flex items-center gap-2 mb-3">
              <BookOpenIcon className="h-6 w-6 text-gold-500" />
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">
                Cognitive Load Optimization
              </h3>
            </div>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Content is chunked into digestible 10-30 minute modules with progressive 
              difficulty. Multimedia integration supports dual-channel processing for 
              enhanced retention.
            </p>
          </div>

          <div className="bg-white dark:bg-neutral-800 rounded-xl p-6 border border-neutral-200 dark:border-neutral-700">
            <div className="flex items-center gap-2 mb-3">
              <SparklesIcon className="h-6 w-6 text-gold-500" />
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">
                Zone of Proximal Development
              </h3>
            </div>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Our recommendation engine finds the sweet spot between what you know and 
              what you're ready to learn, keeping you challenged but not overwhelmed.
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="space-y-6">
        <div className="flex items-center gap-3 mb-4">
          <AcademicCapIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
          <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">
            Intelligent Learning Features
          </h2>
        </div>

        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-2 bg-primary-500 rounded-full"></div>
            <div>
              <h3 className="font-semibold text-neutral-900 dark:text-white mb-1">
                Adaptive Assessment System
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Dynamic testing that adjusts to your level, providing accurate competency 
                ratings across multiple dimensions including accuracy, consistency, and speed.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-2 bg-primary-500 rounded-full"></div>
            <div>
              <h3 className="font-semibold text-neutral-900 dark:text-white mb-1">
                Spaced Repetition
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Reviews are scheduled based on the forgetting curve, ensuring knowledge 
                moves from short-term to long-term memory efficiently.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-2 bg-primary-500 rounded-full"></div>
            <div>
              <h3 className="font-semibold text-neutral-900 dark:text-white mb-1">
                Personalized Learning Paths
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                AI-driven recommendations based on your interests, current knowledge level, 
                and learning goals create a unique journey through the skill tree.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-2 bg-primary-500 rounded-full"></div>
            <div>
              <h3 className="font-semibold text-neutral-900 dark:text-white mb-1">
                Gamified Progress Tracking
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Visual progress indicators, achievement badges, and skill ratings make 
                learning feel like leveling up in a game you can't put down.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Work in Progress Section */}
      <section className="bg-yellow-50 dark:bg-yellow-900/20 rounded-xl p-8 border border-yellow-200 dark:border-yellow-800">
        <div className="flex items-start gap-4">
          <UserGroupIcon className="h-8 w-8 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-1" />
          <div className="space-y-3">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">
              Growing Together
            </h2>
            <p className="text-neutral-700 dark:text-neutral-300">
              SkillTree is a work in progress, constantly evolving based on user feedback 
              and the latest educational research. We're building this platform with and for 
              our community of learners.
            </p>
            <p className="text-neutral-700 dark:text-neutral-300">
              Your input shapes our development. If you'd like to see specific content added, 
              features implemented, or have suggestions for improvement, we want to hear from you!
            </p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="text-center space-y-6">
        <div className="flex items-center justify-center gap-3 mb-4">
          <EnvelopeIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
          <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">
            Get in Touch
          </h2>
        </div>
        
        <p className="text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
          We value your feedback and suggestions. Whether you're an educator with content 
          recommendations, a parent with feature requests, or a learner with ideas for 
          improvement, we'd love to hear from you.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/feedback"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <EnvelopeIcon className="h-5 w-5" />
            Send Feedback
          </Link>
          <a
            href="https://github.com/anthropics/skilltree/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
          >
            Report an Issue
          </a>
        </div>
      </section>

      {/* Footer Note */}
      <footer className="text-center py-8 border-t border-neutral-200 dark:border-neutral-700">
        <p className="text-sm text-neutral-500 dark:text-neutral-400 flex items-center justify-center gap-1">
          Built with <HeartIcon className="h-4 w-4 text-red-500" /> for lifelong learners everywhere
        </p>
      </footer>
    </div>
  )
}

export default AboutPage