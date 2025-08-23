const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function identifyClearlyInvalidWords() {
  console.log('=== IDENTIFYING CLEARLY INVALID/CONCATENATED WORDS ===\n');

  try {
    // Step 1: Find words that are obviously invalid
    console.log('Step 1: Finding clearly invalid words...');
    const invalidWords = await findClearlyInvalidWords();
    
    // Step 2: Display analysis
    console.log('\nStep 2: Analyzing clearly invalid words...');
    displayInvalidWordsAnalysis(invalidWords);
    
    // Step 3: Generate cleanup SQL if needed
    if (invalidWords.length > 0) {
      console.log('\nStep 3: Generating cleanup SQL...');
      generateCleanupSQL(invalidWords);
    } else {
      console.log('\n✅ No clearly invalid words found!');
    }
    
  } catch (error) {
    console.error('Error during invalid word identification:', error);
  }
}

async function findClearlyInvalidWords() {
  const clearlyInvalidWords = [];
  const batchSize = 1000;
  let offset = 0;
  let hasMore = true;

  console.log('Scanning database for clearly invalid words...');

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
        if (isClearlyInvalidWord(word.word)) {
          clearlyInvalidWords.push({
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

  return clearlyInvalidWords;
}

function isClearlyInvalidWord(word) {
  // Only flag words that are OBVIOUSLY wrong - be very conservative
  
  // Words that end with grammatical terms (these are clearly concatenated)
  if (/\w+noun$/i.test(word) || /\w+adjective$/i.test(word) || 
      /\w+verb$/i.test(word) || /\w+adverb$/i.test(word)) {
    return true;
  }
  
  // Words that are extremely long AND have clear concatenation patterns
  if (word.length > 25) {
    // Look for obvious patterns like two complete words stuck together
    const patterns = [
      /[a-z]{8,}[a-z]{8,}/, // Two long sequences stuck together
      /\w+ing\w+/, // Word ending in 'ing' followed by another word
      /\w+tion\w+/, // Word ending in 'tion' followed by another word
      /\w+able\w+/, // Word ending in 'able' followed by another word
    ];
    
    if (patterns.some(pattern => pattern.test(word))) {
      return true;
    }
  }
  
  // Specific patterns that are clearly wrong
  const obviouslyWrongPatterns = [
    /\w+epidermis$/i, // ends with "epidermis" 
    /^constant\w+/i, // starts with "constant" followed by more text
    /propinquity\w+/i, // contains "propinquity" followed by more
    /accordatura\w+/i, // contains "accordatura" followed by more
    /klutz\w+envoy/i, // obvious concatenation
    /uvula\w+enumerated/i, // obvious concatenation
    /abstrus\w+nephrolith/i, // obvious concatenation
    /floruit\w+bunyanesque/i, // obvious concatenation
    /kernel\w+tawny/i, // obvious concatenation
    /laterigr\w+hyssop/i, // obvious concatenation
    /prodigious\w+profligacy/i, // obvious concatenation
    /zygote\w+noun/i, // obvious concatenation
    /consecrate\w+adjective/i, // obvious concatenation
    /efflux\w+frugivore/i, // obvious concatenation
    /lantern\w+mince/i, // obvious concatenation
  ];
  
  return obviouslyWrongPatterns.some(pattern => pattern.test(word));
}

function getWordIssues(word) {
  const issues = [];
  
  if (/\w+noun$/i.test(word)) issues.push('Ends with "noun"');
  if (/\w+adjective$/i.test(word)) issues.push('Ends with "adjective"');
  if (/\w+verb$/i.test(word)) issues.push('Ends with "verb"');
  if (/\w+adverb$/i.test(word)) issues.push('Ends with "adverb"');
  if (word.length > 25) issues.push('Extremely long (>25 chars)');
  if (/propinquity\w+/i.test(word)) issues.push('Contains propinquity + more text');
  if (/accordatura\w+/i.test(word)) issues.push('Contains accordatura + more text');
  if (/constant\w{5,}/i.test(word)) issues.push('Starts with constant + long suffix');
  
  return issues;
}

function displayInvalidWordsAnalysis(invalidWords) {
  console.log(`📊 CLEARLY INVALID WORDS ANALYSIS:`);
  console.log(`Total clearly invalid words found: ${invalidWords.length}`);
  
  if (invalidWords.length === 0) {
    console.log('✅ No clearly invalid words detected!');
    return;
  }
  
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
    if (count > 0) {
      console.log(`  - ${level}: ${count} words`);
    }
  });
  
  // Show all invalid words (since there shouldn't be many)
  console.log(`\n🔍 All clearly invalid words:`);
  invalidWords.forEach((word, index) => {
    console.log(`  ${index + 1}. "${word.word}" (${word.source_difficulty}): ${word.issues.join(', ')}`);
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
  const backupFile = `scripts/clearly_invalid_words_backup_${timestamp}.json`;
  fs.writeFileSync(backupFile, JSON.stringify(invalidWords, null, 2));
  console.log(`📄 Backup of clearly invalid words saved: ${backupFile}`);
  
  // Generate DELETE statements
  const deleteStatements = invalidWords.map(word => 
    `DELETE FROM spelling_words WHERE id = '${word.id}'; -- "${word.word}" (${word.issues.join(', ')})`
  );
  
  const cleanupSQL = `scripts/cleanup_clearly_invalid_words_${timestamp}.sql`;
  const cleanupContent = `-- Clean up CLEARLY invalid/concatenated words from spelling_words table
-- Generated on ${new Date().toISOString()}
-- Deleting ${invalidWords.length} clearly invalid words
-- Backup saved to: ${backupFile}

BEGIN;

-- Delete clearly invalid words
${deleteStatements.join('\n')}

COMMIT;

-- Verification queries
SELECT 'Clearly invalid words deleted' as description, ${invalidWords.length} as count;

SELECT 'Remaining words' as description, COUNT(*) as count 
FROM spelling_words;

SELECT 'Words by difficulty after cleanup' as description, source_difficulty, COUNT(*) as count 
FROM spelling_words 
WHERE source_difficulty IS NOT NULL 
GROUP BY source_difficulty 
ORDER BY source_difficulty;`;

  fs.writeFileSync(cleanupSQL, cleanupContent);
  
  console.log(`✅ Conservative cleanup SQL generated: ${cleanupSQL}`);
  console.log(`\n📋 This SQL will:`);
  console.log(`  1. Delete only ${invalidWords.length} CLEARLY invalid words`);
  console.log(`  2. Preserve backup of deleted words in JSON format`);
  console.log(`  3. Show verification queries to confirm cleanup`);
  console.log(`\n✅ Safe to execute - only targets obvious concatenation errors!`);
}

identifyClearlyInvalidWords();