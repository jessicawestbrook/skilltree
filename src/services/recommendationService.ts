import { supabase } from './supabase'
import { SkillTreeNode, UserInterestLevel } from '../types/database.types'

export interface RecommendationScore {
  node: SkillTreeNode
  score: number
  category: 'ready_to_learn' | 'challenge' | 'review' | 'interest' | 'skill_gap'
  reasons: string[]
}

export interface UserProfile {
  id: string
  overall_rating: number
  starred_skills: string[]
  completed_skills: string[]
  in_progress_skills: string[]
  recent_activity: Array<{
    skill_id: string
    timestamp: string
  }>
}

export interface RecommendationSettings {
  maxRecommendations?: number
  includeCategories?: string[]
  excludeCompleted?: boolean
  focusOnStarred?: boolean
}

class RecommendationService {
  /**
   * Get user interest levels from intro assessment
   */
  private async getUserInterestLevels(userId: string): Promise<UserInterestLevel[]> {
    const { data, error } = await supabase
      .from('user_interest_levels')
      .select('*')
      .eq('user_id', userId)

    if (error) {
      console.error('Error fetching user interest levels:', error)
      return []
    }
    return data || []
  }

  /**
   * Calculate interest score based on quiz results
   */
  private async calculateInterestScore(
    node: SkillTreeNode,
    userId: string
  ): Promise<number> {
    const interestLevels = await this.getUserInterestLevels(userId)
    
    if (interestLevels.length === 0) {
      return 0.5 // Neutral score if no interests set
    }

    // Map categories from quiz to learning areas
    const categoryMappings: Record<string, string[]> = {
      'Mathematics': ['math', 'mathematics', 'algebra', 'geometry', 'calculus', 'statistics', 'arithmetic', 'number'],
      'Science': ['science', 'physics', 'chemistry', 'biology', 'astronomy', 'earth science', 'environmental'],
      'English/Language Arts': ['english', 'language arts', 'reading', 'writing', 'literature', 'grammar', 'composition'],
      'Social Studies': ['history', 'geography', 'civics', 'government', 'economics', 'social studies', 'world cultures'],
      'Foreign Languages': ['spanish', 'french', 'german', 'chinese', 'japanese', 'foreign language', 'language learning'],
      'Computer Science': ['programming', 'computer science', 'coding', 'technology', 'software', 'algorithms'],
      'Arts': ['art', 'music', 'drama', 'creative arts', 'visual arts', 'performing arts', 'design'],
      'Physical Education': ['physical education', 'sports', 'fitness', 'health', 'nutrition', 'wellness', 'exercise'],
      'Career/Business Skills': ['career', 'business', 'entrepreneurship', 'professional skills', 'leadership', 'finance'],
      'Life Skills': ['life skills', 'personal development', 'communication', 'psychology', 'self-help']
    }

    let maxScore = 0
    const nodeName = node.name.toLowerCase()
    const nodeDescription = node.description?.toLowerCase() || ''
    const nodeContent = `${nodeName} ${nodeDescription}`

    // Check each user interest against the node
    for (const interest of interestLevels) {
      const categoryKeywords = categoryMappings[interest.category] || [interest.category.toLowerCase()]
      
      for (const keyword of categoryKeywords) {
        if (nodeContent.includes(keyword)) {
          const normalizedScore = interest.interest_level / 10 // Convert 1-10 to 0-1
          maxScore = Math.max(maxScore, normalizedScore)
        }
      }
    }

    return maxScore
  }

  /**
   * Calculate readiness score based on prerequisites
   */
  private calculateReadiness(
    skill: SkillTreeNode,
    completedSkills: Set<string>
  ): number {
    // Check if skill has prerequisites (parent must be completed)
    if (!skill.parent_id) {
      // Root skills are always ready
      return 1.0
    }

    // Check if parent is completed
    if (completedSkills.has(skill.parent_id)) {
      return 1.0
    }

    // Check how many ancestors are completed
    // This would need recursive checking in real implementation
    return 0.3 // Partial readiness if prerequisites not met
  }

