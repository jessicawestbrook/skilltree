const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Final 28 pronunciations to complete the dataset
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
  'grumpy': 'GRUM-pee',
  'gruyère': 'groo-YAIR',
  'guam': 'GWAHM',
  'guan': 'GWAHN',
  'guanine': 'GWAH-neen',
  'guapena': 'gwah-PEH-nah',
  'guarantor': 'gar-un-TOR',
  'guardian': 'GAR-dee-un',
  'guarnerius': 'gwar-NAIR-ee-us',
  'guava': 'GWAH-vuh',
  'guayabera': 'gwy-uh-BAIR-uh',
  'gubernatorial': 'goo-ber-nuh-TOR-ee-ul',
  'gudgeon': 'GUJ-un',
  'guerilla': 'guh-RIL-uh',
  'guerite': 'guh-REET',
  'gueritegallivat': 'guh-REET GAL-i-vat',
  'guerrilla': 'guh-RIL-uh',
  'guess': 'GES',
  'gueule': 'GEL',
  'guffaw': 'guh-FAW',
  'guichet': 'gee-SHAY',
  'guido': 'GEE-doh',
  'guidonian': 'gwy-DOH-nee-un',
  'guilloche': 'gi-LOHSH',
  'guineas': 'GIN-eez',
  'gules': 'GYOOLZ',
  'gullet': 'GUL-it',
  'gullibility': 'gul-uh-BIL-i-tee',
  'gummy': 'GUM-ee',
  'gumption': 'GUMP-shun',
  'gung': 'GUNG',
  'gurdy': 'GER-dee',
  'gurmukhi': 'goor-MUK-hee',
  'gurmukhigyascutus': 'goor-MUK-hee jy-AS-kyoo-tus',
  'gurney': 'GER-nee',
  'gurneysanctimonious': 'GER-nee sangk-tuh-MOH-nee-us',
  'gushedchina': 'GUSHT CHY-nuh',
  'gustatory': 'GUS-tuh-tor-ee',
  'gusto': 'GUS-toh',
  'gutter': 'GUT-er',
  'gyascutus': 'jy-AS-kyoo-tus',
  'gyascutusgyokuro': 'jy-AS-kyoo-tus joh-koo-ROH',
  'gymnastics': 'jim-NAS-tiks',
  'gyokuro': 'joh-koo-ROH',
  'gypsophila': 'jip-SOF-i-luh',
  'gypsum': 'JIP-sum',
  'gyrocopter': 'JY-roh-kop-ter',
  'gyttja': 'GIT-yah'
};

async function completePronunciations() {
  try {
    console.log('Completing final pronunciation updates...');
    
    // Get all remaining words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} words still missing pronunciation`);
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
    
    console.log(`\nFinal batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`Words still not found: ${notFound.length}`);
      notFound.forEach(word => console.log(`- ${word}`));
    }
    
    // Final progress check
    const { data: finalStats } = await supabase
      .from('spelling_words')
      .select('pronunciation_guide');
      
    const finalTotal = finalStats.length;
    const finalWithPronunciation = finalStats.filter(w => w.pronunciation_guide).length;
    const finalProgress = ((finalWithPronunciation/finalTotal)*100).toFixed(1);
    
    console.log(`\n🎉 FINAL STATUS: ${finalWithPronunciation}/${finalTotal} (${finalProgress}%)`);
    
    if (finalWithPronunciation === finalTotal) {
      console.log('🎉 PRONUNCIATION UPDATE COMPLETE! All words now have pronunciation guides.');
    }
    
  } catch (error) {
    console.error('Final batch failed:', error);
  }
}

completePronunciations();