const { createClient } = require('@supabase/supabase-js');

// Supabase configuration - using service role key for elevated permissions
const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTI0MTMzNSwiZXhwIjoyMDcwODE3MzM1fQ.x-QbhMeO7HzECupWqq_XuHXeTbQmQwvVKasC61jb7Ws';

const supabase = createClient(supabaseUrl, supabaseKey);

async function createSpellingBeeStudyLists() {
  console.log('Creating Scripps Spelling Bee study lists...');
  
  try {
    // Get the first existing user to own these public study lists
    const { data: users, error: userError } = await supabase
      .from('users')
      .select('id')
      .limit(1);
    
    if (userError || !users || users.length === 0) {
      console.error('No users found in database:', userError);
      return;
    }
    
    const SYSTEM_USER_ID = users[0].id;
    console.log('Using user ID:', SYSTEM_USER_ID);
    
    // Study lists to create
    const studyLists = [
      {
        user_id: SYSTEM_USER_ID,
        name: 'Scripps One Bee',
        description: 'Words from the Scripps National Spelling Bee One Bee level - designed for beginners',
        color: '#22c55e', // green
        is_public: true
      },
      {
        user_id: SYSTEM_USER_ID,
        name: 'Scripps Two Bee',
        description: 'Words from the Scripps National Spelling Bee Two Bee level - intermediate difficulty',
        color: '#f59e0b', // amber
        is_public: true
      },
      {
        user_id: SYSTEM_USER_ID,
        name: 'Scripps Three Bee',
        description: 'Words from the Scripps National Spelling Bee Three Bee level - advanced difficulty',
        color: '#ef4444', // red
        is_public: true
      }
    ];

    // Create the study lists
    const { data: createdLists, error: listError } = await supabase
      .from('study_lists')
      .insert(studyLists)
      .select();

    if (listError) {
      console.error('Error creating study lists:', listError);
      return;
    }

    console.log(`Created ${createdLists?.length || 0} study lists`);

    // Now populate each list with appropriate words
    for (const list of createdLists || []) {
      await populateStudyListWithWords(list);
    }

    console.log('Successfully created and populated all Scripps Spelling Bee study lists!');

  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

async function populateStudyListWithWords(studyList) {
  console.log(`Populating ${studyList.name} with words...`);
  
  try {
    // Determine difficulty level based on study list name
    let difficultyName;
    if (studyList.name === 'Scripps One Bee') {
      difficultyName = 'One Bee';
    } else if (studyList.name === 'Scripps Two Bee') {
      difficultyName = 'Two Bee';
    } else if (studyList.name === 'Scripps Three Bee') {
      difficultyName = 'Three Bee';
    }

    if (!difficultyName) {
      console.log(`Skipping ${studyList.name} - no matching difficulty level`);
      return;
    }

    // Fetch words with the matching difficulty
    const { data: words, error: wordsError } = await supabase
      .from('spelling_words')
      .select('id, word, definition, source_difficulty')
      .eq('source_difficulty', difficultyName)
      .limit(500); // Limit to 500 words per list to take advantage of larger dataset

    if (wordsError) {
      console.error(`Error fetching words for ${studyList.name}:`, wordsError);
      return;
    }

    if (!words || words.length === 0) {
      console.log(`No words found for difficulty: ${difficultyName}`);
      return;
    }

    // Create study list items
    const studyListItems = words.map(word => ({
      study_list_id: studyList.id,
      item_type: 'spelling_word',
      item_id: word.id,
      item_data: {
        word: word.word,
        definition: word.definition,
        difficulty: difficultyName
      }
    }));

    const { data: createdItems, error: itemsError } = await supabase
      .from('study_list_items')
      .insert(studyListItems);

    if (itemsError) {
      console.error(`Error adding items to ${studyList.name}:`, itemsError);
      return;
    }

    console.log(`Added ${words.length} words to ${studyList.name}`);

  } catch (error) {
    console.error(`Error populating ${studyList.name}:`, error);
  }
}

// Run the script
if (require.main === module) {
  createSpellingBeeStudyLists()
    .then(() => {
      console.log('Script completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Script failed:', error);
      process.exit(1);
    });
}

module.exports = { createSpellingBeeStudyLists };