  /**
   * Calculate interest match based on starred categories
   */
  private async calculateInterestMatch(
    skill: SkillTreeNode,
    starredSkills: string[]
  ): Promise<number> {
    if (starredSkills.includes(skill.id)) {
      return 1.0 // Direct match
    }

    // Check if skill is child of starred category
    if (skill.parent_id && starredSkills.includes(skill.parent_id)) {
      return 0.8
    }

    // Check category similarity
    const starredCategories = new Set<string>()
    for (const starredId of starredSkills) {
      const { data } = await supabase
        .from('skill_tree_nodes')
        .select('name, parent_id')
        .eq('id', starredId)
        .single()
      
      if (data) {
        // Use name as category indicator
        const nameParts = data.name.toLowerCase().split(/[\s-_]+/)
        nameParts.forEach((part: string) => starredCategories.add(part))
      }
    }

    // Check if skill name matches starred categories
    let score = 0
    const skillNameParts = skill.name.toLowerCase().split(/[\s-_]+/)
    const matchingParts = skillNameParts.filter((part: string) => starredCategories.has(part))
    score += Math.min(matchingParts.length * 0.3, 0.5)

    return Math.min(score, 1.0)
  }

  /**
   * Calculate difficulty fit based on user's current level
   */
  private calculateDifficultyFit(
    skillLevel: number | null,
    userRating: number
  ): number {
    const skillDifficulty = skillLevel || 5 // Default to medium
    const userLevel = Math.floor(userRating / 10) // Convert 0-100 to 0-10
    
    const difference = Math.abs(skillDifficulty - userLevel)
    
    if (difference <= 1) {
      return 1.0 // Perfect fit
    } else if (difference <= 2) {
      return 0.8 // Good fit
    } else if (difference <= 3) {
      return 0.5 // Moderate fit
    } else {
      return 0.2 // Poor fit
    }
  }

  /**
   * Calculate recency factor for spaced repetition
   */
  private calculateRecency(
    skillId: string,
    recentActivity: Array<{ skill_id: string; timestamp: string }>
  ): number {
    const lastActivity = recentActivity.find(a => a.skill_id === skillId)
    
    if (!lastActivity) {
      return 1.0 // Never accessed, high priority
    }

    const daysSince = (Date.now() - new Date(lastActivity.timestamp).getTime()) / (1000 * 60 * 60 * 24)
    
    if (daysSince < 1) {
      return 0.1 // Too recent
    } else if (daysSince < 7) {
      return 0.5 // Recent
    } else if (daysSince < 30) {
      return 0.8 // Good for review
    } else {
      return 1.0 // Needs review
    }
  }

  /**
   * Calculate path efficiency towards user goals
   */
  private async calculatePathEfficiency(
    skill: SkillTreeNode,
    userGoals: string[]
  ): Promise<number> {
    if (userGoals.length === 0) {
      return 0.5 // Neutral if no specific goals
    }

    // Check if skill is on path to any goal
    let maxEfficiency = 0

    for (const goalId of userGoals) {
      // Get goal node
      const { data: goalNode } = await supabase
        .from('skill_tree_nodes')
        .select('name, parent_id')
        .eq('id', goalId)
        .single()

      if (goalNode) {
        // Check if current skill is related to goal
        const goalName = goalNode.name.toLowerCase()
        const skillName = skill.name.toLowerCase()
        
        // Calculate name similarity
        const commonWords = skillName.split(/[\s-_]+/).filter((part: string) => 
          goalName.includes(part) && part.length > 3
        )
        
        const efficiency = commonWords.length > 0 ? 0.5 : 0
        maxEfficiency = Math.max(maxEfficiency, efficiency)
      }
    }

    return maxEfficiency
  }

  /**
   * Main recommendation calculation based on Zone of Proximal Development and user interests
   */
  async calculateRecommendationScore(
    skill: SkillTreeNode,
    userProfile: UserProfile
  ): Promise<number> {
    const completedSet = new Set(userProfile.completed_skills)
    
    // Calculate individual factors with updated weightings to prioritize interests
    const readiness = this.calculateReadiness(skill, completedSet) * 0.25
    const quizInterest = await this.calculateInterestScore(skill, userProfile.id) * 0.35 // Prioritize quiz interests
    const starredInterest = await this.calculateInterestMatch(skill, userProfile.starred_skills) * 0.15
    const difficultyFit = this.calculateDifficultyFit(
      skill.display_order, // Using display_order as difficulty proxy
      userProfile.overall_rating
    ) * 0.15
    const recency = this.calculateRecency(skill.id, userProfile.recent_activity) * 0.05
    const pathEfficiency = await this.calculatePathEfficiency(
      skill, 
      userProfile.starred_skills // Using starred as goals
    ) * 0.05

    return readiness + quizInterest + starredInterest + difficultyFit + recency + pathEfficiency
  }

