const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Final remaining M-words pronunciations
const pronunciations = {
  'mackinaw': 'MAK-uh-naw',
  'malapropism': 'MAL-uh-prop-izm',
  'mambomanacle': 'MAM-boh MAN-uh-kul',
  'marionette': 'mair-ee-uh-NET',
  'mariposa': 'mair-uh-POH-suh',
  'maritime': 'MAIR-uh-tym',
  'mark': 'MARK',
  'marked': 'MARKT',
  'marring': 'MAIR-ing',
  'marry': 'MAIR-ee',
  'mars': 'MARZ',
  'masse': 'ma-SAY',
  'masses': 'MAS-iz',
  'mässig': 'MESS-ikh',
  'matriculation': 'muh-trik-yuh-LAY-shun',
  'matrimony': 'MAT-ruh-moh-nee',
  'memorandum': 'mem-uh-RAN-dum',
  'memorial': 'muh-MOR-ee-ul',
  'menacing': 'MEN-uh-sing',
  'menagerie': 'muh-NAJ-uh-ree',
  'menaia': 'muh-NY-uh',
  'mendacious': 'men-DAY-shus',
  'mendicity': 'men-DIS-uh-tee',
  'menial': 'MEE-nee-ul',
  'meningitis': 'men-in-JY-tis',
  'menthol': 'MEN-thol',
  'mention': 'MEN-shun',
  'mentor': 'MEN-tor',
  'mephitic': 'muh-FIT-ik',
  'merak': 'MEE-rak',
  'mercenary': 'MER-suh-nair-ee',
  'merchandise': 'MER-chun-dyz',
  'mercury': 'MER-kyuh-ree',
  'merely': 'MEER-lee',
  'merfolk': 'MER-fohk',
  'merganser': 'mer-GAN-ser',
  'meridian': 'muh-RID-ee-un',
  'meringue': 'muh-RANG',
  'merino': 'muh-REE-noh',
  'merlin': 'MER-lin',
  'merriam': 'MAIR-ee-um',
  'merrier': 'MAIR-ee-er',
  'merrimack': 'MAIR-uh-mak',
  'millegrain': 'MIL-uh-grayn',
  'millennial': 'muh-LEN-ee-ul',
  'ministrations': 'min-uh-STRAY-shunz',
  'minotaur': 'MIN-uh-taw',
  'misinterpret': 'mis-in-TER-prit',
  'mislead': 'mis-LEED',
  'miss': 'MIS',
  'mince': 'MINS',
  'monk': 'MUNGK'
};

async function updateFinalMWords() {
  try {
    console.log('Processing final remaining M-words...');
    
    // Get all remaining M-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'm%');
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} final M-words missing pronunciation`);
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
    
    console.log(`\nFinal M-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`M-words still not found: ${notFound.length}`);
      notFound.forEach(word => console.log(`- ${word}`));
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
    console.error('Final M-words batch failed:', error);
  }
}

updateFinalMWords();