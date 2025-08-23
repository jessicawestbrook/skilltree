const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

// Test with different keys
const supabaseAnon = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

const supabaseService = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
)

async function testDirectAuth() {
  console.log('Testing direct auth operations...\n')
  console.log('=' .repeat(50))
  
  const testEmail = 'test_' + Date.now() + '@example.com'
  const jessicaEmail = 'jessicawestbrook88@gmail.com'
  
  try {
    // 1. Test with a completely new email
    console.log('\n1. Testing signup with new test email:', testEmail)
    const { data: testData, error: testError } = await supabaseAnon.auth.signUp({
      email: testEmail,
      password: 'TestPassword123!'
    })
    
    if (testError) {
      console.log('❌ Test email signup failed:', testError.message)
      console.log('Error code:', testError.code)
      console.log('Status:', testError.status)
    } else {
      console.log('✅ Test email signup succeeded!')
      console.log('User ID:', testData.user?.id)
      
      // Clean up test user
      if (testData.user?.id) {
        const { error: deleteError } = await supabaseService.auth.admin.deleteUser(
          testData.user.id
        )
        if (!deleteError) {
          console.log('✅ Test user cleaned up')
        }
      }
    }
    
    // 2. Test with Jessica's email
    console.log('\n2. Testing signup with Jessica\'s email:', jessicaEmail)
    const { data: jessicaData, error: jessicaError } = await supabaseAnon.auth.signUp({
      email: jessicaEmail,
      password: 'TestPassword123!'
    })
    
    if (jessicaError) {
      console.log('❌ Jessica signup failed:', jessicaError.message)
      console.log('Error code:', jessicaError.code)
      console.log('Status:', jessicaError.status)
      console.log('Full error:', jessicaError)
    } else {
      console.log('✅ Jessica signup succeeded!')
      console.log('User ID:', jessicaData.user?.id)
      console.log('Email:', jessicaData.user?.email)
    }
    
    // 3. Check if it's a specific email issue
    console.log('\n3. Testing with different Gmail account...')
    const altEmail = 'test_gmail_' + Date.now() + '@gmail.com'
    const { data: altData, error: altError } = await supabaseAnon.auth.signUp({
      email: altEmail,
      password: 'TestPassword123!'
    })
    
    if (altError) {
      console.log('❌ Alternative Gmail failed:', altError.message)
      console.log('This suggests Gmail might be blocked or rate limited')
    } else {
      console.log('✅ Alternative Gmail succeeded')
      // Clean up
      if (altData.user?.id) {
        await supabaseService.auth.admin.deleteUser(altData.user.id)
      }
    }
    
    // 4. Check project settings
    console.log('\n4. Checking auth settings...')
    const { data: settings, error: settingsError } = await supabaseService
      .from('auth.config')
      .select('*')
    
    if (settingsError) {
      console.log('Cannot access auth.config directly')
    } else {
      console.log('Auth settings:', settings)
    }
    
    // 5. Try to create user directly with admin API
    console.log('\n5. Trying admin user creation for Jessica...')
    const { data: adminData, error: adminError } = await supabaseService.auth.admin.createUser({
      email: jessicaEmail,
      password: 'TestPassword123!',
      email_confirm: true
    })
    
    if (adminError) {
      console.log('❌ Admin creation failed:', adminError.message)
      console.log('This means the email is truly blocked somehow')
    } else {
      console.log('✅ Admin creation succeeded!')
      console.log('User ID:', adminData.user?.id)
      console.log('This means regular signup has an issue but admin API works')
    }
    
  } catch (error) {
    console.error('Unexpected error:', error)
  }
  
  console.log('\n' + '=' .repeat(50))
  console.log('\n📊 DIAGNOSIS:')
  console.log('If test emails work but Jessica\'s doesn\'t, the issue is specific to that email.')
  console.log('If no emails work, there\'s a general auth configuration issue.')
  console.log('\nCheck the Supabase dashboard:')
  console.log('1. Authentication > Settings > Email Auth - Make sure it\'s enabled')
  console.log('2. Authentication > Settings > User Signups - Make sure it\'s enabled')
  console.log('3. Project Settings > API > Check rate limiting settings')
}

testDirectAuth()