'use client';

import React, { useState, useEffect } from 'react';
import { Search, BookOpen, Brain, Trophy, Target, Users, UserPlus, Activity, ChevronRight, Zap, TrendingUp, ChevronDown, Plus, Minus, Settings, Moon, Sun, Bell, Volume2, VolumeX, Eye, EyeOff, Palette, Bookmark } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
// Lazy load the knowledge structure to improve performance
const getKnowledgeStructure = () => import('@/data/comprehensiveKnowledgeStructure').then(m => m.knowledgeStructure);
import FriendsPanel from '@/components/social/FriendsPanel';
import StudyGroupsPanel from '@/components/social/StudyGroupsPanel';
import BookmarksPanel from '@/components/BookmarksPanel';
import { ProgressService } from '@/services/progressService';
import { useAuth } from '@/contexts/AuthContext';

interface ModernSidebarProps {
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  currentView: string;
  setCurrentView: (view: string) => void;
  activeFilters: string[];
  toggleFilter: (filter: string) => void;
}

interface ProgressStats {
  totalNodes: number;
  totalPoints: number;
  averageScore: number;
  neuralLevel: number;
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
  const { user } = useAuth();
  const [showSocialPanel, setShowSocialPanel] = useState<'friends' | 'groups' | 'bookmarks' | null>(null);
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [hoveredCategory, setHoveredCategory] = useState<string | null>(null);
  const [showSettings, setShowSettings] = useState(false);
  const [settings, setSettings] = useState({
    theme: 'system', // 'light', 'dark', 'system'
    colorScheme: 'forest', // 'forest', 'ocean', 'sunset', 'purple', 'emerald'
    notifications: true,
    sound: true,
    focusMode: false,
    compactMode: false
  });

  // Color schemes configuration
  const colorSchemes = {
    forest: {
      name: 'Forest Green',
      primary: 'forest',
      colors: {
        50: '#f0fdf4',
        100: '#dcfce7',
        200: '#bbf7d0',
        300: '#86efac',
        400: '#4ade80',
        500: '#22c55e',
        600: '#16a34a',
        700: '#15803d',
        800: '#166534',
        900: '#14532d'
      },
      accent: '#10b981'
    },
    ocean: {
      name: 'Ocean Blue',
      primary: 'blue',
      colors: {
        50: '#eff6ff',
        100: '#dbeafe',
        200: '#bfdbfe',
        300: '#93c5fd',
        400: '#60a5fa',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
        800: '#1e40af',
        900: '#1e3a8a'
      },
      accent: '#0ea5e9'
    },
    sunset: {
      name: 'Sunset Orange',
      primary: 'orange',
      colors: {
        50: '#fff7ed',
        100: '#ffedd5',
        200: '#fed7aa',
        300: '#fdba74',
        400: '#fb923c',
        500: '#f97316',
        600: '#ea580c',
        700: '#c2410c',
        800: '#9a3412',
        900: '#7c2d12'
      },
      accent: '#f59e0b'
    },
    purple: {
      name: 'Royal Purple',
      primary: 'purple',
      colors: {
        50: '#faf5ff',
        100: '#f3e8ff',
        200: '#e9d5ff',
        300: '#d8b4fe',
        400: '#c084fc',
        500: '#a855f7',
        600: '#9333ea',
        700: '#7c3aed',
        800: '#6b21a8',
        900: '#581c87'
      },
      accent: '#8b5cf6'
    },
    emerald: {
      name: 'Emerald Teal',
      primary: 'emerald',
      colors: {
        50: '#ecfdf5',
        100: '#d1fae5',
        200: '#a7f3d0',
        300: '#6ee7b7',
        400: '#34d399',
        500: '#10b981',
        600: '#059669',
        700: '#047857',
        800: '#065f46',
        900: '#064e3b'
      },
      accent: '#14b8a6'
    }
  };
  const [stats, setStats] = useState<ProgressStats>({
    totalNodes: 0,
    totalPoints: 0,
    averageScore: 0,
    neuralLevel: 1
  });
  const [progressLoading, setProgressLoading] = useState(true);

