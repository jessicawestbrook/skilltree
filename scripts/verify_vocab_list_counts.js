const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyVocabListCounts() {
  console.log('Verifying actual vocabulary list counts...\n');
  
  const difficultyNames = [
    'Foundation Vocabulary',
    'Academic Vocabulary',
    'Sophisticated Vocabulary',
    'Specialized Vocabulary',
    'Scholarly Vocabulary'
  ];
  
  // Get the study lists
  const { data: lists, error: listsError } = await supabase
    .from('study_lists')
    .select('id, name')
    .in('name', difficultyNames)
    .order('name');
    
  if (listsError) {
    console.error('Error fetching lists:', listsError);
    return;
  }
  
  console.log('=== Study List Item Counts ===');
  for (const list of lists || []) {
    // Get count using count: 'exact' which bypasses row limit
    const { count, error } = await supabase
      .from('study_list_items')
      .select('*', { count: 'exact', head: true })
      .eq('study_list_id', list.id)
      .eq('item_type', 'spelling_word');
      
    if (error) {
      console.error(`Error counting items for ${list.name}:`, error);
    } else {
      console.log(`${list.name}: ${count} items`);
    }
  }
  
  console.log('\n=== Direct Vocabulary Word Counts by Difficulty ===');
  // Also check direct counts from spelling_words table
  for (let difficulty_id = 1; difficulty_id <= 5; difficulty_id++) {
    const { count, error } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .eq('is_vocabulary_word', true)
      .eq('vocabulary_difficulty_id', difficulty_id);
      
    if (error) {
      console.error(`Error counting difficulty ${difficulty_id}:`, error);
    } else {
      const difficultyNames = ['Foundation', 'Academic', 'Sophisticated', 'Specialized', 'Scholarly'];
      console.log(`${difficultyNames[difficulty_id - 1]} (difficulty ${difficulty_id}): ${count} words`);
    }
  }
  
  console.log('\n=== Checking for Study List Population Issues ===');
  // Check if lists might need more words added
  for (const list of lists || []) {
    // Get a sample of items to check
    const { data: items, error: itemsError } = await supabase
      .from('study_list_items')
      .select('item_id')
      .eq('study_list_id', list.id)
      .eq('item_type', 'spelling_word')
      .limit(5);
      
    if (!itemsError && items && items.length > 0) {
      // Check if these items are valid vocabulary words
      const { data: words } = await supabase
        .from('spelling_words')
        .select('id, word, vocabulary_difficulty_id')
        .in('id', items.map(i => i.item_id));
        
      console.log(`\n${list.name} - Sample words:`);
      words?.forEach(w => console.log(`  - ${w.word} (difficulty ${w.vocabulary_difficulty_id})`));
    }
  }
}

verifyVocabListCounts()
  .then(() => console.log('\nDone!'))
  .catch(console.error);