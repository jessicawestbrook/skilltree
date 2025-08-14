'use client';

import React, { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase-client';
import { 
  Users, 
  Brain, 
  BookOpen, 
  TrendingUp, 
  Activity,
  Calendar,
  Award,
  Clock,
  BarChart,
  PieChart,
  AlertCircle,
  CheckCircle,
  Home,
  ArrowLeft
} from 'lucide-react';
import Link from 'next/link';

interface Stats {
  totalQuestions: number;
  totalNodes: number;
  totalPaths: number;
  totalUsers: number;
  activeUsers: number;
  completionRate: number;
  averageScore: number;
  totalCompletions: number;
  recentActivity: Array<{
    type: 'success' | 'info' | 'warning' | 'error';
    description: string;
    timestamp: string;
    user?: string;
  }>;
  weeklyProgress: Array<{
    day: string;
    completions: number;
  }>;
  topPerformers: Array<{
    user_id: string;
    username: string;
    total_points: number;
    nodes_completed: number;
  }>;
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<Stats>({
    totalQuestions: 0,
    totalNodes: 0,
    totalPaths: 0,
    totalUsers: 0,
    activeUsers: 0,
    completionRate: 0,
    averageScore: 0,
    totalCompletions: 0,
    recentActivity: [],
    weeklyProgress: [],
    topPerformers: []
  });
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7d'); // 7d, 30d, all

  useEffect(() => {
    fetchStats();
    // Set up real-time subscription for activity
    const subscription = supabase
      .channel('admin-activity')
      .on('postgres_changes', { 
        event: '*', 
        schema: 'public', 
        table: 'user_progress' 
      }, handleRealtimeUpdate)
      .subscribe();

    return () => {
      subscription.unsubscribe();
    };
  }, [timeRange]);

  const handleRealtimeUpdate = (payload: any) => {
    // Add new activity to the feed
    const newActivity = {
      type: 'success' as const,
      description: `New completion: ${payload.new?.node_id || 'Unknown node'}`,
      timestamp: new Date().toISOString(),
      user: payload.new?.user_id
    };
    
    setStats(prev => ({
      ...prev,
      recentActivity: [newActivity, ...prev.recentActivity.slice(0, 9)]
    }));
  };

  const fetchStats = async () => {
    try {
      setLoading(true);
      
      // Parallel fetch all stats
      const [
        questionsResult,
        nodesResult,
        pathsResult,
        usersResult,
        progressResult,
        activeUsersResult
      ] = await Promise.all([
        supabase.from('quiz_questions').select('*', { count: 'exact', head: true }),
        supabase.from('knowledge_nodes').select('*', { count: 'exact', head: true }),
        supabase.from('learning_paths').select('*', { count: 'exact', head: true }),
        supabase.from('user_profiles').select('*', { count: 'exact', head: true }),
        supabase.from('user_progress').select('*'),
        supabase.from('user_progress')
          .select('user_id')
          .gte('completed_at', new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString())
      ]);

      // Calculate analytics
      const progressData = progressResult.data || [];
      const totalCompletions = progressData.length;
      const averageScore = progressData.length > 0 
        ? progressData.reduce((sum, p) => sum + (p.quiz_score || 0), 0) / progressData.length 
        : 0;

      // Get unique active users from last 7 days
      const activeUserIds = new Set(activeUsersResult.data?.map(p => p.user_id) || []);
      
      // Calculate completion rate
      const completionRate = nodesResult.count && totalCompletions 
        ? Math.round((totalCompletions / (nodesResult.count * (usersResult.count || 1))) * 100) 
        : 0;

      // Get weekly progress
      const weeklyProgress = getWeeklyProgress(progressData);

      // Get top performers
      const topPerformers = await getTopPerformers();

      // Get recent activity
      const recentActivity = await getRecentActivity();

      setStats({
        totalQuestions: questionsResult.count || 0,
        totalNodes: nodesResult.count || 0,
        totalPaths: pathsResult.count || 0,
        totalUsers: usersResult.count || 0,
        activeUsers: activeUserIds.size,
        completionRate,
        averageScore: Math.round(averageScore),
        totalCompletions,
        recentActivity,
        weeklyProgress,
        topPerformers
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const getWeeklyProgress = (progressData: any[]) => {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const weekData = days.map(day => ({ day, completions: 0 }));
    
    progressData.forEach(p => {
      const date = new Date(p.completed_at);
      const dayIndex = date.getDay();
      weekData[dayIndex].completions++;
    });
    
    return weekData;
  };

  const getTopPerformers = async () => {
    const { data } = await supabase
      .from('user_progress')
      .select('user_id, points_earned')
      .order('points_earned', { ascending: false })
      .limit(5);

    if (!data) return [];

    // Group by user and calculate totals
    const userTotals = new Map();
    data.forEach(record => {
      const current = userTotals.get(record.user_id) || { 
        user_id: record.user_id, 
        total_points: 0, 
        nodes_completed: 0 
      };
      current.total_points += record.points_earned || 0;
      current.nodes_completed += 1;
      userTotals.set(record.user_id, current);
    });

    return Array.from(userTotals.values())
      .sort((a, b) => b.total_points - a.total_points)
      .slice(0, 5)
      .map(u => ({ ...u, username: `User ${u.user_id.slice(0, 8)}` }));
  };

  const getRecentActivity = async () => {
    const { data } = await supabase
      .from('user_progress')
      .select('*')
      .order('completed_at', { ascending: false })
      .limit(10);

    if (!data) return [];

    return data.map(record => ({
      type: record.quiz_score >= 80 ? 'success' as const : 'info' as const,
      description: `${record.quiz_score}% score on ${record.node_id}`,
      timestamp: record.completed_at,
      user: record.user_id
    }));
  };

  const StatCard = ({ 
    title, 
    value, 
    icon: Icon, 
    trend, 
    color,
    subtitle 
  }: { 
    title: string; 
    value: number | string; 
    icon: any; 
    trend?: number;
    color: string;
    subtitle?: string;
  }) => (
    <div className={`bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-6 border-l-4 ${color}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-gray-500 text-sm font-medium">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
          {subtitle && (
            <p className="text-sm text-gray-600 mt-1">{subtitle}</p>
          )}
          {trend !== undefined && (
            <div className={`flex items-center gap-1 mt-2 text-sm ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              <TrendingUp className={`w-4 h-4 ${trend < 0 ? 'rotate-180' : ''}`} />
              <span>{Math.abs(trend)}% from last week</span>
            </div>
          )}
        </div>
        <div className={`p-3 rounded-lg ${color.replace('border-', 'bg-').replace('500', '100')}`}>
          <Icon className={`w-6 h-6 ${color.replace('border-', 'text-')}`} />
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-4 mb-2">
              <Link 
                href="/"
                className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft size={20} />
                <Home size={20} />
                <span className="font-medium">Back to Learning</span>
              </Link>
            </div>
            <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="text-gray-600 mt-1">Monitor your platform's performance and user engagement</p>
          </div>
          <div className="flex items-center gap-2">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="all">All time</option>
            </select>
            <button
              onClick={fetchStats}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center gap-2"
            >
              <Activity className="w-4 h-4" />
              Refresh
            </button>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Users"
          value={stats.totalUsers}
          icon={Users}
          trend={12}
          color="border-blue-500"
          subtitle={`${stats.activeUsers} active this week`}
        />
        <StatCard
          title="Knowledge Nodes"
          value={stats.totalNodes}
          icon={Brain}
          color="border-purple-500"
          subtitle={`${stats.totalCompletions} completions`}
        />
        <StatCard
          title="Average Score"
          value={`${stats.averageScore}%`}
          icon={Award}
          trend={5}
          color="border-green-500"
        />
        <StatCard
          title="Completion Rate"
          value={`${stats.completionRate}%`}
          icon={CheckCircle}
          trend={-3}
          color="border-orange-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Weekly Progress Chart */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Weekly Progress</h2>
            <BarChart className="w-5 h-5 text-gray-400" />
          </div>
          <div className="flex items-end justify-between h-40 gap-2">
            {stats.weeklyProgress.map((day, index) => (
              <div key={index} className="flex-1 flex flex-col items-center gap-2">
                <div className="w-full bg-gray-200 rounded-t flex-1 relative">
                  <div 
                    className="absolute bottom-0 w-full bg-indigo-500 rounded-t transition-all"
                    style={{ 
                      height: `${day.completions > 0 ? (day.completions / Math.max(...stats.weeklyProgress.map(d => d.completions))) * 100 : 0}%` 
                    }}
                  />
                </div>
                <span className="text-xs text-gray-600">{day.day}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Top Performers */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Top Performers</h2>
            <Award className="w-5 h-5 text-gray-400" />
          </div>
          <div className="space-y-3">
            {stats.topPerformers.map((performer, index) => (
              <div key={performer.user_id} className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm
                  ${index === 0 ? 'bg-yellow-500' : index === 1 ? 'bg-gray-400' : index === 2 ? 'bg-orange-600' : 'bg-gray-300'}`}>
                  {index + 1}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{performer.username}</p>
                  <p className="text-xs text-gray-500">{performer.total_points} points • {performer.nodes_completed} nodes</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions & Activity Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-3">
            <a
              href="/admin/questions/new"
              className="flex items-center justify-center gap-2 p-4 bg-gradient-to-r from-blue-50 to-blue-100 text-blue-700 rounded-lg hover:from-blue-100 hover:to-blue-200 transition-all"
            >
              <BookOpen className="w-5 h-5" />
              <span className="font-medium">Add Question</span>
            </a>
            <a
              href="/admin/content/new"
              className="flex items-center justify-center gap-2 p-4 bg-gradient-to-r from-green-50 to-green-100 text-green-700 rounded-lg hover:from-green-100 hover:to-green-200 transition-all"
            >
              <Brain className="w-5 h-5" />
              <span className="font-medium">Create Content</span>
            </a>
            <a
              href="/admin/users"
              className="flex items-center justify-center gap-2 p-4 bg-gradient-to-r from-purple-50 to-purple-100 text-purple-700 rounded-lg hover:from-purple-100 hover:to-purple-200 transition-all"
            >
              <Users className="w-5 h-5" />
              <span className="font-medium">Manage Users</span>
            </a>
            <a
              href="/admin/upload"
              className="flex items-center justify-center gap-2 p-4 bg-gradient-to-r from-orange-50 to-orange-100 text-orange-700 rounded-lg hover:from-orange-100 hover:to-orange-200 transition-all"
            >
              <Activity className="w-5 h-5" />
              <span className="font-medium">Batch Upload</span>
            </a>
          </div>
        </div>

        {/* Real-time Activity Feed */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Live Activity</h2>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-xs text-gray-500">Real-time</span>
            </div>
          </div>
          <div className="space-y-3 max-h-64 overflow-y-auto">
            {stats.recentActivity.length > 0 ? (
              stats.recentActivity.map((activity, index) => (
                <div key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                  <div className={`mt-0.5 p-1 rounded-full ${
                    activity.type === 'success' ? 'bg-green-100' :
                    activity.type === 'warning' ? 'bg-yellow-100' :
                    activity.type === 'error' ? 'bg-red-100' : 'bg-blue-100'
                  }`}>
                    {activity.type === 'success' ? <CheckCircle className="w-4 h-4 text-green-600" /> :
                     activity.type === 'warning' ? <AlertCircle className="w-4 h-4 text-yellow-600" /> :
                     activity.type === 'error' ? <AlertCircle className="w-4 h-4 text-red-600" /> :
                     <Activity className="w-4 h-4 text-blue-600" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900">{activity.description}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <Clock className="w-3 h-3 text-gray-400" />
                      <p className="text-xs text-gray-500">
                        {new Date(activity.timestamp).toLocaleTimeString()}
                      </p>
                      {activity.user && (
                        <span className="text-xs text-gray-400">
                          • User {activity.user.slice(0, 8)}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-8">No recent activity</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}