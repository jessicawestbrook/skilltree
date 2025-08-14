import { createClient } from '../lib/supabase-client';

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
   * Initialize default progress data for new users
   */
  static async initializeUserProgress(userId: string): Promise<{ success: boolean; error?: string }> {
    try {
      const supabase = createClient();
      
      // Check if user already has progress records
      const { data: existingProgress } = await supabase
        .from('user_progress')
        .select('id')
        .eq('user_id', userId)
        .limit(1);
      
      // If user already has progress, don't initialize
      if (existingProgress && existingProgress.length > 0) {
        return { success: true };
      }
      
      // Initialize user stats if they don't exist
      const { error: statsError } = await supabase
        .from('user_stats')
        .upsert({
          user_id: userId,
          total_nodes_completed: 0,
          total_points: 0,
          current_streak: 0,
          longest_streak: 0,
          last_activity: new Date().toISOString(),
          created_at: new Date().toISOString()
        }, {
          onConflict: 'user_id',
          ignoreDuplicates: true
        });
      
      if (statsError) {
        console.error('Error initializing user stats:', statsError);
      }
      
      // Initialize learning preferences
      const { error: prefsError } = await supabase
        .from('learning_preferences')
        .upsert({
          user_id: userId,
          daily_goal_minutes: 30,
          reminder_enabled: false,
          reminder_time: '19:00',
          preferred_difficulty: 'beginner',
          preferred_subjects: ['general'],
          created_at: new Date().toISOString()
        }, {
          onConflict: 'user_id',
          ignoreDuplicates: true
        });
      
      if (prefsError) {
        console.error('Error initializing learning preferences:', prefsError);
      }
      
      // Initialize achievements (unlock the "Getting Started" achievement)
      const { error: achievementError } = await supabase
        .from('user_achievements')
        .upsert({
          user_id: userId,
          achievement_id: 'getting_started',
          unlocked_at: new Date().toISOString()
        }, {
          onConflict: 'user_id,achievement_id',
          ignoreDuplicates: true
        });
      
      if (achievementError) {
        console.error('Error initializing achievements:', achievementError);
      }
      
      return { success: true };
    } catch (error) {
      console.error('Error initializing user progress:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Failed to initialize user progress' 
      };
    }
  }

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

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText || 'Failed to submit progress'}`);
      }

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const responseText = await response.text();
        throw new Error(`Expected JSON response but got: ${contentType}. Response: ${responseText.substring(0, 200)}`);
      }

      const result = await response.json();

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

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Failed to fetch progress:', errorText);
        return null;
      }

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const responseText = await response.text();
        console.error(`Expected JSON response but got: ${contentType}. Response: ${responseText.substring(0, 200)}`);
        return null;
      }

      const result = await response.json();

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

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Failed to fetch all progress:', errorText);
        return [];
      }

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const responseText = await response.text();
        console.error(`Expected JSON response but got: ${contentType}. Response: ${responseText.substring(0, 200)}`);
        return [];
      }

      const result = await response.json();

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
      const supabase = createClient();
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
      const supabase = createClient();
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
      const supabase = createClient();
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
      const supabase = createClient();
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