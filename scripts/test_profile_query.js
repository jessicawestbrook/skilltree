const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

// Test with both keys
const supabaseAnon = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

const supabaseService = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function testProfileQuery() {
  console.log('Testing profile query...\n')
  console.log('=' .repeat(50))
  
  const userId = '5876bd4e-5e68-4b4d-be15-8f0171bfae93'
  
  try {
    // 1. Test with anon key (what the app uses)
    console.log('\n1. Testing with ANON key (app uses this)...')
    const { data: anonData, error: anonError } = await supabaseAnon
      .from('profiles')
      .select('is_admin')
      .eq('id', userId)
      .single()
    
    if (anonError) {
      console.log('❌ Anon key query failed:', anonError.message)
      console.log('   Error code:', anonError.code)
      console.log('   Details:', anonError.details)
    } else {
      console.log('✅ Anon key query succeeded:')
      console.log('   is_admin:', anonData.is_admin)
    }
    
    // 2. Test with service key
    console.log('\n2. Testing with SERVICE key...')
    const { data: serviceData, error: serviceError } = await supabaseService
      .from('profiles')
      .select('is_admin')
      .eq('id', userId)
      .single()
    
    if (serviceError) {
      console.log('❌ Service key query failed:', serviceError.message)
      console.log('   Error code:', serviceError.code)
    } else {
      console.log('✅ Service key query succeeded:')
      console.log('   is_admin:', serviceData.is_admin)
    }
    
    // 3. Test full profile fetch
    console.log('\n3. Testing full profile fetch...')
    const { data: fullProfile, error: fullError } = await supabaseService
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single()
    
    if (fullError) {
      console.log('❌ Full profile fetch failed:', fullError.message)
    } else {
      console.log('✅ Full profile data:')
      Object.entries(fullProfile).forEach(([key, value]) => {
        console.log(`   ${key}: ${value}`)
      })
    }
    
    // 4. Check RLS policies
    console.log('\n4. Checking if RLS might be blocking...')
    console.log('If anon key fails but service key works, it\'s an RLS issue.')
    console.log('If both fail, it\'s a different problem.')
    
  } catch (error) {
    console.error('Unexpected error:', error)
  }
  
  console.log('\n' + '=' .repeat(50))
  console.log('\n📝 DIAGNOSIS:')
  if (anonError && !serviceError) {
    console.log('RLS policies are blocking the query. Need to fix policies.')
  } else if (anonError && serviceError) {
    console.log('Database query issue. Check table structure.')
  } else {
    console.log('Queries work fine. Issue might be in the React app.')
  }
}

testProfileQuery()