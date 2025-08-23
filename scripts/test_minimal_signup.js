const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function testMinimalSignup() {
  console.log('Testing minimal signup...\n')
  console.log('=' .repeat(50))
  
  // Use a timestamp to ensure unique email
  const timestamp = Date.now()
  const email = `test${timestamp}@example.com`
  const password = 'TestPass123!'
  
  console.log('Attempting signup with:')
  console.log('Email:', email)
  console.log('Password:', password)
  console.log('')
  
  try {
    // Try the absolute minimal signup
    const { data, error } = await supabase.auth.signUp({
      email: email,
      password: password
    })
    
    if (error) {
      console.log('❌ Signup failed')
      console.log('Error message:', error.message)
      console.log('Error status:', error.status)
      console.log('Error code:', error.code)
      
      // Try to get more details
      if (error.status === 500) {
        console.log('\n500 Internal Server Error indicates a server-side issue.')
        console.log('This is likely a Supabase configuration problem.')
        console.log('\nPossible causes:')
        console.log('1. Email provider is disabled in Supabase Dashboard')
        console.log('2. SMTP settings are not configured (if email confirmations are required)')
        console.log('3. Auth service is having issues')
      }
    } else {
      console.log('✅ Signup succeeded!')
      console.log('User ID:', data.user?.id)
      console.log('User email:', data.user?.email)
      
      if (data.session) {
        console.log('Session created:', data.session.access_token ? 'Yes' : 'No')
      }
      
      if (!data.user?.confirmed_at) {
        console.log('Note: Email confirmation is required')
      }
    }
    
  } catch (err) {
    console.error('Unexpected error:', err)
  }
  
  console.log('\n' + '=' .repeat(50))
  console.log('\nIMPORTANT: Check these in Supabase Dashboard:')
  console.log('1. Authentication → Providers → Email (must be ENABLED)')
  console.log('2. If using email confirmations, SMTP must be configured')
  console.log('3. Check Edge Functions logs for any errors')
  console.log('\nDashboard URL:')
  console.log('https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/auth/providers')
}

testMinimalSignup()