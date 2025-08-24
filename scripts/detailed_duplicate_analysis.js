// Load environment variables first
require('dotenv').config({ path: '.env.local' });

const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function detailedAnalysis() {
  console.log('=== DETAILED SKILL TREE NODES ANALYSIS ===\n');

  try {
    // Get all nodes
    const { data: allNodes, error: allNodesError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .order('created_at');
    
    if (allNodesError) throw allNodesError;

    console.log(`Analyzing ${allNodes.length} nodes...\n`);

    // 1. Analyze duplicate patterns in detail
    console.log('1. DETAILED DUPLICATE NAME ANALYSIS:\n');
    
    const nameGroups = {};
    allNodes.forEach(node => {
      if (node.name) {
        if (!nameGroups[node.name]) {
          nameGroups[node.name] = [];
        }
        nameGroups[node.name].push(node);
      }
    });

    const duplicateGroups = Object.entries(nameGroups)
      .filter(([name, nodes]) => nodes.length > 1)
      .sort((a, b) => b[1].length - a[1].length);

    console.log(`Found ${duplicateGroups.length} duplicate name groups:\n`);

    duplicateGroups.forEach(([name, nodes], index) => {
      console.log(`${index + 1}. "${name}" (${nodes.length} instances):`);
      
      // Group by parent to see if they're in different branches
      const parentGroups = {};
      nodes.forEach(node => {
        const parentId = node.parent_id || 'ROOT';
        if (!parentGroups[parentId]) {
          parentGroups[parentId] = [];
        }
        parentGroups[parentId].push(node);
      });

      Object.entries(parentGroups).forEach(([parentId, siblingNodes]) => {
        if (parentId === 'ROOT') {
          console.log(`   Root level nodes: ${siblingNodes.length}`);
        } else {
          console.log(`   Under parent ${parentId}: ${siblingNodes.length} nodes`);
        }
        
        siblingNodes.forEach(node => {
          const hasContent = node.learning_content_ids && node.learning_content_ids.length > 0 ? 'YES' : 'NO';
          const createdDate = new Date(node.created_at).toLocaleString();
          console.log(`     - ID: ${node.id}, Created: ${createdDate}, Has Content: ${hasContent}`);
        });
      });
      console.log();
    });

    // 2. Analyze hierarchy patterns
    console.log('2. HIERARCHY ANALYSIS:\n');
    
    // Build parent-child relationships
    const childrenMap = {};
    const parentMap = {};
    
    allNodes.forEach(node => {
      if (node.parent_id) {
        if (!childrenMap[node.parent_id]) {
          childrenMap[node.parent_id] = [];
        }
        childrenMap[node.parent_id].push(node);
        parentMap[node.id] = node.parent_id;
      }
    });

    // Find nodes with many children
    const parentStats = Object.entries(childrenMap)
      .map(([parentId, children]) => ({
        parentId,
        childCount: children.length,
        parentNode: allNodes.find(n => n.id === parentId)
      }))
      .sort((a, b) => b.childCount - a.childCount);

    console.log('Parents with most children:');
    parentStats.slice(0, 10).forEach(({ parentNode, childCount }) => {
      if (parentNode) {
        console.log(`   "${parentNode.name}" (${parentNode.id}): ${childCount} children`);
      }
    });
    console.log();

    // 3. Analyze batch creation patterns more deeply
    console.log('3. BATCH CREATION ANALYSIS:\n');
    
    const batchAnalysis = {};
    allNodes.forEach(node => {
      const date = new Date(node.created_at);
      const batchKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
      
      if (!batchAnalysis[batchKey]) {
        batchAnalysis[batchKey] = [];
      }
      batchAnalysis[batchKey].push(node);
    });

    const largeBatches = Object.entries(batchAnalysis)
      .filter(([batch, nodes]) => nodes.length > 5)
      .sort((a, b) => b[1].length - a[1].length);

    console.log('Large batch creation events:');
    largeBatches.forEach(([batch, nodes]) => {
      console.log(`   ${batch}: ${nodes.length} nodes`);
      
      // Sample some node names from this batch
      const sampleNames = nodes.slice(0, 5).map(n => n.name);
      console.log(`     Sample names: ${sampleNames.join(', ')}`);
      
      // Check if there are duplicates within this batch
      const batchNameCounts = {};
      nodes.forEach(node => {
        if (node.name) {
          batchNameCounts[node.name] = (batchNameCounts[node.name] || 0) + 1;
        }
      });
      
      const batchDuplicates = Object.entries(batchNameCounts)
        .filter(([name, count]) => count > 1);
      
      if (batchDuplicates.length > 0) {
        console.log(`     Duplicates in this batch: ${batchDuplicates.length} name groups`);
        batchDuplicates.slice(0, 3).forEach(([name, count]) => {
          console.log(`       "${name}": ${count} times`);
        });
      }
    });
    console.log();

    // 4. Learning content analysis
    console.log('4. LEARNING CONTENT ANALYSIS:\n');
    
    const nodeWithContent = allNodes.find(node => node.learning_content_ids && node.learning_content_ids.length > 0);
    if (nodeWithContent) {
      console.log('Node with learning content:');
      console.log(`   ID: ${nodeWithContent.id}`);
      console.log(`   Name: "${nodeWithContent.name}"`);
      console.log(`   Parent ID: ${nodeWithContent.parent_id}`);
      console.log(`   Content IDs: ${JSON.stringify(nodeWithContent.learning_content_ids)}`);
      console.log(`   Created: ${nodeWithContent.created_at}`);
    }
    console.log();

    // 5. Generate duplicate resolution recommendations
    console.log('5. DUPLICATE RESOLUTION RECOMMENDATIONS:\n');
    
    // Focus on duplicates that are likely problematic
    const problematicDuplicates = duplicateGroups.filter(([name, nodes]) => {
      // Filter for duplicates that might actually be mistakes
      return nodes.length > 2 || // More than 2 instances
        nodes.some(node => node.learning_content_ids && node.learning_content_ids.length > 0); // Has content
    });

    if (problematicDuplicates.length > 0) {
      console.log('Potentially problematic duplicates that may need review:');
      problematicDuplicates.forEach(([name, nodes]) => {
        console.log(`\n   "${name}" (${nodes.length} instances):`);
        console.log('   Action needed: Review if these should be separate categories or merged');
        
        // Show hierarchy paths for context
        nodes.forEach(node => {
          const path = getNodePath(node, allNodes, parentMap);
          const hasContent = node.learning_content_ids && node.learning_content_ids.length > 0 ? ' [HAS CONTENT]' : '';
          console.log(`     Path: ${path}${hasContent}`);
        });
      });
    } else {
      console.log('Most duplicates appear to be intentional (same topic in different branches)');
    }

    console.log('\n=== ANALYSIS COMPLETE ===');
    
    // Save detailed report
    const report = {
      timestamp: new Date().toISOString(),
      summary: {
        totalNodes: allNodes.length,
        uniqueNames: Object.keys(nameGroups).length,
        duplicateNameGroups: duplicateGroups.length,
        problematicDuplicates: problematicDuplicates.length,
        rootNodes: allNodes.filter(n => !n.parent_id).length,
        nodesWithContent: allNodes.filter(n => n.learning_content_ids && n.learning_content_ids.length > 0).length
      },
      duplicateGroups: duplicateGroups.map(([name, nodes]) => ({
        name,
        count: nodes.length,
        nodes: nodes.map(n => ({
          id: n.id,
          parentId: n.parent_id,
          hasContent: !!(n.learning_content_ids && n.learning_content_ids.length > 0),
          createdAt: n.created_at
        }))
      })),
      batchCreationEvents: largeBatches.map(([batch, nodes]) => ({
        batch,
        nodeCount: nodes.length,
        sampleNames: nodes.slice(0, 10).map(n => n.name)
      }))
    };

    fs.writeFileSync('scripts/duplicate_analysis_report.json', JSON.stringify(report, null, 2));
    console.log('\nDetailed report saved to scripts/duplicate_analysis_report.json');

  } catch (error) {
    console.error('Error during analysis:', error);
  }
}

function getNodePath(node, allNodes, parentMap) {
  const path = [node.name];
  let currentId = node.parent_id;
  
  while (currentId) {
    const parent = allNodes.find(n => n.id === currentId);
    if (parent) {
      path.unshift(parent.name);
      currentId = parent.parent_id;
    } else {
      break;
    }
  }
  
  return path.join(' > ');
}

// Run the analysis
detailedAnalysis();