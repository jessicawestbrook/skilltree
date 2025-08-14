'use client';

import React from 'react';
import { Trees, Flame, Trophy, Star, User, Menu, Users, Settings } from 'lucide-react';
import { UserStats } from '../types';
import { useAuth } from '../contexts/AuthContext';
import Link from 'next/link';

interface ModernHeaderProps {
  userStats: UserStats;
  isMobile?: boolean;
  calculateProgress: () => number;
  onAuthClick: () => void;
  onMenuClick?: () => void;
  onSettingsClick?: () => void;
}

export default function ModernHeader({ 
  userStats, 
  isMobile = false, 
  calculateProgress, 
  onAuthClick,
  onMenuClick,
  onSettingsClick 
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
                <div className="absolute inset-0 bg-gradient-to-r from-forest-600 to-sky-600 rounded-xl blur-lg opacity-50"></div>
                <div className="relative bg-gradient-to-r from-forest-600 to-sky-600 p-2.5 rounded-xl">
                  <Trees className="w-6 h-6 md:w-7 md:h-7 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-xl md:text-2xl font-bold bg-gradient-to-r from-forest-600 to-sky-600 bg-clip-text text-transparent">
                  SkillTree
                </h1>
                <p className="text-xs text-gray-600 dark:text-gray-400 font-medium hidden md:block">
                  Grow Your Skills. Master Your Future.
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
                <div className="p-2 bg-sky-100 dark:bg-sky-900/30 rounded-lg">
                  <Star className="w-4 h-4 text-sky-600 dark:text-sky-400" />
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
                    className="h-full bg-gradient-to-r from-forest-600 to-sky-600 transition-all duration-500"
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
                {/* Settings & Profile Button */}
                <button
                  onClick={onSettingsClick}
                  className="group relative flex items-center gap-3 px-4 py-2.5 bg-white dark:bg-gray-800 rounded-xl hover:bg-gradient-to-r hover:from-forest-50 hover:to-sky-50 dark:hover:from-gray-800 dark:hover:to-gray-700 transition-all duration-300 border-2 border-gray-200 dark:border-gray-700 hover:border-forest-400 dark:hover:border-forest-600 hover:shadow-xl shadow-lg"
                  aria-label="Settings & Profile"
                >
                  {/* Avatar */}
                  <div className="relative">
                    {user?.photoURL ? (
                      <img 
                        src={user.photoURL} 
                        alt="Profile" 
                        className="w-8 h-8 rounded-full border-2 border-gray-300 dark:border-gray-600 group-hover:border-forest-500 transition-all duration-300" 
                      />
                    ) : (
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-forest-500 to-sky-500 flex items-center justify-center shadow-inner">
                        <User className="w-4 h-4 text-white" />
                      </div>
                    )}
                    {/* Hover glow effect */}
                    <div className="absolute inset-0 rounded-full bg-gradient-to-r from-forest-400 to-sky-400 opacity-0 group-hover:opacity-40 blur-md transition-opacity duration-300 pointer-events-none"></div>
                  </div>
                  
                  {/* Username with gradient on hover */}
                  <span className="text-sm font-semibold text-gray-700 dark:text-gray-200 group-hover:bg-gradient-to-r group-hover:from-forest-600 group-hover:to-sky-600 group-hover:bg-clip-text group-hover:text-transparent transition-all duration-300 hidden md:block">
                    {user?.username || 'Profile'}
                  </span>
                  
                  {/* Settings icon with animation */}
                  <div className="relative">
                    <Settings className="w-4 h-4 text-gray-500 dark:text-gray-400 group-hover:text-forest-600 dark:group-hover:text-forest-400 transition-all duration-500 group-hover:rotate-180" />
                  </div>
                  
                  {/* Premium shine overlay */}
                  <div className="absolute inset-0 rounded-xl overflow-hidden pointer-events-none">
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/0 group-hover:via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                  </div>
                </button>
              </>
            ) : (
              <button
                onClick={onAuthClick}
                className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-forest-600 to-sky-600 text-white rounded-xl hover:shadow-lg transition-all duration-200 font-medium text-sm"
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