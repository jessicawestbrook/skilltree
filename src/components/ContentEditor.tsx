import React, { useState, useEffect } from 'react'
import { supabase } from '../services/supabase'
import ImageUploader from './ImageUploader'
import { 
  DocumentTextIcon, 
  PhotoIcon, 
  TrashIcon, 
  CheckIcon,
  XMarkIcon,
  ClockIcon,
  LinkIcon
} from '@heroicons/react/24/outline'
import { LearningContent } from '../types/database.types'

interface ContentEditorProps {
  contentId?: string
  onSave?: (content: LearningContent) => void
  onCancel?: () => void
}

const ContentEditor: React.FC<ContentEditorProps> = ({
  contentId,
  onSave,
  onCancel
}) => {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [images, setImages] = useState<Array<{ url: string; caption?: string }>>([])
  const [estimatedTime, setEstimatedTime] = useState(15)
  const [difficultyLevel, setDifficultyLevel] = useState('medium')
  const [sourceUrl, setSourceUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (contentId) {
      fetchContent()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [contentId])

  const fetchContent = async () => {
    if (!contentId) return

    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('learning_content')
        .select('*')
        .eq('id', contentId)
        .single()

      if (error) throw error

      if (data) {
        setTitle(data.title || '')
        setContent(data.content || '')
        setImages(data.images || [])
        setEstimatedTime(data.estimated_time_minutes || 15)
        setDifficultyLevel(data.difficulty_level || 'medium')
        setSourceUrl(data.source_url || '')
      }
    } catch (err) {
      console.error('Error fetching content:', err)
      setError('Failed to load content')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!title.trim() || !content.trim()) {
      setError('Title and content are required')
      return
    }

    setSaving(true)
    setError('')

    try {
      const contentData = {
        title,
        content,
        images: images.length > 0 ? images : null,
        estimated_time_minutes: estimatedTime,
        difficulty_level: difficultyLevel,
        source_url: sourceUrl || null,
        updated_at: new Date().toISOString()
      }

      let result
      if (contentId) {
        // Update existing content
        const { data, error } = await supabase
          .from('learning_content')
          .update(contentData)
          .eq('id', contentId)
          .select()
          .single()

        if (error) throw error
        result = data
      } else {
        // Create new content
        const { data, error } = await supabase
          .from('learning_content')
          .insert({
            ...contentData,
            id: crypto.randomUUID(),
            created_at: new Date().toISOString()
          })
          .select()
          .single()

        if (error) throw error
        result = data
      }

      if (onSave && result) {
        onSave(result)
      }
    } catch (err) {
      console.error('Error saving content:', err)
      setError('Failed to save content')
    } finally {
      setSaving(false)
    }
  }

  const handleAddImage = (url: string) => {
    setImages([...images, { url, caption: '' }])
  }

  const handleUpdateImageCaption = (index: number, caption: string) => {
    const updated = [...images]
    updated[index].caption = caption
    setImages(updated)
  }

  const handleRemoveImage = (index: number) => {
    setImages(images.filter((_, i) => i !== index))
  }

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <DocumentTextIcon className="h-6 w-6" />
          {contentId ? 'Edit Learning Content' : 'Create Learning Content'}
        </h2>

        {error && (
          <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}

        {/* Title */}
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">
            Title <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter content title..."
            className="w-full px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Content */}
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">
            Content <span className="text-red-500">*</span>
          </label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter learning content..."
            rows={10}
            className="w-full px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          <p className="text-xs text-neutral-500 mt-1">
            Separate paragraphs with blank lines
          </p>
        </div>

        {/* Images */}
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">
            <PhotoIcon className="h-4 w-4 inline mr-1" />
            Images
          </label>
          
          <div className="space-y-4">
            {images.map((image, index) => (
              <div key={index} className="border border-neutral-200 dark:border-neutral-700 rounded-lg p-4">
                <div className="flex gap-4">
                  <img
                    src={image.url}
                    alt=""
                    className="w-32 h-32 object-cover rounded-lg"
                  />
                  <div className="flex-1">
                    <input
                      type="text"
                      value={image.caption || ''}
                      onChange={(e) => handleUpdateImageCaption(index, e.target.value)}
                      placeholder="Image caption (optional)..."
                      className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                    <button
                      onClick={() => handleRemoveImage(index)}
                      className="mt-2 text-red-600 hover:text-red-700 flex items-center gap-1 text-sm"
                    >
                      <TrashIcon className="h-4 w-4" />
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            ))}
            
            <ImageUploader
              onImageUploaded={handleAddImage}
              folder="content"
              className="mt-4"
            />
          </div>
        </div>

        {/* Metadata */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {/* Estimated Time */}
          <div>
            <label className="block text-sm font-medium mb-2">
              <ClockIcon className="h-4 w-4 inline mr-1" />
              Estimated Time (minutes)
            </label>
            <input
              type="number"
              value={estimatedTime}
              onChange={(e) => setEstimatedTime(parseInt(e.target.value) || 15)}
              min="1"
              max="180"
              className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* Difficulty Level */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Difficulty Level
            </label>
            <select
              value={difficultyLevel}
              onChange={(e) => setDifficultyLevel(e.target.value)}
              className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
              <option value="expert">Expert</option>
            </select>
          </div>

          {/* Source URL */}
          <div>
            <label className="block text-sm font-medium mb-2">
              <LinkIcon className="h-4 w-4 inline mr-1" />
              Source URL
            </label>
            <input
              type="url"
              value={sourceUrl}
              onChange={(e) => setSourceUrl(e.target.value)}
              placeholder="https://..."
              className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-3">
          {onCancel && (
            <button
              onClick={onCancel}
              className="px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors flex items-center gap-2"
            >
              <XMarkIcon className="h-4 w-4" />
              Cancel
            </button>
          )}
          <button
            onClick={handleSave}
            disabled={saving || !title.trim() || !content.trim()}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            {saving ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Saving...
              </>
            ) : (
              <>
                <CheckIcon className="h-4 w-4" />
                {contentId ? 'Update' : 'Create'} Content
              </>
            )}
          </button>
        </div>
      </div>

      {/* Preview Section */}
      {(title || content) && (
        <div className="bg-white dark:bg-neutral-800 rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Preview</h3>
          <div className="prose dark:prose-invert max-w-none">
            <h2>{title}</h2>
            {content.split('\n\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
            {images.map((image, index) => (
              <figure key={index}>
                <img src={image.url} alt="" className="rounded-lg" />
                {image.caption && <figcaption>{image.caption}</figcaption>}
              </figure>
            ))}
          </div>
          {sourceUrl && (
            <div className="mt-4 pt-4 border-t border-neutral-200 dark:border-neutral-700">
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Source: <a href={sourceUrl} target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">{sourceUrl}</a>
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ContentEditor