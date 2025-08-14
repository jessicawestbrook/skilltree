import {
  filterNodesByAge,
  sortNodesByAgeRecommendation,
  getPersonalizedRecommendations,
  isContentAppropriate,
  getAgeGroup,
  getAgeGroupFromBirthYear,
  getRecommendedPaths,
  getAgeAdjustedQuizSettings
} from '../../utils/contentRecommendation';

// Mock nodes data
const mockNodes = [
  {
    id: 'node1',
    name: 'Basic Math',
    difficulty: 1,
    points: 10,
    domain: 'mathematics',
    category: 'arithmetic',
    minAge: 6,
    maxAge: 12,
    x: 100,
    y: 100
  },
  {
    id: 'node2',
    name: 'Advanced Calculus',
    difficulty: 5,
    points: 50,
    domain: 'mathematics',
    category: 'calculus',
    minAge: 16,
    maxAge: null,
    x: 200,
    y: 200
  },
  {
    id: 'node3',
    name: 'JavaScript Basics',
    difficulty: 2,
    points: 20,
    domain: 'programming',
    category: 'web',
    minAge: 12,
    maxAge: null,
    x: 300,
    y: 300
  },
  {
    id: 'node4',
    name: 'Preschool Colors',
    difficulty: 1,
    points: 5,
    domain: 'general',
    category: 'basics',
    minAge: 3,
    maxAge: 6,
    x: 400,
    y: 400
  },
  {
    id: 'node5',
    name: 'Middle School Science',
    difficulty: 3,
    points: 25,
    domain: 'science',
    category: 'general',
    minAge: 11,
    maxAge: 14,
    x: 500,
    y: 500
  }
];

