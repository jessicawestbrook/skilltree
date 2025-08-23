import { supabase } from './supabase'

export interface HiddenNodeConfig {
  hiddenNodes: string[]
  hiddenByDefault: string[]
  lastUpdated: string
  notes: string
}

class HiddenNodesService {
  private hiddenNodeIds: Set<string> = new Set()
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
      const config = localStorage.getItem('hiddenNodes')
      if (config) {
        const parsed = JSON.parse(config)
        this.hiddenNodeIds = new Set(parsed.hiddenNodes || [])
      }
    } catch (error) {
      console.error('Error loading local config:', error)
      this.hiddenNodeIds = new Set()
    }
  }

  /**
   * Save to local storage (fallback)
   */
  private saveLocalConfig() {
    try {
      const config = {
        hiddenNodes: Array.from(this.hiddenNodeIds),
        lastUpdated: new Date().toISOString()
      }
      localStorage.setItem('hiddenNodes', JSON.stringify(config))
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
   * Check if a node should be hidden
   */
  async isNodeHidden(nodeId: string): Promise<boolean> {
    await this.ensureInitialized()

    if (this.useDatabase) {
      try {
        const { data, error } = await supabase
          .from('skill_tree_nodes')
          .select('is_hidden')
          .eq('id', nodeId)
          .single()

        if (!error && data) {
          return data.is_hidden === true
        }
      } catch (error) {
        console.error('Error checking node visibility:', error)
      }
    }

    // Fallback to local storage
    return this.hiddenNodeIds.has(nodeId)
  }

  /**
   * Get all hidden node IDs
   */
  async getHiddenNodeIds(): Promise<string[]> {
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
    return Array.from(this.hiddenNodeIds)
  }

  /**
   * Filter out hidden nodes from a list
   */
  async filterVisibleNodes<T extends { id: string }>(nodes: T[]): Promise<T[]> {
    await this.ensureInitialized()

    if (this.useDatabase) {
      // Get all hidden node IDs in one query
      const hiddenIds = await this.getHiddenNodeIds()
      const hiddenSet = new Set(hiddenIds)
      return nodes.filter(node => !hiddenSet.has(node.id))
    }

    // Fallback to local storage
    return nodes.filter(node => !this.hiddenNodeIds.has(node.id))
  }

  /**
   * Synchronous version for immediate filtering (uses cached data)
   */
  filterVisibleNodesSync<T extends { id: string }>(nodes: T[]): T[] {
    if (!this.initialized) {
      // If not initialized, return all nodes (safe default)
      return nodes
    }

    if (this.useDatabase) {
      // For database mode, we need the async version
      console.warn('filterVisibleNodesSync called but database mode is active. Some nodes might not be filtered.')
      return nodes
    }

    // Use local cache
    return nodes.filter(node => !this.hiddenNodeIds.has(node.id))
  }

  /**
   * Check if any ancestor of a node is hidden (which would hide this node too)
   */
  async isNodeOrAncestorHidden(nodeId: string): Promise<boolean> {
    await this.ensureInitialized()

    // First check if the node itself is hidden
    if (await this.isNodeHidden(nodeId)) {
      return true
    }

    // Check ancestors
    try {
      let currentId: string | null = nodeId
      const visitedIds = new Set<string>()

      while (currentId) {
        // Prevent infinite loops
        if (visitedIds.has(currentId)) {
          break
        }
        visitedIds.add(currentId)

        // Check if current node is hidden
        if (await this.isNodeHidden(currentId)) {
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
  async getDescendantIds(nodeId: string): Promise<string[]> {
    const descendants: string[] = []
    const queue: string[] = [nodeId]
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
  async hideNode(nodeId: string, hideDescendants: boolean = true): Promise<void> {
    await this.ensureInitialized()

    const nodeIds = [nodeId]
    if (hideDescendants) {
      const descendants = await this.getDescendantIds(nodeId)
      nodeIds.push(...descendants)
    }

    if (this.useDatabase) {
      try {
        const { error } = await supabase
          .from('skill_tree_nodes')
          .update({ is_hidden: true })
          .in('id', nodeIds)

        if (error) {
          console.error('Error hiding nodes:', error)
          // Fallback to local storage
          nodeIds.forEach(id => this.hiddenNodeIds.add(id))
          this.saveLocalConfig()
        } else {
          console.log(`Hidden ${nodeIds.length} node(s)`)
        }
      } catch (error) {
        console.error('Error hiding nodes:', error)
        // Fallback to local storage
        nodeIds.forEach(id => this.hiddenNodeIds.add(id))
        this.saveLocalConfig()
      }
    } else {
      // Use local storage
      nodeIds.forEach(id => this.hiddenNodeIds.add(id))
      this.saveLocalConfig()
      console.log(`Hidden ${nodeIds.length} node(s) locally`)
    }
  }

  /**
   * Remove a node from the hidden list (admin only)
   */
  async showNode(nodeId: string, showDescendants: boolean = true): Promise<void> {
    await this.ensureInitialized()

    const nodeIds = [nodeId]
    if (showDescendants) {
      const descendants = await this.getDescendantIds(nodeId)
      nodeIds.push(...descendants)
    }

    if (this.useDatabase) {
      try {
        const { error } = await supabase
          .from('skill_tree_nodes')
          .update({ is_hidden: false })
          .in('id', nodeIds)

        if (error) {
          console.error('Error showing nodes:', error)
          // Fallback to local storage
          nodeIds.forEach(id => this.hiddenNodeIds.delete(id))
          this.saveLocalConfig()
        } else {
          console.log(`Shown ${nodeIds.length} node(s)`)
        }
      } catch (error) {
        console.error('Error showing nodes:', error)
        // Fallback to local storage
        nodeIds.forEach(id => this.hiddenNodeIds.delete(id))
        this.saveLocalConfig()
      }
    } else {
      // Use local storage
      nodeIds.forEach(id => this.hiddenNodeIds.delete(id))
      this.saveLocalConfig()
      console.log(`Shown ${nodeIds.length} node(s) locally`)
    }
  }

  /**
   * Toggle node visibility (admin only)
   */
  async toggleNodeVisibility(nodeId: string, includeDescendants: boolean = true): Promise<boolean> {
    if (await this.isNodeHidden(nodeId)) {
      await this.showNode(nodeId, includeDescendants)
      return false // Now visible
    } else {
      await this.hideNode(nodeId, includeDescendants)
      return true // Now hidden
    }
  }

  /**
   * Filter nodes to only include visible ones, considering parent visibility
   */
  async filterVisibleNodesWithAncestors<T extends { id: string }>(nodes: T[]): Promise<T[]> {
    const visibleNodes: T[] = []

    for (const node of nodes) {
      const isHidden = await this.isNodeOrAncestorHidden(node.id)
      if (!isHidden) {
        visibleNodes.push(node)
      }
    }

    return visibleNodes
  }

  /**
   * Check if database column exists (for UI display)
   */
  isUsingDatabase(): boolean {
    return this.useDatabase
  }
}

// Export singleton instance
export const hiddenNodesService = new HiddenNodesService()