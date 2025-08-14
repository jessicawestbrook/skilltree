import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST(request: NextRequest) {
  try {
    const { userIds } = await request.json();
    
    if (!userIds || !Array.isArray(userIds) || userIds.length === 0) {
      return NextResponse.json(
        { error: 'User IDs array is required' },
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

    // Fetch user profiles
    const { data: profiles, error } = await supabase
      .from('user_profiles')
      .select('id, username, avatar_url, bio, neural_level, total_points')
      .in('id', userIds);

    if (error) {
      console.error('Error fetching profiles:', error);
      return NextResponse.json(
        { error: 'Failed to fetch profiles' },
        { status: 500 }
      );
    }

    // Map id to user_id for consistency with frontend
    const mappedProfiles = profiles?.map(p => ({
      ...p,
      user_id: p.id
    })) || [];
    
    return NextResponse.json({ profiles: mappedProfiles });
  } catch (error) {
    console.error('Error fetching profiles:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}