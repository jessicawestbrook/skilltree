import { NextRequest, NextResponse } from 'next/server';
import { cache, cacheKeys, cacheTTL } from '@/lib/redis';

interface CacheOptions {
  ttl?: number;
  key?: string | ((req: NextRequest) => string);
  invalidateOn?: string[];
  skipCache?: (req: NextRequest) => boolean;
}

/**
 * Cache middleware for API routes
 * Usage: wrap your API handler with this middleware
 */
export function withCache(
  handler: (req: NextRequest) => Promise<NextResponse>,
  options: CacheOptions = {}
) {
  return async (req: NextRequest): Promise<NextResponse> => {
    const { 
      ttl = cacheTTL.medium, 
      key, 
      skipCache 
    } = options;
    
    // Skip cache for non-GET requests
    if (req.method !== 'GET') {
      return handler(req);
    }
    
    // Check if we should skip cache
    if (skipCache && skipCache(req)) {
      return handler(req);
    }
    
    // Generate cache key
    const cacheKey = typeof key === 'function' 
      ? key(req)
      : key || generateCacheKey(req);
    
    // Try to get from cache
    const cached = await cache.get<any>(cacheKey);
    if (cached) {
      // Add cache hit header
      const response = NextResponse.json(cached);
      response.headers.set('X-Cache', 'HIT');
      response.headers.set('X-Cache-Key', cacheKey);
      return response;
    }
    
    // Execute handler
    const response = await handler(req);
    
    // Cache the response if successful
    if (response.ok) {
      const data = await response.json();
      await cache.set(cacheKey, data, ttl);
      
      // Create new response with cache headers
      const cachedResponse = NextResponse.json(data);
      cachedResponse.headers.set('X-Cache', 'MISS');
      cachedResponse.headers.set('X-Cache-Key', cacheKey);
      cachedResponse.headers.set('X-Cache-TTL', ttl.toString());
      
      return cachedResponse;
    }
    
    return response;
  };
}

/**
 * Invalidate cache middleware
 * Use this for mutations that should clear related caches
 */
export function withCacheInvalidation(
  handler: (req: NextRequest) => Promise<NextResponse>,
  patterns: string[] | ((req: NextRequest) => string[])
) {
  return async (req: NextRequest): Promise<NextResponse> => {
    const response = await handler(req);
    
    // Only invalidate on successful mutations
    if (response.ok && ['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method || '')) {
      const invalidationPatterns = typeof patterns === 'function' 
        ? patterns(req)
        : patterns;
      
      // Invalidate all matching patterns
      await Promise.all(
        invalidationPatterns.map(pattern => 
          cache.invalidatePattern(pattern)
        )
      );
    }
    
    return response;
  };
}

/**
 * Generate a cache key from request
 */
function generateCacheKey(req: NextRequest): string {
  const url = new URL(req.url);
  const params = Array.from(url.searchParams.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key}=${value}`)
    .join('&');
  
  return `api:${url.pathname}:${params}`;
}

/**
 * Cache decorator for class methods
 */
export function Cacheable(ttl: number = cacheTTL.medium) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    
    descriptor.value = async function (...args: any[]) {
      const cacheKey = `method:${target.constructor.name}:${propertyKey}:${JSON.stringify(args)}`;
      
      // Try to get from cache
      const cached = await cache.get(cacheKey);
      if (cached) {
        return cached;
      }
      
      // Execute original method
      const result = await originalMethod.apply(this, args);
      
      // Cache the result
      await cache.set(cacheKey, result, ttl);
      
      return result;
    };
    
    return descriptor;
  };
}

/**
 * Middleware to handle API rate limiting with Redis
 */
export function withRateLimit(
  limiter: any,
  identifier?: (req: NextRequest) => string
) {
  return async (
    handler: (req: NextRequest) => Promise<NextResponse>
  ) => {
    return async (req: NextRequest): Promise<NextResponse> => {
      // Get identifier (IP or user ID)
      const id = identifier 
        ? identifier(req)
        : req.ip || req.headers.get('x-forwarded-for') || 'anonymous';
      
      // Check rate limit
      const { success, limit, reset, remaining } = await limiter.limit(id);
      
      if (!success) {
        const response = NextResponse.json(
          { 
            error: 'Too many requests', 
            retryAfter: Math.round((reset - Date.now()) / 1000) 
          },
          { status: 429 }
        );
        
        response.headers.set('X-RateLimit-Limit', limit.toString());
        response.headers.set('X-RateLimit-Remaining', remaining.toString());
        response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
        
        return response;
      }
      
      // Execute handler
      const response = await handler(req);
      
      // Add rate limit headers
      response.headers.set('X-RateLimit-Limit', limit.toString());
      response.headers.set('X-RateLimit-Remaining', remaining.toString());
      response.headers.set('X-RateLimit-Reset', new Date(reset).toISOString());
      
      return response;
    };
  };
}