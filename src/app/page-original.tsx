'use client';

import React, { useState, useEffect, useMemo, CSSProperties } from 'react';
import { Trees, Trophy, Star, Lock, CheckCircle, X, ChevronRight, Grid, Map, User, Plus, Minus, MessageSquare, Users, Activity, Settings } from 'lucide-react';
import { useRouter } from 'next/navigation';

// Import types
import { Node, AnswerFeedback } from '../types';

// Import data - lazy load heavy modules
import { domainIcons } from '../data/domainIcons';
// Lazy load heavy data to improve initial page load
const loadHierarchicalNodes = () => import('../data/hierarchicalKnowledgeGraph').then(m => ({
  getAllHierarchicalNodes: m.getAllHierarchicalNodes,
  getCategoryLabels: m.getCategoryLabels
}));

// Import hooks
import { useUserStats } from '../hooks/useUserStats';
import { useQuizQuestions } from '../hooks/useQuizQuestions';
import { useAuth } from '../contexts/AuthContext';

// Import utilities - these are lightweight, OK to import directly
import { 
  getNodeState, 
  createHierarchicalConnections, 
  filterHierarchicalNodes,
  toggleNodeExpansion,
  getVisibleNodes,
  calculateHierarchicalProgress
} from '../utils/hierarchicalNodeUtils';
import { 
  filterNodesByAge, 
  sortNodesByAgeRecommendation,
  getPersonalizedRecommendations 
} from '../utils/contentRecommendation';

// Import components
// Dynamically import heavy components
const ModernHeader = dynamic(() => import('../components/ModernHeader'), {
  loading: () => <div className="h-16 bg-white dark:bg-gray-800" />
});
const ModernSidebar = dynamic(() => import('../components/ModernSidebar'), {
  loading: () => <div className="w-64 bg-white dark:bg-gray-800" />
});
const Layout = dynamic(() => import('../components/Layout'), {
  loading: () => <div className="min-h-screen" />
});
const AuthModal = dynamic(() => import('../components/AuthModal').then(m => ({ default: m.AuthModal })), {
  loading: () => null
});
const SettingsModal = dynamic(() => import('../components/SettingsModal').then(m => ({ default: m.SettingsModal })), {
  loading: () => null
});
// Lazy load heavy components
import dynamic from 'next/dynamic';
const LearningModal = dynamic(() => import('../components/LearningModal'), {
  loading: () => <div className="fixed inset-0 bg-black/50 flex items-center justify-center"><div className="text-white">Loading...</div></div>
});
const Homepage = dynamic(() => import('../components/Homepage').then(m => ({ default: m.Homepage })), {
  ssr: false,
  loading: () => <div className="min-h-screen flex items-center justify-center">Loading...</div>
});
import LearningInsights from '../components/LearningInsights';
import { ChatbotContainer } from '../components/ChatbotContainer';
// Lazy load analytics service
const loadAnalyticsService = () => import('../services/analyticsService').then(m => m.AnalyticsService);
import { OnboardingTrigger } from '../components/onboarding/OnboardingTrigger';
import PerformanceMonitor from '../components/PerformanceMonitor';
import { NotificationPermission } from '../components/NotificationPermission';
// Lazy load push notification service
const loadPushNotificationService = () => import('../services/pushNotificationService').then(m => m.pushNotificationService);
// import Hierarchical2DKnowledgeMap from '../components/Hierarchical2DKnowledgeMap'; // Removed - no longer using knowledge map
const NodeCommentary = dynamic(() => import('../components/comments/NodeCommentary'), {
  loading: () => <div className="p-4">Loading comments...</div>
});
const BookmarkButton = dynamic(() => import('../components/BookmarkButton'), {
  loading: () => null
});
import FriendsPanel from '../components/social/FriendsPanel';
import StudyGroupsPanel from '../components/social/StudyGroupsPanel';
import ActivityFeed from '../components/social/ActivityFeed';

