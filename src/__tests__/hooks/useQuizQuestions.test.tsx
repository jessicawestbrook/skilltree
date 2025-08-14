import React from 'react';
import { renderHook, waitFor } from '@testing-library/react';
import { useQuizQuestions } from '../../hooks/useQuizQuestions';

// Mock the QuizService
jest.mock('../../services/quizService', () => ({
  QuizService: {
    getQuestionsForNode: jest.fn(),
    getAllQuestions: jest.fn()
  }
}));

import { QuizService } from '../../services/quizService';

const mockQuizService = QuizService as jest.Mocked<typeof QuizService>;

describe('useQuizQuestions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('basic functionality', () => {
    it('should return initial loading state', () => {
      mockQuizService.getQuestionsForNode.mockImplementation(() => new Promise(() => {})); // Never resolves

      const { result } = renderHook(() => useQuizQuestions('node123'));

      expect(result.current.loading).toBe(true);
      expect(result.current.questions).toEqual([]);
      expect(result.current.error).toBeNull();
    });

    it('should fetch questions successfully', async () => {
      const mockQuestions = [
        {
          id: '1',
          node_id: 'node123',
          question: 'What is JavaScript?',
          options: ['Language', 'Framework', 'Library', 'Database'],
          correct: 0,
          explanation: 'JavaScript is a programming language'
        },
        {
          id: '2',
          node_id: 'node123',
          question: 'What is React?',
          options: ['Language', 'Framework', 'Library', 'Database'],
          correct: 2,
          explanation: 'React is a JavaScript library'
        }
      ];

      mockQuizService.getQuestionsForNode.mockResolvedValue(mockQuestions);

      const { result } = renderHook(() => useQuizQuestions('node123'));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.questions).toEqual(mockQuestions);
        expect(result.current.error).toBeNull();
      });

      expect(mockQuizService.getQuestionsForNode).toHaveBeenCalledWith('node123');
    });

    it('should handle fetch errors', async () => {
      const errorMessage = 'Failed to fetch questions';
      mockQuizService.getQuestionsForNode.mockRejectedValue(new Error(errorMessage));

      const { result } = renderHook(() => useQuizQuestions('node123'));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        // On error, the hook provides fallback questions
        expect(result.current.questions).toHaveLength(1);
        expect(result.current.error).toBe('Failed to load quiz questions');
      });
    });
  });

  describe('node ID changes', () => {
    it('should refetch questions when node ID changes', async () => {
      const mockQuestions1 = [
        {
          id: '1',
          node_id: 'node123',
          question: 'Question 1',
          options: ['A', 'B', 'C', 'D'],
          correct: 0,
          explanation: 'Explanation 1'
        }
      ];

      const mockQuestions2 = [
        {
          id: '2',
          node_id: 'node456',
          question: 'Question 2',
          options: ['A', 'B', 'C', 'D'],
          correct: 1,
          explanation: 'Explanation 2'
        }
      ];

      mockQuizService.getQuestionsForNode
        .mockResolvedValueOnce(mockQuestions1)
        .mockResolvedValueOnce(mockQuestions2);

      const { result, rerender } = renderHook(
        ({ nodeId }) => useQuizQuestions(nodeId),
        { initialProps: { nodeId: 'node123' } }
      );

      await waitFor(() => {
        expect(result.current.questions).toEqual(mockQuestions1);
      });

      // Change node ID
      rerender({ nodeId: 'node456' });

      await waitFor(() => {
        expect(result.current.questions).toEqual(mockQuestions2);
      });

      expect(mockQuizService.getQuestionsForNode).toHaveBeenCalledWith('node123');
      expect(mockQuizService.getQuestionsForNode).toHaveBeenCalledWith('node456');
      expect(mockQuizService.getQuestionsForNode).toHaveBeenCalledTimes(2);
    });

    it('should not fetch when node ID is null', () => {
      const { result } = renderHook(() => useQuizQuestions(null));

      expect(result.current.loading).toBe(false);
      expect(result.current.questions).toEqual([]);
      expect(result.current.error).toBeNull();
      expect(mockQuizService.getQuestionsForNode).not.toHaveBeenCalled();
    });

    it('should not fetch when node ID is empty string', () => {
      const { result } = renderHook(() => useQuizQuestions(''));

      expect(result.current.loading).toBe(false);
      expect(result.current.questions).toEqual([]);
      expect(result.current.error).toBeNull();
      expect(mockQuizService.getQuestionsForNode).not.toHaveBeenCalled();
    });

    it('should clear questions when node ID becomes null', async () => {
      const mockQuestions = [
        {
          id: '1',
          node_id: 'node123',
          question: 'Question 1',
          options: ['A', 'B', 'C', 'D'],
          correct: 0,
          explanation: 'Explanation 1'
        }
      ];

      mockQuizService.getQuestionsForNode.mockResolvedValue(mockQuestions);

      const { result, rerender } = renderHook(
        ({ nodeId }) => useQuizQuestions(nodeId),
        { initialProps: { nodeId: 'node123' } }
      );

      await waitFor(() => {
        expect(result.current.questions).toEqual(mockQuestions);
      });

      // Change to null node ID
      rerender({ nodeId: null });

      expect(result.current.loading).toBe(false);
      expect(result.current.questions).toEqual([]);
      expect(result.current.error).toBeNull();
    });
  });

  describe('loading states', () => {
    it('should show loading when switching between valid node IDs', async () => {
      mockQuizService.getQuestionsForNode
        .mockImplementation(() => new Promise(resolve => setTimeout(() => resolve([]), 100)))
        .mockImplementationOnce(() => Promise.resolve([]));

      const { result, rerender } = renderHook(
        ({ nodeId }) => useQuizQuestions(nodeId),
        { initialProps: { nodeId: 'node123' } }
      );

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Change node ID - should trigger loading
      rerender({ nodeId: 'node456' });

      expect(result.current.loading).toBe(true);

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });
    });

    it('should reset error state when refetching', async () => {
      mockQuizService.getQuestionsForNode
        .mockRejectedValueOnce(new Error('First error'))
        .mockResolvedValueOnce([]);

      const { result, rerender } = renderHook(
        ({ nodeId }) => useQuizQuestions(nodeId),
        { initialProps: { nodeId: 'node123' } }
      );

      await waitFor(() => {
        expect(result.current.error).toBe('Failed to load quiz questions');
      });

      // Change node ID - should clear error
      rerender({ nodeId: 'node456' });

      await waitFor(() => {
        expect(result.current.error).toBeNull();
        expect(result.current.loading).toBe(false);
      });
    });
  });

  describe('edge cases', () => {
    it('should handle empty questions array', async () => {
      mockQuizService.getQuestionsForNode.mockResolvedValue([]);

      const { result } = renderHook(() => useQuizQuestions('node123'));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.questions).toEqual([]);
        expect(result.current.error).toBeNull();
      });
    });

    it('should handle service returning null', async () => {
      mockQuizService.getQuestionsForNode.mockResolvedValue(null as any);

      const { result } = renderHook(() => useQuizQuestions('node123'));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.questions).toBe(null);
        expect(result.current.error).toBeNull();
      });
    });

    it('should handle malformed questions data', async () => {
      const malformedQuestions = [
        { id: '1' }, // Missing required fields
        null,
        undefined,
        {
          id: '2',
          node_id: 'node123',
          question: 'Valid question',
          options: ['A', 'B', 'C', 'D'],
          correct: 0,
          explanation: 'Valid explanation'
        }
      ];

      mockQuizService.getQuestionsForNode.mockResolvedValue(malformedQuestions as any);

      const { result } = renderHook(() => useQuizQuestions('node123'));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
        expect(result.current.questions).toEqual(malformedQuestions);
        expect(result.current.error).toBeNull();
      });
    });

    it('should handle rapid node ID changes', async () => {
      mockQuizService.getQuestionsForNode.mockImplementation(
        (nodeId) => new Promise(resolve => 
          setTimeout(() => resolve([{ 
            id: nodeId, 
            node_id: nodeId,
            question: `Question for ${nodeId}`,
            options: ['A', 'B', 'C', 'D'],
            correct: 0,
            explanation: 'Test'
          }]), 50)
        )
      );

      const { result, rerender } = renderHook(
        ({ nodeId }) => useQuizQuestions(nodeId),
        { initialProps: { nodeId: 'node1' } }
      );

      // Rapidly change node IDs
      rerender({ nodeId: 'node2' });
      rerender({ nodeId: 'node3' });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Should have the questions for the final node ID
      expect(result.current.questions[0]?.node_id).toBe('node3');
    });
  });

  describe('cleanup', () => {
    it('should not update state after unmount', async () => {
      let resolvePromise: (value: any) => void;
      const promise = new Promise(resolve => {
        resolvePromise = resolve;
      });

      mockQuizService.getQuestionsForNode.mockReturnValue(promise);

      const { result, unmount } = renderHook(() => useQuizQuestions('node123'));

      expect(result.current.loading).toBe(true);

      unmount();

      // Resolve after unmount
      resolvePromise!([]);

      // Wait a bit to ensure no state updates occur
      await new Promise(resolve => setTimeout(resolve, 10));

      // Should still be loading since component was unmounted
      expect(result.current.loading).toBe(true);
    });
  });

  describe('concurrent requests', () => {
    it('should handle overlapping requests correctly', async () => {
      let resolveFirst: (value: any) => void;
      let resolveSecond: (value: any) => void;

      const firstPromise = new Promise(resolve => {
        resolveFirst = resolve;
      });

      const secondPromise = new Promise(resolve => {
        resolveSecond = resolve;
      });

      mockQuizService.getQuestionsForNode
        .mockReturnValueOnce(firstPromise)
        .mockReturnValueOnce(secondPromise);

      const { result, rerender } = renderHook(
        ({ nodeId }) => useQuizQuestions(nodeId),
        { initialProps: { nodeId: 'node1' } }
      );

      // Start second request before first completes
      rerender({ nodeId: 'node2' });

      // Resolve first request (should be ignored)
      resolveFirst!([{ id: '1', node_id: 'node1', question: 'Q1', options: ['A'], correct: 0, explanation: 'E1' }]);

      // Resolve second request
      resolveSecond!([{ id: '2', node_id: 'node2', question: 'Q2', options: ['B'], correct: 0, explanation: 'E2' }]);

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Should have questions from second request only
      expect(result.current.questions[0]?.node_id).toBe('node2');
    });
  });
});