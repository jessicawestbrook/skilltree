const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function showMoreExamples() {
  // Get a variety of populated words
  const { data: words, error } = await supabase
    .from('spelling_words')
    .select('word, definition, example_sentence, pronunciation_guide, etymology, source_difficulty')
    .not('definition', 'is', null)
    .order('word')
    .limit(15);

  if (error) {
    console.error('Error:', error);
    return;
  }

  console.log('=== SAMPLE OF POPULATED WORDS ===\n');
  
  words.forEach((w, index) => {
    console.log(`${index + 1}. Word: "${w.word}" [${w.source_difficulty || 'No source difficulty'}]`);
    console.log(`   Definition: ${w.definition}`);
    console.log(`   Example: ${w.example_sentence}`);
    console.log(`   Pronunciation: ${w.pronunciation_guide}`);
    console.log(`   Etymology: ${w.etymology}`);
    console.log('   ---');
  });

  // Also get some common words specifically
  console.log('\n=== COMMON WORDS ===\n');
  
  const { data: commonWords } = await supabase
    .from('spelling_words')
    .select('word, definition, example_sentence, pronunciation_guide')
    .in('word', ['difficulty', 'drum', 'pie', 'mix', 'being', 'art', 'awe'])
    .not('definition', 'is', null)
    .order('word');

  if (commonWords && commonWords.length > 0) {
    commonWords.forEach(w => {
      console.log(`Word: "${w.word}"`);
      console.log(`Definition: ${w.definition}`);
      console.log(`Example: ${w.example_sentence}`);
      console.log(`Pronunciation: ${w.pronunciation_guide}`);
      console.log('---');
    });
  } else {
    console.log('No common words have been populated yet.');
  }
}

showMoreExamples();