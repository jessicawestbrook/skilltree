import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { sendVerificationEmail } from '@/services/emailService';
import { withRateLimit } from '@/lib/rateLimit';

function getSupabaseAdmin() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  
  if (!supabaseUrl) {
    throw new Error('Missing NEXT_PUBLIC_SUPABASE_URL environment variable');
  }
  
  // Check if we have a valid service role key (not placeholder)
  if (!serviceRoleKey || serviceRoleKey.includes('placeholder')) {
    console.warn('Service role key not configured - email verification disabled');
    return null;
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

export async function POST(request: NextRequest) {
  return withRateLimit(request, async () => {
  try {
    const { userId, email, username } = await request.json();

    if (!userId || !email) {
      return NextResponse.json(
        { error: 'User ID and email are required' },
        { status: 400 }
      );
    }

    // Get Supabase admin client
    const supabaseAdmin = getSupabaseAdmin();
    
    // If email service isn't configured, return success without sending email
    if (!supabaseAdmin) {
      console.log('Email service not configured - skipping verification email');
      return NextResponse.json({
        success: true,
        message: 'Registration successful (email verification disabled in development)',
        emailSkipped: true
      });
    }

    // Generate verification token using the database function
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
  }, 'auth-verification');
}