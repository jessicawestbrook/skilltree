const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

// Enhanced grade level estimation with better distribution and educational alignment
function estimateGradeLevel(word) {
  const length = word.word.length;
  const spellingLevel = word.spelling_difficulty_level;
  const vocabLevel = word.vocabulary_difficulty_level;
  const definition = word.definition || '';
  const wordText = word.word.toLowerCase();
  
  // Start with base scores from difficulty levels
  let gradeScore = 0;
  
  // Spelling difficulty mapping (more distributed approach)
  if (spellingLevel === 1) {
    gradeScore = 2; // Beginner spelling -> Grade 2 base
  } else if (spellingLevel === 2) {
    gradeScore = 4; // Elementary -> Grade 4 base
  } else if (spellingLevel === 3) {
    gradeScore = 7; // Intermediate -> Grade 7 base
  } else if (spellingLevel === 4) {
    gradeScore = 10; // Advanced -> Grade 10 base
  } else if (spellingLevel === 5) {
    gradeScore = 12; // Expert -> Grade 12 base
  }
  
  // Vocabulary difficulty adjustments
  if (vocabLevel === 1) {
    // Foundation vocabulary - cap at early elementary
    gradeScore = Math.min(gradeScore, 3);
  } else if (vocabLevel === 2) {
    // Academic vocabulary - appropriate for elementary to middle
    gradeScore = Math.max(gradeScore - 1, 3);
  } else if (vocabLevel === 3) {
    // Sophisticated vocabulary - middle school and up
    gradeScore = Math.max(gradeScore, 6);
  } else if (vocabLevel === 4) {
    // Specialized vocabulary - high school level
    gradeScore = Math.max(gradeScore, 9);
  } else if (vocabLevel === 5) {
    // Scholarly vocabulary - advanced high school
    gradeScore = Math.max(gradeScore, 11);
  }
  
  // Word length adjustments for better K-2 representation
  if (length <= 3) {
    if (isBasicSightWord(wordText) || hasSimpleCVCPattern(wordText)) {
      gradeScore = Math.min(gradeScore, 1); // K-1 for very simple words
    } else {
      gradeScore = Math.min(gradeScore, 2); // Grade 2 for short words
    }
  } else if (length <= 4) {
    gradeScore = Math.min(gradeScore, 3); // Cap at Grade 3
  } else if (length <= 5) {
    gradeScore = Math.min(gradeScore, 5); // Cap at Grade 5
  } else if (length >= 12) {
    gradeScore = Math.max(gradeScore, 8); // Long words at least Grade 8
  } else if (length >= 10) {
    gradeScore = Math.max(gradeScore, 7); // Medium-long words at least Grade 7
  }
  
  // Pattern-based adjustments for early grades
  if (isBasicSightWord(wordText)) {
    return 'K'; // Kindergarten sight words
  } else if (hasSimpleCVCPattern(wordText) && length <= 4) {
    gradeScore = Math.min(gradeScore, 1); // Grade 1 for simple CVC
  } else if (hasSimplePhonicPattern(wordText) && length <= 5) {
    gradeScore = Math.min(gradeScore, 2); // Grade 2 for simple phonics
  }
  
  // Complex pattern adjustments
  if (hasComplexPattern(wordText)) {
    gradeScore = Math.max(gradeScore, 6); // Complex patterns need at least Grade 6
  }
  
  // Definition complexity analysis
  if (definition) {
    if (isSimpleDefinition(definition)) {
      gradeScore = Math.min(gradeScore, 4); // Simple definitions cap at Grade 4
    } else if (isTechnicalDefinition(definition)) {
      gradeScore = Math.max(gradeScore, 9); // Technical terms need Grade 9+
    } else if (isAcademicDefinition(definition)) {
      gradeScore = Math.max(gradeScore, 6); // Academic terms need Grade 6+
    }
  }
  
  // Subject-specific adjustments
  if (isMathTerm(wordText, definition)) {
    if (isBasicMath(wordText)) gradeScore = Math.max(gradeScore, 3);
    else if (isAdvancedMath(wordText)) gradeScore = Math.max(gradeScore, 9);
  }
  
  if (isScienceTerm(wordText, definition)) {
    if (isBasicScience(wordText)) gradeScore = Math.max(gradeScore, 4);
    else gradeScore = Math.max(gradeScore, 7);
  }
  
  // Final grade conversion with better distribution
  gradeScore = Math.max(0, Math.min(12, gradeScore));
  
  // Convert to grade level string
  if (gradeScore <= 0.5) return 'K';
  else if (gradeScore <= 1.5) return '1';
  else if (gradeScore <= 2.5) return '2';
  else if (gradeScore <= 3.5) return '3';
  else if (gradeScore <= 4.5) return '4';
  else if (gradeScore <= 5.5) return '5';
  else if (gradeScore <= 6.5) return '6';
  else if (gradeScore <= 7.5) return '7';
  else if (gradeScore <= 8.5) return '8';
  else if (gradeScore <= 9.5) return '9';
  else if (gradeScore <= 10.5) return '10';
  else if (gradeScore <= 11.5) return '11';
  else return '12';
}

