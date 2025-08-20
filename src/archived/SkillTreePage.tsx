import React, { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import { supabase } from '../services/supabase'
import { cacheService } from '../services/cache'
import { SkillTreeNode } from '../types/database.types'
import { useAuth } from '../contexts/AuthContext'
import { StarIcon, ChevronRightIcon, ChevronDownIcon } from '@heroicons/react/24/outline'
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid'
import LearningContentModal from '../components/LearningContentModal'

interface HierarchicalListProps {
  nodes: SkillTreeNode[]
  starredNodes: Set<string>
  onToggleStar: (nodeId: string) => void
}

const HierarchicalList: React.FC<HierarchicalListProps> = ({ nodes, starredNodes, onToggleStar }) => {
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set())
  
  // Calculate top-level nodes
  const getTopLevelNodes = React.useMemo(() => {
    if (!nodes || nodes.length === 0) return []
    
    // Find the root node (usually "Knowledge")
    const rootNode = nodes.find(n => !n.parent_id && n.name === 'Knowledge')
    
    if (rootNode) {
      // If we have a Knowledge root node, show its direct children
      return nodes.filter(n => n.parent_id === rootNode.id)
    } else {
      // Otherwise, show all nodes without parents
      const nodesWithoutParents = nodes.filter(n => !n.parent_id)
      if (nodesWithoutParents.length > 0) {
        return nodesWithoutParents
      }
      // Last resort: show nodes whose parents don't exist in the list
      // const parentIds = new Set(nodes.map(n => n.parent_id).filter(Boolean))
      const nodeIds = new Set(nodes.map(n => n.id))
      return nodes.filter(n => !n.parent_id || !nodeIds.has(n.parent_id!))
    }
  }, [nodes])
  
  // Initialize expanded nodes after first render
  React.useEffect(() => {
    const topCategories = getTopLevelNodes
      .filter(n => n.type === 'category')
      .slice(0, 3)
      .map(n => n.id)
    
    if (topCategories.length > 0) {
      setExpandedNodes(new Set(topCategories))
    }
  }, [getTopLevelNodes])

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

  const renderNode = (node: SkillTreeNode, level: number = 0) => {
    const children = nodes.filter(n => n.parent_id === node.id)
    const hasChildren = children.length > 0
    // Auto-expand tree modules and manually expanded nodes
    const isTreeModule = node.type === 'module' || node.type === 'tree'
    const isExpanded = isTreeModule || expandedNodes.has(node.id)

    return (
      <div key={node.id} className="select-none">
        <div 
          className={`flex items-center justify-between py-2 px-3 hover:bg-neutral-50 dark:hover:bg-neutral-800 rounded-lg transition-colors`}
          style={{ paddingLeft: `${level * 24 + 12}px` }}
        >
          <div className="flex items-center flex-1">
            {hasChildren && !isTreeModule && (
              <button
                onClick={() => toggleExpand(node.id)}
                className="mr-2 p-1 hover:bg-neutral-200 dark:hover:bg-neutral-700 rounded"
              >
                {isExpanded ? (
                  <ChevronDownIcon className="h-4 w-4" />
                ) : (
                  <ChevronRightIcon className="h-4 w-4" />
                )}
              </button>
            )}
            {hasChildren && isTreeModule && (
              <span className="mr-2 p-1">
                <ChevronDownIcon className="h-4 w-4 text-neutral-400" />
              </span>
            )}
            {!hasChildren && <span className="w-6 mr-2" />}
            
            <div className="flex-1">
              <span className={`font-medium ${isTreeModule ? 'text-primary-600 dark:text-primary-400' : ''}`}>
                {node.name}
              </span>
              {isTreeModule && (
                <span className="ml-2 text-xs text-neutral-500 dark:text-neutral-400">(tree)</span>
              )}
            </div>
          </div>
          
          <button
            onClick={() => onToggleStar(node.id)}
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

  // Check if we have nodes and top-level nodes
  if (!nodes || nodes.length === 0) {
    return (
      <div className="text-neutral-500 dark:text-neutral-400 text-center py-4">
        No nodes available
      </div>
    )
  }

  if (getTopLevelNodes.length === 0) {
    return (
      <div className="text-neutral-500 dark:text-neutral-400 text-center py-4">
        No top-level nodes found. Total nodes: {nodes.length}
      </div>
    )
  }

  return (
    <div className="py-2">
      {getTopLevelNodes.map(node => renderNode(node))}
    </div>
  )
}

const SkillTreePage: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null)
  const [nodes, setNodes] = useState<SkillTreeNode[]>([])
  const [selectedNode, setSelectedNode] = useState<SkillTreeNode | null>(null)
  const [starredNodes, setStarredNodes] = useState<Set<string>>(new Set())
  const [viewMode, setViewMode] = useState<'tree' | 'list'>('tree')
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPath, setSelectedPath] = useState<string[]>([])
  const [focusedNodeId, setFocusedNodeId] = useState<string | null>(null)
  const [userProgress, setUserProgress] = useState<Map<string, string>>(new Map())
  const [learningContent, setLearningContent] = useState<Set<string>>(new Set())
  const [showLearningModal, setShowLearningModal] = useState(false)
  const [selectedLearningNode, setSelectedLearningNode] = useState<SkillTreeNode | null>(null)
  const [showOnlyStarred, setShowOnlyStarred] = useState(false)
  const { user } = useAuth()

  useEffect(() => {
    // Fetch skill nodes and user data in parallel for better performance
    const fetchData = async () => {
      const promises = [fetchSkillNodes()]
      
      if (user) {
        promises.push(fetchStarredNodes())
        promises.push(fetchUserProgress())
      }
      
      await Promise.all(promises)
    }
    
    fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const fetchSkillNodes = async (forceRefresh = false) => {
    try {
      // Check cache first (unless force refresh)
      const cacheKey = 'skill_tree_nodes'
      if (!forceRefresh) {
        const cachedNodes = cacheService.get<SkillTreeNode[]>(cacheKey)
        
        if (cachedNodes) {
          setNodes(cachedNodes)
          const contentNodeIds = new Set(
            cachedNodes.filter(node => node.has_learning_content).map(node => node.id)
          )
          setLearningContent(contentNodeIds)
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
          .order('display_order')
        
        if (error) throw error
        
        if (data && data.length > 0) {
          allNodes.push(...data)
          offset += pageSize
          hasMore = data.length === pageSize
        } else {
          hasMore = false
        }
      }
      
      console.log('SkillTreePage - Fetched nodes:', allNodes.length)
      
      // Cache the results for 5 minutes
      cacheService.set(cacheKey, allNodes, 5 * 60 * 1000)
      
      setNodes(allNodes)
      
      // After nodes are loaded, identify which have learning content
      const contentNodeIds = new Set(
        allNodes.filter(node => node.has_learning_content).map(node => node.id)
      )
      setLearningContent(contentNodeIds)
    } catch (error) {
      console.error('Error fetching skill nodes:', error)
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
      
      const starred = new Set(data?.map(d => d.skill_node_id) || [])
      setStarredNodes(starred)
    } catch (error) {
      console.error('Error fetching starred nodes:', error)
    }
  }

  const fetchUserProgress = async () => {
    if (!user) return

    try {
      const { data, error } = await supabase
        .from('user_progress')
        .select('skill_node_id, status, rating')
        .eq('user_id', user.id)

      if (error) throw error
      
      const progressMap = new Map<string, string>()
      data?.forEach(item => {
        // Map status: 'completed' with high rating = 'passed', 'in_progress' = 'in_progress', default = 'not_started'
        if (item.status === 'completed' && item.rating >= 70) {
          progressMap.set(item.skill_node_id, 'passed')
        } else if (item.status === 'in_progress' || (item.status === 'completed' && item.rating < 70)) {
          progressMap.set(item.skill_node_id, 'in_progress')
        } else {
          progressMap.set(item.skill_node_id, 'not_started')
        }
      })
      setUserProgress(progressMap)
    } catch (error) {
      console.error('Error fetching user progress:', error)
    }
  }

  // Learning content info is now handled directly when nodes are loaded

  const toggleStar = async (nodeId: string) => {
    if (!user) {
      alert('Please sign in to star categories')
      return
    }

    try {
      if (starredNodes.has(nodeId)) {
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

  // Filter nodes based on search
  const filteredNodes = searchTerm 
    ? nodes.filter(node => 
        node.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        node.path?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : nodes

  // Get nodes to display in tree view
  const getVisibleNodes = React.useCallback(() => {
    let nodesToShow = nodes
    
    // Filter for starred nodes if enabled
    if (showOnlyStarred && starredNodes.size > 0) {
      // Include starred nodes and their ancestors/descendants for tree structure
      const starredAndRelated = new Set<string>()
      
      // Add starred nodes
      starredNodes.forEach(id => starredAndRelated.add(id))
      
      // Add ancestors of starred nodes
      starredNodes.forEach(starredId => {
        let currentNode = nodes.find(n => n.id === starredId)
        while (currentNode?.parent_id) {
          starredAndRelated.add(currentNode.parent_id)
          // eslint-disable-next-line no-loop-func
          currentNode = nodes.find(n => n.id === currentNode!.parent_id)
        }
      })
      
      // Add immediate children of starred nodes
      starredNodes.forEach(starredId => {
        nodes.filter(n => n.parent_id === starredId).forEach(child => {
          starredAndRelated.add(child.id)
        })
      })
      
      nodesToShow = nodes.filter(n => starredAndRelated.has(n.id))
    }
    
    if (nodesToShow.length === 0) return []
    
    if (focusedNodeId) {
      // Show focused node and its children
      const focusedNode = nodesToShow.find(n => n.id === focusedNodeId)
      if (!focusedNode) {
        console.log('Focused node not found:', focusedNodeId)
        return []
      }
      
      // Include parent if it exists (for proper tree structure)
      const parent = focusedNode.parent_id ? nodesToShow.find(n => n.id === focusedNode.parent_id) : null
      const children = nodesToShow.filter(n => n.parent_id === focusedNodeId)
      console.log(`Showing focused node ${focusedNode.name} with ${children.length} children`)
      
      // Return parent (if exists), focused node, and children
      return parent ? [parent, focusedNode, ...children] : [focusedNode, ...children]
    } else {
      // Show root and top-level categories only
      const nodeIds = new Set(nodesToShow.map(n => n.id))
      const rootNodes = nodesToShow.filter(node => !node.parent_id || !nodeIds.has(node.parent_id))
      const topLevelChildren = rootNodes.length > 0 
        ? nodesToShow.filter(n => rootNodes.some(r => r.id === n.parent_id))
        : []
      console.log(`Showing ${rootNodes.length} root nodes and ${topLevelChildren.length} top-level children`)
      return [...rootNodes, ...topLevelChildren]
    }
  }, [nodes, focusedNodeId, showOnlyStarred, starredNodes])


  const navigateToBreadcrumb = (index: number) => {
    const newPath = selectedPath.slice(0, index)
    setSelectedPath(newPath)
    setFocusedNodeId(newPath[newPath.length - 1] || null)
  }

  useEffect(() => {
    if (!svgRef.current || nodes.length === 0 || viewMode === 'list') return

    const visibleNodes = getVisibleNodes()
    console.log('Visible nodes count:', visibleNodes.length)
    if (visibleNodes.length === 0) return

    // Calculate dimensions to fit viewport
    const container = svgRef.current?.parentElement
    if (!container) return
    
    // Get available viewport space (accounting for header, controls, etc.)
    const headerHeight = 200 // Approximate height of header + controls
    const footerHeight = 100 // Space for selected node info
    const availableHeight = window.innerHeight - headerHeight - footerHeight
    const maxWidth = Math.min(1200, container.clientWidth || window.innerWidth - 40)
    const availableWidth = maxWidth
    
    // Check if mobile
    const isMobile = window.innerWidth < 768
    const width = availableWidth
    const height = availableHeight
    
    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')

    try {
      
      let treeData: any
      
      if (focusedNodeId) {
        // Show only focused node and its immediate children
        const focusedNode = nodes.find(n => n.id === focusedNodeId)
        if (!focusedNode) return
        
        const parentNode = focusedNode.parent_id ? nodes.find(n => n.id === focusedNode.parent_id) : null
        
        // Build only immediate children, no deep recursion
        const children = nodes.filter(n => n.parent_id === focusedNodeId).map(child => ({
          ...child,
          children: []
        }))
        
        treeData = d3.hierarchy({
          ...focusedNode,
          children: children,
          parentNode: parentNode // Store parent for reference
        })
      } else {
        // Show root and immediate children only
        const nodeIds = new Set(nodes.map(n => n.id))
        const rootNodes = nodes.filter(node => !node.parent_id || !nodeIds.has(node.parent_id))
        
        if (rootNodes.length === 0) return
        
        const rootNode = rootNodes[0] // Assuming single root
        
        // Build only immediate children
        const children = nodes.filter(n => n.parent_id === rootNode.id).map(child => ({
          ...child,
          children: []
        }))
        
        treeData = d3.hierarchy({
          ...rootNode,
          children: children
        })
      }

      // Since we're always showing only immediate children, max depth is always 1
      // const maxDepth = 1 // Not needed since we use fixed scale
      
      // Use optimal radius for single-level display
      const baseRadius = Math.min(width, height) / 3.5 // Good spacing for parent-children view
      const radius = baseRadius
      
      // Use tree layout for more organic branching
      const treeLayout = d3.tree<any>()
        .size([2 * Math.PI, radius])
        .separation((a, b) => {
          // Dynamic separation based on depth and sibling relationship
          if (a.parent === b.parent) {
            // Siblings - reduce separation at deeper levels
            return 1 / (1 + a.depth * 0.3)
          } else {
            // Non-siblings - maintain more separation
            return 2 / (1 + a.depth * 0.2)
          }
        })

      const root = treeLayout(treeData)

      // Add zoom behavior (without pan)
      const zoom = d3.zoom()
        .scaleExtent([0.2, 4])
        .on('zoom', (event) => {
          // Only apply zoom scale, keep position centered
          const scale = event.transform.k
          g.transition()
            .duration(50)
            .attr('transform', `translate(${width / 2}, ${height / 2}) scale(${scale})`)
        })
        .filter((event) => {
          // Only allow zoom with wheel/pinch, disable pan drag
          return event.type === 'wheel' || event.type === 'touchmove'
        })
      
      // Enable zoom with touchpad and mouse support
      svg.call(zoom as any)
        .on('dblclick.zoom', null) // Disable double-click zoom
      
      // Add a background rect for better interaction
      svg.append('rect')
        .attr('width', width)
        .attr('height', height)
        .style('fill', 'transparent')
        .style('cursor', 'default') // Changed from 'move' to 'default'
      
      // Calculate initial scale based on tree depth
      // Since we're always showing only immediate children, use optimal scale
      const scaleFactor = 250 // Good scale for parent-children view
      const initialScale = Math.min(width, height) / scaleFactor
      
      const g = svg.append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2}) scale(${initialScale})`)

      // Create radial link generator
      const linkGenerator = d3.linkRadial()
        .angle((d: any) => d.x)
        .radius((d: any) => d.y)

      // Create gradient definitions for links
      const defs = svg.append('defs')
      
      const gradient = defs.append('radialGradient')
        .attr('id', 'nodeGradient')
        .attr('cx', '50%')
        .attr('cy', '50%')
        .attr('r', '50%')
      
      gradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', '#fbbf24')
        .attr('stop-opacity', 0.8)
      
      gradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', '#f59e0b')
        .attr('stop-opacity', 1)
      
      // Draw curved links with animation
      g.selectAll('.link')
        .data(root.links())
        .enter()
        .append('path')
        .attr('class', 'link')
        .attr('fill', 'none')
        .attr('stroke', '#d6d3d1')
        .attr('stroke-width', 3)
        .attr('opacity', 0)
        .attr('d', linkGenerator as any)
        .transition()
        .duration(500)
        .attr('opacity', 0.4)

      // Create tooltip element
      const isDarkMode = document.documentElement.classList.contains('dark')
      const tooltip = d3.select('body').append('div')
        .attr('class', 'tree-tooltip')
        .style('position', 'absolute')
        .style('visibility', 'hidden')
        .style('background', isDarkMode ? '#1f2937' : 'white')
        .style('color', isDarkMode ? '#f9fafb' : '#111827')
        .style('padding', '8px 12px')
        .style('border-radius', '6px')
        .style('box-shadow', '0 4px 6px rgba(0,0,0,0.1)')
        .style('font-size', '12px')
        .style('z-index', '1000')
        .style('pointer-events', 'none')
        .style('max-width', '250px')

      // Draw nodes with radial positioning and hover effects
      const nodeGroups = g.selectAll('.node')
        .data(root.descendants())
        .enter()
        .append('g')
        .attr('class', 'node')
        .attr('transform', (d: any) => {
          // Convert from polar to cartesian coordinates
          const angle = d.x - Math.PI / 2  // Rotate to start from top
          const radius = d.y
          const x = Math.cos(angle) * radius
          const y = Math.sin(angle) * radius
          return `translate(${x}, ${y})`
        })
        .style('cursor', 'pointer')
        .style('opacity', 0)
        .on('mouseenter', function(event, d) {
          // Highlight on hover
          const currentRadius = d.depth === 0 ? 16 : Math.max(8, 14 - d.depth * 1.5)
          d3.select(this).select('circle')
            .transition()
            .duration(200)
            .attr('r', currentRadius + 2)
          
          // Show tooltip-like effect
          d3.select(this).select('text')
            .transition()
            .duration(200)
            .style('font-weight', 'bold')
            .style('font-size', d.depth === 0 ? '18px' : '17px')
          
          // Show tooltip with node details
          const hasContent = learningContent.has(d.data.id)
          const progress = userProgress.get(d.data.id)
          const childCount = nodes.filter(n => n.parent_id === d.data.id).length
          
          let tooltipContent = `<strong>${d.data.name}</strong><br/>`
          if (childCount > 0) {
            tooltipContent += `${childCount} sub-modules<br/>`
          }
          if (hasContent) {
            tooltipContent += `<span style="color: ${isDarkMode ? '#fbbf24' : '#f59e0b'}">Has learning content</span><br/>`
          }
          if (progress === 'passed') {
            tooltipContent += `<span style="color: #22c55e">✓ Completed</span>`
          } else if (progress === 'in_progress') {
            tooltipContent += `<span style="color: #eab308">In Progress</span>`
          }
          
          tooltip.html(tooltipContent)
            .style('visibility', 'visible')
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px')
        })
        .on('mousemove', function(event) {
          tooltip
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px')
        })
        .on('mouseleave', function(event, d) {
          // Reset on mouse leave
          const normalRadius = d.depth === 0 ? 16 : Math.max(8, 14 - d.depth * 1.5)
          d3.select(this).select('circle')
            .transition()
            .duration(200)
            .attr('r', normalRadius)
          
          d3.select(this).select('text')
            .transition()
            .duration(200)
            .style('font-weight', d.depth === 0 ? 'bold' : 'normal')
            .style('font-size', '12px')
          
          // Hide tooltip
          tooltip.style('visibility', 'hidden')
        })
        .on('click', (event, d) => {
          event.stopPropagation()
          // Always allow navigation, even to leaf nodes
          setFocusedNodeId(d.data.id)
          setSelectedPath(prev => [...prev, d.data.id])
          setSelectedNode(d.data)
        })
        // Add touch support for mobile devices
        .on('touchstart', function(event, d) {
          event.preventDefault()
          // Show node highlight on touch
          const currentRadius = d.depth === 0 ? 16 : Math.max(8, 14 - d.depth * 1.5)
          d3.select(this).select('circle')
            .transition()
            .duration(200)
            .attr('r', currentRadius + 2)
        })
        .on('touchend', function(event, d) {
          event.preventDefault()
          // Reset highlight and trigger click action
          const normalRadius = d.depth === 0 ? 16 : Math.max(8, 14 - d.depth * 1.5)
          d3.select(this).select('circle')
            .transition()
            .duration(200)
            .attr('r', normalRadius)
          
          // Always allow navigation, even to leaf nodes
          setFocusedNodeId(d.data.id)
          setSelectedPath(prev => [...prev, d.data.id])
          setSelectedNode(d.data)
        })
        .transition()
        .duration(800)
        .delay((d: any, i: number) => Math.min(i * 10, 500)) // Cap delay at 500ms for performance
        .style('opacity', 1)

      // Add circles for nodes with progress indicators
      nodeGroups.each(function(d: any) {
        const nodeData = d.data
        const hasContent = learningContent.has(nodeData.id)
        const progress = userProgress.get(nodeData.id)
        const group = d3.select(this)
        
        // Determine fill color based on progress
        let fillColor = '#e5e7eb'  // Default gray for not started
        let strokeWidth = 2
        let fillOpacity = 1
        
        if (!hasContent) {
          // No content available - unfilled circle (white/transparent)
          fillColor = 'transparent'
          strokeWidth = 2
        } else if (progress === 'passed') {
          fillColor = '#22c55e'  // Green (primary-500) for passed
        } else if (progress === 'in_progress') {
          fillColor = '#eab308'  // Yellow (yellow-500) for in progress
        } else {
          fillColor = '#a8a29e'  // Neutral gray for not started (with content)
        }
        
        // Add shadow/glow effect for nodes with content
        if (hasContent && progress === 'passed') {
          group.append('circle')
            .attr('r', 12)
            .attr('fill', fillColor)
            .attr('fill-opacity', 0.3)
            .attr('filter', 'blur(4px)')
        }
        
        // Scale node size based on depth
        const nodeRadius = d.depth === 0 ? 16 : Math.max(8, 14 - d.depth * 1.5)
        const circle = group.append('circle')
          .attr('r', nodeRadius)
          .attr('fill', fillColor)
          .attr('fill-opacity', fillOpacity)
          .attr('stroke', starredNodes.has(nodeData.id) ? '#f59e0b' : 
                         !hasContent ? '#78716c' : 
                         progress === 'passed' ? '#16a34a' : '#fff')
          .attr('stroke-width', starredNodes.has(nodeData.id) ? 3 : strokeWidth)
          .style('filter', hasContent && progress === 'passed' ? 'drop-shadow(0 0 3px rgba(34, 197, 94, 0.5))' : 
                          hasContent && progress === 'in_progress' ? 'drop-shadow(0 0 3px rgba(251, 191, 36, 0.5))' : 'none')
        
        // Add pulse animation for in-progress nodes
        if (progress === 'in_progress') {
          circle
            .style('animation', 'pulse 2s infinite')
        }
        
        // Add a small indicator for nodes with many children
        const childCount = nodes.filter(n => n.parent_id === nodeData.id).length
        if (childCount > 5) {
          group.append('text')
            .attr('x', 8)
            .attr('y', -8)
            .attr('text-anchor', 'middle')
            .style('font-size', '9px')
            .style('fill', '#f59e0b')
            .style('font-weight', 'bold')
            .text(`+${childCount}`)
        }
      })

      // Add text with proper radial positioning
      nodeGroups.each(function(d: any) {
        const group = d3.select(this)
        
        // For root node (center), just add text below
        if (d.depth === 0) {
          group.append('text')
            .attr('dy', '20')
            .attr('text-anchor', 'middle')
            .style('font-size', '12px')
            .style('fill', isDarkMode ? '#f9fafb' : '#292524')
            .style('font-weight', 'bold')
            .style('text-shadow', isDarkMode ? '0 0 3px rgba(0, 0, 0, 0.8)' : '0 0 3px rgba(255, 255, 255, 0.8)')
            .text(d.data.name)
        } else {
          // Calculate the actual angle for this node
          const angle = (d.x - Math.PI / 2) * 180 / Math.PI
          
          // For left side of circle, we need to flip text and read from the inside out
          const isLeftSide = angle > 90 || angle < -90
          
          // Get the node radius for this depth level
          const textNodeRadius = d.depth === 0 ? 16 : Math.max(8, 14 - d.depth * 1.5)
          
          group.append('text')
            .attr('dy', '0.31em')
            // Adjust text position based on side with more offset
            .attr('transform', 
              isLeftSide 
                ? `rotate(${angle + 180}) translate(-${20 + textNodeRadius}, 0)`  // Flip and position for left side
                : `rotate(${angle}) translate(${20 + textNodeRadius}, 0)`  // Normal rotation for right side
            )
            .style('text-anchor', isLeftSide ? 'end' : 'start')
            .style('font-size', d.depth === 0 ? (isMobile ? '16px' : '18px') : 
                               d.depth === 1 ? (isMobile ? '14px' : '16px') :
                               d.depth === 2 ? (isMobile ? '12px' : '14px') :
                               (isMobile ? '10px' : '12px'))
            .style('fill', isDarkMode ? '#f9fafb' : '#292524')
            .style('font-weight', d.depth === 0 ? 'bold' : 'normal')
            .style('text-shadow', isDarkMode ? '0 0 2px rgba(0, 0, 0, 0.5)' : '0 0 2px rgba(255, 255, 255, 0.5)')
            // Adjust truncation based on depth and angle
            .text(() => {
              const maxLength = d.depth === 0 ? 50 : d.depth === 1 ? 40 : 25
              return d.data.name.length > maxLength ? 
                d.data.name.substring(0, maxLength) + '...' : 
                d.data.name
            })
        }
      })

      // Add parent node button if in focused view and parent exists
      if (focusedNodeId && treeData.data.parentNode) {
        const parentButton = g.append('g')
          .attr('class', 'parent-node')
          .attr('transform', `translate(0, -${radius + 40})`)
          .style('cursor', 'pointer')
          .on('click', () => {
            // Navigate to parent node
            const parentId = treeData.data.parentNode.id
            setFocusedNodeId(parentId)
            const parentIndex = selectedPath.indexOf(focusedNodeId)
            if (parentIndex > 0) {
              setSelectedPath(selectedPath.slice(0, parentIndex))
            } else if (parentIndex === 0) {
              setSelectedPath([])
              setFocusedNodeId(null)
            }
          })

        // Add background circle for parent button
        parentButton.append('circle')
          .attr('r', 20)
          .attr('fill', '#3b82f6')
          .attr('fill-opacity', 0.9)
          .attr('stroke', '#2563eb')
          .attr('stroke-width', 2)
          .style('filter', 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))')

        // Add up arrow icon
        parentButton.append('text')
          .attr('text-anchor', 'middle')
          .attr('dy', '0.35em')
          .style('font-size', '20px')
          .style('fill', 'white')
          .style('font-weight', 'bold')
          .text('↑')

        // Add label below the button
        parentButton.append('text')
          .attr('text-anchor', 'middle')
          .attr('dy', '35px')
          .style('font-size', '14px')
          .style('fill', isDarkMode ? '#93c5fd' : '#3b82f6')
          .style('font-weight', 'bold')
          .text(`← ${treeData.data.parentNode.name.substring(0, 20)}${treeData.data.parentNode.name.length > 20 ? '...' : ''}`)

        // Add hover effect
        parentButton
          .on('mouseenter', function() {
            d3.select(this).select('circle')
              .transition()
              .duration(200)
              .attr('r', 22)
              .attr('fill', '#2563eb')
          })
          .on('mouseleave', function() {
            d3.select(this).select('circle')
              .transition()
              .duration(200)
              .attr('r', 20)
              .attr('fill', '#3b82f6')
          })
      }

    } catch (error) {
      console.error('Error creating skill tree visualization:', error)
    }
    
    // Cleanup function to remove tooltips
    return () => {
      d3.selectAll('.tree-tooltip').remove()
    }
  }, [nodes, starredNodes, viewMode, focusedNodeId, selectedPath, getVisibleNodes, userProgress, learningContent])

  // Add resize listener for responsive updates
  useEffect(() => {
    const handleResize = () => {
      // Force re-render of the tree on window resize
      if (viewMode === 'tree' && nodes.length > 0) {
        const event = new Event('resize')
        window.dispatchEvent(event)
      }
    }

    const debounceResize = debounce(handleResize, 300)
    window.addEventListener('resize', debounceResize)
    
    return () => window.removeEventListener('resize', debounceResize)
  }, [viewMode, nodes.length])

  // Debounce helper
  const debounce = (func: Function, wait: number) => {
    let timeout: NodeJS.Timeout
    return (...args: any[]) => {
      clearTimeout(timeout)
      timeout = setTimeout(() => func(...args), wait)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-4 space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-3xl font-bold">
          Skill Tree <span className="text-sm font-normal italic text-neutral-500">({nodes.length} learning modules)</span>
        </h1>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('tree')}
            className={`px-4 py-2 rounded-lg ${
              viewMode === 'tree' 
                ? 'bg-primary-600 text-white' 
                : 'bg-neutral-200 dark:bg-neutral-700'
            }`}
          >
            Tree View
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`px-4 py-2 rounded-lg ${
              viewMode === 'list' 
                ? 'bg-primary-600 text-white' 
                : 'bg-neutral-200 dark:bg-neutral-700'
            }`}
          >
            List View
          </button>
          <button
            onClick={async () => {
              setLoading(true)
              cacheService.clear() // Clear all cache
              await fetchSkillNodes(true) // Force refresh
              if (user) {
                await fetchStarredNodes()
                await fetchUserProgress()
              }
            }}
            className="px-4 py-2 rounded-lg bg-neutral-200 dark:bg-neutral-700 hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
            title="Refresh data from database"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Search Bar and Filters */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            placeholder="Search skills and categories..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg 
                       bg-white dark:bg-neutral-800 focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          {user && starredNodes.size > 0 && (
            <button
              onClick={() => setShowOnlyStarred(!showOnlyStarred)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                showOnlyStarred
                  ? 'bg-gold-500 text-white hover:bg-gold-600'
                  : 'bg-neutral-200 dark:bg-neutral-700 hover:bg-neutral-300 dark:hover:bg-neutral-600'
              }`}
            >
              {showOnlyStarred ? '★ Starred Only' : '☆ Show Starred'}
            </button>
          )}
        </div>
      </div>

      {/* Breadcrumb Navigation for Tree View */}
      {viewMode === 'tree' && selectedPath.length > 0 && (
        <div className="card flex items-center gap-2 flex-wrap">
          <button
            onClick={() => {
              setSelectedPath([])
              setFocusedNodeId(null)
            }}
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            Root
          </button>
          {selectedPath.map((pathId, index) => {
            const node = nodes.find(n => n.id === pathId)
            return (
              <React.Fragment key={pathId}>
                <ChevronRightIcon className="h-4 w-4 text-neutral-400" />
                <button
                  onClick={() => navigateToBreadcrumb(index + 1)}
                  className="text-primary-600 hover:text-primary-700 font-medium"
                >
                  {node?.name}
                </button>
              </React.Fragment>
            )
          })}
        </div>
      )}

      {viewMode === 'tree' ? (
        <div className="card">
          {/* Progress Legend with improved styling */}
          <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-3 mb-4">
            <div className="flex flex-wrap gap-4 text-xs">
              <div className="flex items-center gap-2">
                <div className="relative">
                  <div className="w-4 h-4 rounded-full bg-green-500"></div>
                  <div className="absolute inset-0 rounded-full bg-green-500 opacity-30 animate-ping"></div>
                </div>
                <span className="font-medium">Passed</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-yellow-500 animate-pulse"></div>
                <span className="font-medium">In Progress</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-gray-400"></div>
                <span className="font-medium">Available</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full border-2 border-gray-500"></div>
                <span className="font-medium">No Content</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-gray-400 ring-2 ring-orange-500 ring-offset-1"></div>
                <span className="font-medium">Starred</span>
              </div>
            </div>
          </div>
          <div className="flex justify-between items-center mb-2">
            <div className="text-xs text-neutral-500">
              Mouse: Drag to pan, Scroll to zoom • 
              Touchpad: Two-finger drag to pan, Pinch to zoom • 
              Click modules to explore
            </div>
            <div className="flex gap-2">
              {focusedNodeId && (
                <button
                  onClick={() => {
                    const focusedNode = nodes.find(n => n.id === focusedNodeId)
                    if (focusedNode?.parent_id) {
                      setFocusedNodeId(focusedNode.parent_id)
                      const parentIndex = selectedPath.indexOf(focusedNodeId)
                      if (parentIndex > 0) {
                        setSelectedPath(selectedPath.slice(0, parentIndex))
                      }
                    } else {
                      setFocusedNodeId(null)
                      setSelectedPath([])
                    }
                  }}
                  className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors flex items-center gap-1"
                >
                  <span>↑</span> Parent
                </button>
              )}
              {(focusedNodeId || selectedPath.length > 0) && (
                <button
                  onClick={() => {
                    setFocusedNodeId(null)
                    setSelectedPath([])
                    setSelectedNode(null)
                  }}
                  className="px-3 py-1 text-xs bg-primary-600 text-white rounded hover:bg-primary-700 transition-colors"
                >
                  Reset View
                </button>
              )}
              <button
                onClick={() => {
                  // Reset zoom
                  if (svgRef.current) {
                    const svg = d3.select(svgRef.current)
                    const g = svg.select('g')
                    const width = svgRef.current.clientWidth || 1200
                    const height = svgRef.current.clientHeight || 800
                    const initialScale = Math.min(width, height) / 350
                    g.transition()
                      .duration(750)
                      .attr('transform', `translate(${width / 2}, ${height / 2}) scale(${initialScale})`)
                    // Reset the zoom transform
                    svg.call(
                      d3.zoom().transform as any,
                      d3.zoomIdentity
                    )
                  }
                }}
                className="px-3 py-1 text-xs bg-neutral-600 text-white rounded hover:bg-neutral-700 transition-colors"
              >
                Reset Zoom
              </button>
            </div>
          </div>
          <div className="border border-neutral-200 dark:border-neutral-700 rounded-lg bg-white dark:bg-neutral-950" style={{ height: 'calc(100vh - 300px)', overflow: 'hidden' }}>
            <svg ref={svgRef} style={{ display: 'block', width: '100%', height: '100%' }}></svg>
          </div>
          {selectedNode && (
            <div className="mt-4 p-4 bg-gradient-to-r from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 rounded-lg border border-primary-200 dark:border-primary-800">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-1">{selectedNode.name}</h3>
                  <div className="flex gap-3 text-sm text-neutral-600 dark:text-neutral-400">
                    <span className="flex items-center gap-1">
                      <span className="font-medium">Type:</span> {selectedNode.type}
                    </span>
                    <span className="flex items-center gap-1">
                      <span className="font-medium">Area:</span> {selectedNode.learning_area}
                    </span>
                  </div>
                </div>
                {userProgress.has(selectedNode.id) && (
                  <div className="flex items-center gap-2 px-3 py-1 bg-white dark:bg-neutral-800 rounded-full text-xs font-medium">
                    {userProgress.get(selectedNode.id) === 'completed' ? (
                      <>
                        <div className="w-2 h-2 rounded-full bg-green-500"></div>
                        <span className="text-green-700 dark:text-green-400">Completed</span>
                      </>
                    ) : (
                      <>
                        <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
                        <span className="text-yellow-700 dark:text-yellow-400">In Progress</span>
                      </>
                    )}
                  </div>
                )}
              </div>
              
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => toggleStar(selectedNode.id)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    starredNodes.has(selectedNode.id)
                      ? 'bg-orange-500 text-white hover:bg-orange-600'
                      : 'bg-white dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 border border-neutral-300 dark:border-neutral-600 hover:bg-neutral-50 dark:hover:bg-neutral-700'
                  }`}
                >
                  {starredNodes.has(selectedNode.id) ? '★ Starred' : '☆ Star'} Module
                </button>
                {selectedNode.has_learning_content && (
                  <button
                    onClick={() => {
                      if (!user) {
                        alert('Please sign in to access learning content')
                        return
                      }
                      setSelectedLearningNode(selectedNode)
                      setShowLearningModal(true)
                    }}
                    className="btn-primary flex items-center gap-2"
                  >
                    <span>Start Learning</span>
                    <span className="text-lg">→</span>
                  </button>
                )}
                {nodes.filter(n => n.parent_id === selectedNode.id).length > 0 && (
                  <button
                    onClick={() => {
                      setViewMode('list')
                      setSearchTerm(selectedNode.name)
                    }}
                    className="btn-secondary flex items-center gap-2"
                  >
                    <span>View Sub-modules</span>
                    <span className="text-lg">→</span>
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="card">
          {searchTerm && (
            <div className="mb-4 text-sm text-neutral-600 dark:text-neutral-400">
              Found {filteredNodes.length} results for "{searchTerm}"
            </div>
          )}
          <HierarchicalList 
            nodes={(() => {
              let nodesToShow = searchTerm ? filteredNodes : nodes
              
              // Apply starred filter if enabled
              if (showOnlyStarred && starredNodes.size > 0) {
                const starredAndRelated = new Set<string>()
                
                // Add starred nodes and their ancestors
                starredNodes.forEach(starredId => {
                  starredAndRelated.add(starredId)
                  let currentNode = nodes.find(n => n.id === starredId)
                  while (currentNode?.parent_id) {
                    starredAndRelated.add(currentNode.parent_id)
                    // eslint-disable-next-line no-loop-func
                    currentNode = nodes.find(n => n.id === currentNode!.parent_id)
                  }
                })
                
                // Add all descendants of starred nodes
                const addDescendants = (nodeId: string) => {
                  nodes.filter(n => n.parent_id === nodeId).forEach(child => {
                    starredAndRelated.add(child.id)
                    addDescendants(child.id)
                  })
                }
                starredNodes.forEach(starredId => addDescendants(starredId))
                
                nodesToShow = nodesToShow.filter(n => starredAndRelated.has(n.id))
              }
              
              return nodesToShow
            })()} 
            starredNodes={starredNodes}
            onToggleStar={toggleStar}
          />
        </div>
      )}
      
      {/* Learning Content Modal */}
      {selectedLearningNode && (
        <LearningContentModal
          node={selectedLearningNode}
          isOpen={showLearningModal}
          onClose={() => {
            setShowLearningModal(false)
            fetchUserProgress() // Refresh progress after learning
          }}
          onComplete={(passed) => {
            // Update local progress state
            setUserProgress(prev => {
              const newMap = new Map(prev)
              newMap.set(selectedLearningNode.id, passed ? 'completed' : 'in_progress')
              return newMap
            })
          }}
        />
      )}
    </div>
  )
}

export default SkillTreePage