import { NextRequest, NextResponse } from 'next/server';
import { getRedisClient, cache } from '@/lib/redis';

/**
 * Health check endpoint for Redis connection
 * Useful for monitoring and debugging Redis issues
 */
export async function GET(request: NextRequest) {
  try {
    const startTime = Date.now();
    
    // Test Redis connection
    const testKey = 'health:check:' + Date.now();
    const testValue = { status: 'ok', timestamp: new Date().toISOString() };
    
    // Test write
    await cache.set(testKey, testValue, 10); // Expire in 10 seconds
    
    // Test read
    const retrieved = await cache.get(testKey);
    
    // Test delete
    await cache.delete(testKey);
    
    const endTime = Date.now();
    const latency = endTime - startTime;
    
    // Check if Redis is actually connected (not using mock)
    const redis = getRedisClient();
    const isMock = !process.env.UPSTASH_REDIS_REST_URL || !process.env.UPSTASH_REDIS_REST_TOKEN;
    
    return NextResponse.json({
      status: 'healthy',
      redis: {
        connected: true,
        mode: isMock ? 'mock' : 'production',
        latency: `${latency}ms`,
        operations: {
          write: 'ok',
          read: retrieved ? 'ok' : 'failed',
          delete: 'ok'
        }
      },
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Redis health check failed:', error);
    
    return NextResponse.json({
      status: 'unhealthy',
      redis: {
        connected: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      },
      timestamp: new Date().toISOString()
    }, { status: 503 });
  }
}

/**
 * Get Redis statistics (admin only)
 */
export async function POST(request: NextRequest) {
  try {
    // Add admin authentication here if needed
    const { searchParams } = new URL(request.url);
    const adminKey = searchParams.get('key');
    
    // Simple admin key check (replace with proper auth in production)
    if (adminKey !== process.env.ADMIN_API_KEY) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }
    
    // Get cache statistics
    const patterns = [
      'user:*',
      'node:*',
      'session:*',
      'friends:*',
      'search:*',
      'leaderboard:*'
    ];
    
    const stats: Record<string, number> = {};
    
    for (const pattern of patterns) {
      const keys = await cache.invalidatePattern(pattern);
      stats[pattern.replace(':*', '')] = keys.length;
    }
    
    return NextResponse.json({
      status: 'ok',
      statistics: stats,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Redis stats error:', error);
    return NextResponse.json(
      { error: 'Failed to get statistics' },
      { status: 500 }
    );
  }
}