/**
 * Enhanced Math Content Generator with Educational Philosophy
 * =============================================================
 * 
 * This script generates comprehensive learning content for math topics
 * incorporating storytelling, philosophical questions, and engaging narratives
 * based on Kieran Egan's educational philosophy.
 * 
 * Features:
 * - HTML-formatted content for rich presentation
 * - Story-driven mathematical concepts
 * - Historical context and real-world applications
 * - Philosophical questions to engage deeper thinking
 * - 20-50 questions per topic with detailed explanations
 * - Progressive difficulty from basic to advanced math
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

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

// Configuration
const CONFIG = {
  batchSize: 5,
  apiDelay: 5000, // 5 seconds between API calls
  maxRetries: 3,
  outputDir: path.join(__dirname, 'output', 'math_content'),
  checkpointFile: path.join(__dirname, 'output', 'math_content', 'checkpoint.json'),
  progressFile: path.join(__dirname, 'output', 'math_content', 'progress.log'),
  reviewFile: path.join(__dirname, 'output', 'math_content', 'content_for_review.json')
}

// Difficulty ordering for math topics (from easiest to hardest)
const MATH_DIFFICULTY_ORDER = [
  'counting', 'numbers', 'basic_arithmetic', 'addition', 'subtraction',
  'multiplication', 'division', 'fractions', 'decimals', 'percentages',
  'basic_algebra', 'geometry', 'measurement', 'data_analysis', 'probability',
  'pre_algebra', 'algebra_1', 'algebra_2', 'trigonometry', 'pre_calculus',
  'calculus', 'statistics', 'linear_algebra', 'differential_equations',
  'abstract_algebra', 'topology', 'number_theory'
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
    
    console.log('Math Content Generator initialized')
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

  async loadMathNodes() {
    await this.logProgress('Loading math nodes from database...')
    
    let allNodes = []
    let from = 0
    const batchSize = 1000
    
    while (true) {
      const { data, error } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .or('learning_area.eq.Mathematics,path.ilike.%mathematics%,path.ilike.%math%')
        .range(from, from + batchSize - 1)
      
      if (error) {
        throw new Error(`Database error: ${error.message}`)
      }
      
      if (!data || data.length === 0) break
      
      allNodes = allNodes.concat(data)
      
      if (data.length < batchSize) break
      from += batchSize
    }
    
    // Filter for leaf nodes that need content
    const leafNodes = allNodes.filter(node => 
      (node.is_menu_leaf || !node.children || node.children.length === 0) &&
      !node.has_learning_content &&
      !this.processedNodeIds.includes(node.id)
    )
    
    // Sort by difficulty order
    const sortedNodes = this.sortNodesByDifficulty(leafNodes)
    
    await this.logProgress(`Found ${sortedNodes.length} math nodes needing content`)
    return sortedNodes
  }

  sortNodesByDifficulty(nodes) {
    return nodes.sort((a, b) => {
      const aName = a.name.toLowerCase()
      const bName = b.name.toLowerCase()
      const aPath = a.path.toLowerCase()
      const bPath = b.path.toLowerCase()
      
      // Find difficulty index
      let aIndex = MATH_DIFFICULTY_ORDER.length
      let bIndex = MATH_DIFFICULTY_ORDER.length
      
      for (let i = 0; i < MATH_DIFFICULTY_ORDER.length; i++) {
        const difficulty = MATH_DIFFICULTY_ORDER[i]
        if (aName.includes(difficulty) || aPath.includes(difficulty)) {
          aIndex = Math.min(aIndex, i)
        }
        if (bName.includes(difficulty) || bPath.includes(difficulty)) {
          bIndex = Math.min(bIndex, i)
        }
      }
      
      return aIndex - bIndex
    })
  }

  async generateLearningContent(node) {
    const prompt = `Generate comprehensive, engaging learning content for the mathematical topic: "${node.name}"

Context:
- Learning Path: ${node.path}
- Target Audience: Varied (adapt explanations for different levels)
- Content Length: 10-30 minutes of reading/study time
- Format: HTML with rich formatting

IMPORTANT: Follow Kieran Egan's educational philosophy as described in "The Lost Tools of Learning":
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
  <h2>Understanding [Topic]</h2>
  [Clear explanations with visual descriptions]
  [Use analogies and real-world examples]
  [Build from simple to complex]
  [Include mathematical notation where appropriate using HTML entities or LaTeX-style formatting]
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

Additional Requirements:
- Use vivid, specific language (not generic academic prose)
- Include sensory details in stories
- Make abstract concepts concrete through narrative
- Estimated reading time: 15-25 minutes
- Difficulty level: Automatically determine based on topic complexity

Format as JSON:
{
  "title": "Engaging title",
  "content": "Full HTML content as structured above",
  "estimated_time_minutes": 20,
  "difficulty_level": "beginner|intermediate|advanced",
  "key_concepts": ["concept1", "concept2", "concept3"],
  "philosophical_questions": ["question1", "question2", "question3"]
}`

    try {
      this.stats.apiCalls++
      
      const response = await anthropic.messages.create({
        model: "claude-3-opus-20240229",
        max_tokens: 4000,
        temperature: 0.7,
        messages: [{ role: "user", content: prompt }]
      })
      
      const responseText = response.content[0].text
      
      // Try to parse as JSON
      try {
        const contentData = JSON.parse(responseText)
        return {
          title: contentData.title || node.name,
          content: contentData.content,
          estimated_time_minutes: contentData.estimated_time_minutes || 20,
          difficulty_level: contentData.difficulty_level || 'intermediate',
          images: null, // Will be added later if needed
          key_concepts: contentData.key_concepts,
          philosophical_questions: contentData.philosophical_questions
        }
      } catch (parseError) {
        // If JSON parsing fails, extract content
        await this.logProgress(`JSON parse error for ${node.name}, attempting to extract content`)
        return {
          title: node.name,
          content: responseText,
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
    const prompt = `Based on the following learning content about "${content.title}", generate 25-30 multiple choice questions.

Learning Content Summary:
${content.content.substring(0, 2000)}...

Requirements:
1. Create questions that test understanding at different cognitive levels:
   - 30% Knowledge/Recall questions
   - 40% Comprehension/Application questions  
   - 30% Analysis/Synthesis questions
2. Mix difficulty levels:
   - 30% Easy (basic recall and simple applications)
   - 50% Medium (require understanding and problem-solving)
   - 20% Hard (complex reasoning or multi-step problems)
3. Each question must have exactly 4 options
4. Only one correct answer per question
5. Include questions about:
   - The historical context and human stories
   - Core mathematical concepts
   - Real-world applications
   - The philosophical questions raised
6. Explanations should:
   - Explain why the correct answer is right
   - Explain why each incorrect option is wrong
   - Provide additional context or learning points
   - Reference the content where applicable

Question Types to Include:
- Conceptual understanding questions
- Problem-solving questions (keep calculations simple)
- Historical/contextual questions
- Application questions
- "What if" scenario questions
- Questions about the philosophical implications

Format as JSON:
{
  "questions": [
    {
      "question_text": "Clear, specific question?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Detailed explanation with educational value",
      "difficulty": "easy|medium|hard",
      "cognitive_level": "recall|comprehension|application|analysis",
      "topic_area": "history|concept|application|philosophy"
    }
  ]
}

Generate exactly 25 high-quality, diverse questions.`

    try {
      this.stats.apiCalls++
      
      const response = await anthropic.messages.create({
        model: "claude-3-opus-20240229",
        max_tokens: 6000,
        temperature: 0.8,
        messages: [{ role: "user", content: prompt }]
      })
      
      const responseText = response.content[0].text
      
      try {
        const questionsData = JSON.parse(responseText)
        return questionsData.questions || []
      } catch (parseError) {
        await this.logProgress(`Failed to parse questions for ${node.name}: ${parseError.message}`)
        return []
      }
    } catch (error) {
      await this.logProgress(`Error generating questions for ${node.name}: ${error.message}`)
      throw error
    }
  }

  async saveContentToDatabase(node, content, questions) {
    try {
      // Save learning content
      const contentData = {
        title: content.title,
        content: content.content,
        estimated_time_minutes: content.estimated_time_minutes,
        difficulty_level: content.difficulty_level,
        images: content.images,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
      
      const { data: contentResult, error: contentError } = await supabase
        .from('learning_content')
        .insert(contentData)
        .select()
        .single()
      
      if (contentError) throw contentError
      
      const contentId = contentResult.id
      
      // Save questions
      const questionIds = []
      for (const question of questions) {
        const questionId = uuidv4()
        const questionData = {
          id: questionId,
          question_text: question.question_text,
          options: question.options,
          correct_answer: question.correct_answer,
          explanation: question.explanation,
          difficulty: question.difficulty,
          created_at: new Date().toISOString()
        }
        
        const { error: questionError } = await supabase
          .from('questions')
          .insert(questionData)
        
        if (!questionError) {
          questionIds.push(questionId)
        }
      }
      
      // Update learning content with question IDs
      await supabase
        .from('learning_content')
        .update({ question_ids: questionIds })
        .eq('id', contentId)
      
      // Update skill tree node
      await supabase
        .from('skill_tree_nodes')
        .update({
          has_learning_content: true,
          learning_content_ids: [contentId],
          updated_at: new Date().toISOString()
        })
        .eq('id', node.id)
      
      this.stats.successfulContent++
      await this.logProgress(`Successfully saved content and ${questionIds.length} questions for ${node.name}`)
      
      return { contentId, questionIds }
    } catch (error) {
      await this.logProgress(`Database error for ${node.name}: ${error.message}`)
      throw error
    }
  }

  async saveForReview(node, content, questions) {
    const reviewData = {
      nodeId: node.id,
      nodeName: node.name,
      nodePath: node.path,
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
      await this.logProgress(`Processing: ${node.name} (${node.path})`)
      
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
      
      // Save checkpoint every 5 nodes
      if (this.stats.processedNodes % 5 === 0) {
        await this.saveCheckpoint()
      }
      
      return { content, questions }
    } catch (error) {
      this.stats.failedNodes++
      await this.logProgress(`Failed to process ${node.name}: ${error.message}`)
      throw error
    }
  }

  async processBatch(nodes, batchNum, totalBatches) {
    await this.logProgress(`Processing batch ${batchNum}/${totalBatches} (${nodes.length} nodes)`)
    
    for (const node of nodes) {
      try {
        await this.processNode(node)
        
        // Add delay between nodes
        await new Promise(resolve => setTimeout(resolve, CONFIG.apiDelay))
      } catch (error) {
        await this.logProgress(`Error in batch ${batchNum}, node ${node.name}: ${error.message}`)
        // Continue with next node
      }
    }
    
    await this.saveCheckpoint()
  }

  async estimateCosts(nodeCount) {
    // Claude-3 Opus pricing
    const inputCostPer1k = 0.015  // $15 per 1M tokens
    const outputCostPer1k = 0.075  // $75 per 1M tokens
    
    // Estimates per node
    const contentInputTokens = 2000   // Prompt
    const contentOutputTokens = 3000  // Content generation
    const questionsInputTokens = 3000 // Prompt + content
    const questionsOutputTokens = 5000 // 25-30 questions
    
    const totalInputTokens = nodeCount * (contentInputTokens + questionsInputTokens)
    const totalOutputTokens = nodeCount * (contentOutputTokens + questionsOutputTokens)
    
    const inputCost = (totalInputTokens / 1000) * inputCostPer1k
    const outputCost = (totalOutputTokens / 1000) * outputCostPer1k
    const totalCost = inputCost + outputCost
    
    return {
      inputCost,
      outputCost,
      totalCost,
      totalInputTokens,
      totalOutputTokens
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
      
      // Estimate costs
      const costs = await this.estimateCosts(mathNodes.length)
      await this.logProgress(`Estimated costs: $${costs.totalCost.toFixed(2)} (Input: $${costs.inputCost.toFixed(2)}, Output: $${costs.outputCost.toFixed(2)})`)
      
      // Process first 3 nodes for review
      const nodesToProcess = mathNodes.slice(0, 3)
      await this.logProgress(`Processing first ${nodesToProcess.length} nodes for review`)
      
      for (const node of nodesToProcess) {
        await this.processNode(node)
        await new Promise(resolve => setTimeout(resolve, CONFIG.apiDelay))
      }
      
      // Final stats
      const duration = (new Date() - this.stats.startTime) / 1000 / 60
      await this.logProgress(`
=== Processing Complete ===
Total nodes: ${this.stats.totalNodes}
Processed: ${this.stats.processedNodes}
Successful: ${this.stats.successfulContent}
Failed: ${this.stats.failedNodes}
Duration: ${duration.toFixed(2)} minutes
API Calls: ${this.stats.apiCalls}

Review file saved to: ${CONFIG.reviewFile}
Please review the generated content before proceeding with full batch processing.
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