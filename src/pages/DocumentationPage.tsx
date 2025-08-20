import React, { useState } from 'react'
import { 
  AcademicCapIcon,
  BookOpenIcon,
  ChartBarIcon,
  BeakerIcon,
  LightBulbIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline'

interface Section {
  id: string
  title: string
  icon: React.ReactNode
  content: React.ReactNode
}

const DocumentationPage: React.FC = () => {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['executive-summary']))

  const toggleSection = (sectionId: string) => {
    const newExpanded = new Set(expandedSections)
    if (newExpanded.has(sectionId)) {
      newExpanded.delete(sectionId)
    } else {
      newExpanded.add(sectionId)
    }
    setExpandedSections(newExpanded)
  }

  const sections: Section[] = [
    {
      id: 'executive-summary',
      title: 'Executive Summary',
      icon: <DocumentTextIcon className="h-5 w-5" />,
      content: (
        <div className="prose dark:prose-invert max-w-none">
          <p>
            The SkillTree platform is built on established educational theories, cognitive science research, 
            and modern adaptive learning methodologies. This documentation outlines the theoretical foundations 
            that guide our implementation of educationally sound features.
          </p>
          <p>
            Our approach combines constructivist learning principles, cognitive load theory, and mastery-based 
            progression to create an engaging and effective learning experience that adapts to each user's needs.
          </p>
        </div>
      )
    },
    {
      id: 'learning-theory',
      title: 'Learning Theory Framework',
      icon: <AcademicCapIcon className="h-5 w-5" />,
      content: (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Constructivist Approach
            </h3>
            <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-3">
              Learners build knowledge through active engagement rather than passive reception (Ausubel, 1968).
            </p>
            <ul className="list-disc list-inside space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
              <li><strong>Pre-quiz assessments</strong> activate prior knowledge before learning</li>
              <li><strong>Interactive modules</strong> require active participation and engagement</li>
              <li><strong>Immediate feedback</strong> reinforces learning and corrects misconceptions</li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Cognitive Load Theory
            </h3>
            <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-3">
              Based on Sweller's research (1988), we optimize learning by managing cognitive load:
            </p>
            <ul className="list-disc list-inside space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
              <li><strong>Content chunking</strong> into 10-30 minute digestible modules</li>
              <li><strong>Progressive difficulty</strong> to avoid overwhelming learners</li>
              <li><strong>Multimedia integration</strong> supports dual-channel processing (Mayer, 2009)</li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Mastery Learning
            </h3>
            <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-3">
              Following Bloom's Mastery Learning model (1968):
            </p>
            <ul className="list-disc list-inside space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
              <li><strong>100% accuracy requirement</strong> ensures complete understanding</li>
              <li><strong>Multiple attempts</strong> allow self-paced mastery achievement</li>
              <li><strong>Prerequisite tracking</strong> ensures foundational knowledge</li>
            </ul>
          </div>
        </div>
      )
    },
    {
      id: 'competency-rating',
      title: 'User Competency Rating System',
      icon: <ChartBarIcon className="h-5 w-5" />,
      content: (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Multi-Dimensional Rating Model
            </h3>
            <div className="bg-neutral-100 dark:bg-neutral-800 rounded-lg p-4 mb-4">
              <code className="text-sm">
                Overall Rating = (0.4 × Accuracy) + (0.3 × Consistency) + (0.2 × Difficulty) + (0.1 × Speed)
              </code>
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex items-start gap-2">
                <span className="font-semibold text-primary-600 dark:text-primary-400">Accuracy:</span>
                <span className="text-neutral-600 dark:text-neutral-400">Percentage of correct answers (0-100)</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="font-semibold text-primary-600 dark:text-primary-400">Consistency:</span>
                <span className="text-neutral-600 dark:text-neutral-400">Standard deviation across attempts</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="font-semibold text-primary-600 dark:text-primary-400">Difficulty:</span>
                <span className="text-neutral-600 dark:text-neutral-400">Weighted average of question levels</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="font-semibold text-primary-600 dark:text-primary-400">Speed:</span>
                <span className="text-neutral-600 dark:text-neutral-400">Time efficiency vs. estimated time</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Rating Levels
            </h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-neutral-200 dark:divide-neutral-700">
                <thead className="bg-neutral-50 dark:bg-neutral-800">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Range</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Level</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase">Description</th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-neutral-900 divide-y divide-neutral-200 dark:divide-neutral-700">
                  <tr>
                    <td className="px-4 py-2 text-sm">90-100</td>
                    <td className="px-4 py-2 text-sm font-medium text-green-600 dark:text-green-400">Expert</td>
                    <td className="px-4 py-2 text-sm text-neutral-600 dark:text-neutral-400">Can teach others, creates connections</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 text-sm">80-89</td>
                    <td className="px-4 py-2 text-sm font-medium text-blue-600 dark:text-blue-400">Proficient</td>
                    <td className="px-4 py-2 text-sm text-neutral-600 dark:text-neutral-400">Applies knowledge in various contexts</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 text-sm">70-79</td>
                    <td className="px-4 py-2 text-sm font-medium text-yellow-600 dark:text-yellow-400">Competent</td>
                    <td className="px-4 py-2 text-sm text-neutral-600 dark:text-neutral-400">Understands and applies in familiar contexts</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 text-sm">60-69</td>
                    <td className="px-4 py-2 text-sm font-medium text-orange-600 dark:text-orange-400">Developing</td>
                    <td className="px-4 py-2 text-sm text-neutral-600 dark:text-neutral-400">Basic understanding with some gaps</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 text-sm">0-59</td>
                    <td className="px-4 py-2 text-sm font-medium text-red-600 dark:text-red-400">Novice</td>
                    <td className="px-4 py-2 text-sm text-neutral-600 dark:text-neutral-400">Beginning to understand fundamentals</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Dynamic Rating Adjustment
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
              <li><strong>Recency weighting:</strong> Recent performance weighted more heavily (0.9 decay factor)</li>
              <li><strong>Confidence intervals:</strong> Ratings become more reliable with more data</li>
              <li><strong>Forgetting curve:</strong> Ratings decay without practice (Ebbinghaus, 1885)</li>
            </ol>
          </div>
        </div>
      )
    },
    {
      id: 'assessment-theory',
      title: 'Assessment and Testing Theory',
      icon: <BeakerIcon className="h-5 w-5" />,
      content: (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Pre-Quiz Design (Diagnostic Assessment)
            </h3>
            <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-3">
              <strong>Purpose:</strong> Activate prior knowledge and assess readiness
            </p>
            <ul className="list-disc list-inside space-y-1 text-sm text-neutral-600 dark:text-neutral-400">
              <li>3 questions covering key prerequisites</li>
              <li>No penalty for incorrect answers</li>
              <li>Immediate feedback with explanations</li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Node Test Design (Summative Assessment)
            </h3>
            <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-3">
              <strong>Purpose:</strong> Verify mastery of learning objectives
            </p>
            <ul className="list-disc list-inside space-y-1 text-sm text-neutral-600 dark:text-neutral-400">
              <li>Minimum 5 questions per node (increases with complexity)</li>
              <li>100% accuracy required for mastery badge</li>
              <li>Spaced repetition of previously incorrect answers</li>
            </ul>
            <div className="bg-neutral-100 dark:bg-neutral-800 rounded-lg p-3 mt-3">
              <p className="text-xs font-mono">
                Question Selection Algorithm:<br/>
                1. Prioritize unviewed questions<br/>
                2. Include previously incorrect (spaced repetition)<br/>
                3. Balance difficulty levels
              </p>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Spaced Repetition Algorithm
            </h3>
            <p className="text-sm text-neutral-700 dark:text-neutral-300">
              Based on SuperMemo SM-2 algorithm, optimized for educational content:
            </p>
            <div className="bg-neutral-100 dark:bg-neutral-800 rounded-lg p-3 mt-2">
              <p className="text-xs font-mono">
                Review Intervals:<br/>
                • First review: 1 day<br/>
                • Second: 3 days (if correct)<br/>
                • Third: 7 days<br/>
                • Fourth: 14 days<br/>
                • Fifth: 30 days<br/>
                • Reset on incorrect answer
              </p>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'recommendation-algorithm',
      title: 'Recommendation Algorithm',
      icon: <LightBulbIcon className="h-5 w-5" />,
      content: (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Content Recommendation Logic
            </h3>
            <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-3">
              The recommendation system uses a weighted scoring algorithm:
            </p>
            <div className="bg-neutral-100 dark:bg-neutral-800 rounded-lg p-4">
              <code className="text-sm">
                Score = (0.3 × Prerequisite) + (0.25 × Interest) + (0.2 × Difficulty) + 
                        (0.15 × Recency) + (0.1 × Diversity)
              </code>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Factors Explained
            </h3>
            <div className="space-y-3">
              <div className="border-l-4 border-primary-500 pl-3">
                <p className="font-semibold text-sm">Prerequisite Completion (30%)</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  Ensures foundational knowledge before advancing
                </p>
              </div>
              <div className="border-l-4 border-gold-500 pl-3">
                <p className="font-semibold text-sm">User Interest (25%)</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  Based on starred nodes and completion patterns
                </p>
              </div>
              <div className="border-l-4 border-blue-500 pl-3">
                <p className="font-semibold text-sm">Difficulty Match (20%)</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  Aligns with user's current competency level
                </p>
              </div>
              <div className="border-l-4 border-green-500 pl-3">
                <p className="font-semibold text-sm">Recency (15%)</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  Prioritizes continuation of recent learning paths
                </p>
              </div>
              <div className="border-l-4 border-purple-500 pl-3">
                <p className="font-semibold text-sm">Topic Diversity (10%)</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  Encourages exploration of different subject areas
                </p>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Zone of Proximal Development
            </h3>
            <p className="text-sm text-neutral-700 dark:text-neutral-300">
              Following Vygotsky's theory, we recommend content that is slightly above the learner's 
              current level but achievable with effort. This "sweet spot" maximizes learning efficiency 
              and maintains engagement.
            </p>
          </div>
        </div>
      )
    },
    {
      id: 'gamification',
      title: 'Gamification Principles',
      icon: <BookOpenIcon className="h-5 w-5" />,
      content: (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Motivation Design
            </h3>
            <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-3">
              Based on Self-Determination Theory (Deci & Ryan, 1985):
            </p>
            <div className="grid gap-3">
              <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-3">
                <p className="font-semibold text-sm text-green-700 dark:text-green-400">Autonomy</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  Users choose their learning path and pace
                </p>
              </div>
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                <p className="font-semibold text-sm text-blue-700 dark:text-blue-400">Competence</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  Clear progress indicators and achievable challenges
                </p>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-3">
                <p className="font-semibold text-sm text-purple-700 dark:text-purple-400">Relatedness</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  Connection to real-world applications and community
                </p>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Progress Mechanics
            </h3>
            <ul className="list-disc list-inside space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
              <li><strong>Visual progress:</strong> Color-coded completion indicators</li>
              <li><strong>Skill trees:</strong> Clear advancement paths like video games</li>
              <li><strong>Mastery badges:</strong> Recognition for 100% completion</li>
              <li><strong>Streak tracking:</strong> Encourages consistent practice</li>
              <li><strong>Level progression:</strong> Difficulty increases gradually</li>
            </ul>
          </div>
        </div>
      )
    },
    {
      id: 'references',
      title: 'Scientific References',
      icon: <DocumentTextIcon className="h-5 w-5" />,
      content: (
        <div className="space-y-3">
          <p className="text-sm font-semibold text-neutral-700 dark:text-neutral-300">
            Key Research Supporting Our Approach:
          </p>
          <ul className="space-y-2 text-xs text-neutral-600 dark:text-neutral-400">
            <li>• Ausubel, D. P. (1968). Educational psychology: A cognitive view. Holt, Rinehart & Winston.</li>
            <li>• Bloom, B. S. (1968). Learning for mastery. Evaluation Comment, 1(2), 1-12.</li>
            <li>• Deci, E. L., & Ryan, R. M. (1985). Intrinsic motivation and self-determination in human behavior.</li>
            <li>• Ebbinghaus, H. (1885). Memory: A contribution to experimental psychology.</li>
            <li>• Mayer, R. E. (2009). Multimedia learning (2nd ed.). Cambridge University Press.</li>
            <li>• Sweller, J. (1988). Cognitive load during problem solving. Cognitive Science, 12(2), 257-285.</li>
            <li>• Vygotsky, L. S. (1978). Mind in society: The development of higher psychological processes.</li>
            <li>• Webb, N. L. (1997). Depth-of-knowledge levels for four content areas.</li>
            <li>• Wozniak, P. A. (1990). Optimization of learning (Master's thesis). University of Technology, Poznan.</li>
          </ul>
        </div>
      )
    }
  ]

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4">
          <span className="text-primary-600 dark:text-primary-400">
            Educational Foundations
          </span>
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400">
          The science and theory behind effective learning
        </p>
      </div>

      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 mb-6">
        <div className="flex items-start gap-3">
          <AcademicCapIcon className="h-6 w-6 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-semibold text-blue-900 dark:text-blue-300 mb-1">
              Evidence-Based Design
            </p>
            <p className="text-xs text-blue-700 dark:text-blue-400">
              Every feature in SkillTree is grounded in educational research and cognitive science 
              to maximize learning effectiveness and engagement.
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {sections.map((section) => (
          <div
            key={section.id}
            className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg overflow-hidden"
          >
            <button
              onClick={() => toggleSection(section.id)}
              className="w-full px-6 py-4 flex items-center justify-between hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="text-primary-600 dark:text-primary-400">
                  {section.icon}
                </div>
                <h2 className="text-lg font-semibold text-left">
                  {section.title}
                </h2>
              </div>
              {expandedSections.has(section.id) ? (
                <ChevronDownIcon className="h-5 w-5 text-neutral-400" />
              ) : (
                <ChevronRightIcon className="h-5 w-5 text-neutral-400" />
              )}
            </button>
            
            {expandedSections.has(section.id) && (
              <div className="px-6 pb-6 border-t border-neutral-200 dark:border-neutral-700">
                <div className="pt-4">
                  {section.content}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-8 p-4 bg-neutral-100 dark:bg-neutral-800 rounded-lg">
        <p className="text-xs text-neutral-600 dark:text-neutral-400 text-center">
          This documentation is based on peer-reviewed research and established educational theories. 
          Implementation details may evolve as we gather user data and feedback.
        </p>
      </div>
    </div>
  )
}

export default DocumentationPage