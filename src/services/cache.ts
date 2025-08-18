import { siteConfig } from '../config/site.config'

// Simple in-memory cache with TTL
interface CacheItem<T> {
  data: T
  timestamp: number
  ttl: number
}

class CacheService {
  private cache: Map<string, CacheItem<any>> = new Map()
  
  set<T>(key: string, data: T, ttlMs: number = siteConfig.learning.cacheTTL): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl: ttlMs
    })
  }
  
  get<T>(key: string): T | null {
    const item = this.cache.get(key)
    
    if (!item) {
      return null
    }
    
    // Check if cache has expired
    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key)
      return null
    }
    
    return item.data as T
  }
  
  clear(): void {
    this.cache.clear()
  }
  
  delete(key: string): void {
    this.cache.delete(key)
  }
  
  // Clean up expired items
  cleanup(): void {
    const now = Date.now()
    const entries = Array.from(this.cache.entries())
    for (const [key, item] of entries) {
      if (now - item.timestamp > item.ttl) {
        this.cache.delete(key)
      }
    }
  }
}

export const cacheService = new CacheService()

// Run cleanup every minute
setInterval(() => {
  cacheService.cleanup()
}, 60 * 1000)