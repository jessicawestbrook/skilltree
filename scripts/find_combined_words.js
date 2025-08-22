const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function findCombinedWords() {
  try {
    const { data: allWords, error } = await supabase
      .from('spelling_words')
      .select('word, definition, example_sentence')
      .order('word');
      
    if (error) {
      console.error('Error:', error);
      return;
    }
    
    console.log(`Analyzing ${allWords.length} words for potential combinations...`);
    const suspiciousWords = [];
    
    allWords.forEach(entry => {
      const word = entry.word;
      
      // Look for obvious combined words patterns
      const isSuspicious = 
        word.length > 20 ||  // Very long words
        (word.length > 12 && /[a-z][A-Z]/.test(word)) ||  // camelCase
        (word.length > 10 && word.includes('the')) ||     // 'the' in middle
        (word.length > 10 && word.includes('and')) ||     // 'and' in middle
        (word.includes(' ') && word.split(' ').length > 1) ||  // Already has spaces
        (word.length > 15 && !/[aeiou]/.test(word.slice(-3))) ||  // Long word ending without vowels
        (word.length > 12 && /[bcdfghjklmnpqrstvwxyz]{4,}/.test(word)); // 4+ consecutive consonants
      
      if (isSuspicious) {
        suspiciousWords.push(entry);
      }
    });
    
    console.log(`Found ${suspiciousWords.length} suspicious words:`);
    console.log('='.repeat(50));
    
    suspiciousWords.forEach((entry, index) => {
      console.log(`${index + 1}. Word: "${entry.word}" (${entry.word.length} chars)`);
      if (entry.definition) {
        console.log(`   Definition: ${entry.definition.substring(0, 100)}...`);
      } else {
        console.log('   Definition: NO DEFINITION');
      }
      console.log('');
    });
    
    // Check for words with missing data
    const { data: missingData, error: missingError } = await supabase
      .from('spelling_words')
      .select('word, definition, example_sentence, pronunciation_guide, etymology')
      .or('definition.is.null,example_sentence.is.null,pronunciation_guide.is.null,etymology.is.null')
      .limit(20);
      
    if (!missingError && missingData.length > 0) {
      console.log('\\n' + '='.repeat(50));
      console.log('Words with missing data:');
      console.log('='.repeat(50));
      missingData.forEach(entry => {
        console.log(`Word: ${entry.word}`);
        console.log(`  Definition: ${entry.definition ? 'YES' : 'MISSING'}`);
        console.log(`  Example: ${entry.example_sentence ? 'YES' : 'MISSING'}`);
        console.log(`  Pronunciation: ${entry.pronunciation_guide ? 'YES' : 'MISSING'}`);
        console.log(`  Etymology: ${entry.etymology ? 'YES' : 'MISSING'}`);
        console.log('');
      });
    }
    
  } catch (error) {
    console.error('Script error:', error);
  }
}

findCombinedWords();