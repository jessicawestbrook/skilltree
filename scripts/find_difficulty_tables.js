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

async function findDifficultyTables() {
  console.log('=== SEARCHING FOR DIFFICULTY TABLES ===\n');
  
  // Try different possible table names
  const possibleVocabTables = [
    'vocabulary_difficulties',
    'vocabulary_difficulty',
    'vocab_difficulties',
    'vocab_difficulty',
    'vocabulary_difficulty_levels',
    'difficulties'
  ];
  
  const possibleSpellingTables = [
    'spelling_difficulties',
    'spelling_difficulty', 
    'spell_difficulties',
    'spell_difficulty',
    'spelling_difficulty_levels',
    'difficulties'
  ];
  
  console.log('Searching for vocabulary difficulty tables...');
  for (const tableName of possibleVocabTables) {
    try {
      const { data, error } = await supabase
        .from(tableName)
        .select('*')
        .limit(1);
      
      if (!error) {
        console.log(`✓ Found table: ${tableName}`);
        const { count } = await supabase
          .from(tableName)
          .select('*', { count: 'exact', head: true });
        console.log(`  Contains ${count} records`);
        
        // Show structure
        if (data && data.length > 0) {
          console.log(`  Columns: ${Object.keys(data[0]).join(', ')}`);
        }
        
        // Show all records
        const { data: allData } = await supabase
          .from(tableName)
          .select('*')
          .order('id');
        
        if (allData) {
          console.log('  Records:');
          allData.forEach(record => {
            console.log(`    ID ${record.id}: ${record.name || record.level || record.difficulty || 'unnamed'}`);
          });
        }
      }
    } catch (e) {
      // Table doesn't exist, continue
    }
  }
  
  console.log('\nSearching for spelling difficulty tables...');
  for (const tableName of possibleSpellingTables) {
    try {
      const { data, error } = await supabase
        .from(tableName)
        .select('*')
        .limit(1);
      
      if (!error) {
        console.log(`✓ Found table: ${tableName}`);
        const { count } = await supabase
          .from(tableName)
          .select('*', { count: 'exact', head: true });
        console.log(`  Contains ${count} records`);
        
        // Show structure
        if (data && data.length > 0) {
          console.log(`  Columns: ${Object.keys(data[0]).join(', ')}`);
        }
        
        // Show all records
        const { data: allData } = await supabase
          .from(tableName)
          .select('*')
          .order('id');
        
        if (allData) {
          console.log('  Records:');
          allData.forEach(record => {
            console.log(`    ID ${record.id}: ${record.name || record.level || record.difficulty || 'unnamed'}`);
          });
        }
      }
    } catch (e) {
      // Table doesn't exist, continue
    }
  }
  
  // Check for a general difficulties table
  console.log('\nChecking for general difficulty tables...');
  const generalTables = ['difficulties', 'difficulty_levels', 'skill_difficulties'];
  
  for (const tableName of generalTables) {
    try {
      const { data, error } = await supabase
        .from(tableName)
        .select('*')
        .limit(1);
      
      if (!error) {
        console.log(`✓ Found table: ${tableName}`);
        const { data: allData } = await supabase
          .from(tableName)
          .select('*');
        
        if (allData) {
          console.log(`  Contains ${allData.length} records`);
          if (allData.length > 0) {
            console.log(`  Columns: ${Object.keys(allData[0]).join(', ')}`);
            console.log('  Sample records:');
            allData.slice(0, 5).forEach(record => {
              console.log(`    ${JSON.stringify(record)}`);
            });
          }
        }
      }
    } catch (e) {
      // Table doesn't exist, continue
    }
  }
}

findDifficultyTables().catch(console.error);