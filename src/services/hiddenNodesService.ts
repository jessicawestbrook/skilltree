import { supabase } from './supabase'

export interface HiddenSkillConfig {
  hiddenSkills: string[]
  hiddenByDefault: string[]
  lastUpdated: string
  notes: string
}

class HiddenSkillsService {
  private hiddenSkillIds: Set<string> = new Set()
  private initialized: boolean = false
  private useDatabase: boolean = false

  constructor() {
    this.checkDatabaseColumn()
  }

  /**
   * Check if the database has the is_hidden column
   */
  private async checkDatabaseColumn(): Promise<void> {
    try {
      const { data, error } = await supabase
        .from('skill_tree_nodes')
        .select('id, is_hidden')
        .limit(1)

      if (!error && data) {
        // Column exists, use database
        this.useDatabase = true
        console.log('Using database for hidden nodes management')
      } else {
        // Column doesn't exist, fall back to local config
        this.useDatabase = false
        console.log('Using local config for hidden nodes (is_hidden column not found)')
        this.loadLocalConfig()
      }
      this.initialized = true
    } catch (error) {
      console.error('Error checking database column:', error)
      this.useDatabase = false
      this.loadLocalConfig()
      this.initialized = true
    }
  }

  /**
   * Load from local config file (fallback)
   */
  private loadLocalConfig() {
    try {
      // Try to load from local config if it exists
      const config = localStorage.getItem('hiddenSkills')
      if (config) {
        const parsed = JSON.parse(config)
        this.hiddenSkillIds = new Set(parsed.hiddenSkills || [])
      }
    } catch (error) {
      console.error('Error loading local config:', error)
      this.hiddenSkillIds = new Set()
    }
  }

  /**
   * Save to local storage (fallback)
   */
  private saveLocalConfig() {
    try {
      const config = {
        hiddenSkills: Array.from(this.hiddenSkillIds),
        lastUpdated: new Date().toISOString()
      }
      localStorage.setItem('hiddenSkills', JSON.stringify(config))
    } catch (error) {
      console.error('Error saving local config:', error)
    }
  }

  /**
   * Wait for initialization
   */
  private async ensureInitialized(): Promise<void> {
    if (!this.initialized) {
      await this.checkDatabaseColumn()
    }
  }

  /**
   * Check if a skill should be hidden
   */
  async isSkillHidden(skillId: string): Promise<boolean> {
    await this.ensureInitialized()

    if (this.useDatabase) {
      try {
        const { data, error } = await supabase
          .from('skill_tree_nodes')
          .select('is_hidden')
          .eq('id', skillId)
          .single()

        if (!error && data) {
          return data.is_hidden === true
        }
      } catch (error) {
        console.error('Error checking node visibility:', error)
      }
    }

    // Fallback to local storage
    return this.hiddenSkillIds.has(skillId)
  }

  /**
   * Get all hidden skill IDs
   */
  async getHiddenSkillIds(): Promise<string[]> {
    await this.ensureInitialized()

    if (this.useDatabase) {
      try {
        const { data, error } = await supabase
          .from('skill_tree_nodes')
          .select('id')
          .eq('is_hidden', true)

        if (!error && data) {
          return data.map(node => node.id)
        }
      } catch (error) {
        console.error('Error fetching hidden nodes:', error)
      }
    }

    // Fallback to local storage
    return Array.from(this.hiddenSkillIds)
  }

  /**
   * Filter out hidden skills from a list
   */
  async filterVisibleSkills<T extends { id: string }>(skills: T[]): Promise<T[]> {
    await this.ensureInitialized()

    if (this.useDatabase) {
      // Get all hidden skill IDs in one query
      const hiddenIds = await this.getHiddenSkillIds()
      const hiddenSet = new Set(hiddenIds)
      return skills.filter(skill => !hiddenSet.has(skill.id))
    }

    // Fallback to local storage
    return skills.filter(skill => !this.hiddenSkillIds.has(skill.id))
  }

  /**
   * Synchronous version for immediate filtering (uses cached data)
   */
  filterVisibleSkillsSync<T extends { id: string }>(skills: T[]): T[] {
    if (!this.initialized) {
      // If not initialized, return all skills (safe default)
      return skills
    }

    if (this.useDatabase) {
      // For database mode, we need the async version
      console.warn('filterVisibleSkillsSync called but database mode is active. Some skills might not be filtered.')
      return skills
    }

    // Use local cache
    return skills.filter(skill => !this.hiddenSkillIds.has(skill.id))
  }

