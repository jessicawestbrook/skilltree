import { NextRequest, NextResponse } from 'next/server';
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { getRateLimiter, cache, cacheKeys, cacheTTL } from '@/lib/redis';

// Rate limiters
const apiRateLimiter = getRateLimiter().api;
const quizRateLimiter = getRateLimiter().quiz;

export async function POST(request: NextRequest) {
  try {
    // Apply rate limiting for quiz submissions
    const identifier = request.headers.get('x-forwarded-for') || 'anonymous';
    const { success, limit, reset, remaining } = await quizRateLimiter.limit(identifier);
    
    if (!success) {
      const response = NextResponse.json(
        { 
          error: 'Too many quiz attempts. Please try again later.', 
          retryAfter: Math.round((reset - Date.now()) / 1000) 
        },
        { status: 429 }
      );
      
      response.headers.set('X-RateLimit-Limit', limit.toString());
      response.headers.set('X-RateLimit-Remaining', remaining.toString());
      response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
      
      return response;
    }

    const supabase = createRouteHandlerClient({ cookies });
    
    // Check authentication
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const body = await request.json();
    const { nodeId, quiz_score, time_spent_seconds } = body;

    if (!nodeId || quiz_score === undefined) {
      return NextResponse.json(
        { error: 'Missing required fields: nodeId and quiz_score' },
        { status: 400 }
      );
    }

    // Calculate points based on quiz score
    const basePoints = 100;
    const points_earned = Math.round(basePoints * (quiz_score / 100));

    // Check if progress already exists
    const { data: existingProgress } = await supabase
      .from('user_progress')
      .select('*')
      .eq('user_id', user.id)
      .eq('node_id', nodeId)
      .single();

    let progressData;

    if (existingProgress) {
      // Update existing progress if new score is better
      if (quiz_score > (existingProgress.quiz_score || 0)) {
        const { data, error } = await supabase
          .from('user_progress')
          .update({
            quiz_score,
            points_earned,
            time_spent_seconds: time_spent_seconds || existingProgress.time_spent_seconds,
            completed_at: new Date().toISOString()
          })
          .eq('user_id', user.id)
          .eq('node_id', nodeId)
          .select()
          .single();

        if (error) throw error;
        progressData = data;
      } else {
        progressData = existingProgress;
      }
    } else {
      // Insert new progress
      const { data, error } = await supabase
        .from('user_progress')
        .insert({
          user_id: user.id,
          node_id: nodeId,
          quiz_score,
          points_earned,
          time_spent_seconds: time_spent_seconds || 0,
          completed_at: new Date().toISOString()
        })
        .select()
        .single();

      if (error) throw error;
      progressData = data;
    }

    // Update user profile stats
    const { error: profileError } = await supabase.rpc('update_user_stats', {
      p_user_id: user.id,
      p_points: points_earned,
      p_node_completed: !existingProgress
    });

    if (profileError) {
      console.error('Error updating user stats:', profileError);
    }

    // Invalidate related caches
    await Promise.all([
      cache.delete(cacheKeys.userProgress(user.id)),
      cache.delete(cacheKeys.userStats(user.id)),
      cache.delete(cacheKeys.nodeStats(nodeId))
    ]);

    const response = NextResponse.json({
      success: true,
      data: progressData,
      message: existingProgress 
        ? 'Progress updated successfully' 
        : 'Progress recorded successfully'
    });

    response.headers.set('X-RateLimit-Limit', limit.toString());
    response.headers.set('X-RateLimit-Remaining', remaining.toString());
    response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());

    return response;

  } catch (error) {
    console.error('Error recording progress:', error);
    return NextResponse.json(
      { error: 'Failed to record progress' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    // Apply general API rate limiting
    const identifier = request.headers.get('x-forwarded-for') || 'anonymous';
    const { success, limit, reset, remaining } = await apiRateLimiter.limit(identifier);
    
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

    const supabase = createRouteHandlerClient({ cookies });
    
    // Check authentication
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const { searchParams } = new URL(request.url);
    const nodeId = searchParams.get('nodeId');

    // Try to get from cache
    const cacheKey = nodeId 
      ? `${cacheKeys.userProgress(user.id)}:${nodeId}`
      : cacheKeys.userProgress(user.id);
    
    const cached = await cache.get(cacheKey);
    if (cached) {
      const response = NextResponse.json({
        success: true,
        data: cached
      });
      response.headers.set('X-Cache', 'HIT');
      response.headers.set('X-RateLimit-Limit', limit.toString());
      response.headers.set('X-RateLimit-Remaining', remaining.toString());
      response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
      return response;
    }

    let query = supabase
      .from('user_progress')
      .select('*')
      .eq('user_id', user.id);

    if (nodeId) {
      query = query.eq('node_id', nodeId);
    }

    const { data, error } = await query;

    if (error) throw error;

    // Cache the result
    await cache.set(cacheKey, data, cacheTTL.medium);

    const response = NextResponse.json({
      success: true,
      data
    });

    response.headers.set('X-Cache', 'MISS');
    response.headers.set('X-RateLimit-Limit', limit.toString());
    response.headers.set('X-RateLimit-Remaining', remaining.toString());
    response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());

    return response;

  } catch (error) {
    console.error('Error fetching progress:', error);
    return NextResponse.json(
      { error: 'Failed to fetch progress' },
      { status: 500 }
    );
  }
}