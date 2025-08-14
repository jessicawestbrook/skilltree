import { createClient } from '../lib/supabase-client';

// Simple UUID v4 generator
function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

export interface LearningSession {
  id: string;
  user_id: string;
  session_start: string;
  session_end?: string;
  total_duration_seconds: number;
  nodes_attempted: string[];
  nodes_completed: string[];
  total_questions_answered: number;
  correct_answers: number;
  user_agent?: string;
  device_type?: string;
}

export interface AnalyticsEvent {
  event_type: string;
  node_id?: string;
  event_data?: Record<string, any>;
}

export interface UserAnalytics {
  total_study_time_hours: number;
  nodes_completed: number;
  average_quiz_score: number;
  study_streak_days: number;
  most_active_domains: Array<{ domain: string; count: number }>;
  daily_activity: Array<{
    date: string;
    study_time_minutes: number;
    nodes_completed: number;
  }>;
  quiz_performance_trend: Array<{
    date: string;
    average_score: number;
  }>;
}

export interface LearningInsight {
  insight_type: string;
  title: string;
  description: string;
  action_suggestion: string;
  priority: number;
}

export interface LearningRecommendation {
  id: string;
  recommendation_type: string;
  node_id: string;
  priority_score: number;
  reasoning: string;
  created_at: string;
}

export class AnalyticsService {
  private static currentSessionId: string | null = null;
  private static sessionStartTime: Date | null = null;

  /**
   * Start a new learning session
   */
  static startSession(): string {
    // Generate a proper UUID for the session
    const sessionId = generateUUID();
    this.currentSessionId = sessionId;
    this.sessionStartTime = new Date();
    
    // Asynchronously handle the database operations without blocking
    this.startSessionAsync().catch(() => {
      // Silently handle errors - session tracking is non-critical
      // and we don't want to spam the console in development
    });
    
    return sessionId;
  }

  private static async startSessionAsync(): Promise<void> {
    try {
      const { data: { user } } = await createClient().auth.getUser();
      if (!user) return;

      const userAgent = typeof navigator !== 'undefined' ? navigator.userAgent : 'Unknown';
      const deviceType = this.detectDeviceType();

      await createClient().rpc('start_learning_session', {
        p_user_id: user.id,
        p_user_agent: userAgent,
        p_device_type: deviceType,
        p_session_id: this.currentSessionId
      });
    } catch (error) {
      // Silently fail - session tracking is non-critical
      // The app will work fine without analytics
    }
  }

  /**
   * End the current learning session
   */
  static endSession(sessionId?: string): void {
    const targetSessionId = sessionId || this.currentSessionId;
    if (!targetSessionId) {
      console.warn('Attempted to end session with no session ID');
      return;
    }

    // Validate session ID format - must be a valid UUID
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    if (typeof targetSessionId !== 'string' || !uuidRegex.test(targetSessionId)) {
      // Silently skip invalid session IDs - this might be an old format session
      return;
    }

    // If ending the current session, clear the local state
    if (targetSessionId === this.currentSessionId) {
      this.currentSessionId = null;
      this.sessionStartTime = null;
    }

    // Handle the database operations asynchronously
    this.endSessionAsync(targetSessionId).catch(() => {
      // Silently handle errors - session ending is non-critical
      // and we don't want to spam the console in development
    });
  }

  private static async endSessionAsync(sessionId: string): Promise<void> {
    try {
      const duration = this.sessionStartTime 
        ? Math.round((new Date().getTime() - this.sessionStartTime.getTime()) / 1000)
        : 0;

      // Skip session ending if no session ID or in development without proper DB setup
      if (!sessionId || sessionId === 'undefined' || sessionId === 'null') {
        return; // Silently skip invalid session IDs
      }

      // For now, just use API endpoint to avoid RPC errors
      try {
        const response = await fetch('/api/analytics/end-session', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ sessionId, duration })
        });

