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

async function backupSpellingWordsTable() {
  console.log('Creating backup of spelling_words table...\n');
  
  try {
    // Check for existing backup tables
    const { data: tables } = await supabase.rpc('get_table_names');
    
    let backupNumber = 1;
    let backupTableName = 'spelling_words_bkp';
    
    // Find the next available backup table name
    while (tables?.some(t => t.table_name === backupTableName)) {
      backupNumber++;
      backupTableName = `spelling_words_bkp${backupNumber}`;
    }
    
    console.log(`Creating backup table: ${backupTableName}`);
    
    // Create backup table using SQL
    const { error: createError } = await supabase.rpc('exec_sql', {
      sql: `CREATE TABLE ${backupTableName} AS SELECT * FROM spelling_words;`
    });
    
    if (createError) {
      // Try alternative approach
      console.log('Trying alternative backup approach...');
      
      const { error: altError } = await supabase.rpc('exec_sql', {
        sql: `
          CREATE TABLE ${backupTableName} (LIKE spelling_words INCLUDING ALL);
          INSERT INTO ${backupTableName} SELECT * FROM spelling_words;
        `
      });
      
      if (altError) {
        console.error('Error creating backup:', altError);
        return;
      }
    }
    
    // Verify backup
    const { count } = await supabase
      .from(backupTableName)
      .select('*', { count: 'exact', head: true });
    
    const { count: originalCount } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });
    
    console.log(`\nBackup complete!`);
    console.log(`Original table has ${originalCount} rows`);
    console.log(`Backup table ${backupTableName} has ${count} rows`);
    
    if (count === originalCount) {
      console.log('✓ Backup verified successfully');
    } else {
      console.log('⚠ Warning: Row count mismatch');
    }
    
  } catch (error) {
    console.error('Error during backup:', error);
  }
}

backupSpellingWordsTable().catch(console.error);