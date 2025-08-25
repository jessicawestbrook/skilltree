const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkStudyListStructure() {
  console.log('Checking study_lists table structure and existing data...\n');
  
  // Check one of the existing Grade vocabulary lists to see its user_id
  const { data: sampleList, error } = await supabase
    .from('study_lists')
    .select('*')
    .eq('name', 'Grade 2 Vocabulary')
    .single();
    
  if (error) {
    console.error('Error fetching sample list:', error);
  } else {
    console.log('Sample existing list (Grade 2 Vocabulary):');
    console.log('- user_id:', sampleList.user_id);
    console.log('- is_public:', sampleList.is_public);
    console.log('- created_at:', sampleList.created_at);
    console.log('\nWe need to use the same user_id for creating new lists.');
    
    // Return the user_id to use for creating new lists
    return sampleList.user_id;
  }
  
  return null;
}

checkStudyListStructure()
  .then(userId => {
    if (userId) {
      console.log(`\nUse this user_id for creating new lists: ${userId}`);
    }
  })
  .catch(console.error);