import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST(request: NextRequest) {
  try {
    const { name, description, isPublic, maxMembers } = await request.json();

    if (!name) {
      return NextResponse.json(
        { error: 'Group name is required' },
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

    // Create the study group
    const { data: group, error: groupError } = await supabase
      .from('study_groups')
      .insert({
        name,
        description,
        owner_id: user.id,
        is_public: isPublic ?? true,
        max_members: maxMembers || 20
      })
      .select()
      .single();

    if (groupError) {
      console.error('Error creating study group:', groupError);
      return NextResponse.json(
        { error: 'Failed to create study group' },
        { status: 500 }
      );
    }

    // Add the creator as the first member with owner role
    const { error: memberError } = await supabase
      .from('study_group_members')
      .insert({
        group_id: group.id,
        user_id: user.id,
        role: 'owner'
      });

    if (memberError) {
      console.error('Error adding owner as member:', memberError);
      // Rollback by deleting the group
      await supabase.from('study_groups').delete().eq('id', group.id);
      return NextResponse.json(
        { error: 'Failed to initialize study group' },
        { status: 500 }
      );
    }

    // Create activity feed entry
    await supabase
      .from('activity_feed')
      .insert({
        user_id: user.id,
        activity_type: 'group_created',
        title: 'Created Study Group',
        description: `Created the study group "${name}"`,
        metadata: { group_id: group.id, group_name: name },
        visibility: 'friends'
      });

    return NextResponse.json({ data: group });
  } catch (error) {
    console.error('Error creating study group:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

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

    let query = supabase
      .from('study_groups')
      .select(`
        *,
        members:study_group_members(count),
        user_member:study_group_members!inner(
          user_id,
          role
        )
      `);

    if (filter === 'my-groups') {
      // Groups the user is a member of
      query = query.eq('user_member.user_id', user.id);
    } else if (filter === 'public') {
      // Public groups
      query = query.eq('is_public', true);
    } else if (filter === 'owned') {
      // Groups owned by the user
      query = query.eq('owner_id', user.id);
    }

    const { data: groups, error } = await query
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching study groups:', error);
      return NextResponse.json(
        { error: 'Failed to fetch study groups' },
        { status: 500 }
      );
    }

    // Transform the data to include member count
    const transformedGroups = groups?.map((group: any) => ({
      ...group,
      member_count: group.members?.[0]?.count || 0,
      user_role: group.user_member?.[0]?.role || null
    }));

    return NextResponse.json({ data: transformedGroups || [] });
  } catch (error) {
    console.error('Error fetching study groups:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}