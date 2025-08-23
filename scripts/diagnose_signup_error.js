const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function diagnoseSignupError() {
  console.log('Diagnosing signup error for jessicawestbrook88@gmail.com\n')
  console.log('=' .repeat(50))
  
  try {
    // 1. Verify user doesn't exist in auth.users
    console.log('\n1. Checking if user exists in auth.users...')
    console.log('Note: We cannot directly query auth.users from client')
    console.log('Please check manually at:')
    console.log('https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/auth/users')
    
    // 2. Check if email exists in profiles
    console.log('\n2. Checking profiles table for email...')
    const { data: profileByEmail, error: emailError } = await supabase
      .from('profiles')
      .select('*')
      .eq('email', 'jessicawestbrook88@gmail.com')
    
    if (profileByEmail && profileByEmail.length > 0) {
      console.log('❌ Found profile with this email:', profileByEmail)
      console.log('This could be blocking signup!')
    } else {
      console.log('✅ No profile with this email')
    }
    
    // 3. Check for orphaned profiles (profiles without auth.users)
    console.log('\n3. Checking for orphaned profiles...')
    const { data: allProfiles, error: profilesError } = await supabase
      .from('profiles')
      .select('id, email, username')
      .limit(100)
    
    if (allProfiles) {
      console.log(`Found ${allProfiles.length} profiles`)
      const jessicaProfiles = allProfiles.filter(p => 
        p.email && p.email.toLowerCase().includes('jessica')
      )
      if (jessicaProfiles.length > 0) {
        console.log('Found profiles with "jessica" in email:', jessicaProfiles)
      }
    }
    
    // 4. Check database triggers
    console.log('\n4. Checking for database triggers...')
    console.log('Run this SQL in Supabase to check triggers:')
    console.log(`
SELECT 
  trigger_name,
  event_manipulation,
  event_object_table,
  action_statement
FROM information_schema.triggers 
WHERE trigger_schema = 'public' OR event_object_schema = 'auth';
`)
    
    // 5. Provide cleanup SQL
    console.log('\n' + '=' .repeat(50))
    console.log('\n🔧 CLEANUP SQL - Run this in Supabase SQL Editor:\n')
    console.log(`
-- 1. Remove any orphaned profile with this email
DELETE FROM profiles 
WHERE email = 'jessicawestbrook88@gmail.com';

-- 2. Check and fix the trigger function
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  -- Only insert if profile doesn't exist
  INSERT INTO public.profiles (id, email, created_at, updated_at)
  VALUES (
    new.id, 
    new.email,
    NOW(),
    NOW()
  )
  ON CONFLICT (id) DO UPDATE
  SET 
    email = EXCLUDED.email,
    updated_at = NOW();
  
  RETURN new;
EXCEPTION
  WHEN unique_violation THEN
    -- If there's a unique constraint violation, just return
    RETURN new;
  WHEN OTHERS THEN
    -- Log other errors but don't fail the signup
    RAISE WARNING 'Error in handle_new_user: %', SQLERRM;
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 3. Recreate the trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW 
  EXECUTE FUNCTION public.handle_new_user();

-- 4. Check constraints on profiles table
SELECT 
  constraint_name,
  constraint_type,
  table_name
FROM information_schema.table_constraints
WHERE table_name = 'profiles';

-- 5. Make sure email column allows NULL or has proper constraints
ALTER TABLE profiles 
ALTER COLUMN email DROP NOT NULL;

-- 6. Add IF NOT EXISTS to unique constraint
ALTER TABLE profiles 
DROP CONSTRAINT IF EXISTS profiles_email_key;

ALTER TABLE profiles 
ADD CONSTRAINT profiles_email_key UNIQUE (email);
`)
    
    console.log('\n' + '=' .repeat(50))
    console.log('\n📋 Steps to fix:')
    console.log('1. Run the cleanup SQL above in Supabase SQL Editor')
    console.log('2. Try signing up again')
    console.log('3. If it still fails, check the Supabase logs:')
    console.log('   https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/logs/edge-logs')
    
    // 6. Test creating a profile directly
    console.log('\n5. Testing direct profile creation...')
    const testId = 'test-' + Date.now()
    const { data: testProfile, error: testError } = await supabase
      .from('profiles')
      .insert({
        id: '00000000-0000-0000-0000-000000000000',
        email: `test${testId}@example.com`
      })
      .select()
    
    if (testError) {
      console.log('❌ Cannot create test profile:', testError.message)
      console.log('This indicates a table/permission issue')
    } else {
      console.log('✅ Can create profiles directly')
      // Clean up test
      await supabase
        .from('profiles')
        .delete()
        .eq('email', `test${testId}@example.com`)
    }
    
  } catch (error) {
    console.error('Error:', error)
  }
}

diagnoseSignupError()