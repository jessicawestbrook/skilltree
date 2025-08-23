import React, { useState, useEffect } from 'react'
import { supabase } from '../services/supabase'
import { hiddenNodesService } from '../services/hiddenNodesService'
import { SkillTreeNode } from '../types/database.types'
import { 
  EyeIcon, 
  EyeSlashIcon, 
  MagnifyingGlassIcon,
  ArrowPathIcon,
  ChevronRightIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline'

const HiddenNodesManager: React.FC = () => {
  const [nodes, setNodes] = useState<SkillTreeNode[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set())
  const [hiddenNodes, setHiddenNodes] = useState<Set<string>>(new Set())
  const [nodeChildren, setNodeChildren] = useState<Record<string, SkillTreeNode[]>>({})
  const [filterMode, setFilterMode] = useState<'all' | 'visible' | 'hidden'>('all')

  useEffect(() => {
    fetchNodes()
  }, [])

  const fetchNodes = async () => {
    try {
      setLoading(true)
      
      // Fetch all top-level nodes
      const { data: topNodes, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .is('parent_id', null)
        .order('display_order', { nullsFirst: false })
        .order('name')

      if (error) throw error

      setNodes(topNodes || [])
      
      // Initialize hidden nodes from service
      const hiddenIds = await hiddenNodesService.getHiddenNodeIds()
      setHiddenNodes(new Set(hiddenIds))
      
      // Pre-fetch children for all top nodes
      const childrenMap: Record<string, SkillTreeNode[]> = {}
      for (const node of topNodes || []) {
        const { data: children } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .eq('parent_id', node.id)
          .order('display_order', { nullsFirst: false })
          .order('name')
        
        if (children && children.length > 0) {
          childrenMap[node.id] = children
        }
      }
      setNodeChildren(childrenMap)
      
    } catch (error) {
      console.error('Error fetching nodes:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchChildren = async (nodeId: string) => {
    if (nodeChildren[nodeId]) return // Already fetched

    try {
      const { data: children, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('parent_id', nodeId)
        .order('display_order', { nullsFirst: false })
        .order('name')

      if (error) throw error

      setNodeChildren(prev => ({
        ...prev,
        [nodeId]: children || []
      }))

      // Fetch grandchildren for each child
      for (const child of children || []) {
        const { data: grandchildren } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .eq('parent_id', child.id)
          .order('display_order', { nullsFirst: false })
          .order('name')
        
        if (grandchildren && grandchildren.length > 0) {
          setNodeChildren(prev => ({
            ...prev,
            [child.id]: grandchildren
          }))
        }
      }
    } catch (error) {
      console.error('Error fetching children:', error)
    }
  }

  const toggleNodeVisibility = async (nodeId: string, includeDescendants: boolean = true) => {
    const isHidden = await hiddenNodesService.toggleNodeVisibility(nodeId, includeDescendants)
    
    // Update local state
    setHiddenNodes(prev => {
      const newSet = new Set(prev)
      if (isHidden) {
        newSet.add(nodeId)
        if (includeDescendants) {
          // Add all descendants
          const addDescendants = (id: string) => {
            const children = nodeChildren[id] || []
            children.forEach(child => {
              newSet.add(child.id)
              addDescendants(child.id)
            })
          }
          addDescendants(nodeId)
        }
      } else {
        newSet.delete(nodeId)
        if (includeDescendants) {
          // Remove all descendants
          const removeDescendants = (id: string) => {
            const children = nodeChildren[id] || []
            children.forEach(child => {
              newSet.delete(child.id)
              removeDescendants(child.id)
            })
          }
          removeDescendants(nodeId)
        }
      }
      return newSet
    })
    
    // Save to config file (in production, this would save to database)
    console.log('Updated hidden nodes:', Array.from(hiddenNodes))
  }

  const toggleExpanded = (nodeId: string) => {
    setExpandedNodes(prev => {
      const newSet = new Set(prev)
      if (newSet.has(nodeId)) {
        newSet.delete(nodeId)
      } else {
        newSet.add(nodeId)
        fetchChildren(nodeId)
      }
      return newSet
    })
  }

  const filteredNodes = nodes.filter(node => {
    // Filter by search term
    if (searchTerm && !node.name.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false
    }
    
    // Filter by visibility mode
    if (filterMode === 'hidden' && !hiddenNodes.has(node.id)) {
      return false
    }
    if (filterMode === 'visible' && hiddenNodes.has(node.id)) {
      return false
    }
    
    return true
  })

  const renderNode = (node: SkillTreeNode, level: number = 0) => {
    const children = nodeChildren[node.id] || []
    const hasChildren = children.length > 0
    const isExpanded = expandedNodes.has(node.id)
    const isHidden = hiddenNodes.has(node.id)
    const isCategory = !node.learning_content_ids || node.learning_content_ids.length === 0

    return (
      <div key={node.id} className={`${level > 0 ? 'ml-6' : ''}`}>
        <div className={`flex items-center gap-2 p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 ${
          isHidden ? 'opacity-50' : ''
        }`}>
          {hasChildren && (
            <button
              onClick={() => toggleExpanded(node.id)}
              className="p-1 hover:bg-neutral-200 dark:hover:bg-neutral-600 rounded"
            >
              {isExpanded ? (
                <ChevronDownIcon className="h-4 w-4" />
              ) : (
                <ChevronRightIcon className="h-4 w-4" />
              )}
            </button>
          )}
          {!hasChildren && <div className="w-6" />}
          
          <div className="flex-1">
            <span className={`text-sm font-medium ${isCategory ? 'text-primary-600' : 'text-neutral-700 dark:text-neutral-300'}`}>
              {node.name}
            </span>
            {isCategory && (
              <span className="ml-2 text-xs text-blue-500">
                Category
              </span>
            )}
          </div>
          
          <button
            onClick={() => toggleNodeVisibility(node.id, true)}
            className={`p-2 rounded-lg transition-colors ${
              isHidden 
                ? 'bg-red-100 text-red-600 hover:bg-red-200 dark:bg-red-900/30 dark:text-red-400 dark:hover:bg-red-900/50' 
                : 'bg-green-100 text-green-600 hover:bg-green-200 dark:bg-green-900/30 dark:text-green-400 dark:hover:bg-green-900/50'
            }`}
            title={isHidden ? 'Show this node and its children' : 'Hide this node and its children'}
          >
            {isHidden ? (
              <EyeSlashIcon className="h-4 w-4" />
            ) : (
              <EyeIcon className="h-4 w-4" />
            )}
          </button>
        </div>
        
        {isExpanded && children.length > 0 && (
          <div className="mt-1">
            {children.map(child => renderNode(child, level + 1))}
          </div>
        )}
      </div>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {!hiddenNodesService.isUsingDatabase() && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
          <p className="text-sm text-yellow-800 dark:text-yellow-200">
            <strong>Note:</strong> Hidden nodes configuration is currently stored locally. 
            To persist changes, add the is_hidden column to the database.
          </p>
        </div>
      )}
      
      {hiddenNodesService.isUsingDatabase() && (
        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <p className="text-sm text-green-800 dark:text-green-200">
            <strong>✓ Database Mode:</strong> Changes are saved to the database and will persist.
          </p>
        </div>
      )}

      <div className="flex items-center gap-4">
        <div className="flex-1 relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-neutral-400" />
          <input
            type="text"
            placeholder="Search nodes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
          />
        </div>
        
        <select
          value={filterMode}
          onChange={(e) => setFilterMode(e.target.value as any)}
          className="px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800"
        >
          <option value="all">All Nodes</option>
          <option value="visible">Visible Only</option>
          <option value="hidden">Hidden Only</option>
        </select>
        
        <button
          onClick={fetchNodes}
          className="p-2 rounded-lg bg-neutral-100 hover:bg-neutral-200 dark:bg-neutral-700 dark:hover:bg-neutral-600"
        >
          <ArrowPathIcon className="h-5 w-5" />
        </button>
      </div>

      <div className="bg-white dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700 p-4">
        <div className="space-y-1">
          {filteredNodes.map(node => renderNode(node))}
          
          {filteredNodes.length === 0 && (
            <div className="text-center py-8 text-neutral-500">
              No nodes found matching your filters
            </div>
          )}
        </div>
      </div>
      
      <div className="text-sm text-neutral-600 dark:text-neutral-400">
        Total: {nodes.length} nodes | Hidden: {hiddenNodes.size} nodes
      </div>
    </div>
  )
}

export default HiddenNodesManager