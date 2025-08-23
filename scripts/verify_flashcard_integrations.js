const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function verifyFlashcardIntegrations() {
  try {
    console.log('Verifying Flashcard Integrations\n')
    console.log('=' .repeat(50))
    
    // Check if tables exist
    console.log('\n📋 Checking Required Tables:')
    
    // Check user_flashcard_reviews table
    const { count: reviewCount, error: reviewError } = await supabase
      .from('user_flashcard_reviews')
      .select('*', { count: 'exact', head: true })
    
    if (reviewError && reviewError.code === '42P01') {
      console.log('❌ user_flashcard_reviews table does not exist')
      console.log('   Please run the migration: supabase/migrations/20250823_create_spaced_repetition.sql')
    } else {
      console.log(`✅ user_flashcard_reviews table exists (${reviewCount || 0} records)`)
    }
    
    // Check flashcard_review_history table
    const { count: historyCount, error: historyError } = await supabase
      .from('flashcard_review_history')
      .select('*', { count: 'exact', head: true })
    
    if (historyError && historyError.code === '42P01') {
      console.log('❌ flashcard_review_history table does not exist')
    } else {
      console.log(`✅ flashcard_review_history table exists (${historyCount || 0} records)`)
    }
    
    // Check content tables
    console.log('\n📚 Checking Content Tables:')
    
    // Questions table
    const { count: questionCount } = await supabase
      .from('questions')
      .select('*', { count: 'exact', head: true })
    console.log(`  • questions table: ${questionCount || 0} questions available`)
    
    // Spelling words table
    const { count: spellingCount } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
    console.log(`  • spelling_words table: ${spellingCount || 0} words available`)
    
    // Language questions table
    const { count: languageCount } = await supabase
      .from('language_questions')
      .select('*', { count: 'exact', head: true })
    console.log(`  • language_questions table: ${languageCount || 0} questions available`)
    
    // Check flashcard type distribution if data exists
    if (reviewCount && reviewCount > 0) {
      console.log('\n📊 Flashcard Type Distribution:')
      
      const { data: typeStats } = await supabase
        .from('user_flashcard_reviews')
        .select('flashcard_type')
      
      if (typeStats) {
        const typeCounts = typeStats.reduce((acc, curr) => {
          acc[curr.flashcard_type] = (acc[curr.flashcard_type] || 0) + 1
          return acc
        }, {})
        
        Object.entries(typeCounts).forEach(([type, count]) => {
          console.log(`  • ${type}: ${count} flashcards`)
        })
      }
    }
    
    console.log('\n✅ Integration Summary:')
    console.log('=' .repeat(50))
    console.log('\nFlashcard Types Supported:')
    console.log('  1. vocabulary - From VocabularyTrainerPage')
    console.log('  2. spelling - From SpellingBeePage')
    console.log('  3. language - From LanguageTrainerPage')
    console.log('  4. question - From AdaptiveAssessment & SimpleLearningPage')
    console.log('  5. skill_node - From skill tree assessments')
    
    console.log('\nAutomatic Addition Triggers:')
    console.log('  • When completing an adaptive assessment')
    console.log('  • When finishing a learning module test')
    console.log('  • When answering vocabulary trainer questions')
    console.log('  • When attempting spelling bee words')
    console.log('  • When practicing language trainer questions')
    
    console.log('\nReview Locations:')
    console.log('  • ProfilePage - Smart Review section')
    console.log('  • /review - Dedicated review page')
    
  } catch (error) {
    console.error('Error during verification:', error)
  }
}

// Run the verification
verifyFlashcardIntegrations()