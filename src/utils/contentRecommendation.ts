import { Node } from '../types';
import { GradeLevel, Subject, assignGradeLevel, analyzeContent, validateGradeLevelAppropriate } from './gradeLevelAnalysis';

export interface AgeGroup {
  minAge: number;
  maxAge: number;
  label: string;
  difficultyRange: [number, number];
  recommendedDomains: string[];
  maxSessionMinutes: number;
}

// Define age groups with their characteristics
export const AGE_GROUPS: AgeGroup[] = [
  {
    minAge: 5,
    maxAge: 8,
    label: 'Early Elementary',
    difficultyRange: [1, 3],
    recommendedDomains: ['reading', 'math-basics', 'science-discovery', 'art', 'music'],
    maxSessionMinutes: 20
  },
  {
    minAge: 9,
    maxAge: 11,
    label: 'Late Elementary',
    difficultyRange: [2, 4],
    recommendedDomains: ['math', 'science', 'history', 'geography', 'reading', 'writing'],
    maxSessionMinutes: 30
  },
  {
    minAge: 12,
    maxAge: 14,
    label: 'Middle School',
    difficultyRange: [3, 6],
    recommendedDomains: ['algebra', 'biology', 'chemistry', 'world-history', 'literature', 'coding'],
    maxSessionMinutes: 45
  },
  {
    minAge: 15,
    maxAge: 18,
    label: 'High School',
    difficultyRange: [5, 8],
    recommendedDomains: ['advanced-math', 'physics', 'chemistry', 'biology', 'computer-science', 'economics'],
    maxSessionMinutes: 60
  },
  {
    minAge: 19,
    maxAge: 22,
    label: 'College',
    difficultyRange: [6, 9],
    recommendedDomains: ['calculus', 'engineering', 'computer-science', 'philosophy', 'economics', 'research'],
    maxSessionMinutes: 90
  },
  {
    minAge: 23,
    maxAge: 120,
    label: 'Adult Learning',
    difficultyRange: [1, 10],
    recommendedDomains: ['all'],
    maxSessionMinutes: 120
  }
];

/**
 * Get the age group for a given age
 */
export function getAgeGroup(age: number): AgeGroup | null {
  return AGE_GROUPS.find(group => age >= group.minAge && age <= group.maxAge) || null;
}

/**
 * Get the age group from birth year
 */
export function getAgeGroupFromBirthYear(birthYear: number): AgeGroup | null {
  const currentYear = new Date().getFullYear();
  const age = currentYear - birthYear;
  return getAgeGroup(age);
}

/**
 * Filter nodes based on age-appropriate difficulty
 */
export function filterNodesByAge(nodes: Node[], birthYear: number): Node[] {
  const ageGroup = getAgeGroupFromBirthYear(birthYear);
  if (!ageGroup) return nodes;

  const [minDifficulty, maxDifficulty] = ageGroup.difficultyRange;
  
  return nodes.filter(node => 
    node.difficulty >= minDifficulty && 
    node.difficulty <= maxDifficulty
  );
}

/**
 * Sort nodes by age-appropriate recommendations
 */
export function sortNodesByAgeRecommendation(nodes: Node[], birthYear: number): Node[] {
  const ageGroup = getAgeGroupFromBirthYear(birthYear);
  if (!ageGroup) return nodes;

  const [minDifficulty, maxDifficulty] = ageGroup.difficultyRange;
  const optimalDifficulty = (minDifficulty + maxDifficulty) / 2;

  return [...nodes].sort((a, b) => {
    // Prioritize recommended domains
    const aIsRecommended = ageGroup.recommendedDomains.includes('all') || 
                          ageGroup.recommendedDomains.includes(a.domain);
    const bIsRecommended = ageGroup.recommendedDomains.includes('all') || 
                          ageGroup.recommendedDomains.includes(b.domain);
    
    if (aIsRecommended && !bIsRecommended) return -1;
    if (!aIsRecommended && bIsRecommended) return 1;

    // Sort by distance from optimal difficulty
    const aDiff = Math.abs(a.difficulty - optimalDifficulty);
    const bDiff = Math.abs(b.difficulty - optimalDifficulty);
    
    return aDiff - bDiff;
  });
}

/**
 * Get recommended learning paths based on age
 */
