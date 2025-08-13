'use client';

import React from 'react';
import { Search, Filter, BookOpen, Brain, Trophy, Target, Users, UserPlus, Activity } from 'lucide-react';
import Link from 'next/link';

interface ModernSidebarProps {
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  currentView: string;
  setCurrentView: (view: string) => void;
  activeFilters: string[];
  toggleFilter: (filter: string) => void;
}

export default function ModernSidebar({
  searchTerm,
  setSearchTerm,
  currentView,
  setCurrentView,
  activeFilters,
  toggleFilter
}: ModernSidebarProps) {
  const views = [
    { id: 'all', label: 'All Nodes', icon: Brain, color: 'purple' },
    { id: 'available', label: 'Available', icon: Target, color: 'blue' },
    { id: 'completed', label: 'Completed', icon: Trophy, color: 'green' },
    { id: 'locked', label: 'Locked', icon: BookOpen, color: 'gray' }
  ];

  const filters = [
    { id: 'fundamentals', label: 'Fundamentals', icon: '📚' },
    { id: 'specialized', label: 'Specialized', icon: '🎯' },
    { id: 'advanced', label: 'Advanced', icon: '🚀' },
    { id: 'practical', label: 'Practical', icon: '🛠️' }
  ];

  return (
    <div className="space-y-4">
      {/* Search */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search knowledge..."
            className="w-full pl-10 pr-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:focus:ring-purple-400 text-gray-900 dark:text-gray-100 placeholder-gray-500"
          />
        </div>
      </div>

      {/* View Selector */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
          <Filter className="w-4 h-4" />
          View Mode
        </h3>
        <div className="space-y-2">
          {views.map((view) => {
            const Icon = view.icon;
            const isActive = currentView === view.id;
            return (
              <button
                key={view.id}
                onClick={() => setCurrentView(view.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${
                  isActive
                    ? `bg-${view.color}-100 dark:bg-${view.color}-900/30 text-${view.color}-700 dark:text-${view.color}-300 font-medium`
                    : 'hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span className="text-sm">{view.label}</span>
                {isActive && (
                  <div className="ml-auto w-2 h-2 bg-current rounded-full"></div>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Category Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
          Categories
        </h3>
        <div className="space-y-2">
          {filters.map((filter) => {
            const isActive = activeFilters.includes(filter.id);
            return (
              <button
                key={filter.id}
                onClick={() => toggleFilter(filter.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${
                  isActive
                    ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 font-medium'
                    : 'hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`}
              >
                <span className="text-lg">{filter.icon}</span>
                <span className="text-sm">{filter.label}</span>
                <div className={`ml-auto w-4 h-4 rounded border-2 transition-all ${
                  isActive
                    ? 'bg-purple-600 border-purple-600'
                    : 'border-gray-300 dark:border-gray-600'
                }`}>
                  {isActive && (
                    <svg className="w-full h-full text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Social Hub */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">Social Hub</h3>
        <Link href="/social" className="block">
          <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-3 mb-3 cursor-pointer hover:from-green-600 hover:to-emerald-700 transition-all">
            <div className="flex items-center gap-3 text-white">
              <Users className="w-5 h-5" />
              <div>
                <div className="font-semibold text-sm">Connect & Learn Together</div>
                <div className="text-xs opacity-90">Join study groups, make friends</div>
              </div>
            </div>
          </div>
        </Link>
        
        <div className="grid grid-cols-2 gap-2">
          <Link href="/social?tab=friends" className="block">
            <button className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-all flex items-center justify-center gap-2 text-gray-700 dark:text-gray-300 text-sm">
              <UserPlus className="w-4 h-4" />
              Friends
            </button>
          </Link>
          
          <Link href="/social?tab=activity" className="block">
            <button className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-all flex items-center justify-center gap-2 text-gray-700 dark:text-gray-300 text-sm">
              <Activity className="w-4 h-4" />
              Activity
            </button>
          </Link>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl shadow-lg p-4 text-white">
        <h3 className="text-sm font-semibold mb-3">Your Progress</h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm opacity-90">Nodes Completed</span>
            <span className="font-bold">42/150</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm opacity-90">Mastery Level</span>
            <span className="font-bold">28%</span>
          </div>
          <div className="w-full bg-white/20 rounded-full h-2 mt-2">
            <div className="bg-white h-2 rounded-full" style={{ width: '28%' }}></div>
          </div>
        </div>
      </div>
    </div>
  );
}