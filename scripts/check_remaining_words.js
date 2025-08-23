const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkRemainingWords() {
  console.log('=== CHECKING REMAINING WORDS NEEDING CONTENT ===\n');
  
  try {
    // Count words that still need content
    const { data: needingContent, error } = await supabase
      .from('spelling_words')
      .select('word, definition, example_sentence, pronunciation_guide, etymology', { count: 'exact' })
      .or('definition.is.null,example_sentence.is.null,pronunciation_guide.is.null,etymology.is.null')
      .limit(10);

    if (error) {
      throw new Error(`Error fetching words needing content: ${error.message}`);
    }

    console.log(`Words still needing some content:`);
    needingContent.forEach((word, index) => {
      const missing = [];
      if (!word.definition) missing.push('definition');
      if (!word.example_sentence) missing.push('example_sentence');
      if (!word.pronunciation_guide) missing.push('pronunciation');
      if (!word.etymology) missing.push('etymology');
      
      console.log(`  ${index + 1}. "${word.word}" - missing: ${missing.join(', ')}`);
    });

    // Get total counts
    const { count: totalWords } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });

    const { count: wordsWithAllContent } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .not('definition', 'is', null)
      .not('example_sentence', 'is', null)
      .not('pronunciation_guide', 'is', null)
      .not('etymology', 'is', null);

    const { count: wordsNeedingContent } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .or('definition.is.null,example_sentence.is.null,pronunciation_guide.is.null,etymology.is.null');

    console.log(`\n📊 SUMMARY:`);
    console.log(`  Total words: ${totalWords}`);
    console.log(`  Words with complete content: ${wordsWithAllContent}`);
    console.log(`  Words needing some content: ${wordsNeedingContent}`);

  } catch (error) {
    console.error('Error checking remaining words:', error);
  }
}

checkRemainingWords();