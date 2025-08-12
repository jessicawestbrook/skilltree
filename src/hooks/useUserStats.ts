import { useState } from 'react';
import { UserStats } from '../types';

export const useUserStats = () => {
  const [userStats, setUserStats] = useState<UserStats>({
    pathfinderPoints: 2450,
    neuralLevel: 12,
    memoryCrystals: 8,
    synapticStreak: 7,
    conqueredNodes: ['symbols-meaning', 'quantity-concept', 'self-care', 'tool-use-basic'],
    neuralPower: 85,
    title: 'Knowledge Seeker'
  });

  const updateUserStats = (updates: Partial<UserStats>) => {
    setUserStats(prev => ({ ...prev, ...updates }));
  };

  const completeNode = (nodeId: string, points: number) => {
    if (!userStats.conqueredNodes.includes(nodeId)) {
      const newConqueredNodes = [...userStats.conqueredNodes, nodeId];
      const newPoints = userStats.pathfinderPoints + points;
      const newLevel = Math.floor(newConqueredNodes.length / 5) + 1;
      
      setUserStats(prev => ({
        ...prev,
        conqueredNodes: newConqueredNodes,
        pathfinderPoints: newPoints,
        memoryCrystals: prev.memoryCrystals + 1,
        neuralLevel: newLevel,
        title: newConqueredNodes.length > 20 ? 'Knowledge Master' : 
               newConqueredNodes.length > 10 ? 'Neural Explorer' : 'Knowledge Seeker'
      }));
      
      return true; // Node was newly completed
    }
    return false; // Node was already completed
  };

  const calculateProgress = (totalNodes: number) => {
    const completedNodes = userStats.conqueredNodes.length;
    return Math.round((completedNodes / totalNodes) * 100);
  };

  return {
    userStats,
    updateUserStats,
    completeNode,
    calculateProgress
  };
};