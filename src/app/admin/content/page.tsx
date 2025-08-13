'use client';

import React, { useEffect, useState } from 'react';
import { CourseContentService } from '@/services/courseContentService';
import { 
  BookOpen, 
  Clock, 
  Plus, 
  Edit, 
  Search,
  Filter,
  FileText,
  Eye,
  Calendar,
  TrendingUp,
  MoreVertical,
  Copy,
  Trash2,
  Download,
  Upload
} from 'lucide-react';

interface ContentSummary {
  id: string;
  node_id: string;
  title: string;
  estimated_time: number;
  updated_at: string;
}

interface ContentStats {
  total: number;
  published: number;
  draft: number;
  avgReadTime: number;
}

export default function ContentPage() {
  const [contents, setContents] = useState<ContentSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<'all' | 'recent' | 'popular'>('all');
  const [stats, setStats] = useState<ContentStats>({
    total: 0,
    published: 0,
    draft: 0,
    avgReadTime: 0
  });
  const [selectedContent, setSelectedContent] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetchContents();
  }, []);

  useEffect(() => {
    // Calculate stats whenever contents change
    const totalTime = contents.reduce((sum, c) => sum + c.estimated_time, 0);
    setStats({
      total: contents.length,
      published: Math.floor(contents.length * 0.8), // Mock data
      draft: Math.ceil(contents.length * 0.2), // Mock data
      avgReadTime: contents.length > 0 ? Math.round(totalTime / contents.length) : 0
    });
  }, [contents]);

  const fetchContents = async () => {
    setLoading(true);
    const data = await CourseContentService.getAllContentSummaries();
    setContents(data);
    setLoading(false);
  };

  const handleSelectContent = (id: string) => {
    const newSelected = new Set(selectedContent);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedContent(newSelected);
  };

  const handleBulkAction = (action: 'delete' | 'export' | 'duplicate') => {
    console.log(`Bulk ${action} for:`, Array.from(selectedContent));
    // Implement bulk actions here
    setSelectedContent(new Set());
  };

  let filteredContents = contents.filter(c =>
    c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.node_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Apply additional filters
  if (filterType === 'recent') {
    filteredContents = filteredContents.sort((a, b) => 
      new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
    ).slice(0, 10);
  } else if (filterType === 'popular') {
    // Mock popular content (in real app, would use view/completion metrics)
    filteredContents = filteredContents.slice(0, 5);
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading content library...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Content Library</h1>
            <p className="text-gray-600 mt-1">Create and manage course content for knowledge nodes</p>
          </div>
          <div className="flex items-center gap-3">
            {selectedContent.size > 0 && (
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">
                  {selectedContent.size} selected
                </span>
                <button
                  onClick={() => handleBulkAction('export')}
                  className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                  title="Export selected"
                >
                  <Download className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleBulkAction('duplicate')}
                  className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                  title="Duplicate selected"
                >
                  <Copy className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleBulkAction('delete')}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  title="Delete selected"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            )}
            <a
              href="/admin/content/import"
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center gap-2"
            >
              <Upload className="w-4 h-4" />
              Import
            </a>
            <a
              href="/admin/content/new"
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Create Content
            </a>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Content</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <FileText className="w-8 h-8 text-blue-500 opacity-20" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Published</p>
              <p className="text-2xl font-bold text-gray-900">{stats.published}</p>
            </div>
            <Eye className="w-8 h-8 text-green-500 opacity-20" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-yellow-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Drafts</p>
              <p className="text-2xl font-bold text-gray-900">{stats.draft}</p>
            </div>
            <Edit className="w-8 h-8 text-yellow-500 opacity-20" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Avg. Read Time</p>
              <p className="text-2xl font-bold text-gray-900">{stats.avgReadTime}m</p>
            </div>
            <Clock className="w-8 h-8 text-purple-500 opacity-20" />
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-xl shadow-sm p-4 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search by title or node ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value as any)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="all">All Content</option>
              <option value="recent">Recently Updated</option>
              <option value="popular">Most Popular</option>
            </select>
          </div>
        </div>
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredContents.map((content) => {
          const isSelected = selectedContent.has(content.id);
          const isRecent = new Date(content.updated_at) > new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
          
          return (
            <div 
              key={content.id} 
              className={`bg-white rounded-xl shadow-sm hover:shadow-md transition-all border-2 ${
                isSelected ? 'border-green-500' : 'border-transparent'
              }`}
            >
              <div className="p-6">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start gap-3 flex-1">
                    <div className="p-2 bg-gradient-to-br from-green-100 to-emerald-100 rounded-lg">
                      <BookOpen className="w-6 h-6 text-green-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 truncate">{content.title}</h3>
                      <p className="text-sm text-gray-500">Node: {content.node_id}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => handleSelectContent(content.id)}
                      className="w-4 h-4 text-green-600 rounded focus:ring-green-500"
                    />
                    <button className="p-1 hover:bg-gray-100 rounded">
                      <MoreVertical className="w-4 h-4 text-gray-400" />
                    </button>
                  </div>
                </div>

                {/* Badges */}
                <div className="flex items-center gap-2 mb-4">
                  {isRecent && (
                    <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded-full">
                      Recently Updated
                    </span>
                  )}
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                    Published
                  </span>
                </div>

                {/* Metadata */}
                <div className="space-y-2 mb-4">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Clock className="w-4 h-4" />
                    <span>{content.estimated_time} min read</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Calendar className="w-4 h-4" />
                    <span>Updated {new Date(content.updated_at).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <TrendingUp className="w-4 h-4" />
                    <span>{Math.floor(Math.random() * 100) + 50} completions</span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-2 pt-4 border-t">
                  <a
                    href={`/admin/content/${content.id}/edit`}
                    className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
                  >
                    <Edit className="w-4 h-4" />
                    <span className="text-sm font-medium">Edit</span>
                  </a>
                  <a
                    href={`/admin/content/${content.id}/preview`}
                    className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-gray-50 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <Eye className="w-4 h-4" />
                    <span className="text-sm font-medium">Preview</span>
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {filteredContents.length === 0 && (
        <div className="bg-white rounded-xl shadow-sm p-12">
          <div className="text-center">
            <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {searchTerm ? 'No content found' : 'No course content yet'}
            </h3>
            <p className="text-gray-500 mb-6">
              {searchTerm 
                ? 'Try adjusting your search or filters' 
                : 'Start creating engaging content for your knowledge nodes'}
            </p>
            {!searchTerm && (
              <a
                href="/admin/content/new"
                className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                <Plus className="w-4 h-4" />
                Create First Content
              </a>
            )}
          </div>
        </div>
      )}
    </div>
  );
}