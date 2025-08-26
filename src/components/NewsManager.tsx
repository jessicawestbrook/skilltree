import React, { useState, useEffect } from 'react'
import { 
  PlusIcon, 
  PencilIcon, 
  TrashIcon, 
  EyeIcon, 
  EyeSlashIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  CheckIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import { newsService, NewsItem } from '../services/newsService'

const NewsManager: React.FC = () => {
  const [newsItems, setNewsItems] = useState<NewsItem[]>([])
  const [loading, setLoading] = useState(true)
  const [editingItem, setEditingItem] = useState<NewsItem | null>(null)
  const [isCreating, setIsCreating] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    icon_name: 'NewspaperIcon',
    link: '',
    link_text: '',
    date_posted: new Date().toISOString().split('T')[0],
    is_published: true,
    display_order: 0
  })

  useEffect(() => {
    loadNews()
  }, [])

  const loadNews = async () => {
    setLoading(true)
    try {
      const items = await newsService.getAllNews()
      setNewsItems(items)
    } catch (error) {
      console.error('Error loading news:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async () => {
    if (!formData.title || !formData.description) {
      alert('Please fill in title and description')
      return
    }

    const newItem = await newsService.createNewsItem(formData)

    if (newItem) {
      await loadNews()
      setIsCreating(false)
      resetForm()
    }
  }

  const handleUpdate = async () => {
    if (!editingItem || !formData.title || !formData.description) return

    const success = await newsService.updateNewsItem(editingItem.id, formData)
    if (success) {
      await loadNews()
      setEditingItem(null)
      resetForm()
    }
  }

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this news item?')) return

    const success = await newsService.deleteNewsItem(id)
    if (success) {
      await loadNews()
    }
  }

  const handleTogglePublished = async (item: NewsItem) => {
    const success = await newsService.togglePublished(item.id, !item.is_published)
    if (success) {
      await loadNews()
    }
  }

  const handleUpdateOrder = async (item: NewsItem, direction: 'up' | 'down') => {
    const newOrder = direction === 'up' ? item.display_order - 1 : item.display_order + 1
    const success = await newsService.updateNewsItem(item.id, { display_order: newOrder })
    if (success) {
      await loadNews()
    }
  }

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      icon_name: 'NewspaperIcon',
      link: '',
      link_text: '',
      date_posted: new Date().toISOString().split('T')[0],
      is_published: true,
      display_order: 0
    })
  }

  const startEdit = (item: NewsItem) => {
    setEditingItem(item)
    setFormData({
      title: item.title,
      description: item.description,
      icon_name: item.icon_name || 'NewspaperIcon',
      link: item.link || '',
      link_text: item.link_text || '',
      date_posted: item.date_posted,
      is_published: item.is_published,
      display_order: item.display_order
    })
    setIsCreating(false)
  }

  const iconOptions = [
    'NewspaperIcon',
    'SparklesIcon',
    'BookOpenIcon',
    'AcademicCapIcon',
    'TrophyIcon',
    'ChartBarIcon',
    'LightBulbIcon'
  ]

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Add New Button */}
      {!isCreating && !editingItem && (
        <button
          onClick={() => setIsCreating(true)}
          className="btn-primary flex items-center gap-2"
        >
          <PlusIcon className="h-5 w-5" />
          Add News Item
        </button>
      )}

      {/* Create/Edit Form */}
      {(isCreating || editingItem) && (
        <div className="bg-white dark:bg-neutral-800 rounded-lg p-6 shadow-lg">
          <h3 className="text-lg font-semibold mb-4">
            {isCreating ? 'Create News Item' : 'Edit News Item'}
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Title *</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-900"
                placeholder="News title..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Description *</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-900"
                rows={3}
                placeholder="News description..."
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Icon</label>
                <select
                  value={formData.icon_name}
                  onChange={(e) => setFormData({ ...formData, icon_name: e.target.value })}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-900"
                >
                  {iconOptions.map(icon => (
                    <option key={icon} value={icon}>{icon.replace('Icon', '')}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Date</label>
                <input
                  type="date"
                  value={formData.date_posted}
                  onChange={(e) => setFormData({ ...formData, date_posted: e.target.value })}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-900"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Link URL (optional)</label>
                <input
                  type="text"
                  value={formData.link}
                  onChange={(e) => setFormData({ ...formData, link: e.target.value })}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-900"
                  placeholder="/spelling-bee"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Link Text (optional)</label>
                <input
                  type="text"
                  value={formData.link_text}
                  onChange={(e) => setFormData({ ...formData, link_text: e.target.value })}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-900"
                  placeholder="Learn More"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Display Order</label>
                <input
                  type="number"
                  value={formData.display_order}
                  onChange={(e) => setFormData({ ...formData, display_order: parseInt(e.target.value) || 0 })}
                  className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-900"
                />
              </div>

              <div className="flex items-center">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.is_published}
                    onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
                    className="mr-2"
                  />
                  <span className="text-sm font-medium">Published</span>
                </label>
              </div>
            </div>

            <div className="flex gap-2 pt-4">
              <button
                onClick={isCreating ? handleCreate : handleUpdate}
                className="btn-primary flex items-center gap-2"
              >
                <CheckIcon className="h-4 w-4" />
                {isCreating ? 'Create' : 'Update'}
              </button>
              <button
                onClick={() => {
                  setIsCreating(false)
                  setEditingItem(null)
                  resetForm()
                }}
                className="btn-secondary flex items-center gap-2"
              >
                <XMarkIcon className="h-4 w-4" />
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* News Items List */}
      <div className="space-y-4">
        {newsItems.map((item, index) => (
          <div 
            key={item.id}
            className={`bg-white dark:bg-neutral-800 rounded-lg p-4 shadow ${
              !item.is_published ? 'opacity-60' : ''
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-semibold text-lg">{item.title}</h3>
                  {!item.is_published && (
                    <span className="text-xs bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 px-2 py-1 rounded">
                      Unpublished
                    </span>
                  )}
                </div>
                <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                  {item.description}
                </p>
                <div className="flex items-center gap-4 text-xs text-neutral-500">
                  <span>Icon: {item.icon_name?.replace('Icon', '')}</span>
                  <span>Date: {new Date(item.date_posted).toLocaleDateString()}</span>
                  <span>Order: {item.display_order}</span>
                  {item.link && <span>Link: {item.link}</span>}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleUpdateOrder(item, 'up')}
                  disabled={index === 0}
                  className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded disabled:opacity-50"
                  title="Move up"
                >
                  <ArrowUpIcon className="h-4 w-4" />
                </button>
                <button
                  onClick={() => handleUpdateOrder(item, 'down')}
                  disabled={index === newsItems.length - 1}
                  className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded disabled:opacity-50"
                  title="Move down"
                >
                  <ArrowDownIcon className="h-4 w-4" />
                </button>
                <button
                  onClick={() => handleTogglePublished(item)}
                  className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded"
                  title={item.is_published ? 'Unpublish' : 'Publish'}
                >
                  {item.is_published ? (
                    <EyeIcon className="h-4 w-4 text-green-600" />
                  ) : (
                    <EyeSlashIcon className="h-4 w-4 text-neutral-400" />
                  )}
                </button>
                <button
                  onClick={() => startEdit(item)}
                  className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded"
                  title="Edit"
                >
                  <PencilIcon className="h-4 w-4 text-blue-600" />
                </button>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded"
                  title="Delete"
                >
                  <TrashIcon className="h-4 w-4 text-red-600" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {newsItems.length === 0 && !isCreating && (
        <div className="text-center py-8 text-neutral-500">
          No news items yet. Click "Add News Item" to create one.
        </div>
      )}
    </div>
  )
}

export default NewsManager