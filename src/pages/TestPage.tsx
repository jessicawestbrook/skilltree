import React from 'react'
import { useParams, Navigate } from 'react-router-dom'
import { 
  AcademicCapIcon, 
  DocumentTextIcon,
  ClockIcon,
  ChartBarIcon,
  ArrowRightIcon,
  BookOpenIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

interface TestInfo {
  id: string
  name: string
  fullName: string
  description: string
  sections: string[]
  duration: string
  scoreRange: string
  available: boolean
  icon: React.ReactNode
}

const TestPage: React.FC = () => {
  const { testId } = useParams<{ testId: string }>()

  const tests: Record<string, TestInfo> = {
    sat: {
      id: 'sat',
      name: 'SAT',
      fullName: 'Scholastic Assessment Test',
      description: 'College admission test measuring mathematical, reading, and writing skills',
      sections: ['Reading', 'Writing and Language', 'Math (No Calculator)', 'Math (Calculator)', 'Essay (Optional)'],
      duration: '3 hours (3 hours 50 minutes with Essay)',
      scoreRange: '400-1600',
      available: true,
      icon: <AcademicCapIcon className="h-12 w-12" />
    },
    act: {
      id: 'act',
      name: 'ACT',
      fullName: 'American College Testing',
      description: 'College readiness assessment covering English, mathematics, reading, and science',
      sections: ['English', 'Mathematics', 'Reading', 'Science', 'Writing (Optional)'],
      duration: '2 hours 55 minutes (3 hours 35 minutes with Writing)',
      scoreRange: '1-36',
      available: true,
      icon: <DocumentTextIcon className="h-12 w-12" />
    },
    lsat: {
      id: 'lsat',
      name: 'LSAT',
      fullName: 'Law School Admission Test',
      description: 'Standardized test for law school admissions assessing reading and reasoning skills',
      sections: ['Logical Reasoning', 'Analytical Reasoning', 'Reading Comprehension', 'Writing Sample'],
      duration: '3 hours 30 minutes',
      scoreRange: '120-180',
      available: true,
      icon: <BookOpenIcon className="h-12 w-12" />
    },
    gre: {
      id: 'gre',
      name: 'GRE',
      fullName: 'Graduate Record Examination',
      description: 'Graduate school admission test measuring verbal, quantitative, and analytical skills',
      sections: ['Analytical Writing', 'Verbal Reasoning', 'Quantitative Reasoning'],
      duration: '3 hours 45 minutes',
      scoreRange: '260-340 (Verbal + Quantitative)',
      available: false,
      icon: <ChartBarIcon className="h-12 w-12" />
    },
    gmat: {
      id: 'gmat',
      name: 'GMAT',
      fullName: 'Graduate Management Admission Test',
      description: 'Business school admission test assessing analytical, writing, quantitative, and verbal skills',
      sections: ['Analytical Writing', 'Integrated Reasoning', 'Quantitative', 'Verbal'],
      duration: '3 hours 7 minutes',
      scoreRange: '200-800',
      available: false,
      icon: <ChartBarIcon className="h-12 w-12" />
    },
    mcat: {
      id: 'mcat',
      name: 'MCAT',
      fullName: 'Medical College Admission Test',
      description: 'Medical school admission test covering physical sciences, biological sciences, and critical analysis',
      sections: ['Chemical and Physical Foundations', 'Critical Analysis and Reasoning', 'Biological and Biochemical Foundations', 'Psychological, Social, and Biological Foundations'],
      duration: '7 hours 30 minutes',
      scoreRange: '472-528',
      available: false,
      icon: <AcademicCapIcon className="h-12 w-12" />
    }
  }

  if (!testId || !tests[testId]) {
    return <Navigate to="/standardized-tests" replace />
  }

  const test = tests[testId]

  const handleStartTest = () => {
    // This would navigate to the actual test interface
    console.log(`Starting ${test.name} test...`)
    // For now, just show an alert
    alert(`${test.name} test functionality will be implemented soon!`)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center mb-6">
          <div className={`${test.available ? 'text-primary-600' : 'text-neutral-400'}`}>
            {test.icon}
          </div>
        </div>
        <h1 className="text-4xl font-bold mb-2 text-primary-600 dark:text-primary-400">
          {test.name}
        </h1>
        <p className="text-xl text-neutral-600 dark:text-neutral-400 mb-2">
          {test.fullName}
        </p>
        <p className="text-lg text-neutral-500 dark:text-neutral-400 max-w-2xl mx-auto">
          {test.description}
        </p>
      </div>

      {/* Test Information */}
      <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-semibold mb-6">Test Information</h2>
        
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <ClockIcon className="h-5 w-5 text-primary-600" />
              <div>
                <p className="font-medium text-neutral-700 dark:text-neutral-300">Duration</p>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">{test.duration}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <ChartBarIcon className="h-5 w-5 text-primary-600" />
              <div>
                <p className="font-medium text-neutral-700 dark:text-neutral-300">Score Range</p>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">{test.scoreRange}</p>
              </div>
            </div>
          </div>
          
          <div>
            <p className="font-medium text-neutral-700 dark:text-neutral-300 mb-3">Test Sections</p>
            <ul className="space-y-2">
              {test.sections.map((section, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm text-neutral-600 dark:text-neutral-400">
                  <span className="text-primary-600 dark:text-primary-400 mt-1">•</span>
                  <span>{section}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Action Button */}
        <div className="text-center">
          {test.available ? (
            <button
              onClick={handleStartTest}
              className="inline-flex items-center gap-3 px-8 py-4 bg-primary-600 text-white text-lg font-medium rounded-lg hover:bg-primary-700 transition-colors"
            >
              <span>Start Practice Test</span>
              <ArrowRightIcon className="h-5 w-5" />
            </button>
          ) : (
            <div className="inline-flex items-center gap-3 px-8 py-4 bg-neutral-200 dark:bg-neutral-700 text-neutral-500 dark:text-neutral-400 text-lg font-medium rounded-lg">
              <ExclamationTriangleIcon className="h-5 w-5" />
              <span>Coming Soon</span>
            </div>
          )}
        </div>
      </div>

      {/* Study Tips */}
      <div className="bg-neutral-100 dark:bg-neutral-800 rounded-xl p-8">
        <h3 className="text-xl font-semibold mb-6">Test Preparation Tips</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-neutral-700 dark:text-neutral-300 mb-3">Before Taking the Test:</h4>
            <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
              <li>• Familiarize yourself with the test format and timing</li>
              <li>• Create a quiet, distraction-free environment</li>
              <li>• Have scratch paper and writing materials ready</li>
              <li>• Ensure you have a stable internet connection</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-neutral-700 dark:text-neutral-300 mb-3">During the Test:</h4>
            <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
              <li>• Read all instructions carefully before starting</li>
              <li>• Manage your time effectively across sections</li>
              <li>• Don't spend too much time on difficult questions</li>
              <li>• Review your answers if time permits</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Practice Features */}
      {test.available && (
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-8">
          <h3 className="text-xl font-semibold text-blue-900 dark:text-blue-300 mb-4">
            What's Included in Practice Tests
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-400">
              <li>• Actual past exam questions</li>
              <li>• Realistic timing and pacing</li>
              <li>• Official scoring methodology</li>
            </ul>
            <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-400">
              <li>• Detailed performance analytics</li>
              <li>• Section-by-section breakdown</li>
              <li>• Personalized study recommendations</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}

export default TestPage