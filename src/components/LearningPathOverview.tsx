import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabase';
import { BookOpenIcon, ClockIcon, AcademicCapIcon, ChevronRightIcon } from '@heroicons/react/24/outline';

interface LearningPath {
  id: string;
  name: string;
  description: string;
  difficulty_level: string;
  estimated_duration_hours: number;
  prerequisites: string[];
  learning_objectives: string[];
  created_at: string;
}

interface PathCourse {
  id: string;
  learning_path_id: string;
  course_id: string;
  sequence_number: number;
  is_required: boolean;
  unlock_after_course_id: string | null;
  created_at: string;
  language_courses: {
    id: string;
    name: string;
    description: string;
    level: string;
    estimated_hours: number;
    slug: string;
  };
}

const LearningPathOverview: React.FC = () => {
  const { pathSlug } = useParams<{ pathSlug: string }>();
  const navigate = useNavigate();
  const [path, setPath] = useState<LearningPath | null>(null);
  const [courses, setCourses] = useState<PathCourse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (pathSlug) {
      loadPathData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathSlug]);

  const loadPathData = async () => {
    try {
      setLoading(true);
      
      // Load learning path details by slug
      const { data: pathData, error: pathError } = await supabase
        .from('learning_paths')
        .select('*')
        .eq('slug', pathSlug)
        .single();
        
      if (pathError) throw pathError;
      setPath(pathData);
      
      // Load courses in this path using the path's ID
      const { data: coursesData, error: coursesError } = await supabase
        .from('learning_path_courses')
        .select(`
          *,
          language_courses!course_id(
            id, name, description, level, estimated_hours, slug
          )
        `)
        .eq('learning_path_id', pathData.id)
        .order('sequence_number');
        
      if (coursesError) throw coursesError;
      setCourses(coursesData || []);
      
    } catch (err: any) {
      console.error('Error loading path data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCourseLevel = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'beginner': return 'bg-emerald-50 border-emerald-200';
      case 'elementary': return 'bg-blue-50 border-blue-200';
      case 'intermediate': return 'bg-indigo-50 border-indigo-200';
      case 'advanced': return 'bg-purple-50 border-purple-200';
      default: return 'bg-gray-50 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading learning path...</p>
        </div>
      </div>
    );
  }

  if (error || !path) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600">Error: {error || 'Path not found'}</p>
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="container mx-auto px-4 py-8">
        {/* Path Header */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <div className="flex items-start justify-between mb-6">
            <div className="flex-1">
              <h1 className="text-4xl font-bold text-gray-800 mb-4">{path.name}</h1>
              <p className="text-gray-600 text-lg leading-relaxed">{path.description}</p>
            </div>
            <span className={`px-4 py-2 rounded-full text-sm font-semibold ${getDifficultyColor(path.difficulty_level)}`}>
              {path.difficulty_level}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            {/* Duration */}
            <div className="flex items-center space-x-3">
              <ClockIcon className="h-8 w-8 text-green-600" />
              <div>
                <p className="text-sm text-gray-500">Estimated Duration</p>
                <p className="text-lg font-semibold text-gray-800">
                  {path.estimated_duration_hours} hours
                </p>
              </div>
            </div>

            {/* Courses */}
            <div className="flex items-center space-x-3">
              <BookOpenIcon className="h-8 w-8 text-green-600" />
              <div>
                <p className="text-sm text-gray-500">Total Courses</p>
                <p className="text-lg font-semibold text-gray-800">
                  {courses.length} courses
                </p>
              </div>
            </div>

            {/* Level */}
            <div className="flex items-center space-x-3">
              <AcademicCapIcon className="h-8 w-8 text-green-600" />
              <div>
                <p className="text-sm text-gray-500">Difficulty Level</p>
                <p className="text-lg font-semibold text-gray-800">
                  {path.difficulty_level}
                </p>
              </div>
            </div>
          </div>

          {/* Prerequisites */}
          {path.prerequisites && path.prerequisites.length > 0 && (
            <div className="mt-8 p-4 bg-amber-50 rounded-lg border border-amber-200">
              <h3 className="font-semibold text-amber-800 mb-2">Prerequisites</h3>
              <ul className="list-disc list-inside text-amber-700 space-y-1">
                {path.prerequisites.map((prereq, index) => (
                  <li key={index}>{prereq}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Learning Objectives */}
          {path.learning_objectives && path.learning_objectives.length > 0 && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <h3 className="font-semibold text-blue-800 mb-2">Learning Objectives</h3>
              <ul className="list-disc list-inside text-blue-700 space-y-1">
                {path.learning_objectives.map((objective, index) => (
                  <li key={index}>{objective}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Courses List */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Courses in this Path</h2>
          
          <div className="space-y-4">
            {courses.map((course, index) => (
              <div
                key={course.id}
                className={`p-6 rounded-lg border-2 transition-all hover:shadow-md cursor-pointer ${getCourseLevel(course.language_courses.level)}`}
                onClick={() => navigate(`/course/${course.language_courses.slug}/overview`)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0 w-12 h-12 bg-white rounded-full flex items-center justify-center font-bold text-lg text-green-600 border-2 border-green-300">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-xl font-semibold text-gray-800">
                          {course.language_courses.name}
                        </h3>
                        {course.is_required && (
                          <span className="px-2 py-1 bg-red-100 text-red-600 text-xs font-semibold rounded">
                            Required
                          </span>
                        )}
                        <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs font-semibold rounded">
                          {course.language_courses.level}
                        </span>
                      </div>
                      <p className="text-gray-600 mb-2">
                        {course.language_courses.description}
                      </p>
                      <p className="text-sm text-gray-500">
                        Estimated time: {course.language_courses.estimated_hours} hours
                      </p>
                    </div>
                  </div>
                  <ChevronRightIcon className="h-6 w-6 text-gray-400 flex-shrink-0" />
                </div>
              </div>
            ))}
          </div>

          {/* Start Path Button */}
          <div className="mt-8 flex justify-center">
            <button
              onClick={() => {
                if (courses.length > 0) {
                  navigate(`/course/${courses[0].language_courses.slug}/overview`);
                }
              }}
              className="px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-lg shadow-lg hover:from-green-700 hover:to-emerald-700 transform hover:scale-105 transition-all duration-200"
            >
              Start Learning Path
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LearningPathOverview;