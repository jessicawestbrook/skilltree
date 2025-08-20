import { supabase } from './supabase'
import { SkillTreeNode } from '../types/database.types'

export interface RecommendationScore {
  node: SkillTreeNode
  score: number
  category: 'ready_to_learn' | 'challenge' | 'review' | 'interest' | 'skill_gap'
  reasons: string[]
}

export interface UserProfile {
  id: string
  overall_rating: number
  starred_nodes: string[]
  completed_nodes: string[]
  in_progress_nodes: string[]
  recent_activity: Array<{
    node_id: string
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
   * Calculate readiness score based on prerequisites
   */
  private calculateReadiness(
    node: SkillTreeNode,
    completedNodes: Set<string>
  ): number {
    // Check if node has prerequisites (parent must be completed)
    if (!node.parent_id) {
      // Root nodes are always ready
      return 1.0
    }

    // Check if parent is completed
    if (completedNodes.has(node.parent_id)) {
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
    node: SkillTreeNode,
    starredNodes: string[]
  ): Promise<number> {
    if (starredNodes.includes(node.id)) {
      return 1.0 // Direct match
    }

    // Check if node is child of starred category
    if (node.parent_id && starredNodes.includes(node.parent_id)) {
      return 0.8
    }

    // Check category similarity
    const starredCategories = new Set<string>()
    for (const starredId of starredNodes) {
      const { data } = await supabase
        .from('skill_tree_nodes')
        .select('type, path')
        .eq('id', starredId)
        .single()
      
      if (data) {
        starredCategories.add(data.type)
        // Add path components as interests
        const pathParts = data.path?.split('/') || []
        pathParts.forEach((part: string) => starredCategories.add(part))
      }
    }

    // Check if node's type or path matches starred categories
    let score = 0
    if (starredCategories.has(node.type)) {
      score += 0.5
    }
    
    const nodePath = node.path?.split('/') || []
    const matchingPaths = nodePath.filter(part => starredCategories.has(part))
    score += (matchingPaths.length / nodePath.length) * 0.5

    return Math.min(score, 1.0)
  }

  /**
   * Calculate difficulty fit based on user's current level
   */
  private calculateDifficultyFit(
    nodeLevel: number | null,
    userRating: number
  ): number {
    const nodeDifficulty = nodeLevel || 5 // Default to medium
    const userLevel = Math.floor(userRating / 10) // Convert 0-100 to 0-10
    
    const difference = Math.abs(nodeDifficulty - userLevel)
    
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
    nodeId: string,
    recentActivity: Array<{ node_id: string; timestamp: string }>
  ): number {
    const lastActivity = recentActivity.find(a => a.node_id === nodeId)
    
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
    node: SkillTreeNode,
    userGoals: string[]
  ): Promise<number> {
    if (userGoals.length === 0) {
      return 0.5 // Neutral if no specific goals
    }

    // Check if node is on path to any goal
    let maxEfficiency = 0

    for (const goalId of userGoals) {
      // Get goal node
      const { data: goalNode } = await supabase
        .from('skill_tree_nodes')
        .select('path')
        .eq('id', goalId)
        .single()

      if (goalNode) {
        // Check if current node is on path to goal
        const goalPath = goalNode.path?.split('/') || []
        const nodePath = node.path?.split('/') || []
        
        // Calculate path overlap
        const commonPath = nodePath.filter((part, index) => 
          index < goalPath.length && goalPath[index] === part
        )
        
        const efficiency = commonPath.length / Math.max(nodePath.length, 1)
        maxEfficiency = Math.max(maxEfficiency, efficiency)
      }
    }

    return maxEfficiency
  }

  /**
   * Main recommendation calculation based on Zone of Proximal Development
   */
  async calculateRecommendationScore(
    node: SkillTreeNode,
    userProfile: UserProfile
  ): Promise<number> {
    const completedSet = new Set(userProfile.completed_nodes)
    
    // Calculate individual factors
    const readiness = this.calculateReadiness(node, completedSet) * 0.35
    const interest = await this.calculateInterestMatch(node, userProfile.starred_nodes) * 0.25
    const difficultyFit = this.calculateDifficultyFit(
      node.display_order, // Using display_order as difficulty proxy
      userProfile.overall_rating
    ) * 0.20
    const recency = this.calculateRecency(node.id, userProfile.recent_activity) * 0.10
    const pathEfficiency = await this.calculatePathEfficiency(
      node, 
      userProfile.starred_nodes // Using starred as goals
    ) * 0.10

    return readiness + interest + difficultyFit + recency + pathEfficiency
  }

  /**
   * Categorize recommendation based on characteristics
   */
  private categorizeRecommendation(
    node: SkillTreeNode,
    score: number,
    userProfile: UserProfile,
    reasons: string[]
  ): 'ready_to_learn' | 'challenge' | 'review' | 'interest' | 'skill_gap' {
    const isCompleted = userProfile.completed_nodes.includes(node.id)
    const isInProgress = userProfile.in_progress_nodes.includes(node.id)
    const isStarred = userProfile.starred_nodes.includes(node.id)
    
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
    const nodeDifficulty = node.display_order || 5
    const userLevel = Math.floor(userProfile.overall_rating / 10)
    
    if (nodeDifficulty > userLevel + 2) {
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
        supabase.from('user_starred_nodes').select('skill_node_id').eq('user_id', userId),
        supabase.from('user_progress')
          .select('skill_node_id, last_accessed')
          .eq('user_id', userId)
          .order('last_accessed', { ascending: false })
          .limit(50)
      ])

      const userProfile: UserProfile = {
        id: userId,
        overall_rating: (profileResult.status === 'fulfilled' && profileResult.value.data?.overall_rating) || 50,
        starred_nodes: (starredResult.status === 'fulfilled' && starredResult.value.data?.map((s: any) => s.skill_node_id)) || [],
        completed_nodes: (progressResult.status === 'fulfilled' && progressResult.value.data
          ?.filter((p: any) => p.status === 'completed')
          .map((p: any) => p.skill_node_id)) || [],
        in_progress_nodes: (progressResult.status === 'fulfilled' && progressResult.value.data
          ?.filter((p: any) => p.status === 'in_progress')
          .map((p: any) => p.skill_node_id)) || [],
        recent_activity: (activityResult.status === 'fulfilled' && activityResult.value.data?.map((a: any) => ({
          node_id: a.skill_node_id,
          timestamp: a.last_accessed
        }))) || []
      }

      // Fetch candidate nodes
      let nodesQuery = supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('has_learning_content', true)

      if (includeCategories.length > 0) {
        nodesQuery = nodesQuery.in('type', includeCategories)
      }

      if (excludeCompleted) {
        nodesQuery = nodesQuery.not('id', 'in', `(${userProfile.completed_nodes.join(',')})`)
      }

      if (focusOnStarred && userProfile.starred_nodes.length > 0) {
        // Get children of starred nodes
        nodesQuery = nodesQuery.in('parent_id', userProfile.starred_nodes)
      }

      const { data: candidateNodes, error } = await nodesQuery

      if (error) throw error
      if (!candidateNodes || candidateNodes.length === 0) return []

      // Calculate scores for all candidates
      const recommendations: RecommendationScore[] = []
      
      for (const node of candidateNodes) {
        const score = await this.calculateRecommendationScore(node, userProfile)
        
        const reasons: string[] = []
        
        // Determine reasons for recommendation
        if (userProfile.starred_nodes.includes(node.parent_id || '')) {
          reasons.push('Related to your interests')
        }
        
        if (node.parent_id && userProfile.completed_nodes.includes(node.parent_id)) {
          reasons.push('Prerequisites completed')
        }
        
        const nodeDifficulty = node.display_order || 5
        const userLevel = Math.floor(userProfile.overall_rating / 10)
        if (Math.abs(nodeDifficulty - userLevel) <= 1) {
          reasons.push('Matches your skill level')
        }
        
        const lastActivity = userProfile.recent_activity.find(a => a.node_id === node.id)
        if (lastActivity) {
          const daysSince = (Date.now() - new Date(lastActivity.timestamp).getTime()) / (1000 * 60 * 60 * 24)
          if (daysSince > 7) {
            reasons.push('Good time for review')
          }
        } else {
          reasons.push('New content to explore')
        }

        const category = this.categorizeRecommendation(node, score, userProfile, reasons)
        
        recommendations.push({
          node,
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
    goalNodeId: string
  ): Promise<SkillTreeNode[]> {
    try {
      // Get user's completed nodes
      const { data: progress } = await supabase
        .from('user_progress')
        .select('skill_node_id')
        .eq('user_id', userId)
        .eq('status', 'completed')

      const completedSet = new Set(progress?.map(p => p.skill_node_id) || [])

      // Get goal node and its ancestors
      const { data: goalNode } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('id', goalNodeId)
        .single()

      if (!goalNode) return []

      // Build path from root to goal
      const path: SkillTreeNode[] = []
      const pathComponents = goalNode.path?.split('/') || []
      
      // Get all nodes in the path
      for (let i = 0; i < pathComponents.length; i++) {
        const partialPath = pathComponents.slice(0, i + 1).join('/')
        
        const { data: pathNode } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .eq('path', partialPath)
          .single()

        if (pathNode && !completedSet.has(pathNode.id)) {
          path.push(pathNode)
        }
      }

      // Add goal node if not completed
      if (!completedSet.has(goalNode.id)) {
        path.push(goalNode)
      }

      return path
    } catch (error) {
      console.error('Error getting learning path:', error)
      return []
    }
  }
}

export const recommendationService = new RecommendationService()