import { NextRequest, NextResponse } from 'next/server';
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';

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
    const daysBack = parseInt(searchParams.get('days') || '30');
    const type = searchParams.get('type') || 'summary';

    switch (type) {
      case 'summary':
        const { data: analytics, error: analyticsError } = await supabase.rpc('get_user_analytics', {
          p_user_id: user.id,
          p_days_back: daysBack
        });

        if (analyticsError) {
          throw analyticsError;
        }

        return NextResponse.json({
          success: true,
          data: analytics?.[0] || null
        });

      case 'insights':
        const { data: insights, error: insightsError } = await supabase.rpc('generate_learning_insights', {
          p_user_id: user.id
        });

        if (insightsError) {
          throw insightsError;
        }

        return NextResponse.json({
          success: true,
          data: insights || []
        });

      case 'recommendations':
        // First generate recommendations
        const { error: genError } = await supabase.rpc('generate_recommendations', {
          p_user_id: user.id
        });

        if (genError) {
          console.error('Error generating recommendations:', genError);
        }

        // Then fetch them
        const { data: recommendations, error: recError } = await supabase
          .from('learning_recommendations')
          .select(`
            id,
            recommendation_type,
            node_id,
            priority_score,
            reasoning,
            created_at,
            knowledge_nodes!inner(name, domain, difficulty)
          `)
          .eq('user_id', user.id)
          .eq('is_active', true)
          .order('priority_score', { ascending: false })
          .limit(10);

        if (recError) {
          throw recError;
        }

        return NextResponse.json({
          success: true,
          data: recommendations || []
        });

      case 'sessions':
        const { data: sessions, error: sessionsError } = await supabase
          .from('learning_sessions')
          .select('*')
          .eq('user_id', user.id)
          .gte('session_start', new Date(Date.now() - daysBack * 24 * 60 * 60 * 1000).toISOString())
          .order('session_start', { ascending: false })
          .limit(100);

        if (sessionsError) {
          throw sessionsError;
        }

        return NextResponse.json({
          success: true,
          data: sessions || []
        });

      default:
        return NextResponse.json({
          error: 'Invalid analytics type'
        }, { status: 400 });
    }

  } catch (error) {
    console.error('Error fetching analytics:', error);
    return NextResponse.json(
      { error: 'Failed to fetch analytics data' },
      { status: 500 }
    );
  }
}

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
    const { event_type, node_id, event_data, session_id } = body;

    if (!event_type) {
      return NextResponse.json(
        { error: 'Missing event_type' },
        { status: 400 }
      );
    }

    // Track the event
    const { error } = await supabase.rpc('track_learning_event', {
      p_user_id: user.id,
      p_event_type: event_type,
      p_session_id: session_id,
      p_node_id: node_id,
      p_event_data: event_data || {}
    });

    if (error) {
      throw error;
    }

    return NextResponse.json({
      success: true,
      message: 'Event tracked successfully'
    });

  } catch (error) {
    console.error('Error tracking event:', error);
    return NextResponse.json(
      { error: 'Failed to track event' },
      { status: 500 }
    );
  }
}