export function getRecommendedPaths(birthYear: number): string[] {
  const ageGroup = getAgeGroupFromBirthYear(birthYear);
  if (!ageGroup) return [];

  const pathRecommendations: Record<string, string[]> = {
    'Early Elementary': ['Reading Fundamentals', 'Math Basics', 'Science Explorer'],
    'Late Elementary': ['Math Foundations', 'Science Discovery', 'History Adventures'],
    'Middle School': ['Pre-Algebra Path', 'Life Science', 'World History', 'Coding Basics'],
    'High School': ['Algebra & Geometry', 'Biology & Chemistry', 'Computer Science', 'College Prep'],
    'College': ['Advanced Mathematics', 'Engineering Basics', 'Research Methods'],
    'Adult Learning': ['Professional Development', 'Technical Skills', 'Personal Growth']
  };

  return pathRecommendations[ageGroup.label] || [];
}

/**
 * Get personalized learning recommendations
 */
export interface LearningRecommendation {
  dailyGoal: number;
  sessionLength: number;
  difficultyLevel: 'beginner' | 'intermediate' | 'advanced';
  focusAreas: string[];
  tips: string[];
}

export function getPersonalizedRecommendations(birthYear: number): LearningRecommendation {
  const ageGroup = getAgeGroupFromBirthYear(birthYear);
  
  if (!ageGroup) {
    return {
      dailyGoal: 30,
      sessionLength: 30,
      difficultyLevel: 'intermediate',
      focusAreas: [],
      tips: []
    };
  }

  const [minDiff, maxDiff] = ageGroup.difficultyRange;
  let difficultyLevel: 'beginner' | 'intermediate' | 'advanced' = 'intermediate';
  
  if (maxDiff <= 3) difficultyLevel = 'beginner';
  else if (minDiff >= 6) difficultyLevel = 'advanced';

  const tips = {
    'Early Elementary': [
      'Keep sessions short and fun',
      'Use visual learning aids',
      'Celebrate small victories',
      'Include breaks for physical activity'
    ],
    'Late Elementary': [
      'Encourage curiosity and questions',
      'Mix different subjects in each session',
      'Use real-world examples',
      'Set achievable daily goals'
    ],
    'Middle School': [
      'Foster independent learning',
      'Connect topics to interests',
      'Encourage peer collaboration',
      'Build study habits'
    ],
    'High School': [
      'Focus on college preparation',
      'Develop critical thinking',
      'Practice time management',
      'Explore career interests'
    ],
    'College': [
      'Deep dive into specializations',
      'Build professional skills',
      'Network with peers',
      'Apply knowledge practically'
    ],
    'Adult Learning': [
      'Set specific career goals',
      'Learn at your own pace',
      'Focus on practical applications',
      'Balance learning with responsibilities'
    ]
  };

  return {
    dailyGoal: Math.min(ageGroup.maxSessionMinutes, 60),
    sessionLength: ageGroup.maxSessionMinutes,
    difficultyLevel,
    focusAreas: ageGroup.recommendedDomains.slice(0, 3),
    tips: tips[ageGroup.label] || []
  };
}

/**
 * Check if content is appropriate for age
 */
export function isContentAppropriate(node: Node, birthYear: number): boolean {
  const ageGroup = getAgeGroupFromBirthYear(birthYear);
  if (!ageGroup) return true; // If no age group, allow all content

  const [minDifficulty, maxDifficulty] = ageGroup.difficultyRange;
  
  // Check if difficulty is within range
  if (node.difficulty < minDifficulty - 1 || node.difficulty > maxDifficulty + 1) {
    return false;
  }

  // For younger groups, be more restrictive with advanced content
  const age = new Date().getFullYear() - birthYear;
  if (age < 13 && node.difficulty > 5) {
    return false;
  }

  return true;
}

/**
 * Adjust quiz difficulty based on age
 */
export function getAgeAdjustedQuizSettings(birthYear: number) {
  const ageGroup = getAgeGroupFromBirthYear(birthYear);
  if (!ageGroup) {
    return {
      questionCount: 5,
      timePerQuestion: 60,
      hintsAllowed: true,
      showExplanations: true
    };
  }

  const age = new Date().getFullYear() - birthYear;

  return {
    questionCount: age < 10 ? 3 : age < 15 ? 5 : 10,
    timePerQuestion: age < 10 ? 120 : age < 15 ? 90 : 60,
    hintsAllowed: age < 15,
    showExplanations: true,
    adaptiveDifficulty: age >= 12
  };
}

/**
 * Convert age to grade level approximation
 */
