const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

const MONEY_COUNTING_ID = 'fea1ba27-904d-4a1c-85d3-7e708a80727c';

async function debugRecommendations() {
  console.log('\n=== Debugging Money Counting in Recommendations ===\n');
  
  try {
    // Get the Money Counting node details
    const { data: moneyNode, error: nodeError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('id', MONEY_COUNTING_ID)
      .single();
    
    if (nodeError || !moneyNode) {
      console.error('Error getting Money Counting node:', nodeError);
      return;
    }
    
    console.log('Money Counting Node Details:');
    console.log(`  Name: ${moneyNode.name}`);
    console.log(`  Parent ID: ${moneyNode.parent_id}`);
    console.log(`  Learning Content IDs: ${JSON.stringify(moneyNode.learning_content_ids)}`);
    console.log(`  Has Learning Content: ${moneyNode.has_learning_content}`);
    console.log('');
    
    // Get a test user's data to simulate recommendations
    const { data: users, error: usersError } = await supabase
      .from('profiles')
      .select('id, email')
      .limit(1);
    
    if (usersError || !users || users.length === 0) {
      console.error('Error getting test user:', usersError);
      return;
    }
    
    const testUser = users[0];
    console.log(`Testing with user: ${testUser.email} (${testUser.id})`);
    
    // Check user's progress
    const { data: userProgress, error: progressError } = await supabase
      .from('user_progress')
      .select('*')
      .eq('user_id', testUser.id)
      .order('last_accessed', { ascending: false });
    
    if (progressError) {
      console.error('Error getting user progress:', progressError);
      return;
    }
    
    console.log(`\nUser has ${userProgress?.length || 0} progress records`);
    
    // Check user's starred items
    const { data: starred, error: starredError } = await supabase
      .from('starred_items')
      .select('*')
      .eq('user_id', testUser.id)
      .eq('item_type', 'skill_node');
    
    if (starredError) {
      console.error('Error getting starred items:', starredError);
      return;
    }
    
    console.log(`User has ${starred?.length || 0} starred items`);
    
    // Simulate recommendation query that would include Money Counting
    console.log('\n=== Simulating Recommendation Query ===\n');
    
    const completedNodes = userProgress?.filter(p => p.status === 'completed').map(p => p.skill_id) || [];
    const inProgressNodes = userProgress?.filter(p => p.status === 'in_progress').map(p => p.skill_id) || [];
    const excludedNodes = [...completedNodes, ...inProgressNodes];
    
    console.log(`Excluding ${excludedNodes.length} completed/in-progress nodes`);
    
    // Check if Money Counting would be returned in recommendations
    let recommendationQuery = supabase
      .from('skill_tree_nodes')
      .select('*')
      .not('learning_content_ids', 'eq', '{}');
    
    if (excludedNodes.length > 0) {
      // Check if Money Counting is in excluded list
      if (excludedNodes.includes(MONEY_COUNTING_ID)) {
        console.log('✓ Money Counting SHOULD be excluded (user has progress)');
      } else {
        console.log('⚠ Money Counting would NOT be excluded (no user progress)');
        
        // This means it could appear in recommendations
        const { data: candidateNodes, error: candidateError } = await recommendationQuery.eq('id', MONEY_COUNTING_ID);
        
        if (candidateError) {
          console.error('Error checking candidate:', candidateError);
        } else if (candidateNodes && candidateNodes.length > 0) {
          console.log('✓ Money Counting IS a valid recommendation candidate');
          console.log('  Reasons:');
          console.log('  - Has learning content');
          console.log('  - User has no progress on it');
          console.log('  - Not excluded from recommendations');
        }
      }
    }
    
    // Check why it might show in Recent Activity section
    console.log('\n=== Recent Activity Check ===\n');
    
    const recentProgressForThisNode = userProgress?.find(p => p.skill_id === MONEY_COUNTING_ID);
    if (recentProgressForThisNode) {
      console.log('⚠ FOUND: Money Counting DOES appear in user progress!');
      console.log(`  Status: ${recentProgressForThisNode.status}`);
      console.log(`  Last Accessed: ${recentProgressForThisNode.last_accessed}`);
      console.log(`  Rating: ${recentProgressForThisNode.rating}`);
    } else {
      console.log('✓ Money Counting does NOT appear in user progress');
    }
    
    // Final check: Show recent progress nodes
    console.log('\n=== Current Recent Progress Nodes ===\n');
    const recentTop5 = userProgress?.slice(0, 5) || [];
    
    if (recentTop5.length === 0) {
      console.log('No recent progress found');
    } else {
      console.log('Top 5 recent progress items:');
      recentTop5.forEach((item, index) => {
        console.log(`  ${index + 1}. ${item.skill_id} (Status: ${item.status}, Last: ${item.last_accessed})`);
        if (item.skill_id === MONEY_COUNTING_ID) {
          console.log('    ^^^ THIS IS MONEY COUNTING! ^^^');
        }
      });
    }
    
  } catch (error) {
    console.error('Script error:', error);
  }
  
  process.exit(0);
}

debugRecommendations();