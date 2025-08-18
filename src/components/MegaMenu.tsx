import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { SkillTreeNode } from '../types/database.types'
import { ChevronRightIcon } from '@heroicons/react/24/outline'
import { cacheService } from '../services/cache'

interface CategoryChildren {
  directChildren: SkillTreeNode[]
  grandchildMap: Record<string, SkillTreeNode[]>
}

const MegaMenu: React.FC = () => {
  const [topCategories, setTopCategories] = useState<SkillTreeNode[]>([])
  const [childNodes, setChildNodes] = useState<Record<string, CategoryChildren>>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTopCategories()
  }, [])

  const fetchTopCategories = async () => {
    try {
      const cachedNodes = cacheService.get<SkillTreeNode[]>('skill_tree_nodes')
      let allNodes: SkillTreeNode[]
      
      if (cachedNodes) {
        allNodes = cachedNodes
      } else {
        // Fetch all nodes with pagination
        allNodes = []
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
        
        console.log('MegaMenu - Fetched nodes:', allNodes.length)
        cacheService.set('skill_tree_nodes', allNodes)
      }

      const nodeIds = new Set(allNodes.map(n => n.id))
      const rootNodes = allNodes.filter(node => !node.parent_id || !nodeIds.has(node.parent_id))
      
      const topLevelCategories = rootNodes.length > 0 
        ? allNodes.filter(n => rootNodes.some(r => r.id === n.parent_id))
            .filter(n => n.type === 'category')
            .slice(0, 3)
        : []

      setTopCategories(topLevelCategories)

      const childMap: Record<string, CategoryChildren> = {}
      topLevelCategories.forEach(category => {
        // Get all direct children of each top category
        const directChildren = allNodes
          .filter(n => n.parent_id === category.id)
        
        // For each direct child that is a category, also get its children (grandchildren)
        const grandchildMap: Record<string, SkillTreeNode[]> = {}
        directChildren.forEach(child => {
          if (child.type === 'category') {
            grandchildMap[child.id] = allNodes
              .filter(n => n.parent_id === child.id)
              .slice(0, 5) // Limit grandchildren to keep it manageable
          }
        })
        
        childMap[category.id] = { directChildren, grandchildMap }
      })
      setChildNodes(childMap)
    } catch (error) {
      console.error('Error fetching categories:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-neutral-200 dark:bg-neutral-700 rounded w-1/3 mx-auto"></div>
          <div className="grid md:grid-cols-3 gap-6">
            {[1, 2, 3].map(i => (
              <div key={i} className="space-y-3">
                <div className="h-6 bg-neutral-200 dark:bg-neutral-700 rounded"></div>
                <div className="space-y-2">
                  {[1, 2, 3].map(j => (
                    <div key={j} className="h-4 bg-neutral-100 dark:bg-neutral-800 rounded"></div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <section className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-8">
      <h2 className="text-3xl font-bold text-center mb-8">
        Explore Learning Categories
      </h2>
      
      <div className="grid lg:grid-cols-3 md:grid-cols-2 gap-8">
        {topCategories.map(category => (
          <div key={category.id} className="space-y-4">
            <Link
              to={`/category/${category.id}`}
              className="block group"
            >
              <div className="flex items-center justify-between p-4 bg-gradient-to-r from-primary-50 to-gold-50 dark:from-primary-900/20 dark:to-gold-900/20 rounded-lg hover:shadow-md transition-all">
                <div>
                  <h3 className="text-xl font-semibold text-primary-700 dark:text-primary-400 group-hover:text-primary-800 dark:group-hover:text-primary-300">
                    {category.name}
                  </h3>
                  {category.learning_area && (
                    <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-1">
                      {category.learning_area}
                    </p>
                  )}
                </div>
                <ChevronRightIcon className="h-5 w-5 text-primary-600 dark:text-primary-400 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>
            
            {childNodes[category.id] && childNodes[category.id].directChildren.length > 0 && (
              <div className="space-y-2 max-h-96 overflow-y-auto custom-scrollbar">
                {childNodes[category.id].directChildren.slice(0, 15).map(child => (
                  <div key={child.id} className="border-l-2 border-neutral-200 dark:border-neutral-700 pl-3 ml-2">
                    <Link
                      to={`/skill-tree?node=${child.id}`}
                      className="block py-1 px-2 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-800 rounded transition-colors hover:text-primary-600 dark:hover:text-primary-400"
                    >
                      <div className="flex items-center gap-2">
                        <span className={`inline-block w-2 h-2 rounded-full flex-shrink-0 ${
                          child.has_learning_content 
                            ? 'bg-green-500' 
                            : child.type === 'category'
                            ? 'bg-gold-500'
                            : 'bg-neutral-300 dark:bg-neutral-600'
                        }`}></span>
                        <span className="truncate">{child.name}</span>
                      </div>
                    </Link>
                    {/* Show grandchildren if this is a category */}
                    {child.type === 'category' && childNodes[category.id].grandchildMap[child.id] && 
                     childNodes[category.id].grandchildMap[child.id].length > 0 && (
                      <div className="pl-4 mt-1 space-y-0.5 border-l border-neutral-100 dark:border-neutral-800 ml-1">
                        {childNodes[category.id].grandchildMap[child.id].slice(0, 3).map(grandchild => (
                          <Link
                            key={grandchild.id}
                            to={`/skill-tree?node=${grandchild.id}`}
                            className="block py-0.5 px-2 text-xs text-neutral-500 dark:text-neutral-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors truncate"
                          >
                            {grandchild.name}
                          </Link>
                        ))}
                        {childNodes[category.id].grandchildMap[child.id].length > 3 && (
                          <span className="block py-0.5 px-2 text-xs text-neutral-400 dark:text-neutral-500">
                            +{childNodes[category.id].grandchildMap[child.id].length - 3} more...
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                ))}
                {childNodes[category.id].directChildren.length > 15 && (
                  <div className="pt-2 mt-2 border-t border-neutral-200 dark:border-neutral-700">
                    <Link
                      to={`/category/${category.id}`}
                      className="block py-2 px-3 text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-center"
                    >
                      View all {childNodes[category.id].directChildren.length} subcategories →
                    </Link>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-8 text-center">
        <Link 
          to="/skill-tree" 
          className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium"
        >
          View Complete Skill Tree
          <ChevronRightIcon className="h-5 w-5" />
        </Link>
      </div>
    </section>
  )
}

export default MegaMenu