function ageToGradeLevel(age: number): GradeLevel | null {
  if (age >= 8 && age <= 9) return 3;
  if (age >= 9 && age <= 10) return 4;
  if (age >= 10 && age <= 11) return 5;
  if (age >= 11 && age <= 12) return 6;
  if (age >= 12 && age <= 13) return 7;
  if (age >= 13 && age <= 14) return 8;
  if (age >= 14 && age <= 15) return 9;
  if (age >= 15 && age <= 16) return 10;
  if (age >= 16 && age <= 17) return 11;
  if (age >= 17 && age <= 18) return 12;
  return null;
}

/**
 * Convert birth year to grade level
 */
export function birthYearToGradeLevel(birthYear: number): GradeLevel | null {
  const currentYear = new Date().getFullYear();
  const age = currentYear - birthYear;
  return ageToGradeLevel(age);
}

/**
 * Filter nodes by grade level appropriateness
 */
export function filterNodesByGradeLevel(nodes: Node[], targetGrade: GradeLevel, tolerance: number = 1): Node[] {
  return nodes.filter(node => {
    // If node already has a grade level assigned, use it
    if (node.gradeLevel) {
      const gradeDiff = Math.abs(node.gradeLevel - targetGrade);
      return gradeDiff <= tolerance;
    }
    
    // Otherwise, analyze the content to determine grade level
    const validation = validateGradeLevelAppropriate(node, targetGrade, tolerance);
    return validation.appropriate;
  });
}

/**
 * Filter nodes by grade level based on birth year
 */
export function filterNodesByBirthYearGradeLevel(nodes: Node[], birthYear: number, tolerance: number = 1): Node[] {
  const gradeLevel = birthYearToGradeLevel(birthYear);
  if (!gradeLevel) return nodes; // If we can't determine grade level, return all nodes
  
  return filterNodesByGradeLevel(nodes, gradeLevel, tolerance);
}

/**
 * Sort nodes by grade level appropriateness
 */
export function sortNodesByGradeLevel(nodes: Node[], targetGrade: GradeLevel): Node[] {
  return [...nodes].sort((a, b) => {
    // Get grade levels for both nodes
    const gradeA = a.gradeLevel || assignGradeLevel(a).gradeLevel;
    const gradeB = b.gradeLevel || assignGradeLevel(b).gradeLevel;
    
    // Calculate distance from target grade
    const distanceA = Math.abs(gradeA - targetGrade);
    const distanceB = Math.abs(gradeB - targetGrade);
    
    // Sort by distance (closer is better)
    if (distanceA !== distanceB) {
      return distanceA - distanceB;
    }
    
    // If same distance, prefer the one that's slightly easier
    return gradeA - gradeB;
  });
}

/**
 * Enhanced recommendation system that combines age and grade level filtering
 */
export interface EnhancedRecommendationOptions {
  birthYear?: number;
  gradeLevel?: GradeLevel;
  subject?: Subject;
  tolerance?: number; // Grade level tolerance
  maxResults?: number;
  prioritizeStandards?: boolean; // Prioritize content aligned with educational standards
}

export function getEnhancedRecommendations(
  nodes: Node[], 
  options: EnhancedRecommendationOptions = {}
): Node[] {
  let filteredNodes = [...nodes];
  const {
    birthYear,
    gradeLevel: targetGrade,
    subject,
    tolerance = 1,
    maxResults = 20,
    prioritizeStandards = true
  } = options;

  // Determine target grade level
  let effectiveGradeLevel = targetGrade;
  if (!effectiveGradeLevel && birthYear) {
    effectiveGradeLevel = birthYearToGradeLevel(birthYear);
  }

  // Apply grade level filtering
  if (effectiveGradeLevel) {
    filteredNodes = filterNodesByGradeLevel(filteredNodes, effectiveGradeLevel, tolerance);
  } else if (birthYear) {
    // Fallback to age-based filtering
    filteredNodes = filterNodesByAge(filteredNodes, birthYear);
  }

  // Apply subject filtering
  if (subject && subject !== 'other') {
    filteredNodes = filteredNodes.filter(node => {
      // Check if node has subject assigned
      if (node.subject) {
        return node.subject === subject;
      }
      
      // Otherwise, try to detect subject from content
      const analysis = analyzeContent(node);
      return analysis.detectedSubject === subject;
    });
  }

  // Sort by appropriateness
  if (effectiveGradeLevel) {
    filteredNodes = sortNodesByGradeLevel(filteredNodes, effectiveGradeLevel);
  } else if (birthYear) {
    filteredNodes = sortNodesByAgeRecommendation(filteredNodes, birthYear);
  }

  // Prioritize standards-aligned content if requested
  if (prioritizeStandards) {
    filteredNodes.sort((a, b) => {
      const aHasStandards = (a.standardsAlignment?.length || 0) > 0;
      const bHasStandards = (b.standardsAlignment?.length || 0) > 0;
      
      if (aHasStandards && !bHasStandards) return -1;
      if (!aHasStandards && bHasStandards) return 1;
      return 0;
    });
  }

  return filteredNodes.slice(0, maxResults);
}

