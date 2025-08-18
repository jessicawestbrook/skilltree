import React, { useEffect, useRef, useState, useCallback } from 'react'
import * as d3 from 'd3'
import { supabase } from '../services/supabase'
import { cacheService } from '../services/cache'
import { SkillTreeNode } from '../types/database.types'
import { useAuth } from '../contexts/AuthContext'
import { 
  StarIcon, 
  ChevronRightIcon, 
  ChevronDownIcon,
  MagnifyingGlassIcon,
  EyeIcon,
  EyeSlashIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid'
import LearningContentModal from '../components/LearningContentModal'

interface HierarchicalListProps {
  nodes: SkillTreeNode[]
  starredNodes: Set<string>
  onToggleStar: (nodeId: string) => void
  onNodeClick: (nodeId: string) => void
  selectedNodeId: string | null
  expandedNodes: Set<string>
  onToggleExpand: (nodeId: string) => void
}

const HierarchicalList: React.FC<HierarchicalListProps> = ({ 
  nodes, 
  starredNodes, 
  onToggleStar, 
  onNodeClick,
  selectedNodeId,
  expandedNodes,
  onToggleExpand
}) => {
  // Find root nodes
  const nodeIds = new Set(nodes.map(n => n.id))
  const rootNodes = nodes.filter(node => !node.parent_id || !nodeIds.has(node.parent_id))

  const renderNode = (node: SkillTreeNode, level: number = 0) => {
    const children = nodes.filter(n => n.parent_id === node.id)
    const hasChildren = children.length > 0
    const isExpanded = expandedNodes.has(node.id)
    const isSelected = selectedNodeId === node.id

    return (
      <div key={node.id} className="select-none" id={`list-node-${node.id}`}>
        <div 
          className={`flex items-center justify-between py-2 px-3 hover:bg-neutral-50 dark:hover:bg-neutral-800 rounded-lg transition-colors cursor-pointer ${
            isSelected ? 'bg-primary-50 dark:bg-primary-900/20 border-l-4 border-primary-500' : ''
          }`}
          style={{ paddingLeft: `${level * 24 + 12}px` }}
          onClick={() => onNodeClick(node.id)}
        >
          <div className="flex items-center flex-1">
            {hasChildren && (
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  onToggleExpand(node.id)
                }}
                className="mr-2 p-1 hover:bg-neutral-200 dark:hover:bg-neutral-700 rounded"
              >
                {isExpanded ? (
                  <ChevronDownIcon className="h-4 w-4" />
                ) : (
                  <ChevronRightIcon className="h-4 w-4" />
                )}
              </button>
            )}
            {!hasChildren && <span className="w-6 mr-2" />}
            
            <div className="flex-1">
              <span className="font-medium">{node.name}</span>
              {node.learning_area && (
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  {node.learning_area}
                </p>
              )}
            </div>
          </div>
          
          <button
            onClick={(e) => {
              e.stopPropagation()
              onToggleStar(node.id)
            }}
            className="p-1.5 hover:bg-neutral-200 dark:hover:bg-neutral-700 rounded-lg transition-colors"
          >
            {starredNodes.has(node.id) ? (
              <StarIconSolid className="h-5 w-5 text-yellow-500" />
            ) : (
              <StarIcon className="h-5 w-5 text-neutral-400 hover:text-neutral-600" />
            )}
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

  return (
    <div className="py-2">
      {rootNodes.map(node => renderNode(node))}
    </div>
  )
}

const UnifiedSkillTreePage: React.FC = () => {
  const { user } = useAuth()
  const svgRef = useRef<SVGSVGElement>(null)
  const [nodes, setNodes] = useState<SkillTreeNode[]>([])
  const [loading, setLoading] = useState(true)
  const [starredNodes, setStarredNodes] = useState<Set<string>>(new Set())
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null)
  const [selectedNode, setSelectedNode] = useState<SkillTreeNode | null>(null)
  const [showLearningModal, setShowLearningModal] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showOnlyStarred, setShowOnlyStarred] = useState(false)
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set())
  const [showVisualization, setShowVisualization] = useState(true)
  const [splitView, setSplitView] = useState(true)

  useEffect(() => {
    fetchNodes()
    if (user) {
      fetchStarredNodes()
    }
  }, [user])

  useEffect(() => {
    // Set default expanded nodes (first 3 top-level categories)
    if (nodes.length > 0 && expandedNodes.size === 0) {
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
  }, [nodes])

  const fetchNodes = async () => {
    try {
      const cachedNodes = cacheService.get<SkillTreeNode[]>('skill_tree_nodes')
      if (cachedNodes) {
        console.log('Using cached nodes:', cachedNodes.length)
        setNodes(cachedNodes)
        setLoading(false)
        return
      }

      // Fetch all nodes with pagination (Supabase limits to 1000 per request)
      const allNodes: SkillTreeNode[] = []
      const pageSize = 1000
      let offset = 0
      let hasMore = true
      
      // Get total count first
      const { count, error: countError } = await supabase
        .from('skill_tree_nodes')
        .select('*', { count: 'exact', head: true })
      
      if (countError) throw countError
      
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
      
      const nodesData = allNodes
      console.log('Fetched nodes from DB:', nodesData.length, 'Total count:', count)
      cacheService.set('skill_tree_nodes', nodesData)
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
        .from('user_starred_nodes')
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
          .from('user_starred_nodes')
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
          .from('user_starred_nodes')
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

  const handleNodeClick = useCallback((nodeId: string) => {
    const node = nodes.find(n => n.id === nodeId)
    if (!node) return

    setSelectedNodeId(nodeId)
    
    // Expand path to this node in list view
    const path: string[] = []
    let currentNode: SkillTreeNode | undefined = node
    while (currentNode) {
      if (currentNode.parent_id) {
        path.unshift(currentNode.parent_id)
      }
      currentNode = nodes.find(n => n.id === currentNode?.parent_id)
    }
    
    // Expand all nodes in the path
    setExpandedNodes(prev => {
      const newSet = new Set(prev)
      path.forEach(id => newSet.add(id))
      newSet.add(nodeId) // Also expand the clicked node if it has children
      return newSet
    })
    
    // Scroll to the selected node in list view after a brief delay
    setTimeout(() => {
      const element = document.getElementById(`list-node-${nodeId}`)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }, 100)

    // Open learning modal if node has content
    if (node.has_learning_content) {
      setSelectedNode(node)
      setShowLearningModal(true)
    }
  }, [nodes])

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

  const drawTree = useCallback(() => {
    if (!svgRef.current || !showVisualization) return
    
    const filteredNodes = getFilteredNodes()
    if (filteredNodes.length === 0) return

    const containerWidth = svgRef.current?.parentElement?.clientWidth || 600
    const width = containerWidth
    const height = 600
    
    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)

    // Create zoom behavior
    const g = svg.append('g')
    
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform.toString())
      })
    
    svg.call(zoom)

    // Build hierarchy
    const nodeIds = new Set(filteredNodes.map(n => n.id))
    const rootNodes = filteredNodes.filter(node => !node.parent_id || !nodeIds.has(node.parent_id))
    
    if (rootNodes.length === 0) return

    const nodeMap = new Map(filteredNodes.map(n => [n.id, n]))
    const buildHierarchy = (nodeId: string): any => {
      const node = nodeMap.get(nodeId)
      if (!node) return null
      
      const children = filteredNodes
        .filter(n => n.parent_id === nodeId)
        .map(child => buildHierarchy(child.id))
        .filter(Boolean)
      
      return { ...node, children: children.length > 0 ? children : undefined }
    }

    const rootData = rootNodes.length === 1 
      ? buildHierarchy(rootNodes[0].id)
      : { 
          id: 'root', 
          name: 'Knowledge Tree', 
          children: rootNodes.map(r => buildHierarchy(r.id)).filter(Boolean)
        }

    const root = d3.hierarchy(rootData)
    
    // Create radial tree layout
    const treeLayout = d3.tree<any>()
      .size([2 * Math.PI, Math.min(width, height) / 2 - 100])
      .separation((a, b) => (a.parent === b.parent ? 1 : 2) / a.depth)

    treeLayout(root)

    // Draw links
    g.append('g')
      .attr('fill', 'none')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.4)
      .attr('stroke-width', 1.5)
      .selectAll('path')
      .data(root.links())
      .join('path')
      .attr('d', d3.linkRadial<any, any>()
        .angle((d: any) => d.x)
        .radius((d: any) => d.y))

    // Draw nodes
    const node = g.append('g')
      .selectAll('g')
      .data(root.descendants())
      .join('g')
      .attr('transform', (d: any) => 
        `rotate(${d.x * 180 / Math.PI - 90}) translate(${d.y},0)`)

    // Add circles for nodes
    node.append('circle')
      .attr('fill', (d: any) => {
        if (selectedNodeId === d.data.id) return '#10b981'
        if (starredNodes.has(d.data.id)) return '#eab308'
        if (d.data.has_learning_content) return '#22c55e'
        return '#d1d5db'
      })
      .attr('r', (d: any) => selectedNodeId === d.data.id ? 6 : 4)
      .attr('cursor', 'pointer')
      .on('click', (event, d: any) => {
        event.stopPropagation()
        handleNodeClick(d.data.id)
      })

    // Add labels
    node.append('text')
      .attr('dy', '0.31em')
      .attr('x', (d: any) => (d.x < Math.PI) === !d.children ? 6 : -6)
      .attr('text-anchor', (d: any) => (d.x < Math.PI) === !d.children ? 'start' : 'end')
      .attr('transform', (d: any) => d.x >= Math.PI ? 'rotate(180)' : null)
      .text((d: any) => d.data.name)
      .attr('font-size', '10px')
      .attr('cursor', 'pointer')
      .on('click', (event, d: any) => {
        event.stopPropagation()
        handleNodeClick(d.data.id)
      })

    // Center the view
    g.attr('transform', `translate(${width / 2},${height / 2})`)

    // Initial zoom to fit
    const bounds = g.node()?.getBBox()
    if (bounds) {
      const fullWidth = bounds.width
      const fullHeight = bounds.height
      const midX = bounds.x + fullWidth / 2
      const midY = bounds.y + fullHeight / 2
      const scale = 0.8 / Math.max(fullWidth / width, fullHeight / height)
      
      svg.call(
        zoom.transform as any,
        d3.zoomIdentity
          .translate(width / 2, height / 2)
          .scale(scale)
          .translate(-midX, -midY)
      )
    }
  }, [nodes, starredNodes, selectedNodeId, showOnlyStarred, searchTerm, showVisualization, handleNodeClick])

  useEffect(() => {
    drawTree()
  }, [drawTree])

  const filteredNodes = getFilteredNodes()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-full mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-4">Skill Tree Explorer</h1>
        
        {/* Controls */}
        <div className="flex flex-wrap gap-4 mb-4">
          <div className="flex-1 min-w-[200px]">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-neutral-400" />
              <input
                type="text"
                placeholder="Search skills..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-neutral-800"
              />
            </div>
          </div>
          
          <button
            onClick={() => setShowOnlyStarred(!showOnlyStarred)}
            className={`px-4 py-2 rounded-lg transition-colors ${
              showOnlyStarred 
                ? 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400' 
                : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300'
            }`}
          >
            <StarIcon className="h-5 w-5 inline mr-2" />
            {showOnlyStarred ? 'Showing Starred' : 'Show Starred'}
          </button>
          
          <button
            onClick={() => {
              cacheService.clear()
              window.location.reload()
            }}
            className="px-4 py-2 rounded-lg transition-colors bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400"
            title="Clear cache and reload data"
          >
            <ArrowPathIcon className="h-5 w-5 inline mr-2" />
            Refresh Data
          </button>

          <button
            onClick={() => setSplitView(!splitView)}
            className="px-4 py-2 bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-lg"
          >
            {splitView ? 'Full Width' : 'Split View'}
          </button>

          <button
            onClick={() => setShowVisualization(!showVisualization)}
            className="px-4 py-2 bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-lg"
          >
            {showVisualization ? (
              <>
                <EyeSlashIcon className="h-5 w-5 inline mr-2" />
                Hide Tree
              </>
            ) : (
              <>
                <EyeIcon className="h-5 w-5 inline mr-2" />
                Show Tree
              </>
            )}
          </button>

          <button
            onClick={fetchNodes}
            className="px-4 py-2 bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-lg"
          >
            <ArrowPathIcon className="h-5 w-5" />
          </button>
        </div>

        {/* Statistics */}
        <div className="text-sm text-neutral-600 dark:text-neutral-400">
          Showing {filteredNodes.length} of {nodes.length} modules
          {starredNodes.size > 0 && ` • ${starredNodes.size} starred`}
        </div>
      </div>

      {/* Main Content Area */}
      <div className={`grid ${splitView && showVisualization ? 'lg:grid-cols-2' : 'grid-cols-1'} gap-6`}>
        {/* Tree Visualization */}
        {showVisualization && (
          <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-4 overflow-hidden">
            <h2 className="text-lg font-semibold mb-4">Visual Tree</h2>
            <div className="border border-neutral-200 dark:border-neutral-700 rounded-lg overflow-hidden">
              <svg ref={svgRef} className="w-full" />
            </div>
            <div className="mt-4 text-xs text-neutral-500">
              <div className="flex flex-wrap gap-4">
                <span><span className="inline-block w-3 h-3 rounded-full bg-green-500 mr-1"></span>Has Content</span>
                <span><span className="inline-block w-3 h-3 rounded-full bg-yellow-500 mr-1"></span>Starred</span>
                <span><span className="inline-block w-3 h-3 rounded-full bg-neutral-300 mr-1"></span>No Content</span>
              </div>
            </div>
          </div>
        )}

        {/* List View */}
        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-4">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Hierarchical List</h2>
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={expandedNodes.size === nodes.length}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setExpandedNodes(new Set(nodes.map(n => n.id)))
                    } else {
                      // Reset to default: top 3 categories
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
                  className="rounded border-neutral-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-neutral-700 dark:text-neutral-300">Expand All</span>
              </label>
              {selectedNodeId && (
                <button
                  onClick={() => setSelectedNodeId(null)}
                  className="text-sm text-primary-600 hover:text-primary-700"
                >
                  Clear Selection
                </button>
              )}
            </div>
          </div>
          <div className="max-h-[600px] overflow-y-auto border border-neutral-200 dark:border-neutral-700 rounded-lg">
            <HierarchicalList
              nodes={filteredNodes}
              starredNodes={starredNodes}
              onToggleStar={toggleStarNode}
              onNodeClick={handleNodeClick}
              selectedNodeId={selectedNodeId}
              expandedNodes={expandedNodes}
              onToggleExpand={toggleExpand}
            />
          </div>
        </div>
      </div>

      {/* Random Question Box */}
      {user && (
        <div className="mt-8">
          {/* Random Question Box removed - shown in Layout */}
        </div>
      )}

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

export default UnifiedSkillTreePage