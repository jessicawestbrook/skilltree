/**
 * Utility to update the knowledge structure with grade levels and standards alignment
 * This script analyzes all nodes and assigns appropriate grade levels based on content analysis
 */

import { Node } from '../types';
import { KnowledgeCategory } from '../data/comprehensiveKnowledgeStructure';
import { assignGradeLevel, analyzeContent } from './gradeLevelAnalysis';
import { Subject, ALL_STANDARDS } from '../data/gradeLevelStandards';

/**
 * Grade level mappings for common mathematical concepts
 */
const MATH_GRADE_MAPPINGS: Record<string, number> = {
  // Elementary Math (Grades 3-5)
  'basic algebra': 4,
  'arithmetic': 3,
  'fractions': 4,
  'decimals': 5,
  'percentages': 5,
  'basic geometry': 4,
  'euclidean geometry': 8,
  'descriptive statistics': 6,
  
  // Middle School Math (Grades 6-8)
  'pre-algebra': 7,
  'ratios': 6,
  'proportions': 7,
  'probability': 7,
  'basic statistics': 7,
  'coordinate geometry': 8,
  
  // High School Math (Grades 9-12)
  'algebra': 9,
  'linear algebra': 11,
  'geometry': 10,
  'analytic geometry': 11,
  'trigonometry': 11,
  'calculus': 12,
  'statistics': 11,
  'probability theory': 11,
  
  // Advanced Math (College Level - Grade 12+)
  'abstract algebra': 12,
  'real analysis': 12,
  'complex analysis': 12,
  'differential geometry': 12,
  'topology': 12,
  'number theory': 12,
  'optimization': 12
};

/**
 * Grade level mappings for science concepts
 */
const SCIENCE_GRADE_MAPPINGS: Record<string, number> = {
  // Elementary Science (Grades 3-5)
  'basic biology': 3,
  'plants': 3,
  'animals': 3,
  'weather': 4,
  'simple machines': 4,
  'matter': 5,
  'energy': 5,
  
  // Middle School Science (Grades 6-8)
  'cell biology': 6,
  'ecology': 7,
  'chemistry basics': 7,
  'physics basics': 8,
  'earth science': 6,
  'astronomy': 8,
  
  // High School Science (Grades 9-12)
  'biology': 9,
  'chemistry': 10,
  'physics': 11,
  'environmental science': 9,
  'anatomy': 10,
  'genetics': 11,
  'biochemistry': 12,
  'organic chemistry': 12,
  'quantum physics': 12,
  'molecular biology': 12
};

/**
 * Grade level mappings for language arts concepts
 */
const ELA_GRADE_MAPPINGS: Record<string, number> = {
  // Elementary ELA (Grades 3-5)
  'basic reading': 3,
  'phonics': 3,
  'vocabulary': 4,
  'comprehension': 4,
  'basic writing': 4,
  'grammar': 5,
  'spelling': 4,
  
  // Middle School ELA (Grades 6-8)
  'literature': 6,
  'poetry': 7,
  'essay writing': 7,
  'research': 8,
  'critical thinking': 8,
  
  // High School ELA (Grades 9-12)
  'advanced literature': 9,
  'composition': 10,
  'rhetoric': 11,
  'literary analysis': 11,
  'creative writing': 10,
  'journalism': 11,
  'debate': 12
};

/**
 * Grade level mappings for social studies concepts
 */
const SOCIAL_STUDIES_GRADE_MAPPINGS: Record<string, number> = {
  // Elementary Social Studies (Grades 3-5)
  'community': 3,
  'geography basics': 4,
  'maps': 4,
  'local history': 4,
  'civics basics': 5,
  'government basics': 5,
  
  // Middle School Social Studies (Grades 6-8)
  'world geography': 6,
  'ancient civilizations': 6,
  'world history': 7,
  'american history': 8,
  'civics': 8,
  
  // High School Social Studies (Grades 9-12)
  'world history advanced': 9,
  'us history': 10,
  'government': 11,
  'economics': 12,
  'psychology': 11,
  'sociology': 12,
  'political science': 12
};

