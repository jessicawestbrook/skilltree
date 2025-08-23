/**
 * Extract and display the actual content properly
 */

const fs = require('fs').promises
const path = require('path')

async function extractContent() {
  const inputFile = path.join(__dirname, 'output', 'math_content', 'content_for_review.json')
  const outputFile = path.join(__dirname, 'output', 'math_content', 'cleaned', 'final_content.json')
  const summaryFile = path.join(__dirname, 'output', 'math_content', 'cleaned', 'content_summary.txt')
  
  // Read the file
  const data = JSON.parse(await fs.readFile(inputFile, 'utf-8'))
  
  const extracted = []
  let summary = 'MATH CONTENT GENERATION SUMMARY\n'
  summary += '================================\n\n'
  
  for (const item of data) {
    // Extract the embedded JSON
    const contentStr = item.content.content
    const jsonMatch = contentStr.match(/\{[\s\S]*\}/)
    
    if (jsonMatch) {
      try {
        const parsed = JSON.parse(jsonMatch[0])
        
        const cleanItem = {
          nodeId: item.nodeId,
          nodeName: item.nodeName,
          content: {
            title: parsed.title,
            content: parsed.content,
            estimated_time_minutes: parsed.estimated_time_minutes,
            difficulty_level: parsed.difficulty_level
          },
          questions: item.questions || []
        }
        
        extracted.push(cleanItem)
        
        // Add to summary
        summary += `Topic: ${item.nodeName}\n`
        summary += `Title: ${parsed.title}\n`
        summary += `Time: ${parsed.estimated_time_minutes} minutes\n`
        summary += `Level: ${parsed.difficulty_level}\n`
        summary += `Questions: ${item.questions.length}\n`
        
        // Extract key sections
        const sections = parsed.content.match(/<h2>([^<]+)<\/h2>/g) || []
        if (sections.length > 0) {
          summary += 'Sections:\n'
          sections.forEach(s => {
            const title = s.replace(/<\/?h2>/g, '')
            summary += `  - ${title}\n`
          })
        }
        
        // Extract philosophical questions
        const philMatch = parsed.content.match(/<section class="philosophical-questions">[\s\S]*?<\/section>/)
        if (philMatch) {
          const questions = philMatch[0].match(/<li>([^<]+)<\/li>/g) || []
          if (questions.length > 0) {
            summary += 'Philosophical Questions:\n'
            questions.forEach((q, i) => {
              const text = q.replace(/<\/?li>/g, '').substring(0, 80) + '...'
              summary += `  ${i+1}. ${text}\n`
            })
          }
        }
        
        summary += '\n' + '-'.repeat(50) + '\n\n'
        
      } catch (e) {
        console.error(`Failed to parse content for ${item.nodeName}`)
      }
    }
  }
  
  // Save extracted content
  await fs.writeFile(outputFile, JSON.stringify(extracted, null, 2))
  await fs.writeFile(summaryFile, summary)
  
  console.log(summary)
  console.log(`\nExtracted content saved to: ${outputFile}`)
  console.log(`Summary saved to: ${summaryFile}`)
  
  return extracted
}

extractContent().catch(console.error)