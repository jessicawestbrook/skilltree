const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkScrippsLists() {
  // Check for existing Scripps lists
  const { data: scrippsLists, error } = await supabase
    .from('study_lists')
    .select('id, name, description')
    .ilike('name', '%Scripps%')
    .order('name');
    
  if (error) {
    console.error('Error:', error);
    return;
  }
  
  console.log('Existing Scripps lists:', scrippsLists?.length || 0);
  scrippsLists?.forEach(list => {
    console.log(`  - ${list.name}: ${list.id}`);
  });
  
  // Check how many words have Scripps in original_source
  const { data: scrippsWords, count } = await supabase
    .from('spelling_words')
    .select('source_difficulty', { count: 'exact', head: true })
    .ilike('original_source', '%Scripps%');
    
  console.log(`\nTotal words with 'Scripps' in original_source: ${count}`);
  
  // Check distribution by source_difficulty
  const { data: difficultyDist } = await supabase
    .from('spelling_words')
    .select('source_difficulty')
    .ilike('original_source', '%Scripps%');
    
  const distribution = {};
  difficultyDist?.forEach(word => {
    const diff = word.source_difficulty || 'null';
    distribution[diff] = (distribution[diff] || 0) + 1;
  });
  
  console.log('\nDistribution by source_difficulty:');
  Object.entries(distribution).sort().forEach(([key, value]) => {
    console.log(`  ${key}: ${value}`);
  });
}

checkScrippsLists().catch(console.error);