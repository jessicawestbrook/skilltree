const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function migrateInterestsQuizData() {
  console.log('Migrating interests quiz data to row-based storage...\n')
  console.log('=' .repeat(50))
  
  try {
    // 1. Check if old column-based data exists
    console.log('\n1. Checking for existing quiz data in profiles table...')
    
    // Get a sample profile to check structure
    const { data: sampleProfile, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .limit(1)
      .single()
    
    if (profileError) {
      console.log('❌ Error fetching profile:', profileError.message)
      return
    }
    
    // Check if profile has quiz-related columns
    const quizColumns = []
    const profileKeys = Object.keys(sampleProfile || {})
    
    // Common patterns for quiz columns
    const quizPatterns = [
      'interest_', 'quiz_', 'preference_', 'learning_style',
      'career_interest', 'subject_interest', 'skill_level'
    ]
    
    profileKeys.forEach(key => {
      if (quizPatterns.some(pattern => key.toLowerCase().includes(pattern))) {
        quizColumns.push(key)
      }
    })
    
    if (quizColumns.length === 0) {
      console.log('✅ No quiz columns found in profiles table. Nothing to migrate.')
      return
    }
    
    console.log(`Found ${quizColumns.length} potential quiz columns:`)
    quizColumns.forEach(col => console.log(`  - ${col}`))
    
    // 2. Get all profiles with quiz data
    console.log('\n2. Fetching profiles with quiz data...')
    const { data: profiles, error: fetchError } = await supabase
      .from('profiles')
      .select('id, email, ' + quizColumns.join(', '))
    
    if (fetchError) {
      console.log('❌ Error fetching profiles:', fetchError.message)
      return
    }
    
    const profilesWithData = profiles.filter(p => 
      quizColumns.some(col => p[col] !== null && p[col] !== undefined)
    )
    
    console.log(`Found ${profilesWithData.length} profiles with quiz data`)
    
    if (profilesWithData.length === 0) {
      console.log('✅ No quiz data to migrate')
      return
    }
    
    // 3. Migrate each profile's quiz data
    console.log('\n3. Migrating quiz data...')
    let migrated = 0
    let failed = 0
    
    for (const profile of profilesWithData) {
      try {
        // Create a quiz response record
        const { data: response, error: responseError } = await supabase
          .from('interests_quiz_responses')
          .insert({
            user_id: profile.id,
            quiz_version: 0, // Mark as migrated data
            started_at: new Date().toISOString(),
            completed_at: new Date().toISOString(),
            is_complete: true,
            metadata: { 
              source: 'migration',
              migrated_from: 'profiles_table',
              original_columns: quizColumns
            }
          })
          .select()
          .single()
        
        if (responseError) {
          console.log(`❌ Failed to create response for user ${profile.email}:`, responseError.message)
          failed++
          continue
        }
        
        // Convert column data to interests
        const interests = []
        
        quizColumns.forEach(col => {
          const value = profile[col]
          if (value !== null && value !== undefined) {
            // Determine category from column name
            let category = col.replace(/^(interest_|quiz_|preference_)/, '')
            
            // Calculate interest level based on value type
            let interestLevel = 0.5 // default
            if (typeof value === 'boolean') {
              interestLevel = value ? 0.8 : 0.2
            } else if (typeof value === 'number') {
              // Assume 0-10 scale, normalize to 0-1
              interestLevel = Math.min(1, Math.max(0, value / 10))
            } else if (typeof value === 'string') {
              // If it's a string, assume interest exists
              interestLevel = 0.7
            }
            
            interests.push({
              user_id: profile.id,
              interest_category: category,
              interest_level: interestLevel,
              confidence_score: 0.5, // Lower confidence for migrated data
              source: 'migration',
              quiz_response_id: response.id
            })
          }
        })
        
        if (interests.length > 0) {
          const { error: interestError } = await supabase
            .from('user_interests')
            .insert(interests)
          
          if (interestError) {
            console.log(`⚠️  Failed to insert interests for user ${profile.email}:`, interestError.message)
          } else {
            console.log(`✅ Migrated ${interests.length} interests for ${profile.email}`)
            migrated++
          }
        }
        
      } catch (err) {
        console.error(`Error migrating profile ${profile.id}:`, err)
        failed++
      }
    }
    
    // 4. Summary
    console.log('\n' + '=' .repeat(50))
    console.log('\n📊 MIGRATION SUMMARY:')
    console.log(`✅ Successfully migrated: ${migrated} profiles`)
    console.log(`❌ Failed migrations: ${failed} profiles`)
    
    if (migrated > 0) {
      console.log('\n🎯 NEXT STEPS:')
      console.log('1. Verify the migrated data in the new tables')
      console.log('2. Update the application to use interestsQuizService')
      console.log('3. Consider removing old quiz columns from profiles table')
      console.log('\nTo remove old columns (after verification), run:')
      
      console.log('\nALTER TABLE profiles')
      quizColumns.forEach(col => {
        console.log(`  DROP COLUMN IF EXISTS ${col},`)
      })
      console.log('  DROP COLUMN IF EXISTS dummy; -- Remove trailing comma')
    }
    
  } catch (error) {
    console.error('Migration error:', error)
  }
}

// Run migration
migrateInterestsQuizData()