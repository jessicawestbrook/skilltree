const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function showDefinitions() {
  console.log('=== DEFINITIONS GENERATED ===\n');
  
  try {
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('word, definition')
      .not('definition', 'is', null)
      .order('word')
      .limit(50);

    if (error) {
      throw new Error(`Error fetching words: ${error.message}`);
    }

    if (!words || words.length === 0) {
      console.log('No words with definitions found.');
      return;
    }

    console.log(`Definitions for ${words.length} words:\n`);

    words.forEach((word, index) => {
      console.log(`${index + 1}. "${word.word}"`);
      console.log(`   ${word.definition}\n`);
    });

  } catch (error) {
    console.error('Error showing definitions:', error);
  }
}

showDefinitions();