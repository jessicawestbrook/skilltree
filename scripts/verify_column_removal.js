import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: join(__dirname, '..', '.env.local') });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceRoleKey = process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceRoleKey) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceRoleKey);

async function verifyColumnRemoval() {
  console.log('=== VERIFYING COLUMN REMOVAL ===\n');
  
  // Get a sample row to check columns
  const { data: sampleRow, error } = await supabase
    .from('spelling_words')
    .select('*')
    .limit(1);
  
  if (error) {
    console.error('Error fetching sample row:', error);
    return;
  }
  
  if (!sampleRow || sampleRow.length === 0) {
    console.log('No data found in spelling_words table');
    return;
  }
  
  const columns = Object.keys(sampleRow[0]);
  
  // Check if the old columns are gone
  const removedColumns = ['spelling_difficulty_name', 'vocabulary_difficulty_name'];
  const stillPresent = removedColumns.filter(col => columns.includes(col));
  
  if (stillPresent.length === 0) {
    console.log('✅ Success! The following columns have been removed:');
    removedColumns.forEach(col => console.log(`  - ${col}`));
  } else {
    console.log('⚠️ The following columns are still present:');
    stillPresent.forEach(col => console.log(`  - ${col}`));
  }
  
  // Test that joins still work
  console.log('\n--- Testing Foreign Key Joins ---');
  
  const { data: joinTest, error: joinError } = await supabase
    .from('spelling_words')
    .select(`
      word,
      spelling_difficulty_id,
      vocabulary_difficulty_id,
      spelling_difficulty_levels!spelling_difficulty_id(name),
      vocabulary_difficulty_levels!vocabulary_difficulty_id(name)
    `)
    .limit(3);
  
  if (joinError) {
    console.log('❌ Error with joins:', joinError.message);
  } else {
    console.log('✅ Joins are working correctly!');
    if (joinTest && joinTest.length > 0) {
      console.log('\nSample data with joined difficulty names:');
      joinTest.forEach(word => {
        console.log(`  ${word.word}:`);
        console.log(`    Spelling: ${word.spelling_difficulty_levels?.name} (ID: ${word.spelling_difficulty_id})`);
        console.log(`    Vocabulary: ${word.vocabulary_difficulty_levels?.name} (ID: ${word.vocabulary_difficulty_id})`);
      });
    }
  }
  
  // Test the view
  console.log('\n--- Testing spelling_words_with_sources View ---');
  
  const { data: viewTest, error: viewError } = await supabase
    .from('spelling_words_with_sources')
    .select('*')
    .limit(1);
  
  if (viewError) {
    console.log('❌ Error with view:', viewError.message);
  } else {
    console.log('✅ View is working correctly!');
    if (viewTest && viewTest.length > 0) {
      const viewColumns = Object.keys(viewTest[0]);
      const hasOldColumns = removedColumns.some(col => viewColumns.includes(col));
      if (!hasOldColumns) {
        console.log('  ✅ View does not contain removed columns');
      } else {
        console.log('  ⚠️ View still contains old columns');
      }
    }
  }
  
  console.log('\n--- Summary ---');
  console.log('Total columns in spelling_words table:', columns.length);
  console.log('Columns removed:', removedColumns.length);
  console.log('Foreign key columns present:', 
    columns.includes('spelling_difficulty_id') && columns.includes('vocabulary_difficulty_id') 
      ? '✅ Yes' : '❌ No'
  );
}

verifyColumnRemoval().catch(console.error);