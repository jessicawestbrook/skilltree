const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function analyzeLearningContent() {
  console.log('\n=== Analyzing Learning Content Distribution ===\n');
  
  try {
    // Get all nodes with learning content
    const { data: allNodesWithContent, error: contentError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .not('learning_content_ids', 'eq', '{}')
      .order('name');
    
    if (contentError) {
      console.error('Error getting nodes with content:', contentError);
      return;
    }
    
    console.log(`Total nodes with learning content: ${allNodesWithContent?.length || 0}`);
    
    if (allNodesWithContent && allNodesWithContent.length > 0) {
      console.log('\nNodes with learning content:');
      allNodesWithContent.forEach((node, index) => {
        console.log(`  ${index + 1}. ${node.name} (ID: ${node.id})`);
        console.log(`     Content IDs: ${JSON.stringify(node.learning_content_ids)}`);
        console.log(`     Parent: ${node.parent_id}`);
        if (node.name.toLowerCase().includes('money')) {
          console.log('     ^^^ MONEY-RELATED NODE ^^^');
        }
      });
    }
    
    // Check which nodes have user progress
    console.log('\n=== Checking User Progress Distribution ===\n');
    
    const { data: allProgress, error: progressError } = await supabase
      .from('user_progress')
      .select('skill_id, status')
      .order('skill_id');
    
    if (progressError) {
      console.error('Error getting all progress:', progressError);
      return;
    }
    
    console.log(`Total user progress records: ${allProgress?.length || 0}`);
    
    // Group by skill_id
    const progressBySkill = {};
    if (allProgress) {
      allProgress.forEach(p => {
        if (!progressBySkill[p.skill_id]) {
          progressBySkill[p.skill_id] = [];
        }
        progressBySkill[p.skill_id].push(p.status);
      });
    }
    
    console.log(`Unique skills with progress: ${Object.keys(progressBySkill).length}`);
    
    // Check which learning content nodes have no progress
    if (allNodesWithContent) {
      const nodesWithoutProgress = allNodesWithContent.filter(node => !progressBySkill[node.id]);
      
      console.log('\n=== Learning Content Nodes WITHOUT User Progress ===\n');
      console.log(`Nodes with content but no user progress: ${nodesWithoutProgress.length}`);
      
      if (nodesWithoutProgress.length > 0 && nodesWithoutProgress.length <= 20) {
        nodesWithoutProgress.forEach((node, index) => {
          console.log(`  ${index + 1}. ${node.name} (${node.id})`);
        });
      } else if (nodesWithoutProgress.length > 20) {
        console.log('  (Too many to list - showing first 10)');
        nodesWithoutProgress.slice(0, 10).forEach((node, index) => {
          console.log(`  ${index + 1}. ${node.name} (${node.id})`);
        });
      }
    }
    
    // Check the fallback query that's causing the issue
    console.log('\n=== Analyzing Current Fallback Query Results ===\n');
    
    const { data: fallbackResults, error: fallbackError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .not('learning_content_ids', 'eq', '{}')
      .limit(6)
      .order('updated_at', { ascending: false });
    
    if (fallbackError) {
      console.error('Error with fallback query:', fallbackError);
    } else {
      console.log(`Fallback query returns ${fallbackResults?.length || 0} results:`);
      if (fallbackResults) {
        fallbackResults.forEach((node, index) => {
          console.log(`  ${index + 1}. ${node.name} (updated: ${node.updated_at})`);
        });
      }
    }
    
  } catch (error) {
    console.error('Script error:', error);
  }
  
  process.exit(0);
}

analyzeLearningContent();