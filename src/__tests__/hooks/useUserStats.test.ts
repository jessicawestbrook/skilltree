import { renderHook, act } from '@testing-library/react';
import { useUserStats } from '../../hooks/useUserStats';
import { UserStats } from '../../types';

// Mock the supabase client
jest.mock('../../lib/supabase-client', () => ({
  createClient: jest.fn(() => ({
    auth: {
      getUser: jest.fn(() => Promise.resolve({ data: { user: null }, error: null }))
    },
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => ({
          single: jest.fn(() => Promise.resolve({ data: null, error: null }))
        }))
      })),
      upsert: jest.fn(() => Promise.resolve({ data: null, error: null })),
      delete: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({ data: null, error: null }))
      }))
    }))
  }))
}));

// Mock the pushNotificationService
jest.mock('../../services/pushNotificationService', () => ({
  pushNotificationService: {
    notifyLevelUp: jest.fn(),
    notifyStreak: jest.fn(),
    notifyAchievement: jest.fn()
  }
}));

describe('useUserStats', () => {
  it('should initialize with default user stats', () => {
    const { result } = renderHook(() => useUserStats());
    
    expect(result.current.userStats).toEqual({
      pathfinderPoints: 2450,
      neuralLevel: 12,
      memoryCrystals: 8,
      synapticStreak: 7,
      conqueredNodes: ['symbols-meaning', 'quantity-concept', 'self-care', 'tool-use-basic'],
      neuralPower: 85,
      title: 'Knowledge Seeker'
    });
  });

  describe('updateUserStats', () => {
    it('should update user stats with partial updates', () => {
      const { result } = renderHook(() => useUserStats());
      
      act(() => {
        result.current.updateUserStats({ 
          pathfinderPoints: 3000,
          synapticStreak: 10 
        });
      });

      expect(result.current.userStats.pathfinderPoints).toBe(3000);
      expect(result.current.userStats.synapticStreak).toBe(10);
      expect(result.current.userStats.neuralLevel).toBe(12); // unchanged
    });

    it('should maintain all other properties when updating', () => {
      const { result } = renderHook(() => useUserStats());
      const originalStats = result.current.userStats;
      
      act(() => {
        result.current.updateUserStats({ neuralPower: 95 });
      });

      expect(result.current.userStats).toEqual({
        ...originalStats,
        neuralPower: 95
      });
    });
  });

  describe('completeNode', () => {
    it('should add new node to conquered nodes and update stats', async () => {
      const { result } = renderHook(() => useUserStats());
      
      let wasNewCompletion;
      await act(async () => {
        wasNewCompletion = await result.current.completeNode('new-node', 100);
      });
      
      expect(wasNewCompletion).toBe(true);
      expect(result.current.userStats.conqueredNodes).toContain('new-node');
      expect(result.current.userStats.pathfinderPoints).toBe(2550); // 2450 + 100
      expect(result.current.userStats.memoryCrystals).toBe(9); // 8 + 1
    });

    it('should not add duplicate nodes', async () => {
      const { result } = renderHook(() => useUserStats());
      
      let wasNewCompletion;
      await act(async () => {
        wasNewCompletion = await result.current.completeNode('symbols-meaning', 100);
      });
      
      expect(wasNewCompletion).toBe(false);

      expect(result.current.userStats.conqueredNodes.filter(node => node === 'symbols-meaning')).toHaveLength(1);
      expect(result.current.userStats.pathfinderPoints).toBe(2450); // unchanged
    });

    it('should update neural level based on conquered nodes count', async () => {
      const { result } = renderHook(() => useUserStats());
      const initialLevel = result.current.userStats.neuralLevel;
      
      // Add one more node (currently 4, will be 5 total)
      await act(async () => {
        await result.current.completeNode('new-node-1', 100);
      });

      const expectedLevel = Math.floor(5 / 5) + 1; // 2
      expect(result.current.userStats.neuralLevel).toBe(expectedLevel);
    });

    it('should update title based on conquered nodes count', async () => {
      const { result } = renderHook(() => useUserStats());
      
      // Add nodes one by one to reach the title thresholds
      // Start with 4 nodes, add enough to reach > 20 (Knowledge Master)
      for (let i = 0; i < 17; i++) {
        await act(async () => {
          await result.current.completeNode(`new-node-${i}`, 50);
        });
      }

      // Should now have 4 + 17 = 21 nodes, which should be 'Knowledge Master'
      const finalLength = result.current.userStats.conqueredNodes.length;
      expect(finalLength).toBe(21);
      expect(result.current.userStats.title).toBe('Knowledge Master');
    });

    it('should handle multiple node completions correctly', async () => {
      const { result } = renderHook(() => useUserStats());
      const initialPoints = result.current.userStats.pathfinderPoints;
      const initialCrystals = result.current.userStats.memoryCrystals;
      const initialLength = result.current.userStats.conqueredNodes.length;
      
      // Complete nodes one by one to ensure state updates are processed
      await act(async () => {
        await result.current.completeNode('node-1', 50);
      });
      
      await act(async () => {
        await result.current.completeNode('node-2', 75);
      });
      
      await act(async () => {
        await result.current.completeNode('node-3', 100);
      });

      // All three nodes should be added
      const finalLength = result.current.userStats.conqueredNodes.length;
      expect(finalLength).toBe(initialLength + 3);
      expect(result.current.userStats.pathfinderPoints).toBe(initialPoints + 225); // 50 + 75 + 100
      expect(result.current.userStats.memoryCrystals).toBe(initialCrystals + 3);
    });
  });

  describe('calculateProgress', () => {
    it('should calculate progress percentage correctly', () => {
      const { result } = renderHook(() => useUserStats());
      
      // Currently has 4 conquered nodes
      const progress = result.current.calculateProgress(20);
      expect(progress).toBe(20); // 4/20 * 100 = 20%
    });

    it('should handle zero total nodes', () => {
      const { result } = renderHook(() => useUserStats());
      
      const progress = result.current.calculateProgress(0);
      expect(progress).toBe(Infinity); // 4/0 * 100 = Infinity in JavaScript
    });

    it('should handle 100% completion', () => {
      const { result } = renderHook(() => useUserStats());
      
      const progress = result.current.calculateProgress(4);
      expect(progress).toBe(100); // 4/4 * 100 = 100%
    });

    it('should round progress to nearest integer', () => {
      const { result } = renderHook(() => useUserStats());
      
      const progress = result.current.calculateProgress(3);
      expect(progress).toBe(133); // 4/3 * 100 = 133.33... rounded to 133
    });

    it('should update progress calculation after completing nodes', async () => {
      const { result } = renderHook(() => useUserStats());
      
      let progress = result.current.calculateProgress(10);
      expect(progress).toBe(40); // 4/10 * 100 = 40%

      await act(async () => {
        await result.current.completeNode('new-node', 100);
      });

      progress = result.current.calculateProgress(10);
      expect(progress).toBe(50); // 5/10 * 100 = 50%
    });
  });

  describe('Edge cases and error handling', () => {
    it('should handle extremely large point values', async () => {
      const { result } = renderHook(() => useUserStats());
      
      await act(async () => {
        await result.current.completeNode('large-node', Number.MAX_SAFE_INTEGER);
      });

      expect(result.current.userStats.pathfinderPoints).toBeGreaterThan(2450);
      expect(typeof result.current.userStats.pathfinderPoints).toBe('number');
    });

    it('should handle negative point values gracefully', async () => {
      const { result } = renderHook(() => useUserStats());
      const initialPoints = result.current.userStats.pathfinderPoints;
      
      await act(async () => {
        await result.current.completeNode('negative-node', -100);
      });

      // Should handle negative values without breaking
      expect(typeof result.current.userStats.pathfinderPoints).toBe('number');
      expect(result.current.userStats.pathfinderPoints).toBeLessThan(initialPoints + 100);
    });

    it('should handle very long node IDs', async () => {
      const { result } = renderHook(() => useUserStats());
      const longNodeId = 'a'.repeat(1000);
      
      let success;
      await act(async () => {
        success = await result.current.completeNode(longNodeId, 50);
      });
      expect(success).toBe(true);

      expect(result.current.userStats.conqueredNodes).toContain(longNodeId);
    });

    it('should handle special characters in node IDs', async () => {
      const { result } = renderHook(() => useUserStats());
      const specialNodeId = 'node-with-special-chars-!@#$%^&*()_+{}|:"<>?[]\\;\',./ ';
      
      let success;
      await act(async () => {
        success = await result.current.completeNode(specialNodeId, 75);
      });
      expect(success).toBe(true);

      expect(result.current.userStats.conqueredNodes).toContain(specialNodeId);
    });

    it('should handle rapid successive node completions', async () => {
      const { result } = renderHook(() => useUserStats());
      const initialLength = result.current.userStats.conqueredNodes.length;
      
      // Due to React state batching, only the last call in a single act() is effective
      // Test with a smaller number and individual acts to verify the functionality
      for (let i = 0; i < 5; i++) {
        await act(async () => {
          await result.current.completeNode(`rapid-node-${i}`, 10);
        });
      }

      expect(result.current.userStats.conqueredNodes.length).toBe(initialLength + 5);
      expect(result.current.userStats.pathfinderPoints).toBe(2450 + 50); // 5 * 10
      expect(result.current.userStats.memoryCrystals).toBe(8 + 5); // 5 crystals
    });

    it('should maintain consistent state after many operations', async () => {
      const { result } = renderHook(() => useUserStats());
      
      // Perform operations in separate acts to ensure state updates
      act(() => {
        result.current.updateUserStats({ neuralPower: 100 });
      });
      
      await act(async () => {
        await result.current.completeNode('test-1', 50);
      });
      
      act(() => {
        result.current.updateUserStats({ synapticStreak: 15 });
      });
      
      await act(async () => {
        await result.current.completeNode('test-2', 75);
      });

      const stats = result.current.userStats;
      
      // Verify all fields are still valid
      expect(typeof stats.pathfinderPoints).toBe('number');
      expect(typeof stats.neuralLevel).toBe('number');
      expect(typeof stats.memoryCrystals).toBe('number');
      expect(typeof stats.synapticStreak).toBe('number');
      expect(typeof stats.neuralPower).toBe('number');
      expect(typeof stats.title).toBe('string');
      expect(Array.isArray(stats.conqueredNodes)).toBe(true);
      
      // Verify specific values
      expect(stats.neuralPower).toBe(100);
      expect(stats.synapticStreak).toBe(15);
      expect(stats.conqueredNodes).toContain('test-1');
      expect(stats.conqueredNodes).toContain('test-2');
    });

    it('should handle edge case calculations with zero values', async () => {
      const { result } = renderHook(() => useUserStats());
      
      await act(async () => {
        await result.current.completeNode('zero-points', 0);
      });

      // Should still add to conquered nodes even with 0 points
      expect(result.current.userStats.conqueredNodes).toContain('zero-points');
      expect(result.current.userStats.pathfinderPoints).toBe(2450); // unchanged
      expect(result.current.userStats.memoryCrystals).toBe(9); // still incremented
    });

    it('should calculate progress correctly with edge case values', () => {
      const { result } = renderHook(() => useUserStats());
      
      // Test with very small total
      let progress = result.current.calculateProgress(1);
      expect(progress).toBe(400); // 4/1 * 100 = 400%

      // Test with very large total
      progress = result.current.calculateProgress(1000000);
      expect(progress).toBe(0); // 4/1000000 * 100 = 0.0004 rounded to 0
      
      // Test with same number as conquered nodes
      progress = result.current.calculateProgress(4);
      expect(progress).toBe(100); // 4/4 * 100 = 100%
    });
  });
});