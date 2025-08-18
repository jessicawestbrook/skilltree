import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  BriefcaseIcon,
  ChartBarIcon,
  AcademicCapIcon,
  CurrencyDollarIcon,
  LightBulbIcon,
  ArrowTrendingUpIcon,
  UserGroupIcon,
  ComputerDesktopIcon,
  BeakerIcon,
  BuildingOfficeIcon,
  HeartIcon,
  GlobeAltIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'

interface CareerPath {
  id: string
  title: string
  category: string
  description: string
  averageSalary: string
  growthRate: string
  requiredSkills: string[]
  icon: React.ReactNode
  color: string
  treeNodeId?: string
}

const CareerAdvancementPage: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  const careerPaths: CareerPath[] = [
    {
      id: 'software-engineer',
      title: 'Software Engineer',
      category: 'technology',
      description: 'Design, develop, and maintain software applications and systems',
      averageSalary: '$110,000',
      growthRate: '22%',
      requiredSkills: ['Programming', 'Data Structures', 'Algorithms', 'System Design'],
      icon: <ComputerDesktopIcon className="h-6 w-6" />,
      color: 'blue',
      treeNodeId: 'computer-science'
    },
    {
      id: 'data-scientist',
      title: 'Data Scientist',
      category: 'technology',
      description: 'Analyze complex data to help companies make better decisions',
      averageSalary: '$120,000',
      growthRate: '36%',
      requiredSkills: ['Statistics', 'Machine Learning', 'Python', 'Data Visualization'],
      icon: <ChartBarIcon className="h-6 w-6" />,
      color: 'purple',
      treeNodeId: 'data-science'
    },
    {
      id: 'medical-doctor',
      title: 'Medical Doctor',
      category: 'healthcare',
      description: 'Diagnose and treat illnesses, injuries, and health conditions',
      averageSalary: '$208,000',
      growthRate: '3%',
      requiredSkills: ['Biology', 'Chemistry', 'Anatomy', 'Clinical Skills'],
      icon: <HeartIcon className="h-6 w-6" />,
      color: 'red',
      treeNodeId: 'medicine'
    },
    {
      id: 'nurse',
      title: 'Registered Nurse',
      category: 'healthcare',
      description: 'Provide and coordinate patient care, educate patients about health',
      averageSalary: '$77,000',
      growthRate: '6%',
      requiredSkills: ['Patient Care', 'Medical Knowledge', 'Communication', 'Critical Thinking'],
      icon: <HeartIcon className="h-6 w-6" />,
      color: 'pink',
      treeNodeId: 'nursing'
    },
    {
      id: 'financial-analyst',
      title: 'Financial Analyst',
      category: 'business',
      description: 'Evaluate investment opportunities and provide financial guidance',
      averageSalary: '$87,000',
      growthRate: '9%',
      requiredSkills: ['Financial Analysis', 'Excel', 'Accounting', 'Market Research'],
      icon: <CurrencyDollarIcon className="h-6 w-6" />,
      color: 'green',
      treeNodeId: 'finance'
    },
    {
      id: 'marketing-manager',
      title: 'Marketing Manager',
      category: 'business',
      description: 'Plan and execute marketing strategies to promote products and services',
      averageSalary: '$135,000',
      growthRate: '10%',
      requiredSkills: ['Marketing Strategy', 'Digital Marketing', 'Analytics', 'Communication'],
      icon: <BuildingOfficeIcon className="h-6 w-6" />,
      color: 'orange',
      treeNodeId: 'marketing'
    },
    {
      id: 'teacher',
      title: 'Teacher',
      category: 'education',
      description: 'Educate students and help them develop academic and social skills',
      averageSalary: '$61,000',
      growthRate: '4%',
      requiredSkills: ['Subject Expertise', 'Classroom Management', 'Curriculum Development', 'Communication'],
      icon: <AcademicCapIcon className="h-6 w-6" />,
      color: 'indigo',
      treeNodeId: 'education'
    },
    {
      id: 'research-scientist',
      title: 'Research Scientist',
      category: 'science',
      description: 'Conduct experiments and research to advance scientific knowledge',
      averageSalary: '$95,000',
      growthRate: '8%',
      requiredSkills: ['Scientific Method', 'Laboratory Skills', 'Data Analysis', 'Technical Writing'],
      icon: <BeakerIcon className="h-6 w-6" />,
      color: 'teal',
      treeNodeId: 'science'
    },
    {
      id: 'entrepreneur',
      title: 'Entrepreneur',
      category: 'business',
      description: 'Start and manage your own business ventures',
      averageSalary: 'Variable',
      growthRate: 'N/A',
      requiredSkills: ['Business Strategy', 'Leadership', 'Financial Management', 'Innovation'],
      icon: <LightBulbIcon className="h-6 w-6" />,
      color: 'yellow',
      treeNodeId: 'entrepreneurship'
    },
    {
      id: 'international-relations',
      title: 'International Relations Specialist',
      category: 'government',
      description: 'Analyze political and economic developments between nations',
      averageSalary: '$92,000',
      growthRate: '5%',
      requiredSkills: ['Foreign Languages', 'Political Science', 'Economics', 'Cultural Awareness'],
      icon: <GlobeAltIcon className="h-6 w-6" />,
      color: 'gray',
      treeNodeId: 'international-relations'
    }
  ]

  const categories = [
    { id: 'all', label: 'All Careers', icon: <BriefcaseIcon className="h-5 w-5" /> },
    { id: 'technology', label: 'Technology', icon: <ComputerDesktopIcon className="h-5 w-5" /> },
    { id: 'healthcare', label: 'Healthcare', icon: <HeartIcon className="h-5 w-5" /> },
    { id: 'business', label: 'Business', icon: <BuildingOfficeIcon className="h-5 w-5" /> },
    { id: 'education', label: 'Education', icon: <AcademicCapIcon className="h-5 w-5" /> },
    { id: 'science', label: 'Science', icon: <BeakerIcon className="h-5 w-5" /> },
    { id: 'government', label: 'Government', icon: <GlobeAltIcon className="h-5 w-5" /> }
  ]

  const filteredCareers = selectedCategory === 'all' 
    ? careerPaths 
    : careerPaths.filter(career => career.category === selectedCategory)

  const getColorClasses = (color: string) => {
    const colors: Record<string, string> = {
      blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
      purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
      red: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400',
      pink: 'bg-pink-100 dark:bg-pink-900/30 text-pink-700 dark:text-pink-400',
      green: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
      orange: 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400',
      indigo: 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400',
      teal: 'bg-teal-100 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400',
      yellow: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400',
      gray: 'bg-gray-100 dark:bg-gray-900/30 text-gray-700 dark:text-gray-400'
    }
    return colors[color] || colors.blue
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">
          <span className="bg-gradient-to-r from-primary-600 to-gold-500 bg-clip-text text-transparent">
            Career Advancement
          </span>
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-3xl mx-auto">
          Explore career paths and learn the skills needed to achieve your professional goals.
          Each path links to relevant learning modules in our skill tree.
        </p>
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2 justify-center">
        {categories.map(category => (
          <button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2 ${
              selectedCategory === category.id
                ? 'bg-primary-600 text-white'
                : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700'
            }`}
          >
            {category.icon}
            <span>{category.label}</span>
          </button>
        ))}
      </div>

      {/* Career Cards */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCareers.map(career => (
          <div 
            key={career.id}
            className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`p-3 rounded-lg ${getColorClasses(career.color)}`}>
                {career.icon}
              </div>
              <div className="flex items-center gap-1 text-xs text-green-600 dark:text-green-400">
                <ArrowTrendingUpIcon className="h-4 w-4" />
                <span>{career.growthRate}</span>
              </div>
            </div>

            <h3 className="text-xl font-bold mb-2">{career.title}</h3>
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-4">
              {career.description}
            </p>

            <div className="space-y-2 mb-4">
              <div className="flex items-center gap-2 text-sm">
                <CurrencyDollarIcon className="h-4 w-4 text-neutral-500" />
                <span className="font-medium">Avg. Salary:</span>
                <span className="text-neutral-600 dark:text-neutral-400">{career.averageSalary}</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <UserGroupIcon className="h-4 w-4 text-neutral-500" />
                <span className="font-medium">Growth Rate:</span>
                <span className="text-neutral-600 dark:text-neutral-400">{career.growthRate}</span>
              </div>
            </div>

            <div className="mb-4">
              <p className="text-xs font-semibold text-neutral-700 dark:text-neutral-300 mb-2">
                Key Skills Required:
              </p>
              <div className="flex flex-wrap gap-1">
                {career.requiredSkills.map((skill, idx) => (
                  <span 
                    key={idx}
                    className="text-xs px-2 py-1 bg-neutral-100 dark:bg-neutral-800 rounded-full"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {career.treeNodeId && (
              <Link
                to={`/skill-tree?focus=${career.treeNodeId}`}
                className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
              >
                <span>Learn Required Skills</span>
                <ArrowRightIcon className="h-4 w-4" />
              </Link>
            )}
          </div>
        ))}
      </div>

      {/* Career Planning Tips */}
      <div className="bg-gradient-to-r from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 rounded-xl p-8">
        <h2 className="text-2xl font-bold mb-4">Career Planning Tips</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <LightBulbIcon className="h-5 w-5 text-primary-600" />
              Getting Started
            </h3>
            <ul className="text-sm text-neutral-600 dark:text-neutral-400 space-y-1">
              <li>• Identify your interests and strengths</li>
              <li>• Research career requirements and growth</li>
              <li>• Set short-term and long-term goals</li>
              <li>• Create a learning roadmap</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <ChartBarIcon className="h-5 w-5 text-primary-600" />
              Skill Development
            </h3>
            <ul className="text-sm text-neutral-600 dark:text-neutral-400 space-y-1">
              <li>• Focus on both technical and soft skills</li>
              <li>• Practice through real-world projects</li>
              <li>• Seek mentorship and networking</li>
              <li>• Stay updated with industry trends</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CareerAdvancementPage