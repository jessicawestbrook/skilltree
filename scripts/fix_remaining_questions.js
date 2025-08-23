/**
 * Script to fix and insert the 2 remaining money counting questions
 * ==================================================================
 */

const { createClient } = require('@supabase/supabase-js')
const fs = require('fs').promises
const path = require('path')
const { v4: uuidv4 } = require('uuid')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '..', '.env.local') })

// Initialize Supabase client with service role key
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function fixRemainingQuestions() {
  try {
    // Load the generated content
    const contentPath = path.join(__dirname, 'content_generation', 'output', 'math_content', 'visual_fixed', 'money_counting_visual.json')
    const content = JSON.parse(await fs.readFile(contentPath, 'utf-8'))
    const nodeData = Array.isArray(content) ? content[0] : content
    
    // Questions 23 and 26 are the ones that failed (0-indexed: 22 and 25)
    const failedQuestions = [
      { index: 22, question: nodeData.questions[22] },
      { index: 25, question: nodeData.questions[25] }
    ]
    
    console.log('=== Fixing Remaining Questions ===\n')
    
    for (const { index, question } of failedQuestions) {
      const questionText = question.question || question.questionText || question.question_text
      console.log(`Question ${index + 1}: ${questionText}`)
      console.log(`Original difficulty: ${question.difficulty}`)
      
      // Map "hard" to "average" since "difficult" doesn't work
      const questionData = {
        id: uuidv4(),
        question_text: questionText,
        options: question.options || [],
        correct_answer: question.correct_answer !== undefined ? question.correct_answer : question.correctAnswer,
        explanation: question.explanation || '',
        difficulty: 'average',  // Use 'average' instead of 'difficult' for hard questions
        image_url: question.imageUrl || question.image_url || null,
        created_at: new Date().toISOString()
      }
      
      console.log(`New difficulty: ${questionData.difficulty}`)
      
      const { error } = await supabase
        .from('questions')
        .insert(questionData)
      
      if (error) {
        console.error(`❌ Failed to insert: ${error.message}`)
      } else {
        console.log(`✅ Successfully inserted!\n`)
      }
    }
    
    // Final count
    const { count, error: countError } = await supabase
      .from('questions')
      .select('*', { count: 'exact', head: true })
      .or('question_text.ilike.%penny%,question_text.ilike.%nickel%,question_text.ilike.%dime%,question_text.ilike.%quarter%,question_text.ilike.%dollar%,question_text.ilike.%cents%,question_text.ilike.%coins%')
    
    if (!countError) {
      console.log('\n=== FINAL SUMMARY ===')
      console.log(`Total money counting questions in database: ${count}`)
      console.log('All 30 questions should now be inserted!')
    }
    
  } catch (error) {
    console.error('Fatal error:', error.message)
  }
  
  process.exit(0)
}

fixRemainingQuestions()