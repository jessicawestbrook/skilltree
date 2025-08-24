// Comprehensive script to fix ALL nodes without display_order
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Academic ordering rules
const academicOrder = {
  // Languages - prioritize common modern languages
  'Spanish': 1,
  'French': 2,
  'German': 3,
  'Italian': 4,
  'Portuguese': 5,
  'Chinese': 6,
  'Japanese': 7,
  'Korean': 8,
  'Arabic': 9,
  'Russian': 10,
  'Latin': 15,
  'Ancient Greek': 20,
  
  // Math - by difficulty/grade level
  'Early': 1,
  'Elementary': 2,
  'Basic': 3,
  'Pre-Algebra': 4,
  'Algebra': 5,
  'Geometry': 6,
  'Trigonometry': 7,
  'Pre-Calculus': 8,
  'Calculus': 9,
  'Statistics': 10,
  'Differential': 11,
  'Abstract': 15,
  'Advanced': 20,
  
  // Sciences - typical academic order
  'Biology': 1,
  'Chemistry': 2,
  'Physics': 3,
  'Earth Science': 4,
  'Environmental': 5,
  'Astronomy': 6,
  
  // History periods
  'Ancient': 1,
  'Classical': 2,
  'Medieval': 3,
  'Renaissance': 4,
  'Modern': 5,
  'Contemporary': 6,
  
  // Grade levels
  'Kindergarten': 1,
  'First': 2,
  'Second': 3,
  'Third': 4,
  'Fourth': 5,
  'Fifth': 6,
  'Sixth': 7,
  'Seventh': 8,
  'Eighth': 9,
  'Ninth': 10,
  'Tenth': 11,
  'Eleventh': 12,
  'Twelfth': 13,
};

function getAcademicPriority(name) {
  // Check for keywords in the name
  for (const [keyword, priority] of Object.entries(academicOrder)) {
    if (name.includes(keyword)) {
      return priority;
    }
  }
  return 100; // Default priority for unmatched items
}

async function fixAllDisplayOrders() {
  console.log('Starting comprehensive display_order fix...\n');
  
  // Get ALL nodes that don't have display_order
  const { data: nodesWithoutOrder, error } = await supabase
    .from('skill_tree_nodes')
    .select('id, name, parent_id')
    .is('display_order', null);
  
  if (error) {
    console.error('Error fetching nodes:', error);
    return;
  }
  
  console.log(`Found ${nodesWithoutOrder.length} nodes without display_order\n`);
  
  // Group nodes by parent_id
  const nodesByParent = {};
  nodesWithoutOrder.forEach(node => {
    const parentId = node.parent_id || 'root';
    if (!nodesByParent[parentId]) {
      nodesByParent[parentId] = [];
    }
    nodesByParent[parentId].push(node);
  });
  
  console.log(`Grouped into ${Object.keys(nodesByParent).length} parent groups\n`);
  
  let totalUpdated = 0;
  let totalErrors = 0;
  
  // Process each parent group
  for (const [parentId, nodes] of Object.entries(nodesByParent)) {
    console.log(`Processing parent group: ${parentId === 'root' ? 'root' : parentId.substring(0, 8)}... (${nodes.length} nodes)`);
    
    // Sort nodes by academic priority
    const sortedNodes = nodes.sort((a, b) => {
      const priorityA = getAcademicPriority(a.name);
      const priorityB = getAcademicPriority(b.name);
      
      if (priorityA !== priorityB) {
        return priorityA - priorityB;
      }
      
      // If same priority, sort alphabetically
      return a.name.localeCompare(b.name);
    });
    
    // Get the highest existing display_order for this parent
    const { data: existingSiblings, error: siblingError } = await supabase
      .from('skill_tree_nodes')
      .select('display_order')
      .eq('parent_id', parentId === 'root' ? null : parentId)
      .not('display_order', 'is', null)
      .order('display_order', { ascending: false })
      .limit(1);
    
    let startingOrder = 1;
    if (!siblingError && existingSiblings && existingSiblings.length > 0) {
      startingOrder = existingSiblings[0].display_order + 1;
    }
    
    // Update each node
    for (let i = 0; i < sortedNodes.length; i++) {
      const node = sortedNodes[i];
      const newDisplayOrder = startingOrder + i;
      
      const { error: updateError } = await supabase
        .from('skill_tree_nodes')
        .update({ display_order: newDisplayOrder })
        .eq('id', node.id);
      
      if (updateError) {
        console.error(`  Error updating ${node.name}:`, updateError.message);
        totalErrors++;
      } else {
        totalUpdated++;
        if (totalUpdated % 100 === 0) {
          console.log(`  Progress: ${totalUpdated} nodes updated...`);
        }
      }
    }
  }
  
  console.log(`\n✅ Update complete!`);
  console.log(`Successfully updated: ${totalUpdated} nodes`);
  console.log(`Errors: ${totalErrors}`);
  
  // Final verification
  console.log('\nFinal verification...');
  
  const { count: totalCount } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true });
  
  const { count: withOrderCount } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true })
    .not('display_order', 'is', null);
  
  const { count: withoutOrderCount } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true })
    .is('display_order', null);
  
  console.log(`\nFinal statistics:`);
  console.log(`Total nodes: ${totalCount}`);
  console.log(`Nodes with display_order: ${withOrderCount}`);
  console.log(`Nodes without display_order: ${withoutOrderCount}`);
  
  if (withoutOrderCount === 0) {
    console.log('\n🎉 SUCCESS: All nodes now have display_order values!');
  } else {
    console.log(`\n⚠️  Warning: Still ${withoutOrderCount} nodes without display_order`);
    
    // Show a few examples
    const { data: remaining } = await supabase
      .from('skill_tree_nodes')
      .select('name, parent_id')
      .is('display_order', null)
      .limit(5);
    
    if (remaining && remaining.length > 0) {
      console.log('\nExamples of remaining nodes:');
      remaining.forEach(node => {
        console.log(`  - ${node.name}`);
      });
    }
  }
}

fixAllDisplayOrders().catch(console.error);