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

async function checkAllUsers() {
  console.log('\n=== Checking All Users for Money Counting Progress ===\n');
  
  try {
    // Get all users
    const { data: users, error: usersError } = await supabase
      .from('profiles')
      .select('id, email');
    
    if (usersError) {
      console.error('Error getting users:', usersError);
      return;
    }
    
    console.log(`Found ${users?.length || 0} users to check`);
    
    for (const user of users || []) {
      console.log(`\nChecking user: ${user.email} (${user.id})`);
      
      // Check if this user has Money Counting in their progress
      const { data: progress, error: progressError } = await supabase
        .from('user_progress')
        .select('*')
        .eq('user_id', user.id)
        .eq('skill_id', MONEY_COUNTING_ID);
      
      if (progressError) {
        console.error(`  Error getting progress: ${progressError.message}`);
        continue;
      }
      
      if (progress && progress.length > 0) {
        console.log(`  ⚠ HAS Money Counting progress!`);
        progress.forEach((p, i) => {
          console.log(`    ${i + 1}. Status: ${p.status}, Rating: ${p.rating}, Last Accessed: ${p.last_accessed}`);
        });
      } else {
        console.log(`  ✓ No Money Counting progress`);
      }
      
      // Also check their recent progress to see what shows up in Recent Activity
      const { data: recentProgress, error: recentError } = await supabase
        .from('user_progress')
        .select(`
          *,
          skill_tree_nodes!skill_id (
            id,
            name,
            description
          )
        `)
        .eq('user_id', user.id)
        .order('last_accessed', { ascending: false })
        .limit(5);
      
      if (recentError) {
        console.log(`  Error getting recent progress: ${recentError.message}`);
        continue;
      }
      
      if (recentProgress && recentProgress.length > 0) {
        console.log(`  Recent progress (${recentProgress.length} items):`);
        recentProgress.forEach((item, index) => {
          const nodeName = item.skill_tree_nodes?.name || 'Unknown Node';
          console.log(`    ${index + 1}. ${nodeName} (${item.skill_id}) - ${item.status}`);
          if (item.skill_id === MONEY_COUNTING_ID) {
            console.log(`      ^^^ THIS IS MONEY COUNTING IN RECENT ACTIVITY! ^^^`);
          }
        });
      } else {
        console.log(`  No recent progress found`);
      }
    }
    
    // Also check for any orphaned progress records that might reference Money Counting
    console.log('\n=== Checking for Any Money Counting Progress Records ===\n');
    
    const { data: allMoneyProgress, error: allProgressError } = await supabase
      .from('user_progress')
      .select('*')
      .eq('skill_id', MONEY_COUNTING_ID);
    
    if (allProgressError) {
      console.error('Error getting all Money Counting progress:', allProgressError);
    } else {
      console.log(`Found ${allMoneyProgress?.length || 0} total Money Counting progress records`);
      
      if (allMoneyProgress && allMoneyProgress.length > 0) {
        allMoneyProgress.forEach((p, i) => {
          console.log(`  ${i + 1}. User: ${p.user_id}, Status: ${p.status}, Last Accessed: ${p.last_accessed}`);
        });
      }
    }
    
  } catch (error) {
    console.error('Script error:', error);
  }
  
  process.exit(0);
}

checkAllUsers();