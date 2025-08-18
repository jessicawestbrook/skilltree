import React, { useState, useEffect } from 'react'
import { supabase } from '../services/supabase'
import { LinkIcon, PencilIcon, CheckIcon, XMarkIcon } from '@heroicons/react/24/outline'

interface ContentItem {
  id: string
  title: string
  type: 'learning_content' | 'question' | 'skill_node'
  source_url?: string
}

const SourceURLManager: React.FC = () => {
  const [content, setContent] = useState<ContentItem[]>([])
  const [loading, setLoading] = useState(true)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editingUrl, setEditingUrl] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [contentType, setContentType] = useState<'all' | 'learning_content' | 'question' | 'skill_node'>('all')

  useEffect(() => {
    fetchContent()
  }, [contentType])

  const fetchContent = async () => {
    setLoading(true)
    try {
      const allContent: ContentItem[] = []

      // Fetch learning content
      if (contentType === 'all' || contentType === 'learning_content') {
        const { data: learningContent, error: lcError } = await supabase
          .from('learning_content')
          .select('id, title, source_url')
        
        if (lcError) throw lcError
        if (learningContent) {
          allContent.push(...learningContent.map(item => ({
            ...item,
            type: 'learning_content' as const
          })))
        }
      }

      // Fetch questions
      if (contentType === 'all' || contentType === 'question') {
        const { data: questions, error: qError } = await supabase
          .from('questions')
          .select('id, question_text, source_url')
        
        if (qError) throw qError
        if (questions) {
          allContent.push(...questions.map(item => ({
            id: item.id,
            title: item.question_text?.substring(0, 100) + (item.question_text?.length > 100 ? '...' : ''),
            type: 'question' as const,
            source_url: item.source_url
          })))
        }
      }

      // Fetch skill tree nodes
      if (contentType === 'all' || contentType === 'skill_node') {
        const { data: nodes, error: nError } = await supabase
          .from('skill_tree_nodes')
          .select('id, name, source_url')
        
        if (nError) throw nError
        if (nodes) {
          allContent.push(...nodes.map(item => ({
            id: item.id,
            title: item.name,
            type: 'skill_node' as const,
            source_url: item.source_url
          })))
        }
      }

      setContent(allContent)
    } catch (error) {
      console.error('Error fetching content:', error)
    } finally {
      setLoading(false)
    }
  }

  const updateSourceURL = async (id: string, type: string, newUrl: string) => {
    try {
      const tableName = type === 'skill_node' ? 'skill_tree_nodes' : type === 'learning_content' ? 'learning_content' : 'questions'
      
      const { error } = await supabase
        .from(tableName)
        .update({ source_url: newUrl || null })
        .eq('id', id)

      if (error) throw error

      // Update local state
      setContent(prev => prev.map(item => 
        item.id === id ? { ...item, source_url: newUrl || undefined } : item
      ))

      setEditingId(null)
      setEditingUrl('')
    } catch (error) {
      console.error('Error updating source URL:', error)
    }
  }

  const startEditing = (id: string, currentUrl?: string) => {
    setEditingId(id)
    setEditingUrl(currentUrl || '')
  }

  const cancelEditing = () => {
    setEditingId(null)
    setEditingUrl('')
  }

  const filteredContent = content.filter(item => 
    item.title.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'learning_content': return '📚'
      case 'question': return '❓'
      case 'skill_node': return '🎯'
      default: return '📄'
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'learning_content': return 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400'
      case 'question': return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
      case 'skill_node': return 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400'
      default: return 'bg-neutral-100 dark:bg-neutral-900/30 text-neutral-700 dark:text-neutral-400'
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Source URL Manager</h1>
        <p className="text-neutral-600 dark:text-neutral-400">
          Manage source URLs for learning content, questions, and skill tree nodes
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 mb-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search content..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <select
              value={contentType}
              onChange={(e) => setContentType(e.target.value as any)}
              className="px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">All Content</option>
              <option value="learning_content">Learning Content</option>
              <option value="question">Questions</option>
              <option value="skill_node">Skill Nodes</option>
            </select>
          </div>
        </div>
      </div>

      {/* Content List */}
      {loading ? (
        <div className="flex justify-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredContent.length === 0 ? (
            <div className="text-center py-8 text-neutral-500 dark:text-neutral-400">
              No content found
            </div>
          ) : (
            filteredContent.map(item => (
              <div key={`${item.type}-${item.id}`} className="bg-white dark:bg-neutral-800 rounded-lg p-4 shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-lg">{getTypeIcon(item.type)}</span>
                      <span className={`text-xs px-2 py-1 rounded ${getTypeColor(item.type)}`}>
                        {item.type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </span>
                      <h3 className="font-semibold text-neutral-900 dark:text-white">
                        {item.title}
                      </h3>
                    </div>
                    
                    {editingId === item.id ? (
                      <div className="flex items-center gap-2 mt-2">
                        <input
                          type="url"
                          value={editingUrl}
                          onChange={(e) => setEditingUrl(e.target.value)}
                          placeholder="Enter source URL..."
                          className="flex-1 px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                        <button
                          onClick={() => updateSourceURL(item.id, item.type, editingUrl)}
                          className="p-2 text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 rounded"
                          title="Save"
                        >
                          <CheckIcon className="h-5 w-5" />
                        </button>
                        <button
                          onClick={cancelEditing}
                          className="p-2 text-neutral-500 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded"
                          title="Cancel"
                        >
                          <XMarkIcon className="h-5 w-5" />
                        </button>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 mt-2">
                        {item.source_url ? (
                          <a
                            href={item.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-1 text-primary-600 dark:text-primary-400 hover:underline text-sm break-all"
                          >
                            <LinkIcon className="h-4 w-4 flex-shrink-0" />
                            {item.source_url}
                          </a>
                        ) : (
                          <span className="text-neutral-500 dark:text-neutral-400 text-sm">
                            No source URL set
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                  
                  {editingId !== item.id && (
                    <button
                      onClick={() => startEditing(item.id, item.source_url)}
                      className="p-2 text-neutral-500 hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded ml-2"
                      title="Edit source URL"
                    >
                      <PencilIcon className="h-5 w-5" />
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}
      
      {/* Stats */}
      <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-neutral-900 dark:text-white">
            {filteredContent.length}
          </div>
          <div className="text-sm text-neutral-600 dark:text-neutral-400">Total Items</div>
        </div>
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-600">
            {filteredContent.filter(item => item.source_url).length}
          </div>
          <div className="text-sm text-neutral-600 dark:text-neutral-400">With Source URL</div>
        </div>
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-red-600">
            {filteredContent.filter(item => !item.source_url).length}
          </div>
          <div className="text-sm text-neutral-600 dark:text-neutral-400">Missing URL</div>
        </div>
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-primary-600">
            {filteredContent.length > 0 ? Math.round((filteredContent.filter(item => item.source_url).length / filteredContent.length) * 100) : 0}%
          </div>
          <div className="text-sm text-neutral-600 dark:text-neutral-400">Completion</div>
        </div>
      </div>
    </div>
  )
}

export default SourceURLManager