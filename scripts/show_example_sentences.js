const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function showExampleSentences() {
  console.log('=== EXAMPLE SENTENCES GENERATED ===\n');
  
  try {
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('word, example_sentence')
      .not('example_sentence', 'is', null)
      .order('word')
      .limit(50);

    if (error) {
      throw new Error(`Error fetching words: ${error.message}`);
    }

    if (!words || words.length === 0) {
      console.log('No words with example sentences found.');
      return;
    }

    console.log(`Example sentences for ${words.length} words:\n`);

    words.forEach((word, index) => {
      console.log(`${index + 1}. "${word.word}" -> ${word.example_sentence}`);
    });

  } catch (error) {
    console.error('Error showing example sentences:', error);
  }
}

showExampleSentences();