/**
 * Combine all grade mappings
 */
const ALL_GRADE_MAPPINGS = {
  ...MATH_GRADE_MAPPINGS,
  ...SCIENCE_GRADE_MAPPINGS,
  ...ELA_GRADE_MAPPINGS,
  ...SOCIAL_STUDIES_GRADE_MAPPINGS
};

/**
 * Detect subject based on domain and content
 */
function detectNodeSubject(node: Node): Subject {
  const domain = node.domain.toLowerCase();
  const name = node.name.toLowerCase();
  const content = `${domain} ${name}`;

  // Math indicators
  if (content.includes('math') || content.includes('algebra') || content.includes('calculus') || 
      content.includes('geometry') || content.includes('statistics') || content.includes('number') ||
      content.includes('equation') || content.includes('formula') || content.includes('arithmetic')) {
    return 'math';
  }

  // Science indicators
  if (content.includes('biology') || content.includes('chemistry') || content.includes('physics') ||
      content.includes('science') || content.includes('molecular') || content.includes('cell') ||
      content.includes('organism') || content.includes('energy') || content.includes('matter') ||
      content.includes('quantum') || content.includes('ecology') || content.includes('genetics')) {
    return 'science';
  }

  // ELA indicators
  if (content.includes('literature') || content.includes('writing') || content.includes('reading') ||
      content.includes('language') || content.includes('grammar') || content.includes('poetry') ||
      content.includes('essay') || content.includes('composition') || content.includes('rhetoric')) {
    return 'ela';
  }

  // Social Studies indicators
  if (content.includes('history') || content.includes('geography') || content.includes('government') ||
      content.includes('civics') || content.includes('economics') || content.includes('politics') ||
      content.includes('society') || content.includes('culture') || content.includes('civilization')) {
    return 'social-studies';
  }

  return 'other';
}

/**
 * Get manual grade level mapping for a node
 */
function getManualGradeLevel(node: Node): number | null {
  const name = node.name.toLowerCase();
  const domain = node.domain.toLowerCase();
  
  // Check exact matches first
  if (ALL_GRADE_MAPPINGS[name]) {
    return ALL_GRADE_MAPPINGS[name];
  }
  
  if (ALL_GRADE_MAPPINGS[domain]) {
    return ALL_GRADE_MAPPINGS[domain];
  }
  
  // Check partial matches
  for (const [concept, grade] of Object.entries(ALL_GRADE_MAPPINGS)) {
    if (name.includes(concept) || domain.includes(concept)) {
      return grade;
    }
  }
  
  return null;
}

/**
 * Find matching standards for a node
 */
function findMatchingStandards(node: Node, subject: Subject, gradeLevel: number): string[] {
  const matchingStandards: string[] = [];
  const content = `${node.name} ${node.domain}`.toLowerCase();
  
  // Find standards that match the subject and grade level
  const relevantStandards = ALL_STANDARDS.filter(s => 
    s.subject === subject && Math.abs(s.gradeLevel - gradeLevel) <= 1
  );
  
  for (const standard of relevantStandards) {
    let score = 0;
    
    // Check keyword matches
    for (const keyword of standard.keywords) {
      if (content.includes(keyword.toLowerCase())) {
        score += 1;
      }
    }
    
    // Check title matches
    if (content.includes(standard.title.toLowerCase())) {
      score += 2;
    }
    
    // Check domain matches
    if (standard.domain.toLowerCase().includes(node.domain.toLowerCase()) ||
        node.domain.toLowerCase().includes(standard.domain.toLowerCase())) {
      score += 1;
    }
    
    // If we have a good match, include this standard
    if (score >= 2) {
      matchingStandards.push(standard.id);
    }
  }
  
  return matchingStandards;
}

/**
 * Update a single node with grade level and standards alignment
 */
