import { NextRequest, NextResponse } from 'next/server';
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { withRateLimit } from '@/lib/rateLimit';

// This endpoint is specifically for handling session end via sendBeacon
export async function POST(request: NextRequest) {
  return withRateLimit(request, async () => {
    try {
    const supabase = createRouteHandlerClient({ cookies });
    
    const body = await request.json();
    const { sessionId } = body;

    if (!sessionId) {
      return NextResponse.json(
        { error: 'Missing sessionId' },
        { status: 400 }
      );
    }

    // End the session without user verification since this is called on page unload
    const { error } = await supabase.rpc('end_learning_session', {
      p_session_id: sessionId
    });

    if (error) {
      console.error('Error ending session via beacon:', error);
      // Don't throw error since this is best-effort cleanup
    }

    return NextResponse.json({
      success: true
    });

    } catch (error) {
      console.error('Error in end-session endpoint:', error);
      // Return success anyway since this is cleanup
      return NextResponse.json({
        success: true
      });
    }
  }, 'api-relaxed');
}