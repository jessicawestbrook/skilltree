import React, { useState } from 'react'
import { 
  AcademicCapIcon, 
  DocumentTextIcon,
  ClockIcon,
  ChartBarIcon,
  ArrowRightIcon,
  BookOpenIcon
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

const StandardizedTestsPage: React.FC = () => {
  const [selectedTest, setSelectedTest] = useState<string | null>(null)

  const tests: TestInfo[] = [
    {
      id: 'sat',
      name: 'SAT',
      fullName: 'Scholastic Assessment Test',
      description: 'College admission test measuring mathematical, reading, and writing skills',
      sections: ['Reading', 'Writing and Language', 'Math (No Calculator)', 'Math (Calculator)', 'Essay (Optional)'],
      duration: '3 hours (3 hours 50 minutes with Essay)',
      scoreRange: '400-1600',
      available: true,
      icon: <AcademicCapIcon className="h-8 w-8" />
    },
    {
      id: 'act',
      name: 'ACT',
      fullName: 'American College Testing',
      description: 'College readiness assessment covering English, mathematics, reading, and science',
      sections: ['English', 'Mathematics', 'Reading', 'Science', 'Writing (Optional)'],
      duration: '2 hours 55 minutes (3 hours 35 minutes with Writing)',
      scoreRange: '1-36',
      available: true,
      icon: <DocumentTextIcon className="h-8 w-8" />
    },
    {
      id: 'lsat',
      name: 'LSAT',
      fullName: 'Law School Admission Test',
      description: 'Standardized test for law school admissions assessing reading and reasoning skills',
      sections: ['Logical Reasoning', 'Analytical Reasoning', 'Reading Comprehension', 'Writing Sample'],
      duration: '3 hours 30 minutes',
      scoreRange: '120-180',
      available: true,
      icon: <BookOpenIcon className="h-8 w-8" />
    },
    {
      id: 'gre',
      name: 'GRE',
      fullName: 'Graduate Record Examination',
      description: 'Graduate school admission test measuring verbal, quantitative, and analytical skills',
      sections: ['Analytical Writing', 'Verbal Reasoning', 'Quantitative Reasoning'],
      duration: '3 hours 45 minutes',
      scoreRange: '260-340 (Verbal + Quantitative)',
      available: false,
      icon: <ChartBarIcon className="h-8 w-8" />
    },
    {
      id: 'gmat',
      name: 'GMAT',
      fullName: 'Graduate Management Admission Test',
      description: 'Business school admission test assessing analytical, writing, quantitative, and verbal skills',
      sections: ['Analytical Writing', 'Integrated Reasoning', 'Quantitative', 'Verbal'],
      duration: '3 hours 7 minutes',
      scoreRange: '200-800',
      available: false,
      icon: <ChartBarIcon className="h-8 w-8" />
    },
    {
      id: 'mcat',
      name: 'MCAT',
      fullName: 'Medical College Admission Test',
      description: 'Medical school admission test covering physical sciences, biological sciences, and critical analysis',
      sections: ['Chemical and Physical Foundations', 'Critical Analysis and Reasoning', 'Biological and Biochemical Foundations', 'Psychological, Social, and Biological Foundations'],
      duration: '7 hours 30 minutes',
      scoreRange: '472-528',
      available: false,
      icon: <AcademicCapIcon className="h-8 w-8" />
    }
  ]

  const handleStartTest = (testId: string) => {
    // This would navigate to the specific test page
    // For now, we'll just set the selected test
    setSelectedTest(testId)
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">
          <span className="bg-gradient-to-r from-primary-600 to-gold-500 bg-clip-text text-transparent">
            Standardized Tests
          </span>
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-3xl mx-auto">
          Practice for major standardized tests with actual past exam questions. 
          Track your progress and identify areas for improvement.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tests.map((test) => (
          <div 
            key={test.id}
            className={`bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-6 ${
              !test.available ? 'opacity-60' : 'hover:shadow-xl transition-shadow'
            }`}
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`${test.available ? 'text-primary-600' : 'text-neutral-400'}`}>
                {test.icon}
              </div>
              {!test.available && (
                <span className="text-xs px-2 py-1 bg-neutral-200 dark:bg-neutral-700 rounded-full">
                  Coming Soon
                </span>
              )}
            </div>

            <h2 className="text-2xl font-bold mb-1">{test.name}</h2>
            <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-3">
              {test.fullName}
            </p>
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-4">
              {test.description}
            </p>

            <div className="space-y-2 mb-4">
              <div className="flex items-center gap-2 text-xs text-neutral-600 dark:text-neutral-400">
                <ClockIcon className="h-4 w-4" />
                <span>{test.duration}</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-neutral-600 dark:text-neutral-400">
                <ChartBarIcon className="h-4 w-4" />
                <span>Score Range: {test.scoreRange}</span>
              </div>
            </div>

            <div className="mb-4">
              <p className="text-xs font-semibold text-neutral-700 dark:text-neutral-300 mb-2">
                Test Sections:
              </p>
              <ul className="text-xs text-neutral-600 dark:text-neutral-400 space-y-1">
                {test.sections.slice(0, 3).map((section, idx) => (
                  <li key={idx} className="flex items-start gap-1">
                    <span className="text-primary-600 dark:text-primary-400 mt-0.5">•</span>
                    <span>{section}</span>
                  </li>
                ))}
                {test.sections.length > 3 && (
                  <li className="text-neutral-500 dark:text-neutral-500 italic">
                    +{test.sections.length - 3} more sections
                  </li>
                )}
              </ul>
            </div>

            {test.available ? (
              <button
                onClick={() => handleStartTest(test.id)}
                className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
              >
                <span>Start Practice</span>
                <ArrowRightIcon className="h-4 w-4" />
              </button>
            ) : (
              <button
                disabled
                className="w-full py-2 bg-neutral-200 dark:bg-neutral-700 text-neutral-500 dark:text-neutral-400 rounded-lg cursor-not-allowed"
              >
                Coming Soon
              </button>
            )}
          </div>
        ))}
      </div>

      {selectedTest && (
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
            Test Selected: {tests.find(t => t.id === selectedTest)?.name}
          </h3>
          <p className="text-sm text-blue-800 dark:text-blue-400">
            Full test functionality will be implemented soon. Tests will include:
          </p>
          <ul className="mt-2 space-y-1 text-sm text-blue-700 dark:text-blue-400">
            <li>• Actual past exam questions</li>
            <li>• Timed practice sessions</li>
            <li>• Score calculation based on official scoring</li>
            <li>• Detailed performance analytics</li>
            <li>• Study recommendations based on weak areas</li>
          </ul>
        </div>
      )}

      <div className="bg-neutral-100 dark:bg-neutral-800 rounded-lg p-6">
        <h3 className="font-semibold mb-3">Tips for Test Preparation:</h3>
        <div className="grid md:grid-cols-2 gap-4 text-sm text-neutral-600 dark:text-neutral-400">
          <div>
            <h4 className="font-medium text-neutral-700 dark:text-neutral-300 mb-2">Before Practice:</h4>
            <ul className="space-y-1">
              <li>• Review test format and timing</li>
              <li>• Set up a quiet environment</li>
              <li>• Have scratch paper ready</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-neutral-700 dark:text-neutral-300 mb-2">During Practice:</h4>
            <ul className="space-y-1">
              <li>• Simulate real test conditions</li>
              <li>• Track your time carefully</li>
              <li>• Review all incorrect answers</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StandardizedTestsPage