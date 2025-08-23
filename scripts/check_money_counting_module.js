const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function checkMoneyCountingModule() {
  try {
    // Find Money Counting module
    const { data: moneyCountingNode, error: nodeError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, learning_area, learning_content_ids')
      .ilike('name', '%money counting%')
      .limit(5);

    if (nodeError) {
      console.error('Error finding Money Counting node:', nodeError);
      return;
    }

    console.log('Money Counting nodes found:', moneyCountingNode);

    if (moneyCountingNode && moneyCountingNode.length > 0) {
      const nodeId = moneyCountingNode[0].id;
      console.log('\nChecking user progress for node ID:', nodeId);

      // First check table structure
      console.log('\nChecking user_progress table structure...');
      const { data: sampleProgress, error: sampleError } = await supabase
        .from('user_progress')
        .select('*')
        .limit(1);
      
      if (sampleError) {
        console.error('Error getting sample progress:', sampleError);
      } else if (sampleProgress && sampleProgress.length > 0) {
        console.log('Sample user_progress row columns:', Object.keys(sampleProgress[0]));
        
        // Now try with the correct column name
        const columnName = Object.keys(sampleProgress[0]).find(col => 
          col.includes('skill') && (col.includes('id') || col.includes('node'))
        );
        console.log('Using column name:', columnName);
        
        if (columnName) {
          const { data: userProgress, error: progressError } = await supabase
            .from('user_progress')
            .select('*')
            .eq(columnName, nodeId)
            .limit(5);
          
          if (progressError) {
            console.error('Error checking user progress:', progressError);
          } else {
            console.log('\nUser progress entries for Money Counting:', userProgress);
          }
        }
      } else {
        console.log('No sample progress data found');
      }

      // Check if it appears in starred items
      const { data: starredItems, error: starredError } = await supabase
        .from('starred_items')
        .select('*')
        .eq('item_id', nodeId)
        .eq('item_type', 'skill_node')
        .limit(5);

      if (starredError) {
        console.error('Error checking starred items:', starredError);
      } else {
        console.log('\nStarred items for Money Counting:', starredItems);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

checkMoneyCountingModule();