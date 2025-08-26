const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

// Use service role key for admin operations
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function executeSQLStatements() {
  try {
    console.log('Starting to link courses to skill nodes...\n');
    
    // Step 1: Check backup
    console.log('Step 1: Checking if backup table exists...');
    try {
      const { error } = await supabase
        .from('learning_paths_bkp')
        .select('id')
        .limit(1);
      
      if (error) {
        console.log('Backup table does not exist yet, will be created by SQL script');
      } else {
        console.log('✓ Backup table already exists');
      }
    } catch (err) {
      console.log('Note: Could not check backup table');
    }
    
    // Step 2: Check if skill_node_id column exists
    console.log('\nStep 2: Checking if skill_node_id column exists...');
    const { data: checkColumn, error: checkError } = await supabase
      .from('learning_paths')
      .select('skill_node_id')
      .limit(1);
    
    if (checkError && checkError.message.includes('column')) {
      console.log('Column does not exist, will be added via SQL execution');
    } else {
      console.log('✓ Column already exists or will be added');
    }
    
    // Step 3: Update the Latin course
    console.log('\nStep 3: Updating Complete Henle Latin Program with skill node association...');
    
    // First check current state
    const { data: currentPath, error: fetchError } = await supabase
      .from('learning_paths')
      .select('*')
      .eq('id', '97765ae5-4d73-43eb-8072-6b110a8c6a8a')
      .single();
    
    if (!fetchError && currentPath) {
      console.log('Current Latin path:', {
        name: currentPath.name,
        skill_node_id: currentPath.skill_node_id || 'Not set'
      });
    }
    
    // Verify the skill node exists
    const { data: skillNode, error: skillError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name')
      .eq('id', 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8')
      .single();
    
    if (!skillError && skillNode) {
      console.log('✓ Found skill node:', skillNode.name);
    } else {
      console.log('⚠️ Warning: Skill node not found');
    }
    
    // Step 4: Show the SQL that needs to be executed
    console.log('\n========================================');
    console.log('IMPORTANT: Please execute the following SQL in Supabase SQL Editor:');
    console.log('========================================\n');
    
    const sqlContent = fs.readFileSync(
      path.join(__dirname, 'link_courses_to_skills.sql'),
      'utf8'
    );
    
    console.log('File: scripts/link_courses_to_skills.sql');
    console.log('\nSQL Preview (first 500 chars):');
    console.log(sqlContent.substring(0, 500) + '...\n');
    
    console.log('Steps the SQL will perform:');
    console.log('1. Create backup of learning_paths table');
    console.log('2. Add skill_node_id column with foreign key to skill_tree_nodes');
    console.log('3. Create index for performance');
    console.log('4. Link the Latin course to the Latin Language skill node');
    console.log('5. Create a view for easier querying');
    console.log('6. Grant appropriate permissions');
    
    console.log('\n========================================');
    console.log('To execute: ');
    console.log('1. Go to your Supabase dashboard');
    console.log('2. Navigate to SQL Editor');
    console.log('3. Copy and paste the contents of scripts/link_courses_to_skills.sql');
    console.log('4. Click "Run" to execute');
    console.log('========================================\n');
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

executeSQLStatements();