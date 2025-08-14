'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Activity, Trophy, Target, Users, BookOpen, Award, Clock, TrendingUp } from 'lucide-react';
import { safeFetch } from '@/utils/apiHelpers';

interface ActivityItem {
  id: string;
  user_id: string;
  activity_type: string;
  title: string;
  description?: string;
  metadata: any;
  visibility: string;
  created_at: string;
  user?: {
    id: string;
    email: string;
    user_profiles: {
      username: string;
      avatar_url?: string;
      neural_level: number;
    };
  };
  group?: {
    id: string;
    name: string;
  };
}

const activityIcons: { [key: string]: any } = {
  achievement_earned: Trophy,
  level_up: TrendingUp,
  node_completed: Target,
  friend_added: Users,
  group_joined: Users,
  group_created: Users,
  challenge_completed: Award,
  quiz_completed: BookOpen,
  streak_milestone: Clock,
};

interface ActivityFeedProps {
  compact?: boolean;
}

export default function ActivityFeed({ compact = false }: ActivityFeedProps = {}) {
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'friends' | 'groups' | 'personal'>('all');
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const limit = 20;

  const fetchActivities = useCallback(async (reset = false) => {
    const currentOffset = reset ? 0 : offset;
    setLoading(true);
    
    try {
      const data = await safeFetch(
        `/api/activity-feed?filter=${filter}&limit=${limit}&offset=${currentOffset}`
      );
      
      if (reset) {
        setActivities(data.data || []);
      } else {
        setActivities(prev => [...prev, ...(data.data || [])]);
      }
      setHasMore(data.hasMore);
      setOffset(currentOffset + limit);
    } catch (error) {
      console.error('Error fetching activities:', error);
    } finally {
      setLoading(false);
    }
  }, [filter, offset]);

  useEffect(() => {
    setOffset(0);
    fetchActivities(true);
  }, [filter]);

  const getActivityIcon = (type: string) => {
    const Icon = activityIcons[type] || Activity;
    return <Icon className="w-5 h-5" />;
  };

  const getActivityColor = (type: string) => {
    const colors: { [key: string]: string } = {
      achievement_earned: 'text-yellow-500',
      level_up: 'text-forest-500',
      node_completed: 'text-green-500',
      friend_added: 'text-blue-500',
      group_joined: 'text-cyan-500',
      group_created: 'text-indigo-500',
      challenge_completed: 'text-orange-500',
      quiz_completed: 'text-emerald-500',
      streak_milestone: 'text-red-500',
    };
    return colors[type] || 'text-gray-500';
  };

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'just now';
  };

  // Compact version for sidebar - no wrapper, no filters
  if (compact) {
    return (
      <div className="space-y-2 max-h-56 overflow-y-auto pr-2 custom-scrollbar">
        {loading ? (
          <div className="text-center text-gray-500 py-4 text-sm">
            Loading activities...
          </div>
        ) : activities.length === 0 ? (
          <div className="text-center text-gray-500 py-4 text-sm">
            No recent activity
          </div>
        ) : (
          activities.slice(0, 5).map((activity) => (
            <div
              key={activity.id}
              className="flex items-start gap-2 p-2 bg-gray-50 dark:bg-gray-700/50 rounded-lg text-sm"
            >
              <div className={`mt-0.5 flex-shrink-0 ${getActivityColor(activity.activity_type)}`}>
                {React.cloneElement(getActivityIcon(activity.activity_type), { size: 14 })}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs">
                  <span className="font-medium text-gray-900 dark:text-gray-100">
                    {activity.user?.user_profiles?.username || 'Someone'}
                  </span>
                  <span className="text-gray-600 dark:text-gray-400 ml-1">
                    {activity.title}
                  </span>
                </p>
                <p className="text-xs text-gray-500 mt-0.5">
                  {formatTimeAgo(activity.created_at)}
                </p>
              </div>
            </div>
          ))
        )}
        <style jsx>{`
          .custom-scrollbar::-webkit-scrollbar {
            width: 4px;
          }
          .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent;
          }
          .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(156, 163, 175, 0.3);
            border-radius: 2px;
          }
          .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(156, 163, 175, 0.5);
          }
        `}</style>
      </div>
    );
  }

  // Full version with wrapper and filters
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <Activity className="w-6 h-6" />
          Activity Feed
        </h2>
      </div>

      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setFilter('all')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
            filter === 'all'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          All Activity
        </button>
        <button
          onClick={() => setFilter('friends')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
            filter === 'friends'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          Friends
        </button>
        <button
          onClick={() => setFilter('groups')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
            filter === 'groups'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          Groups
        </button>
        <button
          onClick={() => setFilter('personal')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
            filter === 'personal'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          My Activity
        </button>
      </div>

      <div className="space-y-4">
        {activities.length === 0 && !loading ? (
          <div className="text-center text-gray-500 py-8">
            No activities to show
          </div>
        ) : (
          activities.map((activity) => (
            <div
              key={activity.id}
              className="flex items-start gap-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
            >
              <div className={`mt-1 ${getActivityColor(activity.activity_type)}`}>
                {getActivityIcon(activity.activity_type)}
              </div>
              
              <div className="flex-1">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-semibold">
                      {activity.user?.user_profiles?.username || 'Anonymous'}
                      <span className="font-normal text-gray-600 dark:text-gray-300 ml-2">
                        {activity.title}
                      </span>
                    </p>
                    {activity.description && (
                      <p className="text-sm text-gray-500 mt-1">
                        {activity.description}
                      </p>
                    )}
                    {activity.group && (
                      <p className="text-sm text-blue-500 mt-1">
                        in {activity.group.name}
                      </p>
                    )}
                  </div>
                  <span className="text-xs text-gray-400">
                    {formatTimeAgo(activity.created_at)}
                  </span>
                </div>

                {activity.metadata && Object.keys(activity.metadata).length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-2">
                    {activity.metadata.points && (
                      <span className="text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-600 dark:text-yellow-300 px-2 py-1 rounded">
                        +{activity.metadata.points} points
                      </span>
                    )}
                    {activity.metadata.level && (
                      <span className="text-xs bg-forest-100 dark:bg-forest-900 text-forest-600 dark:text-forest-300 px-2 py-1 rounded">
                        Level {activity.metadata.level}
                      </span>
                    )}
                    {activity.metadata.streak && (
                      <span className="text-xs bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-300 px-2 py-1 rounded">
                        {activity.metadata.streak} day streak
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))
        )}

        {loading && (
          <div className="text-center py-4">
            <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          </div>
        )}

        {hasMore && !loading && (
          <button
            onClick={() => fetchActivities()}
            className="w-full py-2 text-blue-500 hover:text-blue-600 font-medium"
          >
            Load more
          </button>
        )}
      </div>
    </div>
  );
}