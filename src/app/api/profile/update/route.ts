import { NextRequest, NextResponse } from 'next/server';
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';

export async function POST(request: NextRequest) {
  try {
    const supabase = createRouteHandlerClient({ cookies });
    
    // Get the authenticated user
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Parse the request body
    const body = await request.json();
    const { birthYear, ...otherUpdates } = body;

    // Update user metadata in auth.users
    if (birthYear !== undefined) {
      const { error: updateError } = await supabase.auth.updateUser({
        data: { birthYear }
      });

      if (updateError) {
        console.error('Error updating user metadata:', updateError);
        return NextResponse.json(
          { error: 'Failed to update user metadata' },
          { status: 500 }
        );
      }
    }

    // Update user_profiles table
    const { data, error: profileError } = await supabase
      .from('user_profiles')
      .upsert({
        id: user.id,
        birth_year: birthYear,
        ...otherUpdates,
        updated_at: new Date().toISOString()
      }, {
        onConflict: 'id'
      })
      .select()
      .single();

    if (profileError) {
      console.error('Error updating profile:', profileError);
      return NextResponse.json(
        { error: 'Failed to update profile' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      profile: data
    });

  } catch (error) {
    console.error('Profile update error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const supabase = createRouteHandlerClient({ cookies });
    
    // Get the authenticated user
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Get user profile with calculated age
    const { data, error } = await supabase
      .from('age_groups')
      .select('*')
      .eq('user_id', user.id)
      .single();

    if (error && error.code !== 'PGRST116') { // Ignore "no rows" error
      console.error('Error fetching profile:', error);
      return NextResponse.json(
        { error: 'Failed to fetch profile' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      profile: data || null,
      userMetadata: {
        birthYear: user.user_metadata?.birthYear
      }
    });

  } catch (error) {
    console.error('Profile fetch error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}