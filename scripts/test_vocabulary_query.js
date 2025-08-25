const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function testVocabularyQueries() {
  console.log('Testing vocabulary queries...\n');
  
  // Test 1: Check if spelling_words table exists
  console.log('1. Testing basic spelling_words query:');
  const { data: basicWords, error: basicError } = await supabase
    .from('spelling_words')
    .select('id, word, vocabulary_difficulty_id')
    .eq('is_vocabulary_word', true)
    .limit(5);
    
  if (basicError) {
    console.error('Error with basic query:', basicError);
  } else {
    console.log(`Found ${basicWords?.length || 0} words`);
    if (basicWords && basicWords.length > 0) {
      console.log('Sample word:', basicWords[0]);
    }
  }
  
  // Test 2: Check if vocabulary_difficulty_levels table exists
  console.log('\n2. Testing vocabulary_difficulty_levels table:');
  const { data: diffLevels, error: diffError } = await supabase
    .from('vocabulary_difficulty_levels')
    .select('*');
    
  if (diffError) {
    console.error('Error with difficulty levels:', diffError);
    console.log('Table might not exist, will use fallback values');
  } else {
    console.log('Difficulty levels found:', diffLevels);
  }
  
  // Test 3: Test the join query (this is what's failing in the app)
  console.log('\n3. Testing join query with vocabulary_difficulty_levels:');
  const { data: joinedWords, error: joinError } = await supabase
    .from('spelling_words')
    .select(`
      *,
      vocabulary_difficulty_levels!vocabulary_difficulty_id(id, name, description)
    `)
    .eq('is_vocabulary_word', true)
    .limit(5);
    
  if (joinError) {
    console.error('Error with join query:', joinError);
    console.log('Will need to use fallback approach');
  } else {
    console.log(`Found ${joinedWords?.length || 0} words with joined data`);
    if (joinedWords && joinedWords.length > 0) {
      console.log('Sample joined word:', JSON.stringify(joinedWords[0], null, 2));
    }
  }
  
  // Test 4: Check study lists
  console.log('\n4. Checking vocabulary study lists:');
  const { data: studyLists, error: listsError } = await supabase
    .from('study_lists')
    .select('id, name')
    .or('name.ilike.%Foundation Vocabulary%,name.ilike.%Academic Vocabulary%,name.ilike.%Sophisticated Vocabulary%,name.ilike.%Specialized Vocabulary%,name.ilike.%Scholarly Vocabulary%');
    
  if (listsError) {
    console.error('Error fetching study lists:', listsError);
  } else {
    console.log('Found vocabulary difficulty lists:');
    studyLists?.forEach(list => console.log(`- ${list.name}`));
  }
}

testVocabularyQueries()
  .then(() => console.log('\nDone testing!'))
  .catch(console.error);