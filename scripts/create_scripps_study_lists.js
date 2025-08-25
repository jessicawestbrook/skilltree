const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function createScrippsStudyLists() {
  console.log('Creating Scripps Level study lists...\n');
  
  // First, get a user_id from an existing public study list
  const { data: existingList } = await supabase
    .from('study_lists')
    .select('user_id')
    .eq('is_public', true)
    .limit(1)
    .single();
    
  if (!existingList) {
    console.error('No existing public study list found to get user_id');
    return;
  }
  
  const userId = existingList.user_id;
  console.log(`Using user_id: ${userId}\n`);
  
  // Define the three Scripps levels
  const scrippsLevels = [
    {
      name: 'Scripps One Bee',
      description: 'Beginner level words from Scripps National Spelling Bee',
      source_difficulty: 'One Bee'
    },
    {
      name: 'Scripps Two Bee',
      description: 'Intermediate level words from Scripps National Spelling Bee',
      source_difficulty: 'Two Bee'
    },
    {
      name: 'Scripps Three Bee',
      description: 'Advanced level words from Scripps National Spelling Bee',
      source_difficulty: 'Three Bee'
    }
  ];
  
  for (const level of scrippsLevels) {
    console.log(`Processing ${level.name}...`);
    
    // Check if this list already exists
    const { data: existingScripps } = await supabase
      .from('study_lists')
      .select('id')
      .eq('name', level.name)
      .single();
      
    if (existingScripps) {
      console.log(`  - ${level.name} already exists (${existingScripps.id})`);
      continue;
    }
    
    // Create the study list
    const { data: newList, error: createError } = await supabase
      .from('study_lists')
      .insert({
        name: level.name,
        description: level.description,
        user_id: userId,
        is_public: true
      })
      .select()
      .single();
      
    if (createError) {
      console.error(`  - Error creating ${level.name}:`, createError);
      continue;
    }
    
    console.log(`  - Created ${level.name} (${newList.id})`);
    
    // Get all words for this difficulty level
    // For words with multiple difficulties (e.g., "One Bee; Two Bee"), include them if they contain the target difficulty
    const { data: words, error: wordsError } = await supabase
      .from('spelling_words')
      .select('id')
      .ilike('original_source', '%Scripps%')
      .ilike('source_difficulty', `%${level.source_difficulty}%`);
      
    if (wordsError) {
      console.error(`  - Error fetching words:`, wordsError);
      continue;
    }
    
    console.log(`  - Found ${words.length} words for ${level.name}`);
    
    if (words.length === 0) {
      console.log(`  - No words found, skipping...`);
      continue;
    }
    
    // Create study list items in batches
    const batchSize = 500;
    let totalInserted = 0;
    
    for (let i = 0; i < words.length; i += batchSize) {
      const batch = words.slice(i, i + batchSize);
      const items = batch.map(word => ({
        study_list_id: newList.id,
        spelling_word_id: word.id,
        user_id: userId
      }));
      
      const { error: insertError } = await supabase
        .from('study_list_items')
        .insert(items);
        
      if (insertError) {
        console.error(`  - Error inserting batch ${i / batchSize + 1}:`, insertError);
      } else {
        totalInserted += batch.length;
        console.log(`  - Inserted batch ${Math.floor(i / batchSize) + 1}: ${totalInserted}/${words.length} words`);
      }
    }
    
    console.log(`  - Completed ${level.name}: ${totalInserted} words added\n`);
  }
  
  // Verify the lists were created
  console.log('\nVerifying Scripps study lists:');
  const { data: finalLists } = await supabase
    .from('study_lists')
    .select('id, name')
    .ilike('name', '%Scripps%')
    .order('name');
    
  finalLists?.forEach(list => {
    console.log(`  - ${list.name}: ${list.id}`);
  });
  
  // Get counts for each list
  console.log('\nGetting word counts for each list:');
  for (const list of finalLists || []) {
    const { count } = await supabase
      .from('study_list_items')
      .select('*', { count: 'exact', head: true })
      .eq('study_list_id', list.id);
      
    console.log(`  - ${list.name}: ${count} words`);
  }
}

createScrippsStudyLists().catch(console.error);