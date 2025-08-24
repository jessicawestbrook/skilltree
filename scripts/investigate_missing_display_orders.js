// Script to investigate why some nodes don't have display_order
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function investigateNodes() {
  console.log('Investigating nodes without display_order...\n');
  
  // Get a sample of nodes without display_order
  const { data: nodesWithoutOrder, error } = await supabase
    .from('skill_tree_nodes')
    .select('id, name, parent_id, display_order')
    .is('display_order', null)
    .limit(20);
  
  if (error) {
    console.error('Error fetching nodes:', error);
    return;
  }
  
  console.log(`Found ${nodesWithoutOrder.length} nodes without display_order (showing first 20):\n`);
  
  // Check each node's parent and siblings
  for (const node of nodesWithoutOrder) {
    console.log(`\nNode: ${node.name}`);
    console.log(`  ID: ${node.id}`);
    console.log(`  Parent ID: ${node.parent_id}`);
    
    // Check if parent exists
    if (node.parent_id) {
      const { data: parent, error: parentError } = await supabase
        .from('skill_tree_nodes')
        .select('name, display_order')
        .eq('id', node.parent_id)
        .single();
      
      if (parentError) {
        console.log(`  Parent: ERROR - ${parentError.message}`);
      } else if (parent) {
        console.log(`  Parent: ${parent.name} (display_order: ${parent.display_order})`);
      }
    } else {
      console.log(`  Parent: None (root level)`);
    }
    
    // Check siblings
    const { data: siblings, error: siblingsError } = await supabase
      .from('skill_tree_nodes')
      .select('name, display_order')
      .eq('parent_id', node.parent_id)
      .not('id', 'eq', node.id)
      .order('display_order', { ascending: true })
      .limit(3);
    
    if (!siblingsError && siblings && siblings.length > 0) {
      console.log(`  Siblings with display_order:`);
      siblings.forEach(sibling => {
        console.log(`    - ${sibling.name}: ${sibling.display_order}`);
      });
    } else {
      console.log(`  No siblings found or error`);
    }
  }
  
  // Get total count
  const { count } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true })
    .is('display_order', null);
  
  console.log(`\n\nTotal nodes without display_order: ${count}`);
  
  // Check if these are all newer nodes
  const { data: recentNodes, error: recentError } = await supabase
    .from('skill_tree_nodes')
    .select('created_at')
    .is('display_order', null)
    .order('created_at', { ascending: false })
    .limit(5);
  
  if (!recentError && recentNodes) {
    console.log('\nCreation dates of nodes without display_order (most recent):');
    recentNodes.forEach(node => {
      console.log(`  - ${node.created_at}`);
    });
  }
}

investigateNodes().catch(console.error);