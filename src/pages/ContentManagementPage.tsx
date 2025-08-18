import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../services/supabase'
import { useAuth } from '../contexts/AuthContext'
import ContentEditor from '../components/ContentEditor'
import { imageService } from '../services/imageService'
import { 
  PlusIcon, 
  PencilIcon, 
  TrashIcon,
  PhotoIcon,
  DocumentTextIcon,
  MagnifyingGlassIcon,
  ArrowUpTrayIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'
import { LearningContent } from '../types/database.types'

const ContentManagementPage: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [isAdmin, setIsAdmin] = useState(false)
  const [contents, setContents] = useState<LearningContent[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedContent, setSelectedContent] = useState<LearningContent | null>(null)
  const [isEditing, setIsEditing] = useState(false)
  const [isCreating, setIsCreating] = useState(false)
  const [migrationStatus, setMigrationStatus] = useState<{
    inProgress: boolean
    processed: number
    total: number
  }>({ inProgress: false, processed: 0, total: 0 })

  useEffect(() => {
    checkAdminStatus()
    fetchContents()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user])

  const checkAdminStatus = async () => {
    if (!user) {
      navigate('/login')
      return
    }

    // Check if user is admin (you might want to check a specific field in profiles)
    const { data } = await supabase
      .from('profiles')
      .select('is_admin')
      .eq('id', user.id)
      .single()

    if (!data?.is_admin) {
      navigate('/')
      return
    }

    setIsAdmin(true)
  }

  const fetchContents = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('learning_content')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error
      setContents(data || [])
    } catch (error) {
      console.error('Error fetching contents:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this content?')) {
      return
    }

    try {
      const { error } = await supabase
        .from('learning_content')
        .delete()
        .eq('id', id)

      if (error) throw error

      setContents(contents.filter(c => c.id !== id))
      if (selectedContent?.id === id) {
        setSelectedContent(null)
      }
    } catch (error) {
      console.error('Error deleting content:', error)
    }
  }

  const handleMigrateImages = async () => {
    setMigrationStatus({ inProgress: true, processed: 0, total: contents.length })

    let processed = 0
    for (const content of contents) {
      if (content.images && content.images.length > 0) {
        const imageUrls = content.images.map(img => 
          typeof img === 'string' ? img : img.url
        )

        const externalUrls = imageUrls.filter(url => !url.includes('supabase'))
        
        if (externalUrls.length > 0) {
          await imageService.migrateExternalImages('learning_content', content.id, externalUrls)
        }
      }
      
      processed++
      setMigrationStatus(prev => ({ ...prev, processed }))
    }

    setMigrationStatus({ inProgress: false, processed: 0, total: 0 })
    fetchContents() // Refresh to show updated URLs
  }

  const filteredContents = contents.filter(content =>
    content.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    content.content.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const handleSaveContent = (content: LearningContent) => {
    setIsEditing(false)
    setIsCreating(false)
    setSelectedContent(content)
    fetchContents()
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!isAdmin) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold mb-4">Access Denied</h2>
        <p className="text-neutral-600 dark:text-neutral-400">
          You don't have permission to access this page.
        </p>
      </div>
    )
  }

  if (isCreating || isEditing) {
    return (
      <ContentEditor
        contentId={isEditing ? selectedContent?.id : undefined}
        onSave={handleSaveContent}
        onCancel={() => {
          setIsCreating(false)
          setIsEditing(false)
        }}
      />
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Content Management</h1>
        <p className="text-neutral-600 dark:text-neutral-400">
          Create and manage learning content with integrated image storage
        </p>
      </div>

      {/* Actions Bar */}
      <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 mb-6 flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-neutral-400" />
          <input
            type="text"
            placeholder="Search content..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
        
        <button
          onClick={() => setIsCreating(true)}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-2"
        >
          <PlusIcon className="h-5 w-5" />
          Create Content
        </button>

        <button
          onClick={handleMigrateImages}
          disabled={migrationStatus.inProgress}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
        >
          {migrationStatus.inProgress ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Migrating... ({migrationStatus.processed}/{migrationStatus.total})
            </>
          ) : (
            <>
              <ArrowUpTrayIcon className="h-5 w-5" />
              Migrate External Images
            </>
          )}
        </button>
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Content List */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">Content Library</h2>
          
          {filteredContents.length === 0 ? (
            <div className="text-center py-8 text-neutral-500">
              {searchQuery ? 'No content found matching your search' : 'No content created yet'}
            </div>
          ) : (
            filteredContents.map(content => (
              <div
                key={content.id}
                onClick={() => setSelectedContent(content)}
                className={`bg-white dark:bg-neutral-800 rounded-lg p-4 cursor-pointer transition-all hover:shadow-lg ${
                  selectedContent?.id === content.id ? 'ring-2 ring-primary-500' : ''
                }`}
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-neutral-900 dark:text-white">
                    {content.title}
                  </h3>
                  <div className="flex gap-2">
                    {content.images && content.images.length > 0 && (
                      <PhotoIcon className="h-5 w-5 text-neutral-400" title="Has images" />
                    )}
                    {content.source_url && (
                      <CheckCircleIcon className="h-5 w-5 text-green-500" title="Has source" />
                    )}
                  </div>
                </div>
                
                <p className="text-sm text-neutral-600 dark:text-neutral-400 line-clamp-2">
                  {content.content}
                </p>
                
                <div className="flex items-center gap-4 mt-3 text-xs text-neutral-500">
                  <span>{content.estimated_time_minutes} min</span>
                  <span className="capitalize">{content.difficulty_level}</span>
                  {content.images && (
                    <span>{content.images.length} image{content.images.length > 1 ? 's' : ''}</span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Content Detail */}
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-6">
          {selectedContent ? (
            <div>
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-semibold">{selectedContent.title}</h2>
                <div className="flex gap-2">
                  <button
                    onClick={() => setIsEditing(true)}
                    className="p-2 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded"
                    title="Edit"
                  >
                    <PencilIcon className="h-5 w-5" />
                  </button>
                  <button
                    onClick={() => handleDelete(selectedContent.id)}
                    className="p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
                    title="Delete"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>

              <div className="prose dark:prose-invert max-w-none">
                <div className="whitespace-pre-wrap">{selectedContent.content}</div>
                
                {selectedContent.images && selectedContent.images.length > 0 && (
                  <div className="mt-6 space-y-4">
                    <h3 className="text-lg font-semibold">Images</h3>
                    {selectedContent.images.map((img, index) => (
                      <div key={index}>
                        <img
                          src={typeof img === 'string' ? img : img.url}
                          alt=""
                          className="rounded-lg max-w-full"
                        />
                        {typeof img !== 'string' && img.caption && (
                          <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-2">
                            {img.caption}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="mt-6 pt-6 border-t border-neutral-200 dark:border-neutral-700 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-neutral-600 dark:text-neutral-400">Difficulty:</span>
                  <span className="capitalize">{selectedContent.difficulty_level}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-600 dark:text-neutral-400">Duration:</span>
                  <span>{selectedContent.estimated_time_minutes} minutes</span>
                </div>
                {selectedContent.source_url && (
                  <div className="flex justify-between">
                    <span className="text-neutral-600 dark:text-neutral-400">Source:</span>
                    <a
                      href={selectedContent.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:underline truncate max-w-xs"
                    >
                      {selectedContent.source_url}
                    </a>
                  </div>
                )}
                <div className="flex justify-between">
                  <span className="text-neutral-600 dark:text-neutral-400">Created:</span>
                  <span>{new Date(selectedContent.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-neutral-500">
              Select content to view details
            </div>
          )}
        </div>
      </div>

      {/* Stats */}
      <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 text-center">
          <DocumentTextIcon className="h-8 w-8 text-primary-600 mx-auto mb-2" />
          <div className="text-2xl font-bold">{contents.length}</div>
          <div className="text-sm text-neutral-600 dark:text-neutral-400">Total Content</div>
        </div>
        
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 text-center">
          <PhotoIcon className="h-8 w-8 text-blue-600 mx-auto mb-2" />
          <div className="text-2xl font-bold">
            {contents.filter(c => c.images && c.images.length > 0).length}
          </div>
          <div className="text-sm text-neutral-600 dark:text-neutral-400">With Images</div>
        </div>
        
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 text-center">
          <CheckCircleIcon className="h-8 w-8 text-green-600 mx-auto mb-2" />
          <div className="text-2xl font-bold">
            {contents.reduce((total, c) => total + (c.images?.length || 0), 0)}
          </div>
          <div className="text-sm text-neutral-600 dark:text-neutral-400">Total Images</div>
        </div>
        
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-4 text-center">
          <ArrowUpTrayIcon className="h-8 w-8 text-purple-600 mx-auto mb-2" />
          <div className="text-2xl font-bold">
            {contents.filter(c => c.images?.some(img => {
              const url = typeof img === 'string' ? img : img.url
              return url.includes('supabase')
            })).length}
          </div>
          <div className="text-sm text-neutral-600 dark:text-neutral-400">Migrated to DB</div>
        </div>
      </div>
    </div>
  )
}

export default ContentManagementPage