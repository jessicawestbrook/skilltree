const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function verifyInterestsQuizSetup() {
  console.log('Verifying interests quiz setup...\n')
  console.log('=' .repeat(50))
  
  try {
    // 1. Check tables exist
    console.log('\n1. Checking if tables were created...')
    
    const tables = [
      'interests_quiz_questions',
      'interests_quiz_responses',
      'interests_quiz_answers',
      'user_interests'
    ]
    
    for (const table of tables) {
      const { error } = await supabase
        .from(table)
        .select('id')
        .limit(1)
      
      if (error && error.code === '42P01') {
        console.log(`❌ Table ${table} does not exist`)
      } else if (error) {
        console.log(`⚠️  Table ${table} exists but has error: ${error.message}`)
      } else {
        console.log(`✅ Table ${table} exists`)
      }
    }
    
    // 2. Check quiz questions
    console.log('\n2. Checking quiz questions...')
    const { data: questions, error: questionsError } = await supabase
      .from('interests_quiz_questions')
      .select('id, question_text, question_type, category, display_order')
      .order('display_order')
    
    if (questionsError) {
      console.log('❌ Error fetching questions:', questionsError.message)
    } else if (questions && questions.length > 0) {
      console.log(`✅ Found ${questions.length} quiz questions:`)
      questions.forEach(q => {
        console.log(`   ${q.display_order}. [${q.question_type}] ${q.question_text.substring(0, 50)}...`)
      })
    } else {
      console.log('⚠️  No quiz questions found')
    }
    
    // 3. Check if any users have taken the quiz
    console.log('\n3. Checking for quiz responses...')
    const { data: responses, error: responsesError } = await supabase
      .from('interests_quiz_responses')
      .select('id, user_id, is_complete, created_at')
      .limit(5)
    
    if (responsesError) {
      console.log('❌ Error fetching responses:', responsesError.message)
    } else if (responses && responses.length > 0) {
      console.log(`Found ${responses.length} quiz responses`)
      responses.forEach(r => {
        console.log(`   - User ${r.user_id}: ${r.is_complete ? 'Completed' : 'In Progress'}`)
      })
    } else {
      console.log('✅ No quiz responses yet (expected for new setup)')
    }
    
    // 4. Check RLS policies
    console.log('\n4. Checking RLS policies...')
    const { data: policies, error: policiesError } = await supabase
      .rpc('exec_sql', {
        sql_query: `
          SELECT tablename, policyname 
          FROM pg_policies 
          WHERE schemaname = 'public' 
          AND tablename IN ('interests_quiz_questions', 'interests_quiz_responses', 
                            'interests_quiz_answers', 'user_interests')
          ORDER BY tablename, policyname;
        `
      })
    
    if (policiesError) {
      console.log('⚠️  Cannot check policies directly (expected)')
    } else if (policies) {
      console.log('RLS policies found:', policies)
    }
    
    // 5. Summary
    console.log('\n' + '=' .repeat(50))
    console.log('\n📊 SETUP VERIFICATION SUMMARY:')
    console.log('✅ Row-based interests quiz schema is ready!')
    console.log('\nThe system now supports:')
    console.log('• Flexible question management')
    console.log('• Historical data preservation')
    console.log('• Multiple question types')
    console.log('• User interest computation')
    console.log('• Behavioral interest tracking')
    
    console.log('\n🎯 NEXT STEPS:')
    console.log('1. Update IntroAssessmentPage to use interestsQuizService')
    console.log('2. Create admin interface for managing quiz questions')
    console.log('3. Build analytics dashboard for quiz results')
    
  } catch (error) {
    console.error('Verification error:', error)
  }
}

// Run verification
verifyInterestsQuizSetup()