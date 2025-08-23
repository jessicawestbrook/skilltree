const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Columns to remove (old text-based difficulty names and levels)
const columnsToRemove = [
  'spelling_difficulty_level',
  'spelling_difficulty_name', 
  'ai_spelling_difficulty_level',
  'ai_spelling_difficulty_name',
  'vocabulary_difficulty_level',
  'vocabulary_difficulty_name',
  'difficulty',  // appears to be unused (always null)
  'source_difficulty'  // old text-based difficulty from original source
];

// Columns to keep (foreign key references)
const columnsToKeep = [
  'spelling_difficulty_id',
  'vocabulary_difficulty_id'
];

async function cleanupDifficultyColumns() {
  console.log('=== CLEANING UP OLD DIFFICULTY COLUMNS ===\n');
  
  const timestamp = Date.now();
  const backupTableName = `spelling_words_bkp_${timestamp}`;
  
  try {
    // Step 1: Document current state
    console.log('📊 COLUMNS TO REMOVE:');
    columnsToRemove.forEach(col => console.log(`  - ${col}`));
    
    console.log('\n✅ COLUMNS TO KEEP (Foreign Keys):');
    columnsToKeep.forEach(col => console.log(`  - ${col}`));
    
    // Step 2: Verify foreign key columns have data
    console.log('\n🔍 Verifying foreign key columns have data...');
    
    const { data: fkCheck, error: fkError } = await supabase
      .from('spelling_words')
      .select('spelling_difficulty_id, vocabulary_difficulty_id')
      .limit(100);
    
    if (fkError) {
      console.error('Error checking foreign keys:', fkError);
      return;
    }
    
    const hasSpellingFK = fkCheck?.some(row => row.spelling_difficulty_id !== null);
    const hasVocabFK = fkCheck?.some(row => row.vocabulary_difficulty_id !== null);
    
    console.log(`  spelling_difficulty_id: ${hasSpellingFK ? '✅ Has data' : '⚠️ No data found'}`);
    console.log(`  vocabulary_difficulty_id: ${hasVocabFK ? '✅ Has data' : '⚠️ No data found'}`);
    
    if (!hasSpellingFK || !hasVocabFK) {
      console.log('\n⚠️ WARNING: Foreign key columns may not be properly populated.');
      console.log('Please ensure data migration is complete before removing old columns.');
      return;
    }
    
    // Step 3: Create backup
    console.log('\n📦 Creating backup table...');
    console.log(`Backup table name: ${backupTableName}`);
    console.log('\nTo create backup, run this SQL command in Supabase:');
    console.log(`CREATE TABLE ${backupTableName} AS SELECT * FROM spelling_words;`);
    
    // Step 4: Generate ALTER TABLE statements
    console.log('\n📝 SQL COMMANDS TO REMOVE OLD COLUMNS:');
    console.log('----------------------------------------');
    console.log('-- Run these commands in Supabase SQL editor:\n');
    
    // First create the backup
    console.log(`-- Step 1: Create backup`);
    console.log(`CREATE TABLE ${backupTableName} AS SELECT * FROM spelling_words;\n`);
    
    // Then drop each column
    console.log(`-- Step 2: Remove old difficulty columns`);
    columnsToRemove.forEach(col => {
      console.log(`ALTER TABLE spelling_words DROP COLUMN IF EXISTS ${col};`);
    });
    
    // Verification query
    console.log('\n-- Step 3: Verify remaining columns');
    console.log(`SELECT column_name, data_type FROM information_schema.columns`);
    console.log(`WHERE table_name = 'spelling_words' AND column_name LIKE '%difficulty%';`);
    
    // Save cleanup plan
    const cleanupPlan = {
      timestamp: new Date().toISOString(),
      backupTable: backupTableName,
      columnsToRemove,
      columnsToKeep,
      sqlCommands: {
        backup: `CREATE TABLE ${backupTableName} AS SELECT * FROM spelling_words;`,
        dropColumns: columnsToRemove.map(col => `ALTER TABLE spelling_words DROP COLUMN IF EXISTS ${col};`),
        verify: `SELECT column_name FROM information_schema.columns WHERE table_name = 'spelling_words' AND column_name LIKE '%difficulty%';`
      }
    };
    
    const planFile = `scripts/difficulty_cleanup_plan_${timestamp}.json`;
    fs.writeFileSync(planFile, JSON.stringify(cleanupPlan, null, 2));
    
    console.log('\n💾 Cleanup plan saved to:', planFile);
    
    // Step 5: Check vocabulary_words table too
    console.log('\n=== CHECKING VOCABULARY_WORDS TABLE ===');
    
    const { data: vocabSample } = await supabase
      .from('vocabulary_words')
      .select('*')
      .limit(1);
    
    if (vocabSample && vocabSample.length > 0) {
      const vocabCols = Object.keys(vocabSample[0]);
      const vocabDiffCols = vocabCols.filter(col => col.includes('difficulty'));
      
      if (vocabDiffCols.length > 0) {
        console.log('\n📊 Vocabulary table difficulty columns:');
        vocabDiffCols.forEach(col => console.log(`  - ${col}`));
        
        console.log('\n📝 SQL COMMANDS FOR VOCABULARY_WORDS:');
        console.log('----------------------------------------');
        console.log(`CREATE TABLE vocabulary_words_bkp_${timestamp} AS SELECT * FROM vocabulary_words;`);
        
        const vocabColsToRemove = vocabDiffCols.filter(col => 
          !col.endsWith('_id') && col !== 'difficulty_score'
        );
        
        vocabColsToRemove.forEach(col => {
          console.log(`ALTER TABLE vocabulary_words DROP COLUMN IF EXISTS ${col};`);
        });
      }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('⚠️  IMPORTANT: Review the SQL commands above');
    console.log('1. Copy the SQL commands');
    console.log('2. Run them in Supabase SQL editor');
    console.log('3. Verify the changes');
    console.log('='.repeat(60));
    
  } catch (error) {
    console.error('Error:', error);
  }
}

cleanupDifficultyColumns().catch(console.error);