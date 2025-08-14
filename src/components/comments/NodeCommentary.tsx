'use client';

import React, { useState, useEffect } from 'react';
import { MessageSquare, ThumbsUp, ThumbsDown, Reply, Edit2, Trash2, MoreVertical, Flag, BookOpen, Lightbulb, HelpCircle, Send, X } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { formatDistanceToNow } from 'date-fns';

interface Comment {
  id: string;
  node_id: string;
  user_id: string;
  parent_id: string | null;
  content: string;
  comment_type: 'comment' | 'note' | 'insight' | 'question';
  is_edited: boolean;
  upvotes: number;
  downvotes: number;
  created_at: string;
  updated_at: string;
  username: string;
  avatar_url: string;
  user_voted: 'upvote' | 'downvote' | null;
  reply_count: number;
  replies?: Comment[];
}

interface NodeCommentaryProps {
  nodeId: string;
  nodeName: string;
}

export default function NodeCommentary({ nodeId, nodeName }: NodeCommentaryProps) {
  const { user } = useAuth();
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [newComment, setNewComment] = useState('');
  const [commentType, setCommentType] = useState<'comment' | 'note' | 'insight' | 'question'>('comment');
  const [replyingTo, setReplyingTo] = useState<string | null>(null);
  const [replyContent, setReplyContent] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editContent, setEditContent] = useState('');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<string | null>(null);

  useEffect(() => {
    fetchComments();
  }, [nodeId]);

  const fetchComments = async () => {
    try {
      const response = await fetch(`/api/comments?nodeId=${nodeId}`);
      if (response.ok) {
        const data = await response.json();
        setComments(data.comments || []);
      }
    } catch (error) {
      console.error('Error fetching comments:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim() || !user) return;

    try {
      const response = await fetch('/api/comments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nodeId,
          content: newComment,
          commentType,
          parentId: null
        })
      });

      if (response.ok) {
        setNewComment('');
        await fetchComments();
      }
    } catch (error) {
      console.error('Error posting comment:', error);
    }
  };

  const handleSubmitReply = async (parentId: string) => {
    if (!replyContent.trim() || !user) return;

    try {
      const response = await fetch('/api/comments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nodeId,
          content: replyContent,
          commentType: 'comment',
          parentId
        })
      });

      if (response.ok) {
        setReplyContent('');
        setReplyingTo(null);
        await fetchComments();
      }
    } catch (error) {
      console.error('Error posting reply:', error);
    }
  };

  const handleVote = async (commentId: string, voteType: 'upvote' | 'downvote') => {
    if (!user) return;

    try {
      const response = await fetch('/api/comments/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ commentId, voteType })
      });

      if (response.ok) {
        await fetchComments();
      }
    } catch (error) {
      console.error('Error voting:', error);
    }
  };

  const handleEdit = async (commentId: string) => {
    if (!editContent.trim()) return;

    try {
      const response = await fetch('/api/comments', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          commentId,
          content: editContent
        })
      });

      if (response.ok) {
        setEditingId(null);
        setEditContent('');
        await fetchComments();
      }
    } catch (error) {
      console.error('Error editing comment:', error);
    }
  };

  const handleDelete = async (commentId: string) => {
    try {
      const response = await fetch(`/api/comments?commentId=${commentId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setShowDeleteConfirm(null);
        await fetchComments();
      }
    } catch (error) {
      console.error('Error deleting comment:', error);
    }
  };

  const getCommentTypeIcon = (type: string) => {
    switch (type) {
      case 'note': return <BookOpen className="w-4 h-4" />;
      case 'insight': return <Lightbulb className="w-4 h-4" />;
      case 'question': return <HelpCircle className="w-4 h-4" />;
      default: return <MessageSquare className="w-4 h-4" />;
    }
  };

  const getCommentTypeColor = (type: string) => {
    switch (type) {
      case 'note': return 'text-blue-600 bg-blue-50';
      case 'insight': return 'text-yellow-600 bg-yellow-50';
      case 'question': return 'text-purple-600 bg-purple-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const renderComment = (comment: Comment, isReply = false) => (
    <div key={comment.id} className={`${isReply ? 'ml-12' : ''} mb-4`}>
      <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            {comment.avatar_url ? (
              <img 
                src={comment.avatar_url} 
                alt={comment.username}
                className="w-10 h-10 rounded-full"
              />
            ) : (
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold">
                {comment.username[0]?.toUpperCase()}
              </div>
            )}
          </div>
          
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-semibold text-gray-900 dark:text-gray-100">
                {comment.username}
              </span>
              <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs ${getCommentTypeColor(comment.comment_type)}`}>
                {getCommentTypeIcon(comment.comment_type)}
                {comment.comment_type}
              </span>
              <span className="text-xs text-gray-500">
                {formatDistanceToNow(new Date(comment.created_at), { addSuffix: true })}
              </span>
              {comment.is_edited && (
                <span className="text-xs text-gray-400">(edited)</span>
              )}
            </div>

            {editingId === comment.id ? (
              <div className="mt-2">
                <textarea
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 resize-none"
                  rows={3}
                />
                <div className="flex gap-2 mt-2">
                  <button
                    onClick={() => handleEdit(comment.id)}
                    className="px-3 py-1 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm"
                  >
                    Save
                  </button>
                  <button
                    onClick={() => {
                      setEditingId(null);
                      setEditContent('');
                    }}
                    className="px-3 py-1 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 text-sm"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
                {comment.content}
              </p>
            )}

            <div className="flex items-center gap-4 mt-3">
              <button
                onClick={() => handleVote(comment.id, 'upvote')}
                className={`flex items-center gap-1 text-sm ${
                  comment.user_voted === 'upvote' 
                    ? 'text-green-600' 
                    : 'text-gray-500 hover:text-green-600'
                }`}
              >
                <ThumbsUp className="w-4 h-4" />
                {comment.upvotes}
              </button>
              
              <button
                onClick={() => handleVote(comment.id, 'downvote')}
                className={`flex items-center gap-1 text-sm ${
                  comment.user_voted === 'downvote' 
                    ? 'text-red-600' 
                    : 'text-gray-500 hover:text-red-600'
                }`}
              >
                <ThumbsDown className="w-4 h-4" />
                {comment.downvotes}
              </button>

              {!isReply && (
                <button
                  onClick={() => {
                    setReplyingTo(comment.id);
                    setReplyContent('');
                  }}
                  className="flex items-center gap-1 text-sm text-gray-500 hover:text-purple-600"
                >
                  <Reply className="w-4 h-4" />
                  Reply {comment.reply_count > 0 && `(${comment.reply_count})`}
                </button>
              )}

              {user && user.id === comment.user_id && (
                <>
                  <button
                    onClick={() => {
                      setEditingId(comment.id);
                      setEditContent(comment.content);
                    }}
                    className="flex items-center gap-1 text-sm text-gray-500 hover:text-blue-600"
                  >
                    <Edit2 className="w-4 h-4" />
                    Edit
                  </button>
                  
                  <button
                    onClick={() => setShowDeleteConfirm(comment.id)}
                    className="flex items-center gap-1 text-sm text-gray-500 hover:text-red-600"
                  >
                    <Trash2 className="w-4 h-4" />
                    Delete
                  </button>
                </>
              )}
            </div>

            {showDeleteConfirm === comment.id && (
              <div className="mt-3 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                <p className="text-sm text-red-600 dark:text-red-400 mb-2">
                  Are you sure you want to delete this comment?
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleDelete(comment.id)}
                    className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
                  >
                    Delete
                  </button>
                  <button
                    onClick={() => setShowDeleteConfirm(null)}
                    className="px-3 py-1 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded text-sm hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {replyingTo === comment.id && (
              <div className="mt-3">
                <textarea
                  value={replyContent}
                  onChange={(e) => setReplyContent(e.target.value)}
                  placeholder="Write a reply..."
                  className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 resize-none"
                  rows={3}
                />
                <div className="flex gap-2 mt-2">
                  <button
                    onClick={() => handleSubmitReply(comment.id)}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm"
                  >
                    Reply
                  </button>
                  <button
                    onClick={() => {
                      setReplyingTo(null);
                      setReplyContent('');
                    }}
                    className="px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-400 text-sm"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {comment.replies && comment.replies.length > 0 && (
        <div className="mt-2">
          {comment.replies.map(reply => renderComment(reply, true))}
        </div>
      )}
    </div>
  );

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2 flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-purple-600" />
          Community Commentary
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Share your insights, ask questions, and learn from others studying {nodeName}
        </p>
      </div>

      {user ? (
        <form onSubmit={handleSubmitComment} className="mb-6">
          <div className="mb-3">
            <div className="flex gap-2 mb-3">
              {(['comment', 'note', 'insight', 'question'] as const).map(type => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setCommentType(type)}
                  className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm transition-all ${
                    commentType === type
                      ? getCommentTypeColor(type)
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {getCommentTypeIcon(type)}
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </button>
              ))}
            </div>
            
            <textarea
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder={
                commentType === 'question' ? "Ask a question about this topic..." :
                commentType === 'note' ? "Add a personal note or reminder..." :
                commentType === 'insight' ? "Share an insight or tip..." :
                "Share your thoughts..."
              }
              className="w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 resize-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              rows={4}
            />
          </div>
          
          <button
            type="submit"
            disabled={!newComment.trim()}
            className="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
            Post {commentType.charAt(0).toUpperCase() + commentType.slice(1)}
          </button>
        </form>
      ) : (
        <div className="mb-6 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg text-center">
          <p className="text-gray-600 dark:text-gray-400">
            Please log in to add comments and join the discussion
          </p>
        </div>
      )}

      <div className="space-y-4">
        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          </div>
        ) : comments.length > 0 ? (
          comments.map(comment => renderComment(comment))
        ) : (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            <MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>No comments yet. Be the first to share your thoughts!</p>
          </div>
        )}
      </div>
    </div>
  );
}