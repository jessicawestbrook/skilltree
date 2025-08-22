const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Common pronunciation patterns and rules for respelling
const pronunciationMap = {
  'amused': 'uh-MYOOZD',
  'cinerarium': 'sin-uh-RAIR-ee-um',
  'pouch': 'POWCH',
  'polemic': 'puh-LEM-ik',
  'angola': 'an-GOH-luh',
  'the': 'thuh',
  'contours': 'KON-toorz',
  'Acadians': 'uh-KAY-dee-unz',
  'angular': 'ANG-gyuh-ler',
  'concomitant': 'kuhn-KOM-i-tunt',
  'circumspectly': 'SER-kum-spekt-lee',
  'cirrhosis': 'suh-ROH-sis',
  'with': 'with',
  'gargantuan': 'gar-GAN-choo-un',
  'kitchen': 'KICH-un',
  'pneumonia': 'noo-MOH-nyuh',
  'presence': 'PREZ-unts',
  'politesse': 'pol-i-TES',
  'page': 'PAYJ',
  'Bangalore': 'BANG-guh-lor',
  'sizzle': 'SIZ-ul',
  'Ramadhan': 'ram-uh-DAHN',
  'Yankee': 'YANG-kee',
  'sparrow': 'SPAR-oh',
  'craquelure': 'krak-LOOR',
  'propitious': 'pruh-PISH-us',
  'constant': 'KON-stunt',
  'crockery': 'KROK-uh-ree',
  'evo': 'EE-voh',
  'fondant': 'FON-dunt',
  'piper': 'PY-per',
  'ellipsis': 'ih-LIP-sis',
  'balm': 'BAHM',
  'gauze': 'GAWZ',
  'leeward': 'LEE-werd',
  'pinyon': 'PIN-yon',
  'zazen': 'ZAH-zen',
  'demolition': 'dem-uh-LISH-un',
  'menorahs': 'muh-NOR-uhz',
  'landline': 'LAND-lyn',
  'pronaos': 'proh-NAY-os',
  'kimchee': 'KIM-chee',
  'lantern': 'LAN-tern',
  'hurly': 'HER-lee',
  'dysfunctional': 'dis-FUNK-shuh-nul',
  'law': 'LAW',
  'leander': 'lee-AN-der',
  'proscenium': 'proh-SEE-nee-um',
  'volery': 'VOH-luh-ree',
  'volition': 'voh-LISH-un'
};

async function updatePronunciations() {
  try {
    console.log('Continuing pronunciation updates...');
    
    // Get all words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} words missing pronunciation`);
    let updated = 0;
    let remaining = [];
    
    for (const wordData of wordsToUpdate) {
      const word = wordData.word;
      const pronunciation = pronunciationMap[word] || pronunciationMap[word.toLowerCase()];
      
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
        remaining.push(word);
      }
    }
    
    console.log(`\nCompleted: ${updated} pronunciations added`);
    console.log(`Remaining words without pronunciation: ${remaining.length}`);
    
    if (remaining.length > 0) {
      console.log('\nWords still needing pronunciation:');
      remaining.slice(0, 20).forEach(word => console.log(`- ${word}`));
      if (remaining.length > 20) {
        console.log(`... and ${remaining.length - 20} more`);
      }
    }
    
    // Final progress check
    const { data: finalStats } = await supabase
      .from('spelling_words')
      .select('pronunciation_guide');
      
    const total = finalStats.length;
    const withPronunciation = finalStats.filter(w => w.pronunciation_guide).length;
    const progress = ((withPronunciation/total)*100).toFixed(1);
    
    console.log(`\nFinal progress: ${withPronunciation}/${total} (${progress}%)`);
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

updatePronunciations();