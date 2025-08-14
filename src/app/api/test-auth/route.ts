import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function GET(request: NextRequest) {
  try {
    const supabase = await createServerSupabaseClient();

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json({
        authenticated: false,
        error: authError?.message || 'No user found',
        user: null
      });
    }

    return NextResponse.json({
      authenticated: true,
      user: {
        id: user.id,
        email: user.email
      }
    });
  } catch (error) {
    console.error('Auth test error:', error);
    return NextResponse.json({
      authenticated: false,
      error: 'Server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}