import { NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

// Test endpoint to check friend suggestions without auth
export async function GET() {
  try {
    const supabase = await createServerSupabaseClient();

    // Get a sample of user profiles
    const { data: profiles, error } = await supabase
      .from('user_profiles')
      .select('id, username, neural_level, total_points')
      .limit(5);

    if (error) {
      console.error('Error fetching profiles:', error);
      return NextResponse.json({ 
        error: 'Failed to fetch profiles',
        details: error.message 
      }, { status: 500 });
    }

    // Mock suggestions for testing
    const suggestions = profiles?.map(p => ({
      suggested_user_id: p.id,
      username: p.username,
      neural_level: p.neural_level,
      total_points: p.total_points,
      common_groups: Math.floor(Math.random() * 3),
      common_nodes: Math.floor(Math.random() * 10) + 1
    })) || [];

    return NextResponse.json({ 
      success: true,
      suggestions,
      count: suggestions.length
    });
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}