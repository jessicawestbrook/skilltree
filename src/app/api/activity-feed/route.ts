import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function GET(request: NextRequest) {
  try {
    const supabase = await createServerSupabaseClient();

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const searchParams = request.nextUrl.searchParams;
    const filter = searchParams.get('filter') || 'all';
    const limit = parseInt(searchParams.get('limit') || '20');
    const offset = parseInt(searchParams.get('offset') || '0');

    // Get user's friends for filtering
    const { data: friends } = await supabase
      .from('friends')
      .select('friend_id')
      .eq('user_id', user.id);

    const friendIds = friends?.map((f: { friend_id: string }) => f.friend_id) || [];

    // Get user's groups for filtering
    const { data: groups } = await supabase
      .from('study_group_members')
      .select('group_id')
      .eq('user_id', user.id);

    const groupIds = groups?.map((g: { group_id: string }) => g.group_id) || [];

    // Build the query
    let query = supabase
      .from('activity_feed')
      .select(`
        *,
        user:user_id(
          id,
          email,
          user_profiles!inner(
            username,
            avatar_url,
            neural_level
          )
        ),
        group:group_id(
          id,
          name
        )
      `);

    // Apply filters based on visibility and relationships
    if (filter === 'friends') {
      query = query.in('user_id', [...friendIds, user.id]);
    } else if (filter === 'groups') {
      query = query.in('group_id', groupIds);
    } else if (filter === 'personal') {
      query = query.eq('user_id', user.id);
    } else {
      // Show all relevant activities
      query = query.or(`
        visibility.eq.public,
        user_id.eq.${user.id},
        and(visibility.eq.friends,user_id.in.(${[...friendIds, user.id].join(',')})),
        and(visibility.eq.group,group_id.in.(${groupIds.join(',')}))
      `);
    }

    // Apply pagination and ordering
    const { data: activities, error, count } = await query
      .order('created_at', { ascending: false })
      .range(offset, offset + limit - 1);

    if (error) {
      console.error('Error fetching activity feed:', error);
      return NextResponse.json(
        { error: 'Failed to fetch activity feed' },
        { status: 500 }
      );
    }

    return NextResponse.json({ 
      data: activities || [],
      count: count || 0,
      hasMore: (count || 0) > offset + limit
    });
  } catch (error) {
    console.error('Error fetching activity feed:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const { activityType, title, description, metadata, visibility, groupId } = await request.json();

    if (!activityType || !title) {
      return NextResponse.json(
        { error: 'Activity type and title are required' },
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

    // Create activity feed entry
    const { data, error } = await supabase
      .from('activity_feed')
      .insert({
        user_id: user.id,
        activity_type: activityType,
        title,
        description,
        metadata: metadata || {},
        visibility: visibility || 'friends',
        group_id: groupId
      })
      .select()
      .single();

    if (error) {
      console.error('Error creating activity:', error);
      return NextResponse.json(
        { error: 'Failed to create activity' },
        { status: 500 }
      );
    }

    return NextResponse.json({ data });
  } catch (error) {
    console.error('Error creating activity:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}