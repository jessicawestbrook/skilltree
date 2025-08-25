const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function dropDifficultyField() {
  try {
    console.log('=== DROPPING EMPTY DIFFICULTY FIELD ===\n');
    
    // First, check if backup tables already exist
    console.log('1. Checking for existing backup tables...');
    const { data: tables, error: tablesError } = await supabase
      .rpc('get_table_names', {
        schema_name: 'public'
      });
    
    if (tablesError) {
      // If the RPC doesn't exist, we'll proceed anyway
      console.log('Could not check existing tables, proceeding with backup creation...');
    } else if (tables) {
      const backupTables = tables.filter(t => t.startsWith('spelling_words_bkp'));
      console.log(`Found ${backupTables.length} existing backup tables:`, backupTables);
    }
    
    // Create the backup table name
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
    const backupTableName = `spelling_words_bkp_${timestamp}`;
    
    console.log(`\n2. Creating backup table: ${backupTableName}`);
    console.log('This will create a complete copy of the spelling_words table before making changes.');
    
    // SQL to create backup and drop the field
    const sql = `
      -- Create backup table
      CREATE TABLE ${backupTableName} AS 
      SELECT * FROM spelling_words;
      
      -- Add comment to backup table
      COMMENT ON TABLE ${backupTableName} IS 'Backup created before dropping empty difficulty field';
      
      -- Drop the difficulty column from spelling_words
      ALTER TABLE spelling_words 
      DROP COLUMN IF EXISTS difficulty;
    `;
    
    console.log('\n3. SQL to execute:');
    console.log(sql);
    
    console.log('\n⚠️  WARNING: This will permanently remove the difficulty field from spelling_words table.');
    console.log('A backup table will be created first for safety.');
    console.log('\nTo execute this change, run the following SQL in Supabase SQL Editor:');
    console.log('=' .repeat(80));
    console.log(sql);
    console.log('=' .repeat(80));
    
    // Verify current state
    console.log('\n4. Current table structure verification:');
    const { data: sampleWord, error: sampleError } = await supabase
      .from('spelling_words')
      .select('*')
      .limit(1);
    
    if (!sampleError && sampleWord && sampleWord.length > 0) {
      const fields = Object.keys(sampleWord[0]);
      console.log('\nCurrent fields in spelling_words:');
      fields.forEach(field => {
        if (field === 'difficulty') {
          console.log(`  - ${field} (TO BE REMOVED) - Value: ${sampleWord[0][field]}`);
        } else if (field.includes('difficulty')) {
          console.log(`  - ${field} (KEPT) - Value: ${sampleWord[0][field]}`);
        }
      });
      
      console.log('\nDifficulty-related fields that will be KEPT:');
      fields.filter(f => f.includes('difficulty') && f !== 'difficulty').forEach(field => {
        console.log(`  ✓ ${field}`);
      });
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

dropDifficultyField();