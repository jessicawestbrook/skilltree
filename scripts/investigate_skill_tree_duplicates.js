// Load environment variables first
require('dotenv').config({ path: '.env.local' });

const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

console.log('Environment check:');
console.log('REACT_APP_SUPABASE_URL:', supabaseUrl ? 'SET' : 'NOT SET');
console.log('REACT_APP_SUPABASE_ANON_KEY:', supabaseKey ? 'SET' : 'NOT SET');

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function investigateDuplicates() {
  console.log('=== SKILL TREE NODES DUPLICATE INVESTIGATION ===\n');

  try {
    // 1. Check total count of nodes
    console.log('1. Total count of nodes:');
    const { count: totalCount, error: countError } = await supabase
      .from('skill_tree_nodes')
      .select('*', { count: 'exact', head: true });
    
    if (countError) throw countError;
    console.log(`   Total nodes: ${totalCount}\n`);

    // Get all nodes to analyze in JS since we may not have custom RPC functions
    console.log('   Fetching all nodes for analysis...');
    const { data: allNodes, error: allNodesError } = await supabase
      .from('skill_tree_nodes')
      .select('*');
    
    if (allNodesError) throw allNodesError;
    console.log(`   Fetched ${allNodes.length} nodes\n`);

    // Show column structure for first node
    if (allNodes.length > 0) {
      console.log('   Column structure (first node):');
      console.log('   ', Object.keys(allNodes[0]).join(', '));
      console.log();
    }

    // 2. Find duplicate node names and how many times each appears
    console.log('2. Duplicate node names analysis:');
    
    // Count name occurrences
    const nameCount = {};
    allNodes.forEach(node => {
      if (node.name) {
        nameCount[node.name] = (nameCount[node.name] || 0) + 1;
      }
    });
    
    const duplicateNames = Object.entries(nameCount)
      .filter(([name, count]) => count > 1)
      .sort((a, b) => b[1] - a[1]);
    
    console.log(`   Total unique names: ${Object.keys(nameCount).length}`);
    console.log(`   Names appearing multiple times: ${duplicateNames.length}`);
    
    if (duplicateNames.length > 0) {
      console.log('   Top duplicate names:');
      duplicateNames.slice(0, 20).forEach(([name, count]) => {
        console.log(`     "${name}": ${count} times`);
      });
    }
    console.log();

    // 3. Check if nodes have the same name AND parent_id (true duplicates)
    console.log('3. True duplicates (same name + parent_id):');
    const parentNameCount = {};
    allNodes.forEach(node => {
      if (node.name) {
        const key = `${node.name}|${node.parent_id || 'NULL'}`;
        if (!parentNameCount[key]) {
          parentNameCount[key] = [];
        }
        parentNameCount[key].push(node);
      }
    });
    
    const trueDuplicates = Object.entries(parentNameCount)
      .filter(([key, nodes]) => nodes.length > 1)
      .sort((a, b) => b[1].length - a[1].length);
    
    console.log(`   True duplicate groups: ${trueDuplicates.length}`);
    
    if (trueDuplicates.length > 0) {
      console.log('   True duplicate details:');
      trueDuplicates.slice(0, 20).forEach(([key, nodes]) => {
        const [name, parentId] = key.split('|');
        console.log(`     "${name}" (parent: ${parentId === 'NULL' ? 'null' : parentId}): ${nodes.length} nodes`);
        nodes.forEach(node => {
          console.log(`       - ID: ${node.id}, Created: ${node.created_at}`);
        });
      });
    }
    console.log();

    // 4. Look for patterns in created_at timestamps
    console.log('4. Creation timestamp patterns:');
    const createdDates = allNodes.map(node => new Date(node.created_at).toDateString());
    const dateCount = {};
    createdDates.forEach(date => {
      dateCount[date] = (dateCount[date] || 0) + 1;
    });
    
    const sortedDates = Object.entries(dateCount)
      .sort((a, b) => b[1] - a[1]);
    
    console.log('   Days with most node creation:');
    sortedDates.slice(0, 10).forEach(([date, count]) => {
      console.log(`     ${date}: ${count} nodes`);
    });
    
    // Look for batch creation patterns (same minute)
    const createdMinutes = allNodes.map(node => {
      const date = new Date(node.created_at);
      return `${date.toDateString()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
    });
    const minuteCount = {};
    createdMinutes.forEach(minute => {
      minuteCount[minute] = (minuteCount[minute] || 0) + 1;
    });
    
    const batchCreations = Object.entries(minuteCount)
      .filter(([minute, count]) => count > 10)
      .sort((a, b) => b[1] - a[1]);
    
    if (batchCreations.length > 0) {
      console.log('\n   Possible batch creations (>10 nodes in same minute):');
      batchCreations.slice(0, 10).forEach(([minute, count]) => {
        console.log(`     ${minute}: ${count} nodes`);
      });
    }
    console.log();

    // 5. Learning content analysis
    console.log('5. Learning content analysis:');
    
    // Check what learning content fields exist
    const hasLearningContentField = allNodes.length > 0 && 'has_learning_content' in allNodes[0];
    const learningContentIdsField = allNodes.length > 0 && 'learning_content_ids' in allNodes[0];
    
    console.log(`   Has 'has_learning_content' field: ${hasLearningContentField}`);
    console.log(`   Has 'learning_content_ids' field: ${learningContentIdsField}`);
    
    if (hasLearningContentField) {
      const withContent = allNodes.filter(node => node.has_learning_content === true);
      const withoutContent = allNodes.filter(node => node.has_learning_content === false || node.has_learning_content === null);
      
      console.log(`   Nodes with learning content: ${withContent.length}`);
      console.log(`   Nodes without learning content: ${withoutContent.length}`);
      
      // Check duplicates in content vs non-content nodes
      const duplicatesWithContent = trueDuplicates.filter(([key, nodes]) => 
        nodes.some(node => node.has_learning_content === true));
      
      console.log(`   True duplicates that include nodes with content: ${duplicatesWithContent.length}`);
    }
    
    if (learningContentIdsField) {
      const withContentIds = allNodes.filter(node => node.learning_content_ids && node.learning_content_ids.length > 0);
      console.log(`   Nodes with learning content IDs: ${withContentIds.length}`);
    }
    console.log();

    // 6. Check for multiple root nodes
    console.log('6. Root nodes analysis:');
    const rootNodes = allNodes.filter(node => node.parent_id === null);
    console.log(`   Total root nodes (parent_id is null): ${rootNodes.length}`);
    
    if (rootNodes.length > 0) {
      console.log('   Root node details:');
      rootNodes.forEach(node => {
        console.log(`     - ID: ${node.id}, Name: "${node.name}", Created: ${node.created_at}`);
      });
    }
    console.log();

    // 7. Check for orphaned nodes
    console.log('7. Orphaned nodes analysis:');
    const nodeIds = new Set(allNodes.map(node => node.id));
    const orphanedNodes = allNodes.filter(node => 
      node.parent_id !== null && !nodeIds.has(node.parent_id));
    
    console.log(`   Orphaned nodes (parent_id doesn't exist): ${orphanedNodes.length}`);
    if (orphanedNodes.length > 0) {
      console.log('   Orphaned node details:');
      orphanedNodes.forEach(node => {
        console.log(`     - ID: ${node.id}, Name: "${node.name}", Parent ID: ${node.parent_id}`);
      });
    }
    console.log();

    // 8. Summary statistics
    console.log('8. Summary:');
    console.log(`   - Total nodes: ${allNodes.length}`);
    console.log(`   - Unique names: ${Object.keys(nameCount).length}`);
    console.log(`   - Duplicate name groups: ${duplicateNames.length}`);
    console.log(`   - True duplicate groups (name + parent): ${trueDuplicates.length}`);
    console.log(`   - Root nodes: ${rootNodes.length}`);
    console.log(`   - Orphaned nodes: ${orphanedNodes.length}`);
    
    if (learningContentIdsField) {
      const withContentIds = allNodes.filter(node => node.learning_content_ids && node.learning_content_ids.length > 0);
      console.log(`   - Nodes with learning content IDs: ${withContentIds.length}`);
      console.log(`   - Nodes without learning content IDs: ${allNodes.length - withContentIds.length}`);
    }

    console.log('\n=== INVESTIGATION COMPLETE ===');

  } catch (error) {
    console.error('Error during investigation:', error);
  }
}

// Run the investigation
investigateDuplicates();