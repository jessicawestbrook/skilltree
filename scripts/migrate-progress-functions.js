// Load environment variables
require('dotenv').config({ path: '.env.local' });

const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Initialize Supabase client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
  console.error('Missing Supabase environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function runMigration() {
  try {
    console.log('Starting progress functions migration...');
    
    // Read the SQL file
    const sqlPath = path.join(__dirname, '07-progress-functions.sql');
    const sqlContent = fs.readFileSync(sqlPath, 'utf8');
    
    // Split by statement separator ($$) and execute each function separately
    const statements = sqlContent.split(/;(?=\s*(?:CREATE|GRANT|DO))/);
    
    for (const statement of statements) {
      const trimmed = statement.trim();
      if (!trimmed || trimmed.startsWith('--')) continue;
      
      try {
        // Execute the SQL statement
        const { error } = await supabase.rpc('query', { query: trimmed });
        
        if (error) {
          // Try direct execution if RPC doesn't work
          console.log('Attempting alternative execution method...');
          // Note: Supabase JS client doesn't support direct SQL execution
          // We'll need to use the SQL editor in Supabase Dashboard
          console.warn(`Statement needs manual execution: ${trimmed.substring(0, 50)}...`);
        }
      } catch (err) {
        console.warn(`Could not execute statement: ${err.message}`);
      }
    }
    
    console.log('\n===========================================');
    console.log('IMPORTANT: Manual steps required!');
    console.log('===========================================');
    console.log('The SQL functions need to be executed manually in Supabase:');
    console.log('1. Go to your Supabase Dashboard');
    console.log('2. Navigate to SQL Editor');
    console.log('3. Copy and paste the contents of scripts/07-progress-functions.sql');
    console.log('4. Execute the SQL');
    console.log('===========================================\n');
    
    // Test if the functions exist by checking user progress
    console.log('Testing if user_progress table is accessible...');
    const { data, error } = await supabase
      .from('user_progress')
      .select('*')
      .limit(1);
    
    if (error) {
      console.error('Error accessing user_progress table:', error.message);
    } else {
      console.log('✓ user_progress table is accessible');
    }
    
    console.log('\nMigration script completed.');
    console.log('Please execute the SQL functions manually in Supabase Dashboard.');
    
  } catch (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  }
}

runMigration();