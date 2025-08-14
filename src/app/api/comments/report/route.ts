import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST(request: NextRequest) {
  try {
    const { commentId, reason, description } = await request.json();

    if (!commentId || !reason) {
      return NextResponse.json(
        { error: 'Comment ID and reason are required' },
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

    // Check if user already reported this comment
    const { data: existingReport } = await supabase
      .from('comment_reports')
      .select('*')
      .eq('comment_id', commentId)
      .eq('reporter_id', user.id)
      .single();

    if (existingReport) {
      return NextResponse.json(
        { error: 'You have already reported this comment' },
        { status: 400 }
      );
    }

    // Create report
    const { data: report, error } = await supabase
      .from('comment_reports')
      .insert({
        comment_id: commentId,
        reporter_id: user.id,
        reason,
        description
      })
      .select()
      .single();

    if (error) {
      console.error('Error creating report:', error);
      return NextResponse.json(
        { error: 'Failed to create report' },
        { status: 500 }
      );
    }

    return NextResponse.json({ report });
  } catch (error) {
    console.error('Error in report API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}