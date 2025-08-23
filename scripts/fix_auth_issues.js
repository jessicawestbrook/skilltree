const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function fixAuthIssues() {
  console.log('Diagnosing and fixing authentication issues\n')
  console.log('=' .repeat(50))
  
  try {
    // 1. Check profiles table structure
    console.log('\n1. Checking profiles table structure...')
    const { data: profileSample, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .limit(1)
    
    if (profileError) {
      console.log('❌ Error accessing profiles table:', profileError.message)
      
      // Check if table exists
      const { data: tables } = await supabase
        .from('information_schema.tables')
        .select('table_name')
        .eq('table_schema', 'public')
        .eq('table_name', 'profiles')
      
      if (!tables || tables.length === 0) {
        console.log('❌ Profiles table does not exist!')
        console.log('\nCreating profiles table...')
        // SQL to create profiles table would go here
      }
    } else {
      console.log('✅ Profiles table exists')
      if (profileSample && profileSample.length > 0) {
        const columns = Object.keys(profileSample[0])
        console.log('Columns:', columns)
        
        // Check for required columns
        const requiredColumns = ['id', 'email', 'username']
        const missingColumns = requiredColumns.filter(col => !columns.includes(col))
        
        if (missingColumns.length > 0) {
          console.log('⚠️  Missing columns:', missingColumns)
        }
      }
    }
    
    // 2. Test username query
    console.log('\n2. Testing username query...')
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('username')
        .eq('username', 'testuser123456')
      
      if (error) {
        console.log('❌ Username query failed:', error.message)
        console.log('This might be a column issue or RLS policy issue')
      } else {
        console.log('✅ Username query works')
      }
    } catch (err) {
      console.log('❌ Username query error:', err)
    }
    
    // 3. Check for the specific user
    console.log('\n3. Checking for jessicawestbrook88@gmail.com...')
    const { data: existingProfile } = await supabase
      .from('profiles')
      .select('*')
      .eq('email', 'jessicawestbrook88@gmail.com')
      .single()
    
    if (existingProfile) {
      console.log('✅ Profile exists:', existingProfile)
    } else {
      console.log('❌ No profile found for this email')
    }
    
    // 4. Provide SQL to fix issues
    console.log('\n' + '=' .repeat(50))
    console.log('\n📝 SQL to run in Supabase to fix issues:\n')
    
    console.log('-- 1. Ensure profiles table has correct structure')
    console.log(`
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create trigger to auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email)
  VALUES (new.id, new.email)
  ON CONFLICT (id) DO UPDATE
  SET email = EXCLUDED.email,
      updated_at = NOW();
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Create trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 3. Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- 4. Create RLS policies
DROP POLICY IF EXISTS "Public profiles are viewable by everyone" ON profiles;
CREATE POLICY "Public profiles are viewable by everyone"
  ON profiles FOR SELECT
  USING (true);

DROP POLICY IF EXISTS "Users can update own profile" ON profiles;  
CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- 5. Grant permissions
GRANT ALL ON profiles TO postgres, anon, authenticated, service_role;

-- 6. If user exists in auth but not profiles, create profile
DO $$
DECLARE
  user_record RECORD;
BEGIN
  FOR user_record IN 
    SELECT id, email FROM auth.users 
    WHERE email = 'jessicawestbrook88@gmail.com'
  LOOP
    INSERT INTO profiles (id, email)
    VALUES (user_record.id, user_record.email)
    ON CONFLICT (id) DO NOTHING;
  END LOOP;
END $$;
`)
    
    console.log('\n' + '=' .repeat(50))
    console.log('\n🔧 Instructions:')
    console.log('1. Go to: https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/sql/new')
    console.log('2. Copy and paste the SQL above')
    console.log('3. Click "Run"')
    console.log('4. Try signing up again')
    
    console.log('\n🗑️  If you need to completely remove the user to start fresh:')
    console.log('1. Go to: https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/auth/users')
    console.log('2. Search for: jessicawestbrook88@gmail.com')
    console.log('3. Click on the user')
    console.log('4. Click "Delete user"')
    console.log('5. Try signing up again')
    
  } catch (error) {
    console.error('Error:', error)
  }
}

fixAuthIssues()