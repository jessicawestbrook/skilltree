'use client';

import React, { useState, useEffect } from 'react';
import { Bookmark, BookmarkCheck } from 'lucide-react';
import { bookmarkService } from '@/services/bookmarkService';
import { useAuth } from '@/contexts/AuthContext';

interface BookmarkButtonProps {
  node: {
    id: string;
    name: string;
    category?: string;
    domain?: string;
    difficulty?: number;
    points?: number;
  };
  className?: string;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export default function BookmarkButton({ node, className = '', showLabel = false, size = 'md' }: BookmarkButtonProps) {
  const { isAuthenticated } = useAuth();
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      checkBookmarkStatus();
    }
  }, [node.id, isAuthenticated]);

  const checkBookmarkStatus = async () => {
    try {
      const bookmarked = await bookmarkService.isBookmarked(node.id);
      setIsBookmarked(bookmarked);
    } catch (error) {
      // Silently fail - assume not bookmarked
      setIsBookmarked(false);
    }
  };

  const handleToggleBookmark = async (e: React.MouseEvent) => {
    e.stopPropagation();
    
    if (!isAuthenticated) {
      // Could show auth modal here
      console.log('Please sign in to bookmark content');
      return;
    }

    setLoading(true);
    try {
      const success = await bookmarkService.toggleBookmark(node);
      if (success) {
        setIsBookmarked(!isBookmarked);
      }
    } catch (error) {
      console.error('Error toggling bookmark:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  const buttonClasses = {
    sm: 'p-1',
    md: 'p-1.5',
    lg: 'p-2'
  };

  return (
    <button
      onClick={handleToggleBookmark}
      disabled={loading}
      className={`${buttonClasses[size]} rounded-lg transition-all hover:bg-gray-100 dark:hover:bg-gray-700 ${
        isBookmarked 
          ? 'text-yellow-500 hover:text-yellow-600' 
          : 'text-gray-400 hover:text-gray-600 dark:hover:text-gray-300'
      } ${loading ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
      title={isBookmarked ? 'Remove bookmark' : 'Add bookmark'}
    >
      <div className="flex items-center gap-2">
        {isBookmarked ? (
          <BookmarkCheck className={sizeClasses[size]} />
        ) : (
          <Bookmark className={sizeClasses[size]} />
        )}
        {showLabel && (
          <span className="text-sm">
            {isBookmarked ? 'Bookmarked' : 'Bookmark'}
          </span>
        )}
      </div>
    </button>
  );
}