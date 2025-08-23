const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function checkPathIssues() {
  try {
    console.log('Checking for path duplication issues...\n');
    
    // Find the specific node causing issues
    const searchPath = 'computer_science/programming_fundamentals/control_structures';
    const segments = searchPath.split('/');
    
    console.log('Looking for nodes with these names:', segments);
    
    for (const segment of segments) {
      const { data: nodes, error } = await supabase
        .from('skill_tree_nodes')
        .select('id, name, parent_id')
        .ilike('name', `%${segment}%`)
        .limit(10);
      
      if (!error && nodes) {
        console.log(`\nNodes matching "${segment}":`);
        nodes.forEach(node => {
          console.log(`  - ID: ${node.id}, Name: ${node.name}, Parent: ${node.parent_id}`);
        });
      }
    }
    
    // Check for circular references
    console.log('\n\nChecking for circular references...');
    
    async function checkCircular(nodeId, visited = new Set()) {
      if (visited.has(nodeId)) {
        return true; // Found circular reference
      }
      
      visited.add(nodeId);
      
      const { data: node } = await supabase
        .from('skill_tree_nodes')
        .select('parent_id')
        .eq('id', nodeId)
        .single();
      
      if (node && node.parent_id) {
        return checkCircular(node.parent_id, visited);
      }
      
      return false;
    }
    
    // Check a sample of nodes for circular references
    const { data: sampleNodes } = await supabase
      .from('skill_tree_nodes')
      .select('id, name')
      .limit(100);
    
    let circularFound = false;
    for (const node of sampleNodes || []) {
      if (await checkCircular(node.id)) {
        console.log(`  ❌ Circular reference found for node: ${node.name} (${node.id})`);
        circularFound = true;
      }
    }
    
    if (!circularFound) {
      console.log('  ✅ No circular references found in sample');
    }
    
    // Build path for a specific problematic node
    console.log('\n\nTrying to build path for control_structures node...');
    
    const { data: controlNode } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id')
      .eq('name', 'Control Structures')
      .limit(1)
      .single();
    
    if (controlNode) {
      console.log('Found Control Structures node:', controlNode);
      
      // Manually trace the path
      let current = controlNode;
      const path = [];
      const visited = new Set();
      
      while (current && current.parent_id && !visited.has(current.id)) {
        visited.add(current.id);
        path.unshift(current.name);
        
        const { data: parent } = await supabase
          .from('skill_tree_nodes')
          .select('id, name, parent_id')
          .eq('id', current.parent_id)
          .single();
        
        current = parent;
        
        if (parent) {
          console.log(`  Parent: ${parent.name} (${parent.id})`);
        }
      }
      
      if (current && current.name !== 'Knowledge') {
        path.unshift(current.name);
      }
      
      console.log('\nFull path:', path.join(' > '));
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkPathIssues();