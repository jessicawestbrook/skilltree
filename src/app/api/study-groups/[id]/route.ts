import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id: groupId } = await params;

    const supabase = await createServerSupabaseClient();

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Get group details with members
    const { data: group, error } = await supabase
      .from('study_groups')
      .select(`
        *,
        members:study_group_members(
          *,
          user:user_id(
            id,
            email,
            user_profiles!inner(
              username,
              avatar_url,
              bio,
              neural_level,
              total_points
            )
          )
        ),
        challenges:study_group_challenges(
          *,
          participants:study_group_challenge_participants(count)
        )
      `)
      .eq('id', groupId)
      .single();

    if (error) {
      console.error('Error fetching study group:', error);
      return NextResponse.json(
        { error: 'Study group not found' },
        { status: 404 }
      );
    }

    // Check if user is a member or if group is public
    const isMember = group.members.some((m: any) => m.user_id === user.id);
    if (!group.is_public && !isMember) {
      return NextResponse.json(
        { error: 'Access denied' },
        { status: 403 }
      );
    }

    return NextResponse.json({ data: group });
  } catch (error) {
    console.error('Error fetching study group:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id: groupId } = await params;
    const updates = await request.json();

    const supabase = await createServerSupabaseClient();

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Check if user is the owner
    const { data: group } = await supabase
      .from('study_groups')
      .select('owner_id')
      .eq('id', groupId)
      .single();

    if (!group || group.owner_id !== user.id) {
      return NextResponse.json(
        { error: 'Only the group owner can update the group' },
        { status: 403 }
      );
    }

    // Update the group
    const { data, error } = await supabase
      .from('study_groups')
      .update(updates)
      .eq('id', groupId)
      .select()
      .single();

    if (error) {
      console.error('Error updating study group:', error);
      return NextResponse.json(
        { error: 'Failed to update study group' },
        { status: 500 }
      );
    }

    return NextResponse.json({ data });
  } catch (error) {
    console.error('Error updating study group:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id: groupId } = await params;

    const supabase = await createServerSupabaseClient();

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Check if user is the owner
    const { data: group } = await supabase
      .from('study_groups')
      .select('owner_id, name')
      .eq('id', groupId)
      .single();

    if (!group || group.owner_id !== user.id) {
      return NextResponse.json(
        { error: 'Only the group owner can delete the group' },
        { status: 403 }
      );
    }

    // Delete the group (cascade will handle related records)
    const { error } = await supabase
      .from('study_groups')
      .delete()
      .eq('id', groupId);

    if (error) {
      console.error('Error deleting study group:', error);
      return NextResponse.json(
        { error: 'Failed to delete study group' },
        { status: 500 }
      );
    }

    // Create activity feed entry
    await supabase
      .from('activity_feed')
      .insert({
        user_id: user.id,
        activity_type: 'group_deleted',
        title: 'Deleted Study Group',
        description: `Deleted the study group "${group.name}"`,
        metadata: { group_name: group.name },
        visibility: 'private'
      });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error deleting study group:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}