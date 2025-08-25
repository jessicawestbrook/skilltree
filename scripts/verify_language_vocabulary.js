/**
 * Verify language vocabulary tables and data
 */

const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function verifyVocabulary() {
  console.log('Verifying language vocabulary system...')
  console.log('=' .repeat(60))
  
  try {
    // Check if tables exist
    console.log('\n1. Checking tables...')
    
    // Check difficulties table
    const { data: difficulties, error: diffError } = await supabase
      .from('language_vocabulary_difficulties')
      .select('*')
      .order('id')
    
    if (diffError) {
      console.error('Error checking difficulties table:', diffError)
    } else {
      console.log(`✓ language_vocabulary_difficulties: ${difficulties.length} levels`)
      difficulties.forEach(d => {
        console.log(`  - Level ${d.id}: ${d.difficulty_name} (Zipf ${d.min_zipf}${d.max_zipf ? '-' + d.max_zipf : '+'})`)
      })
    }
    
    // Check vocabulary table
    console.log('\n2. Checking vocabulary data...')
    const { data: vocab, error: vocabError } = await supabase
      .from('language_vocabulary')
      .select('language, difficulty_id, COUNT(*)', { count: 'exact' })
      .eq('language', 'es')
    
    if (vocabError) {
      console.error('Error checking vocabulary:', vocabError)
    } else {
      // Get count by difficulty
      const { data: byDifficulty } = await supabase
        .from('language_vocabulary')
        .select('difficulty_id')
        .eq('language', 'es')
      
      const counts = {}
      byDifficulty?.forEach(v => {
        counts[v.difficulty_id] = (counts[v.difficulty_id] || 0) + 1
      })
      
      console.log(`✓ Spanish vocabulary: ${byDifficulty?.length || 0} total words`)
      Object.entries(counts).sort(([a], [b]) => a - b).forEach(([level, count]) => {
        const diff = difficulties?.find(d => d.id === parseInt(level))
        console.log(`  - Level ${level} (${diff?.difficulty_name || 'Unknown'}): ${count} words`)
      })
    }
    
    // Check study lists
    console.log('\n3. Checking study lists...')
    const { data: studyLists, error: listsError } = await supabase
      .from('language_vocabulary_study_lists')
      .select('*')
      .eq('language', 'es')
      .order('difficulty_id')
    
    if (listsError) {
      console.error('Error checking study lists:', listsError)
    } else {
      console.log(`✓ Spanish study lists: ${studyLists.length} lists`)
      studyLists.forEach(list => {
        console.log(`  - ${list.name}`)
      })
    }
    
    // Show sample vocabulary
    console.log('\n4. Sample Spanish vocabulary:')
    const { data: samples } = await supabase
      .from('language_vocabulary')
      .select('word, english_translation, pronunciation_guide, zipf_frequency, difficulty_id')
      .eq('language', 'es')
      .order('zipf_frequency', { ascending: false })
      .limit(10)
    
    if (samples && samples.length > 0) {
      console.log('\nTop 10 most frequent words:')
      samples.forEach(s => {
        console.log(`  ${s.word.padEnd(15)} → ${s.english_translation.padEnd(20)} [${s.pronunciation_guide}] (Zipf: ${s.zipf_frequency}, Level: ${s.difficulty_id})`)
      })
    }
    
    // Check if view exists
    console.log('\n5. Checking view...')
    const { data: viewData, error: viewError } = await supabase
      .from('language_vocabulary_with_difficulty')
      .select('*')
      .eq('language', 'es')
      .limit(1)
    
    if (viewError) {
      console.error('✗ View not accessible:', viewError.message)
    } else {
      console.log('✓ language_vocabulary_with_difficulty view is accessible')
    }
    
    console.log('\n' + '=' .repeat(60))
    console.log('Verification complete!')
    
  } catch (error) {
    console.error('Error during verification:', error)
  }
}

verifyVocabulary()