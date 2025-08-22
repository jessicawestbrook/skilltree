/**
 * Script to generate descriptions for 2nd and 3rd level categories using Claude API
 * 
 * This script:
 * 1. Fetches all 2nd and 3rd level categories without descriptions
 * 2. Uses Claude API to generate engaging, specific descriptions
 * 3. Updates the database with the generated descriptions
 * 4. Processes in batches with rate limiting
 */

const { createClient } = require('@supabase/supabase-js')
const Anthropic = require('@anthropic-ai/sdk')
const fs = require('fs')
const path = require('path')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '..', '.env.local') })

// Initialize clients
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY, // You'll need to add this to your .env.local
})

// Configuration
const BATCH_SIZE = 10
const DELAY_BETWEEN_BATCHES = 2000 // 2 seconds
const OUTPUT_FILE = path.join(__dirname, 'category_descriptions_generated.json')
const BACKUP_FILE = path.join(__dirname, 'category_descriptions_backup.json')

/**
 * Get all nodes that need descriptions
 */
async function getCategoriesNeedingDescriptions() {
  try {
    console.log('Fetching all nodes needing descriptions...')
    
    // Get all nodes with pagination to avoid 1000 limit
    let allNodes = []
    let from = 0
    const batchSize = 1000
    
    while (true) {
      const { data, error } = await supabase
        .from('skill_tree_nodes')
        .select('id, parent_id, name, description, metadata')
        .range(from, from + batchSize - 1)
        
      if (error) {
        throw error
      }
      
      allNodes = allNodes.concat(data)
      
      if (data.length < batchSize) {
        break // No more data
      }
      
      from += batchSize
    }

    console.log(`Loaded ${allNodes.length} total nodes`)

    // Filter for nodes missing descriptions (exclude root nodes)
    const needingDescriptions = allNodes.filter(node => 
      node.parent_id && // Exclude root nodes
      (!node.description || node.description.trim().length === 0)
    )

    console.log(`Found ${needingDescriptions.length} nodes needing descriptions`)
    console.log(`Total nodes: ${allNodes.length}`)
    console.log(`Nodes with descriptions: ${allNodes.length - needingDescriptions.length - allNodes.filter(n => !n.parent_id).length}`)
    
    return needingDescriptions
  } catch (error) {
    console.error('Error fetching categories:', error)
    return []
  }
}

/**
 * Generate description for a node using Claude API
 */
async function generateDescription(node, parentName = null) {
  try {
    const prompt = `Generate an engaging and specific description for this learning topic:

Topic Name: ${node.name}
Parent Category: ${parentName || 'Unknown'}
Metadata: ${node.metadata ? JSON.stringify(node.metadata) : 'None'}

Requirements:
- Make the content seem interesting and appealing to learners
- Be specific enough to differentiate this topic from others
- Give detail about what people are likely to learn
- Keep it between 100-200 words
- Use active, engaging language
- Don't assume hands-on learning (this is an online platform)
- Don't promise professional certification or that users will become professionals
- Focus on knowledge and skills gained, not career outcomes
- Make it appropriate for homeschooling, supplemental learning, and lifelong learning
- Target the appropriate age group based on the subject matter
- If this is a specific skill or concept, explain what it involves and why it's useful

Generate only the description text, no additional formatting or explanation.`

    const message = await anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 300,
      messages: [
        {
          role: "user",
          content: prompt
        }
      ]
    })

    return message.content[0].text.trim()
  } catch (error) {
    console.error(`Error generating description for ${node.name}:`, error)
    return null
  }
}

/**
 * Save progress to file
 */
function saveProgress(processedCategories) {
  const progressData = {
    timestamp: new Date().toISOString(),
    processedCount: processedCategories.length,
    categories: processedCategories
  }
  
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(progressData, null, 2))
  console.log(`Progress saved: ${processedCategories.length} categories processed`)
}

/**
 * Load existing progress
 */
function loadProgress() {
  try {
    if (fs.existsSync(OUTPUT_FILE)) {
      const data = JSON.parse(fs.readFileSync(OUTPUT_FILE, 'utf8'))
      console.log(`Loaded existing progress: ${data.processedCount} categories`)
      return data.categories || []
    }
  } catch (error) {
    console.error('Error loading progress:', error)
  }
  return []
}

/**
 * Update database with generated descriptions
 */
async function updateCategoryDescription(categoryId, description) {
  try {
    const { error } = await supabase
      .from('skill_tree_nodes')
      .update({ 
        description: description,
        updated_at: new Date().toISOString()
      })
      .eq('id', categoryId)

    if (error) {
      throw error
    }

    return true
  } catch (error) {
    console.error(`Error updating category ${categoryId}:`, error)
    return false
  }
}

/**
 * Create backup of existing data
 */
async function createBackup() {
  try {
    console.log('Creating backup of existing node data...')
    
    // Get all nodes with descriptions in batches
    let allNodesWithDesc = []
    let from = 0
    const batchSize = 1000
    
    while (true) {
      const { data, error } = await supabase
        .from('skill_tree_nodes')
        .select('id, name, description, updated_at')
        .not('description', 'is', null)
        .neq('description', '')
        .range(from, from + batchSize - 1)

      if (error) {
        throw error
      }
      
      allNodesWithDesc = allNodesWithDesc.concat(data)
      
      if (data.length < batchSize) {
        break
      }
      
      from += batchSize
    }

    const backupData = {
      timestamp: new Date().toISOString(),
      nodes: allNodesWithDesc
    }

    fs.writeFileSync(BACKUP_FILE, JSON.stringify(backupData, null, 2))
    console.log(`Backup created with ${allNodesWithDesc.length} nodes`)
  } catch (error) {
    console.error('Error creating backup:', error)
  }
}

/**
 * Main execution function
 */
async function main() {
  try {
    console.log('=== Category Description Generation Script ===')
    console.log('This script will generate descriptions for 2nd and 3rd level categories')
    console.log('')

    // Check required environment variables
    if (!process.env.ANTHROPIC_API_KEY) {
      console.error('ERROR: ANTHROPIC_API_KEY environment variable is required')
      console.log('Please add your Claude API key to .env.local file')
      process.exit(1)
    }

    // Create backup
    await createBackup()

    // Load existing progress
    const processedCategories = loadProgress()
    const processedIds = new Set(processedCategories.map(c => c.id))

    // Get categories needing descriptions
    const allCategories = await getCategoriesNeedingDescriptions()
    const remainingCategories = allCategories.filter(c => !processedIds.has(c.id))

    if (remainingCategories.length === 0) {
      console.log('All categories already have descriptions or are processed!')
      return
    }

    console.log(`Processing ${remainingCategories.length} remaining categories...`)
    console.log('')

    // Process in batches
    for (let i = 0; i < remainingCategories.length; i += BATCH_SIZE) {
      const batch = remainingCategories.slice(i, i + BATCH_SIZE)
      console.log(`Processing batch ${Math.floor(i / BATCH_SIZE) + 1}/${Math.ceil(remainingCategories.length / BATCH_SIZE)}`)

      for (const node of batch) {
        console.log(`Generating description for: ${node.name}`)
        
        const description = await generateDescription(node)
        
        if (description) {
          const result = {
            id: node.id,
            name: node.name,
            parent_id: node.parent_id,
            generated_description: description,
            timestamp: new Date().toISOString(),
            updated_in_db: false
          }

          // Update database
          const success = await updateCategoryDescription(node.id, description)
          result.updated_in_db = success

          processedCategories.push(result)
          
          if (success) {
            console.log(`✅ Updated: ${node.name}`)
          } else {
            console.log(`❌ Failed to update: ${node.name}`)
          }
        } else {
          console.log(`❌ Failed to generate description for: ${node.name}`)
        }

        // Small delay between individual requests
        await new Promise(resolve => setTimeout(resolve, 500))
      }

      // Save progress after each batch
      saveProgress(processedCategories)

      // Delay between batches (except for last batch)
      if (i + BATCH_SIZE < remainingCategories.length) {
        console.log(`Waiting ${DELAY_BETWEEN_BATCHES}ms before next batch...`)
        await new Promise(resolve => setTimeout(resolve, DELAY_BETWEEN_BATCHES))
      }
    }

    console.log('')
    console.log('=== Summary ===')
    const successful = processedCategories.filter(c => c.updated_in_db).length
    const failed = processedCategories.filter(c => !c.updated_in_db).length
    
    console.log(`Successfully updated: ${successful} categories`)
    console.log(`Failed updates: ${failed} categories`)
    console.log(`Results saved to: ${OUTPUT_FILE}`)
    console.log(`Backup saved to: ${BACKUP_FILE}`)

  } catch (error) {
    console.error('Script execution error:', error)
    process.exit(1)
  }
}

// Run the script
if (require.main === module) {
  main()
}

module.exports = { main, generateDescription, getCategoriesNeedingDescriptions }