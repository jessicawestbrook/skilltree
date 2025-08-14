import { cache, cacheKeys, cacheTTL } from '@/lib/redis';
import { cookies } from 'next/headers';
import { randomBytes } from 'crypto';

interface SessionData {
  id: string;
  userId?: string;
  data: Record<string, any>;
  createdAt: number;
  updatedAt: number;
  expiresAt: number;
}

export class SessionService {
  private static readonly SESSION_COOKIE_NAME = 'neuroquest_session';
  private static readonly SESSION_TTL = cacheTTL.day * 7; // 7 days
  
  /**
   * Create a new session
   */
  static async createSession(userId?: string, data: Record<string, any> = {}): Promise<string> {
    const sessionId = randomBytes(32).toString('hex');
    const now = Date.now();
    
    const session: SessionData = {
      id: sessionId,
      userId,
      data,
      createdAt: now,
      updatedAt: now,
      expiresAt: now + (this.SESSION_TTL * 1000),
    };
    
    // Store in Redis
    await cache.set(
      cacheKeys.session(sessionId),
      session,
      this.SESSION_TTL
    );
    
    // Set session cookie
    const cookieStore = await cookies();
    cookieStore.set(this.SESSION_COOKIE_NAME, sessionId, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: this.SESSION_TTL,
      path: '/',
    });
    
    return sessionId;
  }
  
  /**
   * Get current session
   */
  static async getCurrentSession(): Promise<SessionData | null> {
    const cookieStore = await cookies();
    const sessionId = cookieStore.get(this.SESSION_COOKIE_NAME)?.value;
    
    if (!sessionId) {
      return null;
    }
    
    return this.getSession(sessionId);
  }
  
  /**
   * Get session by ID
   */
  static async getSession(sessionId: string): Promise<SessionData | null> {
    const session = await cache.get<SessionData>(cacheKeys.session(sessionId));
    
    if (!session) {
      return null;
    }
    
    // Check if session is expired
    if (session.expiresAt < Date.now()) {
      await this.destroySession(sessionId);
      return null;
    }
    
    return session;
  }
  
  /**
   * Update session data
   */
  static async updateSession(
    sessionId: string, 
    updates: Partial<SessionData>
  ): Promise<boolean> {
    const session = await this.getSession(sessionId);
    
    if (!session) {
      return false;
    }
    
    const updatedSession: SessionData = {
      ...session,
      ...updates,
      updatedAt: Date.now(),
    };
    
    await cache.set(
      cacheKeys.session(sessionId),
      updatedSession,
      this.SESSION_TTL
    );
    
    return true;
  }
  
  /**
   * Set session data field
   */
  static async setSessionData(
    sessionId: string,
    key: string,
    value: any
  ): Promise<boolean> {
    const session = await this.getSession(sessionId);
    
    if (!session) {
      return false;
    }
    
    session.data[key] = value;
    session.updatedAt = Date.now();
    
    await cache.set(
      cacheKeys.session(sessionId),
      session,
      this.SESSION_TTL
    );
    
    return true;
  }
  
  /**
   * Get session data field
   */
  static async getSessionData<T = any>(
    sessionId: string,
    key: string
  ): Promise<T | null> {
    const session = await this.getSession(sessionId);
    
    if (!session) {
      return null;
    }
    
    return session.data[key] || null;
  }
  
  /**
   * Destroy session
   */
  static async destroySession(sessionId: string): Promise<void> {
    // Delete from Redis
    await cache.delete(cacheKeys.session(sessionId));
    
    // Clear cookie
    const cookieStore = await cookies();
    cookieStore.delete(this.SESSION_COOKIE_NAME);
  }
  
  /**
   * Regenerate session ID (for security)
   */
  static async regenerateSession(oldSessionId: string): Promise<string | null> {
    const session = await this.getSession(oldSessionId);
    
    if (!session) {
      return null;
    }
    
    // Create new session with same data
    const newSessionId = await this.createSession(session.userId, session.data);
    
    // Destroy old session
    await cache.delete(cacheKeys.session(oldSessionId));
    
    return newSessionId;
  }
  
  /**
   * Get all active sessions for a user
   */
  static async getUserSessions(userId: string): Promise<SessionData[]> {
    // This would require maintaining an index of sessions by user
    // For now, we'll implement this with a pattern search
    const pattern = 'session:*';
    const keys = await cache.invalidatePattern(pattern);
    
    const sessions: SessionData[] = [];
    
    // Note: This is not efficient for large numbers of sessions
    // Consider maintaining a separate index in Redis
    for (const key of keys) {
      const session = await cache.get<SessionData>(key);
      if (session && session.userId === userId) {
        sessions.push(session);
      }
    }
    
    return sessions;
  }
  
  /**
   * Destroy all sessions for a user
   */
  static async destroyUserSessions(userId: string): Promise<void> {
    const sessions = await this.getUserSessions(userId);
    
    await Promise.all(
      sessions.map(session => 
        cache.delete(cacheKeys.session(session.id))
      )
    );
  }
  
  /**
   * Clean up expired sessions
   */
  static async cleanupExpiredSessions(): Promise<number> {
    const pattern = 'session:*';
    const keys = await cache.invalidatePattern(pattern);
    
    let cleaned = 0;
    const now = Date.now();
    
    for (const key of keys) {
      const session = await cache.get<SessionData>(key);
      if (session && session.expiresAt < now) {
        await cache.delete(key);
        cleaned++;
      }
    }
    
    return cleaned;
  }
}

/**
 * Session middleware for API routes
 */
export function withSession(
  handler: (req: any, session: SessionData) => Promise<any>
) {
  return async (req: any) => {
    // Get or create session
    let session = await SessionService.getCurrentSession();
    
    if (!session) {
      const sessionId = await SessionService.createSession();
      session = await SessionService.getSession(sessionId);
    }
    
    if (!session) {
      throw new Error('Failed to create session');
    }
    
    // Add session to request
    req.session = session;
    
    // Execute handler
    return handler(req, session);
  };
}