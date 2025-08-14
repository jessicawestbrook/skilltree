import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST(request: NextRequest) {
  try {
    const { commentId, voteType } = await request.json();

    if (!commentId || !['upvote', 'downvote'].includes(voteType)) {
      return NextResponse.json(
        { error: 'Valid comment ID and vote type are required' },
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

    // Check if user already voted
    const { data: existingVote } = await supabase
      .from('comment_votes')
      .select('*')
      .eq('comment_id', commentId)
      .eq('user_id', user.id)
      .single();

    if (existingVote) {
      if (existingVote.vote_type === voteType) {
        // Remove vote if clicking the same vote type
        const { error: deleteError } = await supabase
          .from('comment_votes')
          .delete()
          .eq('id', existingVote.id);

        if (deleteError) {
          console.error('Error removing vote:', deleteError);
          return NextResponse.json(
            { error: 'Failed to remove vote' },
            { status: 500 }
          );
        }

        return NextResponse.json({ action: 'removed', voteType });
      } else {
        // Update vote type
        const { error: updateError } = await supabase
          .from('comment_votes')
          .update({ vote_type: voteType })
          .eq('id', existingVote.id);

        if (updateError) {
          console.error('Error updating vote:', updateError);
          return NextResponse.json(
            { error: 'Failed to update vote' },
            { status: 500 }
          );
        }

        return NextResponse.json({ action: 'updated', voteType });
      }
    } else {
      // Create new vote
      const { error: insertError } = await supabase
        .from('comment_votes')
        .insert({
          comment_id: commentId,
          user_id: user.id,
          vote_type: voteType
        });

      if (insertError) {
        console.error('Error creating vote:', insertError);
        return NextResponse.json(
          { error: 'Failed to create vote' },
          { status: 500 }
        );
      }

      return NextResponse.json({ action: 'created', voteType });
    }
  } catch (error) {
    console.error('Error in vote API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}