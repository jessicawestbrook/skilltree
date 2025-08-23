/**
 * Test script to generate content for a single math node
 * ========================================================
 * 
 * This script tests the content generation for one specific node
 * to verify the process works correctly before batch processing.
 */

const { createClient } = require('@supabase/supabase-js')
const Anthropic = require('@anthropic-ai/sdk')
const fs = require('fs').promises
const path = require('path')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '../..', '.env.local') })

// Check for API key
if (!process.env.ANTHROPIC_API_KEY) {
  console.error(`
ERROR: ANTHROPIC_API_KEY not found in environment variables.
Please add it to your .env.local file:
ANTHROPIC_API_KEY=your_api_key_here
`)
  process.exit(1)
}

// Initialize clients
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

async function findSimpleMathNode() {
  console.log('Finding a simple math node to test...\n')
  
  // Look for basic counting or addition nodes
  const basicTopics = ['counting 1-10', 'counting', 'addition', 'basic math', 'numbers']
  
  for (const topic of basicTopics) {
    const { data, error } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .ilike('name', `%${topic}%`)
      .limit(1)
    
    if (data && data.length > 0) {
      // Check if it's a leaf node (no children)
      const { data: children } = await supabase
        .from('skill_tree_nodes')
        .select('id')
        .eq('parent_id', data[0].id)
        .limit(1)
      
      if (!children || children.length === 0) {
        return data[0]
      }
    }
  }
  
  // If no specific topic found, get any math leaf node
  const { data } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .ilike('name', '%math%')
    .limit(10)
  
  // Find a leaf node
  for (const node of data || []) {
    const { data: children } = await supabase
      .from('skill_tree_nodes')
      .select('id')
      .eq('parent_id', node.id)
      .limit(1)
    
    if (!children || children.length === 0) {
      return node
    }
  }
  
  return null
}

async function generateContentForNode(node) {
  console.log(`Generating content for: ${node.name}\n`)
  
  const prompt = `Generate a short, engaging learning module about "${node.name}" for students.

Create a simple, clear explanation that includes:
1. An interesting introduction or story
2. The main concept explained simply
3. A practical example
4. Why this is useful to know

Format as JSON:
{
  "title": "Engaging title",
  "content": "<h1>Title</h1><p>Introduction...</p><h2>The Concept</h2><p>Explanation...</p><h2>Example</h2><p>Example...</p><h2>Why It Matters</h2><p>Application...</p>",
  "estimated_time_minutes": 10,
  "difficulty_level": "beginner"
}`

  try {
    const response = await anthropic.messages.create({
      model: "claude-3-haiku-20240307",
      max_tokens: 2000,
      temperature: 0.7,
      messages: [{ role: "user", content: prompt }]
    })
    
    const responseText = response.content[0].text
    console.log('Response received. Parsing...\n')
    
    try {
      const content = JSON.parse(responseText)
      return content
    } catch (parseError) {
      console.log('Could not parse as JSON, using raw response')
      return {
        title: node.name,
        content: responseText,
        estimated_time_minutes: 10,
        difficulty_level: 'beginner'
      }
    }
  } catch (error) {
    console.error('API Error:', error.message)
    throw error
  }
}

async function generateQuestionsForContent(node, content) {
  console.log('Generating questions...\n')
  
  const prompt = `Based on this learning content about "${node.name}", create 5 multiple choice questions.

Each question should:
- Test understanding of the content
- Have 4 options
- Include an explanation

Format as JSON:
{
  "questions": [
    {
      "question_text": "Question?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0,
      "explanation": "Why this is correct",
      "difficulty": "easy"
    }
  ]
}`

  try {
    const response = await anthropic.messages.create({
      model: "claude-3-haiku-20240307",
      max_tokens: 2000,
      temperature: 0.8,
      messages: [{ role: "user", content: prompt }]
    })
    
    const responseText = response.content[0].text
    
    try {
      const data = JSON.parse(responseText)
      return data.questions || []
    } catch (parseError) {
      console.log('Could not parse questions as JSON')
      return []
    }
  } catch (error) {
    console.error('API Error:', error.message)
    throw error
  }
}

async function saveTestOutput(node, content, questions) {
  const outputDir = path.join(__dirname, 'output', 'test_content')
  await fs.mkdir(outputDir, { recursive: true })
  
  const outputFile = path.join(outputDir, 'test_output.json')
  const htmlFile = path.join(outputDir, 'test_content.html')
  
  const output = {
    node: {
      id: node.id,
      name: node.name
    },
    content: content,
    questions: questions,
    timestamp: new Date().toISOString()
  }
  
  await fs.writeFile(outputFile, JSON.stringify(output, null, 2))
  
  // Create HTML preview
  const html = `
<!DOCTYPE html>
<html>
<head>
    <title>${content.title}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #2e7d32; }
        h2 { color: #558b2f; margin-top: 30px; }
        .question { background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .options { margin-left: 20px; }
        .explanation { color: #666; font-style: italic; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="content">
        ${content.content}
    </div>
    
    <h2>Practice Questions</h2>
    ${questions.map((q, i) => `
        <div class="question">
            <strong>Question ${i + 1}:</strong> ${q.question_text}
            <div class="options">
                ${q.options.map((opt, j) => `${j === q.correct_answer ? '✓' : ''} ${opt}<br>`).join('')}
            </div>
            <div class="explanation">
                <strong>Explanation:</strong> ${q.explanation}
            </div>
        </div>
    `).join('')}
</body>
</html>
  `
  
  await fs.writeFile(htmlFile, html)
  
  console.log(`\nOutput saved to:`)
  console.log(`  JSON: ${outputFile}`)
  console.log(`  HTML: ${htmlFile}`)
}

async function main() {
  try {
    console.log('Math Content Generation Test')
    console.log('============================\n')
    
    // Find a node to test
    const node = await findSimpleMathNode()
    
    if (!node) {
      console.log('No suitable math node found for testing')
      return
    }
    
    console.log(`Found node: ${node.name}`)
    console.log(`Node ID: ${node.id}\n`)
    
    // Generate content
    const content = await generateContentForNode(node)
    console.log('✓ Content generated\n')
    
    // Generate questions
    const questions = await generateQuestionsForContent(node, content)
    console.log(`✓ ${questions.length} questions generated\n`)
    
    // Save output
    await saveTestOutput(node, content, questions)
    
    console.log('\n=== TEST COMPLETE ===')
    console.log('Review the generated content in the output/test_content directory')
    console.log('If satisfied, run the full batch generator')
    
  } catch (error) {
    console.error('Test failed:', error)
  }
}

main()