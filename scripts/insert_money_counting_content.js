/**
 * Script to insert money counting content into the database
 * ==========================================================
 * 
 * This script reads the money counting content from the visual_fixed JSON file
 * and inserts it into the Supabase database.
 */

const { createClient } = require('@supabase/supabase-js')
const fs = require('fs').promises
const path = require('path')
const { v4: uuidv4 } = require('uuid')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '..', '.env.local') })

// Initialize Supabase client with service role key for admin access
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

const CONFIG = {
  inputFile: path.join(__dirname, 'content_generation', 'output', 'math_content', 'visual_fixed', 'money_counting_visual.json'),
  progressFile: path.join(__dirname, 'money_counting_insertion_progress.json')
}

async function insertMoneyCountingContent() {
  try {
    console.log('Loading money counting content...')
    const content = JSON.parse(await fs.readFile(CONFIG.inputFile, 'utf-8'))
    
    // Extract the data (handle both object and array format)
    const nodeData = Array.isArray(content) ? content[0] : content
    
    if (nodeData.nodeId !== 'fea1ba27-904d-4a1c-85d3-7e708a80727c') {
      console.error('Node ID mismatch! Expected Money Counting node.')
      return
    }
    
    console.log('\n=== Money Counting Content Found ===')
    console.log('Node ID:', nodeData.nodeId)
    console.log('Node Name:', nodeData.nodeName)
    console.log('Questions count:', nodeData.questions?.length || 0)
    console.log('Has learning content:', !!nodeData.learningContent)
    
    // Insert questions
    if (nodeData.questions && nodeData.questions.length > 0) {
      console.log('\nInserting questions...')
      let insertedCount = 0
      let errorCount = 0
      
      for (const [index, question] of nodeData.questions.entries()) {
        try {
          const questionId = uuidv4()
          // Map difficulty values to match database constraints
          const difficultyMap = {
            'easy': 'easy',
            'medium': 'average',
            'hard': 'difficult',
            'average': 'average',
            'difficult': 'difficult'
          };
          
          const questionData = {
            id: questionId,
            question_text: question.question || question.questionText || question.question_text,
            options: question.options || question.answer_options || [],
            correct_answer: question.correct_answer !== undefined ? question.correct_answer : question.correctAnswer,
            explanation: question.explanation || '',
            difficulty: difficultyMap[question.difficulty] || 'average',
            image_url: question.imageUrl || question.image_url || null,
            created_at: new Date().toISOString()
          }
          
          // Validate question data
          if (!questionData.question_text) {
            console.error(`Question ${index + 1} missing question text`)
            errorCount++
            continue
          }
          
          if (!Array.isArray(questionData.options) || questionData.options.length === 0) {
            console.error(`Question ${index + 1} missing options`)
            errorCount++
            continue
          }
          
          const { error } = await supabase
            .from('questions')
            .insert(questionData)
          
          if (error) {
            console.error(`Error inserting question ${index + 1}:`, error.message)
            errorCount++
          } else {
            insertedCount++
            if (insertedCount % 5 === 0) {
              console.log(`  Inserted ${insertedCount} questions...`)
            }
          }
        } catch (err) {
          console.error(`Error processing question ${index + 1}:`, err.message)
          errorCount++
        }
      }
      
      console.log(`\nQuestions insertion complete:`)
      console.log(`  Successfully inserted: ${insertedCount}`)
      console.log(`  Errors: ${errorCount}`)
    }
    
    // Insert learning content if it exists
    if (nodeData.learningContent) {
      console.log('\nInserting learning content...')
      try {
        const contentId = uuidv4()
        const contentData = {
          id: contentId,
          title: 'Money Counting',
          content: nodeData.learningContent,
          estimated_time_minutes: 20,
          difficulty_level: 'beginner',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        
        const { error } = await supabase
          .from('learning_content')
          .insert(contentData)
        
        if (error) {
          console.error('Error inserting learning content:', error.message)
        } else {
          console.log('Learning content inserted successfully!')
          console.log('Content ID:', contentId)
          
          // Update the skill_tree_nodes table with the content ID
          console.log('\nUpdating skill tree node with content ID...')
          const { error: updateError } = await supabase
            .from('skill_tree_nodes')
            .update({ learning_content_ids: [contentId] })
            .eq('id', nodeData.nodeId)
          
          if (updateError) {
            console.error('Error updating node:', updateError.message)
          } else {
            console.log('Node updated successfully!')
          }
        }
      } catch (err) {
        console.error('Error processing learning content:', err.message)
      }
    }
    
    // Save progress
    const progress = {
      timestamp: new Date().toISOString(),
      nodeId: nodeData.nodeId,
      nodeName: nodeData.nodeName,
      questionsProcessed: nodeData.questions?.length || 0,
      contentInserted: !!nodeData.learningContent
    }
    
    await fs.writeFile(CONFIG.progressFile, JSON.stringify(progress, null, 2))
    console.log('\n✅ Money counting content insertion complete!')
    
  } catch (error) {
    console.error('Fatal error:', error.message)
  }
  
  process.exit(0)
}

// Run the insertion
insertMoneyCountingContent()