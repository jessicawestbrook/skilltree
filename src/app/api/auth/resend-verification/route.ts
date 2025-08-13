import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

function getSupabaseAdmin() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  
  if (!supabaseUrl || !serviceRoleKey) {
    throw new Error('Missing Supabase environment variables');
  }
  
  return createClient(
    supabaseUrl,
    serviceRoleKey,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false
      }
    }
  );
}

export async function POST(request: Request) {
  try {
    const authHeader = request.headers.get('authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        { error: 'Authorization required' },
        { status: 401 }
      );
    }

    const token = authHeader.substring(7);

    // Get the user from the token
    const supabaseAdmin = getSupabaseAdmin();
    const { data: { user }, error: userError } = await supabaseAdmin.auth.getUser(token);

    if (userError || !user) {
      return NextResponse.json(
        { error: 'Invalid authentication' },
        { status: 401 }
      );
    }

    // Check if email is already verified
    const { data: isVerified, error: checkError } = await supabaseAdmin
      .rpc('is_email_verified', {
        user_uuid: user.id
      });

    if (checkError) {
      console.error('Verification check error:', checkError);
      return NextResponse.json(
        { error: 'Failed to check verification status' },
        { status: 500 }
      );
    }

    if (isVerified) {
      return NextResponse.json(
        { error: 'Email is already verified' },
        { status: 400 }
      );
    }

    // Generate new verification token
    const { data: tokenData, error: tokenError } = await supabaseAdmin
      .rpc('generate_email_verification_token', {
        user_uuid: user.id,
        user_email: user.email
      });

    if (tokenError || !tokenData || tokenData.length === 0) {
      console.error('Token generation error:', tokenError);
      return NextResponse.json(
        { error: 'Failed to generate verification token' },
        { status: 500 }
      );
    }

    const { token: verificationToken, expires_at } = tokenData[0];
    
    return NextResponse.json({
      success: true,
      token: verificationToken,
      expiresAt: expires_at,
      message: 'Verification email resent successfully'
    });

  } catch (error) {
    console.error('Resend verification error:', error);
    return NextResponse.json(
      { error: 'Failed to resend verification email' },
      { status: 500 }
    );
  }
}