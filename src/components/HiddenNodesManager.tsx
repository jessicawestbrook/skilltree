import React, { useState, useEffect } from 'react'
import { supabase } from '../services/supabase'
import { hiddenSkillsService } from '../services/hiddenNodesService'
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
  const [skills, setSkills] = useState<SkillTreeNode[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [expandedSkills, setExpandedSkills] = useState<Set<string>>(new Set())
  const [hiddenSkills, setHiddenSkills] = useState<Set<string>>(new Set())
  const [skillChildren, setSkillChildren] = useState<Record<string, SkillTreeNode[]>>({})
  const [filterMode, setFilterMode] = useState<'all' | 'visible' | 'hidden'>('all')

  useEffect(() => {
    fetchSkills()
  }, [])

  const fetchSkills = async () => {
    try {
      setLoading(true)
      
      // Fetch all top-level skills
      const { data: topSkills, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .is('parent_id', null)
        .order('display_order', { nullsFirst: false })
        .order('name')

      if (error) throw error

      setSkills(topSkills || [])
      
      // Initialize hidden skills from service
      const hiddenIds = await hiddenSkillsService.getHiddenSkillIds()
      setHiddenSkills(new Set(hiddenIds))
      
      // Pre-fetch children for all top skills
      const childrenMap: Record<string, SkillTreeNode[]> = {}
      for (const skill of topSkills || []) {
        const { data: children } = await supabase
          .from('skill_tree_nodes')
          .select('*')
          .eq('parent_id', skill.id)
          .order('display_order', { nullsFirst: false })
          .order('name')
        
        if (children && children.length > 0) {
          childrenMap[skill.id] = children
        }
      }
      setSkillChildren(childrenMap)
      
    } catch (error) {
      console.error('Error fetching skills:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchChildren = async (skillId: string) => {
    if (skillChildren[skillId]) return // Already fetched

    try {
      const { data: children, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('parent_id', skillId)
        .order('display_order', { nullsFirst: false })
        .order('name')

      if (error) throw error

      setSkillChildren(prev => ({
        ...prev,
        [skillId]: children || []
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
          setSkillChildren(prev => ({
            ...prev,
            [child.id]: grandchildren
          }))
        }
      }
    } catch (error) {
      console.error('Error fetching children:', error)
    }
  }

  const toggleSkillVisibility = async (skillId: string, includeDescendants: boolean = true) => {
    const isHidden = await hiddenSkillsService.toggleSkillVisibility(skillId, includeDescendants)
    
    // Update local state
    setHiddenSkills(prev => {
      const newSet = new Set(prev)
      if (isHidden) {
        newSet.add(skillId)
        if (includeDescendants) {
          // Add all descendants
          const addDescendants = (id: string) => {
            const children = skillChildren[id] || []
            children.forEach(child => {
              newSet.add(child.id)
              addDescendants(child.id)
            })
          }
          addDescendants(skillId)
        }
      } else {
        newSet.delete(skillId)
        if (includeDescendants) {
          // Remove all descendants
          const removeDescendants = (id: string) => {
            const children = skillChildren[id] || []
            children.forEach(child => {
              newSet.delete(child.id)
              removeDescendants(child.id)
            })
          }
          removeDescendants(skillId)
        }
      }
      return newSet
    })
    
    // Save to config file (in production, this would save to database)
    console.log('Updated hidden skills:', Array.from(hiddenSkills))
  }

  const toggleExpanded = (skillId: string) => {
    setExpandedSkills(prev => {
      const newSet = new Set(prev)
      if (newSet.has(skillId)) {
        newSet.delete(skillId)
      } else {
        newSet.add(skillId)
        fetchChildren(skillId)
      }
      return newSet
    })
  }

  const filteredSkills = skills.filter(skill => {
    // Filter by search term
    if (searchTerm && !skill.name.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false
    }
    
    // Filter by visibility mode
    if (filterMode === 'hidden' && !hiddenSkills.has(skill.id)) {
      return false
    }
    if (filterMode === 'visible' && hiddenSkills.has(skill.id)) {
      return false
    }
    
    return true
  })

  const renderSkill = (skill: SkillTreeNode, level: number = 0) => {
    const children = skillChildren[skill.id] || []
    const hasChildren = children.length > 0
    const isExpanded = expandedSkills.has(skill.id)
    const isHidden = hiddenSkills.has(skill.id)
    const isCategory = !skill.learning_content_ids || skill.learning_content_ids.length === 0

    return (
      <div key={skill.id} className={`${level > 0 ? 'ml-6' : ''}`}>
        <div className={`flex items-center gap-2 p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 ${
          isHidden ? 'opacity-50' : ''
        }`}>
          {hasChildren && (
            <button
              onClick={() => toggleExpanded(skill.id)}
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
              {skill.name}
            </span>
            {isCategory && (
              <span className="ml-2 text-xs text-blue-500">
                Category
              </span>
            )}
          </div>
          
          <button
            onClick={() => toggleSkillVisibility(skill.id, true)}
            className={`p-2 rounded-lg transition-colors ${
              isHidden 
                ? 'bg-red-100 text-red-600 hover:bg-red-200 dark:bg-red-900/30 dark:text-red-400 dark:hover:bg-red-900/50' 
                : 'bg-green-100 text-green-600 hover:bg-green-200 dark:bg-green-900/30 dark:text-green-400 dark:hover:bg-green-900/50'
            }`}
            title={isHidden ? 'Show this skill and its children' : 'Hide this skill and its children'}
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
            {children.map(child => renderSkill(child, level + 1))}
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
      {!hiddenSkillsService.isUsingDatabase() && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
          <p className="text-sm text-yellow-800 dark:text-yellow-200">
            <strong>Note:</strong> Hidden nodes configuration is currently stored locally. 
            To persist changes, add the is_hidden column to the database.
          </p>
        </div>
      )}
      
      {hiddenSkillsService.isUsingDatabase() && (
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
            placeholder="Search skills..."
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
          <option value="all">All Skills</option>
          <option value="visible">Visible Only</option>
          <option value="hidden">Hidden Only</option>
        </select>
        
        <button
          onClick={fetchSkills}
          className="p-2 rounded-lg bg-neutral-100 hover:bg-neutral-200 dark:bg-neutral-700 dark:hover:bg-neutral-600"
        >
          <ArrowPathIcon className="h-5 w-5" />
        </button>
      </div>

      <div className="bg-white dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700 p-4">
        <div className="space-y-1">
          {filteredSkills.map(skill => renderSkill(skill))}
          
          {filteredSkills.length === 0 && (
            <div className="text-center py-8 text-neutral-500">
              No skills found matching your filters
            </div>
          )}
        </div>
      </div>
      
      <div className="text-sm text-neutral-600 dark:text-neutral-400">
        Total: {skills.length} skills | Hidden: {hiddenSkills.size} skills
      </div>
    </div>
  )
}

export default HiddenNodesManager