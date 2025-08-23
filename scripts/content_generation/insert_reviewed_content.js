/**
 * Script to insert reviewed content into the database
 * ====================================================
 * 
 * This script reads the reviewed content from the JSON file
 * and inserts it into the Supabase database.
 */

const { createClient } = require('@supabase/supabase-js')
const fs = require('fs').promises
const path = require('path')
const { v4: uuidv4 } = require('uuid')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '../..', '.env.local') })

// Initialize Supabase client
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

const CONFIG = {
  reviewFile: path.join(__dirname, 'output', 'math_content', 'content_for_review.json'),
  insertedFile: path.join(__dirname, 'output', 'math_content', 'inserted_content.json'),
  errorFile: path.join(__dirname, 'output', 'math_content', 'insertion_errors.json')
}

class ContentInserter {
  constructor() {
    this.stats = {
      totalItems: 0,
      successfulInsertions: 0,
      failedInsertions: 0,
      contentIds: [],
      errors: []
    }
  }

  async loadReviewedContent() {
    try {
      const content = await fs.readFile(CONFIG.reviewFile, 'utf-8')
      return JSON.parse(content)
    } catch (error) {
      console.error('Error loading review file:', error.message)
      return []
    }
  }

  async insertLearningContent(nodeId, content) {
    try {
      // Prepare content data
      const contentData = {
        title: content.title,
        content: content.content,
        estimated_time_minutes: content.estimated_time_minutes || 20,
        difficulty_level: content.difficulty_level || 'intermediate',
        images: content.images || null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }

      // Insert into learning_content table
      const { data, error } = await supabase
        .from('learning_content')
        .insert(contentData)
        .select()
        .single()

      if (error) {
        throw error
      }

      return data.id
    } catch (error) {
      console.error(`Error inserting content for node ${nodeId}:`, error.message)
      throw error
    }
  }

  async insertQuestions(questions) {
    const questionIds = []
    const errors = []

    for (const question of questions) {
      try {
        const questionId = uuidv4()
        const questionData = {
          id: questionId,
          question_text: question.question_text,
          options: question.options,
          correct_answer: question.correct_answer,
          explanation: question.explanation,
          difficulty: question.difficulty || 'medium',
          created_at: new Date().toISOString()
        }

        const { data, error } = await supabase
          .from('questions')
          .insert(questionData)

        if (error) {
          errors.push({ question: question.question_text, error: error.message })
        } else {
          questionIds.push(questionId)
        }
      } catch (error) {
        errors.push({ question: question.question_text, error: error.message })
      }
    }

    return { questionIds, errors }
  }

  async updateSkillNode(nodeId, contentId, questionIds) {
    try {
      // First, get the current node data
      const { data: currentNode, error: fetchError } = await supabase
        .from('skill_tree_nodes')
        .select('learning_content_ids')
        .eq('id', nodeId)
        .single()

      if (fetchError) {
        throw fetchError
      }

      // Prepare the update
      const currentContentIds = currentNode.learning_content_ids || []
      const updatedContentIds = [...currentContentIds, contentId]

      // Update the node
      const { data, error } = await supabase
        .from('skill_tree_nodes')
        .update({
          learning_content_ids: updatedContentIds,
          updated_at: new Date().toISOString()
        })
        .eq('id', nodeId)

      if (error) {
        throw error
      }

      // Also update the learning_content with question IDs
      if (questionIds.length > 0) {
        const { error: updateError } = await supabase
          .from('learning_content')
          .update({ question_ids: questionIds })
          .eq('id', contentId)

        if (updateError) {
          console.error(`Error updating content with question IDs:`, updateError.message)
        }
      }

      return true
    } catch (error) {
      console.error(`Error updating skill node ${nodeId}:`, error.message)
      throw error
    }
  }

  async processItem(item) {
    console.log(`\nProcessing: ${item.nodeName}`)
    
    try {
      // Insert learning content
      console.log('  - Inserting learning content...')
      const contentId = await this.insertLearningContent(item.nodeId, item.content)
      console.log(`    ✓ Content inserted with ID: ${contentId}`)

      // Insert questions
      console.log('  - Inserting questions...')
      const { questionIds, errors } = await this.insertQuestions(item.questions || [])
      console.log(`    ✓ Inserted ${questionIds.length} questions`)
      
      if (errors.length > 0) {
        console.log(`    ⚠ ${errors.length} questions failed to insert`)
        this.stats.errors.push(...errors)
      }

      // Update skill node
      console.log('  - Updating skill node...')
      await this.updateSkillNode(item.nodeId, contentId, questionIds)
      console.log(`    ✓ Skill node updated`)

      this.stats.successfulInsertions++
      this.stats.contentIds.push({
        nodeId: item.nodeId,
        nodeName: item.nodeName,
        contentId: contentId,
        questionCount: questionIds.length
      })

      return { success: true, contentId, questionIds }
    } catch (error) {
      this.stats.failedInsertions++
      this.stats.errors.push({
        nodeId: item.nodeId,
        nodeName: item.nodeName,
        error: error.message
      })
      return { success: false, error: error.message }
    }
  }

  async run() {
    console.log('Content Insertion Script')
    console.log('========================\n')

    // Load reviewed content
    const reviewedContent = await this.loadReviewedContent()
    
    if (reviewedContent.length === 0) {
      console.log('No content found for insertion.')
      console.log('Please run generate_math_content_v2.js first to generate content.')
      return
    }

    this.stats.totalItems = reviewedContent.length
    console.log(`Found ${this.stats.totalItems} items to insert\n`)

    // Process each item
    for (const item of reviewedContent) {
      await this.processItem(item)
    }

    // Save results
    await fs.writeFile(
      CONFIG.insertedFile,
      JSON.stringify(this.stats.contentIds, null, 2)
    )

    if (this.stats.errors.length > 0) {
      await fs.writeFile(
        CONFIG.errorFile,
        JSON.stringify(this.stats.errors, null, 2)
      )
    }

    // Print summary
    console.log('\n' + '='.repeat(50))
    console.log('INSERTION COMPLETE')
    console.log('='.repeat(50))
    console.log(`Total items: ${this.stats.totalItems}`)
    console.log(`Successful: ${this.stats.successfulInsertions}`)
    console.log(`Failed: ${this.stats.failedInsertions}`)
    
    if (this.stats.errors.length > 0) {
      console.log(`\nErrors saved to: ${CONFIG.errorFile}`)
    }
    
    console.log(`\nInserted content details saved to: ${CONFIG.insertedFile}`)
  }
}

// Main execution
if (require.main === module) {
  const inserter = new ContentInserter()
  inserter.run().catch(console.error)
}

module.exports = ContentInserter