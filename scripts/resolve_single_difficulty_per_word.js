const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const csv = require('csv-parser');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function resolveSingleDifficultyPerWord() {
  console.log('=== RESOLVING TO ONE SCRIPPS DIFFICULTY PER WORD ===\n');

  try {
    // Step 1: Load and process CSV data
    console.log('Step 1: Loading CSV data...');
    const csvWords = await loadCSVData();
    console.log(`Loaded ${csvWords.length} total word entries from CSV`);
    
    // Step 2: Resolve to one difficulty per word (most recent year)
    console.log('\nStep 2: Resolving to most recent difficulty per word...');
    const resolvedWords = resolveMostRecentDifficulty(csvWords);
    console.log(`Resolved to ${resolvedWords.size} unique words with single difficulties`);
    
    // Step 3: Get current database words
    console.log('\nStep 3: Fetching current database words...');
    const dbWords = await getAllDatabaseWords();
    console.log(`Found ${dbWords.length} words in database`);
    
    // Step 4: Determine updates vs inserts
    console.log('\nStep 4: Categorizing updates vs new insertions...');
    const { updates, inserts } = categorizeUpdatesAndInserts(dbWords, resolvedWords);
    
    // Step 5: Generate SQL files
    console.log('\nStep 5: Generating SQL files...');
    generateFinalSQL(updates, inserts);
    
    // Step 6: Show summary
    displaySummary(resolvedWords, updates, inserts);
    
  } catch (error) {
    console.error('Error during resolution:', error);
  }
}

async function loadCSVData() {
  const csvPath = 'scripts/spelling_bee/output/proper_header_extraction_1755928335179.csv';
  const words = [];
  
  return new Promise((resolve, reject) => {
    fs.createReadStream(csvPath)
      .pipe(csv())
      .on('data', (row) => {
        const word = row.word?.toLowerCase()?.trim();
        if (word) {
          words.push({
            word,
            source_difficulty: row.source_difficulty?.trim(),
            source_year: parseInt(row.source_year?.trim()) || 2020,
            page_number: row.page_number?.trim(),
            source_file: row.source_file?.trim()
          });
        }
      })
      .on('end', () => resolve(words))
      .on('error', reject);
  });
}

function resolveMostRecentDifficulty(csvWords) {
  // Group words by word text
  const wordGroups = new Map();
  
  csvWords.forEach(entry => {
    if (!wordGroups.has(entry.word)) {
      wordGroups.set(entry.word, []);
    }
    wordGroups.get(entry.word).push(entry);
  });
  
  // For each word, pick the entry from the most recent year
  const resolvedWords = new Map();
  
  wordGroups.forEach((entries, word) => {
    if (entries.length === 1) {
      // Single entry, use as-is
      resolvedWords.set(word, entries[0]);
    } else {
      // Multiple entries - find most recent year
      // Sort by year descending, then by a tiebreaker if needed
      const sortedEntries = entries.sort((a, b) => {
        if (b.source_year !== a.source_year) {
          return b.source_year - a.source_year; // Most recent first
        }
        // If same year, prefer by difficulty order (Three Bee > Two Bee > One Bee for consistency)
        const difficultyOrder = { 'Three Bee': 3, 'Two Bee': 2, 'One Bee': 1 };
        return (difficultyOrder[b.source_difficulty] || 0) - (difficultyOrder[a.source_difficulty] || 0);
      });
      
      resolvedWords.set(word, sortedEntries[0]);
    }
  });
  
  return resolvedWords;
}

async function getAllDatabaseWords() {
  const words = [];
  const batchSize = 1000;
  let offset = 0;
  let hasMore = true;

  while (hasMore) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('id, word, source_difficulty')
      .range(offset, offset + batchSize - 1)
      .order('id');

    if (error) {
      throw new Error(`Error fetching database words: ${error.message}`);
    }

    if (batch && batch.length > 0) {
      batch.forEach(row => {
        words.push({
          id: row.id,
          word: row.word.toLowerCase().trim(),
          source_difficulty: row.source_difficulty
        });
      });
      offset += batchSize;
      hasMore = batch.length === batchSize;
    } else {
      hasMore = false;
    }
  }

  return words;
}

