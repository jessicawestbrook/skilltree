/**
 * Demonstration of the Grade-Level Standards System
 * 
 * This file shows how to use the comprehensive grade-level standards system
 * for educational content tagging and recommendation.
 */

import { Node } from '../types';
import { 
  assignGradeLevel, 
  analyzeContent, 
  validateGradeLevelAppropriate,
  getStandardsForGrade,
  getLearningProgression
} from './gradeLevelAnalysis';
import { 
  getEnhancedRecommendations,
  getSubjectRecommendations,
  filterNodesByGradeLevel,
  birthYearToGradeLevel,
  validateLearningPath
} from './contentRecommendation';
import { 
  ALL_STANDARDS,
  GRADE_PROGRESSIONS,
  GradeLevel,
  Subject
} from '../data/gradeLevelStandards';
import { knowledgeStructure } from '../data/comprehensiveKnowledgeStructure';
import { extractAllNodes, generateGradeLevelReport } from './updateKnowledgeStructureGrades';

/**
 * Demo 1: Analyze content and assign grade levels automatically
 */
export function demoContentAnalysis() {
  console.log('=== Grade Level Content Analysis Demo ===\n');
  
  // Sample nodes for testing
  const sampleNodes: Node[] = [
    {
      id: 'fractions-basic',
      name: 'Introduction to Fractions',
      domain: 'mathematics',
      prereqs: [],
      difficulty: 2,
      points: 100
    },
    {
      id: 'algebra-equations',
      name: 'Solving Linear Equations',
      domain: 'algebra',
      prereqs: ['fractions-basic'],
      difficulty: 3,
      points: 150
    },
    {
      id: 'cell-biology',
      name: 'Plant and Animal Cells',
      domain: 'biology',
      prereqs: [],
      difficulty: 2,
      points: 100
    },
    {
      id: 'civil-war',
      name: 'American Civil War',
      domain: 'history',
      prereqs: [],
      difficulty: 3,
      points: 150
    }
  ];

  for (const node of sampleNodes) {
    console.log(`Analyzing: ${node.name}`);
    
    // Analyze content
    const analysis = analyzeContent(node);
    console.log(`  Detected Subject: ${analysis.detectedSubject || 'Unknown'}`);
    console.log(`  Vocabulary Complexity: ${analysis.vocabularyComplexity.toFixed(1)}/10`);
    console.log(`  Conceptual Depth: ${analysis.conceptualDepth.toFixed(1)}/10`);
    
    // Assign grade level
    const assignment = assignGradeLevel(node);
    console.log(`  Assigned Grade Level: ${assignment.gradeLevel}`);
    console.log(`  Confidence: ${(assignment.confidence * 100).toFixed(1)}%`);
    console.log(`  Matched Standards: ${assignment.matchedStandards.length}`);
    
    if (assignment.reasoning.length > 0) {
      console.log(`  Reasoning: ${assignment.reasoning[0]}`);
    }
    
    console.log('');
  }
}

/**
 * Demo 2: Filter and recommend content based on grade level
 */
export function demoGradeLevelFiltering() {
  console.log('=== Grade Level Filtering Demo ===\n');
  
  // Get all nodes from knowledge structure
  const allNodes = extractAllNodes(knowledgeStructure);
  console.log(`Total nodes in knowledge base: ${allNodes.length}\n`);
  
  // Test filtering for different grade levels
  const testGrades: GradeLevel[] = [6, 9, 12];
  
  for (const grade of testGrades) {
    console.log(`Grade ${grade} Content:`);
    
    // Filter nodes appropriate for this grade level
    const gradeNodes = filterNodesByGradeLevel(allNodes, grade);
    console.log(`  ${gradeNodes.length} appropriate nodes found`);
    
    // Get subject-specific recommendations
    const mathNodes = getSubjectRecommendations(allNodes, 'math', grade, 5);
    const scienceNodes = getSubjectRecommendations(allNodes, 'science', grade, 5);
    
    console.log(`  Math recommendations: ${mathNodes.length}`);
    console.log(`  Science recommendations: ${scienceNodes.length}`);
    
    // Show top recommendations
    if (mathNodes.length > 0) {
      console.log(`  Top Math: ${mathNodes[0].name} (Grade ${mathNodes[0].gradeLevel})`);
    }
    if (scienceNodes.length > 0) {
      console.log(`  Top Science: ${scienceNodes[0].name} (Grade ${scienceNodes[0].gradeLevel})`);
    }
    
    console.log('');
  }
}

