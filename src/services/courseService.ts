import { supabase } from './supabase'
import { Course, UserCourseProgress } from '../types/database.types'

export class CourseService {
  // Fetch all courses for a skill node
  async getCoursesBySkillNode(skillNodeId: string): Promise<Course[]> {
    try {
      const { data, error } = await supabase
        .from('courses')
        .select('*')
        .eq('skill_node_id', skillNodeId)
        .eq('is_active', true)
        .order('display_order')

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching courses by skill node:', error)
      return []
    }
  }

  // Fetch all courses in a learning path
  async getCoursesInLearningPath(learningPathId: string): Promise<(Course & { sequence_order: number; is_required: boolean })[]> {
    try {
      const { data, error } = await supabase
        .from('learning_path_courses')
        .select(`
          sequence_order,
          is_required,
          courses (*)
        `)
        .eq('learning_path_id', learningPathId)
        .order('sequence_order')

      if (error) throw error
      
      // Flatten the response structure
      const courses = data?.map(item => ({
        ...item.courses,
        sequence_order: item.sequence_order,
        is_required: item.is_required
      })) || []
      
      return courses as any
    } catch (error) {
      console.error('Error fetching learning path courses:', error)
      return []
    }
  }

  // Get a single course by ID or slug
  async getCourse(idOrSlug: string): Promise<Course | null> {
    try {
      // Try by ID first
      let { data, error } = await supabase
        .from('courses')
        .select('*')
        .eq('id', idOrSlug)
        .single()

      if (error || !data) {
        // Try by slug
        const slugResult = await supabase
          .from('courses')
          .select('*')
          .eq('slug', idOrSlug)
          .single()
        
        if (slugResult.error) throw slugResult.error
        return slugResult.data
      }

      return data
    } catch (error) {
      console.error('Error fetching course:', error)
      return null
    }
  }

  // Get user's progress for a course
  async getUserCourseProgress(userId: string, courseId: string): Promise<UserCourseProgress | null> {
    try {
      const { data, error } = await supabase
        .from('user_course_progress')
        .select('*')
        .eq('user_id', userId)
        .eq('course_id', courseId)
        .single()

      if (error && error.code !== 'PGRST116') throw error // PGRST116 is "not found"
      return data || null
    } catch (error) {
      console.error('Error fetching user course progress:', error)
      return null
    }
  }

  // Update or create user's progress for a course
  async updateUserCourseProgress(
    userId: string, 
    courseId: string, 
    updates: Partial<UserCourseProgress>
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('user_course_progress')
        .upsert({
          user_id: userId,
          course_id: courseId,
          ...updates,
          updated_at: new Date().toISOString(),
          last_accessed: new Date().toISOString()
        })

      return !error
    } catch (error) {
      console.error('Error updating user course progress:', error)
      return false
    }
  }

  // Get all courses with user's progress
  async getUserCourses(userId: string): Promise<(Course & { progress?: UserCourseProgress })[]> {
    try {
      // Get all active courses
      const { data: courses, error: coursesError } = await supabase
        .from('courses')
        .select('*')
        .eq('is_active', true)
        .order('display_order')

      if (coursesError) throw coursesError

      // Get user's progress for all courses
      const { data: progress, error: progressError } = await supabase
        .from('user_course_progress')
        .select('*')
        .eq('user_id', userId)

      if (progressError) throw progressError

      // Combine courses with progress
      const progressMap = new Map(progress?.map(p => [p.course_id, p]) || [])
      
      return courses?.map(course => ({
        ...course,
        progress: progressMap.get(course.id)
      })) || []
    } catch (error) {
      console.error('Error fetching user courses:', error)
      return []
    }
  }

  // Create a new course (admin only)
  async createCourse(course: Omit<Course, 'id' | 'created_at' | 'updated_at'>): Promise<Course | null> {
    try {
      const { data, error } = await supabase
        .from('courses')
        .insert(course)
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error creating course:', error)
      return null
    }
  }

  // Update a course (admin only)
  async updateCourse(courseId: string, updates: Partial<Course>): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('courses')
        .update({
          ...updates,
          updated_at: new Date().toISOString()
        })
        .eq('id', courseId)

      return !error
    } catch (error) {
      console.error('Error updating course:', error)
      return false
    }
  }

  // Add a course to a learning path
  async addCourseToLearningPath(
    learningPathId: string, 
    courseId: string, 
    sequenceOrder: number = 0,
    isRequired: boolean = true
  ): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('learning_path_courses')
        .insert({
          learning_path_id: learningPathId,
          course_id: courseId,
          sequence_order: sequenceOrder,
          is_required: isRequired
        })

      return !error
    } catch (error) {
      console.error('Error adding course to learning path:', error)
      return false
    }
  }

  // Remove a course from a learning path
  async removeCourseFromLearningPath(learningPathId: string, courseId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('learning_path_courses')
        .delete()
        .eq('learning_path_id', learningPathId)
        .eq('course_id', courseId)

      return !error
    } catch (error) {
      console.error('Error removing course from learning path:', error)
      return false
    }
  }

  // Get learning paths that contain a specific course
  async getLearningPathsForCourse(courseId: string): Promise<any[]> {
    try {
      const { data, error } = await supabase
        .from('learning_path_courses')
        .select(`
          learning_paths (*)
        `)
        .eq('course_id', courseId)

      if (error) throw error
      return data?.map(item => item.learning_paths) || []
    } catch (error) {
      console.error('Error fetching learning paths for course:', error)
      return []
    }
  }
}

export const courseService = new CourseService()