const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function checkForeignKey() {
  try {
    console.log('Testing different query approaches for user_progress with skill_tree_nodes join...\n');
    
    // Test 1: Simple select without join
    console.log('Test 1: Simple select without join');
    const { data: data1, error: error1 } = await supabase
      .from('user_progress')
      .select('*')
      .limit(1);
    
    if (error1) {
      console.log('Error:', error1.message);
    } else {
      console.log('Success - columns:', data1.length > 0 ? Object.keys(data1[0]) : 'No data');
    }
    
    // Test 2: Try with skill_node_id join
    console.log('\nTest 2: Join with skill_node_id');
    const { data: data2, error: error2 } = await supabase
      .from('user_progress')
      .select(`
        *,
        skill_tree_nodes!skill_node_id (
          id,
          name,
          learning_area
        )
      `)
      .limit(1);
    
    if (error2) {
      console.log('Error:', error2.message);
    } else {
      console.log('Success:', data2 ? 'Join worked' : 'No data');
    }
    
    // Test 3: Try with inner join syntax
    console.log('\nTest 3: Join with inner syntax');
    const { data: data3, error: error3 } = await supabase
      .from('user_progress')
      .select(`
        *,
        skill_tree_nodes!inner (
          id,
          name,
          learning_area
        )
      `)
      .limit(1);
    
    if (error3) {
      console.log('Error:', error3.message);
    } else {
      console.log('Success:', data3 ? 'Join worked' : 'No data');
    }
    
    // Test 4: Try without foreign key hint
    console.log('\nTest 4: Join without foreign key hint');
    const { data: data4, error: error4 } = await supabase
      .from('user_progress')
      .select(`
        *,
        skill_tree_nodes (
          id,
          name,
          learning_area
        )
      `)
      .limit(1);
    
    if (error4) {
      console.log('Error:', error4.message);
    } else {
      console.log('Success:', data4 ? 'Join worked' : 'No data');
    }
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

checkForeignKey();