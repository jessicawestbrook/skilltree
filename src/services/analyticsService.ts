import { supabase } from '../lib/supabase';

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
  static async startSession(): Promise<string | null> {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return null;

      const userAgent = navigator.userAgent;
      const deviceType = this.detectDeviceType();

      const { data, error } = await supabase.rpc('start_learning_session', {
        p_user_id: user.id,
        p_user_agent: userAgent,
        p_device_type: deviceType
      });

      if (error) {
        console.error('Error starting session:', error);
        return null;
      }

      this.currentSessionId = data;
      this.sessionStartTime = new Date();
      return data;
    } catch (error) {
      console.error('Error in startSession:', error);
      return null;
    }
  }

  /**
   * End the current learning session
   */
  static async endSession(): Promise<void> {
    if (!this.currentSessionId || !this.sessionStartTime) return;

    try {
      const duration = Math.round((new Date().getTime() - this.sessionStartTime.getTime()) / 1000);

      const { error } = await supabase.rpc('end_learning_session', {
        p_session_id: this.currentSessionId,
        p_total_duration_seconds: duration
      });

      if (error) {
        console.error('Error ending session:', error);
      }

      this.currentSessionId = null;
      this.sessionStartTime = null;
    } catch (error) {
      console.error('Error in endSession:', error);
    }
  }

  /**
   * Track a learning event
   */
  static async trackEvent(event: AnalyticsEvent): Promise<void> {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;

      const { error } = await supabase.rpc('track_learning_event', {
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
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return null;

      const { data, error } = await supabase.rpc('get_user_analytics', {
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
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return [];

      const { data, error } = await supabase.rpc('generate_learning_insights', {
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
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return [];

      // First generate recommendations
      const { error: genError } = await supabase.rpc('generate_recommendations', {
        p_user_id: user.id
      });

      if (genError) {
        console.error('Error generating recommendations:', genError);
      }

      // Then fetch them
      const { data, error } = await supabase
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
    await this.trackEvent({
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
    await this.trackEvent({
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
    await this.trackEvent({
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
    await this.trackEvent({
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
    await this.trackEvent({
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
  static async initialize(): Promise<void> {
    // Start session when analytics service initializes
    await this.startSession();

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
  static async cleanup(): Promise<void> {
    await this.endSession();
  }
}