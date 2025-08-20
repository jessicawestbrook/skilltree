import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { SkillTreeNode } from '../types/database.types'
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
      // Step 1: Find root nodes efficiently
      const { data: rootNodes, error: rootError } = await supabase
        .from('skill_tree_nodes')
        .select('id, name')
        .is('parent_id', null)
        .eq('type', 'category')
        .limit(5)

      if (rootError) throw rootError
      if (!rootNodes || rootNodes.length === 0) {
        setTopCategories([])
        setLoading(false)
        return
      }

      // Step 2: Get 2nd level categories (children of root)
      const { data: secondLevel, error: secondError } = await supabase
        .from('skill_tree_nodes')
        .select('id, name, parent_id')
        .in('parent_id', rootNodes.map(r => r.id))
        .eq('type', 'category')
        .order('name')

      if (secondError) throw secondError
      if (!secondLevel || secondLevel.length === 0) {
        setTopCategories([])
        setLoading(false)
        return
      }

      // Step 3: Get 3rd level categories (our main display categories)
      const { data: thirdLevel, error: thirdError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .in('parent_id', secondLevel.map(s => s.id))
        .eq('type', 'category')
        .order('name')
        .limit(9)

      if (thirdError) throw thirdError
      const topLevelCategories = thirdLevel || []

      setTopCategories(topLevelCategories)

      // Step 4: Get children and grandchildren for each top category
      if (topLevelCategories.length > 0) {
        const categoryIds = topLevelCategories.map(c => c.id)
        
        // Get direct children (4th level)
        const { data: children, error: childrenError } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .in('parent_id', categoryIds)
          .order('name')

        if (childrenError) throw childrenError

        // Get grandchildren (5th level) for categories that are children
        const categoryChildren = (children || []).filter(c => c.type === 'category')
        let grandchildren: SkillTreeNode[] = []
        
        if (categoryChildren.length > 0) {
          const { data: grandchildrenData, error: grandchildrenError } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .in('parent_id', categoryChildren.map(c => c.id))
            .order('name')

          if (grandchildrenError) throw grandchildrenError
          grandchildren = grandchildrenData || []
        }

        // Organize the data structure
        const childMap: Record<string, CategoryChildren> = {}
        topLevelCategories.forEach(category => {
          const directChildren = (children || []).filter(n => n.parent_id === category.id)
          
          const grandchildMap: Record<string, SkillTreeNode[]> = {}
          directChildren.forEach(child => {
            if (child.type === 'category') {
              grandchildMap[child.id] = grandchildren
                .filter(n => n.parent_id === child.id)
                .slice(0, 5) // Limit grandchildren
            }
          })
          
          childMap[category.id] = { 
            directChildren: directChildren.slice(0, 10), // Limit direct children
            grandchildMap 
          }
        })
        
        setChildNodes(childMap)
        console.log('MegaMenu - Total nodes fetched:', topLevelCategories.length + (children?.length || 0) + grandchildren.length)
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
    <section className="bg-white dark:bg-neutral-900 rounded-xl shadow-lg p-6">
      <div className="grid lg:grid-cols-3 md:grid-cols-3 sm:grid-cols-2 gap-6">
        {topCategories.map(category => (
          <div key={category.id} className="space-y-2">
            <Link
              to={`/category/${category.id}`}
              className="block group mb-3"
            >
              <div className="flex items-center justify-between p-3 bg-gradient-to-r from-primary-100 to-gold-100 dark:from-primary-800/30 dark:to-gold-800/30 rounded-lg hover:shadow-lg transition-all border border-primary-200 dark:border-primary-700 hover:border-primary-300 dark:hover:border-primary-600">
                <div>
                  <h3 className="text-lg font-bold text-primary-800 dark:text-primary-300 group-hover:text-primary-900 dark:group-hover:text-primary-200">
                    {category.name}
                  </h3>
                  <p className="text-xs text-primary-600 dark:text-primary-400 mt-1">Click to explore category</p>
                </div>
                <ChevronRightIcon className="h-5 w-5 text-primary-700 dark:text-primary-400 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>
            
            {childNodes[category.id] && childNodes[category.id].directChildren.length > 0 && (
              <div className="space-y-1 max-h-64 overflow-y-auto custom-scrollbar">
                {childNodes[category.id].directChildren.slice(0, 10).map(child => (
                  <div key={child.id} className="border-l border-neutral-200 dark:border-neutral-700 pl-2 ml-1">
                    <Link
                      to={`/skill-tree?node=${child.id}`}
                      className="block py-0.5 px-1 text-xs font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-800 rounded transition-colors hover:text-primary-600 dark:hover:text-primary-400"
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
                      <div className="pl-2 mt-0.5 space-y-0 border-l border-neutral-100 dark:border-neutral-800 ml-1">
                        {childNodes[category.id].grandchildMap[child.id].slice(0, 2).map(grandchild => (
                          <Link
                            key={grandchild.id}
                            to={`/skill-tree?node=${grandchild.id}`}
                            className="block py-0 px-1 text-xs text-neutral-500 dark:text-neutral-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors truncate"
                          >
                            {grandchild.name}
                          </Link>
                        ))}
                        {childNodes[category.id].grandchildMap[child.id].length > 2 && (
                          <span className="block py-0 px-1 text-xs text-neutral-400 dark:text-neutral-500">
                            +{childNodes[category.id].grandchildMap[child.id].length - 2} more...
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                ))}
                {childNodes[category.id].directChildren.length > 10 && (
                  <div className="pt-1 mt-1 border-t border-neutral-200 dark:border-neutral-700">
                    <Link
                      to={`/category/${category.id}`}
                      className="block py-1 px-2 text-xs font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-center"
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

      <div className="mt-4 text-center">
        <Link 
          to="/skill-tree" 
          className="inline-flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium"
        >
          View Complete Skill Tree
          <ChevronRightIcon className="h-4 w-4" />
        </Link>
      </div>
    </section>
  )
}

export default MegaMenu