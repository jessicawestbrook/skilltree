import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { ChevronLeftIcon, ChevronRightIcon, BookOpenIcon, AcademicCapIcon } from '@heroicons/react/24/outline';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { supabase } from '../services/supabase';
import { useAuth } from '../contexts/AuthContext';

interface Course {
  id: string;
  name: string;
  description: string;
  level: string;
  estimated_hours: number;
}

interface CourseModule {
  id: string;
  chapter_number: number;
  title: string;
  description: string;
  module_type: string;
  display_order: number;
}

interface ModuleContent {
  id: string;
  section_number: number;
  title: string;
  content_type: string;
  content: any;
  estimated_minutes: number;
}

interface ModuleQuestion {
  id: string;
  question_id: string;
  display_order: number;
  points: number;
  question: {
    question_text: string;
    question_type: string;
    options: string[];
    correct_answer_index: number;
    explanation: string;
  };
}

interface UserModuleProgress {
  module_id: string;
  content_viewed: string[];
  questions_answered: string[];
  questions_correct: number;
  questions_total: number;
  completion_percentage: number;
}

export const CourseViewer: React.FC = () => {
  const { courseSlug } = useParams<{ courseSlug: string }>();
  const { user } = useAuth();
  
  const [course, setCourse] = useState<Course | null>(null);
  const [modules, setModules] = useState<CourseModule[]>([]);
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [currentModule, setCurrentModule] = useState<CourseModule | null>(null);
  const [moduleContent, setModuleContent] = useState<ModuleContent[]>([]);
  const [moduleQuestions, setModuleQuestions] = useState<ModuleQuestion[]>([]);
  const [userProgress, setUserProgress] = useState<UserModuleProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [currentContentIndex, setCurrentContentIndex] = useState(0);
  const [isShowingContent, setIsShowingContent] = useState(true);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [userAnswers, setUserAnswers] = useState<Record<string, number>>({});

  // Load course data
  useEffect(() => {
    loadCourseData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseSlug]);

  // Load module data when current module changes
  useEffect(() => {
    if (currentModule) {
      loadModuleData(currentModule.id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentModule]);

  const loadCourseData = async () => {
    if (!courseSlug) return;
    
    try {
      setLoading(true);
      
      // Load course details - courseSlug is actually the course ID for skill_tree_nodes
      const { data: courseData, error: courseError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('id', courseSlug)
        .single();
        
      if (courseError) throw courseError;
      setCourse(courseData);
      
      // Load course modules using the course's ID
      const { data: modulesData, error: modulesError } = await supabase
        .from('course_modules')
        .select('*')
        .eq('course_id', courseData.id)
        .order('chapter_number');
        
      if (modulesError) throw modulesError;
      setModules(modulesData || []);
      
      if (modulesData && modulesData.length > 0) {
        setCurrentModule(modulesData[0]);
      }
      
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadModuleData = async (moduleId: string) => {
    try {
      // Load module content
      const { data: contentData, error: contentError } = await supabase
        .from('module_content')
        .select('*')
        .eq('module_id', moduleId)
        .order('section_number');
        
      if (contentError) throw contentError;
      setModuleContent(contentData || []);
      
      // Load module questions with full question data
      const { data: questionsData, error: questionsError } = await supabase
        .from('module_questions')
        .select(`
          *,
          question:language_questions(
            question_text,
            question_type,
            options,
            correct_answer_index,
            explanation
          )
        `)
        .eq('module_id', moduleId)
        .order('display_order');
        
      if (questionsError) throw questionsError;
      setModuleQuestions(questionsData || []);
      
      // Load user progress if logged in
      // Note: user_module_progress table is optional - skip if not available
      if (user) {
        try {
          const { data: progressData, error } = await supabase
            .from('user_module_progress')
            .select('*')
            .eq('user_id', user.id)
            .eq('module_id', moduleId)
            .maybeSingle(); // Use maybeSingle() instead of single() to handle no records
            
          if (!error && progressData) {
            setUserProgress(progressData);
          } else if (!progressData && !error) {
            // No progress yet - create initial record
            const { data: newProgress } = await supabase
              .from('user_module_progress')
              .insert({
                user_id: user.id,
                module_id: moduleId,
                questions_correct: 0,
                questions_total: 0,
                completion_percentage: 0
              })
              .select()
              .single();
            
            if (newProgress) {
              setUserProgress(newProgress);
            }
          }
        } catch (err) {
          // Table might not exist or RLS policies blocking, which is fine
          console.log('User module progress not available:', err);
        }
      }
      
      // Reset to first content
      setCurrentContentIndex(0);
      setIsShowingContent(true);
      
    } catch (err: any) {
      console.error('Error loading module data:', err);
    }
  };

  const handleNextContent = () => {
    if (isShowingContent) {
      if (currentContentIndex < moduleContent.length - 1) {
        setCurrentContentIndex(currentContentIndex + 1);
      } else if (moduleQuestions.length > 0) {
        // Switch to questions
        setIsShowingContent(false);
        setCurrentContentIndex(0);
        setSelectedAnswer(null);
        setShowFeedback(false);
      } else {
        // Move to next module
        handleNextModule();
      }
    } else {
      // In questions mode
      if (currentContentIndex < moduleQuestions.length - 1) {
        setCurrentContentIndex(currentContentIndex + 1);
        setSelectedAnswer(null);
        setShowFeedback(false);
      } else {
        // Finished all questions, move to next module
        handleNextModule();
      }
    }
  };

  const handlePreviousContent = () => {
    if (isShowingContent) {
      if (currentContentIndex > 0) {
        setCurrentContentIndex(currentContentIndex - 1);
      } else if (currentModuleIndex > 0) {
        // Go to previous module
        handlePreviousModule();
      }
    } else {
      // In questions mode
      if (currentContentIndex > 0) {
        setCurrentContentIndex(currentContentIndex - 1);
        setSelectedAnswer(null);
        setShowFeedback(false);
      } else if (moduleContent.length > 0) {
        // Go back to content
        setIsShowingContent(true);
        setCurrentContentIndex(moduleContent.length - 1);
      }
    }
  };

  const handleNextModule = () => {
    if (currentModuleIndex < modules.length - 1) {
      const nextIndex = currentModuleIndex + 1;
      setCurrentModuleIndex(nextIndex);
      setCurrentModule(modules[nextIndex]);
      setUserAnswers({});
    } else {
      // Course completed
      alert('Congratulations! You have completed the course!');
    }
  };

  const handlePreviousModule = () => {
    if (currentModuleIndex > 0) {
      const prevIndex = currentModuleIndex - 1;
      setCurrentModuleIndex(prevIndex);
      setCurrentModule(modules[prevIndex]);
      setUserAnswers({});
    }
  };

  const handleAnswerSelect = (answerIndex: number) => {
    setSelectedAnswer(answerIndex);
  };

  const handleSubmitAnswer = async () => {
    if (selectedAnswer === null) return;
    
    setShowFeedback(true);
    const currentQuestion = moduleQuestions[currentContentIndex];
    setUserAnswers({
      ...userAnswers,
      [currentQuestion.question_id]: selectedAnswer
    });
    
    // Save progress if user is logged in (optional - table might not exist)
    if (user && currentModule) {
      try {
        const isCorrect = selectedAnswer === currentQuestion.question.correct_answer_index;
        
        // Update user module progress if table exists
        const answeredQuestions = userProgress?.questions_answered || [];
        if (!answeredQuestions.includes(currentQuestion.question_id)) {
          answeredQuestions.push(currentQuestion.question_id);
        }
        
        const correctCount = userProgress?.questions_correct || 0;
        const newCorrectCount = isCorrect ? correctCount + 1 : correctCount;
        
        const { data: upsertData, error } = await supabase
          .from('user_module_progress')
          .upsert({
            user_id: user.id,
            module_id: currentModule.id,
            questions_answered: answeredQuestions,
            questions_correct: newCorrectCount,
            questions_total: moduleQuestions.length,
            completion_percentage: (answeredQuestions.length / moduleQuestions.length) * 100
          }, {
            onConflict: 'user_id,module_id'
          })
          .select()
          .maybeSingle();
        
        if (!error && upsertData) {
          // Successfully saved progress
          setUserProgress(upsertData);
        } else {
          // Update local state even if save failed
          const updatedProgress = {
            ...userProgress,
            questions_answered: answeredQuestions,
            questions_correct: newCorrectCount,
            questions_total: moduleQuestions.length,
            completion_percentage: (answeredQuestions.length / moduleQuestions.length) * 100
          } as UserModuleProgress;
          setUserProgress(updatedProgress);
        }
      } catch (err) {
        // Table might not exist, which is fine
        console.log('Could not save module progress');
      }
    }
  };

  const renderContent = () => {
    if (isShowingContent && moduleContent.length > 0) {
      const content = moduleContent[currentContentIndex];
      
      // Extract the text content from different possible formats
      const getContentText = (contentObj: any) => {
        if (typeof contentObj === 'string') return contentObj;
        if (contentObj.text) return contentObj.text;
        if (contentObj.content) return contentObj.content;
        return JSON.stringify(contentObj);
      };
      
      return (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center mb-4">
            <BookOpenIcon className="h-6 w-6 text-green-600 mr-2" />
            <h3 className="text-xl font-semibold">{content.title}</h3>
          </div>
          
          <div className="prose prose-green max-w-none prose-p:my-3 prose-headings:mt-6 prose-headings:mb-4 prose-ul:my-4 prose-li:my-1">
            {content.content_type === 'lesson' && (
              <div className="markdown-content">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    p: ({children}) => <p className="my-3 leading-relaxed">{children}</p>,
                    h1: ({children}) => <h1 className="text-2xl font-bold mt-6 mb-4 text-gray-900">{children}</h1>,
                    h2: ({children}) => <h2 className="text-xl font-bold mt-5 mb-3 text-gray-800">{children}</h2>,
                    h3: ({children}) => <h3 className="text-lg font-semibold mt-4 mb-2 text-gray-800">{children}</h3>,
                    ul: ({children}) => <ul className="list-disc pl-6 my-4 space-y-2">{children}</ul>,
                    ol: ({children}) => <ol className="list-decimal pl-6 my-4 space-y-2">{children}</ol>,
                    li: ({children}) => <li className="my-1 leading-relaxed">{children}</li>,
                    br: () => <br className="my-2" />,
                  }}
                >
                  {getContentText(content.content)}
                </ReactMarkdown>
                {content.content.examples && (
                  <div className="mt-4 bg-green-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-green-800 mb-2">Examples:</h4>
                    <ul className="space-y-2">
                      {content.content.examples.map((example: string, idx: number) => (
                        <li key={idx} className="text-green-700">
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {example}
                          </ReactMarkdown>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
            
            {content.content_type === 'vocabulary' && (
              <div className="space-y-3">
                {content.content.words && content.content.words.map((word: any, idx: number) => (
                  <div key={idx} className="bg-gray-50 p-3 rounded-lg">
                    <span className="font-semibold">{word.latin}</span> - {word.english}
                    {word.notes && <span className="text-gray-600 text-sm ml-2">({word.notes})</span>}
                  </div>
                ))}
              </div>
            )}
            
            {content.content_type === 'grammar_rule' && (
              <div>
                <div className="bg-yellow-50 p-4 rounded-lg mb-4 markdown-content">
                  <ReactMarkdown 
                    remarkPlugins={[remarkGfm]}
                    components={{
                      p: ({children}) => <p className="my-3 leading-relaxed">{children}</p>,
                      h1: ({children}) => <h1 className="text-2xl font-bold mt-6 mb-4 text-gray-900">{children}</h1>,
                      h2: ({children}) => <h2 className="text-xl font-bold mt-5 mb-3 text-gray-800">{children}</h2>,
                      h3: ({children}) => <h3 className="text-lg font-semibold mt-4 mb-2 text-gray-800">{children}</h3>,
                      ul: ({children}) => <ul className="list-disc pl-6 my-4 space-y-2">{children}</ul>,
                      ol: ({children}) => <ol className="list-decimal pl-6 my-4 space-y-2">{children}</ol>,
                      li: ({children}) => <li className="my-1 leading-relaxed">{children}</li>,
                      br: () => <br className="my-2" />,
                    }}
                  >
                    {getContentText(content.content)}
                  </ReactMarkdown>
                </div>
                {content.content.examples && (
                  <div className="space-y-2">
                    <h4 className="font-semibold">Examples:</h4>
                    {content.content.examples.map((ex: string, idx: number) => (
                      <div key={idx} className="text-gray-600 pl-4 flex">
                        <span>• </span>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {ex}
                        </ReactMarkdown>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      );
    }
    
    if (!isShowingContent && moduleQuestions.length > 0) {
      const question = moduleQuestions[currentContentIndex];
      const isCorrect = showFeedback && selectedAnswer === question.question.correct_answer_index;
      
      return (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <AcademicCapIcon className="h-6 w-6 text-green-600 mr-2" />
              <h3 className="text-xl font-semibold">Practice Question {currentContentIndex + 1}</h3>
            </div>
            <span className="text-sm text-gray-500">{question.points} points</span>
          </div>
          
          <div className="mb-6">
            <p className="text-lg text-gray-800 mb-4">{question.question.question_text}</p>
            
            {question.question.question_type === 'multiple_choice' && (
              <div className="space-y-3">
                {question.question.options.map((option: string, idx: number) => (
                  <button
                    key={idx}
                    onClick={() => handleAnswerSelect(idx)}
                    disabled={showFeedback}
                    className={`w-full text-left p-3 rounded-lg border-2 transition-colors ${
                      selectedAnswer === idx
                        ? showFeedback
                          ? idx === question.question.correct_answer_index
                            ? 'border-green-500 bg-green-50'
                            : 'border-red-500 bg-red-50'
                          : 'border-green-500 bg-green-50'
                        : 'border-gray-200 hover:border-gray-300'
                    } ${showFeedback ? 'cursor-not-allowed' : 'cursor-pointer'}`}
                  >
                    <span className="font-medium">{String.fromCharCode(65 + idx)}.</span> {option}
                  </button>
                ))}
              </div>
            )}
            
            {question.question.question_type === 'fill_in_blank' && (
              <input
                type="text"
                className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-green-500 focus:outline-none"
                placeholder="Type your answer here..."
                disabled={showFeedback}
              />
            )}
          </div>
          
          {!showFeedback && (
            <button
              onClick={handleSubmitAnswer}
              disabled={selectedAnswer === null}
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              Submit Answer
            </button>
          )}
          
          {showFeedback && (
            <div className={`mt-4 p-4 rounded-lg ${isCorrect ? 'bg-green-100' : 'bg-red-100'}`}>
              <p className={`font-semibold ${isCorrect ? 'text-green-800' : 'text-red-800'}`}>
                {isCorrect ? 'Correct!' : 'Incorrect'}
              </p>
              <p className="mt-2 text-gray-700">{question.question.explanation}</p>
            </div>
          )}
        </div>
      );
    }
    
    return null;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-600 p-4">
        Error loading course: {error}
      </div>
    );
  }

  if (!course || !currentModule) {
    return (
      <div className="text-center text-gray-600 p-4">
        Course not found
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Course Header */}
      <div className="bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg p-6 mb-6">
        <h1 className="text-3xl font-bold mb-2">{course.name}</h1>
        <p className="text-green-100 mb-4">{course.description}</p>
        <div className="flex items-center space-x-4 text-sm">
          <span className="bg-green-800 px-3 py-1 rounded-full">{course.level}</span>
          <span>{course.estimated_hours} hours</span>
        </div>
      </div>

      {/* Module Navigation */}
      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">
            Chapter {currentModule.chapter_number}: {currentModule.title}
          </h2>
          <div className="flex items-center space-x-2">
            <button
              onClick={handlePreviousModule}
              disabled={currentModuleIndex === 0}
              className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeftIcon className="h-5 w-5" />
            </button>
            <span className="text-sm text-gray-600">
              {currentModuleIndex + 1} / {modules.length}
            </span>
            <button
              onClick={handleNextModule}
              disabled={currentModuleIndex === modules.length - 1}
              className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRightIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
        {currentModule.description && (
          <p className="text-gray-600 mt-2">{currentModule.description}</p>
        )}
      </div>

      {/* Content Area */}
      <div className="mb-6">
        {renderContent()}
      </div>

      {/* Navigation Controls */}
      <div className="flex justify-between items-center">
        <button
          onClick={handlePreviousContent}
          className="flex items-center px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
        >
          <ChevronLeftIcon className="h-5 w-5 mr-1" />
          Previous
        </button>
        
        <div className="flex items-center space-x-2">
          {isShowingContent ? (
            <>
              {moduleContent.map((_, idx) => (
                <div
                  key={idx}
                  className={`h-2 w-2 rounded-full ${
                    idx === currentContentIndex ? 'bg-green-600' : 'bg-gray-300'
                  }`}
                />
              ))}
            </>
          ) : (
            <>
              {moduleQuestions.map((_, idx) => (
                <div
                  key={idx}
                  className={`h-2 w-2 rounded-full ${
                    idx === currentContentIndex ? 'bg-green-600' : 
                    userAnswers[moduleQuestions[idx].question_id] !== undefined ? 'bg-green-400' : 'bg-gray-300'
                  }`}
                />
              ))}
            </>
          )}
        </div>
        
        <button
          onClick={handleNextContent}
          disabled={!isShowingContent && !showFeedback && moduleQuestions.length > 0}
          className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          Next
          <ChevronRightIcon className="h-5 w-5 ml-1" />
        </button>
      </div>
    </div>
  );
};