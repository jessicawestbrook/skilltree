// Script to fix the remaining nodes without display_order
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// The nodes that need display_order
const nodesToFix = [
  { id: 'e69592a0-bcf0-4a11-b7e6-ce8280822ab7', name: 'Valley of the Kings' },
  { id: '8b000766-681d-4156-9c3d-daa2dfc88235', name: 'Mean, Median, Mode' },
  { id: '85ac3e63-d1c4-4c54-a4e7-c8134572e551', name: 'Patterns and Sequences' },
  { id: '6861bf59-739e-48d5-be65-37caf21bf776', name: 'Sumerian Civilization' },
  { id: 'db8872c2-a7e8-4d74-bede-ad2fe009b471', name: 'Silent Letters' },
  { id: 'e4e5774f-8dd4-43aa-81c6-823a6e138780', name: 'Systems of ODEs' },
  { id: '57ea9cdf-7ff0-4a4b-bf00-70fd5167717e', name: 'Counting 1-10' },
  { id: '71228ab8-65f2-478a-a421-2c30626df662', name: 'First-Order ODEs' },
  { id: '0d99c890-0516-4214-91d7-4444b03f555a', name: 'Shapes Recognition' },
  { id: 'fea1ba27-904d-4a1c-85d3-7e708a80727c', name: 'Money Counting' }
];

async function fixRemainingNodes() {
  console.log('Fixing remaining nodes without display_order...\n');
  
  for (const node of nodesToFix) {
    // Get the node details including parent_id
    const { data: nodeData, error: fetchError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id, display_order')
      .eq('id', node.id)
      .single();
    
    if (fetchError) {
      console.error(`Error fetching node ${node.name}:`, fetchError);
      continue;
    }
    
    if (nodeData.display_order !== null) {
      console.log(`Node ${node.name} already has display_order: ${nodeData.display_order}`);
      continue;
    }
    
    // Get siblings to determine the next display_order
    const { data: siblings, error: siblingsError } = await supabase
      .from('skill_tree_nodes')
      .select('display_order')
      .eq('parent_id', nodeData.parent_id)
      .not('display_order', 'is', null)
      .order('display_order', { ascending: false })
      .limit(1);
    
    if (siblingsError) {
      console.error(`Error fetching siblings for ${node.name}:`, siblingsError);
      continue;
    }
    
    // Determine the new display_order
    let newDisplayOrder = 1;
    if (siblings && siblings.length > 0) {
      newDisplayOrder = siblings[0].display_order + 1;
    }
    
    // Update the node
    const { error: updateError } = await supabase
      .from('skill_tree_nodes')
      .update({ display_order: newDisplayOrder })
      .eq('id', node.id);
    
    if (updateError) {
      console.error(`Error updating ${node.name}:`, updateError);
    } else {
      console.log(`✓ Updated ${node.name} with display_order: ${newDisplayOrder}`);
    }
  }
  
  console.log('\nVerifying all nodes now have display_order...');
  
  // Final verification
  const { data: nodesWithoutOrder, error } = await supabase
    .from('skill_tree_nodes')
    .select('id, name')
    .is('display_order', null);
  
  if (error) {
    console.error('Error in final verification:', error);
  } else if (nodesWithoutOrder && nodesWithoutOrder.length > 0) {
    console.log(`\nStill ${nodesWithoutOrder.length} nodes without display_order:`);
    nodesWithoutOrder.forEach(node => {
      console.log(`  - ${node.name} (${node.id})`);
    });
  } else {
    console.log('\n✅ SUCCESS: All nodes now have display_order values!');
  }
  
  // Show statistics
  const { count: totalCount } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true });
  
  const { count: withOrderCount } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true })
    .not('display_order', 'is', null);
  
  console.log(`\nFinal statistics:`);
  console.log(`Total nodes: ${totalCount}`);
  console.log(`Nodes with display_order: ${withOrderCount}`);
  console.log(`Nodes without display_order: ${totalCount - withOrderCount}`);
}

fixRemainingNodes().catch(console.error);