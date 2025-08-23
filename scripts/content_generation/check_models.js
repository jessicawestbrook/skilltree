/**
 * Quick script to check available Claude models
 */

const Anthropic = require('@anthropic-ai/sdk')
const path = require('path')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '../..', '.env.local') })

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

// Try different model names
const modelsToTry = [
  'claude-3-5-sonnet-latest',
  'claude-3-5-sonnet-20240620',
  'claude-3-sonnet-20240229',
  'claude-3-haiku-20240307',
  'claude-2.1',
  'claude-instant-1.2'
]

async function testModel(modelName) {
  try {
    console.log(`Testing ${modelName}...`)
    const response = await anthropic.messages.create({
      model: modelName,
      max_tokens: 10,
      messages: [{ role: "user", content: "Say hello" }]
    })
    console.log(`✓ ${modelName} works!`)
    return true
  } catch (error) {
    console.log(`✗ ${modelName} failed: ${error.message}`)
    return false
  }
}

async function main() {
  console.log('Testing available Claude models...\n')
  
  for (const model of modelsToTry) {
    await testModel(model)
    await new Promise(resolve => setTimeout(resolve, 1000)) // Rate limit
  }
}

main()