import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';
import { getRateLimiter, cache, cacheKeys, cacheTTL } from '@/lib/redis';
import { withCache, withCacheInvalidation } from '@/middleware/cache';

// Rate limiter for comments
const rateLimiter = getRateLimiter().comments;

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const nodeId = searchParams.get('nodeId');

    if (!nodeId) {
      return NextResponse.json(
        { error: 'Node ID is required' },
        { status: 400 }
      );
    }

    // Check cache first
    const cacheKey = cacheKeys.nodeComments(nodeId);
    const cached = await cache.get(cacheKey);
    
    if (cached) {
      const response = NextResponse.json({ comments: cached });
      response.headers.set('X-Cache', 'HIT');
      return response;
    }

    const supabase = await createServerSupabaseClient();
    
    // Get comments with user info using the database function
    const { data: comments, error } = await supabase
      .rpc('get_node_comments_with_users', { p_node_id: nodeId });

    if (error) {
      console.error('Error fetching comments:', error);
      return NextResponse.json(
        { error: 'Failed to fetch comments' },
        { status: 500 }
      );
    }

    // Organize comments into tree structure
    const commentMap = new Map();
    const rootComments: any[] = [];

    comments?.forEach(comment => {
      commentMap.set(comment.id, { ...comment, replies: [] });
    });

    comments?.forEach(comment => {
      if (comment.parent_id) {
        const parent = commentMap.get(comment.parent_id);
        if (parent) {
          parent.replies.push(commentMap.get(comment.id));
        }
      } else {
        rootComments.push(commentMap.get(comment.id));
      }
    });

    // Cache the result
    await cache.set(cacheKey, rootComments, cacheTTL.medium);

    const response = NextResponse.json({ comments: rootComments });
    response.headers.set('X-Cache', 'MISS');
    return response;
  } catch (error) {
    console.error('Error in comments API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    // Apply rate limiting
    const identifier = request.headers.get('x-forwarded-for') || 'anonymous';
    const { success, limit, reset, remaining } = await rateLimiter.limit(identifier);
    
    if (!success) {
      const response = NextResponse.json(
        { 
          error: 'Too many comments. Please try again later.', 
          retryAfter: Math.round((reset - Date.now()) / 1000) 
        },
        { status: 429 }
      );
      
      response.headers.set('X-RateLimit-Limit', limit.toString());
      response.headers.set('X-RateLimit-Remaining', remaining.toString());
      response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
      
      return response;
    }

    const { nodeId, content, commentType = 'comment', parentId = null } = await request.json();

    if (!nodeId || !content) {
      return NextResponse.json(
        { error: 'Node ID and content are required' },
        { status: 400 }
      );
    }

    const supabase = await createServerSupabaseClient();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const { data: comment, error } = await supabase
      .from('node_comments')
      .insert({
        node_id: nodeId,
        user_id: user.id,
        parent_id: parentId,
        content,
        comment_type: commentType
      })
      .select(`
        *,
        user_profiles!node_comments_user_id_fkey(
          username,
          avatar_url
        )
      `)
      .single();

    if (error) {
      console.error('Error creating comment:', error);
      return NextResponse.json(
        { error: 'Failed to create comment' },
        { status: 500 }
      );
    }

    // Invalidate cache for this node's comments
    await cache.delete(cacheKeys.nodeComments(nodeId));

    const response = NextResponse.json({ comment });
    response.headers.set('X-RateLimit-Limit', limit.toString());
    response.headers.set('X-RateLimit-Remaining', remaining.toString());
    response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
    
    return response;
  } catch (error) {
    console.error('Error in comments API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PUT(request: NextRequest) {
  try {
    // Apply rate limiting
    const identifier = request.headers.get('x-forwarded-for') || 'anonymous';
    const { success, limit, reset, remaining } = await rateLimiter.limit(identifier);
    
    if (!success) {
      const response = NextResponse.json(
        { 
          error: 'Too many requests. Please try again later.', 
          retryAfter: Math.round((reset - Date.now()) / 1000) 
        },
        { status: 429 }
      );
      
      response.headers.set('X-RateLimit-Limit', limit.toString());
      response.headers.set('X-RateLimit-Remaining', remaining.toString());
      response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
      
      return response;
    }

    const { commentId, content } = await request.json();

    if (!commentId || !content) {
      return NextResponse.json(
        { error: 'Comment ID and content are required' },
        { status: 400 }
      );
    }

    const supabase = await createServerSupabaseClient();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Get the node ID for cache invalidation
    const { data: existingComment } = await supabase
      .from('node_comments')
      .select('node_id')
      .eq('id', commentId)
      .single();

    const { data: comment, error } = await supabase
      .from('node_comments')
      .update({ 
        content, 
        is_edited: true,
        updated_at: new Date().toISOString()
      })
      .eq('id', commentId)
      .eq('user_id', user.id)
      .select()
      .single();

    if (error) {
      console.error('Error updating comment:', error);
      return NextResponse.json(
        { error: 'Failed to update comment' },
        { status: 500 }
      );
    }

    // Invalidate cache for this node's comments
    if (existingComment?.node_id) {
      await cache.delete(cacheKeys.nodeComments(existingComment.node_id));
    }

    const response = NextResponse.json({ comment });
    response.headers.set('X-RateLimit-Limit', limit.toString());
    response.headers.set('X-RateLimit-Remaining', remaining.toString());
    response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
    
    return response;
  } catch (error) {
    console.error('Error in comments API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    // Apply rate limiting
    const identifier = request.headers.get('x-forwarded-for') || 'anonymous';
    const { success, limit, reset, remaining } = await rateLimiter.limit(identifier);
    
    if (!success) {
      const response = NextResponse.json(
        { 
          error: 'Too many requests. Please try again later.', 
          retryAfter: Math.round((reset - Date.now()) / 1000) 
        },
        { status: 429 }
      );
      
      response.headers.set('X-RateLimit-Limit', limit.toString());
      response.headers.set('X-RateLimit-Remaining', remaining.toString());
      response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
      
      return response;
    }

    const { searchParams } = new URL(request.url);
    const commentId = searchParams.get('commentId');

    if (!commentId) {
      return NextResponse.json(
        { error: 'Comment ID is required' },
        { status: 400 }
      );
    }

    const supabase = await createServerSupabaseClient();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Get the node ID for cache invalidation
    const { data: existingComment } = await supabase
      .from('node_comments')
      .select('node_id')
      .eq('id', commentId)
      .single();

    // Soft delete the comment
    const { error } = await supabase
      .from('node_comments')
      .update({ is_deleted: true })
      .eq('id', commentId)
      .eq('user_id', user.id);

    if (error) {
      console.error('Error deleting comment:', error);
      return NextResponse.json(
        { error: 'Failed to delete comment' },
        { status: 500 }
      );
    }

    // Invalidate cache for this node's comments
    if (existingComment?.node_id) {
      await cache.delete(cacheKeys.nodeComments(existingComment.node_id));
    }

    const response = NextResponse.json({ success: true });
    response.headers.set('X-RateLimit-Limit', limit.toString());
    response.headers.set('X-RateLimit-Remaining', remaining.toString());
    response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
    
    return response;
  } catch (error) {
    console.error('Error in comments API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}