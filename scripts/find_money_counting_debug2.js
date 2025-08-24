const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function findMoneyCountingModule() {
  console.log('\n=== Finding Money Counting Module ===\n');
  
  try {
    // Find the Money Counting node
    const { data: nodes, error: nodeError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .ilike('name', '%Money Counting%');
    
    if (nodeError) {
      console.error('Error finding Money Counting node:', nodeError);
      return;
    }
    
    if (!nodes || nodes.length === 0) {
      console.log('No Money Counting module found in skill_tree_nodes');
      return;
    }
    
    console.log('Found Money Counting nodes:');
    nodes.forEach((node, index) => {
      console.log(`  ${index + 1}. ID: ${node.id}, Name: ${node.name}`);
      console.log(`     Parent ID: ${node.parent_id}`);
      console.log(`     Has Learning Content: ${node.has_learning_content}`);
      console.log(`     Learning Content IDs: ${JSON.stringify(node.learning_content_ids)}`);
      console.log('');
    });
    
    // Check for user progress on these nodes
    console.log('\n=== Checking User Progress ===\n');
    
    for (const node of nodes) {
      console.log(`Checking progress for node ${node.name} (ID: ${node.id}):`);
      
      const { data: progress, error: progressError } = await supabase
        .from('user_progress')
        .select('*')
        .eq('skill_id', node.id);
      
      if (progressError) {
        console.error('  Error getting progress:', progressError);
        continue;
      }
      
      if (!progress || progress.length === 0) {
        console.log('  No user progress found for this node');
      } else {
        console.log(`  Found ${progress.length} progress records:`);
        progress.forEach((p, i) => {
          console.log(`    ${i + 1}. User: ${p.user_id}, Status: ${p.status}, Last Accessed: ${p.last_accessed}`);
        });
      }
      console.log('');
    }
    
    // Check starred items
    console.log('\n=== Checking Starred Items ===\n');
    
    for (const node of nodes) {
      const { data: starred, error: starredError } = await supabase
        .from('starred_items')
        .select('*')
        .eq('item_id', node.id)
        .eq('item_type', 'skill_node');
      
      if (starredError) {
        console.error(`  Error getting starred items for ${node.name}:`, starredError);
        continue;
      }
      
      if (!starred || starred.length === 0) {
        console.log(`  ${node.name} is not starred by any users`);
      } else {
        console.log(`  ${node.name} is starred by ${starred.length} users:`);
        starred.forEach((s, i) => {
          console.log(`    ${i + 1}. User: ${s.user_id}, Starred At: ${s.starred_at}`);
        });
      }
      console.log('');
    }
    
  } catch (error) {
    console.error('Script error:', error);
  }
  
  process.exit(0);
}

findMoneyCountingModule();