import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { sendVerificationEmail } from '@/services/emailService';

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
    const { userId, email, username } = await request.json();

    if (!userId || !email) {
      return NextResponse.json(
        { error: 'User ID and email are required' },
        { status: 400 }
      );
    }

    // Generate verification token using the database function
    const supabaseAdmin = getSupabaseAdmin();
    const { data: tokenData, error: tokenError } = await supabaseAdmin
      .rpc('generate_email_verification_token', {
        user_uuid: userId,
        user_email: email
      });

    if (tokenError || !tokenData || tokenData.length === 0) {
      console.error('Token generation error:', tokenError);
      return NextResponse.json(
        { error: 'Failed to generate verification token' },
        { status: 500 }
      );
    }

    const { token, expires_at } = tokenData[0];
    
    // Create verification link
    const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000';
    const verificationLink = `${baseUrl}/verify-email?token=${token}`;
    
    // Send verification email
    const emailResult = await sendVerificationEmail({
      email,
      username: username || email.split('@')[0],
      verificationLink,
      token
    });
    
    if (!emailResult.success) {
      console.error('Email sending failed:', emailResult.error);
      // Still return success if token was generated (user can request resend)
    }
    
    return NextResponse.json({
      success: true,
      message: 'Verification email sent successfully',
      expiresAt: expires_at
    });

  } catch (error) {
    console.error('Send verification error:', error);
    return NextResponse.json(
      { error: 'Failed to send verification email' },
      { status: 500 }
    );
  }
}