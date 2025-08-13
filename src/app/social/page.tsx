'use client';

import React, { useState } from 'react';
import FriendsPanel from '@/components/social/FriendsPanel';
import StudyGroupsPanel from '@/components/social/StudyGroupsPanel';
import ActivityFeed from '@/components/social/ActivityFeed';
import { Users, UserPlus, Activity, BookOpen } from 'lucide-react';

export default function SocialPage() {
  const [activeView, setActiveView] = useState<'feed' | 'friends' | 'groups'>('feed');

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Social Hub</h1>
          <p className="text-gray-600 dark:text-gray-300">
            Connect with fellow learners, join study groups, and track your community's progress
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Navigation Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
              <nav className="space-y-2">
                <button
                  onClick={() => setActiveView('feed')}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    activeView === 'feed'
                      ? 'bg-blue-500 text-white'
                      : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <Activity className="w-5 h-5" />
                  <span className="font-medium">Activity Feed</span>
                </button>
                
                <button
                  onClick={() => setActiveView('friends')}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    activeView === 'friends'
                      ? 'bg-blue-500 text-white'
                      : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <UserPlus className="w-5 h-5" />
                  <span className="font-medium">Friends</span>
                </button>
                
                <button
                  onClick={() => setActiveView('groups')}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    activeView === 'groups'
                      ? 'bg-blue-500 text-white'
                      : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <Users className="w-5 h-5" />
                  <span className="font-medium">Study Groups</span>
                </button>
              </nav>
            </div>

            {/* Quick Stats */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 mt-6">
              <h3 className="font-semibold mb-4">Your Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-300">Friends</span>
                  <span className="font-bold">0</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-300">Groups</span>
                  <span className="font-bold">0</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-300">Activities</span>
                  <span className="font-bold">0</span>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {activeView === 'feed' && <ActivityFeed />}
            {activeView === 'friends' && <FriendsPanel />}
            {activeView === 'groups' && <StudyGroupsPanel />}
          </div>
        </div>
      </div>
    </div>
  );
}