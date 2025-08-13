import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST(
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

    // Check if user is a member
    const { data: member } = await supabase
      .from('study_group_members')
      .select('role')
      .eq('group_id', groupId)
      .eq('user_id', user.id)
      .single();

    if (!member) {
      return NextResponse.json(
        { error: 'Not a member of this group' },
        { status: 400 }
      );
    }

    // Prevent owner from leaving (they must delete the group)
    if (member.role === 'owner') {
      return NextResponse.json(
        { error: 'Group owner cannot leave. Delete the group instead.' },
        { status: 400 }
      );
    }

    // Get group name for activity feed
    const { data: group } = await supabase
      .from('study_groups')
      .select('name')
      .eq('id', groupId)
      .single();

    // Remove member from group
    const { error } = await supabase
      .from('study_group_members')
      .delete()
      .eq('group_id', groupId)
      .eq('user_id', user.id);

    if (error) {
      console.error('Error leaving study group:', error);
      return NextResponse.json(
        { error: 'Failed to leave study group' },
        { status: 500 }
      );
    }

    // Create activity feed entry
    if (group) {
      await supabase
        .from('activity_feed')
        .insert({
          user_id: user.id,
          activity_type: 'group_left',
          title: 'Left Study Group',
          description: `Left the study group "${group.name}"`,
          metadata: { group_name: group.name },
          visibility: 'private'
        });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error leaving study group:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}