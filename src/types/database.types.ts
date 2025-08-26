export interface SkillTreeNode {
  id: string
  parent_id: string | null
  name: string
  description?: string
  metadata: any
  display_order: number
  created_at: string
  updated_at: string
  learning_content_ids: string[] | null
  is_hidden?: boolean
  source_url?: string
}

export interface LearningContent {
  id: string
  title: string
  content: string
  content_sections?: {
    title?: string
    content: string
    image?: {
      url: string
      caption?: string
    }
  }[] | null
  images: (string | { url: string; caption?: string })[] | null
  estimated_time_minutes: number
  difficulty_level: string
  question_ids: string[] | null
  source_url?: string
  created_at: string
  updated_at: string
}

export interface Question {
  id: string
  question_text: string
  options: string[]
  correct_answer: number
  explanation: string
  difficulty: string
  image_url?: string
  source_url?: string
  created_at: string
}

export interface UserProfile {
  id: string
  email: string
  username?: string
  avatar_url?: string
  created_at: string
  updated_at: string
}

export interface Notification {
  id: string
  user_id: string
  type: 'achievement' | 'progress' | 'reminder' | 'system' | 'social'
  title: string
  message: string
  data?: any
  is_read: boolean
  created_at: string
  expires_at?: string
}

export interface NotificationPreferences {
  user_id: string
  email_notifications: boolean
  push_notifications: boolean
  achievement_notifications: boolean
  progress_notifications: boolean
  reminder_notifications: boolean
  system_notifications: boolean
  created_at: string
  updated_at: string
}

export interface UserProgress {
  id: string
  user_id: string
  skill_id: string
  status: 'not_started' | 'in_progress' | 'completed'
  rating: number
  last_accessed: string
  created_at: string
  updated_at: string
}

export interface UserModuleProgress {
  id: string
  user_id: string
  module_id: string
  status: 'not_started' | 'in_progress' | 'completed'
  progress_percentage: number
  created_at: string
  updated_at: string
}

export interface UserQuestionAttempt {
  id: string
  user_id: string
  question_id: string
  selected_option_id?: string
  user_answer?: string
  is_correct: boolean
  time_taken_seconds: number
  attempt_number: number
  created_at: string
}

export interface StarredCategory {
  id: string
  user_id: string
  skill_id: string
  created_at: string
}

export interface Feedback {
  id: string
  user_id: string
  category: 'bug' | 'content_request' | 'general' | 'question_issue'
  message: string
  status: 'open' | 'in_progress' | 'resolved'
  admin_response?: string
  created_at: string
  updated_at: string
}

export interface Language {
  id: string
  name: string
  code: string
  flag_emoji?: string
  created_at: string
  updated_at: string
}

export interface LanguageCategory {
  id: string
  language_id: string
  name: string
  description: string
  display_order: number
  created_at: string
  updated_at: string
}

export interface LanguageQuestion {
  id: string
  language_id: string
  category_id: string
  question_text: string
  question_type: string
  options: string[]
  correct_answer_index: number
  explanation: string
  difficulty_level: number
  image_url?: string
  audio_url?: string
  source_url?: string
  created_at: string
  updated_at: string
}

export interface UserLanguageAttempt {
  id: string
  user_id: string
  question_id: string
  selected_option_index: number
  is_correct: boolean
  time_taken_seconds: number
  created_at: string
}

export interface UserLanguageProgress {
  id: string
  user_id: string
  language_id: string
  category_id: string
  questions_attempted: number
  questions_correct: number
  accuracy_percentage: number
  last_practiced: string
  created_at: string
  updated_at: string
}

export interface StudyList {
  id: string
  user_id: string
  name: string
  description?: string
  color?: string
  is_public: boolean
  created_at: string
  updated_at: string
}

export interface StarredItem {
  id: string
  user_id: string
  item_type: 'spelling_word' | 'vocabulary_word' | 'language_question' | 'question' | 'skill_node' | 'custom_question'
  item_id: string
  item_data?: any
  created_at: string
}

export interface StudyListItem {
  id: string
  study_list_id: string
  item_type: 'spelling_word' | 'vocabulary_word' | 'language_question' | 'question' | 'skill_node' | 'custom_flashcard' | 'custom_question'
  item_id: string
  item_data?: any
  notes?: string
  added_at: string
}

export interface CustomFlashcard {
  id: string
  user_id: string
  front: string
  back: string
  category?: string
  tags?: string[]
  difficulty_level?: number
  created_at: string
  updated_at: string
}

export interface StudySession {
  id: string
  user_id: string
  study_list_id: string
  started_at: string
  ended_at?: string
  items_studied: number
  items_correct: number
  total_time_seconds: number
}

export interface UserInterestLevel {
  id: string
  user_id: string
  category: string
  interest_level: number
  updated_at: string
  created_at: string
}

export interface Course {
  id: string
  skill_node_id: string
  name: string
  description?: string
  slug?: string
  difficulty?: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  estimated_hours?: number
  prerequisites?: any[]
  learning_objectives?: any[]
  content_modules?: any[]
  metadata?: any
  is_active: boolean
  display_order: number
  created_at: string
  updated_at: string
}

export interface LearningPathCourse {
  id: string
  learning_path_id: string
  course_id: string
  sequence_order: number
  is_required: boolean
  created_at: string
}

export interface UserCourseProgress {
  id: string
  user_id: string
  course_id: string
  status: 'not_started' | 'in_progress' | 'completed'
  progress_percentage: number
  started_at?: string
  completed_at?: string
  last_accessed?: string
  metadata?: any
  created_at: string
  updated_at: string
}