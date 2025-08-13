'use client';

import React, { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

interface Stats {
  totalQuestions: number;
  totalNodes: number;
  totalPaths: number;
  totalUsers: number;
  recentActivity: Array<{
    type: string;
    description: string;
    timestamp: string;
  }>;
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<Stats>({
    totalQuestions: 0,
    totalNodes: 0,
    totalPaths: 0,
    totalUsers: 0,
    recentActivity: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      // Fetch questions count
      const { count: questionsCount } = await supabase
        .from('quiz_questions')
        .select('*', { count: 'exact', head: true });

      // Fetch nodes count
      const { count: nodesCount } = await supabase
        .from('knowledge_nodes')
        .select('*', { count: 'exact', head: true });

      // Fetch paths count
      const { count: pathsCount } = await supabase
        .from('learning_paths')
        .select('*', { count: 'exact', head: true });

      // Fetch users count
      const { count: usersCount } = await supabase
        .from('user_profiles')
        .select('*', { count: 'exact', head: true });

      setStats({
        totalQuestions: questionsCount || 0,
        totalNodes: nodesCount || 0,
        totalPaths: pathsCount || 0,
        totalUsers: usersCount || 0,
        recentActivity: [
          { type: 'info', description: 'Dashboard loaded', timestamp: new Date().toISOString() }
        ]
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon, color }: { title: string; value: number; icon: string; color: string }) => (
    <div className={`bg-white rounded-lg shadow-md p-6 border-l-4 ${color}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm font-medium">{title}</p>
          <p className="text-3xl font-bold text-gray-800 mt-2">{value.toLocaleString()}</p>
        </div>
        <div className="text-4xl opacity-20">{icon}</div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Admin Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome to the NeuroQuest administration panel</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Questions"
          value={stats.totalQuestions}
          icon="❓"
          color="border-blue-500"
        />
        <StatCard
          title="Knowledge Nodes"
          value={stats.totalNodes}
          icon="🧠"
          color="border-purple-500"
        />
        <StatCard
          title="Learning Paths"
          value={stats.totalPaths}
          icon="🛤️"
          color="border-green-500"
        />
        <StatCard
          title="Total Users"
          value={stats.totalUsers}
          icon="👥"
          color="border-orange-500"
        />
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a
            href="/admin/questions/new"
            className="flex items-center justify-center gap-2 p-4 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <span>➕</span>
            <span>Add New Question</span>
          </a>
          <a
            href="/admin/upload"
            className="flex items-center justify-center gap-2 p-4 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors"
          >
            <span>📤</span>
            <span>Batch Upload</span>
          </a>
          <a
            href="/admin/nodes/new"
            className="flex items-center justify-center gap-2 p-4 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors"
          >
            <span>🆕</span>
            <span>Create Node</span>
          </a>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Recent Activity</h2>
        <div className="space-y-3">
          {stats.recentActivity.map((activity, index) => (
            <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded">
              <span className="text-gray-400">ℹ️</span>
              <div className="flex-1">
                <p className="text-gray-700">{activity.description}</p>
                <p className="text-xs text-gray-500">
                  {new Date(activity.timestamp).toLocaleString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}