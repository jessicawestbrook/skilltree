import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id: groupId } = await params;
    const { joinCode } = await request.json();

    const supabase = await createServerSupabaseClient();

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Check if already a member
    const { data: existingMember } = await supabase
      .from('study_group_members')
      .select('id')
      .eq('group_id', groupId)
      .eq('user_id', user.id)
      .single();

    if (existingMember) {
      return NextResponse.json(
        { error: 'Already a member of this group' },
        { status: 400 }
      );
    }

    // Get group details
    const { data: group } = await supabase
      .from('study_groups')
      .select('*')
      .eq('id', groupId)
      .single();

    if (!group) {
      return NextResponse.json(
        { error: 'Study group not found' },
        { status: 404 }
      );
    }

    // Check if group is private and join code is required
    if (!group.is_public && group.join_code !== joinCode) {
      return NextResponse.json(
        { error: 'Invalid join code' },
        { status: 403 }
      );
    }

    // Check if group is full
    const { count } = await supabase
      .from('study_group_members')
      .select('*', { count: 'exact', head: true })
      .eq('group_id', groupId);

    if (count && count >= group.max_members) {
      return NextResponse.json(
        { error: 'Group is full' },
        { status: 400 }
      );
    }

    // Add member to group
    const { data, error } = await supabase
      .from('study_group_members')
      .insert({
        group_id: groupId,
        user_id: user.id,
        role: 'member'
      })
      .select()
      .single();

    if (error) {
      console.error('Error joining study group:', error);
      return NextResponse.json(
        { error: 'Failed to join study group' },
        { status: 500 }
      );
    }

    // Create activity feed entry
    await supabase
      .from('activity_feed')
      .insert({
        user_id: user.id,
        activity_type: 'group_joined',
        title: 'Joined Study Group',
        description: `Joined the study group "${group.name}"`,
        metadata: { group_id: groupId, group_name: group.name },
        visibility: 'friends',
        group_id: groupId
      });

    return NextResponse.json({ data });
  } catch (error) {
    console.error('Error joining study group:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}