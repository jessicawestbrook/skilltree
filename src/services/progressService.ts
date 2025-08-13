import { supabase } from '../lib/supabase';

export interface UserProgress {
  id: string;
  user_id: string;
  node_id: string;
  completed_at: string;
  points_earned: number;
  quiz_score: number;
  time_spent_seconds: number;
}

export interface ProgressSubmission {
  nodeId: string;
  quiz_score: number;
  time_spent_seconds?: number;
}

export class ProgressService {
  /**
   * Submit quiz completion and record progress
   */
  static async submitProgress(data: ProgressSubmission): Promise<{ success: boolean; data?: UserProgress; error?: string }> {
    try {
      const response = await fetch('/api/progress', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Failed to submit progress');
      }

      return { success: true, data: result.data };
    } catch (error) {
      console.error('Error submitting progress:', error);
      return { success: false, error: error instanceof Error ? error.message : 'Failed to submit progress' };
    }
  }

  /**
   * Get user progress for a specific node
   */
  static async getNodeProgress(nodeId: string): Promise<UserProgress | null> {
    try {
      const response = await fetch(`/api/progress?nodeId=${nodeId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const result = await response.json();

      if (!response.ok) {
        console.error('Failed to fetch progress:', result.error);
        return null;
      }

      return result.data?.[0] || null;
    } catch (error) {
      console.error('Error fetching node progress:', error);
      return null;
    }
  }

  /**
   * Get all user progress
   */
  static async getAllProgress(): Promise<UserProgress[]> {
    try {
      const response = await fetch('/api/progress', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const result = await response.json();

      if (!response.ok) {
        console.error('Failed to fetch all progress:', result.error);
        return [];
      }

      return result.data || [];
    } catch (error) {
      console.error('Error fetching all progress:', error);
      return [];
    }
  }

  /**
   * Get user progress directly from Supabase (client-side)
   */
  static async getUserProgress(userId: string): Promise<UserProgress[]> {
    try {
      const { data, error } = await supabase
        .from('user_progress')
        .select('*')
        .eq('user_id', userId)
        .order('completed_at', { ascending: false });

      if (error) {
        console.error('Error fetching user progress:', error);
        return [];
      }

      return data || [];
    } catch (error) {
      console.error('Error in getUserProgress:', error);
      return [];
    }
  }

  /**
   * Check if a node is completed by the current user
   */
  static async isNodeCompleted(nodeId: string): Promise<boolean> {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      
      if (!user) return false;

      const { data, error } = await supabase
        .from('user_progress')
        .select('id')
        .eq('user_id', user.id)
        .eq('node_id', nodeId)
        .single();

      return !!data && !error;
    } catch (error) {
      console.error('Error checking node completion:', error);
      return false;
    }
  }

  /**
   * Get progress summary for the current user
   */
  static async getProgressSummary(): Promise<{
    totalNodes: number;
    totalPoints: number;
    averageScore: number;
    recentCompletions: any[];
  } | null> {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      
      if (!user) return null;

      const { data, error } = await supabase
        .rpc('get_user_progress_summary', { p_user_id: user.id });

      if (error) {
        console.error('Error fetching progress summary:', error);
        return null;
      }

      return data?.[0] || {
        totalNodes: 0,
        totalPoints: 0,
        averageScore: 0,
        recentCompletions: []
      };
    } catch (error) {
      console.error('Error in getProgressSummary:', error);
      return null;
    }
  }

  /**
   * Get leaderboard data
   */
  static async getLeaderboard(limit: number = 10): Promise<any[]> {
    try {
      const { data, error } = await supabase
        .rpc('get_leaderboard', { p_limit: limit });

      if (error) {
        console.error('Error fetching leaderboard:', error);
        return [];
      }

      return data || [];
    } catch (error) {
      console.error('Error in getLeaderboard:', error);
      return [];
    }
  }

  /**
   * Calculate time spent on a quiz (in seconds)
   */
  static calculateTimeSpent(startTime: Date): number {
    const endTime = new Date();
    return Math.round((endTime.getTime() - startTime.getTime()) / 1000);
  }
}