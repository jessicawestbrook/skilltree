const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkLegitimateWords() {
  console.log('Checking for legitimate words with missing content...\n');
  
  // Get simple, legitimate-looking words that need content
  const { data, error } = await supabase
    .from('spelling_words')
    .select('word, definition, example_sentence, pronunciation_guide, etymology')
    .or('definition.is.null,example_sentence.is.null,pronunciation_guide.is.null,etymology.is.null')
    .order('word')
    .limit(30);

  if (error) {
    console.error('Error:', error);
    return;
  }

  console.log('Sample of words needing content:');
  data.forEach(w => {
    const missing = [];
    if (!w.definition) missing.push('def');
    if (!w.example_sentence) missing.push('example');
    if (!w.pronunciation_guide) missing.push('pronunciation');
    if (!w.etymology) missing.push('etymology');
    
    // Check if it looks like a concatenated word
    const isConcatenated = /[a-z][A-Z]/.test(w.word) || 
                          (w.word.length > 15 && !w.word.includes('-') && !w.word.includes(' '));
    
    const status = isConcatenated ? '[CONCATENATED]' : '[VALID]';
    console.log(`  ${status} ${w.word} | Missing: ${missing.join(', ')}`);
  });
  
  // Count concatenated vs valid words
  const { data: allWords } = await supabase
    .from('spelling_words')
    .select('word')
    .or('definition.is.null,example_sentence.is.null,pronunciation_guide.is.null,etymology.is.null');
    
  let concatenatedCount = 0;
  let validCount = 0;
  
  allWords.forEach(w => {
    const isConcatenated = /[a-z][A-Z]/.test(w.word) || 
                          (w.word.length > 20 && !w.word.includes('-') && !w.word.includes(' '));
    if (isConcatenated) {
      concatenatedCount++;
    } else {
      validCount++;
    }
  });
  
  console.log('\n=== SUMMARY ===');
  console.log(`Total words needing content: ${allWords.length}`);
  console.log(`Likely concatenated/invalid: ${concatenatedCount}`);
  console.log(`Likely valid words: ${validCount}`);
  
  // Check some specific common words
  const { data: commonWords } = await supabase
    .from('spelling_words')
    .select('word, definition, example_sentence')
    .in('word', ['difficulty', 'grown-ups', 'hem', 'polo', 'drum', 'mix', 'drool', 'pie'])
    .order('word');
    
  console.log('\n=== COMMON WORDS STATUS ===');
  commonWords?.forEach(w => {
    console.log(`  ${w.word}:`);
    console.log(`    Definition: ${w.definition ? '✓' : '✗ Missing'}`);
    console.log(`    Example: ${w.example_sentence ? '✓' : '✗ Missing'}`);
  });
}

checkLegitimateWords();