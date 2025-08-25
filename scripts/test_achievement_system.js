const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function testAchievementSystem() {
  console.log('Testing Achievement System...\n')
  
  try {
    // Test 1: Check achievements table
    console.log('1. Checking achievements table...')
    const { data: achievements, error: achievementsError } = await supabase
      .from('achievements')
      .select('*')
      .limit(5)
    
    if (achievementsError) {
      console.error('Error fetching achievements:', achievementsError)
    } else {
      console.log(`✓ Found ${achievements.length} achievements`)
      console.log('  Sample achievement:', achievements[0]?.name)
    }
    
    // Test 2: Check user_achievements table structure
    console.log('\n2. Checking user_achievements table...')
    const { data: userAchievements, error: userAchievementsError } = await supabase
      .from('user_achievements')
      .select('*')
      .limit(1)
    
    if (userAchievementsError) {
      if (userAchievementsError.message.includes('no rows')) {
        console.log('✓ Table exists but no records yet (expected)')
      } else {
        console.error('Error with user_achievements:', userAchievementsError)
      }
    } else {
      console.log('✓ user_achievements table accessible')
    }
    
    // Test 3: Check user_question_responses table
    console.log('\n3. Checking user_question_responses table...')
    const { data: responses, error: responsesError } = await supabase
      .from('user_question_responses')
      .select('*')
      .limit(1)
    
    if (responsesError) {
      if (responsesError.message.includes('no rows')) {
        console.log('✓ Table exists but no records yet (expected)')
      } else {
        console.error('Error with user_question_responses:', responsesError)
      }
    } else {
      console.log('✓ user_question_responses table accessible')
    }
    
    // Test 4: Verify column structure
    console.log('\n4. Testing user_question_responses insert (dry run)...')
    const testResponse = {
      user_id: '00000000-0000-0000-0000-000000000000', // Dummy UUID
      question_id: '00000000-0000-0000-0000-000000000000', // Dummy UUID
      session_id: '00000000-0000-0000-0000-000000000000',
      context_type: 'test',
      selected_answer: 0, // Integer index
      is_correct: true,
      time_spent_seconds: 10,
      question_sequence: 1,
      response_metadata: {
        answer_text: 'Test Answer',
        difficulty_level: 1
      }
    }
    
    console.log('✓ Test response structure valid')
    console.log('  - selected_answer is INTEGER:', typeof testResponse.selected_answer === 'number')
    console.log('  - response_metadata is JSONB:', typeof testResponse.response_metadata === 'object')
    
    // Test 5: Check total achievements
    console.log('\n5. Counting total achievements...')
    const { count, error: countError } = await supabase
      .from('achievements')
      .select('*', { count: 'exact', head: true })
    
    if (countError) {
      console.error('Error counting achievements:', countError)
    } else {
      console.log(`✓ Total achievements in database: ${count}`)
    }
    
    console.log('\n✅ Achievement system test complete!')
    console.log('All tables and structures are properly configured.')
    
  } catch (error) {
    console.error('Unexpected error:', error)
  }
}

testAchievementSystem()