const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function debugAdminAccess() {
  console.log('Debugging admin access issue...\n')
  console.log('=' .repeat(50))
  
  const userId = '5876bd4e-5e68-4b4d-be15-8f0171bfae93'
  
  try {
    // 1. Check if user exists in auth.users
    console.log('\n1. Checking auth.users table...')
    const { data: { users }, error: usersError } = await supabase.auth.admin.listUsers()
    
    if (usersError) {
      console.log('❌ Error listing users:', usersError.message)
    } else {
      const targetUser = users.find(u => u.id === userId)
      if (targetUser) {
        console.log('✅ User found in auth.users:')
        console.log('   - ID:', targetUser.id)
        console.log('   - Email:', targetUser.email)
        console.log('   - Created:', targetUser.created_at)
      } else {
        console.log('❌ User NOT found in auth.users')
        console.log('Available users:')
        users.forEach(u => {
          console.log(`   - ${u.id}: ${u.email}`)
        })
      }
    }
    
    // 2. Check if profile exists
    console.log('\n2. Checking profiles table...')
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single()
    
    if (profileError) {
      if (profileError.code === 'PGRST116') {
        console.log('❌ No profile found for this user ID')
      } else {
        console.log('❌ Error fetching profile:', profileError.message)
      }
    } else {
      console.log('✅ Profile found:')
      console.log('   - ID:', profile.id)
      console.log('   - Email:', profile.email)
      console.log('   - Username:', profile.username)
      console.log('   - Is Admin:', profile.is_admin)
    }
    
    // 3. Check all profiles
    console.log('\n3. Checking all profiles...')
    const { data: allProfiles, error: allProfilesError } = await supabase
      .from('profiles')
      .select('id, email, username, is_admin')
      .order('created_at', { ascending: false })
      .limit(10)
    
    if (allProfilesError) {
      console.log('❌ Error fetching profiles:', allProfilesError.message)
    } else {
      console.log(`Found ${allProfiles.length} profiles:`)
      allProfiles.forEach(p => {
        const marker = p.id === userId ? ' <-- THIS USER' : ''
        console.log(`   - ${p.id}: ${p.email} (admin: ${p.is_admin})${marker}`)
      })
    }
    
    // 4. Provide SQL to fix
    console.log('\n' + '=' .repeat(50))
    console.log('\n📝 SQL TO FIX THE ISSUE:')
    console.log('\nRun this in Supabase SQL Editor:')
    console.log(`
-- Create profile for the logged-in user
INSERT INTO public.profiles (
  id,
  email,
  username,
  is_admin,
  created_at,
  updated_at
)
SELECT 
  id,
  email,
  COALESCE(raw_user_meta_data->>'username', split_part(email, '@', 1)) as username,
  true as is_admin,
  NOW() as created_at,
  NOW() as updated_at
FROM auth.users
WHERE id = '${userId}'
ON CONFLICT (id) DO UPDATE
SET 
  is_admin = true,
  updated_at = NOW();

-- Verify it worked
SELECT * FROM public.profiles WHERE id = '${userId}';
`)
    
  } catch (error) {
    console.error('Unexpected error:', error)
  }
}

debugAdminAccess()