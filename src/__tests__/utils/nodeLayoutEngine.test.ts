import { layoutNodesWithCollisionDetection } from '../../utils/nodeLayoutEngine';
import { Node } from '../../types';

describe('nodeLayoutEngine', () => {
  describe('layoutNodesWithCollisionDetection', () => {
    const mockHierarchicalData = {
      foundation: {
        math: [
          {
            id: 'math1',
            name: 'Basic Math',
            domain: 'math',
            category: 'foundation',
            prereqs: [],
            difficulty: 1,
            points: 50,
            isParent: false
          },
          {
            id: 'math2',
            name: 'Advanced Math',
            domain: 'math',
            category: 'foundation',
            prereqs: ['math1'],
            difficulty: 2,
            points: 100,
            isParent: true,
            subnodes: [
              {
                id: 'math2-sub1',
                name: 'Calculus',
                domain: 'math',
                category: 'foundation',
                prereqs: [],
                difficulty: 3,
                points: 150,
                parentId: 'math2'
              }
            ]
          }
        ],
        science: [
          {
            id: 'sci1',
            name: 'Basic Science',
            domain: 'science',
            category: 'foundation',
            prereqs: [],
            difficulty: 1,
            points: 50,
            isParent: false
          }
        ]
      },
      advanced: [
        {
          id: 'adv1',
          name: 'Advanced Topic',
          domain: 'mixed',
          category: 'advanced',
          prereqs: ['math1', 'sci1'],
          difficulty: 4,
          points: 200,
          isParent: false
        }
      ]
    };

    it('should return nodes with positions', () => {
      const result = layoutNodesWithCollisionDetection(mockHierarchicalData);
      
      expect(result.nodes).toBeDefined();
      expect(result.nodes.length).toBeGreaterThan(0);
      expect(result.categoryLabels).toBeDefined();
    });

    it('should assign unique positions to each node', () => {
      const result = layoutNodesWithCollisionDetection(mockHierarchicalData);
      const positions = new Set();
      
      result.nodes.forEach(node => {
        expect(node.x).toBeDefined();
        expect(node.y).toBeDefined();
        expect(typeof node.x).toBe('number');
        expect(typeof node.y).toBe('number');
        
        const posKey = `${node.x},${node.y}`;
        expect(positions.has(posKey)).toBe(false);
        positions.add(posKey);
      });
    });

    it('should handle expanded nodes correctly', () => {
      const expandedNodes = new Set(['math2']);
      const result = layoutNodesWithCollisionDetection(mockHierarchicalData, expandedNodes);
      
      // Should include the subnode when parent is expanded
      const subnode = result.nodes.find(n => n.id === 'math2-sub1');
      expect(subnode).toBeDefined();
    });

    it('should not include subnodes when parent is not expanded', () => {
      const expandedNodes = new Set<string>();
      const result = layoutNodesWithCollisionDetection(mockHierarchicalData, expandedNodes);
      
      // Should not include the subnode when parent is not expanded
      const subnode = result.nodes.find(n => n.id === 'math2-sub1');
      expect(subnode).toBeUndefined();
    });

    it('should create category labels', () => {
      const result = layoutNodesWithCollisionDetection(mockHierarchicalData);
      
      expect(result.categoryLabels).toBeDefined();
      expect(result.categoryLabels['foundation']).toBeDefined();
      expect(result.categoryLabels['foundation'].name).toBe('FOUNDATION');
      expect(typeof result.categoryLabels['foundation'].y).toBe('number');
    });

    it('should handle null or undefined data gracefully', () => {
      const result1 = layoutNodesWithCollisionDetection(null);
      expect(result1.nodes).toEqual([]);
      expect(result1.categoryLabels).toEqual({});
      
      const result2 = layoutNodesWithCollisionDetection(undefined);
      expect(result2.nodes).toEqual([]);
      expect(result2.categoryLabels).toEqual({});
    });

    it('should handle empty data', () => {
      const result = layoutNodesWithCollisionDetection({});
      
      expect(result.nodes).toEqual([]);
      expect(result.categoryLabels).toEqual({});
    });

    it('should prevent node collisions', () => {
      const result = layoutNodesWithCollisionDetection(mockHierarchicalData);
      
      // Check that no two nodes overlap
      for (let i = 0; i < result.nodes.length; i++) {
        for (let j = i + 1; j < result.nodes.length; j++) {
          const node1 = result.nodes[i];
          const node2 = result.nodes[j];
          
          // Simple overlap check (nodes should be at least 120px apart horizontally or 140px vertically)
          const xOverlap = Math.abs(node1.x - node2.x) < 120;
          const yOverlap = Math.abs(node1.y - node2.y) < 140;
          
          // If nodes are close in one dimension, they should be separated in the other
          if (xOverlap && yOverlap) {
            // This should not happen with collision detection
            expect(xOverlap && yOverlap).toBe(false);
          }
        }
      }
    });

    it('should handle arrays within categories', () => {
      const dataWithArrays = {
        mastery: [
          {
            id: 'master1',
            name: 'Master Node',
            domain: 'mastery',
            category: 'mastery',
            prereqs: [],
            difficulty: 5,
            points: 500,
            isParent: false
          }
        ]
      };
      
      const result = layoutNodesWithCollisionDetection(dataWithArrays);
      
      expect(result.nodes.length).toBe(1);
      expect(result.nodes[0].id).toBe('master1');
    });

    it('should maintain consistent positioning across calls', () => {
      const result1 = layoutNodesWithCollisionDetection(mockHierarchicalData);
      const result2 = layoutNodesWithCollisionDetection(mockHierarchicalData);
      
      // Same input should produce same output
      expect(result1.nodes.length).toBe(result2.nodes.length);
      
      result1.nodes.forEach((node, index) => {
        expect(node.x).toBe(result2.nodes[index].x);
        expect(node.y).toBe(result2.nodes[index].y);
      });
    });

    it('should handle very large datasets without errors', () => {
      const largeData: any = {};
      
      // Create a large dataset
      for (let cat = 0; cat < 5; cat++) {
        largeData[`category${cat}`] = {};
        for (let dom = 0; dom < 5; dom++) {
          largeData[`category${cat}`][`domain${dom}`] = [];
          for (let node = 0; node < 10; node++) {
            largeData[`category${cat}`][`domain${dom}`].push({
              id: `node-${cat}-${dom}-${node}`,
              name: `Node ${cat}-${dom}-${node}`,
              domain: `domain${dom}`,
              category: `category${cat}`,
              prereqs: [],
              difficulty: 1,
              points: 50,
              isParent: false
            });
          }
        }
      }
      
      expect(() => {
        const result = layoutNodesWithCollisionDetection(largeData);
        expect(result.nodes.length).toBe(250); // 5 * 5 * 10
      }).not.toThrow();
    });

    it('should handle malformed node data gracefully', () => {
      const malformedData = {
        test: {
          badDomain: [
            {
              // Missing required fields
              id: 'bad1',
              name: 'Bad Node'
              // Missing: domain, category, prereqs, difficulty, points
            } as any
          ]
        }
      };
      
      expect(() => {
        layoutNodesWithCollisionDetection(malformedData);
      }).not.toThrow();
    });

    it('should handle circular references in data', () => {
      const circularData: any = {
        category: {
          domain: []
        }
      };
      
      // Create circular reference
      circularData.category.circular = circularData;
      
      expect(() => {
        layoutNodesWithCollisionDetection(circularData);
      }).not.toThrow();
    });
  });
});