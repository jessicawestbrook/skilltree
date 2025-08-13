'use client';

import React, { useEffect, useState } from 'react';
import { Brain, TrendingUp, Target, Trophy, Star, ChevronRight } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { LearningInsight, LearningRecommendation } from '@/services/analyticsService';

export default function LearningInsights() {
  const { user } = useAuth();
  const [insights, setInsights] = useState<LearningInsight[]>([]);
  const [recommendations, setRecommendations] = useState<LearningRecommendation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      fetchInsights();
    }
  }, [user]);

  const fetchInsights = async () => {
    try {
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
      console.error('Error fetching insights:', error);
    } finally {
      setLoading(false);
    }
  };

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'performance': return TrendingUp;
      case 'engagement': return Brain;
      case 'weak_areas': return Target;
      case 'achievement': return Trophy;
      default: return Star;
    }
  };

  const getInsightColor = (priority: number) => {
    if (priority >= 90) return 'border-l-red-500 bg-red-50';
    if (priority >= 80) return 'border-l-yellow-500 bg-yellow-50';
    return 'border-l-blue-500 bg-blue-50';
  };

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-2/3 mb-3"></div>
          <div className="space-y-2">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-3/4"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="space-y-4">
      {/* Top Insight */}
      {insights.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
          <h3 className="text-base font-bold text-gray-900 dark:text-gray-100 mb-3 flex items-center gap-2">
            <Brain className="w-4 h-4 text-purple-600" />
            Learning Insight
          </h3>
          
          {(() => {
            const topInsight = insights.sort((a, b) => b.priority - a.priority)[0];
            const Icon = getInsightIcon(topInsight.insight_type);
            
            return (
              <div className={`border-l-4 rounded-lg p-3 ${getInsightColor(topInsight.priority)}`}>
                <div className="flex items-start gap-2">
                  <Icon className="w-4 h-4 text-gray-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-gray-900 text-sm mb-1">
                      {topInsight.title}
                    </h4>
                    <p className="text-xs text-gray-700 mb-2">
                      {topInsight.description}
                    </p>
                    <p className="text-xs text-gray-600 italic">
                      💡 {topInsight.action_suggestion}
                    </p>
                  </div>
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* Recommended Next Steps */}
      {recommendations.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
          <h3 className="text-base font-bold text-gray-900 dark:text-gray-100 mb-3 flex items-center gap-2">
            <Target className="w-4 h-4 text-blue-600" />
            Recommended Next
          </h3>
          
          <div className="space-y-2">
            {recommendations
              .sort((a, b) => b.priority_score - a.priority_score)
              .slice(0, 3)
              .map((rec, index) => {
                const isNextNode = rec.recommendation_type === 'next_node';
                const isReview = rec.recommendation_type === 'review';
                
                return (
                  <div 
                    key={index}
                    className="flex items-center gap-3 p-2 bg-gray-50 dark:bg-gray-900 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer"
                  >
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold ${
                      isNextNode ? 'bg-green-500' : isReview ? 'bg-yellow-500' : 'bg-blue-500'
                    }`}>
                      {isNextNode ? '→' : isReview ? '↺' : '★'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-semibold text-gray-900 dark:text-gray-100 truncate">
                        {(rec as { knowledge_nodes?: { name: string } }).knowledge_nodes?.name || rec.node_id}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 truncate">
                        {rec.recommendation_type.replace('_', ' ')} • Priority {rec.priority_score}
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-gray-400 flex-shrink-0" />
                  </div>
                );
              })}
          </div>
          
          <button 
            onClick={() => window.location.href = '/analytics'}
            className="w-full mt-3 text-xs text-blue-600 hover:text-blue-800 font-medium text-center py-2 hover:bg-blue-50 rounded-lg transition-colors"
          >
            View Full Analytics →
          </button>
        </div>
      )}

      {/* No Data State */}
      {insights.length === 0 && recommendations.length === 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 text-center">
          <Brain className="w-8 h-8 text-gray-400 mx-auto mb-2" />
          <h3 className="text-sm font-semibold text-gray-600 mb-1">No Insights Yet</h3>
          <p className="text-xs text-gray-500">
            Complete some quizzes to get personalized learning insights!
          </p>
        </div>
      )}
    </div>
  );
}