'use client';

import React, { useState, useEffect, useMemo, CSSProperties } from 'react';
import { Brain, Trophy, Star, Lock, CheckCircle, X, ChevronRight, Grid, Map, User, ChevronDown, ChevronRight as ChevronRightIcon, Plus, Minus } from 'lucide-react';

// Import types
import { Node, AnswerFeedback } from '../types';

// Import data
import { getAllHierarchicalNodes, getCategoryLabels } from '../data/hierarchicalKnowledgeGraph';
import { quizQuestions } from '../data/quizQuestions';
import { domainIcons } from '../data/domainIcons';

// Import hooks
import { useUserStats } from '../hooks/useUserStats';

// Import utilities
import { 
  getNodeState, 
  createHierarchicalConnections, 
  filterHierarchicalNodes,
  toggleNodeExpansion,
  getVisibleNodes,
  calculateHierarchicalProgress
} from '../utils/hierarchicalNodeUtils';

// Import components
import { Header } from '../components/Header';
import { Sidebar } from '../components/Sidebar';
import { AuthModal } from '../components/AuthModal';
import { UserProfile } from '../components/UserProfile';

const App = () => {
  // Responsive detection
  const [isMobile, setIsMobile] = useState(false);
  const [activeTab, setActiveTab] = useState('graph');
  
  useEffect(() => {
    setIsMobile(window.innerWidth < 768);
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Expanded nodes state for hierarchical display
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set());

  // Get all nodes including hierarchical ones
  const allNodes = useMemo(() => getAllHierarchicalNodes(expandedNodes), [expandedNodes]);
  
  // Get visible nodes (respecting expanded/collapsed state)
  const visibleNodes = useMemo(() => getVisibleNodes(allNodes, expandedNodes), [allNodes, expandedNodes]);
  
  // Calculate container height based on nodes
  const graphHeight = useMemo(() => {
    const maxY = Math.max(...allNodes.map(n => (n.y || 0) + 120), 700);
    return Math.min(maxY, 2000); // Cap at 2000px
  }, [allNodes]);
  
  // Create connections based on prerequisites and hierarchy
  const connections = useMemo(() => createHierarchicalConnections(visibleNodes), [visibleNodes]);

  // User stats hook
  const { userStats, completeNode, calculateProgress } = useUserStats();

  // State management
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
  const [showProfileModal, setShowProfileModal] = useState(false);

  // Filter nodes based on view and search
  const filteredNodes = useMemo(() => 
    filterHierarchicalNodes(visibleNodes, activeFilters, searchTerm, currentView, expandedNodes),
    [visibleNodes, activeFilters, searchTerm, currentView, expandedNodes]
  );

  // Handle node expansion/collapse
  const handleNodeExpansion = (nodeId: string) => {
    setExpandedNodes(prev => toggleNodeExpansion(nodeId, prev));
  };

  // Handle quiz answer
  const handleAnswer = (answerIndex: number) => {
    if (!selectedNode) return;
    
    setSelectedAnswer(answerIndex);
    const questions = quizQuestions[selectedNode.id] || quizQuestions['symbols-meaning'];
    const question = questions[currentQuestion] || questions[0];
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
  const handleCompleteNode = () => {
    if (!selectedNode) return;
    
    const wasNewlyCompleted = completeNode(selectedNode.id, selectedNode.points);
    
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

  // Styles
  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
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
      background: 'linear-gradient(135deg, #8e44ad, #9b59b6)',
      color: 'white',
      boxShadow: '0 5px 15px rgba(142, 68, 173, 0.4)',
      border: '2px solid rgba(155, 89, 182, 0.5)'
    } as CSSProperties
  };

  // Mobile navigation
  const MobileNav = () => (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      background: 'white',
      borderTop: '1px solid #ddd',
      display: 'flex',
      justifyContent: 'space-around',
      padding: '10px 0',
      zIndex: 1000
    }}>
      <button onClick={() => setActiveTab('graph')} style={{ 
        background: 'none', 
        border: 'none', 
        padding: '5px',
        color: activeTab === 'graph' ? '#667eea' : '#4a4a4a'
      }}>
        <Grid size={24} />
        <div style={{ fontSize: '10px' }}>Map</div>
      </button>
      <button onClick={() => setActiveTab('paths')} style={{ 
        background: 'none', 
        border: 'none', 
        padding: '5px',
        color: activeTab === 'paths' ? '#667eea' : '#4a4a4a'
      }}>
        <Map size={24} />
        <div style={{ fontSize: '10px' }}>Paths</div>
      </button>
      <button onClick={() => setActiveTab('profile')} style={{ 
        background: 'none', 
        border: 'none', 
        padding: '5px',
        color: activeTab === 'profile' ? '#667eea' : '#4a4a4a'
      }}>
        <User size={24} />
        <div style={{ fontSize: '10px' }}>Profile</div>
      </button>
    </div>
  );

  return (
    <div style={styles.container}>
      {/* Header */}
      <Header 
        userStats={userStats} 
        isMobile={isMobile} 
        calculateProgress={() => calculateHierarchicalProgress(allNodes, userStats.conqueredNodes, expandedNodes)}
        onAuthClick={() => setShowAuthModal(true)}
        onProfileClick={() => setShowProfileModal(true)}
      />

      <div style={styles.mainGrid}>
        {/* Left Sidebar - Filters */}
        {!isMobile && (
          <Sidebar
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
            currentView={currentView}
            setCurrentView={setCurrentView}
            activeFilters={activeFilters}
            toggleFilter={toggleFilter}
          />
        )}

        {/* Knowledge Graph */}
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
                  stroke={isActive ? '#667eea' : '#ddd'}
                  strokeWidth={isActive ? '2' : '1'}
                  strokeDasharray={!isActive ? '5,5' : '0'}
                  opacity={isActive ? 0.6 : 0.3}
                />
              );
            })}
          </svg>

          {filteredNodes.map(node => {
            const state = getNodeState(node.id, userStats.conqueredNodes, allNodes);
            const Icon = domainIcons[node.domain] || Brain;
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
                    if (state === 'available' && (quizQuestions[node.id] || quizQuestions['symbols-meaning'])) {
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
                <button
                  onClick={() => setSelectedNode(null)}
                  style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                >
                  <X size={20} />
                </button>
              </div>
              {selectedNode.isParent ? (
                <div style={{
                  marginTop: '15px',
                  padding: '10px',
                  background: 'linear-gradient(135deg, #8e44ad, #9b59b6)',
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
                    background: 'linear-gradient(135deg, #667eea, #764ba2)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '10px',
                    cursor: 'pointer',
                    fontWeight: 'bold',
                    width: '100%'
                  }}
                >
                  Start Challenge <ChevronRight size={16} style={{ verticalAlign: 'middle' }} />
                </button>
              )}
            </div>
          )}
        </div>

        {/* Right Sidebar - Stats */}
        {!isMobile && (
          <div>
            {/* User Stats */}
            <div style={styles.panel}>
              <h3 style={{ fontSize: '16px', marginBottom: '15px', color: '#2a2a2a', fontWeight: 'bold' }}>Your Progress</h3>
              <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                <div style={{ 
                  width: '80px', 
                  height: '80px', 
                  margin: '0 auto',
                  background: 'linear-gradient(135deg, #667eea, #764ba2)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '10px'
                }}>
                  <User size={40} color="white" />
                </div>
                <div style={{ fontWeight: 'bold', fontSize: '18px', color: '#2a2a2a' }}>{userStats.title}</div>
                <div style={{ fontSize: '12px', color: '#5a5a5a', fontWeight: '500' }}>Level {userStats.neuralLevel}</div>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <div style={{ background: '#f8f8f8', padding: '10px', borderRadius: '8px', textAlign: 'center' }}>
                  <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#667eea' }}>
                    {userStats.conqueredNodes.length}
                  </div>
                  <div style={{ fontSize: '10px', color: '#5a5a5a', fontWeight: '600' }}>CONQUERED</div>
                </div>
                <div style={{ background: '#f8f8f8', padding: '10px', borderRadius: '8px', textAlign: 'center' }}>
                  <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#764ba2' }}>
                    {userStats.memoryCrystals}
                  </div>
                  <div style={{ fontSize: '10px', color: '#5a5a5a', fontWeight: '600' }}>CRYSTALS</div>
                </div>
              </div>
            </div>

            {/* Recent Achievements */}
            <div style={{ ...styles.panel, marginTop: '15px' }}>
              <h3 style={{ fontSize: '16px', marginBottom: '15px', color: '#2a2a2a', fontWeight: 'bold' }}>Recent Achievements</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '10px', background: '#f8f8f8', borderRadius: '8px' }}>
                  <Trophy size={20} color="#ffd700" />
                  <div>
                    <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#2a2a2a' }}>First Steps</div>
                    <div style={{ fontSize: '11px', color: '#4a4a4a' }}>Complete 5 nodes</div>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '10px', background: '#f8f8f8', borderRadius: '8px' }}>
                  <Star size={20} color="#667eea" />
                  <div>
                    <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#2a2a2a' }}>Quick Learner</div>
                    <div style={{ fontSize: '11px', color: '#4a4a4a' }}>Complete 3 nodes in one day</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Suggested Next */}
            <div style={{ ...styles.panel, marginTop: '15px' }}>
              <h3 style={{ fontSize: '16px', marginBottom: '15px', color: '#2a2a2a', fontWeight: 'bold' }}>Suggested Next</h3>
              {filteredNodes
                .filter(n => getNodeState(n.id, userStats.conqueredNodes, allNodes) === 'available')
                .slice(0, 3)
                .map(node => {
                  const Icon = domainIcons[node.domain] || Brain;
                  return (
                    <div 
                      key={node.id}
                      style={{ 
                        padding: '10px', 
                        background: '#f8f8f8', 
                        borderRadius: '8px', 
                        marginBottom: '8px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px'
                      }}
                      onClick={() => setSelectedNode(node)}
                    >
                      <Icon size={20} color="#667eea" />
                      <div>
                        <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#2a2a2a' }}>{node.name}</div>
                        <div style={{ fontSize: '11px', color: '#4a4a4a', fontWeight: '500' }}>+{node.points} points</div>
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>
        )}
      </div>

      {/* Quiz Modal */}
      {showQuiz && selectedNode && (
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
              <h2 style={{ margin: 0, color: '#2a2a2a', fontWeight: 'bold' }}>{selectedNode.name} Challenge</h2>
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
                Question {currentQuestion + 1} of 1
              </div>
              <div style={{ height: '4px', background: '#e0e0e0', borderRadius: '2px' }}>
                <div style={{
                  width: '100%',
                  height: '100%',
                  background: 'linear-gradient(90deg, #667eea, #764ba2)',
                  borderRadius: '2px'
                }} />
              </div>
            </div>

            <div>
              <h3 style={{ marginBottom: '20px', color: '#2a2a2a', fontWeight: '600' }}>
                {(quizQuestions[selectedNode.id] || quizQuestions['symbols-meaning'])[0].question}
              </h3>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {(quizQuestions[selectedNode.id] || quizQuestions['symbols-meaning'])[0].options.map((option: string, idx: number) => (
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

              {answerFeedback && (
                <div style={{
                  marginTop: '20px',
                  padding: '15px',
                  background: answerFeedback.isCorrect ? '#e8f5e9' : '#fff3e0',
                  borderRadius: '10px',
                  border: `1px solid ${answerFeedback.isCorrect ? '#00c851' : '#ff6f00'}`
                }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                    {answerFeedback.isCorrect ? '✅ Correct!' : '💡 Not quite!'}
                  </div>
                  <div style={{ fontSize: '14px', color: '#4a4a4a' }}>
                    {answerFeedback.explanation}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Achievement Popup */}
      {showAchievement && (
        <div style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          background: 'white',
          borderRadius: '15px',
          padding: '20px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
          zIndex: 1001,
          animation: 'slideIn 0.5s ease-out'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <Trophy size={40} color="#ffd700" />
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '16px', color: '#2a2a2a' }}>Node Conquered!</div>
              <div style={{ fontSize: '14px', color: '#4a4a4a', fontWeight: '500' }}>
                {selectedNode?.name} completed
              </div>
              <div style={{ fontSize: '12px', color: '#667eea', marginTop: '5px' }}>
                +{selectedNode?.points} points earned!
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mobile Navigation */}
      {isMobile && <MobileNav />}

      {/* Auth Modal */}
      <AuthModal 
        isOpen={showAuthModal} 
        onClose={() => setShowAuthModal(false)} 
      />

      {/* Profile Modal */}
      <UserProfile 
        isOpen={showProfileModal} 
        onClose={() => setShowProfileModal(false)} 
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