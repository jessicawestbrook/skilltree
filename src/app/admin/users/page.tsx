'use client';

import React, { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase-client';
import {
  Users,
  Search,
  Filter,
  UserCheck,
  UserX,
  Mail,
  Calendar,
  Award,
  TrendingUp,
  MoreVertical,
  Shield,
  Ban,
  Send,
  Download,
  ChevronDown,
  Activity,
  Target,
  Zap,
  Clock,
  Star,
  AlertCircle
} from 'lucide-react';

const supabase = createClient();

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

interface UserStats {
  totalUsers: number;
  activeToday: number;
  activeWeek: number;
  newThisMonth: number;
}

export default function UsersPage() {
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'recent' | 'points' | 'level' | 'name'>('recent');
  const [filterStatus, setFilterStatus] = useState<'all' | 'active' | 'inactive'>('all');
  const [selectedUsers, setSelectedUsers] = useState<Set<string>>(new Set());
  const [showBulkActions, setShowBulkActions] = useState(false);
  const [stats, setStats] = useState<UserStats>({
    totalUsers: 0,
    activeToday: 0,
    activeWeek: 0,
    newThisMonth: 0
  });

  useEffect(() => {
    fetchUsers();
  }, [sortBy]);

  useEffect(() => {
    // Calculate stats whenever users change
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    const monthAgo = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate());

    const activeToday = users.filter(u => new Date(u.last_active_at) >= today).length;
    const activeWeek = users.filter(u => new Date(u.last_active_at) >= weekAgo).length;
    const newThisMonth = users.filter(u => new Date(u.created_at) >= monthAgo).length;

    setStats({
      totalUsers: users.length,
      activeToday,
      activeWeek,
      newThisMonth
    });
  }, [users]);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      let query = supabase.from('user_profiles').select('*');
      
      if (sortBy === 'recent') {
        query = query.order('last_active_at', { ascending: false });
      } else if (sortBy === 'points') {
        query = query.order('total_points', { ascending: false });
      } else if (sortBy === 'level') {
        query = query.order('neural_level', { ascending: false });
      } else if (sortBy === 'name') {
        query = query.order('username', { ascending: true });
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

  const handleSelectUser = (userId: string) => {
    const newSelected = new Set(selectedUsers);
    if (newSelected.has(userId)) {
      newSelected.delete(userId);
    } else {
      newSelected.add(userId);
    }
    setSelectedUsers(newSelected);
    setShowBulkActions(newSelected.size > 0);
  };

  const handleSelectAll = () => {
    if (selectedUsers.size === filteredUsers.length) {
      setSelectedUsers(new Set());
      setShowBulkActions(false);
    } else {
      setSelectedUsers(new Set(filteredUsers.map(u => u.id)));
      setShowBulkActions(true);
    }
  };

  const handleBulkAction = (action: string) => {
    console.log(`Bulk action: ${action} for users:`, Array.from(selectedUsers));
    // Implement bulk actions here
    setSelectedUsers(new Set());
    setShowBulkActions(false);
  };

  const filteredUsers = users.filter(u => {
    const searchLower = searchTerm.toLowerCase();
    const matchesSearch = (u.username?.toLowerCase().includes(searchLower)) ||
                          (u.email?.toLowerCase().includes(searchLower));
    
    if (!matchesSearch) return false;

    if (filterStatus === 'active') {
      const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
      return new Date(u.last_active_at) >= weekAgo;
    } else if (filterStatus === 'inactive') {
      const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
      return new Date(u.last_active_at) < weekAgo;
    }

    return true;
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

  const getUserStatus = (lastActive: string) => {
    const daysSinceActive = Math.floor((new Date().getTime() - new Date(lastActive).getTime()) / (1000 * 60 * 60 * 24));
    if (daysSinceActive === 0) return { label: 'Online', color: 'bg-green-100 text-green-700' };
    if (daysSinceActive <= 7) return { label: 'Active', color: 'bg-blue-100 text-blue-700' };
    if (daysSinceActive <= 30) return { label: 'Away', color: 'bg-yellow-100 text-yellow-700' };
    return { label: 'Inactive', color: 'bg-gray-100 text-gray-700' };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading users...</p>
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
            <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
            <p className="text-gray-600 mt-1">Monitor and manage your platform users</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center gap-2">
              <Download className="w-4 h-4" />
              Export
            </button>
            <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center gap-2">
              <Mail className="w-4 h-4" />
              Send Announcement
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Users</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalUsers}</p>
              <p className="text-xs text-gray-600 mt-1">All registered users</p>
            </div>
            <Users className="w-8 h-8 text-blue-500 opacity-20" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Active Today</p>
              <p className="text-2xl font-bold text-gray-900">{stats.activeToday}</p>
              <p className="text-xs text-gray-600 mt-1">Last 24 hours</p>
            </div>
            <Activity className="w-8 h-8 text-green-500 opacity-20" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Active This Week</p>
              <p className="text-2xl font-bold text-gray-900">{stats.activeWeek}</p>
              <p className="text-xs text-gray-600 mt-1">Last 7 days</p>
            </div>
            <TrendingUp className="w-8 h-8 text-purple-500 opacity-20" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-orange-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">New This Month</p>
              <p className="text-2xl font-bold text-gray-900">{stats.newThisMonth}</p>
              <p className="text-xs text-gray-600 mt-1">Last 30 days</p>
            </div>
            <UserCheck className="w-8 h-8 text-orange-500 opacity-20" />
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-xl shadow-sm p-4 mb-6">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search by username or email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value as any)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">All Users</option>
              <option value="active">Active Users</option>
              <option value="inactive">Inactive Users</option>
            </select>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="recent">Most Recent</option>
              <option value="points">Most Points</option>
              <option value="level">Highest Level</option>
              <option value="name">Alphabetical</option>
            </select>
          </div>
        </div>

        {/* Bulk Actions */}
        {showBulkActions && (
          <div className="mt-4 pt-4 border-t flex items-center justify-between">
            <span className="text-sm text-gray-600">
              {selectedUsers.size} user{selectedUsers.size !== 1 ? 's' : ''} selected
            </span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleBulkAction('message')}
                className="px-3 py-1.5 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 flex items-center gap-2 text-sm"
              >
                <Send className="w-4 h-4" />
                Message
              </button>
              <button
                onClick={() => handleBulkAction('export')}
                className="px-3 py-1.5 bg-gray-50 text-gray-700 rounded-lg hover:bg-gray-100 flex items-center gap-2 text-sm"
              >
                <Download className="w-4 h-4" />
                Export
              </button>
              <button
                onClick={() => handleBulkAction('suspend')}
                className="px-3 py-1.5 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 flex items-center gap-2 text-sm"
              >
                <Ban className="w-4 h-4" />
                Suspend
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Select All */}
      {filteredUsers.length > 0 && (
        <div className="mb-4 flex items-center gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={selectedUsers.size === filteredUsers.length}
              onChange={handleSelectAll}
              className="w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500"
            />
            <span className="text-sm text-gray-600">Select all {filteredUsers.length} users</span>
          </label>
        </div>
      )}

      {/* Users Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredUsers.map((user) => {
          const isSelected = selectedUsers.has(user.id);
          const status = getUserStatus(user.last_active_at);
          
          return (
            <div
              key={user.id}
              className={`bg-white rounded-xl shadow-sm hover:shadow-md transition-all border-2 ${
                isSelected ? 'border-indigo-500' : 'border-transparent'
              }`}
            >
              <div className="p-6">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="relative">
                      {user.avatar_url ? (
                        <img
                          src={user.avatar_url}
                          alt={user.username}
                          className="w-12 h-12 rounded-full"
                        />
                      ) : (
                        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold">
                          {user.username?.charAt(0).toUpperCase() || '?'}
                        </div>
                      )}
                      {status.label === 'Online' && (
                        <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 truncate">
                        {user.username}
                      </h3>
                      <p className="text-sm text-gray-500 truncate">{user.email || 'No email'}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => handleSelectUser(user.id)}
                      className="w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500"
                    />
                    <button className="p-1 hover:bg-gray-100 rounded">
                      <MoreVertical className="w-4 h-4 text-gray-400" />
                    </button>
                  </div>
                </div>

                {/* Status and Level */}
                <div className="flex items-center gap-2 mb-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${status.color}`}>
                    {status.label}
                  </span>
                  <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                    Level {user.neural_level}
                  </span>
                  {user.synaptic_streak > 7 && (
                    <span className="px-2 py-1 bg-orange-100 text-orange-700 rounded-full text-xs font-medium">
                      {user.synaptic_streak} day streak
                    </span>
                  )}
                </div>

                {/* Title and Bio */}
                <div className="mb-4">
                  <p className="text-sm font-medium text-gray-900">{user.title}</p>
                  {user.bio && (
                    <p className="text-sm text-gray-600 mt-1 line-clamp-2">{user.bio}</p>
                  )}
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 gap-3 mb-4">
                  <div className="bg-gray-50 rounded-lg p-2">
                    <div className="flex items-center gap-1.5">
                      <Zap className="w-4 h-4 text-yellow-600" />
                      <span className="text-xs text-gray-600">Points</span>
                    </div>
                    <p className="text-sm font-semibold text-gray-900 mt-1">
                      {user.total_points.toLocaleString()}
                    </p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-2">
                    <div className="flex items-center gap-1.5">
                      <Target className="w-4 h-4 text-blue-600" />
                      <span className="text-xs text-gray-600">Nodes</span>
                    </div>
                    <p className="text-sm font-semibold text-gray-900 mt-1">
                      {user.total_nodes_completed}
                    </p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-2">
                    <div className="flex items-center gap-1.5">
                      <Star className="w-4 h-4 text-purple-600" />
                      <span className="text-xs text-gray-600">Crystals</span>
                    </div>
                    <p className="text-sm font-semibold text-gray-900 mt-1">
                      {user.memory_crystals}
                    </p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-2">
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-4 h-4 text-gray-600" />
                      <span className="text-xs text-gray-600">Last Seen</span>
                    </div>
                    <p className="text-sm font-semibold text-gray-900 mt-1">
                      {formatDate(user.last_active_at)}
                    </p>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-2 pt-4 border-t">
                  <button className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors text-sm">
                    <Mail className="w-4 h-4" />
                    Message
                  </button>
                  <button className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-gray-50 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors text-sm">
                    <Shield className="w-4 h-4" />
                    Details
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {filteredUsers.length === 0 && (
        <div className="bg-white rounded-xl shadow-sm p-12">
          <div className="text-center">
            <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No users found</h3>
            <p className="text-gray-500">
              {searchTerm || filterStatus !== 'all' 
                ? 'Try adjusting your search or filters' 
                : 'No users have registered yet'}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}