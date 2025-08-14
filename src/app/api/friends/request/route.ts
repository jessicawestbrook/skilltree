import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST(request: NextRequest) {
  try {
    const { receiverId, message } = await request.json();

    if (!receiverId) {
      return NextResponse.json(
        { error: 'Receiver ID is required' },
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

    // Check if request already exists
    const { data: existingRequest } = await supabase
      .from('friend_requests')
      .select('*')
      .or(`sender_id.eq.${user.id},receiver_id.eq.${user.id}`)
      .or(`sender_id.eq.${receiverId},receiver_id.eq.${receiverId}`)
      .single();

    if (existingRequest) {
      if (existingRequest.status === 'pending') {
        return NextResponse.json(
          { error: 'Friend request already pending' },
          { status: 400 }
        );
      }
      if (existingRequest.status === 'accepted') {
        return NextResponse.json(
          { error: 'Already friends' },
          { status: 400 }
        );
      }
    }

    // Create friend request
    const { data, error } = await supabase
      .from('friend_requests')
      .insert({
        sender_id: user.id,
        receiver_id: receiverId,
        message,
        status: 'pending'
      })
      .select()
      .single();

    if (error) {
      console.error('Error creating friend request:', error);
      return NextResponse.json(
        { error: 'Failed to send friend request' },
        { status: 500 }
      );
    }

    // Create activity feed entry
    await supabase
      .from('activity_feed')
      .insert({
        user_id: user.id,
        activity_type: 'friend_request_sent',
        title: 'Friend Request Sent',
        description: `Sent a friend request`,
        metadata: { receiver_id: receiverId },
        visibility: 'private'
      });

    return NextResponse.json({ data });
  } catch (error) {
    console.error('Error in friend request:', error);
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
    const type = searchParams.get('type') || 'all';

    let query = supabase
      .from('friend_requests')
      .select(`
        *,
        sender:sender_id(id, email),
        receiver:receiver_id(id, email)
      `);

    if (type === 'sent') {
      query = query.eq('sender_id', user.id);
    } else if (type === 'received') {
      query = query.eq('receiver_id', user.id);
    } else {
      query = query.or(`sender_id.eq.${user.id},receiver_id.eq.${user.id}`);
    }

    const { data, error } = await query.order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching friend requests:', error);
      console.error('Error details:', { 
        message: error.message, 
        code: error.code, 
        details: error.details,
        hint: error.hint 
      });
      return NextResponse.json(
        { error: 'Failed to fetch friend requests', details: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({ data });
  } catch (error) {
    console.error('Error fetching friend requests:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}