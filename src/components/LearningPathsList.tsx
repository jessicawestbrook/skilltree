import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabase';
import { useAuth } from '../contexts/AuthContext';
import {
  AcademicCapIcon,
  BookOpenIcon,
  ChartBarIcon,
  SparklesIcon,
  ClockIcon,
  ChevronRightIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import CoursesList from './CoursesList';

interface LearningPath {
  id: string;
  name: string;
  slug: string;
  description: string;
  category: string;
  difficulty: string;
  estimated_hours: number;
  icon_name: string;
  color: string;
  language_id: string | null;
  is_active: boolean;
  display_order: number;
  prerequisites: any[];
  metadata: any;
}

interface LearningPathCourse {
  id: string;
  learning_path_id: string;
  course_id: string;
  sequence_number: number;
  is_required: boolean;
  unlock_after_course_id: string | null;
  language_courses: {
    id: string;
    name: string;
    description: string;
    level: string;
    estimated_hours: number;
  };
}

interface UserPathProgress {
  learning_path_id: string;
  current_course_id: string | null;
  courses_completed: number;
  total_courses: number;
  completion_percentage: number;
}

const iconMap: { [key: string]: React.ReactNode } = {
  'AcademicCapIcon': <AcademicCapIcon className="h-6 w-6" />,
  'BookOpenIcon': <BookOpenIcon className="h-6 w-6" />,
  'ChartBarIcon': <ChartBarIcon className="h-6 w-6" />,
  'SparklesIcon': <SparklesIcon className="h-6 w-6" />
};

const colorClasses: { [key: string]: string } = {
  'purple': 'bg-purple-100 dark:bg-purple-900/20 border-purple-300 dark:border-purple-700',
  'blue': 'bg-blue-100 dark:bg-blue-900/20 border-blue-300 dark:border-blue-700',
  'green': 'bg-green-100 dark:bg-green-900/20 border-green-300 dark:border-green-700',
  'gold': 'bg-yellow-100 dark:bg-yellow-900/20 border-yellow-300 dark:border-yellow-700',
  'teal': 'bg-teal-100 dark:bg-teal-900/20 border-teal-300 dark:border-teal-700'
};

export const LearningPathsList: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([]);
  const [pathCourses, setPathCourses] = useState<Map<string, LearningPathCourse[]>>(new Map());
  const [userProgress, setUserProgress] = useState<Map<string, UserPathProgress>>(new Map());
  const [loading, setLoading] = useState(true);
  const [selectedPath, setSelectedPath] = useState<LearningPath | null>(null);

  useEffect(() => {
    loadLearningPaths();
  }, []);

  useEffect(() => {
    if (user) {
      loadUserProgress();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const loadLearningPaths = async () => {
    try {
      setLoading(true);
      
      // Fetch all active learning paths
      const { data: paths, error: pathsError } = await supabase
        .from('learning_paths')
        .select('*')
        .eq('is_active', true)
        .order('display_order');
      
      if (pathsError) throw pathsError;
      setLearningPaths(paths || []);
      
      // Fetch courses for each path
      const coursesMap = new Map<string, LearningPathCourse[]>();
      
      for (const path of paths || []) {
        const { data: courses, error: coursesError } = await supabase
          .from('learning_path_courses')
          .select(`
            *,
            language_courses!course_id(
              id,
              name,
              description,
              level,
              estimated_hours
            )
          `)
          .eq('learning_path_id', path.id)
          .order('sequence_number');
        
        if (!coursesError && courses) {
          coursesMap.set(path.id, courses);
        } else if (coursesError) {
          console.error(`Error loading courses for path ${path.id}:`, coursesError);
        }
      }
      
      setPathCourses(coursesMap);
      
    } catch (err) {
      console.error('Error loading learning paths:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadUserProgress = async () => {
    if (!user) return;
    
    try {
      const { data: progress, error } = await supabase
        .from('user_learning_path_progress')
        .select('*')
        .eq('user_id', user.id);
      
      if (!error && progress) {
        const progressMap = new Map<string, UserPathProgress>();
        progress.forEach(p => {
          progressMap.set(p.learning_path_id, p);
        });
        setUserProgress(progressMap);
      }
    } catch (err) {
      console.error('Error loading user progress:', err);
    }
  };

  const startLearningPath = async (path: LearningPath) => {
    // Navigate to learning path overview using slug
    navigate(`/learning-paths/${path.slug}`);
  };

  const continueLearningPath = (path: LearningPath) => {
    // Navigate to learning path overview using slug
    navigate(`/learning-paths/${path.slug}`);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'beginner':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'advanced':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      case 'comprehensive':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Learning Paths
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Structured curriculum to guide your learning journey
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {learningPaths.map(path => {
          const courses = pathCourses.get(path.id) || [];
          const progress = userProgress.get(path.id);
          const isStarted = !!progress;
          const isCompleted = progress?.completion_percentage === 100;
          
          return (
            <div
              key={path.id}
              className={`relative rounded-lg border-2 p-6 hover:shadow-lg transition-shadow ${
                colorClasses[path.color] || colorClasses['blue']
              }`}
            >
              {/* Icon and Title */}
              <div 
                className="flex items-start justify-between mb-4 cursor-pointer"
                onClick={() => setSelectedPath(path)}
              >
                <div className="flex items-center">
                  <div className={`p-2 rounded-lg bg-white dark:bg-gray-800`}>
                    {iconMap[path.icon_name] || <BookOpenIcon className="h-6 w-6" />}
                  </div>
                  <div className="ml-3">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      {path.name}
                    </h3>
                    <span className={`inline-block px-2 py-1 text-xs rounded-full mt-1 ${
                      getDifficultyColor(path.difficulty)
                    }`}>
                      {path.difficulty}
                    </span>
                  </div>
                </div>
                {isCompleted && (
                  <CheckCircleIcon className="h-6 w-6 text-green-600" />
                )}
              </div>

              {/* Description */}
              <p 
                className="text-sm text-gray-600 dark:text-gray-300 mb-4 line-clamp-2 cursor-pointer"
                onClick={() => setSelectedPath(path)}
              >
                {path.description}
              </p>

              {/* Stats */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                  <ClockIcon className="h-4 w-4 mr-1" />
                  {path.estimated_hours} hours
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  {courses.length} courses
                </div>
              </div>

              {/* Progress Bar */}
              {isStarted && (
                <div className="mb-4">
                  <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mb-1">
                    <span>Progress</span>
                    <span>{Math.round(progress.completion_percentage)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-green-600 h-2 rounded-full transition-all"
                      style={{ width: `${progress.completion_percentage}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Action Button */}
              <button
                onClick={() => {
                  if (isStarted) {
                    continueLearningPath(path);
                  } else {
                    startLearningPath(path);
                  }
                }}
                className="w-full flex items-center justify-center px-4 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors font-medium"
              >
                {isStarted ? 'Continue' : 'Start Path'}
                <ChevronRightIcon className="h-4 w-4 ml-2" />
              </button>
            </div>
          );
        })}
      </div>

      {/* Path Details Modal */}
      {selectedPath && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={() => setSelectedPath(null)}
        >
          <div
            className="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {selectedPath.name}
                </h2>
                <span className={`inline-block px-3 py-1 text-sm rounded-full mt-2 ${
                  getDifficultyColor(selectedPath.difficulty)
                }`}>
                  {selectedPath.difficulty}
                </span>
              </div>
              <button
                onClick={() => setSelectedPath(null)}
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                ✕
              </button>
            </div>

            <p className="text-gray-600 dark:text-gray-300 mb-6">
              {selectedPath.description}
            </p>

            <div className="mb-6">
              <CoursesList
                courses={(pathCourses.get(selectedPath.id) || []).map((pathCourse, index) => ({
                  id: pathCourse.course_id,
                  name: pathCourse.language_courses?.name || 'Course',
                  description: pathCourse.language_courses?.description || '',
                  level: pathCourse.language_courses?.level,
                  estimated_hours: pathCourse.language_courses?.estimated_hours,
                  sequence_number: pathCourse.sequence_number || index + 1,
                  is_required: pathCourse.is_required,
                  unlock_after_course_id: pathCourse.unlock_after_course_id,
                  parent_id: null,
                  display_order: index,
                  metadata: {},
                  created_at: '',
                  updated_at: '',
                  learning_content_ids: null
                }))}
                title="Course Curriculum"
                userProgress={userProgress.get(selectedPath.id)}
                showSequenceNumbers={true}
                onCourseClick={(course) => {
                  navigate(`/course/${course.id}`);
                }}
              />
            </div>

            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setSelectedPath(null)}
                className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
              >
                Close
              </button>
              <button
                onClick={() => {
                  const progress = userProgress.get(selectedPath.id);
                  if (progress) {
                    continueLearningPath(selectedPath);
                  } else {
                    startLearningPath(selectedPath);
                  }
                }}
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                {userProgress.has(selectedPath.id) ? 'Continue Learning' : 'Start Learning Path'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};