const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkDifficultyTableColumns() {
  console.log('=== CHECKING DIFFICULTY TABLE STRUCTURE ===\n');
  
  try {
    // Check spelling_difficulty_levels table structure
    console.log('📊 SPELLING_DIFFICULTY_LEVELS TABLE:');
    const { data: spellingLevels, error: spellingError } = await supabase
      .from('spelling_difficulty_levels')
      .select('*')
      .limit(5);
    
    if (!spellingError && spellingLevels && spellingLevels.length > 0) {
      console.log('Columns:', Object.keys(spellingLevels[0]));
      console.log('\nSample data:');
      spellingLevels.forEach(level => {
        console.log(`  ID ${level.id}: ${JSON.stringify(level)}`);
      });
    } else if (spellingError) {
      console.log('Error:', spellingError.message);
    }
    
    // Check vocabulary_difficulty_levels table structure
    console.log('\n📊 VOCABULARY_DIFFICULTY_LEVELS TABLE:');
    const { data: vocabLevels, error: vocabError } = await supabase
      .from('vocabulary_difficulty_levels')
      .select('*')
      .limit(5);
    
    if (!vocabError && vocabLevels && vocabLevels.length > 0) {
      console.log('Columns:', Object.keys(vocabLevels[0]));
      console.log('\nSample data:');
      vocabLevels.forEach(level => {
        console.log(`  ID ${level.id}: ${JSON.stringify(level)}`);
      });
    } else if (vocabError) {
      console.log('Error:', vocabError.message);
    }
    
    // Now let's see what difficulty IDs are actually being used
    console.log('\n🔍 ANALYZING CURRENT DIFFICULTY ID USAGE:');
    
    // Check what spelling difficulty IDs exist
    const { data: spellingIds } = await supabase
      .from('spelling_words')
      .select('spelling_difficulty_id, spelling_difficulty_level, spelling_difficulty_name')
      .not('spelling_difficulty_id', 'is', null)
      .order('spelling_difficulty_id');
    
    if (spellingIds) {
      const uniqueSpellingMappings = new Map();
      spellingIds.forEach(row => {
        const key = row.spelling_difficulty_id;
        if (!uniqueSpellingMappings.has(key)) {
          uniqueSpellingMappings.set(key, {
            id: row.spelling_difficulty_id,
            level: row.spelling_difficulty_level,
            name: row.spelling_difficulty_name
          });
        }
      });
      
      console.log('\nUnique spelling difficulty mappings:');
      uniqueSpellingMappings.forEach((value, key) => {
        console.log(`  ID ${key}: Level ${value.level} = "${value.name}"`);
      });
    }
    
    // Check what vocabulary difficulty IDs exist
    const { data: vocabIds } = await supabase
      .from('spelling_words')
      .select('vocabulary_difficulty_id, vocabulary_difficulty_level, vocabulary_difficulty_name')
      .not('vocabulary_difficulty_id', 'is', null)
      .order('vocabulary_difficulty_id');
    
    if (vocabIds) {
      const uniqueVocabMappings = new Map();
      vocabIds.forEach(row => {
        const key = row.vocabulary_difficulty_id;
        if (!uniqueVocabMappings.has(key)) {
          uniqueVocabMappings.set(key, {
            id: row.vocabulary_difficulty_id,
            level: row.vocabulary_difficulty_level,
            name: row.vocabulary_difficulty_name
          });
        }
      });
      
      console.log('\nUnique vocabulary difficulty mappings:');
      uniqueVocabMappings.forEach((value, key) => {
        console.log(`  ID ${key}: Level ${value.level} = "${value.name}"`);
      });
    }
    
    // Count words without difficulty IDs
    const { count: noSpellingId } = await supabase
      .from('spelling_words')
      .select('id', { count: 'exact', head: true })
      .is('spelling_difficulty_id', null);
    
    const { count: noVocabId } = await supabase
      .from('spelling_words')
      .select('id', { count: 'exact', head: true })
      .is('vocabulary_difficulty_id', null);
    
    console.log('\n📊 MISSING DIFFICULTY IDS:');
    console.log(`Words without spelling_difficulty_id: ${noSpellingId}`);
    console.log(`Words without vocabulary_difficulty_id: ${noVocabId}`);
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkDifficultyTableColumns().catch(console.error);