import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ClockIcon,
  ChevronRightIcon,
  LockClosedIcon,
  BookOpenIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline';
import { SkillTreeNode } from '../types/database.types';

interface Course extends SkillTreeNode {
  sequence_number?: number;
  is_required?: boolean;
  unlock_after_course_id?: string | null;
  estimated_hours?: number;
  level?: string;
}

interface CoursesListProps {
  courses: Course[];
  title?: string;
  userProgress?: {
    courses_completed: number;
  };
  showSequenceNumbers?: boolean;
  onCourseClick?: (course: Course) => void;
  className?: string;
}

const CoursesList: React.FC<CoursesListProps> = ({
  courses,
  title = "Courses",
  userProgress,
  showSequenceNumbers = true,
  onCourseClick,
  className = ""
}) => {
  const navigate = useNavigate();

  const handleCourseClick = (course: Course) => {
    console.log('handleCourseClick called for:', course.name);
    console.log('onCourseClick provided?', !!onCourseClick);
    if (onCourseClick) {
      console.log('Calling provided onCourseClick');
      onCourseClick(course);
    } else {
      // Default navigation using CategoryLink logic
      // Courses are skill_tree_nodes, so we navigate to them as categories
      const path = `/learning/${course.id}`;
      console.log('Navigating to:', path);
      navigate(path);
    }
  };

  const isUnlocked = (course: Course, index: number) => {
    if (!course.unlock_after_course_id) return true;
    if (!userProgress) return false;
    return userProgress.courses_completed >= index;
  };

  const getDifficultyColor = (difficulty?: string) => {
    switch (difficulty?.toLowerCase()) {
      case 'beginner':
        return 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300';
      case 'advanced':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-300';
      case 'expert':
        return 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/50 dark:text-gray-300';
    }
  };

  if (courses.length === 0) {
    return null;
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <AcademicCapIcon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
          {title}
        </h3>
      )}
      
      <div className="space-y-3">
        {courses.map((course, index) => {
          const unlocked = isUnlocked(course, index);
          const sequenceNum = course.sequence_number ?? (index + 1);
          
          return (
            <button
              key={course.id}
              className={`w-full flex items-center p-4 rounded-lg border transition-all text-left ${
                unlocked
                  ? 'border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer hover:shadow-md'
                  : 'border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50 opacity-60 cursor-not-allowed'
              }`}
              onClick={() => {
                console.log('Course clicked:', course.name, 'unlocked:', unlocked);
                if (unlocked) {
                  handleCourseClick(course);
                }
              }}
              disabled={!unlocked}
            >
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  {!unlocked && <LockClosedIcon className="h-4 w-4 text-gray-400" />}
                  {showSequenceNumbers && (
                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">
                      {sequenceNum}.
                    </span>
                  )}
                  <span className="font-medium text-gray-900 dark:text-white">
                    {course.name}
                  </span>
                  {course.is_required === false && (
                    <span className="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                      Optional
                    </span>
                  )}
                  {course.metadata?.difficulty && (
                    <span className={`text-xs px-2 py-1 rounded ${getDifficultyColor(course.metadata.difficulty)}`}>
                      {course.metadata.difficulty}
                    </span>
                  )}
                </div>
                
                {course.description && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
                    {course.description}
                  </p>
                )}
                
                <div className="flex items-center gap-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                  {course.level && (
                    <span className="flex items-center gap-1">
                      <BookOpenIcon className="h-3 w-3" />
                      {course.level}
                    </span>
                  )}
                  {(course.estimated_hours || course.metadata?.estimated_hours) && (
                    <span className="flex items-center gap-1">
                      <ClockIcon className="h-3 w-3" />
                      {course.estimated_hours || course.metadata?.estimated_hours} hours
                    </span>
                  )}
                  {course.metadata?.textbook && (
                    <span className="flex items-center gap-1">
                      📚 {course.metadata.textbook}
                    </span>
                  )}
                  {course.metadata?.year && (
                    <span className="flex items-center gap-1">
                      Year {course.metadata.year}
                    </span>
                  )}
                </div>
              </div>
              
              {unlocked && (
                <ChevronRightIcon className="h-5 w-5 text-gray-400 flex-shrink-0" />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default CoursesList;