const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const csv = require('csv-parser');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function safeUpdateSpellingWords() {
  console.log('=== SAFE UPDATE OF SPELLING WORDS DATABASE ===\n');

  try {
    const timestamp = Date.now();
    
    // Step 1: Create backup table
    console.log('Step 1: Creating backup table...');
    await createBackupTable(timestamp);
    
    // Step 2: Load new data from CSV
    console.log('\nStep 2: Loading new data from CSV...');
    const newWordsData = await loadCSVData();
    console.log(`Loaded ${newWordsData.length} words from CSV`);
    
    // Step 3: Get existing words from database
    console.log('\nStep 3: Fetching existing words from database...');
    const existingWords = await getAllExistingWords();
    console.log(`Found ${existingWords.length} existing words in database`);
    
    // Step 4: Categorize updates vs inserts
    console.log('\nStep 4: Analyzing updates vs new insertions...');
    const { updates, inserts } = categorizeWords(existingWords, newWordsData);
    console.log(`Updates needed: ${updates.length}`);
    console.log(`New words to insert: ${inserts.length}`);
    
    // Step 5: Generate SQL for updates and inserts
    console.log('\nStep 5: Generating SQL statements...');
    const { updateSQL, insertSQL } = generateSQL(updates, inserts, timestamp);
    
    console.log(`\n✅ SQL files generated:`);
    console.log(`📄 Update SQL: ${updateSQL}`);
    console.log(`📄 Insert SQL: ${insertSQL}`);
    
    console.log(`\n📋 Next steps:`);
    console.log(`1. Review the SQL files to verify correctness`);
    console.log(`2. Execute the update SQL first to fix source difficulties`);
    console.log(`3. Execute the insert SQL to add new words`);
    console.log(`4. Run verification queries to confirm results`);
    
    // Step 6: Generate verification script
    await generateVerificationScript(timestamp);
    
  } catch (error) {
    console.error('Error during safe update:', error);
  }
}

async function createBackupTable(timestamp) {
  // Check if backup tables already exist and find next increment
  const backupName = await findNextBackupName();
  
  console.log(`Creating backup table: spelling_words_${backupName}`);
  
  const backupSQL = `-- Create backup table before updating
-- Generated on ${new Date().toISOString()}

-- Create backup table
CREATE TABLE spelling_words_${backupName} AS SELECT * FROM spelling_words;

-- Verify backup was created
SELECT 
  '${backupName}' as backup_name,
  COUNT(*) as word_count,
  COUNT(DISTINCT source_difficulty) as unique_difficulties,
  MIN(created_at) as oldest_entry,
  MAX(created_at) as newest_entry
FROM spelling_words_${backupName};`;

  const backupFile = `scripts/backup_spelling_words_${timestamp}.sql`;
  fs.writeFileSync(backupFile, backupSQL);
  
  console.log(`✅ Backup SQL generated: ${backupFile}`);
  console.log(`⚠️  IMPORTANT: Execute this backup SQL first before proceeding!`);
  
  return backupName;
}

async function findNextBackupName() {
  // Try to find existing backup tables to determine next increment
  try {
    const { data: bkp, error: bkpError } = await supabase
      .from('spelling_words_bkp')
      .select('COUNT(*)')
      .limit(1);
    
    if (!bkpError) {
      // bkp exists, try bkp2
      const { data: bkp2, error: bkp2Error } = await supabase
        .from('spelling_words_bkp2')
        .select('COUNT(*)')
        .limit(1);
      
      if (!bkp2Error) {
        // bkp2 exists, try bkp3, etc.
        const { data: bkp3, error: bkp3Error } = await supabase
          .from('spelling_words_bkp3')
          .select('COUNT(*)')
          .limit(1);
        
        if (!bkp3Error) {
          // Keep going...
          return 'bkp4';
        } else {
          return 'bkp3';
        }
      } else {
        return 'bkp2';
      }
    } else {
      return 'bkp';
    }
  } catch (error) {
    return 'bkp';
  }
}

async function loadCSVData() {
  const csvPath = 'scripts/spelling_bee/output/proper_header_extraction_1755928335179.csv';
  
  if (!fs.existsSync(csvPath)) {
    throw new Error(`CSV file not found: ${csvPath}`);
  }

  const words = [];
  
  return new Promise((resolve, reject) => {
    fs.createReadStream(csvPath)
      .pipe(csv())
      .on('data', (row) => {
        words.push({
          word: row.word?.toLowerCase()?.trim(),
          source_difficulty: row.source_difficulty?.trim(),
          source_year: row.source_year?.trim(),
          page_number: row.page_number?.trim(),
          source_file: row.source_file?.trim()
        });
      })
      .on('end', () => resolve(words))
      .on('error', reject);
  });
}