  // Fetch progress data
  useEffect(() => {
    const fetchProgress = async () => {
      if (!user) {
        setProgressLoading(false);
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
          setStats({
            totalNodes: 0,
            totalPoints: 0,
            averageScore: 0,
            neuralLevel: 1
          });
        }
      } catch (error) {
        console.error('Error fetching progress summary:', error instanceof Error ? error.message : error);
        setStats({
          totalNodes: 0,
          totalPoints: 0,
          averageScore: 0,
          neuralLevel: 1
        });
      } finally {
        setProgressLoading(false);
      }
    };

    fetchProgress();
  }, [user]);

  // Get main knowledge categories - lazy loaded
  const [mainCategories, setMainCategories] = useState<any[]>([]);
  
  useEffect(() => {
    // Load categories after component mounts
    getKnowledgeStructure().then(structure => {
      setMainCategories(structure.subcategories || []);
    });
  }, []);
  
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

  const handleSubcategoryClick = (categoryId: string, subcategoryId: string) => {
    router.push(`/category/${categoryId}/${subcategoryId}`);
  };

  const handleNodeClick = (nodeId: string) => {
    // For now, navigate to main page with node selected
    // In future, could open a modal or navigate to learning page
    router.push(`/?node=${nodeId}`);
  };

  const toggleCategoryExpansion = (categoryId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(categoryId)) {
      newExpanded.delete(categoryId);
    } else {
      newExpanded.add(categoryId);
    }
    setExpandedCategories(newExpanded);
  };

  const renderSubcategoryNodes = (subcategory: any, categoryId: string) => {
    if (!subcategory.nodes || subcategory.nodes.length === 0) return null;
    
    return (
      <div className="ml-4 mt-2 space-y-1">
        {subcategory.nodes.slice(0, 3).map((node: any) => (
          <div
            key={node.id}
            onClick={() => handleNodeClick(node.id)}
            className="w-full text-left px-2 py-1 text-xs text-gray-600 dark:text-gray-400 hover:text-forest-600 dark:hover:text-forest-400 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded transition-colors cursor-pointer"
            title={`Study ${node.name}`}
          >
            • {node.name}
          </div>
        ))}
        {subcategory.nodes.length > 3 && (
          <div
            onClick={() => handleSubcategoryClick(categoryId, subcategory.id)}
            className="w-full text-left px-2 py-1 text-xs text-gray-500 dark:text-gray-500 hover:text-forest-600 dark:hover:text-forest-400 italic cursor-pointer"
          >
            + {subcategory.nodes.length - 3} more topics...
          </div>
        )}
      </div>
    );
  };

  const updateSetting = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    // In a real app, you'd save to localStorage or API here
    localStorage.setItem('userSettings', JSON.stringify({ ...settings, [key]: value }));
  };

  // Get current color scheme
  const currentColorScheme = colorSchemes[settings.colorScheme as keyof typeof colorSchemes];

  // Generate dynamic CSS classes based on color scheme
  const getColorClasses = (variant: 'primary' | 'secondary' | 'accent' | 'hover' | 'border') => {
    const scheme = currentColorScheme;
    switch (variant) {
      case 'primary':
        return `bg-[${scheme.colors[100]}] dark:bg-[${scheme.colors[900]}]/30 text-[${scheme.colors[700]}] dark:text-[${scheme.colors[300]}] border border-[${scheme.colors[200]}] dark:border-[${scheme.colors[700]}]`;
      case 'secondary':
        return `bg-[${scheme.colors[50]}] dark:bg-[${scheme.colors[900]}]/10 text-[${scheme.colors[600]}] dark:text-[${scheme.colors[400]}]`;
      case 'accent':
        return `bg-[${scheme.colors[600]}]`;
      case 'hover':
        return `hover:bg-[${scheme.colors[50]}] dark:hover:bg-[${scheme.colors[900]}]/10 hover:border-[${scheme.colors[200]}] dark:hover:border-[${scheme.colors[700]}]`;
      case 'border':
        return `border-[${scheme.colors[200]}] dark:border-[${scheme.colors[700]}]`;
      default:
        return '';
    }
  };

  // Load settings from localStorage on mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('userSettings');
    if (savedSettings) {
      try {
        setSettings(JSON.parse(savedSettings));
      } catch (error) {
        console.error('Failed to parse saved settings:', error);
      }
    }
  }, []);

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
            onKeyPress={(e) => {
              if (e.key === 'Enter' && searchTerm.trim()) {
                router.push(`/search?q=${encodeURIComponent(searchTerm)}`);
              }
            }}
            placeholder="Search knowledge... (Press Enter)"
            className="w-full pl-10 pr-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-forest-500 dark:focus:ring-forest-400 focus:border-forest-500 text-gray-900 dark:text-gray-100 placeholder-gray-500 transition-all"
          />
        </div>
      </div>

      {/* Enhanced Knowledge Categories */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <div className="space-y-1">
          {mainCategories.map((category) => {
            const icon = categoryIcons[category.id] || '📚';
            const hasSubcategories = category.subcategories && category.subcategories.length > 0;
            const isExpanded = expandedCategories.has(category.id);
            
            return (
              <div key={category.id} className="relative">
                {/* Main Category */}
                <div className="flex items-center">
                  <button
                    onClick={() => handleCategoryClick(category.id)}
                    className={`flex-1 flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${getColorClasses('hover')} border border-transparent text-gray-700 dark:text-gray-300 group cursor-pointer`}
                    title={`Click to explore ${category.name}`}
                  >
                    <span className="text-base group-hover:scale-110 transition-transform">{icon}</span>
                    <div className="flex-1 text-left">
                      <div className="text-sm font-medium transition-colors" style={{'--hover-color': currentColorScheme.colors[600]} as React.CSSProperties} onMouseEnter={(e) => e.currentTarget.style.color = currentColorScheme.colors[600]} onMouseLeave={(e) => e.currentTarget.style.color = ''}>{category.name}</div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
                        {category.description}
                      </div>
                    </div>
                  </button>
                  
                  {/* Expand/Collapse Button */}
                  {hasSubcategories && (
                    <button
                      onClick={(e) => toggleCategoryExpansion(category.id, e)}
                      className="p-2 ml-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                      title={isExpanded ? 'Collapse' : 'Expand'}
                    >
                      {isExpanded ? (
                        <Minus size={14} className="text-gray-400" />
                      ) : (
                        <Plus size={14} className="text-gray-400" />
                      )}
                    </button>
                  )}
                </div>

                {/* Expanded Subcategories */}
                {hasSubcategories && isExpanded && (
                  <div className="ml-6 mt-2 space-y-1 border-l-2 border-gray-100 dark:border-gray-700 pl-3">
                    {category.subcategories.map((subcategory: any) => (
                      <div key={subcategory.id} className="space-y-1">
                        <button
                          onClick={() => handleSubcategoryClick(category.id, subcategory.id)}
                          className="w-full flex items-start gap-2 px-2 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-left transition-colors group/sub cursor-pointer"
                          title={`View ${subcategory.name}`}
                        >
                          <div 
                            className="w-3 h-3 rounded-full mt-1 flex-shrink-0"
                            style={{ backgroundColor: subcategory.color }}
                          />
                          <div className="flex-1 min-w-0">
                            <div className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover/sub:text-blue-600 dark:group-hover/sub:text-blue-400 transition-colors">
                              {subcategory.name}
                            </div>
                            <div className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                              {subcategory.description.length > 50 
                                ? `${subcategory.description.substring(0, 50)}...` 
                                : subcategory.description
                              }
                            </div>
                            <div className="flex items-center gap-3 mt-1 text-xs text-gray-400">
                              {subcategory.subcategories && (
                                <span>{subcategory.subcategories.length} subcategories</span>
                              )}
                              {subcategory.nodes && (
                                <span>{subcategory.nodes.length} topics</span>
                              )}
                            </div>
                          </div>
                          <ChevronRight size={12} className="text-gray-400 group-hover/sub:text-blue-600 dark:group-hover/sub:text-blue-400 mt-1 transition-colors" />
                        </button>
                        
                        {/* Show first few nodes for quick access */}
                        {renderSubcategoryNodes(subcategory, category.id)}
                      </div>
                    ))}
                  </div>
                )}

                {/* Improved Hover Menu for Desktop */}
                {hasSubcategories && !isExpanded && (
                  <div 
                    className="absolute left-full top-0 ml-2 w-72 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 pointer-events-none group-hover:pointer-events-auto z-50 hidden lg:block"
                    onMouseEnter={() => setHoveredCategory(category.id)}
                    onMouseLeave={() => setHoveredCategory(null)}
                  >
                    <div className="p-4">
                      <div className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3 flex items-center gap-2">
                        <span>{icon}</span>
                        {category.name}
                      </div>
                      <div className="space-y-2 max-h-96 overflow-y-auto">
                        {category.subcategories.map((subcategory: any) => (
                          <div key={subcategory.id} className="group/hover">
                            <div
                              onClick={(e) => {
                                e.stopPropagation();
                                handleSubcategoryClick(category.id, subcategory.id);
                              }}
                              className="w-full flex items-start gap-3 p-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-left transition-colors cursor-pointer"
                            >
                              <div 
                                className="w-4 h-4 rounded-full mt-0.5 flex-shrink-0"
                                style={{ backgroundColor: subcategory.color }}
                              />
                              <div className="flex-1 min-w-0">
                                <div className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover/hover:text-blue-600 dark:group-hover/hover:text-blue-400 transition-colors">
                                  {subcategory.name}
                                </div>
                                <div className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed mt-1">
                                  {subcategory.description}
                                </div>
                                {subcategory.nodes && subcategory.nodes.length > 0 && (
                                  <div className="mt-2 space-y-1">
                                    {subcategory.nodes.slice(0, 2).map((node: any) => (
                                      <div
                                        key={node.id}
                                        onClick={(e) => {
                                          e.stopPropagation();
                                          handleNodeClick(node.id);
                                        }}
                                        className="block w-full text-left text-xs text-gray-600 dark:text-gray-400 hover:text-forest-600 dark:hover:text-forest-400 px-2 py-1 rounded hover:bg-gray-100 dark:hover:bg-gray-600 cursor-pointer"
                                      >
                                        • {node.name}
                                      </div>
                                    ))}
                                    {subcategory.nodes.length > 2 && (
                                      <div className="text-xs text-gray-500 px-2">
                                        +{subcategory.nodes.length - 2} more topics
                                      </div>
                                    )}
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
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


      {/* Social Hub - Integrated */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3 flex items-center gap-2">
          <Users className="w-4 h-4" />
          Community & Study
        </h3>
        
        <div className="space-y-2">
          <button
            onClick={() => setShowSocialPanel(showSocialPanel === 'bookmarks' ? null : 'bookmarks')}
            className={`w-full px-3 py-2 rounded-lg transition-all flex items-center justify-between gap-2 text-sm cursor-pointer ${
              showSocialPanel === 'bookmarks'
                ? 'bg-forest-100 dark:bg-forest-900/30 text-forest-700 dark:text-forest-300 border border-forest-200 dark:border-forest-700'
                : 'bg-gray-50 dark:bg-gray-700 hover:bg-forest-50 dark:hover:bg-forest-900/10 hover:border-forest-200 dark:hover:border-forest-700 text-gray-700 dark:text-gray-300 border border-transparent'
            }`}
            title="Toggle bookmarks panel"
          >
            <span className="flex items-center gap-2">
              <Bookmark className="w-4 h-4" />
              Bookmarks
            </span>
            <ChevronRight className={`w-4 h-4 transition-transform ${showSocialPanel === 'bookmarks' ? 'rotate-90' : ''}`} />
          </button>
          
          <button
            onClick={() => setShowSocialPanel(showSocialPanel === 'friends' ? null : 'friends')}
            className={`w-full px-3 py-2 rounded-lg transition-all flex items-center justify-between gap-2 text-sm cursor-pointer ${
              showSocialPanel === 'friends'
                ? 'bg-forest-100 dark:bg-forest-900/30 text-forest-700 dark:text-forest-300 border border-forest-200 dark:border-forest-700'
                : 'bg-gray-50 dark:bg-gray-700 hover:bg-forest-50 dark:hover:bg-forest-900/10 hover:border-forest-200 dark:hover:border-forest-700 text-gray-700 dark:text-gray-300 border border-transparent'
            }`}
            title="Toggle friends panel"
          >
            <span className="flex items-center gap-2">
              <UserPlus className="w-4 h-4" />
              Friends
            </span>
            <ChevronRight className={`w-4 h-4 transition-transform ${showSocialPanel === 'friends' ? 'rotate-90' : ''}`} />
          </button>
          
          <button
            onClick={() => setShowSocialPanel(showSocialPanel === 'groups' ? null : 'groups')}
            className={`w-full px-3 py-2 rounded-lg transition-all flex items-center justify-between gap-2 text-sm cursor-pointer ${
              showSocialPanel === 'groups'
                ? 'bg-forest-100 dark:bg-forest-900/30 text-forest-700 dark:text-forest-300 border border-forest-200 dark:border-forest-700'
                : 'bg-gray-50 dark:bg-gray-700 hover:bg-forest-50 dark:hover:bg-forest-900/10 hover:border-forest-200 dark:hover:border-forest-700 text-gray-700 dark:text-gray-300 border border-transparent'
            }`}
            title="Toggle study groups panel"
          >
            <span className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              Study Groups
            </span>
            <ChevronRight className={`w-4 h-4 transition-transform ${showSocialPanel === 'groups' ? 'rotate-90' : ''}`} />
          </button>
        </div>
        
        {/* Expandable Social Panels */}
        {showSocialPanel === 'bookmarks' && (
          <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
            <BookmarksPanel compact={true} />
          </div>
        )}
        
        {showSocialPanel === 'friends' && (
          <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
            <FriendsPanel compact={true} />
          </div>
        )}
        
        {showSocialPanel === 'groups' && (
          <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
            <StudyGroupsPanel compact={true} />
          </div>
        )}
      </div>

      {/* Enhanced Progress Card */}
      {user && (
        <div className="bg-gradient-to-br from-forest-600 to-sky-600 rounded-xl shadow-lg p-4 text-white">
          <div 
            onClick={() => router.push('/profile')}
            className="cursor-pointer hover:bg-white/10 rounded-lg p-2 -m-2 transition-all"
            title="View your full progress"
          >
            <h3 className="text-sm font-semibold mb-3 flex items-center justify-between">
              <span className="flex items-center gap-2">
                <Trophy className="w-4 h-4" />
                Your Progress
              </span>
              <ChevronRight className="w-4 h-4 opacity-70" />
            </h3>
          </div>

          {progressLoading ? (
            <div className="space-y-3 animate-pulse">
              <div className="grid grid-cols-2 gap-3">
                {[1, 2, 3, 4].map(i => (
                  <div key={i} className="bg-white/20 rounded-lg h-12"></div>
                ))}
              </div>
              <div className="bg-white/20 rounded h-2"></div>
            </div>
          ) : (
            <>
              {/* Quick Stats Grid */}
              <div className="grid grid-cols-2 gap-2 mb-4">
                <div className="bg-white/10 rounded-lg p-2 text-center">
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <Brain className="w-3 h-3" />
                    <span className="text-xs opacity-90">Level</span>
                  </div>
                  <div className="font-bold text-sm">{stats.neuralLevel}</div>
                </div>
                <div className="bg-white/10 rounded-lg p-2 text-center">
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <Target className="w-3 h-3" />
                    <span className="text-xs opacity-90">Nodes</span>
                  </div>
                  <div className="font-bold text-sm">{stats.totalNodes}</div>
                </div>
                <div className="bg-white/10 rounded-lg p-2 text-center">
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <Zap className="w-3 h-3" />
                    <span className="text-xs opacity-90">Points</span>
                  </div>
                  <div className="font-bold text-sm">{stats.totalPoints}</div>
                </div>
                <div className="bg-white/10 rounded-lg p-2 text-center">
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <TrendingUp className="w-3 h-3" />
                    <span className="text-xs opacity-90">Avg</span>
                  </div>
                  <div className="font-bold text-sm">{Math.round(stats.averageScore)}%</div>
                </div>
              </div>

              {/* Level Progress Bar */}
              <div>
                <div className="flex justify-between text-xs opacity-90 mb-1">
                  <span>Level {stats.neuralLevel}</span>
                  <span>Level {stats.neuralLevel + 1}</span>
                </div>
                <div className="w-full bg-white/20 rounded-full h-2">
                  <div 
                    className="bg-white h-2 rounded-full transition-all"
                    style={{ width: `${(stats.totalPoints % 200) / 2}%` }}
                  />
                </div>
                <div className="text-center text-xs opacity-75 mt-1">
                  {200 - (stats.totalPoints % 200)} points to next level
                </div>
              </div>
            </>
          )}
        </div>
      )}

    </div>
  );
}