const { createClient } = require('@supabase/supabase-js');

// Supabase configuration
const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyNDEzMzUsImV4cCI6MjA3MDgxNzMzNX0.k21_FmGqGsojgPMKN97-dZI-y5kwrbxKGZcGpDnikG4';

const supabase = createClient(supabaseUrl, supabaseKey);

async function analyzeDatabase() {
  console.log('=== Database Structure Analysis ===\n');
  
  try {
    // 1. Check user_progress table structure
    console.log('1. USER_PROGRESS TABLE STRUCTURE:');
    console.log('=====================================');
    
    const { data: userProgressData, error: userProgressError } = await supabase
      .from('user_progress')
      .select('*')
      .limit(1);
    
    if (userProgressError) {
      console.log('Error querying user_progress:', userProgressError.message);
    } else if (userProgressData && userProgressData.length > 0) {
      console.log('Sample row from user_progress:');
      console.log(JSON.stringify(userProgressData[0], null, 2));
      console.log('\nColumn names and types:');
      Object.keys(userProgressData[0]).forEach(key => {
        const value = userProgressData[0][key];
        const type = value === null ? 'null' : typeof value;
        console.log(`  ${key}: ${type} (sample: ${value})`);
      });
    } else {
      console.log('No data found in user_progress table');
    }
    
    console.log('\n');
    
    // 2. Check skill_tree_nodes table structure and find Money Counting
    console.log('2. SKILL_TREE_NODES TABLE STRUCTURE:');
    console.log('====================================');
    
    const { data: skillTreeData, error: skillTreeError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .limit(1);
    
    if (skillTreeError) {
      console.log('Error querying skill_tree_nodes:', skillTreeError.message);
    } else if (skillTreeData && skillTreeData.length > 0) {
      console.log('Sample row from skill_tree_nodes:');
      console.log(JSON.stringify(skillTreeData[0], null, 2));
      console.log('\nColumn names and types:');
      Object.keys(skillTreeData[0]).forEach(key => {
        const value = skillTreeData[0][key];
        const type = value === null ? 'null' : typeof value;
        console.log(`  ${key}: ${type} (sample: ${value})`);
      });
    } else {
      console.log('No data found in skill_tree_nodes table');
    }
    
    console.log('\n');
    
    // 3. Find Money Counting in skill_tree_nodes
    console.log('3. SEARCHING FOR MONEY COUNTING:');
    console.log('================================');
    
    const { data: moneyCountingNodes, error: moneyError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .ilike('name', '%money%counting%')
      .limit(5);
    
    if (moneyError) {
      console.log('Error searching for Money Counting:', moneyError.message);
    } else if (moneyCountingNodes && moneyCountingNodes.length > 0) {
      console.log(`Found ${moneyCountingNodes.length} node(s) matching "money counting":`);
      moneyCountingNodes.forEach((node, index) => {
        console.log(`\nNode ${index + 1}:`);
        console.log(`  ID: ${node.id} (Type: ${typeof node.id})`);
        console.log(`  Name: ${node.name}`);
        console.log(`  Parent ID: ${node.parent_id}`);
        if (node.has_learning_content !== undefined) {
          console.log(`  Has Learning Content: ${node.has_learning_content}`);
        }
        if (node.learning_content_ids !== undefined) {
          console.log(`  Learning Content IDs: ${JSON.stringify(node.learning_content_ids)}`);
        }
      });
    } else {
      console.log('No nodes found matching "money counting"');
      
      // Try broader search
      const { data: moneyNodes, error: moneyBroadError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .ilike('name', '%money%')
        .limit(10);
        
      if (!moneyBroadError && moneyNodes && moneyNodes.length > 0) {
        console.log(`\nFound ${moneyNodes.length} node(s) with "money" in the name:`);
        moneyNodes.forEach((node, index) => {
          console.log(`  ${index + 1}. ID: ${node.id}, Name: ${node.name}`);
        });
      }
    }
    
    console.log('\n');
    
    // 4. Analyze skill_id relationship
    console.log('4. SKILL_ID RELATIONSHIP ANALYSIS:');
    console.log('==================================');
    
    // Get a few user_progress rows to see skill_id values
    const { data: progressSample, error: progressSampleError } = await supabase
      .from('user_progress')
      .select('skill_id, status, user_id')
      .limit(5);
    
    if (progressSampleError) {
      console.log('Error getting user_progress sample:', progressSampleError.message);
    } else if (progressSample && progressSample.length > 0) {
      console.log('Sample skill_id values from user_progress:');
      progressSample.forEach((row, index) => {
        console.log(`  Row ${index + 1}: skill_id = ${row.skill_id} (Type: ${typeof row.skill_id}), Status: ${row.status}`);
      });
      
      // Try to match some skill_ids with skill_tree_nodes
      console.log('\nTrying to match skill_ids with skill_tree_nodes...');
      const skillIds = progressSample.map(row => row.skill_id);
      
      for (let skillId of skillIds.slice(0, 3)) { // Check first 3
        const { data: matchingNode, error: matchError } = await supabase
          .from('skill_tree_nodes')
          .select('id, name')
          .eq('id', skillId)
          .single();
        
        if (!matchError && matchingNode) {
          console.log(`  skill_id ${skillId} matches node: "${matchingNode.name}"`);
        } else {
          console.log(`  skill_id ${skillId} - no matching node found`);
        }
      }
    } else {
      console.log('No data found in user_progress table for analysis');
    }
    
    console.log('\n');
    
    // 5. Check if there are any integer-based IDs in skill_tree_nodes
    console.log('5. ID FORMAT ANALYSIS:');
    console.log('======================');
    
    const { data: allNodes, error: allNodesError } = await supabase
      .from('skill_tree_nodes')
      .select('id')
      .limit(10);
    
    if (!allNodesError && allNodes) {
      console.log('Sample skill_tree_nodes IDs:');
      allNodes.forEach((node, index) => {
        const isUUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(node.id);
        const isInteger = /^\d+$/.test(node.id.toString());
        console.log(`  ${index + 1}. ID: ${node.id} (UUID: ${isUUID}, Integer: ${isInteger})`);
      });
    }
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

// Run the analysis
analyzeDatabase().then(() => {
  console.log('\nAnalysis complete!');
}).catch(error => {
  console.error('Script error:', error);
});