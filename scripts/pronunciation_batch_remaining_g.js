const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Remaining G-words pronunciations
const pronunciations = {
  'gone': 'GAWN',
  'gonzo': 'GON-zoh',
  'goober': 'GOO-ber',
  'goods': 'GOODZ',
  'goofy': 'GOO-fee',
  'google': 'GOO-gul',
  'googly': 'GOO-glee',
  'googol': 'GOO-gol',
  'goondie': 'GOON-dee',
  'goosander': 'goo-SAN-der',
  'gotcha': 'GOT-chuh',
  'greens': 'GREENZ',
  'grits': 'GRITS',
  'grout': 'GROWT',
  'grouth': 'GROWTH',
  'gushedchina': 'GUSHT CHY-nuh',
  'gustatory': 'GUS-tuh-tor-ee',
  'gusto': 'GUS-toh',
  'gutter': 'GUT-er'
};

async function updateRemainingGWords() {
  try {
    console.log('Processing remaining G-words pronunciation batch...');
    
    // Get remaining G-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'g%');
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} remaining G-words missing pronunciation`);
    let updated = 0;
    let notFound = [];
    
    for (const wordData of wordsToUpdate) {
      const word = wordData.word;
      const pronunciation = pronunciations[word] || pronunciations[word.toLowerCase()];
      
      if (pronunciation) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ pronunciation_guide: pronunciation })
          .eq('id', wordData.id);
          
        if (updateError) {
          console.error(`Failed to update ${word}:`, updateError);
        } else {
          console.log(`✓ Added pronunciation for ${word}: ${pronunciation}`);
          updated++;
        }
        
        // Small delay to avoid rate limits
        await new Promise(resolve => setTimeout(resolve, 50));
      } else {
        notFound.push(word);
      }
    }
    
    console.log(`\nRemaining G-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`G-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 20) {
        console.log('Missing G-words:');
        notFound.forEach(word => console.log(`- ${word}`));
      }
    }
    
    // Overall progress check
    const { count: totalCount } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });
      
    const { count: withPronunciation } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .not('pronunciation_guide', 'is', null);
      
    const progress = ((withPronunciation/totalCount)*100).toFixed(1);
    console.log(`\nOverall progress: ${withPronunciation}/${totalCount} (${progress}%)`);
    
  } catch (error) {
    console.error('Remaining G-words batch failed:', error);
  }
}

updateRemainingGWords();