// Enhanced helper functions for better classification
function isBasicSightWord(word) {
  const kindergartenWords = [
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with', 'you'
  ];
  const grade1Words = [
    'all', 'any', 'can', 'had', 'her', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'
  ];
  
  return kindergartenWords.includes(word) || grade1Words.includes(word);
}

function hasSimpleCVCPattern(word) {
  // Simple consonant-vowel-consonant patterns
  return /^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]$/.test(word) && word.length === 3;
}

function hasSimplePhonicPattern(word) {
  // Basic phonetic patterns for early grades
  return /^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]e?$/.test(word) && word.length <= 5;
}

function hasComplexPattern(word) {
  const complexPatterns = [
    /ough/, /augh/, /eigh/, /tion/, /sion/, /cian/, /ph/, /gh/, /kn/, /wr/, /mb$/, /gn/, /ps/, /rh/, /sch/, /tch/, /dge/
  ];
  return complexPatterns.some(pattern => pattern.test(word));
}

function isSimpleDefinition(definition) {
  if (!definition || definition.length > 80) return false;
  const simpleWords = ['a', 'an', 'the', 'is', 'are', 'was', 'were', 'can', 'will', 'would', 'have', 'has', 'had', 'do', 'does', 'did'];
  const words = definition.toLowerCase().split(/\s+/);
  const simpleWordCount = words.filter(word => simpleWords.includes(word) || word.length <= 4).length;
  return simpleWordCount / words.length > 0.4;
}

function isAcademicDefinition(definition) {
  if (!definition) return false;
  const academicTerms = [
    'analyze', 'concept', 'theory', 'principle', 'method', 'process', 'system', 'structure', 'function', 'relationship',
    'demonstrate', 'illustrate', 'examine', 'evaluate', 'compare', 'contrast', 'summarize', 'interpret', 'context'
  ];
  const lowerDef = definition.toLowerCase();
  return academicTerms.some(term => lowerDef.includes(term));
}

function isTechnicalDefinition(definition) {
  if (!definition) return false;
  const technicalTerms = [
    'scientific', 'medical', 'technical', 'specialized', 'professional', 'engineering', 'mathematical', 'chemical', 
    'biological', 'pharmaceutical', 'clinical', 'diagnostic', 'therapeutic', 'analytical', 'computational', 'molecular'
  ];
  const lowerDef = definition.toLowerCase();
  return technicalTerms.some(term => lowerDef.includes(term));
}

function isMathTerm(word, definition) {
  const mathWords = ['algebra', 'geometry', 'calculus', 'equation', 'formula', 'theorem', 'proof', 'angle', 'triangle', 'circle', 'square', 'rectangle', 'polygon'];
  const mathTerms = ['mathematical', 'geometric', 'algebraic', 'arithmetic', 'numeric', 'calculate', 'solve'];
  return mathWords.includes(word) || (definition && mathTerms.some(term => definition.toLowerCase().includes(term)));
}

function isBasicMath(word) {
  const basicMath = ['add', 'plus', 'minus', 'times', 'divide', 'equal', 'number', 'count', 'sum', 'total', 'more', 'less'];
  return basicMath.includes(word);
}

function isAdvancedMath(word) {
  const advancedMath = ['calculus', 'derivative', 'integral', 'logarithm', 'trigonometry', 'polynomial', 'matrix', 'vector'];
  return advancedMath.includes(word);
}

