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

async function simulateProfilePageData() {
  console.log('\n=== Simulating ProfilePage Data Loading ===\n');
  
  try {
    // Get the first user with any data
    const { data: users, error: usersError } = await supabase
      .from('profiles')
      .select('id, email');
    
    if (usersError || !users || users.length === 0) {
      console.error('Error getting users:', usersError);
      return;
    }
    
    const testUser = users[0];
    console.log(`Testing with user: ${testUser.email} (ID: ${testUser.id})`);
    
    // Step 1: Simulate fetchUserData() - Recent Progress
    console.log('\n=== 1. Fetching Recent Progress (fetchUserData) ===');
    
    const { data: progressData, error: progressError } = await supabase
      .from('user_progress')
      .select(`
        *,
        skill_tree_nodes!skill_id (
          id,
          name,
          description
        )
      `)
      .eq('user_id', testUser.id)
      .order('last_accessed', { ascending: false });
    
    if (progressError) {
      console.error('Error getting progress:', progressError);
    } else {
      console.log(`Found ${progressData?.length || 0} progress records`);
      
      const recentProgress = progressData?.slice(0, 5) || [];
      if (recentProgress.length > 0) {
        console.log('Top 5 recent progress items:');
        recentProgress.forEach((item, index) => {
          const nodeName = item.skill_tree_nodes?.name || 'Unknown Node';
          console.log(`  ${index + 1}. ${nodeName} (${item.skill_id}) - Status: ${item.status}`);
          if (item.skill_id === MONEY_COUNTING_ID) {
            console.log('    ^^^ MONEY COUNTING IN RECENT ACTIVITY! ^^^');
          }
        });
      } else {
        console.log('  No recent progress found');
      }
    }
    
    // Step 2: Simulate fetchRecommendedContent() 
    console.log('\n=== 2. Fetching Recommendations (fetchRecommendedContent) ===');
    
    // This would call recommendationService.getRecommendations()
    // Let's simulate the basic fallback logic that happens when recommendations fail
    
    console.log('Simulating fallback recommendations query...');
    
    const { data: fallbackNodes, error: fallbackError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .not('learning_content_ids', 'eq', '{}')
      .limit(6)
      .order('updated_at', { ascending: false });
    
    if (fallbackError) {
      console.error('Error getting fallback recommendations:', fallbackError);
    } else {
      console.log(`Found ${fallbackNodes?.length || 0} fallback recommendation candidates`);
      
      if (fallbackNodes && fallbackNodes.length > 0) {
        console.log('Fallback recommendations:');
        fallbackNodes.forEach((node, index) => {
          console.log(`  ${index + 1}. ${node.name} (${node.id})`);
          console.log(`     Has Learning Content: ${node.has_learning_content}`);
          console.log(`     Learning Content IDs: ${JSON.stringify(node.learning_content_ids)}`);
          if (node.id === MONEY_COUNTING_ID) {
            console.log('    ^^^ MONEY COUNTING IN FALLBACK RECOMMENDATIONS! ^^^');
          }
        });
      }
    }
    
    // Step 3: Check if Money Counting would be in the recommendation service
    console.log('\n=== 3. Check Recommendation Service Candidates ===');
    
    // Simulate the main recommendation query
    const completedNodes = progressData?.filter(p => p.status === 'completed').map(p => p.skill_id) || [];
    const inProgressNodes = progressData?.filter(p => p.status === 'in_progress').map(p => p.skill_id) || [];
    const excludedNodes = [...completedNodes, ...inProgressNodes];
    
    console.log(`Excluding ${excludedNodes.length} completed/in-progress nodes`);
    
    let nodesQuery = supabase
      .from('skill_tree_nodes')
      .select('*')
      .not('learning_content_ids', 'eq', '{}');
    
    if (excludedNodes.length > 0) {
      nodesQuery = nodesQuery.not('id', 'in', `(${excludedNodes.join(',')})`);
    }
    
    const { data: candidateNodes, error: candidateError } = await nodesQuery;
    
    if (candidateError) {
      console.error('Error getting recommendation candidates:', candidateError);
    } else {
      const moneyCountingCandidate = candidateNodes?.find(n => n.id === MONEY_COUNTING_ID);
      
      if (moneyCountingCandidate) {
        console.log('✓ Money Counting IS a recommendation candidate');
        console.log(`  Reason: Has learning content IDs: ${JSON.stringify(moneyCountingCandidate.learning_content_ids)}`);
        console.log('  This means it WOULD appear in recommendations');
      } else {
        console.log('✗ Money Counting is NOT a recommendation candidate');
      }
    }
    
    // Step 4: Check user interest levels that might affect recommendations
    console.log('\n=== 4. Check User Interest Levels ===');
    
    const { data: interests, error: interestError } = await supabase
      .from('user_interest_levels')
      .select('*')
      .eq('user_id', testUser.id);
    
    if (interestError) {
      console.error('Error getting user interests:', interestError);
    } else {
      console.log(`User has ${interests?.length || 0} interest level records`);
      if (interests && interests.length > 0) {
        interests.forEach((interest, index) => {
          console.log(`  ${index + 1}. ${interest.category}: ${interest.interest_level}/10`);
        });
      }
    }
    
  } catch (error) {
    console.error('Script error:', error);
  }
  
  process.exit(0);
}

simulateProfilePageData();