const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY // Using service role to check auth.users
)

async function checkUserAuth() {
  const email = 'jessicawestbrook88@gmail.com'
  
  console.log(`Checking authentication status for: ${email}\n`)
  console.log('=' .repeat(50))
  
  try {
    // Check if user exists in profiles table
    console.log('\n1. Checking profiles table:')
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .eq('email', email)
      .single()
    
    if (profileError) {
      if (profileError.code === 'PGRST116') {
        console.log('❌ No profile found with this email')
      } else {
        console.log('Error checking profile:', profileError)
      }
    } else {
      console.log('✅ Profile found:')
      console.log(`  - ID: ${profile.id}`)
      console.log(`  - Email: ${profile.email}`)
      console.log(`  - Username: ${profile.username || 'Not set'}`)
      console.log(`  - Created: ${new Date(profile.created_at).toLocaleDateString()}`)
    }
    
    // Check for any user progress
    if (profile) {
      console.log('\n2. Checking user activity:')
      const { count: progressCount } = await supabase
        .from('user_progress')
        .select('*', { count: 'exact', head: true })
        .eq('user_id', profile.id)
      
      console.log(`  - Progress records: ${progressCount || 0}`)
      
      const { count: assessmentCount } = await supabase
        .from('user_interests')
        .select('*', { count: 'exact', head: true })
        .eq('user_id', profile.id)
      
      console.log(`  - Interest assessments: ${assessmentCount || 0}`)
    }
    
    // Try to get user via auth admin (this requires service role key)
    console.log('\n3. Checking Supabase Auth:')
    console.log('Note: Full auth.users table access requires admin privileges')
    console.log('If the user exists in auth but can\'t log in, possible issues:')
    console.log('  - Email not confirmed (check email for confirmation link)')
    console.log('  - Password needs to be reset')
    console.log('  - Account might be locked')
    
    console.log('\n' + '=' .repeat(50))
    console.log('\n📝 Troubleshooting Steps:')
    console.log('\n1. Try Password Reset:')
    console.log('   - Go to the login page')
    console.log('   - Click "Forgot Password?"')
    console.log('   - Enter: jessicawestbrook88@gmail.com')
    console.log('   - Check email for reset link')
    
    console.log('\n2. Check Email Confirmation:')
    console.log('   - Look for confirmation email from Supabase')
    console.log('   - Subject usually contains "Confirm your email"')
    console.log('   - Click the confirmation link')
    
    console.log('\n3. Try Creating New Account:')
    console.log('   - If it says email already exists, the account is in auth.users')
    console.log('   - Use password reset instead')
    
    console.log('\n4. Manual Fix via Supabase Dashboard:')
    console.log('   - Go to: https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/auth/users')
    console.log('   - Search for: jessicawestbrook88@gmail.com')
    console.log('   - Check user status and last sign in')
    console.log('   - Can manually send password reset or delete/recreate user')
    
  } catch (error) {
    console.error('Error checking user:', error)
  }
}

checkUserAuth()