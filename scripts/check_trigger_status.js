const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function checkTriggerStatus() {
  console.log('Checking trigger and auth status...\n')
  console.log('=' .repeat(50))
  
  try {
    // 1. Check if we can query profiles at all
    console.log('\n1. Testing basic profiles query...')
    const { data: profiles, error: profilesError } = await supabase
      .from('profiles')
      .select('id, email')
      .limit(1)
    
    if (profilesError) {
      console.log('❌ Cannot query profiles:', profilesError.message)
    } else {
      console.log('✅ Profiles table accessible')
    }
    
    // 2. Check for Jessica profile
    console.log('\n2. Checking for Jessica profile...')
    const { data: jessicaProfile, error: jessicaError } = await supabase
      .from('profiles')
      .select('*')
      .eq('email', 'jessicawestbrook88@gmail.com')
    
    if (jessicaError) {
      console.log('❌ Error checking for Jessica:', jessicaError.message)
    } else if (jessicaProfile && jessicaProfile.length > 0) {
      console.log('⚠️  Found existing Jessica profile:')
      console.log(JSON.stringify(jessicaProfile[0], null, 2))
      console.log('\nThis might be blocking signup!')
    } else {
      console.log('✅ No Jessica profile found')
    }
    
    // 3. List all auth users (using service role)
    console.log('\n3. Checking auth.users for Jessica...')
    const { data: { users }, error: usersError } = await supabase.auth.admin.listUsers({
      page: 1,
      perPage: 1000
    })
    
    if (usersError) {
      console.log('❌ Cannot list auth users:', usersError.message)
    } else {
      const jessicaUsers = users.filter(u => u.email === 'jessicawestbrook88@gmail.com')
      if (jessicaUsers.length > 0) {
        console.log('⚠️  Found Jessica in auth.users:')
        jessicaUsers.forEach(u => {
          console.log(`- ID: ${u.id}`)
          console.log(`- Email: ${u.email}`)
          console.log(`- Created: ${u.created_at}`)
          console.log(`- Confirmed: ${u.confirmed_at}`)
        })
      } else {
        console.log('✅ No Jessica in auth.users')
      }
    }
    
    // 4. Provide SQL to check trigger directly
    console.log('\n' + '=' .repeat(50))
    console.log('\n📝 Run this SQL in Supabase to check trigger status:')
    console.log(`
-- Check if trigger exists
SELECT 
  t.tgname as trigger_name,
  p.proname as function_name,
  t.tgenabled as enabled
FROM pg_trigger t
JOIN pg_class c ON t.tgrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
JOIN pg_proc p ON t.tgfoid = p.oid
WHERE n.nspname = 'auth' 
  AND c.relname = 'users'
  AND t.tgname = 'on_auth_user_created';

-- Check recent errors in logs
SELECT * FROM pg_stat_activity WHERE state = 'idle in transaction (aborted)';

-- Test the trigger function manually
SELECT public.handle_new_user();
`)
    
    console.log('\n' + '=' .repeat(50))
    console.log('\n🔍 DIAGNOSIS:')
    
    // 5. Try to delete Jessica from auth if she exists
    if (jessicaUsers && jessicaUsers.length > 0) {
      console.log('\n⚠️  Jessica exists in auth.users!')
      console.log('To fix, run this in Supabase SQL Editor:')
      console.log(`
-- Delete Jessica from auth.users
DELETE FROM auth.users WHERE email = 'jessicawestbrook88@gmail.com';

-- Also delete from profiles just in case
DELETE FROM public.profiles WHERE email = 'jessicawestbrook88@gmail.com';
`)
    } else if (jessicaProfile && jessicaProfile.length > 0) {
      console.log('\n⚠️  Orphaned Jessica profile exists!')
      console.log('To fix, run this in Supabase SQL Editor:')
      console.log(`
-- Delete orphaned profile
DELETE FROM public.profiles WHERE email = 'jessicawestbrook88@gmail.com';
`)
    } else {
      console.log('\n✅ No conflicting data found')
      console.log('The issue might be with the trigger itself.')
      console.log('Check the Edge Logs in Supabase dashboard for the actual error.')
    }
    
  } catch (error) {
    console.error('Unexpected error:', error)
  }
}

checkTriggerStatus()