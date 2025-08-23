/**
 * Script to clean up generated content and create HTML preview
 * =============================================================
 */

const fs = require('fs').promises
const path = require('path')

const INPUT_FILE = path.join(__dirname, 'output', 'math_content', 'content_for_review.json')
const OUTPUT_DIR = path.join(__dirname, 'output', 'math_content', 'cleaned')
const CLEANED_JSON = path.join(OUTPUT_DIR, 'cleaned_content.json')
const HTML_PREVIEW = path.join(OUTPUT_DIR, 'preview.html')

async function cleanContent() {
  console.log('Cleaning generated content...\n')
  
  // Create output directory
  await fs.mkdir(OUTPUT_DIR, { recursive: true })
  
  // Load the generated content
  const rawContent = await fs.readFile(INPUT_FILE, 'utf-8')
  const items = JSON.parse(rawContent)
  
  const cleanedItems = []
  
  for (const item of items) {
    console.log(`Processing: ${item.nodeName}`)
    
    // Extract the actual content from the nested JSON
    let cleanedContent = item.content
    
    // Check if content has embedded JSON
    if (cleanedContent.content && typeof cleanedContent.content === 'string') {
      // Look for JSON inside the content string
      const contentStr = cleanedContent.content
      
      if (contentStr.includes('"content":')) {
        try {
          // Extract JSON from the wrapper
          const jsonMatch = contentStr.match(/\{[\s\S]*\}/)
          if (jsonMatch) {
            const extracted = JSON.parse(jsonMatch[0])
            cleanedContent = {
              title: extracted.title || cleanedContent.title,
              content: extracted.content,
              estimated_time_minutes: extracted.estimated_time_minutes || 20,
              difficulty_level: extracted.difficulty_level || 'intermediate'
            }
            console.log('  ✓ Extracted embedded content')
          }
        } catch (e) {
          console.log('  ⚠ Could not extract embedded JSON, using as-is')
        }
      }
    }
    
    // Create cleaned item
    const cleanedItem = {
      nodeId: item.nodeId,
      nodeName: item.nodeName,
      content: cleanedContent,
      questions: item.questions || [],
      timestamp: item.timestamp
    }
    
    cleanedItems.push(cleanedItem)
  }
  
  // Save cleaned JSON
  await fs.writeFile(CLEANED_JSON, JSON.stringify(cleanedItems, null, 2))
  console.log(`\n✓ Cleaned content saved to: ${CLEANED_JSON}`)
  
  return cleanedItems
}

