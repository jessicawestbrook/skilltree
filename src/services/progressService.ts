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

      // Get all user progress records
      const { data: progressData, error: progressError } = await supabase
        .from('user_progress')
        .select('*')
        .eq('user_id', user.id)
        .order('completed_at', { ascending: false });

      if (progressError) {
        console.error('Error fetching user progress:', progressError);
        return null;
      }

      if (!progressData || progressData.length === 0) {
        return {
          totalNodes: 0,
          totalPoints: 0,
          averageScore: 0,
          recentCompletions: []
        };
      }

      // Calculate summary statistics
      const totalNodes = progressData.length;
      const totalPoints = progressData.reduce((sum, p) => sum + (p.points_earned || 0), 0);
      const totalScores = progressData.reduce((sum, p) => sum + (p.quiz_score || 0), 0);
      const averageScore = totalNodes > 0 ? Math.round(totalScores / totalNodes) : 0;
      const recentCompletions = progressData.slice(0, 5); // Get 5 most recent

      return {
        totalNodes,
        totalPoints,
        averageScore,
        recentCompletions
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
      // Get user progress grouped by user with aggregated stats
      const { data: progressData, error: progressError } = await supabase
        .from('user_progress')
        .select('user_id, points_earned, quiz_score, completed_at');

      if (progressError) {
        console.error('Error fetching progress for leaderboard:', progressError);
        return [];
      }

      if (!progressData || progressData.length === 0) {
        return [];
      }

      // Group by user and calculate totals
      const userStats = new Map<string, {
        user_id: string;
        total_points: number;
        total_nodes: number;
        avg_score: number;
      }>();

      progressData.forEach(record => {
        const existing = userStats.get(record.user_id) || {
          user_id: record.user_id,
          total_points: 0,
          total_nodes: 0,
          avg_score: 0
        };

        existing.total_points += record.points_earned || 0;
        existing.total_nodes += 1;
        existing.avg_score = ((existing.avg_score * (existing.total_nodes - 1)) + (record.quiz_score || 0)) / existing.total_nodes;

        userStats.set(record.user_id, existing);
      });

      // Convert to array and sort by total points
      const leaderboard = Array.from(userStats.values())
        .sort((a, b) => b.total_points - a.total_points)
        .slice(0, limit)
        .map((stats, index) => ({
          rank: index + 1,
          user_id: stats.user_id,
          total_points: stats.total_points,
          total_nodes: stats.total_nodes,
          avg_score: Math.round(stats.avg_score)
        }));

      return leaderboard;
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