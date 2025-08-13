'use client';

import React, { useEffect, useState } from 'react';
import { 
  TrendingUp, Clock, Target, Brain, BookOpen, Trophy, 
  Calendar, BarChart3, PieChart, Zap, Star 
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { UserAnalytics, LearningInsight, LearningRecommendation } from '@/services/analyticsService';

interface AnalyticsDashboardProps {
  className?: string;
}

export default function AnalyticsDashboard({ className = '' }: AnalyticsDashboardProps) {
  const { user } = useAuth();
  const [analytics, setAnalytics] = useState<UserAnalytics | null>(null);
  const [insights, setInsights] = useState<LearningInsight[]>([]);
  const [recommendations, setRecommendations] = useState<LearningRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState(30);

  useEffect(() => {
    if (user) {
      fetchAnalyticsData();
    }
  }, [user, selectedPeriod]);

  const fetchAnalyticsData = async () => {
    setLoading(true);
    try {
      // Fetch analytics summary
      const analyticsResponse = await fetch(`/api/analytics?type=summary&days=${selectedPeriod}`);
      if (analyticsResponse.ok) {
        const result = await analyticsResponse.json();
        setAnalytics(result.data);
      }

      // Fetch insights
      const insightsResponse = await fetch('/api/analytics?type=insights');
      if (insightsResponse.ok) {
        const result = await insightsResponse.json();
        setInsights(result.data || []);
      }

      // Fetch recommendations
      const recommendationsResponse = await fetch('/api/analytics?type=recommendations');
      if (recommendationsResponse.ok) {
        const result = await recommendationsResponse.json();
        setRecommendations(result.data || []);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 animate-pulse ${className}`}>
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-6"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="bg-gray-100 rounded-lg p-4">
              <div className="h-4 bg-gray-200 rounded w-2/3 mb-2"></div>
              <div className="h-8 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!user || !analytics) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 text-center ${className}`}>
        <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-600 mb-2">No Analytics Data</h3>
        <p className="text-gray-500">Start learning to see your progress analytics!</p>
      </div>
    );
  }

  const statCards = [
    {
      icon: Clock,
      label: 'Study Time',
      value: `${analytics.total_study_time_hours.toFixed(1)}h`,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      icon: Target,
      label: 'Nodes Completed',
      value: analytics.nodes_completed.toString(),
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      icon: TrendingUp,
      label: 'Avg. Quiz Score',
      value: `${Math.round(analytics.average_quiz_score)}%`,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    {
      icon: Zap,
      label: 'Study Streak',
      value: `${analytics.study_streak_days} days`,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    }
  ];

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'performance': return TrendingUp;
      case 'engagement': return Calendar;
      case 'weak_areas': return Target;
      case 'achievement': return Trophy;
      default: return Star;
    }
  };

  const getInsightColor = (priority: number) => {
    if (priority >= 90) return 'border-red-200 bg-red-50';
    if (priority >= 80) return 'border-yellow-200 bg-yellow-50';
    return 'border-blue-200 bg-blue-50';
  };

  const getRecommendationIcon = (type: string) => {
    switch (type) {
      case 'next_node': return Brain;
      case 'review': return BookOpen;
      case 'challenge': return Trophy;
      default: return Star;
    }
  };

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <BarChart3 className="w-6 h-6 text-purple-600" />
          Learning Analytics
        </h2>
        <select
          value={selectedPeriod}
          onChange={(e) => setSelectedPeriod(Number(e.target.value))}
          className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        >
          <option value={7}>Last 7 days</option>
          <option value={30}>Last 30 days</option>
          <option value={90}>Last 90 days</option>
        </select>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <div className={`${stat.bgColor} rounded-full w-10 h-10 flex items-center justify-center`}>
                  <Icon className={`w-5 h-5 ${stat.color}`} />
                </div>
              </div>
              <div className="text-2xl font-bold text-gray-900 mb-1">{stat.value}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
            </div>
          );
        })}
      </div>

      {/* Charts Section */}
      {analytics.daily_activity && analytics.daily_activity.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Daily Activity Chart */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-blue-600" />
              Daily Activity
            </h3>
            <div className="space-y-2">
              {analytics.daily_activity.slice(0, 7).map((day, index) => (
                <div key={index} className="flex items-center gap-3">
                  <div className="text-sm text-gray-600 w-20">
                    {new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </div>
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full"
                      style={{ width: `${Math.min((day.study_time_minutes / 60) * 100, 100)}%` }}
                    />
                  </div>
                  <div className="text-sm text-gray-700 w-16">
                    {Math.round(day.study_time_minutes)}m
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Domain Distribution */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <PieChart className="w-5 h-5 text-green-600" />
              Domain Focus
            </h3>
            <div className="space-y-3">
              {analytics.most_active_domains && analytics.most_active_domains.slice(0, 5).map((domain, index) => (
                <div key={index} className="flex items-center gap-3">
                  <div className="text-sm text-gray-700 flex-1 truncate">{domain.domain}</div>
                  <div className="flex-2 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-green-500 h-2 rounded-full"
                      style={{ width: `${(domain.count / Math.max(...analytics.most_active_domains.map(d => d.count))) * 100}%` }}
                    />
                  </div>
                  <div className="text-sm text-gray-600 w-8">{domain.count}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Insights and Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Learning Insights */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-600" />
            Learning Insights
          </h3>
          {insights.length > 0 ? (
            <div className="space-y-3">
              {insights.map((insight, index) => {
                const Icon = getInsightIcon(insight.insight_type);
                return (
                  <div
                    key={index}
                    className={`border rounded-lg p-4 ${getInsightColor(insight.priority)}`}
                  >
                    <div className="flex items-start gap-3">
                      <Icon className="w-5 h-5 text-gray-600 mt-0.5" />
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-900 mb-1">{insight.title}</h4>
                        <p className="text-sm text-gray-700 mb-2">{insight.description}</p>
                        <p className="text-xs text-gray-600 italic">{insight.action_suggestion}</p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Star className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p>No insights available yet. Keep learning to generate insights!</p>
            </div>
          )}
        </div>

        {/* Recommendations */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-blue-600" />
            Recommendations
          </h3>
          {recommendations.length > 0 ? (
            <div className="space-y-3">
              {recommendations.slice(0, 5).map((rec, index) => {
                const Icon = getRecommendationIcon(rec.recommendation_type);
                return (
                  <div
                    key={index}
                    className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <Icon className="w-5 h-5 text-blue-600 mt-0.5" />
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h4 className="font-semibold text-gray-900">
                            {(rec as { knowledge_nodes?: { name: string } }).knowledge_nodes?.name || rec.node_id}
                          </h4>
                          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                            {rec.recommendation_type.replace('_', ' ')}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2">{rec.reasoning}</p>
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-gray-500">
                            Priority: {rec.priority_score}/100
                          </span>
                          <div className="w-16 bg-gray-200 rounded-full h-1">
                            <div
                              className="bg-blue-500 h-1 rounded-full"
                              style={{ width: `${rec.priority_score}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Target className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p>No recommendations available. Complete some nodes to get personalized suggestions!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}