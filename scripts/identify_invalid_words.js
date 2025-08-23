const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function identifyInvalidWords() {
  console.log('=== IDENTIFYING INVALID/CONCATENATED WORDS ===\n');

  try {
    // Step 1: Find words that are likely invalid
    console.log('Step 1: Finding potentially invalid words...');
    const invalidWords = await findInvalidWords();
    
    // Step 2: Display analysis
    console.log('\nStep 2: Analyzing invalid words...');
    displayInvalidWordsAnalysis(invalidWords);
    
    // Step 3: Generate cleanup SQL
    console.log('\nStep 3: Generating cleanup SQL...');
    generateCleanupSQL(invalidWords);
    
  } catch (error) {
    console.error('Error during invalid word identification:', error);
  }
}

async function findInvalidWords() {
  const suspiciousWords = [];
  const batchSize = 1000;
  let offset = 0;
  let hasMore = true;

  console.log('Scanning database for suspicious words...');

  while (hasMore) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition, source_difficulty')
      .range(offset, offset + batchSize - 1)
      .order('id');

    if (error) {
      throw new Error(`Error fetching words: ${error.message}`);
    }

    if (batch && batch.length > 0) {
      batch.forEach(word => {
        if (isLikelyInvalidWord(word.word)) {
          suspiciousWords.push({
            id: word.id,
            word: word.word,
            definition: word.definition,
            source_difficulty: word.source_difficulty,
            issues: getWordIssues(word.word)
          });
        }
      });

      console.log(`Processed ${offset + batch.length} words so far...`);
      offset += batchSize;
      hasMore = batch.length === batchSize;
    } else {
      hasMore = false;
    }
  }

  return suspiciousWords;
}

function isLikelyInvalidWord(word) {
  // Check for various signs of invalid/concatenated words
  
  // Very long words (likely concatenated)
  if (word.length > 20) return true;
  
  // Contains common word endings that suggest concatenation
  if (word.includes('adjective') || word.includes('noun') || word.includes('verb')) return true;
  
  // Multiple capital letters in middle (like "constantBalm")
  if (/[a-z][A-Z]/.test(word)) return true;
  
  // Looks like multiple words stuck together (simple heuristic)
  const commonWordParts = ['the', 'and', 'ing', 'tion', 'able', 'ment', 'ness', 'less', 'ful'];
  let suspiciousPatternCount = 0;
  commonWordParts.forEach(part => {
    if (word.includes(part) && word !== part) {
      suspiciousPatternCount++;
    }
  });
  
  // Contains multiple recognizable word patterns
  if (suspiciousPatternCount >= 2 && word.length > 15) return true;
  
  // Contains obvious concatenations
  const obviousConcatenations = [
    /\w{5,}\w{5,}/, // Two long word parts stuck together
    /[a-z]{3,}[A-Z][a-z]{3,}/, // camelCase pattern
    /\w+noun$/i,
    /\w+adjective$/i,
    /\w+verb$/i,
    /\w+adverb$/i
  ];
  
  return obviousConcatenations.some(pattern => pattern.test(word));
}

function getWordIssues(word) {
  const issues = [];
  
  if (word.length > 20) issues.push('Very long (>20 chars)');
  if (word.includes('adjective') || word.includes('noun') || word.includes('verb')) {
    issues.push('Contains grammatical terms');
  }
  if (/[a-z][A-Z]/.test(word)) issues.push('Mixed case (likely concatenated)');
  if (/\w+noun$/i.test(word)) issues.push('Ends with "noun"');
  if (/\w+adjective$/i.test(word)) issues.push('Ends with "adjective"');
  if (/\w+verb$/i.test(word)) issues.push('Ends with "verb"');
  
  return issues;
}

function displayInvalidWordsAnalysis(invalidWords) {
  console.log(`\n📊 INVALID WORDS ANALYSIS:`);
  console.log(`Total suspicious words found: ${invalidWords.length}`);
  
  // Group by difficulty
  const byDifficulty = {
    'One Bee': 0,
    'Two Bee': 0,
    'Three Bee': 0,
    'Other': 0
  };
  
  invalidWords.forEach(word => {
    if (['One Bee', 'Two Bee', 'Three Bee'].includes(word.source_difficulty)) {
      byDifficulty[word.source_difficulty]++;
    } else {
      byDifficulty['Other']++;
    }
  });
  
  console.log(`\n📈 By difficulty level:`);
  Object.entries(byDifficulty).forEach(([level, count]) => {
    console.log(`  - ${level}: ${count} words`);
  });
  
  // Show examples by issue type
  console.log(`\n🔍 Examples of invalid words (first 20):`);
  invalidWords.slice(0, 20).forEach(word => {
    console.log(`  - "${word.word}" (${word.source_difficulty}): ${word.issues.join(', ')}`);
  });
  
  // Count by issue type
  const issueTypes = {};
  invalidWords.forEach(word => {
    word.issues.forEach(issue => {
      issueTypes[issue] = (issueTypes[issue] || 0) + 1;
    });
  });
  
  console.log(`\n📋 Issue types:`);
  Object.entries(issueTypes)
    .sort((a, b) => b[1] - a[1])
    .forEach(([issue, count]) => {
      console.log(`  - ${issue}: ${count} words`);
    });
}

function generateCleanupSQL(invalidWords) {
  const timestamp = Date.now();
  
  // Create backup of words we're about to delete
  const backupFile = `scripts/invalid_words_backup_${timestamp}.json`;
  fs.writeFileSync(backupFile, JSON.stringify(invalidWords, null, 2));
  console.log(`📄 Backup of invalid words saved: ${backupFile}`);
  
  // Generate DELETE statements
  const deleteStatements = invalidWords.map(word => 
    `DELETE FROM spelling_words WHERE id = '${word.id}'; -- "${word.word}"`
  );
  
  const cleanupSQL = `scripts/cleanup_invalid_words_${timestamp}.sql`;
  const cleanupContent = `-- Clean up invalid/concatenated words from spelling_words table
-- Generated on ${new Date().toISOString()}
-- Deleting ${invalidWords.length} invalid words
-- Backup saved to: ${backupFile}

BEGIN;

-- Delete invalid words
${deleteStatements.join('\n')}

COMMIT;

-- Verification queries
SELECT 'Words deleted' as description, ${invalidWords.length} as count;

SELECT 'Remaining words' as description, COUNT(*) as count 
FROM spelling_words;

SELECT 'Words by difficulty after cleanup' as description, source_difficulty, COUNT(*) as count 
FROM spelling_words 
WHERE source_difficulty IS NOT NULL 
GROUP BY source_difficulty 
ORDER BY source_difficulty;`;

  fs.writeFileSync(cleanupSQL, cleanupContent);
  
  console.log(`✅ Cleanup SQL generated: ${cleanupSQL}`);
  console.log(`\n📋 This SQL will:`);
  console.log(`  1. Delete ${invalidWords.length} invalid/concatenated words`);
  console.log(`  2. Preserve backup of deleted words in JSON format`);
  console.log(`  3. Show verification queries to confirm cleanup`);
  console.log(`\n⚠️  Review the backup file before executing the cleanup SQL!`);
}

identifyInvalidWords();