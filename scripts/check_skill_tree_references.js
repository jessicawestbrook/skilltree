const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkSkillTreeReferences() {
  console.log('Checking tables that reference skill_tree_nodes...\n');
  
  const tablesToCheck = [
    'questions',
    'user_progress',
    'starred_items',
    'learning_content',
    'user_question_history',
    'user_question_tracking',
    'skill_progress',
    'user_skills',
    'user_test_attempts',
    'assessment_sessions' // if it exists
  ];
  
  for (const table of tablesToCheck) {
    try {
      // Try to get one row to see the structure
      const { data, error } = await supabase
        .from(table)
        .select('*')
        .limit(1);
      
      if (error) {
        if (error.message.includes('not exist')) {
          console.log(`❌ Table '${table}' does not exist`);
        } else {
          console.log(`⚠️ Table '${table}' error: ${error.message}`);
        }
      } else {
        console.log(`✅ Table '${table}' exists`);
        
        if (data && data.length > 0) {
          const columns = Object.keys(data[0]);
          const relevantColumns = columns.filter(col => 
            col.includes('skill') || 
            col.includes('node') || 
            col.includes('category') ||
            col === 'item_id' ||
            col === 'test_id'
          );
          
          if (relevantColumns.length > 0) {
            console.log(`   Potentially related columns: ${relevantColumns.join(', ')}`);
            
            // Check the data type of these columns
            for (const col of relevantColumns) {
              const value = data[0][col];
              if (value) {
                console.log(`   - ${col}: ${typeof value} (sample: ${String(value).substring(0, 50)})`);
              }
            }
          }
        }
      }
      console.log('');
    } catch (err) {
      console.log(`Error checking ${table}:`, err.message);
    }
  }
  
  // Check the current structure of skill_tree_nodes
  console.log('\n=== Current skill_tree_nodes structure ===');
  const { data: sampleNode, error: nodeError } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .limit(1);
  
  if (!nodeError && sampleNode && sampleNode.length > 0) {
    console.log('Sample node:');
    console.log('- id:', sampleNode[0].id, `(type: ${typeof sampleNode[0].id})`);
    console.log('- parent_id:', sampleNode[0].parent_id, `(type: ${typeof sampleNode[0].parent_id})`);
    console.log('- name:', sampleNode[0].name);
  }
  
  console.log('\n✅ Analysis complete');
}

checkSkillTreeReferences().catch(console.error);