import { createClient } from '@/lib/supabase-client';

export interface Bookmark {
  id: string;
  user_id: string;
  node_id: string;
  node_name: string;
  node_category?: string;
  node_difficulty?: number;
  node_points?: number;
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface BookmarkCreateData {
  node_id: string;
  node_name: string;
  node_category?: string;
  node_difficulty?: number;
  node_points?: number;
  notes?: string;
}

class BookmarkService {
  private static instance: BookmarkService;
  private bookmarksCache: Map<string, Bookmark[]> = new Map();

  private constructor() {}

  static getInstance(): BookmarkService {
    if (!BookmarkService.instance) {
      BookmarkService.instance = new BookmarkService();
    }
    return BookmarkService.instance;
  }

  async getUserBookmarks(forceRefresh = false): Promise<Bookmark[]> {
    try {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();
      
      if (!user) {
        return [];
      }

      // Check cache first
      if (!forceRefresh && this.bookmarksCache.has(user.id)) {
        return this.bookmarksCache.get(user.id) || [];
      }

      const response = await fetch('/api/bookmarks', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        // If unauthorized, return empty array
        if (response.status === 401) {
          return [];
        }
        console.warn('Failed to fetch bookmarks:', response.status);
        return [];
      }

      const data = await response.json();
      const bookmarks = data.bookmarks || [];
      
      // Update cache
      this.bookmarksCache.set(user.id, bookmarks);
      
      return bookmarks;
    } catch (error) {
      console.error('Error fetching bookmarks:', error);
      return [];
    }
  }

  async addBookmark(bookmarkData: BookmarkCreateData): Promise<Bookmark | null> {
    try {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();
      
      if (!user) {
        throw new Error('User not authenticated');
      }

      const response = await fetch('/api/bookmarks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookmarkData),
      });

      if (!response.ok) {
        throw new Error('Failed to add bookmark');
      }

      const data = await response.json();
      
      // Clear cache to force refresh
      this.bookmarksCache.delete(user.id);
      
      return data.bookmark;
    } catch (error) {
      console.error('Error adding bookmark:', error);
      return null;
    }
  }

  async removeBookmark(bookmarkId: string): Promise<boolean> {
    try {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();
      
      if (!user) {
        throw new Error('User not authenticated');
      }

      const response = await fetch(`/api/bookmarks?id=${bookmarkId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to remove bookmark');
      }

      // Clear cache to force refresh
      this.bookmarksCache.delete(user.id);
      
      return true;
    } catch (error) {
      console.error('Error removing bookmark:', error);
      return false;
    }
  }

  async toggleBookmark(node: any): Promise<boolean> {
    try {
      const bookmarks = await this.getUserBookmarks();
      const existingBookmark = bookmarks.find(b => b.node_id === node.id);

      if (existingBookmark) {
        // Remove bookmark
        return await this.removeBookmark(existingBookmark.id);
      } else {
        // Add bookmark
        const bookmark = await this.addBookmark({
          node_id: node.id,
          node_name: node.name,
          node_category: node.category || node.domain,
          node_difficulty: node.difficulty,
          node_points: node.points,
        });
        return bookmark !== null;
      }
    } catch (error) {
      console.error('Error toggling bookmark:', error);
      return false;
    }
  }

  async isBookmarked(nodeId: string): Promise<boolean> {
    try {
      const bookmarks = await this.getUserBookmarks();
      return bookmarks.some(b => b.node_id === nodeId);
    } catch (error) {
      console.error('Error checking bookmark status:', error);
      return false;
    }
  }

  async updateBookmarkNotes(bookmarkId: string, notes: string): Promise<boolean> {
    try {
      const response = await fetch('/api/bookmarks', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: bookmarkId, notes }),
      });

      if (!response.ok) {
        throw new Error('Failed to update bookmark notes');
      }

      // Clear cache to force refresh
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        this.bookmarksCache.delete(user.id);
      }
      
      return true;
    } catch (error) {
      console.error('Error updating bookmark notes:', error);
      return false;
    }
  }

  clearCache(): void {
    this.bookmarksCache.clear();
  }
}

export const bookmarkService = BookmarkService.getInstance();