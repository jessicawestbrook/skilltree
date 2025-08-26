import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabase';
import { BookOpenIcon, ClockIcon, DocumentTextIcon, QuestionMarkCircleIcon, PlayIcon } from '@heroicons/react/24/outline';

interface Course {
  id: string;
  language_id: string;
  name: string;
  description: string;
  level: string;
  estimated_hours: number;
  created_at: string;
}

interface CourseModule {
  id: string;
  course_id: string;
  parent_module_id: string | null;
  title: string;
  description: string;
  chapter_number: number;
  module_type: string;
  display_order: number;
  is_locked: boolean;
  prerequisites: string[] | null;
  created_at: string;
  updated_at: string;
}

interface ModuleStats {
  content_count: number;
  question_count: number;
}

const CourseOverview: React.FC = () => {
  const { courseSlug } = useParams<{ courseSlug: string }>();
  const navigate = useNavigate();
  const [course, setCourse] = useState<Course | null>(null);
  const [modules, setModules] = useState<CourseModule[]>([]);
  const [moduleStats, setModuleStats] = useState<Record<string, ModuleStats>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (courseSlug) {
      loadCourseData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseSlug]);

  const loadCourseData = async () => {
    try {
      setLoading(true);
      
      // Load course details by slug
      const { data: courseData, error: courseError } = await supabase
        .from('language_courses')
        .select('*')
        .eq('slug', courseSlug)
        .single();
        
      if (courseError) throw courseError;
      setCourse(courseData);
      
      // Load course modules using the course's ID
      const { data: modulesData, error: modulesError } = await supabase
        .from('course_modules')
        .select('*')
        .eq('course_id', courseData.id)
        .order('chapter_number')
        .order('display_order');
        
      if (modulesError) throw modulesError;
      setModules(modulesData || []);
      
      // Load stats for each module
      const stats: Record<string, ModuleStats> = {};
      for (const module of modulesData || []) {
        // Count content
        const { count: contentCount } = await supabase
          .from('module_content')
          .select('*', { count: 'exact', head: true })
          .eq('module_id', module.id);
          
        // Count questions
        const { count: questionCount } = await supabase
          .from('module_questions')
          .select('*', { count: 'exact', head: true })
          .eq('module_id', module.id);
          
        stats[module.id] = {
          content_count: contentCount || 0,
          question_count: questionCount || 0
        };
      }
      setModuleStats(stats);
      
    } catch (err: any) {
      console.error('Error loading course data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getLevelColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'elementary': return 'bg-blue-100 text-blue-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const groupModulesByChapter = () => {
    const chapters: Record<number, CourseModule[]> = {};
    modules.forEach(module => {
      if (!chapters[module.chapter_number]) {
        chapters[module.chapter_number] = [];
      }
      chapters[module.chapter_number].push(module);
    });
    return chapters;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading course overview...</p>
        </div>
      </div>
    );
  }

  if (error || !course) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600">Error: {error || 'Course not found'}</p>
          <button
            onClick={() => navigate('/learning-paths')}
            className="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Back to Learning Paths
          </button>
        </div>
      </div>
    );
  }

  const chapters = groupModulesByChapter();
  const totalContent = Object.values(moduleStats).reduce((sum, stat) => sum + stat.content_count, 0);
  const totalQuestions = Object.values(moduleStats).reduce((sum, stat) => sum + stat.question_count, 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="container mx-auto px-4 py-8">
        {/* Course Header */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <div className="flex items-start justify-between mb-6">
            <div className="flex-1">
              <h1 className="text-4xl font-bold text-gray-800 mb-4">{course.name}</h1>
              <p className="text-gray-600 text-lg leading-relaxed">{course.description}</p>
            </div>
            <span className={`px-4 py-2 rounded-full text-sm font-semibold ${getLevelColor(course.level)}`}>
              {course.level}
            </span>
          </div>

          {/* Course Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-8 p-6 bg-gray-50 rounded-lg">
            <div className="text-center">
              <BookOpenIcon className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <p className="text-2xl font-bold text-gray-800">{Object.keys(chapters).length}</p>
              <p className="text-sm text-gray-500">Chapters</p>
            </div>
            <div className="text-center">
              <DocumentTextIcon className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <p className="text-2xl font-bold text-gray-800">{totalContent}</p>
              <p className="text-sm text-gray-500">Lessons</p>
            </div>
            <div className="text-center">
              <QuestionMarkCircleIcon className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <p className="text-2xl font-bold text-gray-800">{totalQuestions}</p>
              <p className="text-sm text-gray-500">Exercises</p>
            </div>
            <div className="text-center">
              <ClockIcon className="h-8 w-8 text-orange-600 mx-auto mb-2" />
              <p className="text-2xl font-bold text-gray-800">{course.estimated_hours}h</p>
              <p className="text-sm text-gray-500">Duration</p>
            </div>
          </div>

          {/* Start Course Button */}
          <div className="mt-8 flex justify-center">
            <button
              onClick={() => navigate(`/course/${courseSlug}`)}
              className="px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-lg shadow-lg hover:from-green-700 hover:to-emerald-700 transform hover:scale-105 transition-all duration-200 flex items-center space-x-2"
            >
              <PlayIcon className="h-6 w-6" />
              <span>Start Course</span>
            </button>
          </div>
        </div>

        {/* Table of Contents */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Table of Contents</h2>
          
          <div className="space-y-6">
            {Object.entries(chapters).map(([chapterNum, chapterModules]) => (
              <div key={chapterNum} className="border-l-4 border-green-500 pl-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">
                  Chapter {chapterNum}
                </h3>
                
                <div className="space-y-3">
                  {chapterModules.map((module) => {
                    const stats = moduleStats[module.id] || { content_count: 0, question_count: 0 };
                    return (
                      <div
                        key={module.id}
                        className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                        onClick={() => navigate(`/course/${courseSlug}`)}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-medium text-gray-800">
                              {module.title}
                            </h4>
                            {module.description && (
                              <p className="text-sm text-gray-600 mt-1">{module.description}</p>
                            )}
                            
                            <div className="flex items-center space-x-4 mt-2">
                              {stats.content_count > 0 && (
                                <span className="text-xs text-gray-500 flex items-center">
                                  <DocumentTextIcon className="h-4 w-4 mr-1" />
                                  {stats.content_count} lesson{stats.content_count !== 1 ? 's' : ''}
                                </span>
                              )}
                              {stats.question_count > 0 && (
                                <span className="text-xs text-gray-500 flex items-center">
                                  <QuestionMarkCircleIcon className="h-4 w-4 mr-1" />
                                  {stats.question_count} exercise{stats.question_count !== 1 ? 's' : ''}
                                </span>
                              )}
                              {module.is_locked && (
                                <span className="text-xs text-gray-500 flex items-center">
                                  🔒 Locked
                                </span>
                              )}
                            </div>

                            {module.prerequisites && module.prerequisites.length > 0 && (
                              <div className="mt-2">
                                <p className="text-xs text-gray-500 font-semibold">Prerequisites:</p>
                                <ul className="text-xs text-gray-600 mt-1 list-disc list-inside">
                                  {module.prerequisites.slice(0, 2).map((prereq, idx) => (
                                    <li key={idx}>{prereq}</li>
                                  ))}
                                  {module.prerequisites.length > 2 && (
                                    <li className="text-gray-400">
                                      +{module.prerequisites.length - 2} more...
                                    </li>
                                  )}
                                </ul>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CourseOverview;