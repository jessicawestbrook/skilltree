/**
 * Grade Level Analysis System
 * 
 * This module provides intelligent content analysis to automatically assign
 * appropriate grade levels to educational content based on multiple factors
 * including vocabulary complexity, conceptual depth, and alignment with
 * educational standards.
 */

import { Node } from '../types';
import { 
  LearningStandard, 
  GradeLevel, 
  Subject, 
  ALL_STANDARDS, 
  STANDARDS_BY_GRADE, 
  STANDARDS_BY_SUBJECT,
  GRADE_PROGRESSIONS,
  ContentAnalysisConfig,
  DEFAULT_ANALYSIS_CONFIG
} from '../data/gradeLevelStandards';

export interface GradeLevelAssignment {
  gradeLevel: GradeLevel;
  confidence: number; // 0-1 scale
  reasoning: string[];
  matchedStandards: LearningStandard[];
  alternativeGrades: { grade: GradeLevel; confidence: number }[];
}

export interface ContentAnalysisResult {
  vocabularyComplexity: number; // 1-10 scale
  conceptualDepth: number; // 1-10 scale
  prerequisiteComplexity: number; // 1-10 scale
  cognitiveLoad: number; // 1-10 scale
  detectedSubject: Subject | null;
  keywordMatches: { standard: LearningStandard; score: number }[];
}

/**
 * Vocabulary complexity indicators for different grade levels
 */
const VOCABULARY_COMPLEXITY_PATTERNS: Record<string, GradeLevel[]> = {
  // Elementary vocabulary patterns
  'simple': [3, 4],
  'basic': [3, 4, 5],
  'elementary': [3, 4, 5],
  'fundamental': [4, 5, 6],
  'introduction': [3, 4, 5],
  'beginning': [3, 4],
  
  // Middle school vocabulary patterns
  'intermediate': [6, 7, 8],
  'moderate': [6, 7, 8],
  'developing': [6, 7],
  'expanding': [7, 8],
  'applying': [7, 8, 9],
  
  // High school vocabulary patterns
  'advanced': [9, 10, 11, 12],
  'complex': [10, 11, 12],
  'sophisticated': [11, 12],
  'comprehensive': [10, 11, 12],
  'analytical': [9, 10, 11, 12],
  'synthesis': [11, 12],
  'evaluation': [10, 11, 12],
  'critical': [9, 10, 11, 12]
};

/**
 * Subject detection patterns based on domain and keywords
 */
const SUBJECT_DETECTION_PATTERNS: Record<string, Subject> = {
  // Math patterns
  'algebra': 'math',
  'geometry': 'math',
  'calculus': 'math',
  'arithmetic': 'math',
  'mathematics': 'math',
  'equation': 'math',
  'function': 'math',
  'graph': 'math',
  'number': 'math',
  'fraction': 'math',
  'decimal': 'math',
  'percentage': 'math',
  'ratio': 'math',
  'proportion': 'math',
  'statistics': 'math',
  'probability': 'math',
  
  // ELA patterns
  'reading': 'ela',
  'writing': 'ela',
  'literature': 'ela',
  'grammar': 'ela',
  'vocabulary': 'ela',
  'comprehension': 'ela',
  'essay': 'ela',
  'paragraph': 'ela',
  'sentence': 'ela',
  'poetry': 'ela',
  'story': 'ela',
  'character': 'ela',
  'plot': 'ela',
  'theme': 'ela',
  'author': 'ela',
  'language': 'ela',
  
  // Science patterns
  'biology': 'science',
  'chemistry': 'science',
  'physics': 'science',
  'earth': 'science',
  'space': 'science',
  'experiment': 'science',
  'hypothesis': 'science',
  'observation': 'science',
  'cell': 'science',
  'atom': 'science',
  'molecule': 'science',
  'energy': 'science',
  'force': 'science',
  'motion': 'science',
  'ecosystem': 'science',
  'organism': 'science',
  
  // Social Studies patterns
  'history': 'social-studies',
  'geography': 'social-studies',
  'government': 'social-studies',
  'civics': 'social-studies',
  'economics': 'social-studies',
  'culture': 'social-studies',
  'society': 'social-studies',
  'civilization': 'social-studies',
  'democracy': 'social-studies',
  'constitution': 'social-studies',
  'revolution': 'social-studies',
  'war': 'social-studies',
  'politics': 'social-studies',
  'trade': 'social-studies'
};

/**
 * Analyze vocabulary complexity based on word patterns and length
 */
