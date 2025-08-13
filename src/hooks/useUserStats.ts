import { useState } from 'react';
import { UserStats } from '../types';
import { pushNotificationService } from '../services/pushNotificationService';

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

  const completeNode = async (nodeId: string, points: number) => {
    if (!userStats.conqueredNodes.includes(nodeId)) {
      const newConqueredNodes = [...userStats.conqueredNodes, nodeId];
      const newPoints = userStats.pathfinderPoints + points;
      const previousLevel = userStats.neuralLevel;
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
      
      // Trigger notifications for achievements
      if (newLevel > previousLevel) {
        await pushNotificationService.notifyLevelUp(newLevel);
      }
      
      // Check for streak milestones
      if (userStats.synapticStreak === 7) {
        await pushNotificationService.notifyStreak(7);
      } else if (userStats.synapticStreak === 30) {
        await pushNotificationService.notifyStreak(30);
      }
      
      // Achievement notifications based on conquered nodes
      if (newConqueredNodes.length === 5) {
        await pushNotificationService.notifyAchievement(
          'First Steps',
          'Completed your first 5 knowledge nodes!'
        );
      } else if (newConqueredNodes.length === 10) {
        await pushNotificationService.notifyAchievement(
          'Neural Explorer',
          'Mastered 10 knowledge nodes!'
        );
      } else if (newConqueredNodes.length === 20) {
        await pushNotificationService.notifyAchievement(
          'Knowledge Master',
          'Conquered 20 knowledge nodes!'
        );
      }
      
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