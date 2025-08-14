'use client';

import React, { useEffect, useState } from 'react';
import { Trophy, Brain, Target, Zap, TrendingUp } from 'lucide-react';
import { ProgressService } from '@/services/progressService';
import { useAuth } from '@/contexts/AuthContext';

interface ProgressStats {
  totalNodes: number;
  totalPoints: number;
  averageScore: number;
  neuralLevel: number;
}

export default function ProgressTracker() {
  const { user } = useAuth();
  const [stats, setStats] = useState<ProgressStats>({
    totalNodes: 0,
    totalPoints: 0,
    averageScore: 0,
    neuralLevel: 1
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      if (!user) {
        setLoading(false);
        return;
      }

      try {
        const summary = await ProgressService.getProgressSummary();
        if (summary) {
          setStats({
            totalNodes: summary.totalNodes || 0,
            totalPoints: summary.totalPoints || 0,
            averageScore: summary.averageScore || 0,
            neuralLevel: Math.floor((summary.totalPoints || 0) / 200) + 1
          });
        } else {
          // Set default values if no summary is available
          setStats({
            totalNodes: 0,
            totalPoints: 0,
            averageScore: 0,
            neuralLevel: 1
          });
        }
      } catch (error) {
        console.error('Error fetching progress summary:', error instanceof Error ? error.message : error);
        // Set default values on error
        setStats({
          totalNodes: 0,
          totalPoints: 0,
          averageScore: 0,
          neuralLevel: 1
        });
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
  }, [user]);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="text-center">
              <div className="h-8 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3 mx-auto"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const progressItems = [
    {
      icon: Brain,
      label: 'Neural Level',
      value: stats.neuralLevel,
      color: 'text-forest-600',
      bgColor: 'bg-forest-100'
    },
    {
      icon: Target,
      label: 'Nodes Completed',
      value: stats.totalNodes,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      icon: Zap,
      label: 'Total Points',
      value: stats.totalPoints,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100'
    },
    {
      icon: TrendingUp,
      label: 'Avg. Score',
      value: `${Math.round(stats.averageScore)}%`,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <Trophy className="w-5 h-5 text-yellow-500" />
        Your Progress
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {progressItems.map((item, index) => {
          const Icon = item.icon;
          return (
            <div key={index} className="text-center">
              <div className={`${item.bgColor} rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-2`}>
                <Icon className={`w-6 h-6 ${item.color}`} />
              </div>
              <div className="text-2xl font-bold text-gray-900">{item.value}</div>
              <div className="text-sm text-gray-600">{item.label}</div>
            </div>
          );
        })}
      </div>
      
      {/* Progress bar for next level */}
      <div className="mt-6">
        <div className="flex justify-between text-sm text-gray-600 mb-1">
          <span>Level {stats.neuralLevel}</span>
          <span>Level {stats.neuralLevel + 1}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-forest-500 to-sky-500 h-2 rounded-full transition-all"
            style={{ width: `${(stats.totalPoints % 200) / 2}%` }}
          />
        </div>
        <div className="text-center text-xs text-gray-500 mt-1">
          {200 - (stats.totalPoints % 200)} points to next level
        </div>
      </div>
    </div>
  );
}