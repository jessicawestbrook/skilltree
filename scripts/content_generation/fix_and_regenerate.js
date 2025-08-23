/**
 * Fix HTML formatting and regenerate content with age-appropriate difficulty
 */

const fs = require('fs').promises
const path = require('path')
const Anthropic = require('@anthropic-ai/sdk')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '../..', '.env.local') })

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

// Helper to determine target age group based on topic
function getTargetAudience(nodeName) {
  const nameLower = nodeName.toLowerCase()
  
  // Elementary school topics (ages 5-11)
  const elementaryKeywords = [
    'counting', 'addition', 'subtraction', 'shapes', 'colors', 'basic',
    'simple', 'numbers 1-', 'money counting', 'telling time', 'measurement'
  ]
  
  // Middle school topics (ages 11-14)
  const middleKeywords = [
    'fractions', 'decimals', 'percentages', 'pre-algebra', 'geometry',
    'ratios', 'proportions', 'integers', 'equations'
  ]
  
  // High school topics (ages 14-18)
  const highKeywords = [
    'algebra', 'trigonometry', 'calculus', 'statistics', 'probability',
    'functions', 'logarithms', 'matrices', 'vectors'
  ]
  
  for (const keyword of elementaryKeywords) {
    if (nameLower.includes(keyword)) {
      return { level: 'elementary', age: '6-11 years old', grade: '1st-5th grade' }
    }
  }
  
  for (const keyword of middleKeywords) {
    if (nameLower.includes(keyword)) {
      return { level: 'middle', age: '11-14 years old', grade: '6th-8th grade' }
    }
  }
  
  for (const keyword of highKeywords) {
    if (nameLower.includes(keyword)) {
      return { level: 'high', age: '14-18 years old', grade: '9th-12th grade' }
    }
  }
  
  // Default to middle school
  return { level: 'middle', age: '11-14 years old', grade: '6th-8th grade' }
}

async function generateAgeAppropriateContent(node) {
  const audience = getTargetAudience(node.name)
  
  console.log(`Generating ${audience.level} level content for: ${node.name}`)
  console.log(`Target audience: ${audience.age} (${audience.grade})`)
  
  let prompt = ''
  
  if (audience.level === 'elementary') {
    prompt = `Generate fun, simple learning content about "${node.name}" for elementary school children (${audience.age}).

IMPORTANT: 
- Use very simple language that young children can understand
- Include a fun story with characters kids can relate to
- Make it feel like a game or adventure
- Use short sentences and paragraphs
- Include lots of examples with pictures they'd recognize (toys, candy, animals)
- Make math feel fun and not scary

Structure the content as follows:

<h1>[Fun, Exciting Title]</h1>

<div class="story-intro">
  <h2>Let's Start Our Adventure!</h2>
  <p>[A short, fun story featuring a child character or friendly animal learning about this topic]</p>
  <p>[Make it relatable - maybe about buying toys, sharing candy, or helping friends]</p>
</div>

<div class="learn-together">
  <h2>Let's Learn Together!</h2>
  <p>[Explain the concept in the simplest way possible]</p>
  <p>[Use examples from their daily life]</p>
  <p>[Make it feel like playing, not studying]</p>
</div>

<div class="practice-time">
  <h2>Practice Time - Let's Play!</h2>
  <h3>Game 1:</h3>
  <p>[A simple, fun example - like counting toys or cookies]</p>
  
  <h3>Game 2:</h3>
  <p>[Another playful example]</p>
</div>

<div class="why-cool">
  <h2>Why This Is Super Cool!</h2>
  <p>[Explain why this skill is awesome in kid-friendly terms]</p>
  <p>[Maybe they can help mom at the store, or impress their friends]</p>
</div>

<div class="remember">
  <h2>Things to Remember</h2>
  <ul>
    <li>[Simple point 1]</li>
    <li>[Simple point 2]</li>
    <li>[Simple point 3]</li>
  </ul>
</div>

Return as clean JSON (no escape characters):
{
  "title": "Fun title",
  "content": "HTML content without escaped quotes or newlines",
  "estimated_time_minutes": 10,
  "difficulty_level": "beginner"
}`
  } else if (audience.level === 'middle') {
    prompt = `Generate engaging learning content about "${node.name}" for middle school students (${audience.age}).

Create content that:
- Uses clear, friendly language appropriate for pre-teens
- Includes interesting real-world connections
- Has some fun elements but also teaches seriously
- Connects to their interests (sports, games, social media, etc.)

[Rest of standard prompt...]`
  } else {
    prompt = `Generate comprehensive learning content about "${node.name}" for high school students (${audience.age}).

Create content that:
- Uses mature but accessible language
- Includes deeper mathematical concepts
- Connects to college and career preparation
- Includes historical context and applications

[Rest of standard prompt...]`
  }
  
  try {
    const response = await anthropic.messages.create({
      model: "claude-3-haiku-20240307",
      max_tokens: 3000,
      temperature: 0.7,
      messages: [{ role: "user", content: prompt }]
    })
    
    let responseText = response.content[0].text
    
    // Clean up the response
    responseText = responseText
      .replace(/\\n/g, '')  // Remove literal \n
      .replace(/\\"/g, '"')  // Fix escaped quotes
      .replace(/\\\\/g, '\\')  // Fix double escapes
    
    // Try to parse as JSON
    try {
      const jsonMatch = responseText.match(/\{[\s\S]*\}/)
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0])
        return {
          title: parsed.title,
          content: parsed.content,
          estimated_time_minutes: parsed.estimated_time_minutes || 10,
          difficulty_level: parsed.difficulty_level || 'beginner',
          target_audience: audience
        }
      }
    } catch (e) {
      console.log('Could not parse JSON, using raw content')
    }
    
    return {
      title: node.name,
      content: responseText,
      estimated_time_minutes: 10,
      difficulty_level: 'beginner',
      target_audience: audience
    }
  } catch (error) {
    console.error('Error generating content:', error.message)
    throw error
  }
}

