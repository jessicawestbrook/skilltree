import { NextRequest, NextResponse } from 'next/server';
import { SessionService } from '@/services/sessionService';
import { CacheInvalidationService } from '@/services/cacheInvalidationService';
import { headers } from 'next/headers';

/**
 * Cron job endpoint for periodic cleanup tasks
 * This should be called periodically (e.g., every hour) by a cron service
 * 
 * Example cron services:
 * - Vercel Cron Jobs
 * - GitHub Actions
 * - External cron services (cron-job.org, EasyCron)
 */
export async function GET(request: NextRequest) {
  try {
    // Optional: Add authentication for cron endpoints
    const headersList = headers();
    const cronSecret = headersList.get('x-cron-secret');
    
    // Uncomment to enable cron secret validation
    // if (cronSecret !== process.env.CRON_SECRET) {
    //   return NextResponse.json(
    //     { error: 'Unauthorized' },
    //     { status: 401 }
    //   );
    // }
    
    const results = {
      expiredSessions: 0,
      staleDataInvalidated: false,
      timestamp: new Date().toISOString(),
    };
    
    // Clean up expired sessions
    try {
      results.expiredSessions = await SessionService.cleanupExpiredSessions();
      console.log(`Cleaned up ${results.expiredSessions} expired sessions`);
    } catch (error) {
      console.error('Error cleaning up sessions:', error);
    }
    
    // Invalidate stale cached data
    try {
      await CacheInvalidationService.invalidateStaleData(24); // Data older than 24 hours
      results.staleDataInvalidated = true;
      console.log('Invalidated stale cached data');
    } catch (error) {
      console.error('Error invalidating stale data:', error);
    }
    
    return NextResponse.json({
      success: true,
      message: 'Cleanup tasks completed',
      results,
    });
    
  } catch (error) {
    console.error('Cron cleanup error:', error);
    return NextResponse.json(
      { 
        error: 'Cleanup tasks failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// Optional: POST endpoint for manual trigger
export async function POST(request: NextRequest) {
  // You might want to add admin authentication here
  return GET(request);
}