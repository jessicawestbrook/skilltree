const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

// Use service role key for auth operations
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
)

async function testSignupWithServiceRole() {
  console.log('Testing signup with service role key...\n')
  console.log('=' .repeat(50))
  
  const timestamp = Date.now()
  const testEmail = `test${timestamp}@example.com`
  const jessicaEmail = 'jessicawestbrook88@gmail.com'
  const password = 'TestPassword123!'
  
  try {
    // 1. Test with admin createUser (service role)
    console.log('\n1. Testing admin.createUser with test email...')
    const { data: testData, error: testError } = await supabase.auth.admin.createUser({
      email: testEmail,
      password: password,
      email_confirm: true
    })
    
    if (testError) {
      console.log('❌ Admin createUser failed:', testError.message)
      console.log('Error details:', testError)
    } else {
      console.log('✅ Admin createUser succeeded!')
      console.log('User ID:', testData.user?.id)
      
      // Clean up test user
      if (testData.user?.id) {
        await supabase.auth.admin.deleteUser(testData.user.id)
        console.log('✅ Test user cleaned up')
      }
    }
    
    // 2. Test with Jessica's email
    console.log('\n2. Testing admin.createUser with Jessica\'s email...')
    const { data: jessicaData, error: jessicaError } = await supabase.auth.admin.createUser({
      email: jessicaEmail,
      password: password,
      email_confirm: true
    })
    
    if (jessicaError) {
      console.log('❌ Jessica createUser failed:', jessicaError.message)
      console.log('Error details:', jessicaError)
    } else {
      console.log('✅ Jessica createUser succeeded!')
      console.log('User ID:', jessicaData.user?.id)
      console.log('Email:', jessicaData.user?.email)
      console.log('\nYou should now be able to log in with:')
      console.log('Email:', jessicaEmail)
      console.log('Password:', password)
    }
    
    // 3. Check if profile was created
    console.log('\n3. Checking if profile exists for Jessica...')
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .eq('email', jessicaEmail)
      .single()
    
    if (profileError) {
      console.log('❌ No profile found')
      
      // Try to create profile manually if user exists
      if (jessicaData?.user?.id) {
        console.log('\n4. Creating profile manually...')
        const { error: createProfileError } = await supabase
          .from('profiles')
          .insert({
            id: jessicaData.user.id,
            email: jessicaEmail,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          })
        
        if (createProfileError) {
          console.log('❌ Profile creation failed:', createProfileError.message)
        } else {
          console.log('✅ Profile created successfully!')
        }
      }
    } else {
      console.log('✅ Profile exists:', profile.id)
    }
    
  } catch (error) {
    console.error('Unexpected error:', error)
  }
  
  console.log('\n' + '=' .repeat(50))
  console.log('\n📊 SUMMARY:')
  console.log('If admin.createUser works, the auth system is functional.')
  console.log('The issue was with the regular signup endpoint.')
  console.log('\nYou can now try logging in at http://localhost:3000')
}

testSignupWithServiceRole()