async function fixExistingHTML() {
  console.log('Fixing HTML formatting issues...\n')
  
  const inputFile = path.join(__dirname, 'output', 'math_content', 'content_for_review.json')
  const outputDir = path.join(__dirname, 'output', 'math_content', 'fixed')
  const outputFile = path.join(outputDir, 'fixed_content.json')
  const htmlFile = path.join(outputDir, 'preview.html')
  
  await fs.mkdir(outputDir, { recursive: true })
  
  // Read existing content
  const data = JSON.parse(await fs.readFile(inputFile, 'utf-8'))
  
  const fixed = []
  
  for (const item of data) {
    // Extract and clean the content
    let contentStr = item.content.content || ''
    
    // Remove the wrapper div
    contentStr = contentStr.replace(/<div class="generated-content">/, '').replace(/<\/div>$/, '')
    
    // Try to extract JSON
    const jsonMatch = contentStr.match(/\{[\s\S]*\}/)
    if (jsonMatch) {
      try {
        // Parse and clean
        let jsonStr = jsonMatch[0]
        // Fix common issues
        jsonStr = jsonStr.replace(/\\n/g, ' ')  // Replace \n with space
        jsonStr = jsonStr.replace(/\\"/g, '"')   // Fix escaped quotes in JSON
        jsonStr = jsonStr.replace(/\s+/g, ' ')  // Collapse multiple spaces
        
        const parsed = JSON.parse(jsonStr)
        
        // Clean the HTML content
        if (parsed.content) {
          parsed.content = parsed.content
            .replace(/\\n/g, '')      // Remove literal \n
            .replace(/\\"/g, '"')     // Fix escaped quotes
            .replace(/\\\//g, '/')    // Fix escaped slashes
            .trim()
        }
        
        fixed.push({
          nodeId: item.nodeId,
          nodeName: item.nodeName,
          content: parsed,
          questions: item.questions || []
        })
      } catch (e) {
        console.log(`Could not fix ${item.nodeName}:`, e.message)
      }
    }
  }
  
  // Save fixed content
  await fs.writeFile(outputFile, JSON.stringify(fixed, null, 2))
  
  // Create clean HTML preview
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math Content Preview - Fixed</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .content-card {
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2e7d32; }
        h2 { color: #558b2f; margin-top: 25px; }
        h3 { color: #666; margin-top: 20px; }
        section {
            margin: 20px 0;
            padding: 15px;
            background: #f9f9f9;
            border-left: 4px solid #667eea;
            border-radius: 5px;
        }
        .story-intro, .introduction { 
            background: #e8f5e9; 
            border-left-color: #4caf50;
        }
        .philosophical-questions {
            background: #f3e5f5;
            border-left-color: #9c27b0;
        }
        ul, ol { margin: 15px 0; padding-left: 30px; }
        li { margin-bottom: 8px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Math Learning Content</h1>
        <p>Fixed and Formatted Version</p>
    </div>
    
    ${fixed.map(item => `
        <div class="content-card">
            <h2>${item.nodeName}</h2>
            <div class="meta">
                <small>📖 ${item.content.estimated_time_minutes || 20} minutes | 
                🎯 ${item.content.difficulty_level || 'intermediate'}</small>
            </div>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
            ${item.content.content || '<p>No content available</p>'}
        </div>
    `).join('')}
</body>
</html>`
  
  await fs.writeFile(htmlFile, html)
  
  console.log('Fixed content saved to:', outputFile)
  console.log('HTML preview saved to:', htmlFile)
  
  return fixed
}

async function regenerateWithCorrectAudience() {
  console.log('\nRegenerating content with age-appropriate difficulty...\n')
  
  const { createClient } = require('@supabase/supabase-js')
  const supabase = createClient(
    process.env.REACT_APP_SUPABASE_URL,
    process.env.REACT_APP_SUPABASE_ANON_KEY
  )
  
  // Get Money Counting node
  const { data: nodes } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('name', 'Money Counting')
    .single()
  
  if (nodes) {
    const content = await generateAgeAppropriateContent(nodes)
    
    // Save the new content
    const outputDir = path.join(__dirname, 'output', 'math_content', 'age_appropriate')
    await fs.mkdir(outputDir, { recursive: true })
    
    const result = {
      nodeId: nodes.id,
      nodeName: nodes.name,
      content: content,
      questions: []  // Will generate appropriate questions later
    }
    
    await fs.writeFile(
      path.join(outputDir, 'money_counting_elementary.json'),
      JSON.stringify(result, null, 2)
    )
    
    // Create preview HTML
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${content.title}</title>
    <style>
        body {
            font-family: 'Comic Sans MS', 'Arial', sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(to bottom, #e3f2fd, #f5f5f5);
        }
        h1 {
            color: #4caf50;
            text-align: center;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        h2 {
            color: #ff6b35;
            margin-top: 30px;
            font-size: 1.8em;
        }
        .content-wrapper {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .story-intro, .learn-together {
            background: #fff3e0;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border: 2px solid #ffb74d;
        }
        .practice-time {
            background: #e8f5e9;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border: 2px solid #66bb6a;
        }
        .why-cool {
            background: #f3e5f5;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border: 2px solid #ba68c8;
        }
        .remember {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border: 2px solid #42a5f5;
        }
        p {
            font-size: 1.2em;
            margin: 15px 0;
        }
        ul {
            font-size: 1.1em;
        }
        li {
            margin: 10px 0;
        }
        .audience-info {
            background: #ffeb3b;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="content-wrapper">
        <div class="audience-info">
            📚 For ${content.target_audience.age} (${content.target_audience.grade})
        </div>
        ${content.content}
    </div>
</body>
</html>`
    
    await fs.writeFile(
      path.join(outputDir, 'money_counting_preview.html'),
      html
    )
    
    console.log('\nAge-appropriate content generated!')
    console.log('Preview saved to:', path.join(outputDir, 'money_counting_preview.html'))
    
    return result
  }
}

async function main() {
  console.log('Content Fixing and Regeneration Tool')
  console.log('=====================================\n')
  
  // First fix the existing content
  await fixExistingHTML()
  
  console.log('\n' + '='.repeat(50))
  
  // Then regenerate with age-appropriate content
  await regenerateWithCorrectAudience()
  
  console.log('\n✅ Complete! Check the output folders for:')
  console.log('1. Fixed original content: output/math_content/fixed/')
  console.log('2. Age-appropriate content: output/math_content/age_appropriate/')
}

main().catch(console.error)