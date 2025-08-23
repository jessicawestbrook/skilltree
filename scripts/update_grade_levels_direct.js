const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

// Import our grade level estimation function
function estimateGradeLevel(word) {
  const length = word.word.length;
  const spellingLevel = word.spelling_difficulty_level;
  const vocabLevel = word.vocabulary_difficulty_level;
  const definition = word.definition || '';
  const wordText = word.word.toLowerCase();
  
  let gradeScore = 0;
  
  if (spellingLevel === 1) gradeScore = 2;
  else if (spellingLevel === 2) gradeScore = 4;
  else if (spellingLevel === 3) gradeScore = 7;
  else if (spellingLevel === 4) gradeScore = 10;
  else if (spellingLevel === 5) gradeScore = 12;
  
  if (vocabLevel === 1) gradeScore = Math.min(gradeScore, 3);
  else if (vocabLevel === 2) gradeScore = Math.max(gradeScore - 1, 3);
  else if (vocabLevel === 3) gradeScore = Math.max(gradeScore, 6);
  else if (vocabLevel === 4) gradeScore = Math.max(gradeScore, 9);
  else if (vocabLevel === 5) gradeScore = Math.max(gradeScore, 11);
  
  if (length <= 3) {
    if (isBasicSightWord(wordText) || hasSimpleCVCPattern(wordText)) {
      gradeScore = Math.min(gradeScore, 1);
    } else {
      gradeScore = Math.min(gradeScore, 2);
    }
  } else if (length <= 4) {
    gradeScore = Math.min(gradeScore, 3);
  } else if (length <= 5) {
    gradeScore = Math.min(gradeScore, 5);
  } else if (length >= 12) {
    gradeScore = Math.max(gradeScore, 8);
  } else if (length >= 10) {
    gradeScore = Math.max(gradeScore, 7);
  }
  
  if (isBasicSightWord(wordText)) return 'K';
  else if (hasSimpleCVCPattern(wordText) && length <= 4) gradeScore = Math.min(gradeScore, 1);
  else if (hasSimplePhonicPattern(wordText) && length <= 5) gradeScore = Math.min(gradeScore, 2);
  
  if (hasComplexPattern(wordText)) gradeScore = Math.max(gradeScore, 6);
  
  if (definition) {
    if (isSimpleDefinition(definition)) gradeScore = Math.min(gradeScore, 4);
    else if (isTechnicalDefinition(definition)) gradeScore = Math.max(gradeScore, 9);
    else if (isAcademicDefinition(definition)) gradeScore = Math.max(gradeScore, 6);
  }
  
  gradeScore = Math.max(0, Math.min(12, gradeScore));
  
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

function isBasicSightWord(word) {
  const kindergartenWords = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with', 'you'];
  const grade1Words = ['all', 'any', 'can', 'had', 'her', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'];
  return kindergartenWords.includes(word) || grade1Words.includes(word);
}

function hasSimpleCVCPattern(word) {
  return /^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]$/.test(word) && word.length === 3;
}

function hasSimplePhonicPattern(word) {
  return /^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]e?$/.test(word) && word.length <= 5;
}

function hasComplexPattern(word) {
  const complexPatterns = [/ough/, /augh/, /eigh/, /tion/, /sion/, /cian/, /ph/, /gh/, /kn/, /wr/, /mb$/, /gn/, /ps/, /rh/, /sch/, /tch/, /dge/];
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
  const academicTerms = ['analyze', 'concept', 'theory', 'principle', 'method', 'process', 'system', 'structure', 'function', 'relationship'];
  return academicTerms.some(term => definition.toLowerCase().includes(term));
}

function isTechnicalDefinition(definition) {
  if (!definition) return false;
  const technicalTerms = ['scientific', 'medical', 'technical', 'specialized', 'professional', 'engineering', 'mathematical', 'chemical', 'biological'];
  return technicalTerms.some(term => definition.toLowerCase().includes(term));
}

