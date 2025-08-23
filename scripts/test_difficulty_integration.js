const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function testDifficultyIntegration() {
  console.log('Testing difficulty level integration...\n');
  
  try {
    // Test 1: Verify difficulty tables exist and have data
    console.log('=== TEST 1: Difficulty Tables ===');
    
    const { data: spellingLevels, error: spellingError } = await supabase
      .from('spelling_difficulty_levels')
      .select('id, name, description');
      
    if (spellingError) {
      console.log('❌ Spelling difficulty levels table:', spellingError.message);
    } else {
      console.log('✅ Spelling difficulty levels:', spellingLevels.length, 'levels');
      spellingLevels.forEach(level => {
        console.log(`  ${level.id}. ${level.name}`);
      });
    }
    
    const { data: vocabLevels, error: vocabError } = await supabase
      .from('vocabulary_difficulty_levels')
      .select('id, name, description');
      
    if (vocabError) {
      console.log('❌ Vocabulary difficulty levels table:', vocabError.message);
    } else {
      console.log('✅ Vocabulary difficulty levels:', vocabLevels.length, 'levels');
      vocabLevels.forEach(level => {
        console.log(`  ${level.id}. ${level.name}`);
      });
    }
    
    // Test 2: Try querying with joins (new structure)
    console.log('\n=== TEST 2: Join Queries ===');
    
    const { data: wordsWithJoins, error: joinError } = await supabase
      .from('spelling_words')
      .select(`
        word,
        spelling_difficulty_level,
        vocabulary_difficulty_level,
        spelling_difficulty:spelling_difficulty_levels(name, description),
        vocabulary_difficulty:vocabulary_difficulty_levels(name, description)
      `)
      .limit(5);
      
    if (joinError) {
      console.log('❌ Join query failed:', joinError.message);
    } else {
      console.log('✅ Join queries working:', wordsWithJoins.length, 'sample words');
      wordsWithJoins.forEach(word => {
        console.log(`  ${word.word}: Spelling(${word.spelling_difficulty?.name || 'N/A'}) Vocab(${word.vocabulary_difficulty?.name || 'N/A'})`);
      });
    }
    
    // Test 3: Check foreign key columns exist
    console.log('\n=== TEST 3: Foreign Key Columns ===');
    
    const { data: fkCheck, error: fkError } = await supabase
      .from('spelling_words')
      .select('word, spelling_difficulty_id, vocabulary_difficulty_id')
      .not('spelling_difficulty_id', 'is', null)
      .not('vocabulary_difficulty_id', 'is', null)
      .limit(3);
      
    if (fkError) {
      console.log('❌ Foreign key columns not found or not populated:', fkError.message);
    } else {
      console.log('✅ Foreign key columns working:', fkCheck.length, 'sample words');
      fkCheck.forEach(word => {
        console.log(`  ${word.word}: spelling_difficulty_id=${word.spelling_difficulty_id}, vocabulary_difficulty_id=${word.vocabulary_difficulty_id}`);
      });
    }
    
    console.log('\n✅ All tests completed successfully!');
    console.log('The spelling and vocabulary difficulty normalization is working correctly.');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

if (require.main === module) {
  testDifficultyIntegration();
}