/**
 * Demo 3: Enhanced recommendations based on student profile
 */
export function demoEnhancedRecommendations() {
  console.log('=== Enhanced Recommendation Demo ===\n');
  
  const allNodes = extractAllNodes(knowledgeStructure);
  
  // Simulate different student profiles
  const studentProfiles = [
    {
      name: 'Middle School Student (13 years old)',
      birthYear: new Date().getFullYear() - 13,
      interests: ['science'],
    },
    {
      name: 'High School Freshman (14 years old)',
      birthYear: new Date().getFullYear() - 14,
      interests: ['math'],
    },
    {
      name: 'High School Senior (17 years old)',
      birthYear: new Date().getFullYear() - 17,
      interests: ['science', 'math'],
    }
  ];

  for (const profile of studentProfiles) {
    console.log(`${profile.name}:`);
    
    const gradeLevel = birthYearToGradeLevel(profile.birthYear);
    console.log(`  Estimated Grade Level: ${gradeLevel || 'Unknown'}`);
    
    if (gradeLevel) {
      // Get general recommendations
      const recommendations = getEnhancedRecommendations(allNodes, {
        gradeLevel,
        maxResults: 5,
        prioritizeStandards: true
      });
      
      console.log(`  General Recommendations (${recommendations.length}):`);
      recommendations.slice(0, 3).forEach((node, i) => {
        console.log(`    ${i + 1}. ${node.name} (Grade ${node.gradeLevel}, ${node.subject})`);
      });
      
      // Get subject-specific recommendations
      for (const subject of profile.interests) {
        const subjectRecs = getSubjectRecommendations(
          allNodes, 
          subject as Subject, 
          gradeLevel, 
          3
        );
        
        console.log(`  ${subject.charAt(0).toUpperCase() + subject.slice(1)} Recommendations:`);
        subjectRecs.forEach((node, i) => {
          console.log(`    ${i + 1}. ${node.name} (Grade ${node.gradeLevel})`);
        });
      }
    }
    
    console.log('');
  }
}

/**
 * Demo 4: Standards alignment and learning progressions
 */
export function demoStandardsAlignment() {
  console.log('=== Standards Alignment Demo ===\n');
  
  // Show standards for different grades
  const grades: GradeLevel[] = [3, 6, 9, 12];
  
  for (const grade of grades) {
    console.log(`Grade ${grade} Standards:`);
    
    const mathStandards = getStandardsForGrade(grade, 'math');
    const scienceStandards = getStandardsForGrade(grade, 'science');
    
    console.log(`  Math: ${mathStandards.length} standards`);
    console.log(`  Science: ${scienceStandards.length} standards`);
    
    // Show sample standards
    if (mathStandards.length > 0) {
      const sample = mathStandards[0];
      console.log(`    Sample Math: ${sample.title}`);
      console.log(`    Description: ${sample.description.substring(0, 80)}...`);
    }
    
    if (scienceStandards.length > 0) {
      const sample = scienceStandards[0];
      console.log(`    Sample Science: ${sample.title}`);
      console.log(`    Description: ${sample.description.substring(0, 80)}...`);
    }
    
    console.log('');
  }
  
  // Show learning progression for math
  console.log('Math Learning Progression (Grades 3-8):');
  const mathProgression = getLearningProgression('math');
  
  for (let grade = 3; grade <= 8; grade++) {
    const gradeStandards = mathProgression[grade as GradeLevel] || [];
    if (gradeStandards.length > 0) {
      console.log(`  Grade ${grade}: ${gradeStandards[0].domain} - ${gradeStandards[0].title}`);
    }
  }
  
  console.log('');
}

