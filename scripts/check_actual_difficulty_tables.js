const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkActualDifficultyTables() {
  console.log('=== CHECKING ACTUAL DIFFICULTY TABLES ===\n');
  
  try {
    // Check spelling_difficulty_levels table
    console.log('📊 SPELLING_DIFFICULTY_LEVELS TABLE:');
    const { data: spellingLevels, error: spellingError } = await supabase
      .from('spelling_difficulty_levels')
      .select('*')
      .order('level');
    
    if (!spellingError && spellingLevels) {
      console.log(`Found ${spellingLevels.length} spelling difficulty levels:`);
      spellingLevels.forEach(level => {
        console.log(`  ID ${level.id}: Level ${level.level} - ${level.name}`);
      });
    } else if (spellingError) {
      console.log('Error:', spellingError.message);
    }
    
    // Check vocabulary_difficulty_levels table
    console.log('\n📊 VOCABULARY_DIFFICULTY_LEVELS TABLE:');
    const { data: vocabLevels, error: vocabError } = await supabase
      .from('vocabulary_difficulty_levels')
      .select('*')
      .order('level');
    
    if (!vocabError && vocabLevels) {
      console.log(`Found ${vocabLevels.length} vocabulary difficulty levels:`);
      vocabLevels.forEach(level => {
        console.log(`  ID ${level.id}: Level ${level.level} - ${level.name}`);
      });
    } else if (vocabError) {
      console.log('Error:', vocabError.message);
    }
    
    // Now check how the foreign keys map
    console.log('\n🔍 CHECKING FOREIGN KEY USAGE IN SPELLING_WORDS:');
    
    // Get a sample of words with difficulty IDs
    const { data: sampleWords } = await supabase
      .from('spelling_words')
      .select('word, spelling_difficulty_id, vocabulary_difficulty_id, spelling_difficulty_name, vocabulary_difficulty_name')
      .not('spelling_difficulty_id', 'is', null)
      .limit(10);
    
    if (sampleWords) {
      console.log('\nSample mappings:');
      sampleWords.forEach(w => {
        console.log(`  ${w.word}:`);
        console.log(`    Spelling: ID ${w.spelling_difficulty_id} (old name: ${w.spelling_difficulty_name})`);
        console.log(`    Vocabulary: ID ${w.vocabulary_difficulty_id} (old name: ${w.vocabulary_difficulty_name})`);
      });
    }
    
    // Check distribution of difficulty IDs
    console.log('\n📊 DIFFICULTY ID DISTRIBUTION:');
    
    // Get unique spelling difficulty IDs
    const { data: spellingDist } = await supabase
      .from('spelling_words')
      .select('spelling_difficulty_id')
      .not('spelling_difficulty_id', 'is', null);
    
    if (spellingDist) {
      const spellingCounts = {};
      spellingDist.forEach(row => {
        const id = row.spelling_difficulty_id;
        spellingCounts[id] = (spellingCounts[id] || 0) + 1;
      });
      
      console.log('\nSpelling difficulty ID usage:');
      Object.entries(spellingCounts).sort((a, b) => a[0] - b[0]).forEach(([id, count]) => {
        const level = spellingLevels?.find(l => l.id == id);
        console.log(`  ID ${id} (${level?.name || 'Unknown'}): ${count} words`);
      });
    }
    
    // Get unique vocabulary difficulty IDs
    const { data: vocabDist } = await supabase
      .from('spelling_words')
      .select('vocabulary_difficulty_id')
      .not('vocabulary_difficulty_id', 'is', null);
    
    if (vocabDist) {
      const vocabCounts = {};
      vocabDist.forEach(row => {
        const id = row.vocabulary_difficulty_id;
        vocabCounts[id] = (vocabCounts[id] || 0) + 1;
      });
      
      console.log('\nVocabulary difficulty ID usage:');
      Object.entries(vocabCounts).sort((a, b) => a[0] - b[0]).forEach(([id, count]) => {
        const level = vocabLevels?.find(l => l.id == id);
        console.log(`  ID ${id} (${level?.name || 'Unknown'}): ${count} words`);
      });
    }
    
    console.log('\n=== SUMMARY ===');
    console.log('Tables found:');
    console.log(`  - spelling_difficulty_levels: ${spellingLevels ? '✅' : '❌'}`);
    console.log(`  - vocabulary_difficulty_levels: ${vocabLevels ? '✅' : '❌'}`);
    console.log('\nForeign key columns in spelling_words:');
    console.log('  - spelling_difficulty_id');
    console.log('  - vocabulary_difficulty_id');
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkActualDifficultyTables().catch(console.error);