async function createHTMLPreview(items) {
  console.log('\nCreating HTML preview...')
  
  const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math Content Preview</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .toc {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .toc h2 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        
        .toc a {
            color: #333;
            text-decoration: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .toc a:hover {
            color: #667eea;
        }
        
        .badge {
            background: #e0e7ff;
            color: #667eea;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.85em;
        }
        
        .content-item {
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .content-header {
            border-bottom: 2px solid #667eea;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }
        
        .content-header h2 {
            color: #667eea;
            font-size: 2em;
        }
        
        .meta-info {
            display: flex;
            gap: 20px;
            margin-top: 10px;
            color: #666;
            font-size: 0.9em;
        }
        
        .content-body {
            color: #333;
        }
        
        .content-body h1 {
            color: #2e7d32;
            margin: 30px 0 20px;
            font-size: 1.8em;
        }
        
        .content-body h2 {
            color: #558b2f;
            margin: 25px 0 15px;
            font-size: 1.4em;
        }
        
        .content-body h3 {
            color: #666;
            margin: 20px 0 10px;
            font-size: 1.2em;
        }
        
        .content-body p {
            margin-bottom: 15px;
        }
        
        .content-body ul, .content-body ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        
        .content-body li {
            margin-bottom: 8px;
        }
        
        section {
            margin: 30px 0;
            padding: 20px;
            background: #f9f9f9;
            border-left: 4px solid #667eea;
            border-radius: 5px;
        }
        
        .introduction {
            background: #e8f5e9;
            border-left-color: #4caf50;
        }
        
        .historical-context {
            background: #fff3e0;
            border-left-color: #ff9800;
        }
        
        .philosophical-questions {
            background: #f3e5f5;
            border-left-color: #9c27b0;
        }
        
        .questions-section {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 2px dashed #ddd;
        }
        
        .questions-section h3 {
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .question {
            background: #f9f9f9;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            border-left: 3px solid #667eea;
        }
        
        .question-text {
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .options {
            list-style: none;
            padding-left: 0;
        }
        
        .options li {
            padding: 5px 0;
            padding-left: 25px;
            position: relative;
        }
        
        .options li.correct {
            color: #4caf50;
            font-weight: 600;
        }
        
        .options li.correct::before {
            content: "✓";
            position: absolute;
            left: 5px;
        }
        
        .explanation {
            margin-top: 10px;
            padding: 10px;
            background: #e3f2fd;
            border-radius: 3px;
            font-size: 0.9em;
            color: #666;
        }
        
        .no-questions {
            color: #999;
            font-style: italic;
            padding: 20px;
            text-align: center;
            background: #f5f5f5;
            border-radius: 5px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .content-item {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Math Learning Content Preview</h1>
            <p>Generated using Kieran Egan's Educational Philosophy</p>
        </div>
        
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
                ${items.map((item, index) => `
                    <li>
                        <a href="#content-${index}">
                            <span>${item.nodeName}</span>
                            <span class="badge">${item.content.difficulty_level || 'intermediate'}</span>
                        </a>
                    </li>
                `).join('')}
            </ul>
        </div>
        
        ${items.map((item, index) => `
            <div class="content-item" id="content-${index}">
                <div class="content-header">
                    <h2>${item.nodeName}</h2>
                    <div class="meta-info">
                        <span>📖 ${item.content.estimated_time_minutes || 20} minutes</span>
                        <span>🎯 ${item.content.difficulty_level || 'intermediate'}</span>
                        <span>❓ ${item.questions.length} questions</span>
                    </div>
                </div>
                
                <div class="content-body">
                    ${item.content.content || '<p>Content not available</p>'}
                </div>
                
                ${item.questions.length > 0 ? `
                    <div class="questions-section">
                        <h3>Practice Questions</h3>
                        ${item.questions.slice(0, 5).map((q, qIndex) => `
                            <div class="question">
                                <div class="question-text">
                                    ${qIndex + 1}. ${q.question_text}
                                </div>
                                <ul class="options">
                                    ${q.options.map((opt, optIndex) => `
                                        <li class="${optIndex === q.correct_answer ? 'correct' : ''}">
                                            ${opt}
                                        </li>
                                    `).join('')}
                                </ul>
                                <div class="explanation">
                                    <strong>Explanation:</strong> ${q.explanation}
                                </div>
                            </div>
                        `).join('')}
                        ${item.questions.length > 5 ? `
                            <p style="text-align: center; color: #666; margin-top: 20px;">
                                <em>... and ${item.questions.length - 5} more questions</em>
                            </p>
                        ` : ''}
                    </div>
                ` : `
                    <div class="no-questions">
                        No questions generated for this topic yet.
                    </div>
                `}
            </div>
        `).join('')}
    </div>
</body>
</html>
  `
  
  await fs.writeFile(HTML_PREVIEW, html)
  console.log(`✓ HTML preview saved to: ${HTML_PREVIEW}`)
}

async function main() {
  try {
    console.log('Content Cleaning and Preview Generator')
    console.log('======================================\n')
    
    // Clean the content
    const cleanedItems = await cleanContent()
    
    // Create HTML preview
    await createHTMLPreview(cleanedItems)
    
    console.log('\n' + '='.repeat(50))
    console.log('SUCCESS!')
    console.log('='.repeat(50))
    console.log('\nFiles created:')
    console.log(`1. Cleaned JSON: ${CLEANED_JSON}`)
    console.log(`2. HTML Preview: ${HTML_PREVIEW}`)
    console.log('\nOpen the HTML file in your browser to review the content.')
    console.log('If satisfied, run: node scripts/content_generation/insert_reviewed_content.js')
    
  } catch (error) {
    console.error('Error:', error)
  }
}

main()