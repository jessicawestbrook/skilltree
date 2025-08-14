import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';
import { withRateLimit } from '@/lib/rateLimit';

export async function GET(request: NextRequest) {
  return withRateLimit(request, async () => {
    try {
    const supabase = await createServerSupabaseClient();
    
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
        try {
          const { data: analytics, error: analyticsError } = await supabase.rpc('get_user_analytics', {
            p_user_id: user.id,
            p_days_back: daysBack
          });
          
          if (analyticsError) {
            console.error('Analytics RPC Error:', analyticsError);
            // Return mock data if RPC function doesn't exist
            return NextResponse.json({
              data: {
                total_nodes_completed: 0,
                total_points: 0,
                current_streak: 0,
                avg_quiz_score: 0,
                learning_time_hours: 0,
                nodes_this_week: 0,
                improvement_rate: 0
              }
            });
          }

          return NextResponse.json({
            success: true,
            data: analytics?.[0] || null
          });
        } catch (error) {
          console.error('Error in summary analytics:', error);
          return NextResponse.json(
            { error: 'Failed to fetch analytics' },
            { status: 500 }
          );
        }

      case 'insights':
        try {
          const { data: insights, error: insightsError } = await supabase.rpc('generate_learning_insights', {
            p_user_id: user.id
          });

          if (insightsError) {
            console.error('Insights RPC Error:', insightsError);
            // Return empty insights if RPC function doesn't exist
            return NextResponse.json({
              success: true,
              data: []
            });
          }

          return NextResponse.json({
            success: true,
            data: Array.isArray(insights) ? insights : []
          });
        } catch (error) {
          console.error('Insights error:', error);
          return NextResponse.json({
            success: true,
            data: []
          });
        }

      case 'recommendations':
        try {
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
            console.error('Recommendations fetch error:', recError);
            return NextResponse.json({
              success: true,
              data: []
            });
          }

          return NextResponse.json({
            success: true,
            data: Array.isArray(recommendations) ? recommendations : []
          });
        } catch (error) {
          console.error('Recommendations error:', error);
          return NextResponse.json({
            success: true,
            data: []
          });
        }

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
          data: Array.isArray(sessions) ? sessions : []
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
  }, 'api-moderate');
}

export async function POST(request: NextRequest) {
  return withRateLimit(request, async () => {
    try {
    const supabase = await createServerSupabaseClient();
    
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
  }, 'api-moderate');
}