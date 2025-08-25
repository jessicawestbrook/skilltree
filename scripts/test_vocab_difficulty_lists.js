const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function testVocabDifficultyLists() {
  console.log('Testing vocabulary difficulty lists setup...\n');
  
  // Test 1: Check vocabulary difficulty lists exist
  console.log('1. Checking vocabulary difficulty study lists:');
  const difficultyNames = [
    'Foundation Vocabulary',
    'Academic Vocabulary',
    'Sophisticated Vocabulary',
    'Specialized Vocabulary',
    'Scholarly Vocabulary'
  ];
  
  const { data: vocabLists, error: listsError } = await supabase
    .from('study_lists')
    .select('id, name, description')
    .in('name', difficultyNames)
    .order('name');
    
  if (listsError) {
    console.error('Error fetching vocabulary lists:', listsError);
    return;
  }
  
  console.log(`Found ${vocabLists?.length || 0} vocabulary difficulty lists:`);
  for (const list of vocabLists || []) {
    // Get item count for each list
    const { count } = await supabase
      .from('study_list_items')
      .select('*', { count: 'exact', head: true })
      .eq('study_list_id', list.id);
      
    console.log(`- ${list.name}: ${count} words`);
  }
  
  // Test 2: Verify no grade level lists should be shown
  console.log('\n2. Checking that grade level lists are excluded:');
  const { data: gradeLists } = await supabase
    .from('study_lists')
    .select('name')
    .or('name.ilike.%Grade%,name.ilike.%Kindergarten%,name.ilike.%Pre-K%');
    
  console.log(`Found ${gradeLists?.length || 0} grade-related lists (these should be excluded from dropdown)`);
  if (gradeLists && gradeLists.length > 0) {
    console.log('Grade lists present in database (but should be filtered out in UI):');
    gradeLists.forEach(list => console.log(`  - ${list.name}`));
  }
  
  // Test 3: Test batch fetching simulation
  console.log('\n3. Testing batch fetch simulation for Foundation Vocabulary:');
  const foundationList = vocabLists?.find(l => l.name === 'Foundation Vocabulary');
  if (foundationList) {
    const { data: items } = await supabase
      .from('study_list_items')
      .select('item_id')
      .eq('study_list_id', foundationList.id)
      .eq('item_type', 'spelling_word');
      
    if (items && items.length > 0) {
      console.log(`Total words to fetch: ${items.length}`);
      
      // Simulate batch fetching
      const batchSize = 50;
      const wordIds = items.map(item => item.item_id);
      let totalFetched = 0;
      
      for (let i = 0; i < wordIds.length; i += batchSize) {
        const batchIds = wordIds.slice(i, i + batchSize);
        const { data: batchWords, error: batchError } = await supabase
          .from('spelling_words')
          .select('id, word')
          .in('id', batchIds);
          
        if (batchError) {
          console.error(`Error in batch ${Math.floor(i/batchSize) + 1}:`, batchError);
        } else {
          totalFetched += batchWords?.length || 0;
          console.log(`  Batch ${Math.floor(i/batchSize) + 1}: fetched ${batchWords?.length || 0} words`);
        }
        
        // Only do first 3 batches for testing
        if (i >= batchSize * 2) {
          console.log('  ... (stopping after 3 batches for testing)');
          break;
        }
      }
    }
  }
  
  // Test 4: Verify vocabulary difficulty levels mapping
  console.log('\n4. Verifying vocabulary difficulty mappings:');
  const difficultyMappings = [
    { name: 'Foundation Vocabulary', difficulty_id: 1 },
    { name: 'Academic Vocabulary', difficulty_id: 2 },
    { name: 'Sophisticated Vocabulary', difficulty_id: 3 },
    { name: 'Specialized Vocabulary', difficulty_id: 4 },
    { name: 'Scholarly Vocabulary', difficulty_id: 5 }
  ];
  
  for (const mapping of difficultyMappings) {
    const list = vocabLists?.find(l => l.name === mapping.name);
    if (list) {
      // Check a sample word from this list has the correct difficulty
      const { data: sampleItem } = await supabase
        .from('study_list_items')
        .select('item_id')
        .eq('study_list_id', list.id)
        .eq('item_type', 'spelling_word')
        .limit(1)
        .single();
        
      if (sampleItem) {
        const { data: word } = await supabase
          .from('spelling_words')
          .select('word, vocabulary_difficulty_id')
          .eq('id', sampleItem.item_id)
          .single();
          
        if (word) {
          const match = word.vocabulary_difficulty_id === mapping.difficulty_id;
          console.log(`${mapping.name} (difficulty ${mapping.difficulty_id}): sample word "${word.word}" has difficulty ${word.vocabulary_difficulty_id} - ${match ? '✓' : '✗'}`);
        }
      }
    }
  }
}

testVocabDifficultyLists()
  .then(() => console.log('\nTest complete!'))
  .catch(console.error);