/**
 * Get content recommendations for a specific subject and grade level
 */
export function getSubjectRecommendations(
  nodes: Node[],
  subject: Subject,
  gradeLevel: GradeLevel,
  maxResults: number = 10
): Node[] {
  return getEnhancedRecommendations(nodes, {
    subject,
    gradeLevel,
    maxResults,
    tolerance: 0, // Strict grade level matching for subject-specific recommendations
    prioritizeStandards: true
  });
}

/**
 * Get prerequisite learning path for a target node based on grade progression
 */
export function getGradeLevelPrerequisitePath(
  targetNode: Node,
  allNodes: Node[],
  studentGradeLevel: GradeLevel
): Node[] {
  const targetGradeLevel = targetNode.gradeLevel || assignGradeLevel(targetNode).gradeLevel;
  
  // If target is at or below student level, return empty path
  if (targetGradeLevel <= studentGradeLevel) {
    return [];
  }
  
  const path: Node[] = [];
  const subject = targetNode.subject || analyzeContent(targetNode).detectedSubject;
  
  if (!subject) return [];
  
  // Find prerequisite concepts for each grade level leading up to target
  for (let grade = studentGradeLevel + 1; grade < targetGradeLevel; grade++) {
    const gradeNodes = getSubjectRecommendations(allNodes, subject, grade as GradeLevel, 3);
    
    // Filter for concepts that are actually prerequisites
    const prerequisites = gradeNodes.filter(node =>
      targetNode.prereqs.includes(node.id) ||
      node.domain === targetNode.domain ||
      hasConceptualOverlap(node, targetNode)
    );
    
    path.push(...prerequisites.slice(0, 2)); // Max 2 per grade level
  }
  
  return path;
}

/**
 * Simple check for conceptual overlap between nodes
 */
function hasConceptualOverlap(nodeA: Node, nodeB: Node): boolean {
  const wordsA = nodeA.name.toLowerCase().split(/\s+/);
  const wordsB = nodeB.name.toLowerCase().split(/\s+/);
  
  const commonWords = wordsA.filter(word => 
    word.length > 3 && wordsB.includes(word)
  );
  
  return commonWords.length > 0;
}

/**
 * Get learning progression for a subject across grade levels
 */
export function getSubjectProgression(
  nodes: Node[],
  subject: Subject,
  startGrade: GradeLevel = 3,
  endGrade: GradeLevel = 12
): Record<GradeLevel, Node[]> {
  const progression: Partial<Record<GradeLevel, Node[]>> = {};
  
  for (let grade = startGrade; grade <= endGrade; grade++) {
    const gradeLevel = grade as GradeLevel;
    progression[gradeLevel] = getSubjectRecommendations(nodes, subject, gradeLevel);
  }
  
  return progression as Record<GradeLevel, Node[]>;
}

/**
 * Validate if a learning path is grade-appropriate
 */
export function validateLearningPath(
  path: Node[],
  studentGradeLevel: GradeLevel,
  tolerance: number = 1
): { isValid: boolean; issues: string[]; suggestions: string[] } {
  const issues: string[] = [];
  const suggestions: string[] = [];
  
  for (let i = 0; i < path.length; i++) {
    const node = path[i];
    const nodeGrade = node.gradeLevel || assignGradeLevel(node).gradeLevel;
    const gradeDiff = nodeGrade - studentGradeLevel;
    
    if (gradeDiff > tolerance + i) {
      issues.push(`${node.name} (Grade ${nodeGrade}) may be too advanced for current level`);
      suggestions.push(`Consider adding prerequisite content for Grade ${nodeGrade - 1}`);
    }
    
    if (i > 0) {
      const prevNode = path[i - 1];
      const prevGrade = prevNode.gradeLevel || assignGradeLevel(prevNode).gradeLevel;
      
      if (nodeGrade < prevGrade) {
        issues.push(`Learning path order issue: ${node.name} (Grade ${nodeGrade}) comes after ${prevNode.name} (Grade ${prevGrade})`);
        suggestions.push(`Reorder content to follow grade progression`);
      }
    }
  }
  
  return {
    isValid: issues.length === 0,
    issues,
    suggestions
  };
}