function categorizeUpdatesAndInserts(dbWords, resolvedWords) {
  // Create lookup map for database words
  const dbWordsMap = new Map();
  dbWords.forEach(word => {
    dbWordsMap.set(word.word, word);
  });

  const updates = [];
  const inserts = [];

  resolvedWords.forEach((resolvedWord, word) => {
    const dbEntry = dbWordsMap.get(word);
    
    if (dbEntry) {
      // Word exists in database
      if (dbEntry.source_difficulty !== resolvedWord.source_difficulty) {
        updates.push({
          id: dbEntry.id,
          word: word,
          old_source_difficulty: dbEntry.source_difficulty,
          new_source_difficulty: resolvedWord.source_difficulty,
          source_year: resolvedWord.source_year,
          source_file: resolvedWord.source_file
        });
      }
      // If difficulties match, no update needed
    } else {
      // New word to insert
      inserts.push(resolvedWord);
    }
  });

  return { updates, inserts };
}

function generateFinalSQL(updates, inserts) {
  const timestamp = Date.now();
  
  // Generate UPDATE SQL
  if (updates.length > 0) {
    const updateStatements = updates.map(update => 
      `UPDATE spelling_words SET source_difficulty = '${update.new_source_difficulty.replace(/'/g, "''")}' WHERE id = '${update.id}';`
    );

    const updateSQL = `scripts/final_update_source_difficulties_${timestamp}.sql`;
    const updateContent = `-- FINAL: Update source difficulties (one per word, most recent year)
-- Generated on ${new Date().toISOString()}
-- Updates: ${updates.length} words

BEGIN;

-- Update source difficulties to most recent year's difficulty
${updateStatements.join('\n')}

COMMIT;

-- Verification query
SELECT 
  source_difficulty, 
  COUNT(*) as count 
FROM spelling_words 
WHERE source_difficulty IS NOT NULL 
GROUP BY source_difficulty 
ORDER BY source_difficulty;`;

    fs.writeFileSync(updateSQL, updateContent);
    console.log(`✅ Final update SQL generated: ${updateSQL}`);
  }

  // Generate INSERT SQL  
  if (inserts.length > 0) {
    const insertStatements = inserts.map(word => {
      const escapedWord = word.word.replace(/'/g, "''");
      const escapedDifficulty = word.source_difficulty.replace(/'/g, "''");
      
      return `INSERT INTO spelling_words (word, source_difficulty) 
              VALUES ('${escapedWord}', '${escapedDifficulty}') 
              ON CONFLICT (word) DO NOTHING;`;
    });

    const insertSQL = `scripts/final_insert_new_words_${timestamp}.sql`;
    const insertContent = `-- FINAL: Insert new words (one difficulty per word)
-- Generated on ${new Date().toISOString()}  
-- New words: ${inserts.length}

BEGIN;

-- Insert new words with single difficulty assignments
${insertStatements.join('\n')}

COMMIT;

-- Verification queries
SELECT 'Total words after insert' as description, COUNT(*) as count FROM spelling_words;

SELECT 'Source difficulty distribution' as description, source_difficulty, COUNT(*) as count 
FROM spelling_words 
WHERE source_difficulty IS NOT NULL 
GROUP BY source_difficulty 
ORDER BY source_difficulty;`;

    fs.writeFileSync(insertSQL, insertContent);
    console.log(`✅ Final insert SQL generated: ${insertSQL}`);
  }
  
  // Generate verification script
  const verificationScript = `scripts/verify_final_spelling_update_${timestamp}.js`;
  const verificationContent = `const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyFinalUpdate() {
  console.log('=== VERIFICATION OF FINAL SPELLING WORDS UPDATE ===\\n');
  
  // Get total counts
  const { data: totals, error: totalsError } = await supabase
    .from('spelling_words')
    .select('COUNT(*)');
    
  if (!totalsError && totals) {
    console.log(\`Total words in database: \${totals[0].count}\`);
  }
  
  // Get source difficulty distribution
  let allWords = [];
  const batchSize = 1000;
  let offset = 0;
  let hasMore = true;

  while (hasMore) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('source_difficulty')
      .not('source_difficulty', 'is', null)
      .range(offset, offset + batchSize - 1);

    if (error) break;

    if (batch && batch.length > 0) {
      allWords = allWords.concat(batch);
      offset += batchSize;
      hasMore = batch.length === batchSize;
    } else {
      hasMore = false;
    }
  }
    
  if (allWords.length > 0) {
    const distribution = {};
    allWords.forEach(row => {
      distribution[row.source_difficulty] = (distribution[row.source_difficulty] || 0) + 1;
    });
    
    console.log('\\nFinal Source Difficulty Distribution:');
    Object.entries(distribution)
      .sort()
      .forEach(([diff, count]) => {
        const percentage = ((count / allWords.length) * 100).toFixed(1);
        console.log(\`  \${diff}: \${count} words (\${percentage}%)\`);
      });
      
    console.log(\`\\nTotal words with source difficulties: \${allWords.length}\`);
  }
  
  // Check for null difficulties
  const { data: nulls, error: nullError } = await supabase
    .from('spelling_words')
    .select('COUNT(*)')
    .is('source_difficulty', null);
    
  if (!nullError && nulls) {
    const nullCount = nulls[0].count;
    if (nullCount > 0) {
      console.log(\`\\n⚠️  \${nullCount} words still have null source_difficulty\`);
    } else {
      console.log('\\n✅ All words have source difficulties assigned!');
    }
  }
}

verifyFinalUpdate().then(() => process.exit(0)).catch(console.error);`;

  fs.writeFileSync(verificationScript, verificationContent);
  console.log(`📊 Final verification script generated: ${verificationScript}`);
}

function displaySummary(resolvedWords, updates, inserts) {
  console.log(`\n📊 FINAL RESOLUTION SUMMARY:`);
  console.log(`\n✅ Unique words with single difficulties: ${resolvedWords.size}`);
  console.log(`🔄 Updates needed: ${updates.length}`);
  console.log(`➕ New words to insert: ${inserts.length}`);
  
  // Show difficulty distribution of resolved words
  const difficultyDist = {};
  resolvedWords.forEach(word => {
    difficultyDist[word.source_difficulty] = (difficultyDist[word.source_difficulty] || 0) + 1;
  });
  
  console.log(`\n📈 Difficulty distribution of resolved words:`);
  Object.entries(difficultyDist)
    .sort()
    .forEach(([diff, count]) => {
      const percentage = ((count / resolvedWords.size) * 100).toFixed(1);
      console.log(`  ${diff}: ${count} words (${percentage}%)`);
    });
  
  // Show examples of resolved duplicates
  console.log(`\n🔍 Examples of duplicate resolution (showing most recent year chosen):`);
  let examples = 0;
  resolvedWords.forEach((resolved, word) => {
    if (examples < 10) {
      console.log(`  - "${word}": ${resolved.source_difficulty} (from ${resolved.source_year})`);
      examples++;
    }
  });
  
  console.log(`\n📋 Ready to execute:`);
  if (updates.length > 0) {
    console.log(`  1. Execute update SQL (${updates.length} updates)`);
  }
  if (inserts.length > 0) {
    console.log(`  2. Execute insert SQL (${inserts.length} new words)`);
  }
  console.log(`  3. Run verification script to confirm results`);
}

resolveSingleDifficultyPerWord();