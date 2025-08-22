const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function makeUserAdmin(email) {
  try {
    console.log(`Making user with email "${email}" an admin...`);
    
    // First, find the user by email
    const { data: user, error: userError } = await supabase.auth.admin.listUsers();
    
    if (userError) {
      console.error('Error fetching users:', userError);
      return;
    }
    
    const targetUser = user.users.find(u => u.email === email);
    
    if (!targetUser) {
      console.error(`User with email "${email}" not found`);
      return;
    }
    
    console.log(`Found user: ${targetUser.id}`);
    
    // Update the user's profile to set is_admin = true
    const { data, error } = await supabase
      .from('profiles')
      .upsert({
        id: targetUser.id,
        email: targetUser.email,
        is_admin: true,
        updated_at: new Date().toISOString()
      }, {
        onConflict: 'id'
      });
    
    if (error) {
      console.error('Error updating profile:', error);
      return;
    }
    
    console.log(`✅ Successfully made ${email} an admin user`);
    
    // Verify the change
    const { data: profile, error: verifyError } = await supabase
      .from('profiles')
      .select('id, email, is_admin')
      .eq('id', targetUser.id)
      .single();
    
    if (verifyError) {
      console.error('Error verifying admin status:', verifyError);
    } else {
      console.log('Verified profile:', profile);
    }
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

// Usage: node make_user_admin.js user@example.com
const email = process.argv[2];

if (!email) {
  console.log('Usage: node make_user_admin.js <email>');
  console.log('Example: node make_user_admin.js admin@example.com');
  process.exit(1);
}

makeUserAdmin(email);