// Test script to debug why updates aren't working
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function testSingleUpdate() {
  console.log('Testing single node update...\n');
  
  // Get one node without display_order
  const { data: node, error: fetchError } = await supabase
    .from('skill_tree_nodes')
    .select('id, name, display_order')
    .is('display_order', null)
    .limit(1)
    .single();
  
  if (fetchError) {
    console.error('Error fetching node:', fetchError);
    return;
  }
  
  console.log('Found node:', node.name);
  console.log('ID:', node.id);
  console.log('Current display_order:', node.display_order);
  
  // Try to update it
  console.log('\nAttempting to update display_order to 999...');
  
  const { data: updateData, error: updateError } = await supabase
    .from('skill_tree_nodes')
    .update({ display_order: 999 })
    .eq('id', node.id)
    .select();
  
  if (updateError) {
    console.error('Update error:', updateError);
    console.error('Error details:', JSON.stringify(updateError, null, 2));
  } else {
    console.log('Update response:', updateData);
  }
  
  // Check if it was actually updated
  const { data: checkNode, error: checkError } = await supabase
    .from('skill_tree_nodes')
    .select('id, name, display_order')
    .eq('id', node.id)
    .single();
  
  if (checkError) {
    console.error('Error checking update:', checkError);
  } else {
    console.log('\nAfter update check:');
    console.log('Name:', checkNode.name);
    console.log('display_order:', checkNode.display_order);
    
    if (checkNode.display_order === 999) {
      console.log('✅ Update successful!');
    } else {
      console.log('❌ Update failed - value unchanged');
    }
  }
}

testSingleUpdate().catch(console.error);