const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function checkDatabaseColumns() {
  try {
    console.log('Checking database columns that need renaming...\n');
    
    // Check user_progress table
    console.log('1. Checking user_progress table:');
    const { data: userProgress, error: upError } = await supabase
      .from('user_progress')
      .select('*')
      .limit(1);
    
    if (upError) {
      console.log('   Error:', upError.message);
    } else if (userProgress && userProgress.length > 0) {
      const columns = Object.keys(userProgress[0]);
      console.log('   Columns:', columns.join(', '));
      console.log('   Has skill_node_id:', columns.includes('skill_node_id'));
      console.log('   Has skill_id:', columns.includes('skill_id'));
    } else {
      console.log('   No data found');
    }
    
    // Check starred_categories table
    console.log('\n2. Checking starred_categories table:');
    const { data: starredCat, error: scError } = await supabase
      .from('starred_categories')
      .select('*')
      .limit(1);
    
    if (scError) {
      console.log('   Error:', scError.message);
    } else if (starredCat && starredCat.length > 0) {
      const columns = Object.keys(starredCat[0]);
      console.log('   Columns:', columns.join(', '));
      console.log('   Has skill_node_id:', columns.includes('skill_node_id'));
      console.log('   Has skill_id:', columns.includes('skill_id'));
    } else {
      console.log('   No data found');
    }
    
    // Check questions table for node_id
    console.log('\n3. Checking questions table:');
    const { data: questions, error: qError } = await supabase
      .from('questions')
      .select('*')
      .limit(1);
    
    if (qError) {
      console.log('   Error:', qError.message);
    } else if (questions && questions.length > 0) {
      const columns = Object.keys(questions[0]);
      console.log('   Columns:', columns.join(', '));
      console.log('   Has node_id:', columns.includes('node_id'));
      console.log('   Has skill_id:', columns.includes('skill_id'));
      console.log('   Has skill_tree_node_id:', columns.includes('skill_tree_node_id'));
    } else {
      console.log('   No data found');
    }
    
    // Check money_counting_progress table
    console.log('\n4. Checking money_counting_progress table:');
    const { data: moneyProgress, error: mpError } = await supabase
      .from('money_counting_progress')
      .select('*')
      .limit(1);
    
    if (mpError) {
      console.log('   Error:', mpError.message);
    } else if (moneyProgress && moneyProgress.length > 0) {
      const columns = Object.keys(moneyProgress[0]);
      console.log('   Columns:', columns.join(', '));
      console.log('   Has skill_tree_node_id:', columns.includes('skill_tree_node_id'));
      console.log('   Has skill_id:', columns.includes('skill_id'));
    } else {
      console.log('   No data found');
    }
    
    // Summary
    console.log('\n=== SUMMARY ===');
    console.log('Tables/columns that need renaming:');
    console.log('- user_progress.skill_node_id -> skill_id');
    console.log('- starred_categories.skill_node_id -> skill_id');
    console.log('- questions.node_id -> skill_id (if exists)');
    console.log('- money_counting_progress.skill_tree_node_id -> skill_id (if exists)');
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

checkDatabaseColumns();