const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function checkProfilesStructure() {
  console.log('Checking profiles table structure and data...\n')
  console.log('=' .repeat(50))
  
  try {
    // 1. Try to fetch a sample profile
    console.log('\n1. Fetching sample profile...')
    const { data: sampleProfile, error: sampleError } = await supabase
      .from('profiles')
      .select('*')
      .limit(1)
    
    if (sampleError) {
      console.log('❌ Error fetching profiles:', sampleError.message)
    } else if (sampleProfile && sampleProfile.length > 0) {
      console.log('✅ Sample profile structure:')
      const columns = Object.keys(sampleProfile[0])
      console.log('Columns:', columns)
      console.log('\nSample data:')
      console.log(JSON.stringify(sampleProfile[0], null, 2))
    } else {
      console.log('⚠️  No profiles found in table')
    }
    
    // 2. Test username query specifically
    console.log('\n2. Testing username query...')
    const { data: usernameTest, error: usernameError } = await supabase
      .from('profiles')
      .select('username')
      .eq('username', 'testuser123')
    
    if (usernameError) {
      console.log('❌ Username query error:', usernameError.message)
      console.log('Error code:', usernameError.code)
      console.log('Error details:', usernameError.details)
      console.log('Error hint:', usernameError.hint)
    } else {
      console.log('✅ Username query works')
      console.log('Results:', usernameTest)
    }
    
    // 3. Test if username column exists
    console.log('\n3. Testing if username column exists...')
    const { data: allColumns, error: columnsError } = await supabase
      .from('profiles')
      .select('*')
      .limit(0)
    
    if (!columnsError) {
      console.log('✅ Table accessible')
    } else {
      console.log('❌ Cannot access table:', columnsError.message)
    }
    
    // 4. Try different column queries
    console.log('\n4. Testing different column queries...')
    
    // Test email column
    const { data: emailTest, error: emailError } = await supabase
      .from('profiles')
      .select('email')
      .limit(1)
    
    if (emailError) {
      console.log('❌ Email column query failed:', emailError.message)
    } else {
      console.log('✅ Email column query works')
    }
    
    // Test id column
    const { data: idTest, error: idError } = await supabase
      .from('profiles')
      .select('id')
      .limit(1)
    
    if (idError) {
      console.log('❌ ID column query failed:', idError.message)
    } else {
      console.log('✅ ID column query works')
    }
    
    // 5. Check for any Jessica profiles
    console.log('\n5. Checking for Jessica profiles...')
    const { data: jessicaProfiles, error: jessicaError } = await supabase
      .from('profiles')
      .select('*')
      .ilike('email', '%jessica%')
    
    if (jessicaError) {
      console.log('❌ Jessica search error:', jessicaError.message)
    } else {
      console.log(`Found ${jessicaProfiles?.length || 0} Jessica profiles`)
      if (jessicaProfiles && jessicaProfiles.length > 0) {
        jessicaProfiles.forEach(p => {
          console.log(`- ID: ${p.id}, Email: ${p.email}, Username: ${p.username}`)
        })
      }
    }
    
    // 6. Provide SQL to check/fix table structure
    console.log('\n' + '=' .repeat(50))
    console.log('\n📝 SQL to check table structure in Supabase:')
    console.log(`
-- Check columns in profiles table
SELECT 
  column_name, 
  data_type, 
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'profiles'
ORDER BY ordinal_position;

-- Check if username column exists
SELECT EXISTS (
  SELECT 1 
  FROM information_schema.columns 
  WHERE table_schema = 'public' 
    AND table_name = 'profiles' 
    AND column_name = 'username'
) as username_exists;

-- If username column doesn't exist, add it:
ALTER TABLE profiles 
ADD COLUMN IF NOT EXISTS username TEXT UNIQUE;
`)
    
  } catch (error) {
    console.error('Unexpected error:', error)
  }
}

checkProfilesStructure()