  /**
   * Categorize recommendation based on characteristics
   */
  private categorizeRecommendation(
    skill: SkillTreeNode,
    score: number,
    userProfile: UserProfile,
    reasons: string[]
  ): 'ready_to_learn' | 'challenge' | 'review' | 'interest' | 'skill_gap' {
    const isCompleted = userProfile.completed_skills.includes(skill.id)
    const isInProgress = userProfile.in_progress_skills.includes(skill.id)
    const isStarred = userProfile.starred_skills.includes(skill.id)
    
    if (isCompleted) {
      return 'review'
    }
    
    if (isInProgress) {
      return 'ready_to_learn'
    }
    
    if (isStarred) {
      return 'interest'
    }
    
    // Check difficulty level
    const skillDifficulty = skill.display_order || 5
    const userLevel = Math.floor(userProfile.overall_rating / 10)
    
    if (skillDifficulty > userLevel + 2) {
      return 'challenge'
    }
    
    if (score > 0.7) {
      return 'ready_to_learn'
    }
    
    return 'skill_gap'
  }

  /**
   * Get personalized recommendations for a user
   */
  async getRecommendations(
    userId: string,
    settings: RecommendationSettings = {}
  ): Promise<RecommendationScore[]> {
    const {
      maxRecommendations = 10,
      includeCategories = [],
      excludeCompleted = true,
      focusOnStarred = false
    } = settings

    try {
      // Fetch user profile data
      const [profileResult, progressResult, starredResult, activityResult] = await Promise.allSettled([
        supabase.from('profiles').select('*').eq('id', userId).single(),
        supabase.from('user_progress').select('*').eq('user_id', userId),
        supabase.from('starred_items').select('item_id').eq('user_id', userId).eq('item_type', 'skill_node'),
        supabase.from('user_progress')
          .select('skill_id, last_accessed')
          .eq('user_id', userId)
          .order('last_accessed', { ascending: false })
          .limit(50)
      ])

      const userProfile: UserProfile = {
        id: userId,
        overall_rating: (profileResult.status === 'fulfilled' && profileResult.value.data?.overall_rating) || 50,
        starred_skills: (starredResult.status === 'fulfilled' && starredResult.value.data?.map((s: any) => s.item_id)) || [],
        completed_skills: (progressResult.status === 'fulfilled' && progressResult.value.data
          ?.filter((p: any) => p.status === 'completed')
          .map((p: any) => p.skill_id)) || [],
        in_progress_skills: (progressResult.status === 'fulfilled' && progressResult.value.data
          ?.filter((p: any) => p.status === 'in_progress')
          .map((p: any) => p.skill_id)) || [],
        recent_activity: (activityResult.status === 'fulfilled' && activityResult.value.data?.map((a: any) => ({
          skill_id: a.skill_id,
          timestamp: a.last_accessed
        }))) || []
      }

      // Fetch candidate nodes
      let nodesQuery = supabase
        .from('skill_tree_nodes')
        .select('*')
        .not('learning_content_ids', 'eq', '{}')

      if (includeCategories.length > 0) {
        // Since we don't have a type column, filter by name patterns
        // This is a workaround - ideally we'd have a category/type column
        // Note: This won't work with Supabase query builder, would need client-side filtering
        // For now, we'll skip this filter
      }

      if (excludeCompleted) {
        const excludedSkills = [...userProfile.completed_skills, ...userProfile.in_progress_skills]
        if (excludedSkills.length > 0) {
          nodesQuery = nodesQuery.not('id', 'in', `(${excludedSkills.join(',')})`)
        }
      }

      if (focusOnStarred && userProfile.starred_skills.length > 0) {
        // Get children of starred skills
        nodesQuery = nodesQuery.in('parent_id', userProfile.starred_skills)
      }

      const { data: candidateSkills, error } = await nodesQuery

      if (error) throw error
      if (!candidateSkills || candidateSkills.length === 0) return []

      // Calculate scores for all candidates
      const recommendations: RecommendationScore[] = []
      
      for (const skill of candidateSkills) {
        const score = await this.calculateRecommendationScore(skill, userProfile)
        
        const reasons: string[] = []
        
        // Determine reasons for recommendation
        const interestScore = await this.calculateInterestScore(skill, userProfile.id)
        if (interestScore > 0.6) {
          reasons.push('Matches your interests from the assessment')
        } else if (interestScore > 0.3) {
          reasons.push('Related to your learning preferences')
        }
        
        if (userProfile.starred_skills.includes(skill.parent_id || '')) {
          reasons.push('Related to your bookmarked topics')
        }
        
        if (skill.parent_id && userProfile.completed_skills.includes(skill.parent_id)) {
          reasons.push('Prerequisites completed')
        }
        
        const skillDifficulty = skill.display_order || 5
        const userLevel = Math.floor(userProfile.overall_rating / 10)
        if (Math.abs(skillDifficulty - userLevel) <= 1) {
          reasons.push('Matches your skill level')
        }
        
        const lastActivity = userProfile.recent_activity.find(a => a.skill_id === skill.id)
        if (lastActivity) {
          const daysSince = (Date.now() - new Date(lastActivity.timestamp).getTime()) / (1000 * 60 * 60 * 24)
          if (daysSince > 7) {
            reasons.push('Good time for review')
          }
        } else {
          reasons.push('New content to explore')
        }

        const category = this.categorizeRecommendation(skill, score, userProfile, reasons)
        
        recommendations.push({
          node: skill,
          score,
          category,
          reasons
        })
      }

      // Sort by score and return top recommendations
      recommendations.sort((a, b) => b.score - a.score)
      
      // Ensure variety in categories
      const categorizedRecommendations = this.ensureCategoryVariety(
        recommendations,
        maxRecommendations
      )

      return categorizedRecommendations
    } catch (error) {
      console.error('Error generating recommendations:', error)
      return []
    }
  }

