const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const csv = require('csv-parser');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkForDuplicates() {
  console.log('=== CHECKING FOR POTENTIAL DUPLICATE WORDS ===\n');

  try {
    // Step 1: Load CSV data
    console.log('Loading CSV data...');
    const csvWords = await loadCSVData();
    console.log(`Loaded ${csvWords.length} words from CSV`);
    
    // Step 2: Get current database words (including any recent changes)
    console.log('\nFetching current database words...');
    const dbWords = await getAllDatabaseWords();
    console.log(`Found ${dbWords.length} words in database`);
    
    // Step 3: Check for duplicates
    console.log('\nAnalyzing for duplicates...');
    const duplicateAnalysis = analyzeForDuplicates(dbWords, csvWords);
    
    // Step 4: Display results
    displayDuplicateAnalysis(duplicateAnalysis);
    
    // Step 5: Generate safe insert SQL
    if (duplicateAnalysis.safeToInsert.length > 0) {
      generateSafeInsertSQL(duplicateAnalysis.safeToInsert);
    }
    
  } catch (error) {
    console.error('Error during duplicate check:', error);
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
            source_year: row.source_year?.trim(),
            page_number: row.page_number?.trim(),
            source_file: row.source_file?.trim()
          });
        }
      })
      .on('end', () => resolve(words))
      .on('error', reject);
  });
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

function analyzeForDuplicates(dbWords, csvWords) {
  // Create lookup sets for fast checking
  const dbWordSet = new Set(dbWords.map(w => w.word));
  
  // Track various categories
  const exactDuplicates = [];
  const safeToInsert = [];
  const csvDuplicatesWithinCSV = [];
  
  // Check for duplicates within CSV first
  const csvWordCounts = {};
  csvWords.forEach(word => {
    csvWordCounts[word.word] = (csvWordCounts[word.word] || 0) + 1;
  });
  
  const csvDuplicateWords = Object.keys(csvWordCounts).filter(word => csvWordCounts[word] > 1);
  
  // Analyze each CSV word
  csvWords.forEach(csvWord => {
    if (dbWordSet.has(csvWord.word)) {
      exactDuplicates.push({
        word: csvWord.word,
        csv_source_difficulty: csvWord.source_difficulty,
        db_entry: dbWords.find(w => w.word === csvWord.word)
      });
    } else {
      // Check if this word appears multiple times in CSV
      if (csvWordCounts[csvWord.word] > 1) {
        if (!csvDuplicatesWithinCSV.find(d => d.word === csvWord.word)) {
          csvDuplicatesWithinCSV.push({
            word: csvWord.word,
            count: csvWordCounts[csvWord.word],
            entries: csvWords.filter(w => w.word === csvWord.word)
          });
        }
      } else {
        safeToInsert.push(csvWord);
      }
    }
  });
  
  return {
    exactDuplicates,
    safeToInsert,
    csvDuplicatesWithinCSV,
    csvDuplicateWords
  };
}

function displayDuplicateAnalysis(analysis) {
  console.log(`\n📊 DUPLICATE ANALYSIS RESULTS:`);
  console.log(`\n✅ Safe to insert: ${analysis.safeToInsert.length} words`);
  console.log(`⚠️  Exact duplicates (already in DB): ${analysis.exactDuplicates.length} words`);
  console.log(`🔄 Duplicates within CSV: ${analysis.csvDuplicatesWithinCSV.length} unique words`);
  
  if (analysis.exactDuplicates.length > 0) {
    console.log(`\n📋 First 10 exact duplicates (already in database):`);
    analysis.exactDuplicates.slice(0, 10).forEach(dup => {
      console.log(`  - "${dup.word}": DB has "${dup.db_entry.source_difficulty}", CSV has "${dup.csv_source_difficulty}"`);
    });
  }
  
  if (analysis.csvDuplicatesWithinCSV.length > 0) {
    console.log(`\n🔄 Words that appear multiple times in CSV:`);
    analysis.csvDuplicatesWithinCSV.slice(0, 10).forEach(dup => {
      console.log(`  - "${dup.word}": appears ${dup.count} times`);
      dup.entries.slice(0, 3).forEach(entry => {
        console.log(`    * ${entry.source_difficulty} (${entry.source_file}, page ${entry.page_number})`);
      });
    });
    
    if (analysis.csvDuplicatesWithinCSV.length > 10) {
      console.log(`    ... and ${analysis.csvDuplicatesWithinCSV.length - 10} more duplicated words`);
    }
  }
  
  console.log(`\n📈 Summary:`);
  console.log(`  Total unique words in CSV: ${new Set(analysis.exactDuplicates.concat(analysis.safeToInsert).map(w => w.word)).size}`);
  console.log(`  Words already in database: ${analysis.exactDuplicates.length}`);
  console.log(`  New words to insert: ${analysis.safeToInsert.length}`);
  console.log(`  CSV internal duplicates to resolve: ${analysis.csvDuplicatesWithinCSV.length}`);
}

async function generateSafeInsertSQL(safeWords) {
  const timestamp = Date.now();
  
  // Remove any potential duplicates within safe words (just in case)
  const uniqueWords = [];
  const seen = new Set();
  
  safeWords.forEach(word => {
    if (!seen.has(word.word)) {
      seen.add(word.word);
      uniqueWords.push(word);
    }
  });
  
  console.log(`\n📝 Generating safe insert SQL for ${uniqueWords.length} unique words...`);
  
  const insertStatements = uniqueWords.map(word => {
    const escapedWord = word.word.replace(/'/g, "''");
    const escapedDifficulty = word.source_difficulty.replace(/'/g, "''");
    
    // Use INSERT ... ON CONFLICT DO NOTHING for extra safety
    return `INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('${escapedWord}', '${escapedDifficulty}') 
            ON CONFLICT (word) DO NOTHING;`;
  });

  const safeInsertSQL = `scripts/safe_insert_new_words_${timestamp}.sql`;
  const insertContent = `-- SAFE INSERT: New words with duplicate prevention
-- Generated on ${new Date().toISOString()}  
-- Unique new words: ${uniqueWords.length}
-- Uses ON CONFLICT DO NOTHING for safety

BEGIN;

-- Insert new words, skip if word already exists
${insertStatements.join('\n')}

COMMIT;

-- Verification queries
SELECT 'Total words after safe insert' as description, COUNT(*) as count FROM spelling_words;

SELECT 'Words with source difficulties' as description, COUNT(*) as count 
FROM spelling_words WHERE source_difficulty IS NOT NULL;

SELECT 'Source difficulty distribution' as description, source_difficulty, COUNT(*) as count 
FROM spelling_words 
WHERE source_difficulty IS NOT NULL 
GROUP BY source_difficulty 
ORDER BY source_difficulty;`;

  fs.writeFileSync(safeInsertSQL, insertContent);
  console.log(`✅ Safe insert SQL generated: ${safeInsertSQL}`);
  console.log(`   This SQL uses ON CONFLICT DO NOTHING to prevent any duplicates`);
}

checkForDuplicates();