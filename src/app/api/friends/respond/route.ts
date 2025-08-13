import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST(request: NextRequest) {
  try {
    const { requestId, action } = await request.json();

    if (!requestId || !action) {
      return NextResponse.json(
        { error: 'Request ID and action are required' },
        { status: 400 }
      );
    }

    if (!['accepted', 'declined', 'blocked'].includes(action)) {
      return NextResponse.json(
        { error: 'Invalid action' },
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

    // Verify the request belongs to the user
    const { data: friendRequest, error: fetchError } = await supabase
      .from('friend_requests')
      .select('*')
      .eq('id', requestId)
      .eq('receiver_id', user.id)
      .single();

    if (fetchError || !friendRequest) {
      return NextResponse.json(
        { error: 'Friend request not found' },
        { status: 404 }
      );
    }

    // Update the request status
    const { data, error } = await supabase
      .from('friend_requests')
      .update({
        status: action,
        responded_at: new Date().toISOString()
      })
      .eq('id', requestId)
      .select()
      .single();

    if (error) {
      console.error('Error updating friend request:', error);
      return NextResponse.json(
        { error: 'Failed to respond to friend request' },
        { status: 500 }
      );
    }

    // If accepted, the database trigger will create the friendship automatically
    // Create activity feed entry
    if (action === 'accepted') {
      await supabase
        .from('activity_feed')
        .insert({
          user_id: user.id,
          activity_type: 'friend_request_accepted',
          title: 'New Friend!',
          description: 'Accepted a friend request',
          metadata: { friend_id: friendRequest.sender_id },
          visibility: 'friends'
        });
    }

    return NextResponse.json({ data });
  } catch (error) {
    console.error('Error responding to friend request:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}