  /**
   * Check if any ancestor of a skill is hidden (which would hide this skill too)
   */
  async isSkillOrAncestorHidden(skillId: string): Promise<boolean> {
    await this.ensureInitialized()

    // First check if the skill itself is hidden
    if (await this.isSkillHidden(skillId)) {
      return true
    }

    // Check ancestors
    try {
      let currentId: string | null = skillId
      const visitedIds = new Set<string>()

      while (currentId) {
        // Prevent infinite loops
        if (visitedIds.has(currentId)) {
          break
        }
        visitedIds.add(currentId)

        // Check if current skill is hidden
        if (await this.isSkillHidden(currentId)) {
          return true
        }

        // Get parent
        const { data: node }: { data: { parent_id: string | null } | null } = await supabase
          .from('skill_tree_nodes')
          .select('parent_id')
          .eq('id', currentId)
          .single()

        if (!node) {
          break
        }

        currentId = node.parent_id
      }

      return false
    } catch (error) {
      console.error('Error checking ancestor visibility:', error)
      return false
    }
  }

  /**
   * Get all descendant IDs of a node (for hiding entire subtrees)
   */
  async getDescendantIds(skillId: string): Promise<string[]> {
    const descendants: string[] = []
    const queue: string[] = [skillId]
    const visited = new Set<string>()

    while (queue.length > 0) {
      const currentId = queue.shift()!
      
      if (visited.has(currentId)) {
        continue
      }
      visited.add(currentId)

      // Get children
      const { data: children } = await supabase
        .from('skill_tree_nodes')
        .select('id')
        .eq('parent_id', currentId)

      if (children) {
        for (const child of children) {
          descendants.push(child.id)
          queue.push(child.id)
        }
      }
    }

    return descendants
  }

  /**
   * Add a node to the hidden list (admin only)
   */
  async hideSkill(skillId: string, hideDescendants: boolean = true): Promise<void> {
    await this.ensureInitialized()

    const skillIds = [skillId]
    if (hideDescendants) {
      const descendants = await this.getDescendantIds(skillId)
      skillIds.push(...descendants)
    }

    if (this.useDatabase) {
      try {
        const { error } = await supabase
          .from('skill_tree_nodes')
          .update({ is_hidden: true })
          .in('id', skillIds)

        if (error) {
          console.error('Error hiding nodes:', error)
          // Fallback to local storage
          skillIds.forEach(id => this.hiddenSkillIds.add(id))
          this.saveLocalConfig()
        } else {
          console.log(`Hidden ${skillIds.length} skill(s)`)
        }
      } catch (error) {
        console.error('Error hiding nodes:', error)
        // Fallback to local storage
        skillIds.forEach(id => this.hiddenSkillIds.add(id))
        this.saveLocalConfig()
      }
    } else {
      // Use local storage
      skillIds.forEach(id => this.hiddenSkillIds.add(id))
      this.saveLocalConfig()
      console.log(`Hidden ${skillIds.length} skill(s) locally`)
    }
  }

  /**
   * Remove a skill from the hidden list (admin only)
   */
  async showSkill(skillId: string, showDescendants: boolean = true): Promise<void> {
    await this.ensureInitialized()

    const skillIds = [skillId]
    if (showDescendants) {
      const descendants = await this.getDescendantIds(skillId)
      skillIds.push(...descendants)
    }

    if (this.useDatabase) {
      try {
        const { error } = await supabase
          .from('skill_tree_nodes')
          .update({ is_hidden: false })
          .in('id', skillIds)

        if (error) {
          console.error('Error showing skills:', error)
          // Fallback to local storage
          skillIds.forEach(id => this.hiddenSkillIds.delete(id))
          this.saveLocalConfig()
        } else {
          console.log(`Shown ${skillIds.length} skill(s)`)
        }
      } catch (error) {
        console.error('Error showing nodes:', error)
        // Fallback to local storage
        skillIds.forEach(id => this.hiddenSkillIds.delete(id))
        this.saveLocalConfig()
      }
    } else {
      // Use local storage
      skillIds.forEach(id => this.hiddenSkillIds.delete(id))
      this.saveLocalConfig()
      console.log(`Shown ${skillIds.length} skill(s) locally`)
    }
  }

  /**
   * Toggle skill visibility (admin only)
   */
  async toggleSkillVisibility(skillId: string, includeDescendants: boolean = true): Promise<boolean> {
    if (await this.isSkillHidden(skillId)) {
      await this.showSkill(skillId, includeDescendants)
      return false // Now visible
    } else {
      await this.hideSkill(skillId, includeDescendants)
      return true // Now hidden
    }
  }

  /**
   * Filter skills to only include visible ones, considering parent visibility
   */
  async filterVisibleSkillsWithAncestors<T extends { id: string }>(skills: T[]): Promise<T[]> {
    const visibleSkills: T[] = []

    for (const skill of skills) {
      const isHidden = await this.isSkillOrAncestorHidden(skill.id)
      if (!isHidden) {
        visibleSkills.push(skill)
      }
    }

    return visibleSkills
  }

  /**
   * Check if database column exists (for UI display)
   */
  isUsingDatabase(): boolean {
    return this.useDatabase
  }
}

// Export singleton instance
export const hiddenSkillsService = new HiddenSkillsService()