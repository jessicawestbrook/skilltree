'use client';

import React, { useState, useEffect } from 'react';
import { Bookmark, BookmarkX, Search, Filter, StickyNote, Clock, Star, ChevronRight, X, Edit2, Save, Trash2 } from 'lucide-react';
import { bookmarkService, Bookmark as BookmarkType } from '@/services/bookmarkService';
import { useRouter } from 'next/navigation';

interface BookmarksPanelProps {
  compact?: boolean;
  onNodeSelect?: (nodeId: string) => void;
}

export default function BookmarksPanel({ compact = false, onNodeSelect }: BookmarksPanelProps) {
  const router = useRouter();
  const [bookmarks, setBookmarks] = useState<BookmarkType[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'date' | 'name' | 'difficulty'>('date');
  const [editingNotes, setEditingNotes] = useState<string | null>(null);
  const [noteText, setNoteText] = useState('');

  useEffect(() => {
    loadBookmarks();
  }, []);

  const loadBookmarks = async () => {
    setLoading(true);
    try {
      const userBookmarks = await bookmarkService.getUserBookmarks(true);
      setBookmarks(userBookmarks || []);
    } catch (error) {
      console.error('Error loading bookmarks:', error);
      setBookmarks([]);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveBookmark = async (bookmarkId: string) => {
    const success = await bookmarkService.removeBookmark(bookmarkId);
    if (success) {
      await loadBookmarks();
    }
  };

  const handleNodeClick = (nodeId: string) => {
    if (onNodeSelect) {
      onNodeSelect(nodeId);
    } else {
      router.push(`/?node=${nodeId}`);
    }
  };

  const handleSaveNotes = async (bookmarkId: string) => {
    const success = await bookmarkService.updateBookmarkNotes(bookmarkId, noteText);
    if (success) {
      setEditingNotes(null);
      setNoteText('');
      await loadBookmarks();
    }
  };

  const startEditingNotes = (bookmarkId: string, currentNotes: string) => {
    setEditingNotes(bookmarkId);
    setNoteText(currentNotes || '');
  };

  // Filter and sort bookmarks
  const filteredBookmarks = bookmarks
    .filter(b => {
      const matchesSearch = b.node_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           (b.notes && b.notes.toLowerCase().includes(searchTerm.toLowerCase()));
      const matchesCategory = filterCategory === 'all' || b.node_category === filterCategory;
      return matchesSearch && matchesCategory;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.node_name.localeCompare(b.node_name);
        case 'difficulty':
          return (b.node_difficulty || 0) - (a.node_difficulty || 0);
        case 'date':
        default:
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      }
    });

  // Get unique categories
  const categories = Array.from(new Set(bookmarks.map(b => b.node_category).filter(Boolean)));

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-forest-600"></div>
      </div>
    );
  }

  if (compact) {
    return (
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <Bookmark className="w-4 h-4" />
            Bookmarks ({bookmarks.length})
          </h4>
        </div>
        
        {bookmarks.length === 0 ? (
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center py-4">
            No bookmarks yet. Click the bookmark icon on any topic to save it for later.
          </p>
        ) : (
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {bookmarks.slice(0, 5).map((bookmark) => (
              <div
                key={bookmark.id}
                className="group flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors cursor-pointer"
                onClick={() => handleNodeClick(bookmark.node_id)}
              >
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                    {bookmark.node_name}
                  </div>
                  {bookmark.node_category && (
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {bookmark.node_category}
                    </div>
                  )}
                </div>
                <ChevronRight className="w-4 h-4 text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300" />
              </div>
            ))}
            {bookmarks.length > 5 && (
              <button
                onClick={() => router.push('/bookmarks')}
                className="w-full text-center text-xs text-forest-600 dark:text-forest-400 hover:text-forest-700 dark:hover:text-forest-300 py-2"
              >
                View all {bookmarks.length} bookmarks →
              </button>
            )}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2 flex items-center gap-3">
          <Bookmark className="w-6 h-6 text-forest-600" />
          My Bookmarks
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Save and organize topics for later study
        </p>
      </div>

      {/* Controls */}
      <div className="space-y-4 mb-6">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search bookmarks..."
            className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-forest-500"
          />
        </div>

        {/* Filters and Sort */}
        <div className="flex flex-wrap gap-2">
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="px-3 py-1.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-forest-500"
          >
            <option value="all">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-3 py-1.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-forest-500"
          >
            <option value="date">Sort by Date</option>
            <option value="name">Sort by Name</option>
            <option value="difficulty">Sort by Difficulty</option>
          </select>
        </div>
      </div>

      {/* Bookmarks List */}
      {filteredBookmarks.length === 0 ? (
        <div className="text-center py-12">
          <BookmarkX className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <p className="text-gray-500 dark:text-gray-400">
            {searchTerm || filterCategory !== 'all' 
              ? 'No bookmarks found matching your criteria'
              : 'No bookmarks yet. Start bookmarking topics to see them here!'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredBookmarks.map((bookmark) => (
            <div
              key={bookmark.id}
              className="group bg-gray-50 dark:bg-gray-900 rounded-lg p-4 hover:shadow-md transition-all"
            >
              <div className="flex items-start justify-between mb-2">
                <div 
                  className="flex-1 cursor-pointer"
                  onClick={() => handleNodeClick(bookmark.node_id)}
                >
                  <h3 className="font-semibold text-gray-900 dark:text-gray-100 group-hover:text-forest-600 dark:group-hover:text-forest-400 transition-colors">
                    {bookmark.node_name}
                  </h3>
                  <div className="flex items-center gap-4 mt-1 text-sm text-gray-500 dark:text-gray-400">
                    {bookmark.node_category && (
                      <span className="flex items-center gap-1">
                        <Filter className="w-3 h-3" />
                        {bookmark.node_category}
                      </span>
                    )}
                    {bookmark.node_difficulty && (
                      <span className="flex items-center gap-1">
                        <Star className="w-3 h-3" />
                        {'⭐'.repeat(bookmark.node_difficulty)}
                      </span>
                    )}
                    {bookmark.node_points && (
                      <span>+{bookmark.node_points} pts</span>
                    )}
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {new Date(bookmark.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                
                <button
                  onClick={() => handleRemoveBookmark(bookmark.id)}
                  className="opacity-0 group-hover:opacity-100 p-1.5 text-gray-400 hover:text-red-500 transition-all"
                  title="Remove bookmark"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              {/* Notes Section */}
              <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                {editingNotes === bookmark.id ? (
                  <div className="space-y-2">
                    <textarea
                      value={noteText}
                      onChange={(e) => setNoteText(e.target.value)}
                      placeholder="Add your notes here..."
                      className="w-full p-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-forest-500"
                      rows={3}
                    />
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleSaveNotes(bookmark.id)}
                        className="px-3 py-1 bg-forest-600 text-white rounded-lg text-sm hover:bg-forest-700 transition-colors flex items-center gap-1"
                      >
                        <Save className="w-3 h-3" />
                        Save
                      </button>
                      <button
                        onClick={() => {
                          setEditingNotes(null);
                          setNoteText('');
                        }}
                        className="px-3 py-1 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div 
                    className="flex items-start gap-2 cursor-pointer group/notes"
                    onClick={() => startEditingNotes(bookmark.id, bookmark.notes || '')}
                  >
                    <StickyNote className="w-4 h-4 text-gray-400 mt-0.5" />
                    {bookmark.notes ? (
                      <p className="text-sm text-gray-600 dark:text-gray-400 flex-1">
                        {bookmark.notes}
                      </p>
                    ) : (
                      <p className="text-sm text-gray-400 dark:text-gray-500 italic">
                        Click to add notes...
                      </p>
                    )}
                    <Edit2 className="w-3 h-3 text-gray-400 opacity-0 group-hover/notes:opacity-100 transition-opacity" />
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}