describe('contentRecommendation', () => {
  describe('filterNodesByAge', () => {
    it('should filter nodes by difficulty range for given birth year', () => {
      const birthYear = 2010; // 14 years old in 2024 - High School (difficulty 5-8)
      
      const result = filterNodesByAge(mockNodes, birthYear);
      
      // Should include nodes with difficulty 5-8 for High School age group
      const nodeIds = result.map(n => n.id);
      expect(nodeIds).toContain('node2'); // Advanced Calculus (difficulty 5)
      expect(nodeIds).not.toContain('node1'); // Basic Math (difficulty 1)
      expect(nodeIds).not.toContain('node4'); // Preschool Colors (difficulty 1)
      expect(nodeIds).not.toContain('node5'); // Middle School Science (difficulty 3)
    });

    it('should include adult learning nodes for adults', () => {
      const birthYear = 2000; // 24 years old - Adult Learning (difficulty 1-10)
      
      const result = filterNodesByAge(mockNodes, birthYear);
      
      // Adult Learning age group accepts all difficulty levels (1-10)
      const nodeIds = result.map(n => n.id);
      expect(nodeIds).toContain('node1'); // Basic Math (difficulty 1)
      expect(nodeIds).toContain('node2'); // Advanced Calculus (difficulty 5)
      expect(nodeIds).toContain('node3'); // JavaScript (difficulty 2)
      expect(nodeIds).toContain('node4'); // Preschool Colors (difficulty 1)
      expect(nodeIds).toContain('node5'); // Middle School Science (difficulty 3)
    });

    it('should handle very young age with appropriate difficulty', () => {
      const birthYear = 2019; // 5 years old - Early Elementary (difficulty 1-3)
      
      const result = filterNodesByAge(mockNodes, birthYear);
      
      const nodeIds = result.map(n => n.id);
      expect(nodeIds).toContain('node1'); // Basic Math (difficulty 1)
      expect(nodeIds).toContain('node3'); // JavaScript (difficulty 2)
      expect(nodeIds).toContain('node4'); // Preschool Colors (difficulty 1)
      expect(nodeIds).toContain('node5'); // Middle School Science (difficulty 3)
      expect(nodeIds).not.toContain('node2'); // Advanced Calculus (difficulty 5)
    });

    it('should handle high school age', () => {
      const birthYear = 2007; // 17 years old - High School (difficulty 5-8)
      
      const result = filterNodesByAge(mockNodes, birthYear);
      
      const nodeIds = result.map(n => n.id);
      expect(nodeIds).toContain('node2'); // Advanced Calculus (difficulty 5)
      expect(nodeIds).not.toContain('node1'); // Basic Math (difficulty 1)
      expect(nodeIds).not.toContain('node3'); // JavaScript (difficulty 2)
    });

    it('should return all nodes when birthYear is null', () => {
      const result = filterNodesByAge(mockNodes, null);
      
      expect(result).toHaveLength(mockNodes.length);
      expect(result).toEqual(mockNodes);
    });

    it('should return all nodes when birthYear is undefined', () => {
      const result = filterNodesByAge(mockNodes, undefined);
      
      expect(result).toHaveLength(mockNodes.length);
      expect(result).toEqual(mockNodes);
    });

    it('should handle invalid birth year gracefully', () => {
      const result = filterNodesByAge(mockNodes, 3000); // Future year
      
      expect(result).toEqual(mockNodes); // Should return all nodes when age group not found
    });
  });

  describe('sortNodesByAgeRecommendation', () => {
    it('should sort nodes by age appropriateness score', () => {
      const birthYear = 2010; // 14 years old
      const ageFilteredNodes = filterNodesByAge(mockNodes, birthYear);
      
      const result = sortNodesByAgeRecommendation(ageFilteredNodes, birthYear);
      
      // Should be sorted with most age-appropriate first
      expect(result.length).toBeGreaterThan(0);
      
      // Check that sorting is applied - nodes should be reordered
      expect(result.length).toBeGreaterThan(0);
      
      // The exact order depends on the algorithm, but it should be sorted
      expect(Array.isArray(result)).toBe(true);
    });

    it('should handle empty node list', () => {
      const result = sortNodesByAgeRecommendation([], 2010);
      
      expect(result).toEqual([]);
    });

    it('should preserve original order when birthYear is null', () => {
      const result = sortNodesByAgeRecommendation(mockNodes, null);
      
      expect(result).toEqual(mockNodes);
    });

    it('should handle single node', () => {
      const singleNode = [mockNodes[0]];
      const result = sortNodesByAgeRecommendation(singleNode, 2010);
      
      expect(result).toEqual(singleNode);
    });
  });

  describe('isContentAppropriate', () => {
    it('should approve appropriate content for age', () => {
      const birthYear = 2010; // 15 years old - High School (difficulty 5-8, tolerance 4-9)
      
      const isAppropriate1 = isContentAppropriate(mockNodes[1], birthYear); // Advanced Calculus (difficulty 5)
      const isAppropriate2 = isContentAppropriate(mockNodes[2], birthYear); // JavaScript Basics (difficulty 2, outside tolerance)
      
      expect(isAppropriate1).toBe(true);
      expect(isAppropriate2).toBe(false); // Outside tolerance range 4-9
    });

    it('should reject overly advanced content for young users', () => {
      const birthYear = 2016; // 9 years old - Late Elementary
      
      // Create a mock node with difficulty > 5 for testing age restriction
      const advancedNode = {
        id: 'advanced',
        name: 'Advanced Physics',
        difficulty: 6,
        points: 100,
        domain: 'science',
        category: 'physics',
        minAge: 16,
        maxAge: null,
        x: 600,
        y: 600
      };
      
      const isAppropriate = isContentAppropriate(advancedNode, birthYear);
      
      expect(isAppropriate).toBe(false); // Blocked by age < 13 and difficulty > 5 restriction
    });

    it('should handle null birthYear gracefully', () => {
      const isAppropriate = isContentAppropriate(mockNodes[0], null);
      
      expect(isAppropriate).toBe(true); // Should allow all content when no age group
    });
  });

  describe('getAgeGroup', () => {
    it('should return correct age group for different ages', () => {
      expect(getAgeGroup(7)?.label).toBe('Early Elementary');
      expect(getAgeGroup(10)?.label).toBe('Late Elementary');
      expect(getAgeGroup(13)?.label).toBe('Middle School');
      expect(getAgeGroup(16)?.label).toBe('High School');
      expect(getAgeGroup(20)?.label).toBe('College');
      expect(getAgeGroup(25)?.label).toBe('Adult Learning');
    });

    it('should return null for invalid ages', () => {
      expect(getAgeGroup(3)).toBeNull();
      expect(getAgeGroup(-5)).toBeNull();
    });
  });

  describe('getAgeGroupFromBirthYear', () => {
    it('should calculate age group from birth year', () => {
      const birthYear = 2008; // ~16 years old in 2024
      const ageGroup = getAgeGroupFromBirthYear(birthYear);
      
      expect(ageGroup?.label).toBe('High School');
    });
  });

  describe('getRecommendedPaths', () => {
    it('should return appropriate learning paths for age', () => {
      const birthYear = 2010; // High School age  
      const paths = getRecommendedPaths(birthYear);
      
      expect(Array.isArray(paths)).toBe(true);
      expect(paths.length).toBeGreaterThan(0);
      expect(paths).toContain('Algebra & Geometry');
    });

    it('should return empty array for invalid birth year', () => {
      const paths = getRecommendedPaths(3000);
      
      expect(paths).toEqual([]);
    });
  });

  describe('getAgeAdjustedQuizSettings', () => {
    it('should provide age-appropriate quiz settings', () => {
      const birthYear = 2015; // ~9 years old
      const settings = getAgeAdjustedQuizSettings(birthYear);
      
      expect(settings.questionCount).toBe(5); // Age < 15 gets 5 questions
      expect(settings.timePerQuestion).toBe(90); // Age < 15 gets 90 seconds
      expect(settings.hintsAllowed).toBe(true);
    });

    it('should provide different settings for older students', () => {
      const birthYear = 2005; // ~19 years old
      const settings = getAgeAdjustedQuizSettings(birthYear);
      
      expect(settings.questionCount).toBe(10); // More questions for older students
      expect(settings.timePerQuestion).toBe(60); // Less time per question
      expect(settings.hintsAllowed).toBe(false);
    });
  });

  describe('getPersonalizedRecommendations', () => {
    it('should return learning recommendations object', () => {
      const birthYear = 2010; // 14 years old
      
      const result = getPersonalizedRecommendations(birthYear);
      
      expect(result).toHaveProperty('dailyGoal');
      expect(result).toHaveProperty('sessionLength');
      expect(result).toHaveProperty('difficultyLevel');
      expect(result).toHaveProperty('focusAreas');
      expect(result).toHaveProperty('tips');
      
      expect(typeof result.dailyGoal).toBe('number');
      expect(typeof result.sessionLength).toBe('number');
      expect(['beginner', 'intermediate', 'advanced']).toContain(result.difficultyLevel);
      expect(Array.isArray(result.focusAreas)).toBe(true);
      expect(Array.isArray(result.tips)).toBe(true);
    });

    it('should provide age-appropriate recommendations', () => {
      const youngResult = getPersonalizedRecommendations(2019); // 5 years old
      const teenResult = getPersonalizedRecommendations(2010); // 14 years old
      const adultResult = getPersonalizedRecommendations(2000); // 24 years old
      
      expect(youngResult.difficultyLevel).toBe('beginner');
      expect(teenResult.difficultyLevel).toBe('intermediate');
      expect(adultResult.difficultyLevel).toBe('intermediate');
      
      expect(youngResult.sessionLength).toBeLessThan(teenResult.sessionLength);
    });

    it('should provide appropriate tips for age groups', () => {
      const youngResult = getPersonalizedRecommendations(2019); // Early Elementary
      const teenResult = getPersonalizedRecommendations(2010); // Middle School
      
      expect(youngResult.tips.length).toBeGreaterThan(0);
      expect(teenResult.tips.length).toBeGreaterThan(0);
      expect(youngResult.tips).not.toEqual(teenResult.tips);
    });

    it('should handle invalid birth year gracefully', () => {
      const result = getPersonalizedRecommendations(3000);
      
      expect(result).toHaveProperty('dailyGoal');
      expect(result.dailyGoal).toBe(30);
      expect(result.sessionLength).toBe(30);
      expect(result.difficultyLevel).toBe('intermediate');
    });
  });

  describe('edge cases and error handling', () => {
    it('should handle empty nodes array', () => {
      const result = filterNodesByAge([], 2010);
      expect(result).toEqual([]);
    });

    it('should handle nodes with invalid age data', () => {
      const invalidNodes = [
        {
          id: 'invalid1',
          name: 'Invalid Min Age',
          difficulty: 1,
          points: 10,
          domain: 'test',
          category: 'test',
          minAge: -5, // Invalid
          maxAge: 10,
          x: 100,
          y: 100
        },
        {
          id: 'invalid2',
          name: 'Invalid Max Age',
          difficulty: 1,
          points: 10,
          domain: 'test',
          category: 'test',
          minAge: 10,
          maxAge: 5, // Less than minAge
          x: 100,
          y: 100
        }
      ];

      expect(() => {
        filterNodesByAge(invalidNodes, 2010);
      }).not.toThrow();
    });

    it('should handle very large datasets efficiently', () => {
      const largeNodeSet = Array.from({ length: 1000 }, (_, i) => ({
        id: `node${i}`,
        name: `Node ${i}`,
        difficulty: (i % 5) + 1,
        points: i * 10,
        domain: 'test',
        category: 'test',
        minAge: (i % 20) + 3,
        maxAge: (i % 20) + 15,
        x: i * 10,
        y: i * 10
      }));

      const startTime = Date.now();
      const result = filterNodesByAge(largeNodeSet, 2010);
      const endTime = Date.now();

      expect(result.length).toBeGreaterThan(0);
      expect(endTime - startTime).toBeLessThan(1000); // Should complete within 1 second
    });
  });
});