function isScienceTerm(word, definition) {
  const scienceWords = ['atom', 'molecule', 'cell', 'DNA', 'gene', 'protein', 'enzyme', 'bacteria', 'virus', 'evolution', 'gravity', 'energy'];
  const scienceTerms = ['scientific', 'biological', 'chemical', 'physical', 'molecular', 'cellular', 'genetic'];
  return scienceWords.includes(word) || (definition && scienceTerms.some(term => definition.toLowerCase().includes(term)));
}

function isBasicScience(word) {
  const basicScience = ['water', 'air', 'plant', 'animal', 'rock', 'soil', 'sun', 'moon', 'star', 'weather', 'hot', 'cold'];
  return basicScience.includes(word);
}

async function assignGradeLevelsToAllWords() {
  console.log('=== ASSIGNING GRADE LEVELS TO ALL SPELLING WORDS ===\n');
  
  try {
    // Get total count for progress tracking
    const { count: totalWords } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });
    
    console.log(`Processing ${totalWords} words for grade level assignment...\n`);
    
    // Process in batches to avoid memory issues and provide progress updates
    const batchSize = 100;
    let processed = 0;
    const gradeDistribution = {};
    const processedWords = [];
    
    // Track progress file
    const timestamp = Date.now();
    const progressFile = `scripts/grade_level_assignment_progress_${timestamp}.json`;
    
    for (let offset = 0; offset < totalWords; offset += batchSize) {
      console.log(`Processing batch ${Math.floor(offset/batchSize) + 1}/${Math.ceil(totalWords/batchSize)} (words ${offset + 1}-${Math.min(offset + batchSize, totalWords)})`);
      
      // Get batch of words
      const { data: words, error } = await supabase
        .from('spelling_words')
        .select('id, word, definition, spelling_difficulty_level, vocabulary_difficulty_level')
        .range(offset, offset + batchSize - 1)
        .order('id');
        
      if (error) {
        console.error('Error fetching words:', error);
        continue;
      }
      
      // Process each word in the batch
      const updates = [];
      for (const word of words) {
        const gradeLevel = estimateGradeLevel(word);
        
        updates.push({
          id: word.id,
          grade_level: gradeLevel
        });
        
        // Track distribution
        gradeDistribution[gradeLevel] = (gradeDistribution[gradeLevel] || 0) + 1;
        processedWords.push({
          word: word.word,
          grade: gradeLevel,
          spelling_diff: word.spelling_difficulty_level,
          vocab_diff: word.vocabulary_difficulty_level
        });
        
        processed++;
      }
      
      // Batch update to database
      const { error: updateError } = await supabase
        .from('spelling_words')
        .upsert(updates, { onConflict: 'id' });
        
      if (updateError) {
        console.error(`Error updating batch starting at ${offset}:`, updateError);
      } else {
        console.log(`✅ Updated ${updates.length} words`);
      }
      
      // Save progress
      const progress = {
        processed,
        totalWords,
        percentage: ((processed / totalWords) * 100).toFixed(1),
        gradeDistribution,
        lastProcessedId: words[words.length - 1].id,
        timestamp: new Date().toISOString()
      };
      
      fs.writeFileSync(progressFile, JSON.stringify(progress, null, 2));
      
      // Small delay to avoid overwhelming the database
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    // Final summary
    console.log('\n=== GRADE LEVEL ASSIGNMENT COMPLETE ===\n');
    console.log(`Total words processed: ${processed}`);
    console.log('\nGrade Level Distribution:');
    
    const grades = ['K', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'];
    grades.forEach(grade => {
      const count = gradeDistribution[grade] || 0;
      const percentage = ((count / processed) * 100).toFixed(1);
      console.log(`${grade.padStart(2)}: ${count.toString().padStart(5)} words (${percentage.padStart(5)}%)`);
    });
    
    // Save final results
    const resultsFile = `scripts/grade_level_assignment_results_${timestamp}.json`;
    const results = {
      summary: {
        totalProcessed: processed,
        gradeDistribution,
        completedAt: new Date().toISOString()
      },
      sampleWords: processedWords.slice(0, 100) // First 100 as examples
    };
    
    fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
    console.log(`\nDetailed results saved to: ${resultsFile}`);
    
    return results;
    
  } catch (error) {
    console.error('Failed to assign grade levels:', error);
  }
}

if (require.main === module) {
  assignGradeLevelsToAllWords();
}

module.exports = { assignGradeLevelsToAllWords, estimateGradeLevel };