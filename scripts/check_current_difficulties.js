const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkDistributions() {
  // Check current distributions
  const { data: spelling } = await supabase
    .from('spelling_words')
    .select('spelling_difficulty_level')
    .not('spelling_difficulty_level', 'is', null);
    
  const { data: vocab } = await supabase
    .from('spelling_words')
    .select('vocabulary_difficulty_level')
    .not('vocabulary_difficulty_level', 'is', null);
  
  // Count distributions
  const spellDist = {};
  const vocabDist = {};
  
  spelling.forEach(w => {
    spellDist[w.spelling_difficulty_level] = (spellDist[w.spelling_difficulty_level] || 0) + 1;
  });
  
  vocab.forEach(w => {
    vocabDist[w.vocabulary_difficulty_level] = (vocabDist[w.vocabulary_difficulty_level] || 0) + 1;
  });
  
  console.log('CURRENT DISTRIBUTIONS BEFORE UPDATE:');
  console.log('\nSpelling Difficulty:');
  for (let i = 1; i <= 5; i++) {
    const count = spellDist[i] || 0;
    const pct = (count / spelling.length * 100).toFixed(1);
    console.log(`  Level ${i}: ${count} words (${pct}%)`);
  }
  
  console.log('\nVocabulary Difficulty:');
  for (let i = 1; i <= 5; i++) {
    const count = vocabDist[i] || 0;
    const pct = (count / vocab.length * 100).toFixed(1);
    console.log(`  Level ${i}: ${count} words (${pct}%)`);
  }
  
  console.log(`\nTotal words with spelling difficulty: ${spelling.length}`);
  console.log(`Total words with vocabulary difficulty: ${vocab.length}`);
}

checkDistributions();