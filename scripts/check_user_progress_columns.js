const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function checkUserProgressColumns() {
  try {
    // First, try to get any user_progress row to see structure
    const { data: sample, error } = await supabase
      .from('user_progress')
      .select('*')
      .limit(1);

    if (error) {
      console.error('Error fetching user_progress:', error);
      
      // Try creating a test entry to see what columns are expected
      console.log('\nAttempting to create test user_progress entry...');
      const testUserId = '00000000-0000-0000-0000-000000000000';
      const testNodeId = 'fea1ba27-904d-4a1c-85d3-7e708a80727c'; // Money Counting node
      
      // Try with skill_id
      const { error: error1 } = await supabase
        .from('user_progress')
        .insert({
          user_id: testUserId,
          skill_id: testNodeId,
          status: 'in_progress',
          rating: 0
        });
      
      if (!error1) {
        console.log('Column name is: skill_id');
      } else {
        console.log('skill_id failed:', error1.message);
        
        // Try with skill_node_id
        const { error: error2 } = await supabase
          .from('user_progress')
          .insert({
            user_id: testUserId,
            skill_node_id: testNodeId,
            status: 'in_progress',
            rating: 0
          });
        
        if (!error2) {
          console.log('Column name is: skill_node_id');
        } else {
          console.log('skill_node_id failed:', error2.message);
          
          // Try with skill_tree_node_id
          const { error: error3 } = await supabase
            .from('user_progress')
            .insert({
              user_id: testUserId,
              skill_tree_node_id: testNodeId,
              status: 'in_progress',
              rating: 0
            });
          
          if (!error3) {
            console.log('Column name is: skill_tree_node_id');
          } else {
            console.log('skill_tree_node_id failed:', error3.message);
          }
        }
      }
      
      // Clean up test entry
      await supabase
        .from('user_progress')
        .delete()
        .eq('user_id', testUserId);
        
    } else if (sample && sample.length > 0) {
      console.log('user_progress columns:', Object.keys(sample[0]));
      
      // Find the column that contains skill/node id
      const skillColumn = Object.keys(sample[0]).find(col => 
        col.includes('skill') || col.includes('node')
      );
      console.log('Skill/Node column name:', skillColumn);
    } else {
      console.log('No user_progress data found');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

checkUserProgressColumns();