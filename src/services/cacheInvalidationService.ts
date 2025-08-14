import { cache, cacheKeys } from '@/lib/redis';

/**
 * Service for managing cache invalidation strategies
 * Ensures data consistency across the application
 */
export class CacheInvalidationService {
  
  /**
   * Invalidate all caches related to a user
   */
  static async invalidateUserCaches(userId: string): Promise<void> {
    await Promise.all([
      cache.delete(cacheKeys.user(userId)),
      cache.delete(cacheKeys.userProfile(userId)),
      cache.delete(cacheKeys.userStats(userId)),
      cache.delete(cacheKeys.userProgress(userId)),
      cache.delete(cacheKeys.friends(userId)),
      cache.delete(cacheKeys.friendSuggestions(userId)),
      cache.invalidatePattern(`user:${userId}:*`),
    ]);
  }
  
  /**
   * Invalidate all caches related to a node
   */
  static async invalidateNodeCaches(nodeId: string): Promise<void> {
    await Promise.all([
      cache.delete(cacheKeys.node(nodeId)),
      cache.delete(cacheKeys.nodeComments(nodeId)),
      cache.delete(cacheKeys.nodeQuiz(nodeId)),
      cache.delete(cacheKeys.nodeStats(nodeId)),
      cache.invalidatePattern(`node:${nodeId}:*`),
    ]);
  }
  
  /**
   * Invalidate learning path caches
   */
  static async invalidatePathCaches(pathId: string, userId?: string): Promise<void> {
    const promises = [
      cache.delete(cacheKeys.path(pathId)),
      cache.invalidatePattern(`path:${pathId}:*`),
    ];
    
    if (userId) {
      promises.push(
        cache.delete(cacheKeys.userPath(userId, pathId))
      );
    }
    
    await Promise.all(promises);
  }
  
  /**
   * Invalidate social feature caches
   */
  static async invalidateSocialCaches(userId: string): Promise<void> {
    await Promise.all([
      cache.delete(cacheKeys.friends(userId)),
      cache.delete(cacheKeys.friendSuggestions(userId)),
      // Invalidate activity feed for friends
      cache.invalidatePattern(`friends:${userId}:*`),
    ]);
  }
  
  /**
   * Invalidate discussion/forum caches
   */
  static async invalidateDiscussionCaches(page?: number): Promise<void> {
    if (page !== undefined) {
      await cache.delete(cacheKeys.discussions(page));
    } else {
      // Invalidate all discussion pages
      await cache.invalidatePattern('discussions:page:*');
    }
  }
  
  /**
   * Invalidate leaderboard caches
   */
  static async invalidateLeaderboardCaches(type?: string): Promise<void> {
    if (type) {
      await cache.delete(cacheKeys.leaderboard(type));
    } else {
      // Invalidate all leaderboard types
      await cache.invalidatePattern('leaderboard:*');
    }
  }
  
  /**
   * Invalidate search caches
   */
  static async invalidateSearchCaches(query?: string): Promise<void> {
    if (query) {
      await cache.delete(cacheKeys.search(query));
    } else {
      // Invalidate all search results
      await cache.invalidatePattern('search:*');
    }
  }
  
  /**
   * Invalidate caches after user profile update
   */
  static async onUserProfileUpdate(userId: string): Promise<void> {
    await Promise.all([
      this.invalidateUserCaches(userId),
      this.invalidateLeaderboardCaches(),
      this.invalidateSocialCaches(userId),
    ]);
  }
  
  /**
   * Invalidate caches after progress update
   */
  static async onProgressUpdate(userId: string, nodeId: string): Promise<void> {
    await Promise.all([
      cache.delete(cacheKeys.userProgress(userId)),
      cache.delete(cacheKeys.userStats(userId)),
      cache.delete(cacheKeys.nodeStats(nodeId)),
      this.invalidateLeaderboardCaches(),
    ]);
  }
  
  /**
   * Invalidate caches after comment action
   */
  static async onCommentAction(nodeId: string): Promise<void> {
    await Promise.all([
      cache.delete(cacheKeys.nodeComments(nodeId)),
      cache.delete(cacheKeys.nodeStats(nodeId)),
    ]);
  }
  
  /**
   * Invalidate caches after friend action
   */
  static async onFriendAction(userId1: string, userId2: string): Promise<void> {
    await Promise.all([
      this.invalidateSocialCaches(userId1),
      this.invalidateSocialCaches(userId2),
      cache.invalidatePattern(`activity-feed:${userId1}:*`),
      cache.invalidatePattern(`activity-feed:${userId2}:*`),
    ]);
  }
  
  /**
   * Bulk invalidation for system-wide updates
   */
  static async invalidateAll(): Promise<void> {
    // This should be used sparingly, only for major system updates
    await cache.invalidatePattern('*');
  }
  
  /**
   * Selective invalidation based on tags
   */
  static async invalidateByTags(tags: string[]): Promise<void> {
    await Promise.all(
      tags.map(tag => cache.invalidatePattern(`*:${tag}:*`))
    );
  }
  
  /**
   * Time-based invalidation for stale data
   */
  static async invalidateStaleData(olderThanHours: number = 24): Promise<void> {
    // This would require storing timestamps with cached data
    // For now, we'll invalidate specific cache types that are likely stale
    const stalePatterns = [
      'search:*',
      'discussions:page:*',
      'leaderboard:*',
    ];
    
    await Promise.all(
      stalePatterns.map(pattern => cache.invalidatePattern(pattern))
    );
  }
  
  /**
   * Smart invalidation based on dependency graph
   */
  static async smartInvalidate(entityType: string, entityId: string): Promise<void> {
    const dependencies: Record<string, (id: string) => Promise<void>> = {
      user: (id) => this.onUserProfileUpdate(id),
      node: (id) => this.invalidateNodeCaches(id),
      path: (id) => this.invalidatePathCaches(id),
      comment: (id) => this.onCommentAction(id),
    };
    
    const handler = dependencies[entityType];
    if (handler) {
      await handler(entityId);
    }
  }
}