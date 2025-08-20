import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { cacheService } from '../services/cache'
import { SkillTreeNode } from '../types/database.types'
import { useAuth } from '../contexts/AuthContext'
// import { } from '@heroicons/react/24/outline'
// import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid'
import LearningContentModal from '../components/LearningContentModal'

const TextOnlySkillTreePage: React.FC = () => {
  const { user } = useAuth()
  const [nodes, setNodes] = useState<SkillTreeNode[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set())
  const [starredNodes, setStarredNodes] = useState<Set<string>>(new Set())
  const [showOnlyStarred, setShowOnlyStarred] = useState(false)
  const [selectedNode, setSelectedNode] = useState<SkillTreeNode | null>(null)
  const [showLearningModal, setShowLearningModal] = useState(false)

  useEffect(() => {
    fetchNodes()
    if (user) {
      fetchStarredNodes()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  useEffect(() => {
    // Set default expanded nodes (first 3 top-level categories)
    if (nodes.length > 0 && expandedNodes.size === 0) {
      const knowledgeRoot = nodes.find(n => !n.parent_id && n.name === 'Knowledge')
      
      // Get top categories (children of Knowledge root or top-level nodes)
      const topCategories = knowledgeRoot 
        ? nodes.filter(n => n.parent_id === knowledgeRoot.id)
            .filter(n => n.type === 'category')
            .slice(0, 3)
            .map(n => n.id)
        : nodes.filter(n => !n.parent_id)
            .filter(n => n.type === 'category')
            .slice(0, 3)
            .map(n => n.id)
      
      if (topCategories.length > 0) {
        setExpandedNodes(new Set(topCategories))
      }
    }
  }, [nodes, expandedNodes.size])

  const fetchNodes = async (forceRefresh = false) => {
    try {
      if (!forceRefresh) {
        const cachedNodes = cacheService.get<SkillTreeNode[]>('skill_tree_nodes')
        if (cachedNodes) {
          setNodes(cachedNodes)
          setLoading(false)
          return
        }
      }

      // Fetch all nodes with pagination (Supabase limits to 1000 per request)
      const allNodes: SkillTreeNode[] = []
      const pageSize = 1000
      let offset = 0
      let hasMore = true
      
      while (hasMore) {
        const { data, error } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .range(offset, offset + pageSize - 1)
          .order('name')
        
        if (error) throw error
        
        if (data && data.length > 0) {
          allNodes.push(...data)
          offset += pageSize
          hasMore = data.length === pageSize
        } else {
          hasMore = false
        }
      }
      
      console.log('TextOnlySkillTreePage - Fetched nodes:', allNodes.length)
      cacheService.set('skill_tree_nodes', allNodes)
      const nodesData = allNodes
      setNodes(nodesData)
    } catch (error) {
      console.error('Error fetching nodes:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchStarredNodes = async () => {
    if (!user) return
    
    try {
      const { data, error } = await supabase
        .from('starred_categories')
        .select('skill_node_id')
        .eq('user_id', user.id)

      if (error) throw error
      
      const starred = new Set(data?.map(item => item.skill_node_id) || [])
      setStarredNodes(starred)
    } catch (error) {
      console.error('Error fetching starred nodes:', error)
    }
  }

  const toggleStarNode = async (nodeId: string) => {
    if (!user) {
      alert('Please log in to star nodes')
      return
    }

    const isStarred = starredNodes.has(nodeId)
    
    try {
      if (isStarred) {
        await supabase
          .from('starred_categories')
          .delete()
          .eq('user_id', user.id)
          .eq('skill_node_id', nodeId)
        
        setStarredNodes(prev => {
          const newSet = new Set(prev)
          newSet.delete(nodeId)
          return newSet
        })
      } else {
        await supabase
          .from('starred_categories')
          .insert({
            user_id: user.id,
            skill_node_id: nodeId
          })
        
        setStarredNodes(prev => new Set(Array.from(prev).concat(nodeId)))
      }
    } catch (error) {
      console.error('Error toggling star:', error)
    }
  }

  const toggleExpand = (nodeId: string) => {
    setExpandedNodes(prev => {
      const newSet = new Set(prev)
      if (newSet.has(nodeId)) {
        newSet.delete(nodeId)
      } else {
        newSet.add(nodeId)
      }
      return newSet
    })
  }

  const handleNodeClick = (node: SkillTreeNode) => {
    if (node.has_learning_content) {
      setSelectedNode(node)
      setShowLearningModal(true)
    }
  }

  const getFilteredNodes = () => {
    let filtered = nodes
    
    if (searchTerm) {
      const term = searchTerm.toLowerCase()
      filtered = filtered.filter(node => 
        node.name.toLowerCase().includes(term) ||
        node.learning_area?.toLowerCase().includes(term)
      )
    }
    
    if (showOnlyStarred && starredNodes.size > 0) {
      const starredAndRelated = new Set<string>()
      
      // Add starred nodes
      starredNodes.forEach(id => starredAndRelated.add(id))
      
      // Add ancestors of starred nodes
      starredNodes.forEach(starredId => {
        let currentNode = nodes.find(n => n.id === starredId)
        while (currentNode?.parent_id) {
          starredAndRelated.add(currentNode.parent_id)
          const parentId = currentNode.parent_id
          currentNode = nodes.find(n => n.id === parentId)
        }
      })
      
      // Add immediate children of starred nodes
      starredNodes.forEach(starredId => {
        nodes.filter(n => n.parent_id === starredId).forEach(child => {
          starredAndRelated.add(child.id)
        })
      })
      
      filtered = filtered.filter(n => starredAndRelated.has(n.id))
    }
    
    return filtered
  }

  const renderNode = (node: SkillTreeNode, level: number = 0) => {
    const filteredNodes = getFilteredNodes()
    const children = filteredNodes.filter(n => n.parent_id === node.id)
    const hasChildren = children.length > 0
    const isExpanded = expandedNodes.has(node.id)

    return (
      <div key={node.id} className="text-sm">
        <div 
          className="flex items-center py-1 hover:bg-neutral-50 dark:hover:bg-neutral-800"
          style={{ paddingLeft: `${level * 20}px` }}
        >
          {hasChildren && (
            <button
              onClick={() => toggleExpand(node.id)}
              className="mr-1 p-0.5 text-neutral-500"
              aria-label={isExpanded ? 'Collapse' : 'Expand'}
            >
              {isExpanded ? '▼' : '▶'}
            </button>
          )}
          {!hasChildren && <span className="w-4 mr-1" />}
          
          <button
            onClick={() => handleNodeClick(node)}
            className={`flex-1 text-left ${node.has_learning_content ? 'text-primary-600 underline' : ''}`}
          >
            {node.name}
            {node.learning_area && (
              <span className="ml-2 text-xs text-neutral-500">({node.learning_area})</span>
            )}
          </button>
          
          <button
            onClick={() => toggleStarNode(node.id)}
            className="ml-2 p-0.5"
            aria-label={starredNodes.has(node.id) ? 'Unstar' : 'Star'}
          >
            {starredNodes.has(node.id) ? '★' : '☆'}
          </button>
        </div>
        
        {hasChildren && isExpanded && (
          <div>
            {children.map(child => renderNode(child, level + 1))}
          </div>
        )}
      </div>
    )
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <p>Loading...</p>
      </div>
    )
  }

  const filteredNodes = getFilteredNodes()
  const nodeIds = new Set(filteredNodes.map(n => n.id))
  
  // Find the root "Knowledge" node
  const knowledgeRoot = filteredNodes.find(n => !n.parent_id && n.name === 'Knowledge')
  
  // If we have a Knowledge root, show its children as top-level
  // Otherwise show all nodes without parents
  const rootNodes = knowledgeRoot 
    ? filteredNodes.filter(n => n.parent_id === knowledgeRoot.id)
    : filteredNodes.filter(node => !node.parent_id || !nodeIds.has(node.parent_id))

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-4">SkillTree - Text-Only View</h1>
        
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 p-3 rounded mb-4">
          <p className="text-sm">
            <strong>Low Bandwidth Mode:</strong> This text-only view loads faster and uses less data. 
            Click on any underlined item to learn more.
          </p>
        </div>

        <div className="flex justify-between items-center mb-4">
          <div className="flex gap-2">
            <Link to="/skill-tree" className="text-primary-600 underline text-sm">
              Switch to Visual View
            </Link>
          </div>
          <button
            onClick={async () => {
              setLoading(true)
              cacheService.clear()
              await fetchNodes(true)
              if (user) {
                await fetchStarredNodes()
              }
            }}
            className="text-sm px-3 py-1 bg-neutral-200 dark:bg-neutral-700 rounded hover:bg-neutral-300 dark:hover:bg-neutral-600"
          >
            🔄 Refresh Data
          </button>
        </div>

        {/* Search and Filter */}
        <div className="border border-neutral-300 dark:border-neutral-700 p-3 mb-4 rounded">
          <div className="mb-2">
            <label htmlFor="search" className="block text-sm font-medium mb-1">
              Search:
            </label>
            <input
              id="search"
              type="text"
              placeholder="Type to search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-2 py-1 border border-neutral-300 dark:border-neutral-600 rounded text-sm"
            />
          </div>
          
          <div className="flex gap-4">
            <label className="flex items-center text-sm">
              <input
                type="checkbox"
                checked={showOnlyStarred}
                onChange={(e) => setShowOnlyStarred(e.target.checked)}
                className="mr-2"
              />
              Show only starred items
            </label>
            
            <label className="flex items-center text-sm">
              <input
                type="checkbox"
                checked={expandedNodes.size === nodes.length}
                onChange={(e) => {
                  if (e.target.checked) {
                    // Expand all nodes
                    setExpandedNodes(new Set(nodes.map(n => n.id)))
                  } else {
                    // Collapse all nodes (but keep top 3 categories)
                    const nodeIds = new Set(nodes.map(n => n.id))
                    const rootNodes = nodes.filter(node => !node.parent_id || !nodeIds.has(node.parent_id))
                    const topCategories = rootNodes.length > 0 
                      ? nodes.filter(n => rootNodes.some(r => r.id === n.parent_id))
                          .filter(n => n.type === 'category')
                          .slice(0, 3)
                          .map(n => n.id)
                      : []
                    setExpandedNodes(new Set(topCategories))
                  }
                }}
                className="mr-2"
              />
              Expand all
            </label>
          </div>
        </div>

        {/* Statistics */}
        <div className="text-sm mb-4">
          <p>
            Total modules: {nodes.length} | 
            Displayed: {filteredNodes.length} | 
            Starred: {starredNodes.size}
          </p>
        </div>
      </div>

      {/* Tree Structure */}
      <div className="border border-neutral-300 dark:border-neutral-700 p-3 rounded">
        <h2 className="font-bold mb-2">Knowledge Tree</h2>
        <p className="text-xs text-neutral-500 mb-3">
          Click ▶ to expand, ★ to star, underlined items have content
        </p>
        
        {rootNodes.length > 0 ? (
          <div className="font-mono">
            {rootNodes.map(node => renderNode(node))}
          </div>
        ) : (
          <p className="text-neutral-500">No modules found</p>
        )}
      </div>

      {/* Instructions */}
      <div className="mt-6 text-xs text-neutral-500">
        <h3 className="font-bold mb-1">Keyboard Navigation:</h3>
        <ul className="list-disc list-inside">
          <li>Tab: Navigate through items</li>
          <li>Enter: Select/expand item</li>
          <li>Space: Star/unstar item</li>
        </ul>
      </div>

      {/* Learning Content Modal */}
      {selectedNode && showLearningModal && (
        <LearningContentModal
          node={selectedNode}
          isOpen={showLearningModal}
          onClose={() => {
            setShowLearningModal(false)
            setSelectedNode(null)
          }}
        />
      )}
    </div>
  )
}

export default TextOnlySkillTreePage