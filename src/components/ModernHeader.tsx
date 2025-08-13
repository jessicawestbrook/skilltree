'use client';

import React from 'react';
import { Brain, Flame, Trophy, Star, User, Menu } from 'lucide-react';
import { UserStats } from '../types';
import { useAuth } from '../contexts/AuthContext';

interface ModernHeaderProps {
  userStats: UserStats;
  isMobile?: boolean;
  calculateProgress: () => number;
  onAuthClick: () => void;
  onProfileClick: () => void;
  onMenuClick?: () => void;
}

export default function ModernHeader({ 
  userStats, 
  isMobile = false, 
  calculateProgress, 
  onAuthClick, 
  onProfileClick,
  onMenuClick 
}: ModernHeaderProps) {
  const { user, isAuthenticated } = useAuth();
  const progress = calculateProgress();

  return (
    <header className="sticky top-0 z-40 w-full backdrop-blur-xl bg-white/80 dark:bg-gray-900/80 border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-[1600px] mx-auto px-4 md:px-6">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Left: Logo and Brand */}
          <div className="flex items-center gap-4">
            {isMobile && (
              <button
                onClick={onMenuClick}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                <Menu className="w-5 h-5" />
              </button>
            )}
            
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl blur-lg opacity-50"></div>
                <div className="relative bg-gradient-to-r from-purple-600 to-blue-600 p-2.5 rounded-xl">
                  <Brain className="w-6 h-6 md:w-7 md:h-7 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-xl md:text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                  NeuroQuest
                </h1>
                <p className="text-xs text-gray-600 dark:text-gray-400 font-medium hidden md:block">
                  Master All Human Knowledge
                </p>
              </div>
            </div>
          </div>

          {/* Center: Stats */}
          {isAuthenticated && (
            <div className="hidden md:flex items-center gap-6">
              {/* Streak */}
              <div className="flex items-center gap-2">
                <div className="p-2 bg-orange-100 dark:bg-orange-900/30 rounded-lg">
                  <Flame className="w-4 h-4 text-orange-600 dark:text-orange-400" />
                </div>
                <div>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Streak</p>
                  <p className="text-sm font-bold text-gray-900 dark:text-gray-100">
                    {userStats.synapticStreak} days
                  </p>
                </div>
              </div>

              {/* Points */}
              <div className="flex items-center gap-2">
                <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
                  <Star className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                </div>
                <div>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Points</p>
                  <p className="text-sm font-bold text-gray-900 dark:text-gray-100">
                    {(userStats.totalPoints || userStats.pathfinderPoints).toLocaleString()}
                  </p>
                </div>
              </div>

              {/* Level */}
              <div className="flex items-center gap-2">
                <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                  <Trophy className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Level</p>
                  <p className="text-sm font-bold text-gray-900 dark:text-gray-100">
                    {userStats.neuralLevel}
                  </p>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-32">
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Progress</p>
                <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-purple-600 to-blue-600 transition-all duration-500"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Right: User Actions */}
          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <>
                <button
                  onClick={onProfileClick}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-gray-800 rounded-xl hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                >
                  {user?.photoURL ? (
                    <img src={user.photoURL} alt="Profile" className="w-6 h-6 rounded-full" />
                  ) : (
                    <User className="w-4 h-4" />
                  )}
                  <span className="text-sm font-medium hidden md:block">
                    {user?.username || 'Profile'}
                  </span>
                </button>
              </>
            ) : (
              <button
                onClick={onAuthClick}
                className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl hover:shadow-lg transition-all duration-200 font-medium text-sm"
              >
                <User className="w-4 h-4" />
                <span>Sign In</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}