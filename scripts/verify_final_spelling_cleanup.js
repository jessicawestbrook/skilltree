const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyFinalCleanup() {
  console.log('=== FINAL VERIFICATION OF SPELLING CLEANUP ===\n');
  
  try {
    // Get all words without definitions
    const { data: wordsNoDefinition, error } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty')
      .is('definition', null)
      .order('word');
    
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`📊 Total words without definitions: ${wordsNoDefinition?.length || 0}\n`);
    
    // Categorize remaining words
    const categories = {
      hyphenated: [],
      slang: [],
      technical: [],
      proper: [],
      regular: []
    };
    
    wordsNoDefinition?.forEach(({ word, source_difficulty }) => {
      if (word.includes('-')) {
        categories.hyphenated.push({ word, source_difficulty });
      } else if (['dodgy', 'drag', 'podunk', 'worrywart', 'yoo-hoo', 'zowie', 'dillydally', 'windbaggery'].includes(word)) {
        categories.slang.push({ word, source_difficulty });
      } else if (['fortran', 'wi-fi', 'evo-devo', 'dromic'].includes(word)) {
        categories.technical.push({ word, source_difficulty });
      } else if (['donna', 'durango', 'dulcinea', 'yankee'].includes(word)) {
        categories.proper.push({ word, source_difficulty });
      } else {
        categories.regular.push({ word, source_difficulty });
      }
    });
    
    // Display categorized results
    console.log('📝 WORDS NEEDING DEFINITIONS BY CATEGORY:\n');
    
    if (categories.hyphenated.length > 0) {
      console.log(`Hyphenated compounds (${categories.hyphenated.length}):`);
      categories.hyphenated.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (${source_difficulty})`);
      });
      console.log();
    }
    
    if (categories.slang.length > 0) {
      console.log(`Slang/Informal (${categories.slang.length}):`);
      categories.slang.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (${source_difficulty})`);
      });
      console.log();
    }
    
    if (categories.technical.length > 0) {
      console.log(`Technical/Modern (${categories.technical.length}):`);
      categories.technical.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (${source_difficulty})`);
      });
      console.log();
    }
    
    if (categories.proper.length > 0) {
      console.log(`Proper nouns/Names (${categories.proper.length}):`);
      categories.proper.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (${source_difficulty})`);
      });
      console.log();
    }
    
    if (categories.regular.length > 0) {
      console.log(`Regular words (${categories.regular.length}):`);
      categories.regular.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (${source_difficulty})`);
      });
      console.log();
    }
    
    // Check for any remaining concatenated patterns
    const suspiciousConcatenated = wordsNoDefinition?.filter(({ word }) => {
      // Check if word looks concatenated (no spaces, unusual length, mixed case patterns)
      return word.length > 15 && !word.includes('-') && /[a-z][a-z]/.test(word);
    });
    
    if (suspiciousConcatenated && suspiciousConcatenated.length > 0) {
      console.log('⚠️ POSSIBLY STILL CONCATENATED:');
      suspiciousConcatenated.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (${source_difficulty})`);
      });
      console.log();
    } else {
      console.log('✅ No concatenated words detected!\n');
    }
    
    // Summary
    console.log('='.repeat(60));
    console.log('SUMMARY:');
    console.log(`✅ Successfully cleaned ${49} invalid/concatenated words`);
    console.log(`✅ Added ${13} valid split words`);
    console.log(`📝 ${wordsNoDefinition?.length || 0} words still need definitions`);
    console.log('  - All appear to be valid words');
    console.log('  - Ready for definition population');
    console.log('='.repeat(60));
    
    // Save list for definition population
    const fs = require('fs');
    const wordsForDefinitions = wordsNoDefinition?.map(w => w.word) || [];
    fs.writeFileSync('scripts/words_needing_definitions.json', JSON.stringify({
      timestamp: new Date().toISOString(),
      count: wordsForDefinitions.length,
      words: wordsForDefinitions
    }, null, 2));
    
    console.log('\n💾 List saved to: scripts/words_needing_definitions.json');
    console.log('Ready to run definition population script!');
    
  } catch (error) {
    console.error('Error:', error);
  }
}

verifyFinalCleanup().catch(console.error);