function analyzeVocabularyComplexity(content: string): number {
  const words = content.toLowerCase().split(/\s+/);
  let complexity = 0;
  let indicators = 0;

  // Check for vocabulary complexity indicators
  for (const [pattern, grades] of Object.entries(VOCABULARY_COMPLEXITY_PATTERNS)) {
    if (content.toLowerCase().includes(pattern)) {
      const avgGrade = grades.reduce((sum, grade) => sum + grade, 0) / grades.length;
      complexity += avgGrade;
      indicators++;
    }
  }

  // Average word length analysis
  const avgWordLength = words.reduce((sum, word) => sum + word.length, 0) / words.length;
  if (avgWordLength > 7) complexity += 2;
  else if (avgWordLength > 5) complexity += 1;

  // Syllable estimation (rough approximation)
  const estimatedSyllables = words.reduce((sum, word) => {
    const syllableCount = Math.max(1, word.match(/[aeiouy]+/g)?.length || 1);
    return sum + syllableCount;
  }, 0) / words.length;

  if (estimatedSyllables > 3) complexity += 2;
  else if (estimatedSyllables > 2) complexity += 1;

  // Normalize to 1-10 scale
  return indicators > 0 ? Math.min(10, Math.max(1, complexity / Math.max(1, indicators))) : 5;
}

/**
 * Detect the primary subject of content
 */
function detectSubject(content: string, domain: string): Subject | null {
  const text = (content + ' ' + domain).toLowerCase();
  const subjectScores: Record<Subject, number> = {
    'math': 0,
    'ela': 0,
    'science': 0,
    'social-studies': 0
  };

  // Score based on keyword matches
  for (const [keyword, subject] of Object.entries(SUBJECT_DETECTION_PATTERNS)) {
    const matches = (text.match(new RegExp(keyword, 'g')) || []).length;
    subjectScores[subject] += matches;
  }

  // Find the subject with the highest score
  const maxScore = Math.max(...Object.values(subjectScores));
  if (maxScore === 0) return null;

  const detectedSubject = Object.entries(subjectScores).find(([_, score]) => score === maxScore)?.[0] as Subject;
  return detectedSubject || null;
}

/**
 * Analyze conceptual depth based on content complexity
 */
function analyzeConceptualDepth(content: string, difficulty: number): number {
  const conceptualIndicators = {
    'basic': 1,
    'fundamental': 2,
    'understand': 3,
    'apply': 4,
    'analyze': 5,
    'synthesize': 6,
    'evaluate': 7,
    'create': 8,
    'design': 8,
    'innovate': 9,
    'research': 7,
    'investigate': 6,
    'compare': 5,
    'contrast': 5,
    'explain': 4,
    'describe': 3,
    'identify': 2,
    'list': 1
  };

  let maxDepth = 0;
  const text = content.toLowerCase();

  for (const [indicator, depth] of Object.entries(conceptualIndicators)) {
    if (text.includes(indicator)) {
      maxDepth = Math.max(maxDepth, depth);
    }
  }

  // Factor in the existing difficulty rating
  const difficultyFactor = Math.min(10, difficulty * 1.2);
  
  return Math.min(10, Math.max(1, (maxDepth + difficultyFactor) / 2));
}

/**
 * Calculate cognitive load based on content characteristics
 */
function analyzeCognitiveLoad(content: string, prereqs: string[]): number {
  let load = 1;

  // Factor in prerequisite complexity
  load += Math.min(4, prereqs.length * 0.5);

  // Check for cognitive load indicators
  const loadIndicators = {
    'multiple': 1,
    'complex': 2,
    'simultaneous': 2,
    'integrated': 2,
    'comprehensive': 3,
    'multi-step': 2,
    'interdisciplinary': 3,
    'synthesis': 3,
    'abstract': 2
  };

  const text = content.toLowerCase();
  for (const [indicator, weight] of Object.entries(loadIndicators)) {
    if (text.includes(indicator)) {
      load += weight;
    }
  }

  return Math.min(10, load);
}

/**
 * Find keyword matches with learning standards
 */
