import { NextRequest, NextResponse } from 'next/server';
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { withRateLimit } from '@/lib/rateLimit';

export async function POST(request: NextRequest) {
  return withRateLimit(request, async () => {
    try {
    const supabase = createRouteHandlerClient({ cookies: await cookies() });
    
    // Check authentication
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const body = await request.json();
    const { action, session_id, duration_seconds } = body;

    if (action === 'start') {
      // Start a new session
      const userAgent = request.headers.get('user-agent') || '';
      const deviceType = detectDeviceType(userAgent);

      const { data: sessionId, error } = await supabase.rpc('start_learning_session', {
        p_user_id: user.id,
        p_user_agent: userAgent,
        p_device_type: deviceType
      });

      if (error) {
        throw error;
      }

      return NextResponse.json({
        success: true,
        session_id: sessionId
      });

    } else if (action === 'end') {
      // End existing session
      if (!session_id) {
        return NextResponse.json(
          { error: 'Missing session_id for end action' },
          { status: 400 }
        );
      }

      const { error } = await supabase.rpc('end_learning_session', {
        p_session_id: session_id,
        p_total_duration_seconds: duration_seconds
      });

      if (error) {
        throw error;
      }

      return NextResponse.json({
        success: true,
        message: 'Session ended successfully'
      });

    } else {
      return NextResponse.json(
        { error: 'Invalid action. Use "start" or "end"' },
        { status: 400 }
      );
    }

    } catch (error) {
      console.error('Error managing session:', error);
      return NextResponse.json(
        { error: 'Failed to manage session' },
        { status: 500 }
      );
    }
  }, 'api-relaxed');
}

function detectDeviceType(userAgent: string): string {
  const ua = userAgent.toLowerCase();
  
  if (/tablet|ipad|playbook|silk|(android(?!.*mobile))/.test(ua)) {
    return 'tablet';
  }
  
  if (/mobile|iphone|ipod|android|blackberry|opera|mini|windows\sce|palm|smartphone|iemobile/.test(ua)) {
    return 'mobile';
  }
  
  return 'desktop';
}