const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function executeMigration() {
  try {
    console.log('Starting database migration to rename columns to skill_id...\n');
    
    // Read the SQL migration file
    const sqlPath = path.join(__dirname, 'rename_to_skill_id_migration.sql');
    const sqlContent = fs.readFileSync(sqlPath, 'utf8');
    
    // Note: Supabase JS client doesn't support raw SQL execution directly
    // We'll need to execute this in the Supabase dashboard
    console.log('IMPORTANT: The migration SQL needs to be executed in the Supabase SQL Editor.');
    console.log('The SQL file has been created at:', sqlPath);
    console.log('\nPlease follow these steps:');
    console.log('1. Go to your Supabase dashboard');
    console.log('2. Navigate to the SQL Editor');
    console.log('3. Copy and paste the contents of rename_to_skill_id_migration.sql');
    console.log('4. Execute the SQL');
    console.log('\nThe migration will:');
    console.log('- Create backup tables automatically');
    console.log('- Rename skill_node_id to skill_id in user_progress');
    console.log('- Rename skill_node_id to skill_id in starred_categories (if exists)');
    console.log('- Rename node_id to skill_id in questions (if exists)');
    console.log('- Update foreign key constraints');
    console.log('- Update RLS policies');
    
    // For now, let's check what columns currently exist
    console.log('\n=== Current Database State ===');
    
    // Check user_progress
    const { data: upSample, error: upError } = await supabase
      .from('user_progress')
      .select('*')
      .limit(1);
    
    if (!upError && upSample) {
      console.log('user_progress columns:', upSample.length > 0 ? Object.keys(upSample[0]) : 'No data');
    }
    
    // Check if starred_categories exists
    const { data: scSample, error: scError } = await supabase
      .from('starred_categories')
      .select('*')
      .limit(1);
    
    if (!scError && scSample) {
      console.log('starred_categories columns:', scSample.length > 0 ? Object.keys(scSample[0]) : 'No data');
    }
    
    console.log('\nAfter running the migration in Supabase, proceed with updating the code files.');
    
  } catch (error) {
    console.error('Error:', error);
  }
}

executeMigration();