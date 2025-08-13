import { getNodeState, createConnections, filterNodes } from '../../utils/nodeUtils';
import { Node, NodeState } from '../../types';

describe('nodeUtils', () => {
  const mockNodes: Node[] = [
    {
      id: 'node1',
      name: 'Node 1',
      domain: 'math',
      category: 'beginner',
      prereqs: [],
      difficulty: 1,
      points: 50,
      x: 0,
      y: 0
    },
    {
      id: 'node2',
      name: 'Node 2',
      domain: 'math',
      category: 'intermediate',
      prereqs: ['node1'],
      difficulty: 2,
      points: 100,
      x: 100,
      y: 100
    },
    {
      id: 'node3',
      name: 'Advanced Node',
      domain: 'science',
      category: 'advanced',
      prereqs: ['node1', 'node2'],
      difficulty: 3,
      points: 150,
      x: 200,
      y: 200
    }
  ];

  describe('getNodeState', () => {
    it('should return completed for conquered nodes', () => {
      const conqueredNodes = ['node1'];
      const state = getNodeState('node1', conqueredNodes, mockNodes);
      expect(state).toBe('completed');
    });

    it('should return locked for non-existent nodes', () => {
      const conqueredNodes: string[] = [];
      const state = getNodeState('nonexistent', conqueredNodes, mockNodes);
      expect(state).toBe('locked');
    });

    it('should return available for nodes with no prerequisites', () => {
      const conqueredNodes: string[] = [];
      const state = getNodeState('node1', conqueredNodes, mockNodes);
      expect(state).toBe('available');
    });

    it('should return available when all prerequisites are met', () => {
      const conqueredNodes = ['node1'];
      const state = getNodeState('node2', conqueredNodes, mockNodes);
      expect(state).toBe('available');
    });

    it('should return locked when prerequisites are not met', () => {
      const conqueredNodes: string[] = [];
      const state = getNodeState('node2', conqueredNodes, mockNodes);
      expect(state).toBe('locked');
    });

    it('should return locked when only some prerequisites are met', () => {
      const conqueredNodes = ['node1'];
      const state = getNodeState('node3', conqueredNodes, mockNodes);
      expect(state).toBe('locked');
    });
  });

  describe('createConnections', () => {
    it('should create connections based on prerequisites', () => {
      const connections = createConnections(mockNodes);
      
      expect(connections).toHaveLength(3);
      expect(connections).toContainEqual({ from: 'node1', to: 'node2' });
      expect(connections).toContainEqual({ from: 'node1', to: 'node3' });
      expect(connections).toContainEqual({ from: 'node2', to: 'node3' });
    });

    it('should handle nodes with no prerequisites', () => {
      const nodesWithoutPrereqs: Node[] = [
        {
          id: 'standalone',
          name: 'Standalone',
          domain: 'test',
          category: 'beginner',
          prereqs: [],
          difficulty: 1,
          points: 50,
          x: 0,
          y: 0
        }
      ];
      
      const connections = createConnections(nodesWithoutPrereqs);
      expect(connections).toHaveLength(0);
    });

    it('should handle invalid prerequisite references', () => {
      const nodesWithInvalidPrereqs: Node[] = [
        {
          id: 'node1',
          name: 'Node 1',
          domain: 'test',
          category: 'beginner',
          prereqs: ['nonexistent'],
          difficulty: 1,
          points: 50,
          x: 0,
          y: 0
        }
      ];
      
      const connections = createConnections(nodesWithInvalidPrereqs);
      expect(connections).toHaveLength(0);
    });
  });

  describe('filterNodes', () => {
    it('should return all nodes when no filters are applied', () => {
      const filtered = filterNodes(mockNodes, [], '', 'all');
      expect(filtered).toHaveLength(3);
      expect(filtered).toEqual(mockNodes);
    });

    it('should filter nodes by domain', () => {
      const filtered = filterNodes(mockNodes, ['math'], '', 'all');
      expect(filtered).toHaveLength(2);
      expect(filtered.every(node => node.domain === 'math')).toBe(true);
    });

    it('should filter nodes by multiple domains', () => {
      const filtered = filterNodes(mockNodes, ['math', 'science'], '', 'all');
      expect(filtered).toHaveLength(3);
    });

    it('should filter nodes by search term', () => {
      const filtered = filterNodes(mockNodes, [], 'advanced', 'all');
      expect(filtered).toHaveLength(1);
      expect(filtered[0].name).toBe('Advanced Node');
    });

    it('should filter nodes by search term case insensitive', () => {
      const filtered = filterNodes(mockNodes, [], 'ADVANCED', 'all');
      expect(filtered).toHaveLength(1);
      expect(filtered[0].name).toBe('Advanced Node');
    });

    it('should filter nodes by category', () => {
      const filtered = filterNodes(mockNodes, [], '', 'beginner');
      expect(filtered).toHaveLength(1);
      expect(filtered[0].category).toBe('beginner');
    });

    it('should apply multiple filters simultaneously', () => {
      const filtered = filterNodes(mockNodes, ['math'], 'node', 'intermediate');
      expect(filtered).toHaveLength(1);
      expect(filtered[0].id).toBe('node2');
    });

    it('should return empty array when no nodes match filters', () => {
      const filtered = filterNodes(mockNodes, ['nonexistent'], '', 'all');
      expect(filtered).toHaveLength(0);
    });

    it('should handle empty nodes array', () => {
      const filtered = filterNodes([], ['math'], 'test', 'all');
      expect(filtered).toHaveLength(0);
    });

    it('should handle null/undefined search terms gracefully', () => {
      const filtered1 = filterNodes(mockNodes, [], null as any, 'all');
      const filtered2 = filterNodes(mockNodes, [], undefined as any, 'all');
      expect(filtered1).toHaveLength(3);
      expect(filtered2).toHaveLength(3);
    });

    it('should handle special characters in search terms', () => {
      const nodesWithSpecialChars: Node[] = [
        {
          id: 'special',
          name: 'Node with (parentheses)',
          domain: 'test',
          category: 'beginner',
          prereqs: [],
          difficulty: 1,
          points: 50,
          x: 0,
          y: 0
        }
      ];
      
      const filtered = filterNodes(nodesWithSpecialChars, [], '(parentheses)', 'all');
      expect(filtered).toHaveLength(1);
    });
  });

  describe('Error handling', () => {
    it('should handle malformed node data gracefully', () => {
      const malformedNodes = [
        {
          id: 'valid',
          name: 'Valid Node',
          domain: 'test',
          category: 'beginner',
          prereqs: [],
          difficulty: 1,
          points: 50,
          x: 0,
          y: 0
        },
        {
          id: null,
          name: undefined,
          domain: '',
          category: null,
          prereqs: null,
          x: 'invalid',
          y: 'invalid'
        } as any
      ];

      expect(() => {
        getNodeState('valid', [], malformedNodes);
      }).not.toThrow();

      expect(() => {
        createConnections(malformedNodes);
      }).not.toThrow();

      expect(() => {
        filterNodes(malformedNodes, ['test'], '', 'all');
      }).not.toThrow();
    });

    it('should handle extremely large datasets', () => {
      const largeNodeSet: Node[] = Array.from({ length: 1000 }, (_, i) => ({
        id: `node${i}`,
        name: `Node ${i}`,
        domain: `domain${i % 10}`,
        category: 'beginner',
        prereqs: i > 0 ? [`node${i - 1}`] : [],
        difficulty: 1,
        points: 50,
        x: i,
        y: i
      }));

      const start = performance.now();
      const connections = createConnections(largeNodeSet);
      const end = performance.now();

      expect(connections).toHaveLength(999); // n-1 connections
      expect(end - start).toBeLessThan(1000); // Should complete within 1 second
    });

    it('should handle circular dependencies without infinite loops', () => {
      const circularNodes: Node[] = [
        {
          id: 'a',
          name: 'Node A',
          domain: 'test',
          category: 'beginner',
          prereqs: ['b'],
          difficulty: 1,
          points: 50,
          x: 0,
          y: 0
        },
        {
          id: 'b',
          name: 'Node B',
          domain: 'test',
          category: 'beginner',
          prereqs: ['a'],
          difficulty: 1,
          points: 50,
          x: 100,
          y: 0
        }
      ];

      expect(() => {
        const connections = createConnections(circularNodes);
        expect(connections).toHaveLength(2);
      }).not.toThrow();

      expect(() => {
        const state = getNodeState('a', [], circularNodes);
        expect(state).toBe('locked');
      }).not.toThrow();
    });
  });
});