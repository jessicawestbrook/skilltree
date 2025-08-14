import {
  getNodeState,
  createHierarchicalConnections,
  filterHierarchicalNodes,
  toggleNodeExpansion,
  getVisibleNodes,
  calculateHierarchicalProgress
} from '../../utils/hierarchicalNodeUtils';
import { Node } from '../../types';

describe('hierarchicalNodeUtils', () => {
  const mockNodes: Node[] = [
    {
      id: 'parent1',
      name: 'Parent 1',
      domain: 'math',
      prereqs: [],
      difficulty: 1,
      points: 50,
      x: 0,
      y: 0
    },
    {
      id: 'child1',
      name: 'Child 1',
      domain: 'math',
      prereqs: [],
      parentId: 'parent1',
      difficulty: 1,
      points: 50,
      x: 50,
      y: 50
    },
    {
      id: 'child2',
      name: 'Child 2',
      domain: 'math',
      prereqs: ['child1'],
      parentId: 'parent1',
      difficulty: 2,
      points: 100,
      x: 100,
      y: 50
    },
    {
      id: 'parent2',
      name: 'Parent 2',
      domain: 'science',
      prereqs: ['parent1'],
      difficulty: 3,
      points: 150,
      x: 200,
      y: 0
    }
  ];

  describe('createHierarchicalConnections', () => {
    it('should create connections for prerequisites and parent-child relationships', () => {
      const connections = createHierarchicalConnections(mockNodes);
      
      expect(connections).toContainEqual({ from: 'child1', to: 'child2' });
      expect(connections).toContainEqual({ from: 'parent1', to: 'parent2' });
      expect(connections).toContainEqual({ from: 'parent1', to: 'child1' });
      expect(connections).toContainEqual({ from: 'parent1', to: 'child2' });
    });

    it('should handle nodes without parents or prerequisites', () => {
      const simpleNodes: Node[] = [
        {
          id: 'standalone',
          name: 'Standalone',
          domain: 'test',
          prereqs: [],
          difficulty: 1,
          points: 50,
          x: 0,
          y: 0
        }
      ];
      
      const connections = createHierarchicalConnections(simpleNodes);
      expect(connections).toHaveLength(0);
    });
  });

  describe('filterHierarchicalNodes', () => {
    it('should filter out collapsed subnodes', () => {
      const expandedNodes = new Set<string>();
      const filtered = filterHierarchicalNodes(mockNodes, [], '', 'all', expandedNodes);
      
      // Should only include top-level nodes
      expect(filtered).toHaveLength(2);
      expect(filtered.map(n => n.id)).toEqual(['parent1', 'parent2']);
    });

    it('should include subnodes when parent is expanded', () => {
      const expandedNodes = new Set(['parent1']);
      const filtered = filterHierarchicalNodes(mockNodes, [], '', 'all', expandedNodes);
      
      expect(filtered).toHaveLength(4);
      expect(filtered.map(n => n.id)).toEqual(['parent1', 'child1', 'child2', 'parent2']);
    });

    it('should apply domain filters', () => {
      const expandedNodes = new Set(['parent1']);
      const filtered = filterHierarchicalNodes(mockNodes, ['math'], '', 'all', expandedNodes);
      
      expect(filtered).toHaveLength(3);
      expect(filtered.every(node => node.domain === 'math')).toBe(true);
    });

    it('should apply search filters', () => {
      const expandedNodes = new Set(['parent1']);
      const filtered = filterHierarchicalNodes(mockNodes, [], 'child', 'all', expandedNodes);
      
      expect(filtered).toHaveLength(2);
      expect(filtered.every(node => node.name.toLowerCase().includes('child'))).toBe(true);
    });

  });

  describe('toggleNodeExpansion', () => {
    it('should add node to expanded set when not present', () => {
      const expandedNodes = new Set<string>();
      const result = toggleNodeExpansion('parent1', expandedNodes);
      
      expect(result.has('parent1')).toBe(true);
      expect(result.size).toBe(1);
    });

    it('should remove node from expanded set when present', () => {
      const expandedNodes = new Set(['parent1']);
      const result = toggleNodeExpansion('parent1', expandedNodes);
      
      expect(result.has('parent1')).toBe(false);
      expect(result.size).toBe(0);
    });

    it('should not modify the original set', () => {
      const expandedNodes = new Set(['parent1']);
      const result = toggleNodeExpansion('parent2', expandedNodes);
      
      expect(expandedNodes.has('parent2')).toBe(false);
      expect(result.has('parent2')).toBe(true);
      expect(expandedNodes !== result).toBe(true);
    });
  });

  describe('getVisibleNodes', () => {
    it('should return only top-level nodes when nothing is expanded', () => {
      const expandedNodes = new Set<string>();
      const visible = getVisibleNodes(mockNodes, expandedNodes);
      
      expect(visible).toHaveLength(2);
      expect(visible.map(n => n.id)).toEqual(['parent1', 'parent2']);
    });

    it('should include subnodes when parent is expanded', () => {
      const expandedNodes = new Set(['parent1']);
      const visible = getVisibleNodes(mockNodes, expandedNodes);
      
      expect(visible).toHaveLength(4);
      expect(visible.map(n => n.id)).toEqual(['parent1', 'child1', 'child2', 'parent2']);
    });

    it('should handle multiple expanded parents', () => {
      const nodesWithMultipleParents: Node[] = [
        ...mockNodes,
        {
          id: 'child3',
          name: 'Child 3',
          domain: 'science',
          prereqs: [],
          parentId: 'parent2',
          difficulty: 3,
          points: 150,
          x: 250,
          y: 50
        }
      ];
      
      const expandedNodes = new Set(['parent1', 'parent2']);
      const visible = getVisibleNodes(nodesWithMultipleParents, expandedNodes);
      
      expect(visible).toHaveLength(5);
      expect(visible.map(n => n.id)).toEqual(['parent1', 'child1', 'child2', 'parent2', 'child3']);
    });
  });

  describe('calculateHierarchicalProgress', () => {
    it('should calculate progress based on visible nodes', () => {
      const conqueredNodes = ['parent1', 'child1'];
      const expandedNodes = new Set(['parent1']);
      
      const progress = calculateHierarchicalProgress(mockNodes, conqueredNodes, expandedNodes);
      
      // 2 conquered out of 4 visible nodes = 50%
      expect(progress).toBe(50);
    });

    it('should return 0 when no nodes are visible', () => {
      const conqueredNodes: string[] = [];
      const expandedNodes = new Set<string>();
      const emptyNodes: Node[] = [];
      
      const progress = calculateHierarchicalProgress(emptyNodes, conqueredNodes, expandedNodes);
      expect(progress).toBe(0);
    });

    it('should return 100 when all visible nodes are conquered', () => {
      const conqueredNodes = ['parent1', 'parent2'];
      const expandedNodes = new Set<string>();
      
      const progress = calculateHierarchicalProgress(mockNodes, conqueredNodes, expandedNodes);
      expect(progress).toBe(100);
    });

    it('should handle partial conquest of expanded nodes', () => {
      const conqueredNodes = ['parent1'];
      const expandedNodes = new Set(['parent1']);
      
      const progress = calculateHierarchicalProgress(mockNodes, conqueredNodes, expandedNodes);
      
      // 1 conquered out of 4 visible nodes = 25%
      expect(progress).toBe(25);
    });
  });
});