'use client';

import React, { useState, CSSProperties } from 'react';
import { Play, CheckCircle, Star, ArrowRight, Brain, Clock, Trophy } from 'lucide-react';

export const FirstNodeStep: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [isCompleted, setIsCompleted] = useState(false);

  const beginnerNodes = [
    {
      id: 'intro-science',
      title: 'Introduction to Science',
      description: 'Discover the scientific method and how we understand the world',
      difficulty: 'Beginner',
      duration: '5 min',
      points: 50,
      category: 'Science',
      color: '#4facfe',
    },
    {
      id: 'basic-math',
      title: 'Basic Mathematics',
      description: 'Essential mathematical concepts for everyday life',
      difficulty: 'Beginner',
      duration: '7 min',
      points: 60,
      category: 'Mathematics',
      color: '#667eea',
    },
    {
      id: 'intro-history',
      title: 'Introduction to History',
      description: 'Explore how civilizations developed over time',
      difficulty: 'Beginner',
      duration: '6 min',
      points: 55,
      category: 'History',
      color: '#fa709a',
    },
    {
      id: 'communication',
      title: 'Effective Communication',
      description: 'Learn the basics of clear and persuasive communication',
      difficulty: 'Beginner',
      duration: '4 min',
      points: 45,
      category: 'Skills',
      color: '#4ade80',
    },
  ];

  const styles = {
    container: {
      padding: '20px 0',
    } as CSSProperties,
    header: {
      textAlign: 'center',
      marginBottom: '32px',
    } as CSSProperties,
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '12px',
    } as CSSProperties,
    subtitle: {
      fontSize: '16px',
      color: '#666',
      lineHeight: '1.6',
      marginBottom: '24px',
    } as CSSProperties,
    motivation: {
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      padding: '20px',
      borderRadius: '16px',
      textAlign: 'center',
      marginBottom: '32px',
    } as CSSProperties,
    motivationText: {
      fontSize: '18px',
      fontWeight: 'bold',
      marginBottom: '8px',
    } as CSSProperties,
    motivationSubtext: {
      fontSize: '14px',
      opacity: 0.9,
    } as CSSProperties,
    nodesGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
      gap: '16px',
      marginBottom: '32px',
    } as CSSProperties,
    nodeCard: {
      padding: '20px',
      border: '2px solid #e0e0e0',
      borderRadius: '16px',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      background: '#fff',
      position: 'relative',
      overflow: 'hidden',
    } as CSSProperties,
    nodeCardSelected: {
      borderColor: '#667eea',
      transform: 'translateY(-4px)',
      boxShadow: '0 12px 30px rgba(102, 126, 234, 0.15)',
    } as CSSProperties,
    nodeHeader: {
      display: 'flex',
      alignItems: 'flex-start',
      justifyContent: 'space-between',
      marginBottom: '12px',
    } as CSSProperties,
    nodeCategory: {
      display: 'inline-block',
      padding: '4px 8px',
      borderRadius: '6px',
      fontSize: '10px',
      fontWeight: 'bold',
      color: 'white',
      textTransform: 'uppercase',
      letterSpacing: '0.5px',
    } as CSSProperties,
    playButton: {
      width: '36px',
      height: '36px',
      borderRadius: '50%',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'transform 0.2s ease',
      flexShrink: 0,
    } as CSSProperties,
    nodeTitle: {
      fontSize: '18px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '8px',
    } as CSSProperties,
    nodeDescription: {
      fontSize: '14px',
      color: '#666',
      lineHeight: '1.4',
      marginBottom: '16px',
    } as CSSProperties,
    nodeStats: {
      display: 'flex',
      alignItems: 'center',
      gap: '16px',
      fontSize: '12px',
      color: '#999',
    } as CSSProperties,
    stat: {
      display: 'flex',
      alignItems: 'center',
      gap: '4px',
    } as CSSProperties,
    selectedIndicator: {
      position: 'absolute',
      top: '16px',
      right: '16px',
      width: '24px',
      height: '24px',
      borderRadius: '50%',
      background: '#4ade80',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontSize: '12px',
    } as CSSProperties,
    actionSection: {
      textAlign: 'center',
      padding: '24px',
      background: '#f8f9ff',
      borderRadius: '16px',
      border: '1px solid #e6e8ff',
    } as CSSProperties,
    startButton: {
      padding: '16px 32px',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      border: 'none',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: 'bold',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      disabled: false,
    } as CSSProperties,
    completedState: {
      textAlign: 'center',
      padding: '40px 20px',
    } as CSSProperties,
    completedIcon: {
      width: '80px',
      height: '80px',
      borderRadius: '50%',
      background: 'linear-gradient(135deg, #4ade80, #22c55e)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      margin: '0 auto 20px',
    } as CSSProperties,
    completedTitle: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a',
      marginBottom: '12px',
    } as CSSProperties,
    completedDescription: {
      fontSize: '16px',
      color: '#666',
      marginBottom: '24px',
    } as CSSProperties,
    reward: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      background: 'linear-gradient(135deg, #fbbf24, #f59e0b)',
      color: 'white',
      padding: '12px 20px',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: 'bold',
    } as CSSProperties,
  };

  const handleNodeSelect = (nodeId: string) => {
    setSelectedNode(nodeId);
  };

  const handleStartLearning = () => {
    // Simulate completing the node
    setTimeout(() => {
      setIsCompleted(true);
    }, 2000);
  };

  if (isCompleted) {
    return (
      <div style={styles.completedState}>
        <div style={styles.completedIcon}>
          <CheckCircle size={40} color="white" />
        </div>
        <h2 style={styles.completedTitle}>Congratulations! 🎉</h2>
        <p style={styles.completedDescription}>
          You&apos;ve completed your first knowledge node! You&apos;re now ready to explore the vast world of learning.
        </p>
        <div style={styles.reward}>
          <Trophy size={20} />
          +50 Points Earned!
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Choose Your First Node</h2>
        <p style={styles.subtitle}>
          Select a topic that interests you to begin your learning journey. Don&apos;t worry - you can explore all areas later!
        </p>
        <div style={styles.motivation}>
          <div style={styles.motivationText}>
            Every expert was once a beginner 🌱
          </div>
          <div style={styles.motivationSubtext}>
            Take the first step towards mastering human knowledge
          </div>
        </div>
      </div>

      <div style={styles.nodesGrid}>
        {beginnerNodes.map((node) => (
          <div
            key={node.id}
            style={{
              ...styles.nodeCard,
              ...(selectedNode === node.id ? styles.nodeCardSelected : {}),
            }}
            onClick={() => handleNodeSelect(node.id)}
          >
            {selectedNode === node.id && (
              <div style={styles.selectedIndicator}>
                ✓
              </div>
            )}
            
            <div style={styles.nodeHeader}>
              <span style={{ ...styles.nodeCategory, background: node.color }}>
                {node.category}
              </span>
              <button 
                style={styles.playButton}
                onMouseEnter={(e) => {
                  (e.target as HTMLElement).style.transform = 'scale(1.1)';
                }}
                onMouseLeave={(e) => {
                  (e.target as HTMLElement).style.transform = 'scale(1)';
                }}
              >
                <Play size={16} color="white" />
              </button>
            </div>

            <h3 style={styles.nodeTitle}>{node.title}</h3>
            <p style={styles.nodeDescription}>{node.description}</p>

            <div style={styles.nodeStats}>
              <div style={styles.stat}>
                <Clock size={12} />
                {node.duration}
              </div>
              <div style={styles.stat}>
                <Star size={12} />
                {node.difficulty}
              </div>
              <div style={styles.stat}>
                <Trophy size={12} />
                {node.points} pts
              </div>
            </div>
          </div>
        ))}
      </div>

      <div style={styles.actionSection}>
        <button
          style={styles.startButton}
          onClick={handleStartLearning}
          disabled={!selectedNode}
          onMouseEnter={(e) => {
            if (!selectedNode) return;
            (e.target as HTMLElement).style.transform = 'translateY(-2px)';
            (e.target as HTMLElement).style.boxShadow = '0 8px 25px rgba(102, 126, 234, 0.3)';
          }}
          onMouseLeave={(e) => {
            (e.target as HTMLElement).style.transform = 'translateY(0)';
            (e.target as HTMLElement).style.boxShadow = 'none';
          }}
        >
          <Brain size={20} />
          Start Learning
          <ArrowRight size={16} />
        </button>
        {!selectedNode && (
          <p style={{ fontSize: '14px', color: '#999', marginTop: '12px' }}>
            Please select a node to begin
          </p>
        )}
      </div>
    </div>
  );
};