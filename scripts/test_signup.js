const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY // Use anon key for auth operations
)

async function testSignup() {
  console.log('Testing signup for jessicawestbrook88@gmail.com\n')
  console.log('=' .repeat(50))
  
  const email = 'jessicawestbrook88@gmail.com'
  const password = 'TestPassword123!' // You can change this
  
  try {
    // First, try to sign up
    console.log('\n1. Attempting signup...')
    const { data: signUpData, error: signUpError } = await supabase.auth.signUp({
      email: email,
      password: password,
      options: {
        data: {
          username: 'jessicawestbrook88'
        }
      }
    })
    
    if (signUpError) {
      console.log('❌ Signup failed:', signUpError.message)
      console.log('Full error:', signUpError)
      
      // If signup failed, try to sign in (user might already exist)
      console.log('\n2. Attempting sign in instead...')
      const { data: signInData, error: signInError } = await supabase.auth.signIn({
        email: email,
        password: password
      })
      
      if (signInError) {
        console.log('❌ Sign in also failed:', signInError.message)
      } else {
        console.log('✅ Sign in successful!')
        console.log('User:', signInData.user?.email)
      }
    } else {
      console.log('✅ Signup successful!')
      console.log('User ID:', signUpData.user?.id)
      console.log('Email:', signUpData.user?.email)
      
      // Check if confirmation email is required
      if (signUpData.user?.confirmed_at === null) {
        console.log('📧 Please check your email for confirmation link')
      }
      
      // Check if profile was created
      console.log('\n3. Checking if profile was created...')
      const { data: profile, error: profileError } = await supabase
        .from('profiles')
        .select('*')
        .eq('email', email)
        .single()
      
      if (profileError) {
        console.log('❌ Profile not found:', profileError.message)
      } else {
        console.log('✅ Profile created successfully!')
        console.log('Profile ID:', profile.id)
        console.log('Profile email:', profile.email)
      }
    }
    
    // Additional diagnostics
    console.log('\n' + '=' .repeat(50))
    console.log('\n📊 Diagnostics:')
    
    // Check current session
    const { data: { session } } = await supabase.auth.getSession()
    if (session) {
      console.log('✅ Active session found')
      console.log('Session user:', session.user.email)
    } else {
      console.log('❌ No active session')
    }
    
  } catch (error) {
    console.error('Unexpected error:', error)
  }
  
  console.log('\n' + '=' .repeat(50))
  console.log('\n📝 Next steps:')
  console.log('1. If signup failed with "Database error", run comprehensive_signup_fix.sql in Supabase')
  console.log('2. If signup succeeded but profile wasn\'t created, check the trigger in Supabase')
  console.log('3. If you need to reset, delete the user from Supabase Auth dashboard and try again')
}

// Run the test
testSignup()