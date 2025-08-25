/**
 * Check existing Spanish vocabulary in database
 */

const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function checkExisting() {
  console.log('Checking existing Spanish vocabulary...')
  console.log('=' .repeat(60))
  
  try {
    // Get all existing Spanish words
    const { data: existing, error } = await supabase
      .from('language_vocabulary')
      .select('word, difficulty_id')
      .eq('language', 'es')
      .order('word')
    
    if (error) {
      console.error('Error fetching existing words:', error)
      return
    }
    
    console.log(`Found ${existing.length} existing Spanish words in database`)
    
    // Group by difficulty
    const byDifficulty = {}
    existing.forEach(w => {
      if (!byDifficulty[w.difficulty_id]) {
        byDifficulty[w.difficulty_id] = []
      }
      byDifficulty[w.difficulty_id].push(w.word)
    })
    
    console.log('\nExisting words by difficulty:')
    Object.keys(byDifficulty).sort().forEach(level => {
      console.log(`  Level ${level}: ${byDifficulty[level].length} words`)
    })
    
    // Save to file for reference
    const fs = require('fs')
    const existingWords = existing.map(w => w.word)
    fs.writeFileSync('existing_spanish_words.json', JSON.stringify(existingWords, null, 2))
    console.log('\nExisting words saved to existing_spanish_words.json')
    
    // Show sample
    console.log('\nSample existing words:')
    existing.slice(0, 20).forEach(w => {
      console.log(`  ${w.word} (Level ${w.difficulty_id})`)
    })
    
  } catch (error) {
    console.error('Error:', error)
  }
}

checkExisting()