/**
 * Demo 5: Learning path validation
 */
export function demoLearningPathValidation() {
  console.log('=== Learning Path Validation Demo ===\n');
  
  const allNodes = extractAllNodes(knowledgeStructure);
  
  // Create a sample learning path
  const samplePath = [
    allNodes.find(n => n.gradeLevel === 9) || allNodes[0],
    allNodes.find(n => n.gradeLevel === 11) || allNodes[1],
    allNodes.find(n => n.gradeLevel === 10) || allNodes[2], // This should create an order issue
    allNodes.find(n => n.gradeLevel === 12) || allNodes[3],
  ].filter(Boolean) as Node[];
  
  console.log('Sample Learning Path:');
  samplePath.forEach((node, i) => {
    console.log(`  ${i + 1}. ${node.name} (Grade ${node.gradeLevel})`);
  });
  
  // Validate for different student grade levels
  const studentGrades: GradeLevel[] = [8, 10, 11];
  
  for (const studentGrade of studentGrades) {
    console.log(`\nValidation for Grade ${studentGrade} student:`);
    
    const validation = validateLearningPath(samplePath, studentGrade);
    console.log(`  Valid: ${validation.isValid}`);
    
    if (validation.issues.length > 0) {
      console.log('  Issues:');
      validation.issues.forEach(issue => {
        console.log(`    - ${issue}`);
      });
    }
    
    if (validation.suggestions.length > 0) {
      console.log('  Suggestions:');
      validation.suggestions.forEach(suggestion => {
        console.log(`    - ${suggestion}`);
      });
    }
  }
  
  console.log('');
}

/**
 * Demo 6: Knowledge structure analysis report
 */
export function demoKnowledgeStructureReport() {
  console.log('=== Knowledge Structure Analysis Report ===\n');
  
  const report = generateGradeLevelReport(knowledgeStructure);
  
  console.log(`Total Nodes: ${report.totalNodes}`);
  console.log(`Standards-Aligned Nodes: ${report.standardsAligned} (${((report.standardsAligned / report.totalNodes) * 100).toFixed(1)}%)`);
  
  console.log('\nGrade Level Distribution:');
  Object.entries(report.gradeDistribution)
    .sort(([a], [b]) => parseInt(a) - parseInt(b))
    .forEach(([grade, count]) => {
      const percentage = ((count / report.totalNodes) * 100).toFixed(1);
      console.log(`  Grade ${grade}: ${count} nodes (${percentage}%)`);
    });
  
  console.log('\nSubject Distribution:');
  Object.entries(report.subjectDistribution).forEach(([subject, count]) => {
    const percentage = ((count / report.totalNodes) * 100).toFixed(1);
    console.log(`  ${subject}: ${count} nodes (${percentage}%)`);
  });
  
  console.log('');
}

/**
 * Run all demos
 */
export function runAllDemos() {
  console.log('🎓 NeuroQuest Grade-Level Standards System Demo\n');
  console.log('================================================\n');
  
  try {
    demoContentAnalysis();
    demoGradeLevelFiltering();
    demoEnhancedRecommendations();
    demoStandardsAlignment();
    demoLearningPathValidation();
    demoKnowledgeStructureReport();
    
    console.log('✅ All demos completed successfully!');
    console.log('\nThe grade-level standards system is ready for use.');
    console.log('Key features implemented:');
    console.log('  ✓ Automatic grade level assignment');
    console.log('  ✓ Standards alignment (Common Core, NGSS, etc.)');
    console.log('  ✓ Grade-appropriate content filtering');
    console.log('  ✓ Enhanced recommendation system');
    console.log('  ✓ Learning path validation');
    console.log('  ✓ Comprehensive subject coverage (Math, ELA, Science, Social Studies)');
    
  } catch (error) {
    console.error('❌ Demo failed:', error);
  }
}

// Export for easy testing
export default {
  runAllDemos,
  demoContentAnalysis,
  demoGradeLevelFiltering,
  demoEnhancedRecommendations,
  demoStandardsAlignment,
  demoLearningPathValidation,
  demoKnowledgeStructureReport
};