const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function addUserProgress(userEmail, nodeName, status = 'in_progress', rating = 0) {
  try {
    console.log(`\nAdding progress for "${nodeName}" to user ${userEmail}...`);
    
    // Get user ID from email
    const { data: userData, error: userError } = await supabase
      .from('profiles')
      .select('id')
      .or(`email.eq.${userEmail}`)
      .single();
    
    // If no profile, try auth.users directly
    let userId;
    if (userError || !userData) {
      console.log('Profile not found, checking auth.users...');
      const { data: authData, error: authError } = await supabase.auth.admin.listUsers();
      if (authError) {
        console.error('Error finding user:', authError);
        return;
      }
      const user = authData.users.find(u => u.email === userEmail);
      if (!user) {
        console.error(`User with email ${userEmail} not found`);
        return;
      }
      userId = user.id;
    } else {
      userId = userData.id;
    }
    
    console.log(`Found user ID: ${userId}`);
    
    // Find the node
    const { data: nodeData, error: nodeError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, learning_area')
      .ilike('name', `%${nodeName}%`)
      .limit(1)
      .single();
    
    if (nodeError || !nodeData) {
      console.error(`Node "${nodeName}" not found:`, nodeError);
      return;
    }
    
    console.log(`Found node: ${nodeData.name} (${nodeData.id})`);
    
    // Check if progress already exists
    const { data: existingProgress, error: checkError } = await supabase
      .from('user_progress')
      .select('*')
      .eq('user_id', userId)
      .eq('skill_id', nodeData.id)
      .single();
    
    if (existingProgress) {
      // Update existing progress
      console.log('Updating existing progress...');
      const { data: updated, error: updateError } = await supabase
        .from('user_progress')
        .update({
          status,
          rating,
          last_accessed: new Date().toISOString(),
          updated_at: new Date().toISOString()
        })
        .eq('id', existingProgress.id)
        .select()
        .single();
      
      if (updateError) {
        console.error('Error updating progress:', updateError);
      } else {
        console.log('✅ Successfully updated progress:', updated);
      }
    } else {
      // Insert new progress
      console.log('Creating new progress record...');
      const { data: inserted, error: insertError } = await supabase
        .from('user_progress')
        .insert({
          user_id: userId,
          skill_id: nodeData.id,
          status,
          rating,
          last_accessed: new Date().toISOString(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        })
        .select()
        .single();
      
      if (insertError) {
        console.error('Error inserting progress:', insertError);
      } else {
        console.log('✅ Successfully added progress:', inserted);
      }
    }
    
    // Verify all user progress
    console.log('\nFetching all user progress...');
    const { data: allProgress, error: allError } = await supabase
      .from('user_progress')
      .select(`
        *,
        skill_tree_nodes!inner(
          name,
          learning_area
        )
      `)
      .eq('user_id', userId)
      .order('last_accessed', { ascending: false });
    
    if (allError) {
      console.error('Error fetching progress:', allError);
    } else {
      console.log(`\nUser has ${allProgress.length} progress records:`);
      allProgress.forEach(p => {
        console.log(`  - ${p.skill_tree_nodes.name}: ${p.status} (Last accessed: ${new Date(p.last_accessed).toLocaleDateString()})`);
      });
    }
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

// Usage: node scripts/add_user_progress.js <email> <node_name> [status] [rating]
const args = process.argv.slice(2);
if (args.length < 2) {
  console.log('Usage: node scripts/add_user_progress.js <email> <node_name> [status] [rating]');
  console.log('Example: node scripts/add_user_progress.js user@example.com "Money Counting" in_progress 0');
  console.log('Status options: not_started, in_progress, completed');
  process.exit(1);
}

const [email, nodeName, status = 'in_progress', rating = '0'] = args;
addUserProgress(email, nodeName, status, parseInt(rating));