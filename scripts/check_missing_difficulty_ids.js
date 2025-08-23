const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkMissingDifficultyIds() {
  console.log('=== CHECKING MISSING DIFFICULTY IDS ===\n');
  
  try {
    // Check words missing spelling_difficulty_id
    const { data: missingSpelling, count: missingSpellingCount } = await supabase
      .from('spelling_words')
      .select('id, word, spelling_difficulty_level, spelling_difficulty_name, ai_spelling_difficulty_level, ai_spelling_difficulty_name', { count: 'exact' })
      .is('spelling_difficulty_id', null)
      .limit(10);
    
    console.log(`📊 Words missing spelling_difficulty_id: ${missingSpellingCount || 0}`);
    if (missingSpelling && missingSpelling.length > 0) {
      console.log('Sample words:');
      missingSpelling.slice(0, 5).forEach(w => {
        console.log(`  - ${w.word}`);
        console.log(`    spelling_difficulty_level: ${w.spelling_difficulty_level}`);
        console.log(`    spelling_difficulty_name: ${w.spelling_difficulty_name}`);
      });
    }
    
    // Check words missing vocabulary_difficulty_id
    const { data: missingVocab, count: missingVocabCount } = await supabase
      .from('spelling_words')
      .select('id, word, vocabulary_difficulty_level, vocabulary_difficulty_name', { count: 'exact' })
      .is('vocabulary_difficulty_id', null)
      .limit(10);
    
    console.log(`\n📊 Words missing vocabulary_difficulty_id: ${missingVocabCount || 0}`);
    if (missingVocab && missingVocab.length > 0) {
      console.log('Sample words:');
      missingVocab.slice(0, 5).forEach(w => {
        console.log(`  - ${w.word}`);
        console.log(`    vocabulary_difficulty_level: ${w.vocabulary_difficulty_level}`);
        console.log(`    vocabulary_difficulty_name: ${w.vocabulary_difficulty_name}`);
      });
    }
    
    // Check difficulties table
    console.log('\n📊 DIFFICULTIES TABLE:');
    const { data: difficulties } = await supabase
      .from('difficulties')
      .select('*')
      .order('category', { ascending: true })
      .order('level', { ascending: true });
    
    if (difficulties) {
      const spellingDiffs = difficulties.filter(d => d.category === 'spelling');
      const vocabDiffs = difficulties.filter(d => d.category === 'vocabulary');
      
      console.log('\nSpelling Difficulties:');
      spellingDiffs.forEach(d => {
        console.log(`  ID ${d.id}: Level ${d.level} - ${d.name}`);
      });
      
      console.log('\nVocabulary Difficulties:');
      vocabDiffs.forEach(d => {
        console.log(`  ID ${d.id}: Level ${d.level} - ${d.name}`);
      });
    }
    
    // Create mapping plan
    console.log('\n📝 MAPPING PLAN:');
    console.log('----------------------------------------');
    
    // Check what difficulty levels/names are used
    const { data: spellingLevels } = await supabase
      .from('spelling_words')
      .select('spelling_difficulty_level, spelling_difficulty_name')
      .is('spelling_difficulty_id', null)
      .not('spelling_difficulty_level', 'is', null);
    
    const uniqueSpellingCombos = new Map();
    spellingLevels?.forEach(row => {
      const key = `${row.spelling_difficulty_level}:${row.spelling_difficulty_name}`;
      uniqueSpellingCombos.set(key, {
        level: row.spelling_difficulty_level,
        name: row.spelling_difficulty_name
      });
    });
    
    console.log('\nUnique spelling difficulty combinations to map:');
    uniqueSpellingCombos.forEach((value, key) => {
      console.log(`  Level ${value.level}: ${value.name}`);
    });
    
    const { data: vocabLevels } = await supabase
      .from('spelling_words')
      .select('vocabulary_difficulty_level, vocabulary_difficulty_name')
      .is('vocabulary_difficulty_id', null)
      .not('vocabulary_difficulty_level', 'is', null);
    
    const uniqueVocabCombos = new Map();
    vocabLevels?.forEach(row => {
      const key = `${row.vocabulary_difficulty_level}:${row.vocabulary_difficulty_name}`;
      uniqueVocabCombos.set(key, {
        level: row.vocabulary_difficulty_level,
        name: row.vocabulary_difficulty_name
      });
    });
    
    console.log('\nUnique vocabulary difficulty combinations to map:');
    uniqueVocabCombos.forEach((value, key) => {
      console.log(`  Level ${value.level}: ${value.name}`);
    });
    
    console.log('\n=== SUMMARY ===');
    console.log(`Missing spelling_difficulty_id: ${missingSpellingCount || 0} words`);
    console.log(`Missing vocabulary_difficulty_id: ${missingVocabCount || 0} words`);
    console.log('\nThese need to be populated before removing old columns');
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkMissingDifficultyIds().catch(console.error);