        if (!response.ok) {
          // Silently fail for now - this is non-critical functionality
          // Don't log anything to avoid console errors in development
        }
      } catch (apiError) {
        // Silently fail - this is cleanup and non-critical
        // Don't log anything to avoid console errors in development
      }
    } catch (error) {
      // Silently fail - this is cleanup and non-critical
      // Don't log anything to avoid console errors in development
    }
  }

  /**
   * Track a learning event
   */
  static async trackLearningEvent(event: AnalyticsEvent): Promise<void> {
    try {
      const { data: { user } } = await createClient().auth.getUser();
      if (!user) return;

      const { error } = await createClient().rpc('track_learning_event', {
        p_user_id: user.id,
        p_event_type: event.event_type,
        p_session_id: this.currentSessionId,
        p_node_id: event.node_id,
        p_event_data: event.event_data || {}
      });

      if (error) {
        console.error('Error tracking event:', error);
      }
    } catch (error) {
      console.error('Error in trackEvent:', error);
    }
  }

  /**
   * Get user analytics data
   */
  static async getUserAnalytics(daysBack: number = 30): Promise<UserAnalytics | null> {
    try {
      const { data: { user } } = await createClient().auth.getUser();
      if (!user) return null;

      const { data, error } = await createClient().rpc('get_user_analytics', {
        p_user_id: user.id,
        p_days_back: daysBack
      });

      if (error) {
        console.error('Error fetching analytics:', error);
        return null;
      }

      return data?.[0] || null;
    } catch (error) {
      console.error('Error in getUserAnalytics:', error);
      return null;
    }
  }

  /**
   * Get learning insights
   */
  static async getLearningInsights(): Promise<LearningInsight[]> {
    try {
      const { data: { user } } = await createClient().auth.getUser();
      if (!user) return [];

      const { data, error } = await createClient().rpc('generate_learning_insights', {
        p_user_id: user.id
      });

      if (error) {
        console.error('Error fetching insights:', error);
        return [];
      }

      return data || [];
    } catch (error) {
      console.error('Error in getLearningInsights:', error);
      return [];
    }
  }

  /**
   * Generate and get personalized recommendations
   */
  static async getRecommendations(): Promise<LearningRecommendation[]> {
    try {
      const { data: { user } } = await createClient().auth.getUser();
      if (!user) return [];

      // First generate recommendations
      const { error: genError } = await createClient().rpc('generate_recommendations', {
        p_user_id: user.id
      });

      if (genError) {
        console.error('Error generating recommendations:', genError);
      }

      // Then fetch them
      const { data, error } = await createClient()
        .from('learning_recommendations')
        .select(`
          id,
          recommendation_type,
          node_id,
          priority_score,
          reasoning,
          created_at,
          knowledge_nodes!inner(name, domain, difficulty)
        `)
        .eq('user_id', user.id)
        .eq('is_active', true)
        .order('priority_score', { ascending: false })
        .limit(10);

      if (error) {
        console.error('Error fetching recommendations:', error);
        return [];
      }

      return data || [];
    } catch (error) {
      console.error('Error in getRecommendations:', error);
      return [];
    }
  }

  /**
   * Track quiz start event
   */
  static async trackQuizStart(nodeId: string, questionCount: number): Promise<void> {
    await this.trackLearningEvent({
      event_type: 'quiz_start',
      node_id: nodeId,
      event_data: {
        question_count: questionCount,
        timestamp: new Date().toISOString()
      }
    });
  }

  /**
   * Track quiz completion event
   */
  static async trackQuizComplete(
    nodeId: string, 
    score: number, 
    timeSpent: number,
    totalQuestions: number,
    correctAnswers: number
  ): Promise<void> {
    await this.trackLearningEvent({
      event_type: 'quiz_complete',
      node_id: nodeId,
      event_data: {
        score,
        time_spent_seconds: timeSpent,
        total_questions: totalQuestions,
        correct_answers: correctAnswers,
        timestamp: new Date().toISOString()
      }
    });
  }

  /**
   * Track node visit
   */
  static async trackNodeVisit(nodeId: string, nodeName: string): Promise<void> {
    await this.trackLearningEvent({
      event_type: 'node_visit',
      node_id: nodeId,
      event_data: {
        node_name: nodeName,
        timestamp: new Date().toISOString()
      }
    });
  }

  /**
   * Track content view
   */
  static async trackContentView(nodeId: string, contentType: string, duration?: number): Promise<void> {
    await this.trackLearningEvent({
      event_type: 'content_view',
      node_id: nodeId,
      event_data: {
        content_type: contentType,
        duration_seconds: duration,
        timestamp: new Date().toISOString()
      }
    });
  }

  /**
   * Track search query
   */
  static async trackSearch(query: string, resultsCount: number): Promise<void> {
    await this.trackLearningEvent({
      event_type: 'search',
      event_data: {
        query,
        results_count: resultsCount,
        timestamp: new Date().toISOString()
      }
    });
  }

  /**
   * Get session statistics
   */
  static getSessionStats(): {
    sessionId: string | null;
    duration: number;
    isActive: boolean;
  } {
    return {
      sessionId: this.currentSessionId,
      duration: this.sessionStartTime 
        ? Math.round((new Date().getTime() - this.sessionStartTime.getTime()) / 1000)
        : 0,
      isActive: !!this.currentSessionId
    };
  }

  /**
   * Detect device type from user agent
   */
  private static detectDeviceType(): string {
    const userAgent = navigator.userAgent.toLowerCase();
    
    if (/tablet|ipad|playbook|silk|(android(?!.*mobile))/.test(userAgent)) {
      return 'tablet';
    }
    
    if (/mobile|iphone|ipod|android|blackberry|opera|mini|windows\sce|palm|smartphone|iemobile/.test(userAgent)) {
      return 'mobile';
    }
    
    return 'desktop';
  }

  /**
   * Initialize analytics for the current user session
   */
  static initialize(): void {
    // Start session when analytics service initializes
    this.startSession();

    // Set up beforeunload event to end session
    if (typeof window !== 'undefined') {
      window.addEventListener('beforeunload', () => {
        // Use sendBeacon for reliable event tracking on page unload
        if (this.currentSessionId) {
          navigator.sendBeacon('/api/analytics/end-session', JSON.stringify({
            sessionId: this.currentSessionId
          }));
        }
      });

      // Also end session on visibility change (when tab is hidden)
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
          this.endSession();
        } else if (document.visibilityState === 'visible' && !this.currentSessionId) {
          this.startSession();
        }
      });
    }
  }

  /**
   * Clean up analytics service
   */
  static cleanup(): void {
    this.endSession();
  }

  /**
   * Get current session
   */
  static getCurrentSession(): any {
    return {
      id: this.currentSessionId,
      sessionId: this.currentSessionId,
      startTime: this.sessionStartTime,
      duration: this.sessionStartTime ? Date.now() - this.sessionStartTime.getTime() : 0
    };
  }

  /**
   * Track page view
   */
  static trackPageView(path: string, title?: string): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('config', 'GA_MEASUREMENT_ID', {
        page_title: title,
        page_location: path
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('config', 'GA_MEASUREMENT_ID', {
        page_title: title,
        page_location: path
      });
    } else {
      console.log('Page view tracked:', { path, title });
    }
  }

  /**
   * Track custom event (overloaded version for tests)
   */
  static trackEvent(eventName: string, parameters?: Record<string, any>): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('event', eventName, parameters || {});
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('event', eventName, parameters || {});
    } else {
      console.log('Event tracked:', { eventName, parameters });
    }
  }

  /**
   * Track node completion
   */
  static trackNodeCompletion(nodeId: string, score: number, accuracy: number, timeSpent: number): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('event', 'node_completed', {
        event_category: 'learning',
        node_id: nodeId,
        points_earned: score,
        quiz_score: accuracy,
        time_spent: timeSpent
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('event', 'node_completed', {
        event_category: 'learning',
        node_id: nodeId,
        points_earned: score,
        quiz_score: accuracy,
        time_spent: timeSpent
      });
    } else {
      console.log('Node completion tracked:', { nodeId, score, accuracy, timeSpent });
    }
  }

  /**
   * Track learning path started
   */
  static trackLearningPathStarted(pathId: string, pathName: string): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('event', 'learning_path_started', {
        event_category: 'learning',
        path_id: pathId,
        path_name: pathName
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('event', 'learning_path_started', {
        event_category: 'learning',
        path_id: pathId,
        path_name: pathName
      });
    } else {
      console.log('Learning path started:', { pathId, pathName });
    }
  }

  /**
   * Track quiz attempt
   */
  static trackQuizAttempt(nodeId: string, totalQuestions: number, correctAnswers: number, accuracy: number): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('event', 'quiz_attempt', {
        event_category: 'learning',
        node_id: nodeId,
        total_questions: totalQuestions,
        correct_answers: correctAnswers,
        score_percentage: accuracy
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('event', 'quiz_attempt', {
        event_category: 'learning',
        node_id: nodeId,
        total_questions: totalQuestions,
        correct_answers: correctAnswers,
        score_percentage: accuracy
      });
    } else {
      console.log('Quiz attempt tracked:', { nodeId, totalQuestions, correctAnswers, accuracy });
    }
  }

  /**
   * Track feature usage
   */
  static trackFeatureUsage(feature: string, metadata?: Record<string, any>): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('event', 'feature_used', {
        event_category: 'engagement',
        feature_name: feature,
        metadata: metadata
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('event', 'feature_used', {
        event_category: 'engagement',
        feature_name: feature,
        metadata: metadata
      });
    } else {
      console.log('Feature usage tracked:', { feature, metadata });
    }
  }

  /**
   * Track error
   */
  static trackError(error: Error, context?: string): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('event', 'exception', {
        description: error.message,
        fatal: false,
        context: context
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('event', 'exception', {
        description: error.message,
        fatal: false,
        context: context
      });
    } else {
      console.log('Error tracked:', { error: error.message, context });
    }
  }

  /**
   * Track performance metric
   */
  static trackPerformance(metric: string, value: number): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('event', 'timing_complete', {
        name: metric,
        value: value
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('event', 'timing_complete', {
        name: metric,
        value: value
      });
    } else {
      console.log('Performance tracked:', { metric, value });
    }
  }

  /**
   * Track engagement time
   */
  static trackEngagementTime(timeMs: number): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('event', 'user_engagement', {
        engagement_time_msec: timeMs * 1000
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('event', 'user_engagement', {
        engagement_time_msec: timeMs * 1000
      });
    } else {
      console.log('Engagement time tracked:', { timeMs });
    }
  }

  /**
   * Set user properties
   */
  static setUserProperties(properties: Record<string, any>): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('config', 'GA_MEASUREMENT_ID', {
        custom_map: properties
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('config', 'GA_MEASUREMENT_ID', {
        custom_map: properties
      });
    } else {
      console.log('User properties set:', properties);
    }
  }

  /**
   * Identify user
   */
  static identifyUser(userId: string, traits?: Record<string, any>): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('config', 'GA_MEASUREMENT_ID', {
        user_id: userId,
        custom_map: traits
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('config', 'GA_MEASUREMENT_ID', {
        user_id: userId,
        custom_map: traits
      });
    } else {
      console.log('User identified:', { userId, traits });
    }
  }

  /**
   * Set consent granted
   */
  static setConsentGranted(granted: boolean): void {
    if (typeof (global as any).gtag === 'function') {
      (global as any).gtag('consent', 'update', {
        analytics_storage: granted ? 'granted' : 'denied'
      });
    } else if (typeof window !== 'undefined' && typeof (window as any).gtag === 'function') {
      (window as any).gtag('consent', 'update', {
        analytics_storage: granted ? 'granted' : 'denied'
      });
    } else {
      console.log('Consent set:', { granted });
    }
  }
}