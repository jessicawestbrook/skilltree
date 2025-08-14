import { NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';
import { getRateLimiter } from '@/lib/redis';

// Use general API rate limiter for session checks
const rateLimiter = getRateLimiter().api;

export async function GET(request: Request) {
  try {
    // Apply rate limiting
    const identifier = request.headers.get('x-forwarded-for') || 'anonymous';
    const { success, limit, reset, remaining } = await rateLimiter.limit(identifier);
    
    if (!success) {
      const response = NextResponse.json(
        { 
          error: 'Too many requests. Please try again later.', 
          retryAfter: Math.round((reset - Date.now()) / 1000) 
        },
        { status: 429 }
      );
      
      response.headers.set('X-RateLimit-Limit', limit.toString());
      response.headers.set('X-RateLimit-Remaining', remaining.toString());
      response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
      
      return response;
    }

    const supabase = await createServerSupabaseClient();
    
    const { data: { user }, error } = await supabase.auth.getUser();
    
    if (error || !user) {
      const response = NextResponse.json({ user: null });
      response.headers.set('X-RateLimit-Limit', limit.toString());
      response.headers.set('X-RateLimit-Remaining', remaining.toString());
      response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
      return response;
    }
    
    // Get user profile
    const { data: profile } = await supabase
      .from('user_profiles')
      .select('*')
      .eq('id', user.id)
      .single();
    
    const response = NextResponse.json({ 
      user: {
        id: user.id,
        email: user.email,
        ...profile
      }
    });
    
    response.headers.set('X-RateLimit-Limit', limit.toString());
    response.headers.set('X-RateLimit-Remaining', remaining.toString());
    response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
    
    return response;
  } catch (error) {
    console.error('Session check error:', error);
    return NextResponse.json({ user: null });
  }
}