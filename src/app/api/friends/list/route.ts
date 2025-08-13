import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function GET() {
  try {
    const supabase = await createServerSupabaseClient();

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Get all friends for the user
    const { data: friends, error } = await supabase
      .from('friends')
      .select(`
        *,
        friend:friend_id(
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
      `)
      .eq('user_id', user.id)
      .order('friendship_date', { ascending: false });

    if (error) {
      console.error('Error fetching friends:', error);
      return NextResponse.json(
        { error: 'Failed to fetch friends' },
        { status: 500 }
      );
    }

    // Get friend suggestions
    const { data: suggestions } = await supabase
      .rpc('get_friend_suggestions', { user_id: user.id })
      .limit(5);

    return NextResponse.json({ 
      friends: friends || [],
      suggestions: suggestions || []
    });
  } catch (error) {
    console.error('Error fetching friends:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { friendId } = await request.json();

    if (!friendId) {
      return NextResponse.json(
        { error: 'Friend ID is required' },
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

    // Delete both directions of the friendship
    const { error } = await supabase
      .from('friends')
      .delete()
      .or(`and(user_id.eq.${user.id},friend_id.eq.${friendId}),and(user_id.eq.${friendId},friend_id.eq.${user.id})`);

    if (error) {
      console.error('Error removing friend:', error);
      return NextResponse.json(
        { error: 'Failed to remove friend' },
        { status: 500 }
      );
    }

    // Update the friend request status
    await supabase
      .from('friend_requests')
      .update({ status: 'declined' })
      .or(`and(sender_id.eq.${user.id},receiver_id.eq.${friendId}),and(sender_id.eq.${friendId},receiver_id.eq.${user.id})`);

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error removing friend:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}