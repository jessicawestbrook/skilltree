const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function displayGeneratedContent() {
  console.log('=== DISPLAYING GENERATED CONTENT ===\n');
  
  try {
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('word, definition, example_sentence, pronunciation_guide, etymology')
      .not('definition', 'is', null)
      .not('example_sentence', 'is', null)
      .order('word')
      .limit(20);

    if (error) {
      throw new Error(`Error fetching words: ${error.message}`);
    }

    if (!words || words.length === 0) {
      console.log('No words with generated content found.');
      return;
    }

    console.log(`Found ${words.length} words with generated content:\n`);

    words.forEach((word, index) => {
      console.log(`${index + 1}. WORD: "${word.word.toUpperCase()}"`);
      console.log(`   Definition: ${word.definition}`);
      console.log(`   Example: ${word.example_sentence}`);
      if (word.pronunciation_guide) {
        console.log(`   Pronunciation: ${word.pronunciation_guide}`);
      }
      if (word.etymology) {
        console.log(`   Etymology: ${word.etymology}`);
      }
      console.log('');
    });

  } catch (error) {
    console.error('Error displaying generated content:', error);
  }
}

displayGeneratedContent();