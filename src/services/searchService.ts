import { supabase } from './supabase'

interface KnowledgeSkill {
  id: string
  parent_id: string | null
  title: string
  learning_area: string | null
  skill_type: string
  difficulty_level: number | null
  simple_content_id: string | null
  order_index: number
  created_at?: string
  updated_at?: string
}

interface SearchResult {
  skill: KnowledgeSkill
  score: number
  matchType: 'exact' | 'fuzzy' | 'semantic'
  highlights: {
    title?: string
    learning_area?: string
  }
}

interface SearchOptions {
  limit?: number
  threshold?: number
  searchIn?: ('title' | 'learning_area' | 'keywords')[]
  skillTypes?: string[]
}

class SearchService {
  private searchCache: Map<string, { results: SearchResult[], timestamp: number }> = new Map()
  private cacheTimeout = 5 * 60 * 1000 // 5 minutes
  
  // Levenshtein distance for fuzzy matching
  private levenshteinDistance(str1: string, str2: string): number {
    const m = str1.length
    const n = str2.length
    const dp: number[][] = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0))
    
    for (let i = 0; i <= m; i++) dp[i][0] = i
    for (let j = 0; j <= n; j++) dp[0][j] = j
    
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (str1[i - 1] === str2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1]
        } else {
          dp[i][j] = Math.min(
            dp[i - 1][j] + 1,    // deletion
            dp[i][j - 1] + 1,    // insertion
            dp[i - 1][j - 1] + 1 // substitution
          )
        }
      }
    }
    
    return dp[m][n]
  }
  
  // Calculate similarity score (0-1)
  private calculateSimilarity(str1: string, str2: string): number {
    const distance = this.levenshteinDistance(str1.toLowerCase(), str2.toLowerCase())
    const maxLength = Math.max(str1.length, str2.length)
    return 1 - (distance / maxLength)
  }
  
  // Extract keywords from text for semantic matching
  private extractKeywords(text: string): string[] {
    // Remove common stop words
    const stopWords = new Set([
      'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
      'in', 'with', 'to', 'for', 'of', 'as', 'from', 'by', 'that', 'this',
      'it', 'be', 'are', 'was', 'were', 'been', 'have', 'has', 'had',
      'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might'
    ])
    
    return text
      .toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2 && !stopWords.has(word))
  }
  
  // Semantic similarity using keyword overlap
  private semanticSimilarity(text1: string, text2: string): number {
    const keywords1 = new Set(this.extractKeywords(text1))
    const keywords2 = new Set(this.extractKeywords(text2))
    
    if (keywords1.size === 0 || keywords2.size === 0) return 0
    
    const intersection = new Set(Array.from(keywords1).filter(x => keywords2.has(x)))
    const union = new Set([...Array.from(keywords1), ...Array.from(keywords2)])
    
    // Jaccard similarity coefficient
    return intersection.size / union.size
  }
  
  // Highlight matching parts
  private highlightMatch(text: string, query: string): string {
    const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const regex = new RegExp(`(${escapedQuery})`, 'gi')
    return text.replace(regex, '<mark>$1</mark>')
  }
  
  // Main search function
  async search(query: string, options: SearchOptions = {}): Promise<SearchResult[]> {
    const {
      limit = 20,
      threshold = 0.3,
      searchIn = ['title', 'learning_area'],
      skillTypes = []
    } = options
    
    // Check cache
    const cacheKey = JSON.stringify({ query, options })
    const cached = this.searchCache.get(cacheKey)
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return cached.results
    }
    
    try {
      // Fetch all skills (with optional type filter)
      let skillsQuery = supabase.from('knowledge_skills').select('*')
      
      if (skillTypes.length > 0) {
        skillsQuery = skillsQuery.in('skill_type', skillTypes)
      }
      
      const { data: skills, error } = await skillsQuery
      
      if (error) throw error
      if (!skills) return []
      
      const results: SearchResult[] = []
      const queryLower = query.toLowerCase()
      // const queryKeywords = this.extractKeywords(query)
      
      for (const skill of skills) {
        let bestScore = 0
        let matchType: 'exact' | 'fuzzy' | 'semantic' = 'fuzzy'
        const highlights: { title?: string, learning_area?: string } = {}
        
        // Search in title
        if (searchIn.includes('title') && skill.title) {
          const titleLower = skill.title.toLowerCase()
          
          // Exact match
          if (titleLower.includes(queryLower)) {
            bestScore = Math.max(bestScore, 1.0)
            matchType = 'exact'
            highlights.title = this.highlightMatch(skill.title, query)
          } else {
            // Fuzzy match
            const fuzzyScore = this.calculateSimilarity(query, skill.title)
            if (fuzzyScore > bestScore) {
              bestScore = fuzzyScore
              matchType = 'fuzzy'
              highlights.title = skill.title
            }
            
            // Semantic match
            const semanticScore = this.semanticSimilarity(query, skill.title) * 0.8
            if (semanticScore > bestScore) {
              bestScore = semanticScore
              matchType = 'semantic'
              highlights.title = skill.title
            }
          }
        }
        
        // Search in learning_area
        if (searchIn.includes('learning_area') && skill.learning_area) {
          const areaLower = skill.learning_area.toLowerCase()
          
          // Exact match in learning_area (lower weight than title)
          if (areaLower.includes(queryLower)) {
            const score = 0.7
            if (score > bestScore) {
              bestScore = score
              matchType = 'exact'
              highlights.learning_area = this.highlightMatch(skill.learning_area, query)
            }
          } else {
            // Semantic match in learning_area
            const semanticScore = this.semanticSimilarity(query, skill.learning_area) * 0.6
            if (semanticScore > bestScore) {
              bestScore = semanticScore
              matchType = 'semantic'
              highlights.learning_area = skill.learning_area.substring(0, 150) + '...'
            }
          }
        }
        
        // Add to results if score meets threshold
        if (bestScore >= threshold) {
          results.push({
            skill,
            score: bestScore,
            matchType,
            highlights
          })
        }
      }
      
      // Sort by score (highest first)
      results.sort((a, b) => b.score - a.score)
      
      // Limit results
      const limitedResults = results.slice(0, limit)
      
      // Cache results
      this.searchCache.set(cacheKey, {
        results: limitedResults,
        timestamp: Date.now()
      })
      
      // Clean old cache entries
      this.cleanCache()
      
      return limitedResults
    } catch (error) {
      console.error('Search error:', error)
      return []
    }
  }
  
  // Search suggestions (autocomplete)
  async getSuggestions(prefix: string, limit: number = 5): Promise<string[]> {
    try {
      const { data: skills, error } = await supabase
        .from('knowledge_skills')
        .select('title')
        .ilike('title', `${prefix}%`)
        .limit(limit)
      
      if (error) throw error
      
      return skills?.map(s => s.title) || []
    } catch (error) {
      console.error('Suggestions error:', error)
      return []
    }
  }
  
  // Advanced search with multiple criteria
  async advancedSearch(criteria: {
    query?: string
    skillTypes?: string[]
    parentId?: string
    minDifficulty?: number
    maxDifficulty?: number
    hasContent?: boolean
    isComplete?: boolean
  }): Promise<KnowledgeSkill[]> {
    try {
      let query = supabase.from('knowledge_skills').select('*')
      
      if (criteria.skillTypes?.length) {
        query = query.in('skill_type', criteria.skillTypes)
      }
      
      if (criteria.parentId) {
        query = query.eq('parent_id', criteria.parentId)
      }
      
      if (criteria.minDifficulty !== undefined) {
        query = query.gte('difficulty_level', criteria.minDifficulty)
      }
      
      if (criteria.maxDifficulty !== undefined) {
        query = query.lte('difficulty_level', criteria.maxDifficulty)
      }
      
      if (criteria.hasContent !== undefined) {
        if (criteria.hasContent) {
          query = query.not('simple_content_id', 'is', null)
        } else {
          query = query.is('simple_content_id', null)
        }
      }
      
      const { data: skills, error } = await query
      
      if (error) throw error
      if (!skills) return []
      
      // Apply text search if query provided
      if (criteria.query) {
        const searchResults = await this.search(criteria.query, {
          limit: 1000,
          threshold: 0.3
        })
        
        const skillIds = new Set(searchResults.map(r => r.skill.id))
        return skills.filter(s => skillIds.has(s.id))
      }
      
      return skills
    } catch (error) {
      console.error('Advanced search error:', error)
      return []
    }
  }
  
  // Clean expired cache entries
  private cleanCache() {
    const now = Date.now()
    for (const [key, value] of Array.from(this.searchCache.entries())) {
      if (now - value.timestamp > this.cacheTimeout) {
        this.searchCache.delete(key)
      }
    }
  }
  
  // Search questions
  async searchQuestions(query: string, limit: number = 20): Promise<any[]> {
    try {
      const queryLower = query.toLowerCase()
      
      // First try exact match in question text
      const { data: exactMatches, error: exactError } = await supabase
        .from('questions')
        .select('*')
        .ilike('question_text', `%${query}%`)
        .limit(limit)
      
      if (exactError) throw exactError
      
      // Also search in options (answers)
      const { data: allQuestions, error: allError } = await supabase
        .from('questions')
        .select('*')
        .limit(1000) // Get a reasonable sample
      
      if (allError) throw allError
      
      const optionMatches = allQuestions?.filter(q => {
        // Check if any option contains the query
        return q.options?.some((opt: string) => 
          opt.toLowerCase().includes(queryLower)
        )
      }) || []
      
      // Combine and deduplicate results
      const combinedResults = new Map()
      exactMatches?.forEach(q => combinedResults.set(q.id, q))
      optionMatches.forEach(q => combinedResults.set(q.id, q))
      
      return Array.from(combinedResults.values()).slice(0, limit)
    } catch (error) {
      console.error('Error searching questions:', error)
      return []
    }
  }
  
  // Search learning content
  async searchLearningContent(query: string, limit: number = 20): Promise<any[]> {
    try {
      // const queryLower = query.toLowerCase()
      
      // Search in learning_content table
      const { data: contentResults, error: contentError } = await supabase
        .from('learning_content')
        .select('*')
        .or(`title.ilike.%${query}%,content.ilike.%${query}%,summary.ilike.%${query}%`)
        .limit(limit)
      
      if (contentError) throw contentError
      
      // Also get skill nodes that have learning content matching the query
      const { data: nodeResults, error: nodeError } = await supabase
        .from('skill_tree_nodes')
        .select('*, learning_content(*)')
        .not('learning_content_ids', 'eq', '{}')
        .or(`name.ilike.%${query}%,learning_area.ilike.%${query}%`)
        .limit(limit)
      
      if (nodeError) throw nodeError
      
      // Combine results
      const results = []
      
      // Add direct content matches
      if (contentResults) {
        results.push(...contentResults.map(content => ({
          type: 'content',
          data: content,
          matchIn: 'content'
        })))
      }
      
      // Add node matches with content
      if (nodeResults) {
        results.push(...nodeResults.map(node => ({
          type: 'node_with_content',
          data: node,
          matchIn: 'node'
        })))
      }
      
      return results.slice(0, limit)
    } catch (error) {
      console.error('Error searching learning content:', error)
      return []
    }
  }
  
  // Unified search across all content types
  async searchAll(query: string, options: {
    includeNodes?: boolean
    includeQuestions?: boolean
    includeContent?: boolean
    limit?: number
  } = {}): Promise<any> {
    const {
      includeNodes = true,
      includeQuestions = true,
      includeContent = true,
      limit = 20
    } = options
    
    const results: any = {
      skills: [],
      questions: [],
      learningContent: []
    }
    
    // Search in parallel for better performance
    const promises = []
    
    if (includeNodes) {
      promises.push(
        this.search(query, { limit }).then(r => {
          results.skills = r
        })
      )
    }
    
    if (includeQuestions) {
      promises.push(
        this.searchQuestions(query, limit).then(r => {
          results.questions = r
        })
      )
    }
    
    if (includeContent) {
      promises.push(
        this.searchLearningContent(query, limit).then(r => {
          results.learningContent = r
        })
      )
    }
    
    await Promise.all(promises)
    
    return results
  }
  
  // Clear all cache
  clearCache() {
    this.searchCache.clear()
  }
}

export const searchService = new SearchService()
export type { SearchResult, SearchOptions, KnowledgeSkill }