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

    // Get all friends for the user - simplified query first
    const { data: friends, error } = await supabase
      .from('friends')
      .select('*')
      .eq('user_id', user.id);

    if (error) {
      console.error('Error fetching friends from database:', error);
      console.error('Error details:', { 
        message: error.message, 
        code: error.code, 
        details: error.details,
        hint: error.hint 
      });
      return NextResponse.json(
        { error: 'Failed to fetch friends', details: error.message },
        { status: 500 }
      );
    }

    // Get friend suggestions - try the function first, fallback to simple query
    let suggestions = [];
    
    // First try the get_friend_suggestions function
    const { data: functionSuggestions, error: functionError } = await supabase
      .rpc('get_friend_suggestions', { p_user_id: user.id });
    
    console.log('Friend suggestions function attempt:', { 
      userId: user.id, 
      functionError: functionError?.message, 
      functionSuggestions 
    });
    
    if (!functionError && functionSuggestions && functionSuggestions.length > 0) {
      suggestions = functionSuggestions;
    } else {
      // Fallback: Get random users who aren't already friends
      console.log('Using fallback method for friend suggestions');
      
      const { data: existingFriends } = await supabase
        .from('friends')
        .select('friend_id')
        .eq('user_id', user.id);
      
      const friendIds = existingFriends?.map(f => f.friend_id) || [];
      
      // Get existing friend requests to exclude
      const { data: sentRequests } = await supabase
        .from('friend_requests')
        .select('receiver_id')
        .eq('sender_id', user.id);
      
      const { data: receivedRequests } = await supabase
        .from('friend_requests')
        .select('sender_id')
        .eq('receiver_id', user.id);
      
      const excludeIds = [
        ...friendIds,
        ...(sentRequests?.map(r => r.receiver_id) || []),
        ...(receivedRequests?.map(r => r.sender_id) || []),
        user.id // Exclude self
      ];
      
      // Build query to get other users
      let query = supabase
        .from('user_profiles')
        .select('id, username, neural_level, total_points');
      
      // Only add NOT IN clause if there are IDs to exclude
      if (excludeIds.length > 0) {
        // Use neq for each ID to avoid SQL injection issues
        for (const id of excludeIds) {
          query = query.neq('id', id);
        }
      }
      
      const { data: allUsers, error: usersError } = await query.limit(5);
      
      console.log('Fallback query result:', { 
        excludeIds, 
        allUsers, 
        usersError: usersError?.message 
      });
      
      suggestions = allUsers?.map(u => ({
        suggested_user_id: u.id,
        username: u.username,
        neural_level: u.neural_level,
        total_points: u.total_points,
        common_groups: 0,
        common_nodes: Math.floor(Math.random() * 10) + 1 // Mock common nodes for now
      })) || [];
    }
    
    console.log('Final suggestions:', suggestions);

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