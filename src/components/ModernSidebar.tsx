'use client';

import React from 'react';
import { Search, Filter, BookOpen, Brain, Trophy, Target, Users, UserPlus, Activity, ChevronRight } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { knowledgeStructure } from '@/data/comprehensiveKnowledgeStructure';

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
  const router = useRouter();

  // Get main knowledge categories from the actual data structure
  const mainCategories = knowledgeStructure.subcategories || [];
  
  const categoryIcons: { [key: string]: string } = {
    mathematics: '🧮',
    sciences: '🔬',
    languages: '🗣️',
    arts: '🎨',
    technology: '💻',
    history: '📚',
    'social-sciences': '👥',
    'practical-skills': '🛠️',
    'health-fitness': '💪',
    'philosophy-religion': '🤔',
    business: '💼'
  };

  const handleCategoryClick = (categoryId: string) => {
    router.push(`/category/${categoryId}`);
  };

  return (
    <div className="space-y-4 overflow-visible relative" style={{ zIndex: 100 }}>
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

      {/* Knowledge Categories */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 relative" style={{ zIndex: 100 }}>
        <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
          <BookOpen className="w-4 h-4" />
          Knowledge Categories
        </h3>
        <div className="space-y-1 relative" style={{ zIndex: 100 }}>
          {mainCategories.map((category) => {
            const icon = categoryIcons[category.id] || '📚';
            const hasSubcategories = category.subcategories && category.subcategories.length > 0;
            
            return (
              <div key={category.id} className="relative group/category z-auto">
                <button
                  onClick={() => handleCategoryClick(category.id)}
                  className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 group relative z-10"
                >
                  <span className="text-base">{icon}</span>
                  <div className="flex-1 text-left">
                    <div className="text-sm font-medium">{category.name}</div>
                    <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
                      {category.description}
                    </div>
                  </div>
                  <ChevronRight size={14} className="text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300" />
                </button>
                
                {/* Hover Menu for Subcategories */}
                {hasSubcategories && (
                  <div 
                    className="absolute left-full top-0 ml-2 w-64 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 opacity-0 invisible group-hover/category:opacity-100 group-hover/category:visible transition-all duration-200 pointer-events-none group-hover/category:pointer-events-auto isolate"
                    style={{ 
                      zIndex: 999999,
                      position: 'absolute'
                    }}
                  >
                    <div className="p-3">
                      <div className="text-xs font-semibold text-gray-600 dark:text-gray-400 mb-2 px-2">
                        {category.name} Subcategories
                      </div>
                      <div className="space-y-1 max-h-80 overflow-y-auto">
                        {category.subcategories.map((subcategory) => (
                          <button
                            key={subcategory.id}
                            onClick={() => router.push(`/category/${category.id}/${subcategory.id}`)}
                            className="w-full flex items-start gap-2 px-2 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-left transition-colors group/sub"
                          >
                            <div 
                              className="w-3 h-3 rounded-full mt-1 flex-shrink-0"
                              style={{ backgroundColor: subcategory.color }}
                            />
                            <div className="flex-1 min-w-0">
                              <div className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover/sub:text-blue-600 dark:group-hover/sub:text-blue-400 transition-colors">
                                {subcategory.name}
                              </div>
                              <div className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2 leading-relaxed">
                                {subcategory.description.length > 60 
                                  ? `${subcategory.description.substring(0, 60)}...` 
                                  : subcategory.description
                                }
                              </div>
                              {subcategory.subcategories && (
                                <div className="text-xs text-gray-400 mt-1">
                                  {subcategory.subcategories.length} subcategories
                                </div>
                              )}
                              {subcategory.nodes && (
                                <div className="text-xs text-gray-400 mt-1">
                                  {subcategory.nodes.length} topics
                                </div>
                              )}
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Legacy Domain Filters - for backward compatibility */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
          <Filter className="w-4 h-4" />
          Legacy Filters
        </h3>
        <div className="space-y-2">
          {mainCategories.slice(0, 6).map((category) => {
            const isActive = activeFilters.includes(category.id);
            const icon = categoryIcons[category.id] || '📚';
            return (
              <button
                key={category.id}
                onClick={() => toggleFilter(category.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${
                  isActive
                    ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 font-medium'
                    : 'hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`}
              >
                <span className="text-lg">{icon}</span>
                <span className="text-sm">{category.name}</span>
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