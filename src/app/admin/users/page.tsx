'use client';

import React, { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

interface UserProfile {
  id: string;
  username: string;
  email?: string;
  avatar_url?: string;
  bio?: string;
  title: string;
  neural_level: number;
  total_points: number;
  memory_crystals: number;
  synaptic_streak: number;
  total_nodes_completed: number;
  favorite_domain?: string;
  created_at: string;
  last_active_at: string;
}

export default function UsersPage() {
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'recent' | 'points' | 'level'>('recent');

  useEffect(() => {
    fetchUsers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchUsers = async () => {
    try {
      let query = supabase.from('user_profiles').select('*');
      
      if (sortBy === 'recent') {
        query = query.order('last_active_at', { ascending: false });
      } else if (sortBy === 'points') {
        query = query.order('total_points', { ascending: false });
      } else if (sortBy === 'level') {
        query = query.order('neural_level', { ascending: false });
      }

      const { data, error } = await query;

      if (error) throw error;
      setUsers(data || []);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredUsers = users.filter(u => {
    const searchLower = searchTerm.toLowerCase();
    return (
      (u.username?.toLowerCase().includes(searchLower)) ||
      (u.email?.toLowerCase().includes(searchLower))
    );
  });

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    if (days < 30) return `${Math.floor(days / 7)} weeks ago`;
    if (days < 365) return `${Math.floor(days / 30)} months ago`;
    return date.toLocaleDateString();
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading users...</div>;
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">User Management</h1>
        <p className="text-gray-600 mt-2">View and manage user accounts</p>
      </div>

      {/* Filters and Stats */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            type="text"
            placeholder="Search users..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
          />
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'recent' | 'points' | 'level')}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
          >
            <option value="recent">Most Recent</option>
            <option value="points">Most Points</option>
            <option value="level">Highest Level</option>
          </select>
          <div className="flex items-center justify-end">
            <span className="text-gray-600">
              Total Users: <span className="font-bold">{filteredUsers.length}</span>
            </span>
          </div>
        </div>
      </div>

      {/* Users Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredUsers.map((user) => (
          <div
            key={user.id}
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                {user.avatar_url ? (
                  <img
                    src={user.avatar_url}
                    alt={user.username}
                    className="w-12 h-12 rounded-full"
                  />
                ) : (
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold">
                    {user.username?.charAt(0) || '?'}
                  </div>
                )}
                <div>
                  <h3 className="font-bold text-lg text-gray-800">
                    {user.username}
                  </h3>
                  <p className="text-sm text-gray-500">@{user.username}</p>
                </div>
              </div>
              <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium">
                Lvl {user.neural_level}
              </span>
            </div>

            {user.bio && (
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{user.bio}</p>
            )}

            <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Points:</span>
                <span className="font-medium">{user.total_points.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Crystals:</span>
                <span className="font-medium">{user.memory_crystals}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Nodes:</span>
                <span className="font-medium">{user.total_nodes_completed}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Streak:</span>
                <span className="font-medium">{user.synaptic_streak}🔥</span>
              </div>
            </div>

            <div className="pt-4 border-t space-y-2 text-sm">
              <div className="flex justify-between text-gray-500">
                <span>Title:</span>
                <span className="font-medium text-gray-700">{user.title}</span>
              </div>
              {user.favorite_domain && (
                <div className="flex justify-between text-gray-500">
                  <span>Favorite:</span>
                  <span className="font-medium text-gray-700">{user.favorite_domain}</span>
                </div>
              )}
              <div className="flex justify-between text-gray-500">
                <span>Last Active:</span>
                <span className="font-medium text-gray-700">
                  {formatDate(user.last_active_at)}
                </span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t flex gap-2">
              <button className="flex-1 text-center px-3 py-1 bg-blue-50 text-blue-700 rounded hover:bg-blue-100">
                View Details
              </button>
              <button className="flex-1 text-center px-3 py-1 bg-gray-50 text-gray-700 rounded hover:bg-gray-100">
                Message
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredUsers.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No users found
        </div>
      )}
    </div>
  );
}