const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

// These are the 50 words we just saw with generated content
const wordsWithContent = [
  'aachen', 'aardvark', 'abaculus', 'abaft', 'abalones', 'abandon', 'abandoned', 
  'abashed', 'abated', 'abattoir', 'abbreviations', 'abdomen', 'aberration', 
  'abeyance', 'abhenry', 'abhijay', 'abhorrence', 'abject', 'ablation', 'ablaut', 
  'ablaze', 'able', 'abnegation', 'abodes', 'abolish', 'abomasum', 'abominable', 
  'aboriginal', 'above', 'abracadabra', 'abraum', 'abrogate', 'abruptly', 
  'abscess', 'abscond', 'absent', 'absolution', 'absorptive', 'abstemious', 
  'abstruse', 'absurdly', 'abundance', 'abysmal', 'acacia', 'acade', 'academese', 
  'academic', 'academy', 'acadians', 'accelerates'
];

async function checkWordStatus() {
  console.log('=== CHECKING WORD STATUS ===\n');
  
  try {
    // Check if these words existed before the recent updates
    const { data: allWords, error } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty, created_at')
      .in('word', wordsWithContent)
      .order('word');

    if (error) {
      throw new Error(`Error fetching words: ${error.message}`);
    }

    console.log(`Status of the 50 words with generated content:\n`);

    const existingWords = [];
    const newWords = [];

    wordsWithContent.forEach(word => {
      const found = allWords.find(w => w.word === word);
      if (found) {
        existingWords.push(found);
      } else {
        newWords.push(word);
      }
    });

    console.log(`EXISTING WORDS (${existingWords.length}):`);
    existingWords.forEach((word, index) => {
      console.log(`  ${index + 1}. "${word.word}" - ${word.source_difficulty} (created: ${word.created_at})`);
    });

    if (newWords.length > 0) {
      console.log(`\nNEW WORDS NOT FOUND (${newWords.length}):`);
      newWords.forEach((word, index) => {
        console.log(`  ${index + 1}. "${word}"`);
      });
    }

    console.log(`\nSUMMARY:`);
    console.log(`- Words that already existed: ${existingWords.length}`);
    console.log(`- Words not found in database: ${newWords.length}`);

  } catch (error) {
    console.error('Error checking word status:', error);
  }
}

checkWordStatus();