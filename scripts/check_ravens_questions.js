const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

// Initialize Supabase client
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function checkCurrentQuestions() {
  console.log('Checking current questions table structure...')
  
  try {
    // Get sample questions to see the format
    const { data: sampleQuestions, error } = await supabase
      .from('questions')
      .select('*')
      .limit(5)
    
    if (error) {
      console.error('Error fetching questions:', error)
      return
    }
    
    console.log('\nTable structure (columns):')
    console.log(Object.keys(sampleQuestions[0]).join(', '))
    
    console.log('\nSample questions from database:')
    sampleQuestions.forEach((q, i) => {
      console.log(`${i + 1}. ID: ${q.id}`)
      console.log(`   Text: ${q.question_text.substring(0, 60)}...`)
      console.log(`   Difficulty: ${q.difficulty}`)
      console.log(`   Options: ${JSON.stringify(q.options)}`)
      console.log('')
    })
    
    // Check if any Ravens-style questions exist
    const { data: ravensQuestions, error: ravensError } = await supabase
      .from('questions')
      .select('*')
      .or('question_text.ilike.%matrix%,question_text.ilike.%pattern%,question_text.ilike.%grid%')
    
    if (ravensError) {
      console.error('Error checking for Ravens questions:', ravensError)
      return
    }
    
    console.log(`Found ${ravensQuestions.length} existing pattern/matrix/grid questions`)
    
    if (ravensQuestions.length > 0) {
      console.log('\nExisting pattern-related questions:')
      ravensQuestions.forEach((q, i) => {
        console.log(`${i + 1}. ${q.question_text.substring(0, 80)}...`)
      })
    }
    
  } catch (error) {
    console.error('Failed to check questions:', error)
  }
}

// Run the check
checkCurrentQuestions()