  /**
   * Ensure variety in recommendation categories
   */
  private ensureCategoryVariety(
    recommendations: RecommendationScore[],
    maxCount: number
  ): RecommendationScore[] {
    const result: RecommendationScore[] = []
    const categoryQuotas = {
      'ready_to_learn': Math.ceil(maxCount * 0.4),
      'challenge': Math.ceil(maxCount * 0.2),
      'review': Math.ceil(maxCount * 0.2),
      'interest': Math.ceil(maxCount * 0.1),
      'skill_gap': Math.ceil(maxCount * 0.1)
    }

    const categoryCounts: Record<string, number> = {
      'ready_to_learn': 0,
      'challenge': 0,
      'review': 0,
      'interest': 0,
      'skill_gap': 0
    }

    // First pass: fill quotas
    for (const rec of recommendations) {
      if (result.length >= maxCount) break
      
      const quota = categoryQuotas[rec.category]
      const count = categoryCounts[rec.category]
      
      if (count < quota) {
        result.push(rec)
        categoryCounts[rec.category]++
      }
    }

    // Second pass: fill remaining slots with highest scores
    if (result.length < maxCount) {
      const remaining = recommendations.filter(r => !result.includes(r))
      remaining.sort((a, b) => b.score - a.score)
      
      for (const rec of remaining) {
        if (result.length >= maxCount) break
        result.push(rec)
      }
    }

    return result
  }

  /**
   * Get learning path to a specific goal
   */
  async getLearningPath(
    userId: string,
    goalSkillId: string
  ): Promise<SkillTreeNode[]> {
    try {
      // Get user's completed nodes
      const { data: progress } = await supabase
        .from('user_progress')
        .select('skill_id')
        .eq('user_id', userId)
        .eq('status', 'completed')

      const completedSet = new Set(progress?.map(p => p.skill_id) || [])

      // Get goal skill and its ancestors
      const { data: goalSkill } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('id', goalSkillId)
        .single()

      if (!goalSkill) return []

      // Build path from root to goal by traversing parent relationships
      const path: SkillTreeNode[] = []
      let currentSkill: SkillTreeNode | null = goalSkill
      const visitedSkills = new Set<string>()
      
      // Traverse from goal to root via parent_id
      while (currentSkill && !visitedSkills.has(currentSkill.id)) {
        visitedSkills.add(currentSkill.id)
        
        if (!completedSet.has(currentSkill.id)) {
          path.unshift(currentSkill) // Add to beginning to maintain root-to-goal order
        }
        
        // Get parent skill if exists
        if (currentSkill.parent_id) {
          const { data: parentSkill } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .eq('id', currentSkill.parent_id)
            .single()
          
          currentSkill = parentSkill
        } else {
          currentSkill = null
        }
      }

      return path
    } catch (error) {
      console.error('Error getting learning path:', error)
      return []
    }
  }
}

export const recommendationService = new RecommendationService()