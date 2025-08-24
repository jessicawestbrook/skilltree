// Script to update display_order field in skill_tree_nodes table
require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function checkCurrentState() {
  console.log('Checking current state of display_order field...');
  
  const { data, error } = await supabase
    .from('skill_tree_nodes')
    .select('id, name, parent_id, display_order')
    .order('parent_id', { ascending: true })
    .limit(1000);
  
  if (error) {
    console.error('Error fetching nodes:', error);
    return null;
  }
  
  const totalNodes = data.length;
  const nodesWithDisplayOrder = data.filter(node => node.display_order !== null).length;
  const nodesWithoutDisplayOrder = totalNodes - nodesWithDisplayOrder;
  
  console.log(`Total nodes fetched: ${totalNodes}`);
  console.log(`Nodes with display_order: ${nodesWithDisplayOrder}`);
  console.log(`Nodes without display_order: ${nodesWithoutDisplayOrder}`);
  
  // Get total count
  const { count, error: countError } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true });
  
  if (!countError) {
    console.log(`Total nodes in database: ${count}`);
    if (count > 1000) {
      console.log('Note: Only showing first 1000 nodes in this check');
    }
  }
  
  return data;
}

async function createBackupTable() {
  console.log('\nCreating backup table...');
  
  // We'll create a backup with timestamp
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const backupTableName = `skill_tree_nodes_bkp_${timestamp}`;
  
  console.log(`Suggested backup table name: ${backupTableName}`);
  console.log('Note: Manual backup creation via SQL may be required through Supabase dashboard');
  console.log('You can create a backup with this SQL command in Supabase SQL Editor:');
  console.log(`CREATE TABLE ${backupTableName} AS SELECT * FROM skill_tree_nodes;`);
  
  return backupTableName;
}

async function getNodesByParent() {
  console.log('\nFetching all nodes grouped by parent...');
  
  const { data: allNodes, error } = await supabase
    .from('skill_tree_nodes')
    .select('id, name, parent_id, display_order')
    .order('name', { ascending: true });
  
  if (error) {
    console.error('Error fetching all nodes:', error);
    return null;
  }
  
  // Group nodes by parent_id
  const nodesByParent = {};
  allNodes.forEach(node => {
    const parentId = node.parent_id || 'root';
    if (!nodesByParent[parentId]) {
      nodesByParent[parentId] = [];
    }
    nodesByParent[parentId].push(node);
  });
  
  console.log(`Total nodes: ${allNodes.length}`);
  console.log(`Number of parent groups: ${Object.keys(nodesByParent).length}`);
  
  return { allNodes, nodesByParent };
}

// Academic ordering rules for common subjects
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
  'Elementary': 1,
  'Basic': 2,
  'Pre-Algebra': 3,
  'Algebra': 4,
  'Geometry': 5,
  'Trigonometry': 6,
  'Pre-Calculus': 7,
  'Calculus': 8,
  'Statistics': 9,
  'Abstract': 15,
  'Advanced': 20,
  
  // Sciences - typical academic order
  'Biology': 1,
  'Chemistry': 2,
  'Physics': 3,
  'Earth Science': 4,
  'Environmental': 5,
  'Astronomy': 6,
  
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

function sortNodesByAcademicOrder(nodes) {
  return nodes.sort((a, b) => {
    const priorityA = getAcademicPriority(a.name);
    const priorityB = getAcademicPriority(b.name);
    
    if (priorityA !== priorityB) {
      return priorityA - priorityB;
    }
    
    // If same priority, sort alphabetically
    return a.name.localeCompare(b.name);
  });
}