async function getAllExistingWords() {
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
      throw new Error(`Error fetching existing words: ${error.message}`);
    }

    if (batch && batch.length > 0) {
      words.push(...batch);
      offset += batchSize;
      hasMore = batch.length === batchSize;
    } else {
      hasMore = false;
    }
  }

  return words;
}

function categorizeWords(existingWords, newWordsData) {
  // Create lookup map for existing words
  const existingWordsMap = new Map();
  existingWords.forEach(word => {
    existingWordsMap.set(word.word.toLowerCase(), {
      id: word.id,
      current_source_difficulty: word.source_difficulty
    });
  });

  const updates = [];
  const inserts = [];

  newWordsData.forEach(newWord => {
    if (!newWord.word) return; // Skip invalid entries
    
    const existing = existingWordsMap.get(newWord.word);
    
    if (existing) {
      // Word exists - check if source_difficulty needs updating
      if (existing.current_source_difficulty !== newWord.source_difficulty) {
        updates.push({
          id: existing.id,
          word: newWord.word,
          old_source_difficulty: existing.current_source_difficulty,
          new_source_difficulty: newWord.source_difficulty,
          source_year: newWord.source_year,
          page_number: newWord.page_number,
          source_file: newWord.source_file
        });
      }
      // If source_difficulty is already correct, no update needed
    } else {
      // New word - needs to be inserted
      inserts.push(newWord);
    }
  });

  return { updates, inserts };
}

function generateSQL(updates, inserts, timestamp) {
  // Generate UPDATE SQL
  const updateStatements = updates.map(update => 
    `UPDATE spelling_words SET source_difficulty = '${update.new_source_difficulty}' WHERE id = '${update.id}';`
  );

  const updateSQL = `scripts/update_source_difficulties_${timestamp}.sql`;
  const updateContent = `-- Update source difficulties for existing words
-- Generated on ${new Date().toISOString()}
-- Updates: ${updates.length} words

BEGIN;

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

  // Generate INSERT SQL
  const insertStatements = inserts.map(word => {
    // Escape single quotes in strings
    const escapedWord = word.word.replace(/'/g, "''");
    const escapedDifficulty = word.source_difficulty.replace(/'/g, "''");
    const escapedFile = word.source_file?.replace(/'/g, "''") || '';
    
    return `INSERT INTO spelling_words (word, source_difficulty) VALUES ('${escapedWord}', '${escapedDifficulty}');`;
  });

  const insertSQL = `scripts/insert_new_words_${timestamp}.sql`;
  const insertContent = `-- Insert new words from Scripps extraction
-- Generated on ${new Date().toISOString()}  
-- New words: ${inserts.length}

BEGIN;

${insertStatements.join('\n')}

COMMIT;

-- Verification query
SELECT 
  COUNT(*) as total_words_after_insert,
  COUNT(CASE WHEN source_difficulty IS NOT NULL THEN 1 END) as words_with_source_difficulty
FROM spelling_words;`;

  fs.writeFileSync(insertSQL, insertContent);

  return { updateSQL, insertSQL };
}

async function generateVerificationScript(timestamp) {
  const verificationScript = `scripts/verify_spelling_update_${timestamp}.js`;
  const verificationContent = `const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyUpdate() {
  console.log('=== VERIFICATION OF SPELLING WORDS UPDATE ===\\n');
  
  // Get total counts
  const { data: totals, error: totalsError } = await supabase
    .from('spelling_words')
    .select('COUNT(*)');
    
  if (!totalsError && totals) {
    console.log(\`Total words in database: \${totals[0].count}\`);
  }
  
  // Get source difficulty distribution
  const { data: difficulties, error: diffError } = await supabase
    .from('spelling_words')
    .select('source_difficulty')
    .not('source_difficulty', 'is', null);
    
  if (!diffError && difficulties) {
    const distribution = {};
    difficulties.forEach(row => {
      distribution[row.source_difficulty] = (distribution[row.source_difficulty] || 0) + 1;
    });
    
    console.log('\\nSource Difficulty Distribution:');
    Object.entries(distribution)
      .sort((a, b) => b[1] - a[1])
      .forEach(([diff, count]) => {
        console.log(\`  \${diff}: \${count} words\`);
      });
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

verifyUpdate().then(() => process.exit(0)).catch(console.error);`;

  fs.writeFileSync(verificationScript, verificationContent);
  console.log(`📊 Verification script generated: ${verificationScript}`);
}

safeUpdateSpellingWords();