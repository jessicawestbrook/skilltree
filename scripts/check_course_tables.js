const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkCourseTables() {
  try {
    // Query for course-related tables
    const { data: tables, error: tablesError } = await supabase
      .rpc('get_table_names')
      .select('*');
    
    if (tablesError) {
      // Try alternative approach - query a known table
      console.log('Checking for learning_paths table...');
      const { data: pathsData, error: pathsError } = await supabase
        .from('learning_paths')
        .select('*')
        .limit(1);
      
      if (!pathsError) {
        console.log('learning_paths table exists');
      } else {
        console.log('learning_paths table not found:', pathsError.message);
      }

      console.log('\nChecking for learning_path_modules table...');
      const { data: modulesData, error: modulesError } = await supabase
        .from('learning_path_modules')
        .select('*')
        .limit(1);
      
      if (!modulesError) {
        console.log('learning_path_modules table exists');
      } else {
        console.log('learning_path_modules table not found:', modulesError.message);
      }

      console.log('\nChecking for user_module_progress table...');
      const { data: progressData, error: progressError } = await supabase
        .from('user_module_progress')
        .select('*')
        .limit(1);
      
      if (!progressError) {
        console.log('user_module_progress table exists');
      } else {
        console.log('user_module_progress table not found:', progressError.message);
      }

      // Check for any course-related fields in skill_tree_nodes
      console.log('\nChecking skill_tree_nodes structure...');
      const { data: nodeData, error: nodeError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .limit(1);
      
      if (!nodeError && nodeData && nodeData.length > 0) {
        console.log('skill_tree_nodes columns:', Object.keys(nodeData[0]));
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkCourseTables();