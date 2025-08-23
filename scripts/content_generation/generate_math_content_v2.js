/**
 * Enhanced Math Content Generator v2 - Adapted for actual database schema
 * ========================================================================
 * 
 * This script generates comprehensive learning content for math topics
 * incorporating storytelling, philosophical questions, and engaging narratives
 * based on Kieran Egan's educational philosophy.
 * 
 * Adapted to work with the actual skill_tree_nodes table structure.
 */

const { createClient } = require('@supabase/supabase-js')
const Anthropic = require('@anthropic-ai/sdk')
const fs = require('fs').promises
const path = require('path')
const { v4: uuidv4 } = require('uuid')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '../..', '.env.local') })

// Initialize clients
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

// Check if API key exists
if (!process.env.ANTHROPIC_API_KEY) {
  console.error(`
ERROR: ANTHROPIC_API_KEY not found in environment variables.

Please add it to your .env.local file:
ANTHROPIC_API_KEY=your_api_key_here

You can get an API key from: https://console.anthropic.com/
`)
  process.exit(1)
}

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

// Configuration
const CONFIG = {
  batchSize: 3,
  apiDelay: 5000, // 5 seconds between API calls
  maxRetries: 3,
  outputDir: path.join(__dirname, 'output', 'math_content'),
  checkpointFile: path.join(__dirname, 'output', 'math_content', 'checkpoint.json'),
  progressFile: path.join(__dirname, 'output', 'math_content', 'progress.log'),
  reviewFile: path.join(__dirname, 'output', 'math_content', 'content_for_review.json')
}

// Math-related keywords to identify math nodes
const MATH_KEYWORDS = [
  'math', 'mathematics', 'counting', 'number', 'addition', 'subtraction',
  'multiplication', 'division', 'fraction', 'decimal', 'percentage', 'percent',
  'algebra', 'geometry', 'trigonometry', 'calculus', 'statistics', 'probability',
  'equation', 'formula', 'theorem', 'proof', 'arithmetic', 'measurement',
  'data', 'graph', 'chart', 'angle', 'shape', 'area', 'volume', 'perimeter'
]

// Difficulty ordering for math topics (from easiest to hardest)
const MATH_DIFFICULTY_ORDER = [
  'counting', 'numbers', 'basic', 'addition', 'subtraction',
  'multiplication', 'division', 'fractions', 'decimals', 'percentages',
  'pre-algebra', 'algebra', 'geometry', 'measurement', 'data', 'probability',
  'trigonometry', 'pre-calculus', 'calculus', 'statistics', 'linear algebra',
  'differential', 'abstract', 'topology', 'number theory'
]

class MathContentGenerator {
  constructor() {
    this.stats = {
      totalNodes: 0,
      processedNodes: 0,
      successfulContent: 0,
      failedNodes: 0,
      startTime: new Date(),
      apiCalls: 0,
      estimatedCost: 0
    }
    this.processedNodeIds = []
  }

  async initialize() {
    // Create output directory
    await fs.mkdir(CONFIG.outputDir, { recursive: true })
    
    // Load checkpoint if exists
    await this.loadCheckpoint()
    
    console.log('Math Content Generator v2 initialized')
    console.log(`Output directory: ${CONFIG.outputDir}`)
  }

  async loadCheckpoint() {
    try {
      const checkpointData = await fs.readFile(CONFIG.checkpointFile, 'utf-8')
      const checkpoint = JSON.parse(checkpointData)
      this.processedNodeIds = checkpoint.processedNodeIds || []
      this.stats = { ...this.stats, ...checkpoint.stats }
      console.log(`Loaded checkpoint: ${this.processedNodeIds.length} nodes already processed`)
    } catch (error) {
      console.log('No checkpoint found, starting fresh')
    }
  }

  async saveCheckpoint() {
    const checkpoint = {
      processedNodeIds: this.processedNodeIds,
      stats: this.stats,
      timestamp: new Date().toISOString()
    }
    await fs.writeFile(CONFIG.checkpointFile, JSON.stringify(checkpoint, null, 2))
  }

  async logProgress(message) {
    const timestamp = new Date().toISOString()
    const logMessage = `[${timestamp}] ${message}`
    console.log(logMessage)
    await fs.appendFile(CONFIG.progressFile, logMessage + '\n')
  }

  isMathNode(node) {
    const nameLower = node.name.toLowerCase()
    return MATH_KEYWORDS.some(keyword => nameLower.includes(keyword))
  }

  async loadMathNodes() {
    await this.logProgress('Loading math nodes from database...')
    
    let allNodes = []
    let from = 0
    const batchSize = 1000
    
    while (true) {
      const { data, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .range(from, from + batchSize - 1)
      
      if (error) {
        throw new Error(`Database error: ${error.message}`)
      }
      
      if (!data || data.length === 0) break
      
      allNodes = allNodes.concat(data)
      
      if (data.length < batchSize) break
      from += batchSize
    }
    
    // Filter for math nodes
    const mathNodes = allNodes.filter(node => this.isMathNode(node))
    
    // Filter for leaf nodes that need content
    const leafNodes = mathNodes.filter(node => {
      // Check if it needs content
      const hasContent = node.learning_content_ids && 
                        Array.isArray(node.learning_content_ids) && 
                        node.learning_content_ids.length > 0
      
      // Check if already processed
      const alreadyProcessed = this.processedNodeIds.includes(node.id)
      
      // Find if it has children (is not a leaf)
      const hasChildren = allNodes.some(n => n.parent_id === node.id)
      
      return !hasContent && !alreadyProcessed && !hasChildren
    })
    
    // Sort by difficulty order
    const sortedNodes = this.sortNodesByDifficulty(leafNodes)
    
    await this.logProgress(`Found ${mathNodes.length} math nodes total`)
    await this.logProgress(`Found ${sortedNodes.length} leaf math nodes needing content`)
    
    return sortedNodes
  }

  sortNodesByDifficulty(nodes) {
    return nodes.sort((a, b) => {
      const aName = a.name.toLowerCase()
      const bName = b.name.toLowerCase()
      
      // Find difficulty index
      let aIndex = MATH_DIFFICULTY_ORDER.length
      let bIndex = MATH_DIFFICULTY_ORDER.length
      
      for (let i = 0; i < MATH_DIFFICULTY_ORDER.length; i++) {
        const difficulty = MATH_DIFFICULTY_ORDER[i]
        if (aName.includes(difficulty)) {
          aIndex = Math.min(aIndex, i)
        }
        if (bName.includes(difficulty)) {
          bIndex = Math.min(bIndex, i)
        }
      }
      
      return aIndex - bIndex
    })
  }

  async generateLearningContent(node) {
    const prompt = `Generate comprehensive, engaging learning content for the mathematical topic: "${node.name}"

Context:
- Target Audience: Varied (adapt explanations for different levels)
- Content Length: 10-30 minutes of reading/study time
- Format: HTML with rich formatting

IMPORTANT: Follow Kieran Egan's educational philosophy:
1. Make the content MATTER to students - connect to their lives and big questions
2. Use STORYTELLING with concrete details, conflicts, and surprises
3. Include the human story - who discovered this? what problems did it solve?
4. Show the "So What?" - why this matters today and how it changed the world
5. End with philosophical questions that connect to moral choices or life decisions

Structure the content as follows:

<h1>[Engaging Title]</h1>

<section class="introduction">
  <h2>The Story Begins</h2>
  [Start with an engaging story or scenario that introduces the concept - make it matter!]
  [Include a conflict or problem that needs solving]
</section>

<section class="historical-context">
  <h2>The Human Story</h2>
  [Who discovered/developed this? What was their story?]
  [What problem were they trying to solve?]
  [Include specific historical details and drama]
</section>

<section class="core-concepts">
  <h2>Understanding ${node.name}</h2>
  [Clear explanations with visual descriptions]
  [Use analogies and real-world examples]
  [Build from simple to complex]
</section>

<section class="applications">
  <h2>Why This Matters</h2>
  [Real-world applications]
  [How this changed science/technology/society]
  [Current uses in everyday life]
</section>

<section class="practice-examples">
  <h2>See It In Action</h2>
  [2-3 worked examples with step-by-step solutions]
  [Start simple, increase complexity]
</section>

<section class="so-what">
  <h2>The Bigger Picture</h2>
  [How did this mathematical discovery change the future?]
  [What doors did it open for humanity?]
  [Connection to modern life and technology]
</section>

<section class="philosophical-questions">
  <h2>Questions to Ponder</h2>
  <ul>
    <li>[A question about the ethics of using this knowledge]</li>
    <li>[A question about choices and trade-offs]</li>
    <li>[A question connecting to personal values or society]</li>
  </ul>
</section>

<section class="summary">
  <h2>Key Takeaways</h2>
  <ul>
    <li>[Main concept 1]</li>
    <li>[Main concept 2]</li>
    <li>[Main concept 3]</li>
  </ul>
</section>

Format as JSON:
{
  "title": "Engaging title",
  "content": "Full HTML content as structured above",
  "estimated_time_minutes": 20,
  "difficulty_level": "beginner|intermediate|advanced"
}`

    try {
      this.stats.apiCalls++
      
      const response = await anthropic.messages.create({
        model: "claude-3-haiku-20240307",
        max_tokens: 4000,
        temperature: 0.7,
        messages: [{ role: "user", content: prompt }]
      })
      
      let responseText = response.content[0].text
      
      // Try to parse as JSON
      try {
        // Sometimes the response has JSON embedded in the text
        // Try to extract it if it's there
        const jsonMatch = responseText.match(/\{[\s\S]*\}/)
        if (jsonMatch) {
          responseText = jsonMatch[0]
        }
        
        const contentData = JSON.parse(responseText)
        return {
          title: contentData.title || node.name,
          content: contentData.content,
          estimated_time_minutes: contentData.estimated_time_minutes || 20,
          difficulty_level: contentData.difficulty_level || 'intermediate',
          images: null
        }
      } catch (parseError) {
        // If JSON parsing fails, create basic structure
        await this.logProgress(`JSON parse error for ${node.name}, using fallback`)
        return {
          title: node.name,
          content: `<div class="generated-content">${responseText}</div>`,
          estimated_time_minutes: 20,
          difficulty_level: 'intermediate',
          images: null
        }
      }
    } catch (error) {
      await this.logProgress(`Error generating content for ${node.name}: ${error.message}`)
      throw error
    }
  }

  async generateQuestions(node, content) {
    const prompt = `Based on the following learning content about "${content.title}", generate 25 multiple choice questions.

Content Summary:
${content.content.substring(0, 1500)}...

Requirements:
1. Create questions testing different cognitive levels
2. Mix difficulty: 30% easy, 50% medium, 20% hard
3. Each question has exactly 4 options
4. Include diverse question types
5. Detailed explanations for all answers

Format as JSON:
{
  "questions": [
    {
      "question_text": "Question?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0,
      "explanation": "Detailed explanation",
      "difficulty": "easy|medium|hard"
    }
  ]
}`

    try {
      this.stats.apiCalls++
      
      const response = await anthropic.messages.create({
        model: "claude-3-haiku-20240307",
        max_tokens: 4000,
        temperature: 0.8,
        messages: [{ role: "user", content: prompt }]
      })
      
      const responseText = response.content[0].text
      
      try {
        const questionsData = JSON.parse(responseText)
        return questionsData.questions || []
      } catch (parseError) {
        await this.logProgress(`Failed to parse questions for ${node.name}`)
        return []
      }
    } catch (error) {
      await this.logProgress(`Error generating questions for ${node.name}: ${error.message}`)
      return []
    }
  }

  async saveForReview(node, content, questions) {
    const reviewData = {
      nodeId: node.id,
      nodeName: node.name,
      content: content,
      questions: questions,
      timestamp: new Date().toISOString()
    }
    
    // Load existing review file or create new
    let existingReviews = []
    try {
      const reviewFileContent = await fs.readFile(CONFIG.reviewFile, 'utf-8')
      existingReviews = JSON.parse(reviewFileContent)
    } catch (error) {
      // File doesn't exist yet
    }
    
    existingReviews.push(reviewData)
    
    await fs.writeFile(CONFIG.reviewFile, JSON.stringify(existingReviews, null, 2))
    await this.logProgress(`Saved content for review: ${node.name}`)
  }

  async processNode(node) {
    try {
      await this.logProgress(`Processing: ${node.name}`)
      
      // Generate content
      const content = await this.generateLearningContent(node)
      
      // Wait before next API call
      await new Promise(resolve => setTimeout(resolve, CONFIG.apiDelay))
      
      // Generate questions
      const questions = await this.generateQuestions(node, content)
      
      // Save for review
      await this.saveForReview(node, content, questions)
      
      // Mark as processed
      this.processedNodeIds.push(node.id)
      this.stats.processedNodes++
      this.stats.successfulContent++
      
      // Save checkpoint
      await this.saveCheckpoint()
      
      return { content, questions }
    } catch (error) {
      this.stats.failedNodes++
      await this.logProgress(`Failed to process ${node.name}: ${error.message}`)
      throw error
    }
  }

  async run() {
    try {
      await this.initialize()
      
      // Load math nodes
      const mathNodes = await this.loadMathNodes()
      this.stats.totalNodes = mathNodes.length
      
      if (mathNodes.length === 0) {
        await this.logProgress('No math nodes need processing')
        return
      }
      
      // Show first few nodes that will be processed
      await this.logProgress('\nFirst nodes to process:')
      mathNodes.slice(0, 5).forEach(node => {
        console.log(`  - ${node.name}`)
      })
      
      // Process first 3 nodes for review
      const nodesToProcess = mathNodes.slice(0, 3)
      await this.logProgress(`\nProcessing first ${nodesToProcess.length} nodes for review...`)
      
      for (const node of nodesToProcess) {
        await this.processNode(node)
        await new Promise(resolve => setTimeout(resolve, CONFIG.apiDelay))
      }
      
      // Final stats
      const duration = (new Date() - this.stats.startTime) / 1000 / 60
      await this.logProgress(`
=== Processing Complete ===
Total nodes found: ${this.stats.totalNodes}
Processed: ${this.stats.processedNodes}
Successful: ${this.stats.successfulContent}
Failed: ${this.stats.failedNodes}
Duration: ${duration.toFixed(2)} minutes
API Calls: ${this.stats.apiCalls}

Review file saved to: ${CONFIG.reviewFile}

NEXT STEPS:
1. Review the generated content in: ${CONFIG.reviewFile}
2. Once approved, run: node scripts/content_generation/insert_reviewed_content.js
3. To process more nodes, update the slice range in the script
`)
      
    } catch (error) {
      await this.logProgress(`Fatal error: ${error.message}`)
      console.error(error)
    }
  }
}

// Main execution
if (require.main === module) {
  const generator = new MathContentGenerator()
  generator.run().catch(console.error)
}

module.exports = MathContentGenerator