async function updateGradeLevelsDirectSQL() {
  console.log('=== UPDATING GRADE LEVELS WITH DIRECT SQL ===\n');
  
  try {
    // First, let's create the SQL statements file
    console.log('Generating SQL update statements...');
    
    // Get all words with their difficulty data (no limit)
    console.log('Fetching all words from database...');
    let allWords = [];
    const batchSize = 1000;
    let offset = 0;
    let hasMore = true;

    while (hasMore) {
      const { data: batch, error } = await supabase
        .from('spelling_words')
        .select('id, word, definition, spelling_difficulty_level, vocabulary_difficulty_level')
        .range(offset, offset + batchSize - 1)
        .order('id');

      if (error) {
        console.error('Error fetching words:', error);
        return;
      }

      if (batch && batch.length > 0) {
        allWords = allWords.concat(batch);
        console.log(`Fetched ${allWords.length} words so far...`);
        offset += batchSize;
        hasMore = batch.length === batchSize;
      } else {
        hasMore = false;
      }
    }
    
    console.log(`Processing ${allWords.length} words...`);
    
    // Generate SQL update statements
    const sqlStatements = [];
    const gradeDistribution = {};
    
    for (const word of allWords) {
      const gradeLevel = estimateGradeLevel(word);
      gradeDistribution[gradeLevel] = (gradeDistribution[gradeLevel] || 0) + 1;
      
      // Create SQL update statement
      const sqlUpdate = `UPDATE spelling_words SET grade_level = '${gradeLevel}' WHERE id = '${word.id}';`;
      sqlStatements.push(sqlUpdate);
    }
    
    // Write SQL file
    const timestamp = Date.now();
    const sqlFile = `scripts/update_all_grade_levels_${timestamp}.sql`;
    
    const sqlContent = `-- Update all spelling words with grade levels
-- Generated on ${new Date().toISOString()}
-- Total words: ${allWords.length}

BEGIN;

-- First ensure column exists
ALTER TABLE spelling_words ADD COLUMN IF NOT EXISTS grade_level TEXT;

-- Update all grade levels
${sqlStatements.join('\n')}

COMMIT;

-- Verify results
SELECT grade_level, COUNT(*) as count 
FROM spelling_words 
WHERE grade_level IS NOT NULL 
GROUP BY grade_level 
ORDER BY 
  CASE 
    WHEN grade_level = 'K' THEN 0
    ELSE CAST(grade_level AS INTEGER)
  END;`;
    
    fs.writeFileSync(sqlFile, sqlContent);
    
    console.log('\nGrade Level Distribution (calculated):');
    const grades = ['K', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'];
    grades.forEach(grade => {
      const count = gradeDistribution[grade] || 0;
      const percentage = ((count / allWords.length) * 100).toFixed(1);
      console.log(`${grade.padStart(2)}: ${count.toString().padStart(5)} words (${percentage.padStart(5)}%)`);
    });
    
    console.log(`\n✅ SQL file generated: ${sqlFile}`);
    console.log('\n📋 Next steps:');
    console.log('1. Open your Supabase SQL Editor');
    console.log('2. Copy and paste the contents of the SQL file');
    console.log('3. Execute the SQL to update all grade levels');
    console.log('4. Run the verification query at the end to confirm results');
    
    // Save summary
    const summaryFile = `scripts/grade_level_sql_summary_${timestamp}.json`;
    fs.writeFileSync(summaryFile, JSON.stringify({
      totalWords: allWords.length,
      gradeDistribution,
      sqlFile,
      generatedAt: new Date().toISOString()
    }, null, 2));
    
    console.log(`\n📊 Summary saved: ${summaryFile}`);
    
  } catch (error) {
    console.error('Failed to generate SQL updates:', error);
  }
}

if (require.main === module) {
  updateGradeLevelsDirectSQL();
}