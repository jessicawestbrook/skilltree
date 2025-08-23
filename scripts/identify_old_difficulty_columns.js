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

async function identifyOldDifficultyColumns() {
  console.log('=== IDENTIFYING OLD DIFFICULTY COLUMNS ===\n');
  
  // Get a sample row to see all columns
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
  console.log('All columns in spelling_words table:');
  columns.forEach(col => console.log(`  - ${col}`));
  
  console.log('\n--- COLUMNS TO KEEP (Foreign Keys) ---');
  const keepColumns = [
    'vocabulary_difficulty_id',
    'spelling_difficulty_id'
  ];
  keepColumns.forEach(col => {
    if (columns.includes(col)) {
      console.log(`✅ ${col}: ${sampleRow[0][col]}`);
    }
  });
  
  console.log('\n--- OLD COLUMNS TO REMOVE ---');
  const oldDifficultyColumns = columns.filter(col => 
    (col.includes('difficulty') || col.includes('level')) && 
    !keepColumns.includes(col)
  );
  
  oldDifficultyColumns.forEach(col => {
    console.log(`❌ ${col}: ${sampleRow[0][col]}`);
  });
  
  console.log('\n--- ANALYSIS ---');
  console.log(`Total columns: ${columns.length}`);
  console.log(`Columns to remove: ${oldDifficultyColumns.length}`);
  console.log(`Columns after removal: ${columns.length - oldDifficultyColumns.length}`);
  
  // Check if any of these columns are being used in the app
  console.log('\n--- CHECKING APP USAGE ---');
  const columnsToCheck = [
    'spelling_difficulty_name',
    'vocabulary_difficulty_name',
    'spelling_difficulty_level',
    'vocabulary_difficulty_level'
  ];
  
  console.log('The following columns might still be referenced in the app:');
  columnsToCheck.forEach(col => {
    if (oldDifficultyColumns.includes(col)) {
      console.log(`  ⚠️  ${col} - Check app code before removing`);
    }
  });
  
  console.log('\n--- RECOMMENDED ACTION ---');
  console.log('Columns to remove via ALTER TABLE:');
  oldDifficultyColumns.forEach(col => {
    console.log(`  ALTER TABLE spelling_words DROP COLUMN ${col};`);
  });
}

identifyOldDifficultyColumns().catch(console.error);