export interface SkillTreeNode {
  id: string
  parent_id: string | null
  name: string
  type: string
  path: string
  learning_area: string
  metadata: any
  display_order: number
  created_at: string
  updated_at: string
  has_learning_content: boolean
  learning_content_ids: string[] | null
  is_menu_leaf: boolean
  source_url?: string
}

export interface LearningContent {
  id: string
  title: string
  content: string
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

export interface UserProgress {
  id: string
  user_id: string
  skill_node_id: string
  status: 'not_started' | 'in_progress' | 'completed'
  rating: number
  last_accessed: string
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
  skill_node_id: string
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