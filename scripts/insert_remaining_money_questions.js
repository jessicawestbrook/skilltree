/**
 * Script to insert remaining money counting questions
 * ====================================================
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

async function insertRemainingQuestions() {
  try {
    // First, check existing questions
    console.log('Checking existing money counting questions...')
    const { data: existingQuestions, error: fetchError } = await supabase
      .from('questions')
      .select('question_text')
      .or('question_text.ilike.%penny%,question_text.ilike.%nickel%,question_text.ilike.%dime%,question_text.ilike.%quarter%,question_text.ilike.%dollar%,question_text.ilike.%cents%,question_text.ilike.%coins%')
    
    if (fetchError) throw fetchError
    
    const existingTexts = new Set(existingQuestions.map(q => q.question_text.toLowerCase()));
    console.log(`Found ${existingQuestions.length} existing money counting questions`)
    
    // Load the generated content
    const contentPath = path.join(__dirname, 'content_generation', 'output', 'math_content', 'visual_fixed', 'money_counting_visual.json')
    const content = JSON.parse(await fs.readFile(contentPath, 'utf-8'))
    const nodeData = Array.isArray(content) ? content[0] : content
    
    // Map difficulty values
    const difficultyMap = {
      'easy': 'easy',
      'medium': 'average',
      'hard': 'difficult'
    };
    
    let insertedCount = 0
    let skippedCount = 0
    let errorCount = 0
    
    console.log('\nInserting remaining questions...')
    
    for (const [index, question] of nodeData.questions.entries()) {
      try {
        const questionText = question.question || question.questionText || question.question_text
        
        // Skip if already exists
        if (existingTexts.has(questionText.toLowerCase())) {
          skippedCount++
          continue
        }
        
        const questionData = {
          id: uuidv4(),
          question_text: questionText,
          options: question.options || [],
          correct_answer: question.correct_answer !== undefined ? question.correct_answer : question.correctAnswer,
          explanation: question.explanation || '',
          difficulty: difficultyMap[question.difficulty] || 'average',
          image_url: question.imageUrl || question.image_url || null,
          created_at: new Date().toISOString()
        }
        
        // Validate
        if (!questionData.question_text || !Array.isArray(questionData.options) || questionData.options.length === 0) {
          console.error(`Question ${index + 1} invalid`)
          errorCount++
          continue
        }
        
        const { error } = await supabase
          .from('questions')
          .insert(questionData)
        
        if (error) {
          console.error(`Error inserting question ${index + 1}: ${error.message}`)
          errorCount++
        } else {
          insertedCount++
          console.log(`  ✓ Inserted: ${questionText.substring(0, 50)}...`)
        }
      } catch (err) {
        console.error(`Error processing question ${index + 1}:`, err.message)
        errorCount++
      }
    }
    
    console.log('\n=== SUMMARY ===')
    console.log(`Successfully inserted: ${insertedCount}`)
    console.log(`Already existed (skipped): ${skippedCount}`)
    console.log(`Errors: ${errorCount}`)
    console.log(`Total processed: ${nodeData.questions.length}`)
    
  } catch (error) {
    console.error('Fatal error:', error.message)
  }
  
  process.exit(0)
}

insertRemainingQuestions()