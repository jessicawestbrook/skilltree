'use client';

import React, { useState, useEffect } from 'react';
import { CourseContent as CourseContentType, CourseSection, LearningTip, CourseContentService } from '@/services/courseContentService';
import { ChevronRight, Clock, BookOpen, Lightbulb, AlertCircle, CheckCircle, PlayCircle, FileText, Code } from 'lucide-react';
import { ChatbotContainer } from './ChatbotContainer';

interface CourseContentProps {
  nodeId: string;
  nodeTitle: string;
  onComplete: () => void;
  onStartQuiz: () => void;
}

export default function CourseContent({ nodeId, nodeTitle, onComplete, onStartQuiz }: CourseContentProps) {
  const [content, setContent] = useState<CourseContentType | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentSection, setCurrentSection] = useState(0);
  const [completedSections, setCompletedSections] = useState<Set<number>>(new Set());
  const [showKeyConcepts, setShowKeyConcepts] = useState(false);
  const [showResources, setShowResources] = useState(false);

  useEffect(() => {
    loadContent();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [nodeId]);

  const loadContent = async () => {
    setLoading(true);
    const data = await CourseContentService.getContentForNode(nodeId);
    setContent(data);
    setLoading(false);
  };

  const handleSectionComplete = () => {
    const newCompleted = new Set(completedSections);
    newCompleted.add(currentSection);
    setCompletedSections(newCompleted);

    if (content?.sections && currentSection < content.sections.length - 1) {
      setCurrentSection(currentSection + 1);
    }
  };

  const handleContentComplete = () => {
    onComplete();
    onStartQuiz();
  };

  const getSectionIcon = (type: CourseSection['section_type']) => {
    switch (type) {
      case 'introduction': return <BookOpen className="w-5 h-5" />;
      case 'concept': return <Lightbulb className="w-5 h-5" />;
      case 'example': return <Code className="w-5 h-5" />;
      case 'practice': return <PlayCircle className="w-5 h-5" />;
      case 'summary': return <CheckCircle className="w-5 h-5" />;
      default: return <FileText className="w-5 h-5" />;
    }
  };

  const getTipIcon = (type: LearningTip['tip_type']) => {
    switch (type) {
      case 'warning': return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'best_practice': return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'common_mistake': return <AlertCircle className="w-5 h-5 text-red-500" />;
      default: return <Lightbulb className="w-5 h-5 text-blue-500" />;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading course content...</div>
      </div>
    );
  }

  if (!content) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 text-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">{nodeTitle}</h2>
        <p className="text-gray-700 dark:text-gray-300 font-medium mb-6">Course content is being prepared for this topic.</p>
        <button
          onClick={onStartQuiz}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
        >
          Skip to Quiz
        </button>
      </div>
    );
  }

  const currentSectionData = content.sections?.[currentSection];
  const progress = content.sections ? ((completedSections.size / content.sections.length) * 100) : 0;

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex gap-6">
        {/* Main Content Area */}
        <div className="flex-1 max-w-4xl">
      {/* Header */}
      <div className="relative overflow-hidden rounded-t-lg">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700 dark:from-purple-800 dark:via-blue-800 dark:to-indigo-900"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
        <div className="relative z-10 p-8">
          <h1 className="text-3xl md:text-4xl font-bold mb-3 text-white drop-shadow-lg">{content.title}</h1>
          <p className="text-purple-50 mb-6 text-lg leading-relaxed max-w-3xl">{content.overview}</p>
          <div className="flex flex-wrap items-center gap-4 text-sm">
            <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-full">
              <Clock className="w-4 h-4 text-purple-100" />
              <span className="text-white font-medium">{content.estimated_time} min</span>
            </div>
            <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-full">
              <BookOpen className="w-4 h-4 text-purple-100" />
              <span className="text-white font-medium">{content.sections?.length || 0} sections</span>
            </div>
            <div className="px-3 py-1.5 bg-white/20 backdrop-blur-sm rounded-full">
              <span className="text-white font-medium capitalize">{content.difficulty_level}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Learning Objectives */}
      {content.learning_objectives && content.learning_objectives.length > 0 && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 p-4 mb-6">
          <h3 className="font-bold text-blue-900 dark:text-blue-200 text-lg mb-2">Learning Objectives</h3>
          <ul className="space-y-1">
            {content.learning_objectives.map((objective, index) => (
              <li key={index} className="flex items-start gap-2 text-blue-800 dark:text-blue-300">
                <CheckCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                <span className="text-sm">{objective}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Progress Bar */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 mb-6">
        <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
          <span>Progress</span>
          <span>{Math.round(progress)}% Complete</span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Section Navigation */}
      {content.sections && content.sections.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 mb-6">
          <div className="flex gap-2 overflow-x-auto">
            {content.sections.map((section, index) => (
              <button
                key={section.id}
                onClick={() => setCurrentSection(index)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg whitespace-nowrap transition-colors ${
                  index === currentSection
                    ? 'bg-purple-600 text-white'
                    : completedSections.has(index)
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {getSectionIcon(section.section_type)}
                <span className="text-sm font-semibold">{section.title}</span>
                {completedSections.has(index) && <CheckCircle className="w-4 h-4" />}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Current Section Content */}
      {currentSectionData && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center gap-3 mb-4">
            {getSectionIcon(currentSectionData.section_type)}
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{currentSectionData.title}</h2>
          </div>

          {/* Media Content */}
          {currentSectionData.media_url && (
            <div className="mb-6">
              {currentSectionData.media_type === 'image' && (
                <img 
                  src={currentSectionData.media_url} 
                  alt={currentSectionData.title}
                  className="w-full rounded-lg"
                />
              )}
              {currentSectionData.media_type === 'video' && (
                <video 
                  controls 
                  className="w-full rounded-lg"
                  src={currentSectionData.media_url}
                />
              )}
              {currentSectionData.media_type === 'code' && (
                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                  <code>{currentSectionData.media_url}</code>
                </pre>
              )}
            </div>
          )}

          {/* Text Content */}
          <div className="prose prose-lg max-w-none mb-6">
            {currentSectionData.content.split('\n').map((paragraph, index) => (
              <p key={index} className="mb-4 text-gray-800 dark:text-gray-200 leading-relaxed font-medium">
                {paragraph}
              </p>
            ))}
          </div>

          {/* Section Navigation */}
          <div className="flex justify-between items-center pt-6 border-t">
            <button
              onClick={() => setCurrentSection(Math.max(0, currentSection - 1))}
              disabled={currentSection === 0}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                currentSection === 0
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Previous
            </button>

            {currentSection < (content.sections?.length || 1) - 1 ? (
              <button
                onClick={handleSectionComplete}
                className="flex items-center gap-2 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
              >
                Next Section
                <ChevronRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleContentComplete}
                className="flex items-center gap-2 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Complete & Start Quiz
                <CheckCircle className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      )}

      {/* Key Concepts */}
      {content.key_concepts && content.key_concepts.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <button
            onClick={() => setShowKeyConcepts(!showKeyConcepts)}
            className="w-full flex items-center justify-between text-left"
          >
            <h3 className="text-xl font-bold flex items-center gap-2 text-gray-900">
              <Lightbulb className="w-5 h-5 text-yellow-500" />
              Key Concepts
            </h3>
            <ChevronRight className={`w-5 h-5 transform transition-transform text-gray-700 ${showKeyConcepts ? 'rotate-90' : ''}`} />
          </button>
          
          {showKeyConcepts && (
            <div className="mt-4 space-y-4">
              {content.key_concepts.map((concept) => (
                <div key={concept.id} className="border-l-4 border-purple-500 pl-4">
                  <h4 className="font-bold text-gray-900 text-lg">{concept.term}</h4>
                  <p className="text-gray-800 mt-1 font-medium">{concept.definition}</p>
                  {concept.example && (
                    <p className="text-sm text-gray-700 mt-2 italic font-medium">
                      Example: {concept.example}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Learning Tips */}
      {content.learning_tips && content.learning_tips.length > 0 && (
        <div className="space-y-3 mb-6">
          {content.learning_tips.map((tip) => (
            <div key={tip.id} className={`flex items-start gap-3 p-4 rounded-lg ${
              tip.tip_type === 'warning' ? 'bg-yellow-50' :
              tip.tip_type === 'best_practice' ? 'bg-green-50' :
              tip.tip_type === 'common_mistake' ? 'bg-red-50' :
              'bg-blue-50'
            }`}>
              {getTipIcon(tip.tip_type)}
              <p className="text-sm text-gray-800 font-medium">{tip.content}</p>
            </div>
          ))}
        </div>
      )}

      {/* Additional Resources */}
      {content.resources && content.resources.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <button
            onClick={() => setShowResources(!showResources)}
            className="w-full flex items-center justify-between text-left"
          >
            <h3 className="text-xl font-bold flex items-center gap-2">
              <FileText className="w-5 h-5 text-blue-500" />
              Additional Resources
            </h3>
            <ChevronRight className={`w-5 h-5 transform transition-transform ${showResources ? 'rotate-90' : ''}`} />
          </button>
          
          {showResources && (
            <div className="mt-4 space-y-3">
              {content.resources.map((resource) => (
                <a
                  key={resource.id}
                  href={resource.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block p-3 border rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900">
                        {resource.title}
                        {resource.is_required && (
                          <span className="ml-2 px-2 py-1 bg-red-100 text-red-700 text-xs rounded">
                            Required
                          </span>
                        )}
                      </h4>
                      {resource.description && (
                        <p className="text-sm text-gray-600 mt-1">{resource.description}</p>
                      )}
                    </div>
                    <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                      {resource.resource_type}
                    </span>
                  </div>
                </a>
              ))}
            </div>
          )}
        </div>
      )}
        </div>
        
        {/* Chatbot Sidebar */}
        <div className="w-80 hidden lg:block">
          <div className="sticky top-6">
            <ChatbotContainer
              nodeId={nodeId}
              nodeTitle={nodeTitle}
              currentContent={currentSectionData?.content}
              isLearningMode={true}
              className="h-full"
            />
          </div>
        </div>
      </div>
    </div>
  );
}