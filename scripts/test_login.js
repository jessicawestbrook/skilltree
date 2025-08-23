const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function testLogin() {
  console.log('Testing login functionality...\n')
  console.log('=' .repeat(50))
  
  const email = 'jessicawestbrook88@gmail.com'
  const password = 'TestPassword123!'
  
  console.log('Attempting to sign in with:')
  console.log('Email:', email)
  console.log('Password:', password)
  console.log('')
  
  try {
    // Try to sign in
    const { data, error } = await supabase.auth.signInWithPassword({
      email: email,
      password: password
    })
    
    if (error) {
      console.log('❌ Sign in failed')
      console.log('Error message:', error.message)
      console.log('Error code:', error.code)
      console.log('Error status:', error.status)
      
      if (error.message.includes('Database error querying schema')) {
        console.log('\n⚠️  This error indicates a serious Auth service issue.')
        console.log('The Auth service cannot query the database schema.')
        console.log('\nPossible causes:')
        console.log('1. Auth service needs to be restarted')
        console.log('2. Database permissions issue')
        console.log('3. Supabase project issue')
      }
    } else {
      console.log('✅ Sign in successful!')
      console.log('User ID:', data.user?.id)
      console.log('User email:', data.user?.email)
      console.log('Session:', data.session ? 'Created' : 'Not created')
      
      // Check profile
      if (data.user?.id) {
        const { data: profile, error: profileError } = await supabase
          .from('profiles')
          .select('*')
          .eq('id', data.user.id)
          .single()
        
        if (profile) {
          console.log('\nProfile data:')
          console.log('Username:', profile.username)
          console.log('Email:', profile.email)
        }
      }
    }
    
  } catch (err) {
    console.error('Unexpected error:', err)
  }
  
  console.log('\n' + '=' .repeat(50))
  console.log('\n🔧 TROUBLESHOOTING:')
  console.log('\n1. Try restarting your Supabase project:')
  console.log('   - Go to: https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/settings/general')
  console.log('   - Look for "Restart project" or "Pause/Resume" options')
  console.log('\n2. Check Auth logs:')
  console.log('   - Go to: https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/logs/edge-logs')
  console.log('   - Look for recent errors')
  console.log('\n3. Contact Supabase support:')
  console.log('   - The Auth service appears to be broken')
  console.log('   - Direct SQL works but Auth API fails')
}

testLogin()