function findKeywordMatches(content: string, domain: string, subject: Subject | null): { standard: LearningStandard; score: number }[] {
  const text = (content + ' ' + domain).toLowerCase();
  const matches: { standard: LearningStandard; score: number }[] = [];
  
  const relevantStandards = subject ? STANDARDS_BY_SUBJECT[subject] : ALL_STANDARDS;

  for (const standard of relevantStandards) {
    let score = 0;
    
    // Check for exact keyword matches
    for (const keyword of standard.keywords) {
      const keywordLower = keyword.toLowerCase();
      if (text.includes(keywordLower)) {
        score += text.split(keywordLower).length - 1; // Count occurrences
      }
    }

    // Check title and description matches
    if (text.includes(standard.title.toLowerCase())) {
      score += 2;
    }
    
    const descriptionWords = standard.description.toLowerCase().split(/\s+/);
    const contentWords = text.split(/\s+/);
    const commonWords = descriptionWords.filter(word => 
      word.length > 3 && contentWords.includes(word)
    );
    score += commonWords.length * 0.5;

    if (score > 0) {
      matches.push({ standard, score });
    }
  }

  return matches.sort((a, b) => b.score - a.score);
}

/**
 * Perform comprehensive content analysis
 */
export function analyzeContent(node: Node): ContentAnalysisResult {
  const content = `${node.name} ${node.domain}`;
  
  const vocabularyComplexity = analyzeVocabularyComplexity(content);
  const detectedSubject = detectSubject(content, node.domain);
  const conceptualDepth = analyzeConceptualDepth(content, node.difficulty);
  const prerequisiteComplexity = Math.min(10, node.prereqs.length * 1.5 + 1);
  const cognitiveLoad = analyzeCognitiveLoad(content, node.prereqs);
  const keywordMatches = findKeywordMatches(content, node.domain, detectedSubject);

  return {
    vocabularyComplexity,
    conceptualDepth,
    prerequisiteComplexity,
    cognitiveLoad,
    detectedSubject,
    keywordMatches
  };
}

/**
 * Assign grade level based on comprehensive analysis
 */
export function assignGradeLevel(
  node: Node, 
  config: ContentAnalysisConfig = DEFAULT_ANALYSIS_CONFIG
): GradeLevelAssignment {
  const analysis = analyzeContent(node);
  const reasoning: string[] = [];
  
  // Calculate weighted complexity score
  const complexityScore = (
    analysis.vocabularyComplexity * config.complexityIndicators.vocabularyLevel +
    analysis.conceptualDepth * config.complexityIndicators.conceptualDepth +
    analysis.prerequisiteComplexity * config.complexityIndicators.prerequisiteComplexity +
    analysis.cognitiveLoad * config.complexityIndicators.cognitiveLoad
  );

  // Map complexity to grade level (3-12 scale)
  let baseGrade: GradeLevel;
  if (complexityScore <= 2.5) baseGrade = 3;
  else if (complexityScore <= 3.5) baseGrade = 4;
  else if (complexityScore <= 4.5) baseGrade = 5;
  else if (complexityScore <= 5.5) baseGrade = 6;
  else if (complexityScore <= 6.5) baseGrade = 7;
  else if (complexityScore <= 7.5) baseGrade = 8;
  else if (complexityScore <= 8.5) baseGrade = 9;
  else if (complexityScore <= 9.0) baseGrade = 10;
  else if (complexityScore <= 9.5) baseGrade = 11;
  else baseGrade = 12;

  reasoning.push(`Base complexity score: ${complexityScore.toFixed(2)} maps to grade ${baseGrade}`);

  // Adjust based on keyword matches
  const matchedStandards: LearningStandard[] = [];
  const gradeVotes: Record<GradeLevel, number> = {
    3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0
  };

  for (const match of analysis.keywordMatches.slice(0, 5)) { // Top 5 matches
    const weight = match.score * config.keywordWeights.exact;
    gradeVotes[match.standard.gradeLevel] += weight;
    matchedStandards.push(match.standard);
  }

  // Find the grade with the most votes
  const topVotedGrade = Object.entries(gradeVotes)
    .sort(([,a], [,b]) => b - a)[0];
  
  if (topVotedGrade && gradeVotes[topVotedGrade[0] as unknown as GradeLevel] > 0) {
    const votedGrade = parseInt(topVotedGrade[0]) as GradeLevel;
    const voteStrength = gradeVotes[votedGrade];
    
    // Blend base grade with voted grade based on vote strength
    const blendFactor = Math.min(0.7, voteStrength / 10);
    const blendedGrade = Math.round(baseGrade * (1 - blendFactor) + votedGrade * blendFactor) as GradeLevel;
    baseGrade = Math.max(3, Math.min(12, blendedGrade)) as GradeLevel;
    
    reasoning.push(`Keyword analysis suggests grade ${votedGrade} (strength: ${voteStrength.toFixed(2)})`);
    reasoning.push(`Final grade after blending: ${baseGrade}`);
  }

  // Calculate confidence based on consistency of indicators
  const gradeRange = Math.abs(baseGrade - (parseInt(topVotedGrade?.[0] || baseGrade.toString()) as GradeLevel));
  const confidence = Math.max(0.3, 1 - gradeRange * 0.15);

  // Generate alternative grades
  const alternativeGrades: { grade: GradeLevel; confidence: number }[] = [];
  for (let grade = 3; grade <= 12; grade++) {
    if (grade !== baseGrade) {
      const distance = Math.abs(grade - baseGrade);
      const altConfidence = Math.max(0, confidence - distance * 0.2);
      if (altConfidence > 0.1) {
        alternativeGrades.push({ 
          grade: grade as GradeLevel, 
          confidence: altConfidence 
        });
      }
    }
  }

  alternativeGrades.sort((a, b) => b.confidence - a.confidence);

  // Add detailed reasoning
  if (analysis.detectedSubject) {
    reasoning.push(`Detected subject: ${analysis.detectedSubject}`);
  }
  reasoning.push(`Vocabulary complexity: ${analysis.vocabularyComplexity.toFixed(1)}`);
  reasoning.push(`Conceptual depth: ${analysis.conceptualDepth.toFixed(1)}`);
  reasoning.push(`Prerequisite complexity: ${analysis.prerequisiteComplexity.toFixed(1)}`);
  reasoning.push(`Cognitive load: ${analysis.cognitiveLoad.toFixed(1)}`);

  return {
    gradeLevel: baseGrade,
    confidence,
    reasoning,
    matchedStandards,
    alternativeGrades: alternativeGrades.slice(0, 3) // Top 3 alternatives
  };
}