export function updateNodeGradeLevel(node: Node): Node {
  const updatedNode = { ...node };
  
  // Detect subject
  const subject = detectNodeSubject(node);
  updatedNode.subject = subject;
  
  // Try manual mapping first
  let gradeLevel = getManualGradeLevel(node);
  
  // If no manual mapping, use content analysis
  if (!gradeLevel) {
    const assignment = assignGradeLevel(node);
    gradeLevel = assignment.gradeLevel;
  }
  
  // Ensure grade level is within valid range (3-12)
  gradeLevel = Math.max(3, Math.min(12, gradeLevel));
  updatedNode.gradeLevel = gradeLevel;
  
  // Find matching standards
  if (subject !== 'other') {
    const standards = findMatchingStandards(node, subject, gradeLevel);
    if (standards.length > 0) {
      updatedNode.standardsAlignment = standards;
    }
  }
  
  return updatedNode;
}

/**
 * Recursively update all nodes in a knowledge category
 */
export function updateCategoryGradeLevels(category: KnowledgeCategory): KnowledgeCategory {
  const updatedCategory = { ...category };
  
  // Update nodes in this category
  if (category.nodes) {
    updatedCategory.nodes = category.nodes.map(updateNodeGradeLevel);
  }
  
  // Recursively update subcategories
  if (category.subcategories) {
    updatedCategory.subcategories = category.subcategories.map(updateCategoryGradeLevels);
  }
  
  return updatedCategory;
}

/**
 * Helper function to extract all nodes from a category structure
 */
export function extractAllNodes(category: KnowledgeCategory): Node[] {
  let allNodes: Node[] = [];
  
  // Add nodes from this category
  if (category.nodes) {
    allNodes = allNodes.concat(category.nodes);
  }
  
  // Recursively add nodes from subcategories
  if (category.subcategories) {
    for (const subcat of category.subcategories) {
      allNodes = allNodes.concat(extractAllNodes(subcat));
    }
  }
  
  return allNodes;
}

/**
 * Generate grade level distribution report
 */
export function generateGradeLevelReport(category: KnowledgeCategory): {
  totalNodes: number;
  gradeDistribution: Record<number, number>;
  subjectDistribution: Record<Subject | 'other', number>;
  standardsAligned: number;
} {
  const allNodes = extractAllNodes(category);
  const gradeDistribution: Record<number, number> = {};
  const subjectDistribution: Record<Subject | 'other', number> = {
    'math': 0,
    'ela': 0,
    'science': 0,
    'social-studies': 0,
    'other': 0
  };
  let standardsAligned = 0;
  
  for (const node of allNodes) {
    // Count grade levels
    if (node.gradeLevel) {
      gradeDistribution[node.gradeLevel] = (gradeDistribution[node.gradeLevel] || 0) + 1;
    }
    
    // Count subjects
    const subject = node.subject || 'other';
    subjectDistribution[subject]++;
    
    // Count standards-aligned nodes
    if (node.standardsAlignment && node.standardsAlignment.length > 0) {
      standardsAligned++;
    }
  }
  
  return {
    totalNodes: allNodes.length,
    gradeDistribution,
    subjectDistribution,
    standardsAligned
  };
}

/**
 * Preview changes before applying them
 */
export function previewGradeLevelChanges(category: KnowledgeCategory): {
  nodeName: string;
  currentGrade?: number;
  proposedGrade: number;
  subject: Subject | 'other';
  confidence: number;
  standards: string[];
}[] {
  const allNodes = extractAllNodes(category);
  const changes: {
    nodeName: string;
    currentGrade?: number;
    proposedGrade: number;
    subject: Subject | 'other';
    confidence: number;
    standards: string[];
  }[] = [];
  
  for (const node of allNodes) {
    const updatedNode = updateNodeGradeLevel(node);
    const assignment = assignGradeLevel(node);
    
    changes.push({
      nodeName: node.name,
      currentGrade: node.gradeLevel,
      proposedGrade: updatedNode.gradeLevel!,
      subject: updatedNode.subject!,
      confidence: assignment.confidence,
      standards: updatedNode.standardsAlignment || []
    });
  }
  
  return changes.sort((a, b) => a.proposedGrade - b.proposedGrade);
}