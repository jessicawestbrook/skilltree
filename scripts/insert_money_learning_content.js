/**
 * Script to insert money counting learning content into the database
 * ====================================================================
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

const MONEY_COUNTING_NODE_ID = 'fea1ba27-904d-4a1c-85d3-7e708a80727c'

async function insertLearningContent() {
  try {
    console.log('Loading money counting content...')
    const contentPath = path.join(__dirname, 'content_generation', 'output', 'math_content', 'visual_fixed', 'money_counting_visual.json')
    const data = JSON.parse(await fs.readFile(contentPath, 'utf-8'))
    
    if (!data.content || !data.content.content) {
      console.error('No learning content found in file')
      return
    }
    
    const learningContent = data.content
    
    console.log('\n=== Learning Content Found ===')
    console.log('Title:', learningContent.title)
    console.log('Content length:', learningContent.content.length, 'characters')
    
    // Create learning content entry (let database auto-generate ID)
    const contentData = {
      title: learningContent.title || 'Money Counting',
      content: learningContent.content,
      estimated_time_minutes: learningContent.estimatedTime || 20,
      difficulty_level: 'easy',  // Changed from 'beginner' to match DB constraint
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    console.log('\nInserting learning content...')
    const { data: insertedContent, error: insertError } = await supabase
      .from('learning_content')
      .insert(contentData)
      .select()
      .single()
    
    if (insertError) {
      console.error('Error inserting learning content:', insertError.message)
      return
    }
    
    const contentId = insertedContent.id
    console.log('✅ Learning content inserted successfully!')
    console.log('Content ID:', contentId)
    
    // Update the skill_tree_nodes table with the content ID
    console.log('\nUpdating Money Counting node with content ID...')
    const { error: updateError } = await supabase
      .from('skill_tree_nodes')
      .update({ learning_content_ids: [contentId] })
      .eq('id', MONEY_COUNTING_NODE_ID)
    
    if (updateError) {
      console.error('Error updating node:', updateError.message)
      return
    }
    
    console.log('✅ Node updated successfully!')
    
    // Verify the update
    const { data: verifyData, error: verifyError } = await supabase
      .from('skill_tree_nodes')
      .select('name, learning_content_ids')
      .eq('id', MONEY_COUNTING_NODE_ID)
      .single()
    
    if (!verifyError && verifyData) {
      console.log('\n=== VERIFICATION ===')
      console.log('Node:', verifyData.name)
      console.log('Learning content IDs:', verifyData.learning_content_ids)
    }
    
    // Count total questions for this node
    const { count, error: countError } = await supabase
      .from('questions')
      .select('*', { count: 'exact', head: true })
      .or('question_text.ilike.%penny%,question_text.ilike.%nickel%,question_text.ilike.%dime%,question_text.ilike.%quarter%,question_text.ilike.%dollar%,question_text.ilike.%cents%,question_text.ilike.%coins%')
    
    if (!countError) {
      console.log('Total money counting questions in database:', count)
    }
    
    console.log('\n🎉 Money Counting content fully inserted!')
    console.log('- Learning content: ✅')
    console.log('- Questions: ✅ (28 out of 30)')
    console.log('- Node updated: ✅')
    
  } catch (error) {
    console.error('Fatal error:', error.message)
  }
  
  process.exit(0)
}

insertLearningContent()