/**
 * Get standards for a specific grade level and subject
 */
export function getStandardsForGrade(gradeLevel: GradeLevel, subject?: Subject): LearningStandard[] {
  let standards = STANDARDS_BY_GRADE[gradeLevel];
  if (subject) {
    standards = standards.filter(s => s.subject === subject);
  }
  return standards;
}

/**
 * Find prerequisite standards for a given standard
 */
export function findPrerequisiteStandards(standardId: string): LearningStandard[] {
  const standard = ALL_STANDARDS.find(s => s.id === standardId);
  if (!standard || !standard.prerequisiteStandardIds) {
    return [];
  }

  return standard.prerequisiteStandardIds
    .map(id => ALL_STANDARDS.find(s => s.id === id))
    .filter(Boolean) as LearningStandard[];
}

/**
 * Get learning progression for a subject across grades
 */
export function getLearningProgression(subject: Subject): Record<GradeLevel, LearningStandard[]> {
  const progression: Record<GradeLevel, LearningStandard[]> = {
    3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []
  };

  const subjectStandards = STANDARDS_BY_SUBJECT[subject];
  
  for (const standard of subjectStandards) {
    progression[standard.gradeLevel].push(standard);
  }

  return progression;
}

/**
 * Validate if content is appropriate for a specific grade level
 */
export function validateGradeLevelAppropriate(
  node: Node, 
  targetGrade: GradeLevel,
  tolerance: number = 1
): { appropriate: boolean; reasoning: string[] } {
  const assignment = assignGradeLevel(node);
  const gradeDifference = Math.abs(assignment.gradeLevel - targetGrade);
  
  const reasoning: string[] = [
    `Assigned grade level: ${assignment.gradeLevel}`,
    `Target grade level: ${targetGrade}`,
    `Grade difference: ${gradeDifference}`,
    `Tolerance: ±${tolerance} grades`
  ];

  const appropriate = gradeDifference <= tolerance;
  
  if (!appropriate) {
    reasoning.push(`Content is ${gradeDifference > tolerance ? 'too advanced' : 'too basic'} for grade ${targetGrade}`);
  } else {
    reasoning.push(`Content is appropriate for grade ${targetGrade}`);
  }

  return { appropriate, reasoning };
}

/**
 * Batch process multiple nodes for grade level assignment
 */
export function batchAssignGradeLevels(
  nodes: Node[], 
  config: ContentAnalysisConfig = DEFAULT_ANALYSIS_CONFIG
): Record<string, GradeLevelAssignment> {
  const assignments: Record<string, GradeLevelAssignment> = {};
  
  for (const node of nodes) {
    assignments[node.id] = assignGradeLevel(node, config);
  }
  
  return assignments;
}