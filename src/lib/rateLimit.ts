import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';
import { NextRequest, NextResponse } from 'next/server';

let redis: Redis | null = null;
let rateLimiters: Map<string, Ratelimit> | null = null;

function initializeRedis() {
  if (!redis && process.env.UPSTASH_REDIS_REST_URL && process.env.UPSTASH_REDIS_REST_TOKEN) {
    redis = new Redis({
      url: process.env.UPSTASH_REDIS_REST_URL,
      token: process.env.UPSTASH_REDIS_REST_TOKEN,
    });
  }
  return redis;
}

function initializeRateLimiters() {
  const redisInstance = initializeRedis();
  
  if (!redisInstance) {
    console.warn('Rate limiting disabled: Redis not configured');
    return null;
  }

  if (!rateLimiters) {
    rateLimiters = new Map([
      ['auth', new Ratelimit({
        redis: redisInstance,
        limiter: Ratelimit.slidingWindow(5, '1 m'),
        analytics: true,
        prefix: '@upstash/ratelimit/auth',
      })],
      ['auth-verification', new Ratelimit({
        redis: redisInstance,
        limiter: Ratelimit.slidingWindow(3, '10 m'),
        analytics: true,
        prefix: '@upstash/ratelimit/auth-verification',
      })],
      ['api-strict', new Ratelimit({
        redis: redisInstance,
        limiter: Ratelimit.slidingWindow(10, '1 m'),
        analytics: true,
        prefix: '@upstash/ratelimit/api-strict',
      })],
      ['api-moderate', new Ratelimit({
        redis: redisInstance,
        limiter: Ratelimit.slidingWindow(30, '1 m'),
        analytics: true,
        prefix: '@upstash/ratelimit/api-moderate',
      })],
      ['api-relaxed', new Ratelimit({
        redis: redisInstance,
        limiter: Ratelimit.slidingWindow(100, '1 m'),
        analytics: true,
        prefix: '@upstash/ratelimit/api-relaxed',
      })],
      ['notifications', new Ratelimit({
        redis: redisInstance,
        limiter: Ratelimit.slidingWindow(5, '5 m'),
        analytics: true,
        prefix: '@upstash/ratelimit/notifications',
      })],
    ]);
  }

  return rateLimiters;
}

export type RateLimitType = 'auth' | 'auth-verification' | 'api-strict' | 'api-moderate' | 'api-relaxed' | 'notifications';

export async function rateLimit(
  request: NextRequest,
  type: RateLimitType = 'api-moderate'
): Promise<{ success: boolean; limit?: number; reset?: number; remaining?: number } | null> {
  const limiters = initializeRateLimiters();
  
  if (!limiters) {
    return null;
  }

  const limiter = limiters.get(type);
  if (!limiter) {
    console.error(`Rate limiter type '${type}' not found`);
    return null;
  }

  const ip = request.headers.get('x-forwarded-for') ?? 
             request.headers.get('x-real-ip') ?? 
             'anonymous';

  try {
    const { success, limit, reset, remaining } = await limiter.limit(ip);
    return { success, limit, reset, remaining };
  } catch (error) {
    console.error('Rate limiting error:', error);
    return null;
  }
}

export function createRateLimitResponse(
  message: string = 'Too many requests',
  limit?: number,
  reset?: number,
  remaining?: number
): NextResponse {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  if (limit !== undefined) headers['X-RateLimit-Limit'] = limit.toString();
  if (remaining !== undefined) headers['X-RateLimit-Remaining'] = remaining.toString();
  if (reset !== undefined) headers['X-RateLimit-Reset'] = reset.toString();

  return new NextResponse(
    JSON.stringify({ error: message }),
    { status: 429, headers }
  );
}

export async function withRateLimit(
  request: NextRequest,
  handler: () => Promise<NextResponse>,
  type: RateLimitType = 'api-moderate'
): Promise<NextResponse> {
  const result = await rateLimit(request, type);
  
  if (result === null) {
    return handler();
  }

  if (!result.success) {
    return createRateLimitResponse(
      'Too many requests. Please try again later.',
      result.limit,
      result.reset,
      result.remaining
    );
  }

  const response = await handler();
  
  if (result.limit !== undefined) {
    response.headers.set('X-RateLimit-Limit', result.limit.toString());
  }
  if (result.remaining !== undefined) {
    response.headers.set('X-RateLimit-Remaining', result.remaining.toString());
  }
  if (result.reset !== undefined) {
    response.headers.set('X-RateLimit-Reset', result.reset.toString());
  }

  return response;
}