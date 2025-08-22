import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { SkillTreeNode } from '../types/database.types'
import CategoryLink from './CategoryLink'
import { ChevronRightIcon } from '@heroicons/react/24/outline'

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
      // Get all top-level categories (now they're root nodes)
      const { data: topLevelCategories, error: topError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .is('parent_id', null)
        .or('learning_content_ids.is.null,learning_content_ids.eq.{}')
        .order('display_order', { nullsFirst: false })
        .order('name')

      if (topError) throw topError
      if (!topLevelCategories || topLevelCategories.length === 0) {
        setTopCategories([])
        setLoading(false)
        return
      }

      setTopCategories(topLevelCategories)

      // Get all nodes up to level 3 efficiently
      if (topLevelCategories.length > 0) {
        const categoryIds = topLevelCategories.map(c => c.id)
        
        // Get all level 2 nodes (direct children of top categories)
        const { data: level2Nodes, error: level2Error } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .in('parent_id', categoryIds)
          .order('display_order', { nullsFirst: false })
          .order('name')

        if (level2Error) throw level2Error

        // Get all level 3 nodes (children of level 2 categories)
        const level2CategoryIds = (level2Nodes || []).filter(n => !n.learning_content_ids || n.learning_content_ids.length === 0).map(c => c.id)
        let level3Nodes: SkillTreeNode[] = []
        
        if (level2CategoryIds.length > 0) {
          const { data: level3Data, error: level3Error } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .in('parent_id', level2CategoryIds)
            .order('display_order', { nullsFirst: false })
            .order('name')

          if (level3Error) throw level3Error
          level3Nodes = level3Data || []
        }

        // Organize data for easier access
        const children = level2Nodes || []
        const grandchildren = level3Nodes

        // Organize the data structure
        const childMap: Record<string, CategoryChildren> = {}
        topLevelCategories.forEach(category => {
          const directChildren = (children || []).filter(n => n.parent_id === category.id)
          
          const grandchildMap: Record<string, SkillTreeNode[]> = {}
          directChildren.forEach(child => {
            if (!child.learning_content_ids || child.learning_content_ids.length === 0) {
              grandchildMap[child.id] = grandchildren
                .filter(n => n.parent_id === child.id) // Show all grandchildren
            }
          })
          
          childMap[category.id] = { 
            directChildren: directChildren, // Show all direct children
            grandchildMap 
          }
        })
        
        setChildNodes(childMap)
        // console.log('MegaMenu - Total nodes fetched:', topLevelCategories.length + (children?.length || 0) + grandchildren.length)
      }
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
          <div className="grid md:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map(i => (
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
    <section className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-6">
      {/* Progress Legend */}
      <div className="flex items-center justify-center gap-4 mb-4 text-xs text-neutral-600 dark:text-neutral-400">
        <div className="flex items-center gap-1">
          <span className="inline-block w-2 h-2 rounded-full bg-neutral-400 dark:bg-neutral-500"></span>
          <span>Not started</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="inline-block w-2 h-2 rounded-full bg-yellow-500"></span>
          <span>In progress</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="inline-block w-2 h-2 rounded-full bg-green-500"></span>
          <span>Passed test</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="inline-block w-2 h-2 rounded-full bg-white border border-neutral-400 dark:border-neutral-500"></span>
          <span>No content yet</span>
        </div>
      </div>
      
      <div className="grid xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-6">
        {topCategories.map(category => (
          <div key={category.id} className="space-y-2">
            <CategoryLink
              categoryId={category.id}
              className="block group mb-3"
            >
              <div className="flex items-center justify-between p-3 bg-neutral-100 dark:bg-neutral-800 rounded-lg hover:shadow-lg transition-all border border-neutral-200 dark:border-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600">
                <div>
                  <h3 className="text-lg font-bold text-primary-800 dark:text-primary-300 group-hover:text-primary-900 dark:group-hover:text-primary-200">
                    {category.name}
                  </h3>
                </div>
                <ChevronRightIcon className="h-5 w-5 text-primary-700 dark:text-primary-400 group-hover:translate-x-1 transition-transform" />
              </div>
            </CategoryLink>
            
            {childNodes[category.id] && childNodes[category.id].directChildren.length > 0 && (
              <div className="space-y-1 max-h-64 overflow-y-auto custom-scrollbar">
                {childNodes[category.id].directChildren.map(child => (
                  <div key={child.id} className="border-l border-neutral-200 dark:border-neutral-700 pl-2 ml-1">
                    <CategoryLink
                      categoryId={child.id}
                      className="block py-0.5 px-1 text-xs font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-800 rounded transition-colors hover:text-primary-600 dark:hover:text-primary-400"
                    >
                      <div className="flex items-center gap-2">
                        <span className={`inline-block w-2 h-2 rounded-full flex-shrink-0 ${
                          // TODO: Implement actual user progress tracking:
                          // - bg-neutral-400 (gray): not started
                          // - bg-yellow-500 (yellow): in progress  
                          // - bg-green-500 (green): passed test
                          // - bg-white border (white with gray outline): no content yet
                          (!child.learning_content_ids || child.learning_content_ids.length === 0) 
                            ? 'bg-white border border-neutral-400 dark:border-neutral-500' // No content yet
                            : 'bg-neutral-400 dark:bg-neutral-500' // Not started (default for now)
                        }`}></span>
                        <span className="truncate">{child.name}</span>
                      </div>
                    </CategoryLink>
                    {/* Show grandchildren if this is a category */}
                    {(!child.learning_content_ids || child.learning_content_ids.length === 0) && childNodes[category.id].grandchildMap[child.id] && 
                     childNodes[category.id].grandchildMap[child.id].length > 0 && (
                      <div className="pl-2 mt-0.5 space-y-0 border-l border-neutral-100 dark:border-neutral-800 ml-1">
                        {childNodes[category.id].grandchildMap[child.id].map(grandchild => (
                          <CategoryLink
                            key={grandchild.id}
                            categoryId={grandchild.id}
                            className="block py-0 px-1 text-xs text-neutral-500 dark:text-neutral-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors truncate"
                          >
                            {grandchild.name}
                          </CategoryLink>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
                {childNodes[category.id].directChildren.length > 10 && (
                  <div className="pt-1 mt-1 border-t border-neutral-200 dark:border-neutral-700">
                    <CategoryLink
                      categoryId={category.id}
                      className="block py-1 px-2 text-xs font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-center"
                    >
                      View all {childNodes[category.id].directChildren.length} subcategories →
                    </CategoryLink>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-4 text-center">
        <Link 
          to="/learning-paths" 
          className="inline-flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium"
        >
          View Learning Paths
          <ChevronRightIcon className="h-4 w-4" />
        </Link>
      </div>
    </section>
  )
}

export default MegaMenu