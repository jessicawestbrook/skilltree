import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { sendWelcomeEmail } from '@/services/emailService';

const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
);

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const token = searchParams.get('token');

    if (!token) {
      return NextResponse.json(
        { error: 'Verification token is required' },
        { status: 400 }
      );
    }

    // Verify the token using the database function
    const { data, error } = await supabaseAdmin
      .rpc('verify_email_with_token', {
        verification_token: token
      });

    if (error || !data || data.length === 0) {
      console.error('Verification error:', error);
      return NextResponse.json(
        { error: 'Invalid or expired verification token' },
        { status: 400 }
      );
    }

    const result = data[0];

    if (!result.success) {
      return NextResponse.json(
        { error: result.message },
        { status: 400 }
      );
    }

    // Get user details for welcome email
    const { data: userData } = await supabaseAdmin
      .from('user_profiles')
      .select('username')
      .eq('id', result.user_id)
      .single();

    // Send welcome email
    if (userData) {
      try {
        const { data: authUser } = await supabaseAdmin.auth.admin.getUserById(result.user_id);
        if (authUser?.user?.email) {
          await sendWelcomeEmail({
            email: authUser.user.email,
            username: userData.username || authUser.user.email.split('@')[0]
          });
        }
      } catch (emailError) {
        console.error('Failed to send welcome email:', emailError);
        // Don't fail the verification if welcome email fails
      }
    }

    return NextResponse.json({
      success: true,
      message: result.message,
      userId: result.user_id
    });

  } catch (error) {
    console.error('Email verification error:', error);
    return NextResponse.json(
      { error: 'Failed to verify email' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const { token } = await request.json();

    if (!token) {
      return NextResponse.json(
        { error: 'Verification token is required' },
        { status: 400 }
      );
    }

    // Verify the token using the database function
    const { data, error } = await supabaseAdmin
      .rpc('verify_email_with_token', {
        verification_token: token
      });

    if (error || !data || data.length === 0) {
      console.error('Verification error:', error);
      return NextResponse.json(
        { error: 'Invalid or expired verification token' },
        { status: 400 }
      );
    }

    const result = data[0];

    if (!result.success) {
      return NextResponse.json(
        { error: result.message },
        { status: 400 }
      );
    }

    // Get user details for welcome email
    const { data: userData } = await supabaseAdmin
      .from('user_profiles')
      .select('username')
      .eq('id', result.user_id)
      .single();

    // Send welcome email
    if (userData) {
      try {
        const { data: authUser } = await supabaseAdmin.auth.admin.getUserById(result.user_id);
        if (authUser?.user?.email) {
          await sendWelcomeEmail({
            email: authUser.user.email,
            username: userData.username || authUser.user.email.split('@')[0]
          });
        }
      } catch (emailError) {
        console.error('Failed to send welcome email:', emailError);
        // Don't fail the verification if welcome email fails
      }
    }

    return NextResponse.json({
      success: true,
      message: result.message,
      userId: result.user_id
    });

  } catch (error) {
    console.error('Email verification error:', error);
    return NextResponse.json(
      { error: 'Failed to verify email' },
      { status: 500 }
    );
  }
}