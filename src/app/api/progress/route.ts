import { NextRequest, NextResponse } from 'next/server';
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';

export async function POST(request: NextRequest) {
  try {
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

    return NextResponse.json({
      success: true,
      data: progressData,
      message: existingProgress 
        ? 'Progress updated successfully' 
        : 'Progress recorded successfully'
    });

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

    let query = supabase
      .from('user_progress')
      .select('*')
      .eq('user_id', user.id);

    if (nodeId) {
      query = query.eq('node_id', nodeId);
    }

    const { data, error } = await query;

    if (error) throw error;

    return NextResponse.json({
      success: true,
      data
    });

  } catch (error) {
    console.error('Error fetching progress:', error);
    return NextResponse.json(
      { error: 'Failed to fetch progress' },
      { status: 500 }
    );
  }
}