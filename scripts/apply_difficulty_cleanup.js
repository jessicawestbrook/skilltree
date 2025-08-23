const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function applyDifficultyCleanup() {
  console.log('=== APPLYING DIFFICULTY COLUMNS CLEANUP ===\n');
  
  const timestamp = Date.now();
  const backupTableName = `spelling_words_bkp_${timestamp}`;
  const results = {
    timestamp: new Date().toISOString(),
    backupTable: backupTableName,
    steps: [],
    errors: []
  };
  
  try {
    // Step 1: Check current state
    console.log('📊 CHECKING CURRENT STATE...');
    const { data: sample } = await supabase
      .from('spelling_words')
      .select('*')
      .limit(1);
    
    if (sample && sample.length > 0) {
      const currentColumns = Object.keys(sample[0]);
      const difficultyColumns = currentColumns.filter(col => col.includes('difficulty'));
      console.log(`Current difficulty-related columns: ${difficultyColumns.join(', ')}`);
      results.steps.push({ step: 'check_state', columns: difficultyColumns });
    }
    
    // Step 2: Verify foreign keys have data
    console.log('\n🔍 VERIFYING FOREIGN KEY DATA...');
    const { data: fkData, count } = await supabase
      .from('spelling_words')
      .select('spelling_difficulty_id, vocabulary_difficulty_id', { count: 'exact' })
      .not('spelling_difficulty_id', 'is', null)
      .not('vocabulary_difficulty_id', 'is', null);
    
    console.log(`Words with both foreign keys populated: ${count || 0}`);
    
    const { count: totalCount } = await supabase
      .from('spelling_words')
      .select('id', { count: 'exact', head: true });
    
    console.log(`Total words: ${totalCount}`);
    
    if (count < totalCount * 0.9) {
      console.log('⚠️ WARNING: Less than 90% of records have foreign keys populated');
      console.log('Please ensure data migration is complete before proceeding');
      results.errors.push('Insufficient foreign key data');
      return;
    }
    
    // Step 3: Create backup (show SQL command)
    console.log('\n📦 BACKUP COMMAND:');
    console.log('Please run this SQL command in Supabase to create a backup:');
    console.log(`\nCREATE TABLE ${backupTableName} AS SELECT * FROM spelling_words;\n`);
    
    // Step 4: Generate column removal commands
    const columnsToRemove = [
      'spelling_difficulty_level',
      'spelling_difficulty_name',
      'ai_spelling_difficulty_level',
      'ai_spelling_difficulty_name',
      'vocabulary_difficulty_level',
      'vocabulary_difficulty_name',
      'difficulty',
      'source_difficulty'
    ];
    
    console.log('📝 COLUMN REMOVAL COMMANDS:');
    console.log('Run these commands in Supabase SQL editor:\n');
    
    columnsToRemove.forEach(col => {
      console.log(`ALTER TABLE spelling_words DROP COLUMN IF EXISTS ${col};`);
    });
    
    // Step 5: Save cleanup summary
    results.columnsToRemove = columnsToRemove;
    results.sqlCommands = [
      `CREATE TABLE ${backupTableName} AS SELECT * FROM spelling_words;`,
      ...columnsToRemove.map(col => `ALTER TABLE spelling_words DROP COLUMN IF EXISTS ${col};`)
    ];
    
    const resultsFile = `scripts/difficulty_cleanup_results_${timestamp}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
    
    console.log('\n' + '='.repeat(60));
    console.log('📋 CLEANUP PLAN READY');
    console.log('='.repeat(60));
    console.log('\nTo complete the cleanup:');
    console.log('1. Copy the SQL commands above');
    console.log('2. Go to Supabase SQL editor');
    console.log('3. Run the backup command first');
    console.log('4. Run the ALTER TABLE commands');
    console.log('5. Verify with: SELECT column_name FROM information_schema.columns');
    console.log("   WHERE table_name = 'spelling_words' AND column_name LIKE '%difficulty%';");
    console.log('\n💾 Results saved to:', resultsFile);
    
    // Also save a pure SQL file for easy execution
    const sqlFile = `scripts/execute_cleanup_${timestamp}.sql`;
    const sqlContent = `-- Difficulty Cleanup SQL Commands
-- Generated: ${new Date().toISOString()}

-- Create backup
${results.sqlCommands[0]}

-- Remove old columns
${results.sqlCommands.slice(1).join('\n')}

-- Verify
SELECT column_name, data_type 
FROM information_schema.columns
WHERE table_name = 'spelling_words' 
  AND column_name LIKE '%difficulty%';`;
    
    fs.writeFileSync(sqlFile, sqlContent);
    console.log('📄 SQL file saved to:', sqlFile);
    
  } catch (error) {
    console.error('Error:', error);
    results.errors.push(error.message);
  }
}

applyDifficultyCleanup().catch(console.error);