const App = () => {
  // All hooks must be declared at the top level before any conditional returns
  // State management
  const [componentsLoaded, setComponentsLoaded] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [activeTab, setActiveTab] = useState('graph');
  const [socialView, setSocialView] = useState<'feed' | 'friends' | 'groups'>('feed');
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set());
  const [nodesLoaded, setNodesLoaded] = useState(false);
  const [nodesFunctions, setNodesFunctions] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [currentView, setCurrentView] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilters, setActiveFilters] = useState<string[]>([]);
  const [showQuiz, setShowQuiz] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [showAchievement, setShowAchievement] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [answerFeedback, setAnswerFeedback] = useState<AnswerFeedback | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [showCommentary, setShowCommentary] = useState(false);
  
  // Authentication state from context
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();
  
  // User stats hook
  const { userStats, completeNode } = useUserStats();
  
  // Fetch quiz questions from database
  const { questions: currentQuizQuestions, loading: questionsLoading } = useQuizQuestions(
    selectedNode?.id || null
  );
  
  useEffect(() => {
    // Mark components as loaded after a brief delay
    const timer = setTimeout(() => setComponentsLoaded(true), 10);
    return () => clearTimeout(timer);
  }, []);
  
  // Responsive detection
  useEffect(() => {
    setIsMobile(window.innerWidth < 768);
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Initialize analytics and push notifications when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      // Delay analytics initialization to not block initial render
      const timer = setTimeout(async () => {
        const [Analytics, pushService] = await Promise.all([
          loadAnalyticsService(),
          loadPushNotificationService()
        ]);
        Analytics.initialize();
        pushService.initialize();
      }, 2000);
      
      return () => {
        clearTimeout(timer);
        // Cleanup analytics if loaded
        loadAnalyticsService().then(Analytics => Analytics.cleanup());
      };
    }
  }, [isAuthenticated]);
  
  // Lazy load nodes after initial render
  useEffect(() => {
    if (isAuthenticated && !nodesLoaded) {
      // Load node functions first
      loadHierarchicalNodes().then(funcs => {
        setNodesFunctions(funcs);
        // Then mark nodes as loaded after a short delay
        setTimeout(() => {
          setNodesLoaded(true);
        }, 100);
      });
    }
  }, [isAuthenticated, nodesLoaded]);
  const allNodes = useMemo(() => {
    if (!isAuthenticated || !nodesLoaded || !nodesFunctions) return [];
    return nodesFunctions.getAllHierarchicalNodes(expandedNodes);
  }, [expandedNodes, isAuthenticated, nodesLoaded, nodesFunctions]);
  
  // Apply age-based filtering if user has birthYear
  const ageFilteredNodes = useMemo(() => {
    if (!nodesLoaded || allNodes.length === 0) return [];
    if (!user?.birthYear) return allNodes;
    return sortNodesByAgeRecommendation(
      filterNodesByAge(allNodes, user.birthYear),
      user.birthYear
    );
  }, [allNodes, user?.birthYear, nodesLoaded]);
  
  // Get visible nodes (respecting expanded/collapsed state)
  const visibleNodes = useMemo(() => {
    if (!nodesLoaded || ageFilteredNodes.length === 0) return [];
    return getVisibleNodes(ageFilteredNodes, expandedNodes);
  }, [ageFilteredNodes, expandedNodes, nodesLoaded]);
  
  // Calculate container height based on nodes - removed as we're not using the map
  const graphHeight = 700; // Fixed height, no longer computing from nodes
  
  // Create connections based on prerequisites and hierarchy - removed as we're not using the map
  const connections: any[] = []; // Empty array, no longer computing connections


  // Filter nodes based on view and search - with null check
  const filteredNodes = useMemo(() => {
    if (!nodesLoaded || visibleNodes.length === 0) return [];
    return filterHierarchicalNodes(visibleNodes, activeFilters, searchTerm, currentView, expandedNodes);
  }, [visibleNodes, activeFilters, searchTerm, currentView, expandedNodes, nodesLoaded]);

  // Handle node expansion/collapse
  const handleNodeExpansion = (nodeId: string) => {
    setExpandedNodes(prev => toggleNodeExpansion(nodeId, prev));
  };

  // Handle quiz answer
  const handleAnswer = (answerIndex: number) => {
    if (!selectedNode || !currentQuizQuestions.length) return;
    
    setSelectedAnswer(answerIndex);
    const question = currentQuizQuestions[currentQuestion] || currentQuizQuestions[0];
    const isCorrect = answerIndex === question.correct;
    
    setAnswerFeedback({
      isCorrect,
      explanation: question.explanation
    });
    
    setTimeout(() => {
      handleCompleteNode();
    }, 2000);
  };

  // Complete a node
  const handleCompleteNode = async () => {
    if (!selectedNode) return;
    
    const wasNewlyCompleted = await completeNode(selectedNode.id, selectedNode.points);
    
    if (wasNewlyCompleted) {
      setShowAchievement(true);
      setTimeout(() => setShowAchievement(false), 3000);
    }
    
    setShowQuiz(false);
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setAnswerFeedback(null);
  };

  // Toggle filter
  const toggleFilter = (domain: string) => {
    setActiveFilters(prev => 
      prev.includes(domain) 
        ? prev.filter(f => f !== domain)
        : [...prev, domain]
    );
  };

  // Loading state check - must be after all hooks
  if (!componentsLoaded) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-forest-600 mx-auto mb-4"></div>
          <div className="text-gray-600">Loading NeuroQuest...</div>
        </div>
      </div>
    );
  }
  
  // Styles
  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #059669 0%, #0ea5e9 100%)',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      paddingBottom: isMobile ? '70px' : '0'
    } as CSSProperties,
    mainGrid: {
      display: isMobile ? 'block' : 'grid',
      gridTemplateColumns: isMobile ? '1fr' : '280px 1fr 300px',
      gap: '20px',
      maxWidth: '1400px',
      margin: '0 auto',
      padding: '0 20px'
    } as CSSProperties,
    panel: {
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderRadius: '15px',
      padding: '20px',
      marginBottom: isMobile ? '15px' : '0',
      boxShadow: '0 5px 20px rgba(0,0,0,0.1)'
    } as CSSProperties,
    graphContainer: {
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderRadius: '20px',
      padding: '20px',
      height: isMobile ? '500px' : '700px',
      minHeight: '700px',
      position: 'relative' as const,
      overflow: 'auto',
      boxShadow: '0 5px 20px rgba(0,0,0,0.1)'
    } as CSSProperties,
    node: {
      position: 'absolute' as const,
      width: '100px',
      height: '100px',
      borderRadius: '15px',
      display: 'flex',
      flexDirection: 'column' as const,
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      fontSize: '11px',
      fontWeight: 'bold',
      textAlign: 'center' as const,
      padding: '8px',
      border: '2px solid transparent',
      boxSizing: 'border-box' as const
    } as CSSProperties,
    nodeCompleted: {
      background: 'linear-gradient(135deg, #00c851, #00ff00)',
      color: 'white',
      boxShadow: '0 5px 15px rgba(0, 200, 81, 0.4)'
    } as CSSProperties,
    nodeAvailable: {
      background: 'linear-gradient(135deg, #2196F3, #00bcd4)',
      color: 'white',
      boxShadow: '0 5px 15px rgba(33, 150, 243, 0.4)',
      animation: 'pulse 2s infinite'
    } as CSSProperties,
    nodeLocked: {
      background: '#e0e0e0',
      color: '#5a5a5a',
      opacity: 0.6
    } as CSSProperties,
    subnode: {
      width: '85px',
      height: '85px',
      fontSize: '10px',
      border: '2px solid rgba(103, 126, 234, 0.3)',
      boxShadow: '0 2px 8px rgba(103, 126, 234, 0.15)',
      background: 'rgba(255, 255, 255, 0.98)'
    } as CSSProperties,
    parentNode: {
      background: 'linear-gradient(135deg, #10b981, #34d399)',
      color: 'white',
      boxShadow: '0 5px 15px rgba(16, 185, 129, 0.4)',
      border: '2px solid rgba(52, 211, 153, 0.5)'
    } as CSSProperties
  };

  // Mobile navigation
  const MobileNav = () => (
    <div className="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex justify-around py-2 z-[1000]">
      <button 
        onClick={() => setActiveTab('graph')} 
        className={`flex flex-col items-center justify-center p-2 ${activeTab === 'graph' ? 'text-forest-600' : 'text-gray-500 dark:text-gray-400'}`}
      >
        <Grid size={24} />
        <div className="text-[10px] mt-1">Map</div>
      </button>
      <button 
        onClick={() => setActiveTab('paths')} 
        className={`flex flex-col items-center justify-center p-2 ${activeTab === 'paths' ? 'text-forest-600' : 'text-gray-500 dark:text-gray-400'}`}
      >
        <Map size={24} />
        <div className="text-[10px] mt-1">Paths</div>
      </button>
      <button 
        onClick={() => setActiveTab('profile')} 
        className={`flex flex-col items-center justify-center p-2 ${activeTab === 'profile' ? 'text-forest-600' : 'text-gray-500 dark:text-gray-400'}`}
      >
        <User size={24} />
        <div className="text-[10px] mt-1">Profile</div>
      </button>
      <button 
        onClick={() => setActiveTab('social')} 
        className={`flex flex-col items-center justify-center p-2 ${activeTab === 'social' ? 'text-forest-600' : 'text-gray-500 dark:text-gray-400'}`}
      >
        <Users size={24} />
        <div className="text-[10px] mt-1">Social</div>
      </button>
    </div>
  );

  // Show homepage if not authenticated
  if (!isAuthenticated) {
    return (
      <>
        <Homepage 
          onGetStarted={() => {
            setShowAuthModal(true);
          }}
        />
        <AuthModal 
          isOpen={showAuthModal} 
          onClose={() => setShowAuthModal(false)}
          onSuccess={() => {
            // Modal will be closed by onClose, just handle post-auth logic here if needed
            console.log('Authentication successful');
          }}
        />
      </>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Notification Permission Banner */}
      {isAuthenticated && <NotificationPermission />}
      
      {/* Header */}
      <ModernHeader 
        userStats={userStats} 
        isMobile={isMobile} 
        calculateProgress={() => calculateHierarchicalProgress(allNodes, userStats.conqueredNodes, expandedNodes)}
        onAuthClick={() => setShowAuthModal(true)}
        onSettingsClick={() => setShowSettingsModal(true)}
      />

      <Layout
        isMobile={isMobile}
        sidebar={
          <ModernSidebar
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
            currentView={currentView}
            setCurrentView={setCurrentView}
            activeFilters={activeFilters}
            toggleFilter={toggleFilter}
          />
        }
        rightPanel={
          <div className="space-y-4">
            {/* Suggested Next - Moved to top for better visibility */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
              <h3 className="text-base font-bold text-gray-900 dark:text-gray-100 mb-4">Suggested Next</h3>
              <div className="space-y-2">
                {filteredNodes
                  .filter(n => getNodeState(n.id, userStats.conqueredNodes, allNodes) === 'available')
                  .slice(0, 3)
                  .map(node => {
                    const Icon = domainIcons[node.domain] || Trees;
                    return (
                      <div 
                        key={node.id}
                        className="p-3 bg-gray-50 dark:bg-gray-900 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors flex items-center gap-3"
                        onClick={() => setSelectedNode(node)}
                      >
                        <Icon size={20} color="#059669" />
                        <div className="flex-1">
                          <div className="text-sm font-bold text-gray-900 dark:text-gray-100">{node.name}</div>
                          <div className="text-xs text-gray-600 dark:text-gray-400 font-medium">+{node.points} points</div>
                        </div>
                        <BookmarkButton node={node} size="sm" />
                      </div>
                    );
                  })}
              </div>
            </div>


            {/* Learning Insights */}
            <LearningInsights />

            {/* Social Activity Feed (Desktop) */}
            {!isMobile && (
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-base font-bold text-gray-900 dark:text-gray-100">Community Activity</h3>
                  <Activity className="w-4 h-4 text-gray-400" />
                </div>
                <ActivityFeed compact={true} />
              </div>
            )}

            {/* Recent Achievements */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
              <h3 className="text-base font-bold text-gray-900 dark:text-gray-100 mb-4">Recent Achievements</h3>
              <div className="space-y-2">
                <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
                  <Trophy size={20} className="text-yellow-500" />
                  <div>
                    <div className="text-sm font-bold text-gray-900 dark:text-gray-100">First Steps</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Complete 5 nodes</div>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
                  <Star size={20} className="text-forest-600" />
                  <div>
                    <div className="text-sm font-bold text-gray-900 dark:text-gray-100">Quick Learner</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Complete 3 nodes in one day</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        }
      >
        {/* Tab Content based on activeTab (mobile) or always show graph (desktop) */}
        {(isMobile && activeTab === 'social') ? (
          <div className="space-y-4">
            {/* Social Tab Navigation */}
            <div className="flex gap-2 mb-4">
              <button
                onClick={() => setSocialView('feed')}
                className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  socialView === 'feed'
                    ? 'bg-forest-600 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`}
              >
                <Activity className="inline w-4 h-4 mr-2" />
                Activity
              </button>
              <button
                onClick={() => setSocialView('friends')}
                className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  socialView === 'friends'
                    ? 'bg-forest-600 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`}
              >
                <User className="inline w-4 h-4 mr-2" />
                Friends
              </button>
              <button
                onClick={() => setSocialView('groups')}
                className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  socialView === 'groups'
                    ? 'bg-forest-600 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`}
              >
                <Users className="inline w-4 h-4 mr-2" />
                Groups
              </button>
            </div>

            {/* Social Content */}
            {socialView === 'feed' && <ActivityFeed />}
            {socialView === 'friends' && <FriendsPanel />}
            {socialView === 'groups' && <StudyGroupsPanel />}
          </div>
        ) : (isMobile && activeTab === 'profile') ? (
          <div className="p-4">Profile content moved to Settings</div>
        ) : (isMobile && activeTab === 'paths') ? (
          <div className="p-4">
            <h2 className="text-2xl font-bold mb-4">Learning Paths</h2>
            <p className="text-gray-600 dark:text-gray-400">Coming soon...</p>
          </div>
        ) : (
          /* Default: Main Content Area */
          <div className="space-y-6">
            {/* Welcome Banner */}
            <div className="bg-gradient-to-r from-forest-600 to-blue-600 rounded-2xl p-6 text-white">
              <h2 className="text-2xl font-bold mb-2">Welcome back, {user?.username || 'Learner'}!</h2>
              <p className="text-forest-100">Continue your learning journey and unlock new knowledge.</p>
              <div className="mt-4 flex items-center gap-6 text-sm">
                <div>
                  <span className="text-forest-200">Streak:</span>
                  <span className="ml-2 font-bold">{userStats.synapticStreak} days</span>
                </div>
                <div>
                  <span className="text-forest-200">Level:</span>
                  <span className="ml-2 font-bold">{userStats.neuralLevel}</span>
                </div>
                <div>
                  <span className="text-forest-200">Points:</span>
                  <span className="ml-2 font-bold">{userStats.pathfinderPoints}</span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button
                onClick={() => {
                  const availableNodes = filteredNodes.filter(n => 
                    getNodeState(n.id, userStats.conqueredNodes, allNodes) === 'available'
                  );
                  if (availableNodes.length > 0) {
                    setSelectedNode(availableNodes[0]);
                    setShowQuiz(true);
                  }
                }}
                className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-xl transition-all border border-gray-100 dark:border-gray-700">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-forest-100 dark:bg-forest-900/30 rounded-full flex items-center justify-center">
                    <Trees className="w-6 h-6 text-forest-600 dark:text-forest-400" />
                  </div>
                  <div className="text-left">
                    <h3 className="font-semibold text-gray-900 dark:text-gray-100">Continue Learning</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Pick up where you left off</p>
                  </div>
                </div>
              </button>

              <button
                onClick={() => router.push('/category/science')}
                className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-xl transition-all border border-gray-100 dark:border-gray-700">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                    <Map className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="text-left">
                    <h3 className="font-semibold text-gray-900 dark:text-gray-100">Explore Topics</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Browse all categories</p>
                  </div>
                </div>
              </button>

            </div>

            {/* Recent Progress */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Recent Progress</h3>
              <div className="space-y-3">
                {nodesLoaded ? (
                  userStats.conqueredNodes.slice(-5).reverse().map(nodeId => {
                    const node = allNodes.find(n => n.id === nodeId);
                    if (!node) return null;
                    const Icon = domainIcons[node.domain] || Trees;
                    return (
                      <div key={nodeId} className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
                        <Icon className="w-5 h-5 text-forest-600 dark:text-forest-400" />
                        <div className="flex-1">
                          <div className="font-medium text-gray-900 dark:text-gray-100">{node.name}</div>
                          <div className="text-sm text-gray-600 dark:text-gray-400">+{node.points} points earned</div>
                        </div>
                        <CheckCircle className="w-5 h-5 text-green-500" />
                      </div>
                    );
                  })
                ) : (
                  <div className="animate-pulse space-y-3">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="h-16 bg-gray-100 dark:bg-gray-700 rounded-lg" />
                    ))}
                  </div>
                )}
                {nodesLoaded && userStats.conqueredNodes.length === 0 && (
                  <p className="text-gray-500 dark:text-gray-400 text-center py-4">No completed topics yet. Start learning!</p>
                )}
              </div>
            </div>

            {/* Available Topics */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Available Topics</h3>
              {nodesLoaded ? (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {filteredNodes
                      .filter(n => getNodeState(n.id, userStats.conqueredNodes, allNodes) === 'available')
                      .slice(0, 6)
                      .map(node => {
                        const Icon = domainIcons[node.domain] || Trees;
                        return (
                          <div
                            key={node.id}
                            className="relative p-4 bg-gray-50 dark:bg-gray-900 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                            <button
                              onClick={() => {
                                setSelectedNode(node);
                                setShowQuiz(true);
                              }}
                              className="w-full text-left">
                              <div className="flex items-start gap-3">
                                <Icon className="w-5 h-5 text-forest-600 dark:text-forest-400 mt-1" />
                                <div className="flex-1">
                                  <div className="font-medium text-gray-900 dark:text-gray-100">{node.name}</div>
                                  <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                                    {'⭐'.repeat(node.difficulty)} • +{node.points} pts
                                  </div>
                                </div>
                              </div>
                            </button>
                            <div className="absolute top-2 right-2">
                              <BookmarkButton node={node} size="sm" />
                            </div>
                          </div>
                        );
                      })}
                  </div>
                  {filteredNodes.filter(n => getNodeState(n.id, userStats.conqueredNodes, allNodes) === 'available').length > 6 && (
                    <button 
                      onClick={() => router.push('/category/all')}
                      className="mt-4 w-full py-2 text-center text-forest-600 dark:text-forest-400 hover:text-forest-700 dark:hover:text-forest-300 font-medium">
                      View all available topics →
                    </button>
                  )}
                </>
              ) : (
                <div className="animate-pulse grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {[1, 2, 3, 4, 5, 6].map(i => (
                    <div key={i} className="h-24 bg-gray-100 dark:bg-gray-700 rounded-lg" />
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Old 2D map code - keeping for reference */}
        {false && (
          <div style={{
            ...styles.graphContainer,
            minWidth: isMobile ? '100%' : '1200px',
            height: `${graphHeight}px`
          }}>
          {/* Category Labels */}
          {Object.entries(getCategoryLabels(allNodes)).map(([category, label]) => (
            <div
              key={category}
              style={{
                position: 'absolute',
                left: '20px',
                top: label.y,
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#8e44ad',
                textTransform: 'uppercase',
                letterSpacing: '2px',
                opacity: 0.7,
                background: 'rgba(255, 255, 255, 0.9)',
                padding: '4px 12px',
                borderRadius: '20px',
                boxShadow: '0 2px 8px rgba(142, 68, 173, 0.15)',
                zIndex: 5
              }}
            >
              {label.name.replace('_', ' ')}
            </div>
          ))}
          
          <svg style={{ position: 'absolute', width: '100%', height: '100%', top: 0, left: 0 }}>
            {connections.map((conn, idx) => {
              const fromNode = filteredNodes.find(n => n.id === conn.from);
              const toNode = filteredNodes.find(n => n.id === conn.to);
              
              if (!fromNode || !toNode || !fromNode.x || !fromNode.y || !toNode.x || !toNode.y) return null;
              
              const fromState = getNodeState(fromNode.id, userStats.conqueredNodes, allNodes);
              const toState = getNodeState(toNode.id, userStats.conqueredNodes, allNodes);
              const isActive = fromState === 'completed' && toState !== 'locked';
              
              // Calculate center points based on node sizes
              const fromNodeSize = fromNode.level === 1 ? 42.5 : 50;
              const toNodeSize = toNode.level === 1 ? 42.5 : 50;
              
              return (
                <line
                  key={idx}
                  x1={fromNode.x + fromNodeSize}
                  y1={fromNode.y + fromNodeSize}
                  x2={toNode.x + toNodeSize}
                  y2={toNode.y + toNodeSize}
                  stroke={isActive ? '#059669' : '#ddd'}
                  strokeWidth={isActive ? '2' : '1'}
                  strokeDasharray={!isActive ? '5,5' : '0'}
                  opacity={isActive ? 0.6 : 0.3}
                />
              );
            })}
          </svg>

          {filteredNodes.map(node => {
            const state = getNodeState(node.id, userStats.conqueredNodes, allNodes);
            const Icon = domainIcons[node.domain] || Trees;
            const isExpanded = expandedNodes.has(node.id);
            
            return (
              <div
                key={node.id}
                style={{
                  ...styles.node,
                  ...(node.isParent ? styles.parentNode :
                      state === 'completed' ? styles.nodeCompleted :
                      state === 'available' ? styles.nodeAvailable :
                      styles.nodeLocked),
                  ...(node.level === 1 ? styles.subnode : {}),
                  left: node.x,
                  top: node.y,
                  transform: selectedNode?.id === node.id ? 'scale(1.1)' : 'scale(1)',
                  opacity: node.level === 1 ? 0.9 : 1,
                  zIndex: node.isParent ? 2 : 1
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  
                  if (node.isParent) {
                    // Handle expand/collapse for parent nodes
                    handleNodeExpansion(node.id);
                    // Also allow selecting parent nodes to see their details
                    setSelectedNode(node);
                  } else if (state !== 'locked') {
                    // Handle regular node selection
                    setSelectedNode(node);
                    if (state === 'available') {
                      // Questions will be fetched via hook
                      setShowQuiz(true);
                    }
                  }
                }}
                onMouseEnter={(e) => {
                  if (state !== 'locked' || node.isParent) {
                    e.currentTarget.style.transform = 'scale(1.08)';
                    e.currentTarget.style.zIndex = '10';
                  }
                }}
                onMouseLeave={(e) => {
                  if (selectedNode?.id !== node.id) {
                    e.currentTarget.style.transform = 'scale(1)';
                    e.currentTarget.style.zIndex = node.isParent ? '2' : '1';
                  }
                }}
              >
                <Icon size={node.level === 1 ? 18 : node.isParent ? 26 : 24} />
                <div style={{ 
                  marginTop: '5px', 
                  fontSize: node.level === 1 ? '9px' : node.isParent ? '11px' : '10px', 
                  lineHeight: '1.2',
                  maxWidth: '90%',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical' as const
                }}>
                  {node.name}
                </div>
                {!node.isParent && (
                  <div style={{ fontSize: node.level === 1 ? '8px' : '9px', opacity: 0.8, marginTop: '2px' }}>
                    +{node.points}
                  </div>
                )}
                
                {/* Expand/Collapse indicator for parent nodes */}
                {node.isParent && (
                  <div style={{ 
                    position: 'absolute', 
                    top: '3px', 
                    right: '3px',
                    background: 'rgba(255, 255, 255, 0.95)',
                    borderRadius: '50%',
                    padding: '4px',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                    border: '1px solid rgba(0,0,0,0.1)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    {isExpanded ? <Minus size={12} color="#8e44ad" /> : <Plus size={12} color="#8e44ad" />}
                  </div>
                )}
                
                {/* Show subnode count for parent nodes */}
                {node.isParent && !isExpanded && node.subnodes && (
                  <div style={{
                    position: 'absolute',
                    bottom: '5px',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    background: 'rgba(142, 68, 173, 0.9)',
                    color: 'white',
                    borderRadius: '8px',
                    padding: '1px 5px',
                    fontSize: '8px',
                    fontWeight: 'bold',
                    whiteSpace: 'nowrap'
                  }}>
                    {node.subnodes.length} nodes
                  </div>
                )}
                
                {/* Status indicators */}
                {!node.isParent && state === 'locked' && (
                  <Lock size={16} style={{ position: 'absolute', top: '5px', right: '5px' }} />
                )}
                {!node.isParent && state === 'completed' && (
                  <CheckCircle size={16} style={{ position: 'absolute', top: '5px', right: '5px' }} />
                )}
              </div>
            );
          })}

          {/* Node Details */}
          {selectedNode && !showQuiz && (
            <div style={{
              position: 'absolute',
              bottom: '20px',
              left: '20px',
              right: '20px',
              background: 'white',
              borderRadius: '15px',
              padding: '20px',
              boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
              zIndex: 10
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div>
                  <h3 style={{ margin: '0 0 10px 0', color: '#2a2a2a', fontWeight: 'bold' }}>{selectedNode.name}</h3>
                  <div style={{ display: 'flex', gap: '10px', fontSize: '12px', color: '#3a3a3a' }}>
                    <span style={{ color: '#3a3a3a', fontWeight: '500' }}>Difficulty: {'⭐'.repeat(selectedNode.difficulty)}</span>
                    <span style={{ color: '#3a3a3a', fontWeight: '500' }}>+{selectedNode.points} points</span>
                  </div>
                  {selectedNode.prereqs && selectedNode.prereqs.length > 0 && (
                    <div style={{ marginTop: '10px', fontSize: '12px', color: '#5a5a5a', fontWeight: '500' }}>
                      Prerequisites: {selectedNode.prereqs.join(', ')}
                    </div>
                  )}
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button
                    onClick={() => setShowCommentary(true)}
                    style={{ 
                      background: 'linear-gradient(135deg, #8b5cf6, #a78bfa)',
                      border: 'none',
                      cursor: 'pointer',
                      color: 'white',
                      padding: '8px 12px',
                      borderRadius: '8px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px',
                      fontSize: '12px',
                      fontWeight: 'bold'
                    }}
                  >
                    <MessageSquare size={16} />
                    Commentary
                  </button>
                  <button
                    onClick={() => setSelectedNode(null)}
                    style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                  >
                    <X size={20} />
                  </button>
                </div>
              </div>
              {selectedNode.isParent ? (
                <div style={{
                  marginTop: '15px',
                  padding: '10px',
                  background: 'linear-gradient(135deg, #10b981, #34d399)',
                  color: 'white',
                  borderRadius: '10px',
                  textAlign: 'center',
                  fontWeight: 'bold'
                }}>
                  {expandedNodes.has(selectedNode.id) ? 
                    `Showing ${selectedNode.subnodes?.length || 0} subnodes` : 
                    `Click to explore ${selectedNode.subnodes?.length || 0} subnodes`}
                </div>
              ) : getNodeState(selectedNode.id, userStats.conqueredNodes, allNodes) === 'available' && (
                <button
                  onClick={() => setShowQuiz(true)}
                  style={{
                    marginTop: '15px',
                    padding: '10px 20px',
                    background: 'linear-gradient(135deg, #059669, #0ea5e9)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '10px',
                    cursor: 'pointer',
                    fontWeight: 'bold',
                    width: '100%'
                  }}
                >
                  Start Learning <ChevronRight size={16} style={{ verticalAlign: 'middle' }} />
                </button>
              )}
            </div>
          )}
        </div>
        )}
      </Layout>

      {/* Learning Modal */}
      {selectedNode && (
        <LearningModal
          isOpen={showQuiz}
          onClose={() => {
            setShowQuiz(false);
            setCurrentQuestion(0);
            setSelectedAnswer(null);
            setAnswerFeedback(null);
          }}
          nodeId={selectedNode.id}
          nodeTitle={selectedNode.name}
          questions={currentQuizQuestions}
          onComplete={async (passed) => {
            if (passed && selectedNode) {
              const wasNewlyCompleted = await completeNode(selectedNode.id, selectedNode.points);
              if (wasNewlyCompleted) {
                setShowAchievement(true);
                setTimeout(() => setShowAchievement(false), 3000);
              }
            }
            setShowQuiz(false);
            setCurrentQuestion(0);
            setSelectedAnswer(null);
            setAnswerFeedback(null);
          }}
        />
      )}

      {/* Commentary Modal */}
      {selectedNode && showCommentary && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '20px'
        }}>
          <div style={{
            background: 'white',
            borderRadius: '20px',
            padding: '0',
            maxWidth: '800px',
            width: '100%',
            maxHeight: '90vh',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column' as const
          }}>
            <div style={{
              padding: '20px',
              borderBottom: '1px solid #e5e7eb',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <h2 style={{ margin: 0, color: '#2a2a2a', fontWeight: 'bold' }}>
                Community Commentary: {selectedNode.name}
              </h2>
              <button
                onClick={() => setShowCommentary(false)}
                style={{ background: 'none', border: 'none', cursor: 'pointer' }}
              >
                <X size={24} />
              </button>
            </div>
            <div style={{
              flex: 1,
              overflow: 'auto',
              padding: '20px'
            }}>
              <NodeCommentary nodeId={selectedNode.id} nodeName={selectedNode.name} />
            </div>
          </div>
        </div>
      )}

      {/* Legacy Quiz Modal - Keeping for reference, remove later */}
      {false && showQuiz && selectedNode && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '20px'
        }}>
          <div style={{
            background: 'white',
            borderRadius: '20px',
            padding: '30px',
            maxWidth: '500px',
            width: '100%'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ margin: 0, color: '#2a2a2a', fontWeight: 'bold' }}>{selectedNode?.name} Challenge</h2>
              <button
                onClick={() => {
                  setShowQuiz(false);
                  setCurrentQuestion(0);
                  setSelectedAnswer(null);
                  setAnswerFeedback(null);
                }}
                style={{ background: 'none', border: 'none', cursor: 'pointer' }}
              >
                <X size={24} />
              </button>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <div style={{ fontSize: '14px', color: '#4a4a4a', fontWeight: '500', marginBottom: '5px' }}>
                Question {currentQuestion + 1} of {currentQuizQuestions.length || 1}
              </div>
              <div style={{ height: '4px', background: '#e0e0e0', borderRadius: '2px' }}>
                <div style={{
                  width: `${((currentQuestion + 1) / (currentQuizQuestions.length || 1)) * 100}%`,
                  height: '100%',
                  background: 'linear-gradient(90deg, #059669, #0ea5e9)',
                  borderRadius: '2px'
                }} />
              </div>
            </div>

            <div>
              {questionsLoading ? (
                <div style={{ textAlign: 'center', padding: '40px', color: '#059669' }}>
                  Loading questions...
                </div>
              ) : currentQuizQuestions.length > 0 ? (
                <>
                  <h3 style={{ marginBottom: '20px', color: '#2a2a2a', fontWeight: '600' }}>
                    {currentQuizQuestions[currentQuestion]?.question}
                  </h3>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {currentQuizQuestions[currentQuestion]?.options.map((option: string, idx: number) => (
                      <button
                        key={idx}
                        onClick={() => !answerFeedback && handleAnswer(idx)}
                        disabled={answerFeedback !== null}
                        style={{
                          padding: '15px',
                          border: '2px solid',
                          borderColor: answerFeedback && selectedAnswer === idx
                            ? answerFeedback.isCorrect ? '#00c851' : '#ff4444'
                            : '#e0e0e0',
                          borderRadius: '10px',
                          background: answerFeedback && selectedAnswer === idx
                            ? answerFeedback.isCorrect ? '#e8f5e9' : '#ffebee'
                            : 'white',
                          cursor: answerFeedback ? 'default' : 'pointer',
                          textAlign: 'left',
                          transition: 'all 0.3s'
                        }}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                </>
              ) : (
                <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
                  No questions available for this topic yet.
                </div>
              )}
              {answerFeedback && (
                <div style={{
                  marginTop: '20px',
                  padding: '15px',
                  background: answerFeedback?.isCorrect ? '#e8f5e9' : '#fff3e0',
                  borderRadius: '10px',
                  border: `1px solid ${answerFeedback?.isCorrect ? '#00c851' : '#ff6f00'}`
                }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                    {answerFeedback?.isCorrect ? '✅ Correct!' : '💡 Not quite!'}
                  </div>
                  <div style={{ fontSize: '14px', color: '#4a4a4a' }}>
                    {answerFeedback?.explanation}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Achievement Popup */}
      {showAchievement && (
        <div className="fixed top-5 right-5 bg-white dark:bg-gray-800 rounded-2xl p-5 shadow-2xl z-[1001] animate-slideIn">
          <div className="flex items-center gap-4">
            <Trophy size={40} className="text-yellow-500" />
            <div>
              <div className="font-bold text-base text-gray-900 dark:text-gray-100">Node Conquered!</div>
              <div className="text-sm text-gray-600 dark:text-gray-400 font-medium">
                {selectedNode?.name} completed
              </div>
              <div className="text-xs text-forest-600 dark:text-forest-400 mt-1">
                +{selectedNode?.points} points earned!
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mobile Navigation */}
      {isMobile && <MobileNav />}

      {/* Floating Chatbot */}
      <ChatbotContainer
        nodeId={selectedNode?.id}
        nodeTitle={selectedNode?.name}
        isLearningMode={false}
      />

      {/* Onboarding Trigger */}
      <OnboardingTrigger />

      {/* Performance Monitoring */}
      <PerformanceMonitor />

      {/* Auth Modal */}
      <AuthModal 
        isOpen={showAuthModal} 
        onClose={() => setShowAuthModal(false)}
        onSuccess={() => {
          // Modal will be closed by onClose, just handle post-auth logic here if needed
          console.log('Authentication successful');
        }}
      />

      {/* Settings Modal */}
      <SettingsModal
        isOpen={showSettingsModal}
        onClose={() => setShowSettingsModal(false)}
      />

      <style>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.05); opacity: 0.9; }
        }
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default App;