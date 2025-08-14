import { Redis } from '@upstash/redis';
import { Ratelimit } from '@upstash/ratelimit';

// Redis client configuration
const redisConfig = {
  url: process.env.UPSTASH_REDIS_REST_URL || '',
  token: process.env.UPSTASH_REDIS_REST_TOKEN || '',
};

// Create Redis client instance
let redis: Redis | null = null;

export function getRedisClient(): Redis {
  if (!redis) {
    if (!redisConfig.url || !redisConfig.token) {
      console.warn('Redis credentials not configured. Using mock cache.');
      // Return a mock Redis client for development without Redis
      return createMockRedis() as unknown as Redis;
    }
    
    redis = new Redis({
      url: redisConfig.url,
      token: redisConfig.token,
    });
  }
  
  return redis;
}

// Rate limiting configuration
export function getRateLimiter() {
  const redis = getRedisClient();
  
  // Create different rate limiters for different endpoints
  return {
    // General API rate limit: 100 requests per minute
    api: new Ratelimit({
      redis: redis as any,
      limiter: Ratelimit.slidingWindow(100, '1 m'),
      analytics: true,
      prefix: 'ratelimit:api',
    }),
    
    // Auth rate limit: 5 attempts per 15 minutes
    auth: new Ratelimit({
      redis: redis as any,
      limiter: Ratelimit.slidingWindow(5, '15 m'),
      analytics: true,
      prefix: 'ratelimit:auth',
    }),
    
    // Comments rate limit: 30 per hour
    comments: new Ratelimit({
      redis: redis as any,
      limiter: Ratelimit.slidingWindow(30, '1 h'),
      analytics: true,
      prefix: 'ratelimit:comments',
    }),
    
    // Quiz attempts: 10 per hour
    quiz: new Ratelimit({
      redis: redis as any,
      limiter: Ratelimit.slidingWindow(10, '1 h'),
      analytics: true,
      prefix: 'ratelimit:quiz',
    }),
  };
}

// Cache utility functions
export const cache = {
  async get<T>(key: string): Promise<T | null> {
    try {
      const redis = getRedisClient();
      const data = await redis.get(key);
      return data as T;
    } catch (error) {
      console.error('Redis get error:', error);
      return null;
    }
  },
  
  async set(key: string, value: any, expirationInSeconds?: number): Promise<void> {
    try {
      const redis = getRedisClient();
      if (expirationInSeconds) {
        await redis.set(key, value, { ex: expirationInSeconds });
      } else {
        await redis.set(key, value);
      }
    } catch (error) {
      console.error('Redis set error:', error);
    }
  },
  
  async delete(key: string): Promise<void> {
    try {
      const redis = getRedisClient();
      await redis.del(key);
    } catch (error) {
      console.error('Redis delete error:', error);
    }
  },
  
  async exists(key: string): Promise<boolean> {
    try {
      const redis = getRedisClient();
      const exists = await redis.exists(key);
      return exists === 1;
    } catch (error) {
      console.error('Redis exists error:', error);
      return false;
    }
  },
  
  async expire(key: string, seconds: number): Promise<void> {
    try {
      const redis = getRedisClient();
      await redis.expire(key, seconds);
    } catch (error) {
      console.error('Redis expire error:', error);
    }
  },
  
  // Pattern-based cache invalidation
  async invalidatePattern(pattern: string): Promise<string[]> {
    try {
      const redis = getRedisClient();
      const keys = await redis.keys(pattern);
      if (keys.length > 0) {
        await redis.del(...keys);
      }
      return keys;
    } catch (error) {
      console.error('Redis invalidate pattern error:', error);
      return [];
    }
  },
  
  // Increment counter (useful for view counts, etc.)
  async increment(key: string, amount = 1): Promise<number> {
    try {
      const redis = getRedisClient();
      const value = await redis.incrby(key, amount);
      return value;
    } catch (error) {
      console.error('Redis increment error:', error);
      return 0;
    }
  },
  
  // Get multiple keys at once
  async mget<T>(keys: string[]): Promise<(T | null)[]> {
    try {
      const redis = getRedisClient();
      const values = await redis.mget(...keys);
      return values as (T | null)[];
    } catch (error) {
      console.error('Redis mget error:', error);
      return keys.map(() => null);
    }
  },
};

// Cache key generators
export const cacheKeys = {
  // User-related cache keys
  user: (userId: string) => `user:${userId}`,
  userProfile: (userId: string) => `user:profile:${userId}`,
  userStats: (userId: string) => `user:stats:${userId}`,
  userProgress: (userId: string) => `user:progress:${userId}`,
  
  // Node-related cache keys
  node: (nodeId: string) => `node:${nodeId}`,
  nodeComments: (nodeId: string) => `node:comments:${nodeId}`,
  nodeQuiz: (nodeId: string) => `node:quiz:${nodeId}`,
  nodeStats: (nodeId: string) => `node:stats:${nodeId}`,
  
  // Learning path cache keys
  path: (pathId: string) => `path:${pathId}`,
  userPath: (userId: string, pathId: string) => `user:${userId}:path:${pathId}`,
  
  // Social features cache keys
  friends: (userId: string) => `friends:${userId}`,
  friendSuggestions: (userId: string) => `friends:suggestions:${userId}`,
  discussions: (page: number) => `discussions:page:${page}`,
  
  // Session cache keys
  session: (sessionId: string) => `session:${sessionId}`,
  
  // Leaderboard cache keys
  leaderboard: (type: string) => `leaderboard:${type}`,
  
  // Search cache keys
  search: (query: string) => `search:${query}`,
};

// Cache TTL (Time To Live) in seconds
export const cacheTTL = {
  short: 60, // 1 minute
  medium: 300, // 5 minutes
  long: 3600, // 1 hour
  day: 86400, // 24 hours
  week: 604800, // 7 days
};

// Mock Redis for development without Redis
function createMockRedis() {
  const store = new Map<string, any>();
  const expiry = new Map<string, number>();
  
  return {
    async get(key: string) {
      const expiryTime = expiry.get(key);
      if (expiryTime && Date.now() > expiryTime) {
        store.delete(key);
        expiry.delete(key);
        return null;
      }
      return store.get(key) || null;
    },
    
    async set(key: string, value: any, options?: { ex?: number }) {
      store.set(key, value);
      if (options?.ex) {
        expiry.set(key, Date.now() + options.ex * 1000);
      }
      return 'OK';
    },
    
    async del(...keys: string[]) {
      keys.forEach(key => {
        store.delete(key);
        expiry.delete(key);
      });
      return keys.length;
    },
    
    async exists(key: string) {
      const expiryTime = expiry.get(key);
      if (expiryTime && Date.now() > expiryTime) {
        store.delete(key);
        expiry.delete(key);
        return 0;
      }
      return store.has(key) ? 1 : 0;
    },
    
    async expire(key: string, seconds: number) {
      if (store.has(key)) {
        expiry.set(key, Date.now() + seconds * 1000);
        return 1;
      }
      return 0;
    },
    
    async keys(pattern: string) {
      const regex = new RegExp(pattern.replace(/\*/g, '.*'));
      return Array.from(store.keys()).filter(key => regex.test(key));
    },
    
    async incrby(key: string, amount: number) {
      const current = store.get(key) || 0;
      const newValue = current + amount;
      store.set(key, newValue);
      return newValue;
    },
    
    async mget(...keys: string[]) {
      return keys.map(key => this.get(key));
    },
  };
}