async function updateDisplayOrders(nodesByParent) {
  console.log('\nUpdating display_order values...');
  
  let totalUpdated = 0;
  let totalErrors = 0;
  const batchSize = 100;
  const updates = [];
  
  // Process each parent group
  for (const [parentId, nodes] of Object.entries(nodesByParent)) {
    // Sort nodes within this parent group
    const sortedNodes = sortNodesByAcademicOrder(nodes);
    
    // Assign display_order values
    sortedNodes.forEach((node, index) => {
      const newDisplayOrder = index + 1;
      
      // Only update if display_order is different or null
      if (node.display_order !== newDisplayOrder) {
        updates.push({
          id: node.id,
          display_order: newDisplayOrder,
          name: node.name,
          parent_id: node.parent_id
        });
      }
    });
  }
  
  console.log(`Total updates to make: ${updates.length}`);
  
  // Process updates in batches
  for (let i = 0; i < updates.length; i += batchSize) {
    const batch = updates.slice(i, i + batchSize);
    console.log(`Processing batch ${Math.floor(i / batchSize) + 1} of ${Math.ceil(updates.length / batchSize)}...`);
    
    for (const update of batch) {
      const { error } = await supabase
        .from('skill_tree_nodes')
        .update({ display_order: update.display_order })
        .eq('id', update.id);
      
      if (error) {
        console.error(`Error updating node ${update.name}:`, error);
        totalErrors++;
      } else {
        totalUpdated++;
        if (totalUpdated % 10 === 0) {
          console.log(`  Updated ${totalUpdated} nodes...`);
        }
      }
    }
    
    // Add a small delay between batches to avoid rate limiting
    if (i + batchSize < updates.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  console.log(`\nUpdate complete!`);
  console.log(`Successfully updated: ${totalUpdated} nodes`);
  console.log(`Errors: ${totalErrors}`);
  
  return { totalUpdated, totalErrors };
}

async function verifyUpdates() {
  console.log('\nVerifying updates...');
  
  // Check for nodes without display_order
  const { data: nodesWithoutOrder, error } = await supabase
    .from('skill_tree_nodes')
    .select('id, name, parent_id')
    .is('display_order', null)
    .limit(10);
  
  if (error) {
    console.error('Error verifying updates:', error);
    return;
  }
  
  if (nodesWithoutOrder && nodesWithoutOrder.length > 0) {
    console.log(`Found ${nodesWithoutOrder.length} nodes still without display_order:`);
    nodesWithoutOrder.forEach(node => {
      console.log(`  - ${node.name} (id: ${node.id})`);
    });
  } else {
    console.log('All nodes have display_order values!');
  }
  
  // Show some examples of the ordering
  const { data: examples, error: exampleError } = await supabase
    .from('skill_tree_nodes')
    .select('name, display_order, parent_id')
    .not('display_order', 'is', null)
    .order('parent_id', { ascending: true })
    .order('display_order', { ascending: true })
    .limit(20);
  
  if (!exampleError && examples) {
    console.log('\nExample orderings:');
    let currentParent = null;
    examples.forEach(node => {
      if (node.parent_id !== currentParent) {
        currentParent = node.parent_id;
        console.log(`\n  Parent ID: ${currentParent || 'root'}`);
      }
      console.log(`    ${node.display_order}. ${node.name}`);
    });
  }
}

async function main() {
  console.log('Starting display_order update process...\n');
  
  // Step 1: Check current state
  await checkCurrentState();
  
  // Step 2: Note about backup
  const backupName = await createBackupTable();
  console.log('\nIMPORTANT: Please create a manual backup of skill_tree_nodes table through Supabase dashboard');
  console.log('Suggested backup name:', backupName);
  console.log('\nPress Ctrl+C to cancel, or wait 10 seconds to continue...');
  await new Promise(resolve => setTimeout(resolve, 10000));
  
  // Step 3: Get all nodes grouped by parent
  const result = await getNodesByParent();
  if (!result) {
    console.error('Failed to fetch nodes. Exiting.');
    return;
  }
  
  const { nodesByParent } = result;
  
  // Step 4: Update display orders
  const updateResult = await updateDisplayOrders(nodesByParent);
  
  // Step 5: Verify the updates
  await verifyUpdates();
  
  console.log('\nProcess complete!');
}

// Run the script
main().catch(console.error);