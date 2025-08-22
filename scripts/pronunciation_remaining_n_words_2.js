const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Additional N-words pronunciations (supplement to existing script)
const pronunciations = {
  'newt': 'NOOT',
  'niagara': 'ny-AG-uh-ruh',
  'nicoise': 'nee-SWAHZ',
  'nictitate': 'NIK-tih-tayt',
  'nidicolous': 'nih-DIK-uh-lus',
  'nile': 'NYL',
  'nilpotent': 'NIL-poh-tunt',
  'nimbostratus': 'nim-boh-STRAY-tus',
  'nimiety': 'nih-MY-ih-tee',
  'niminy': 'NIM-ih-nee',
  'nimble': 'NIM-bul',
  'nimbly': 'NIM-blee',
  'nimbus': 'NIM-bus',
  'nina': 'NEE-nuh',
  'nincompoop': 'NIN-kum-poop',
  'nintendo': 'nin-TEN-doh',
  'niobium': 'ny-OH-bee-um',
  'nirvana': 'ner-VAH-nuh',
  'nisi': 'NY-sy',
  'niter': 'NY-ter',
  'nitrate': 'NY-trayt',
  'nitric': 'NY-trik',
  'nitride': 'NY-tryd',
  'nitrogen': 'NY-troh-jun',
  'nitrous': 'NY-trus',
  'nitty': 'NIT-ee',
  'nix': 'NIKS',
  'nizam': 'nih-ZAHM',
  'nobby': 'NOB-ee',
  'nobelium': 'noh-BEE-lee-um',
  'nobility': 'noh-BIL-ih-tee',
  'noble': 'NOH-bul',
  'nobleman': 'NOH-bul-mun',
  'nobody': 'NOH-bod-ee',
  'nocturnal': 'nok-TER-nul',
  'nocturne': 'NOK-tern',
  'nodal': 'NOH-dul',
  'nodding': 'NOD-ing',
  'noddy': 'NOD-ee',
  'nodule': 'NOD-yool',
  'noggin': 'NOG-in',
  'noiseless': 'NOYZ-lis',
  'noisome': 'NOY-sum',
  'nomadic': 'noh-MAD-ik',
  'nomenclature': 'NOH-mun-klay-chur',
  'nominal': 'NOM-ih-nul',
  'nomination': 'nom-ih-NAY-shun',
  'nominee': 'nom-ih-NEE',
  'nonage': 'NON-ij',
  'nonce': 'NONS',
  'nonchalance': 'non-shuh-LAHNS',
  'nondescript': 'non-dih-SKRIPT',
  'none': 'NUN',
  'nonentity': 'non-EN-tih-tee',
  'nonetheless': 'nun-thuh-LES',
  'nonpareil': 'non-puh-REL',
  'nonplus': 'non-PLUS',
  'nonsense': 'NON-sens',
  'nonsensical': 'non-SEN-sih-kul',
  'nonviolent': 'non-VY-uh-lunt',
  'nook': 'NOOK',
  'noon': 'NOON',
  'noonday': 'NOON-day',
  'noontime': 'NOON-tym',
  'noose': 'NOOS',
  'nordic': 'NOR-dik',
  'normalize': 'NOR-muh-lyz',
  'normally': 'NOR-mul-lee',
  'normative': 'NOR-muh-tiv',
  'north': 'NORTH',
  'northbound': 'NORTH-bownd',
  'northeast': 'north-EEST',
  'northeastern': 'north-EES-tern',
  'northerly': 'NOR-ther-lee',
  'northern': 'NOR-thern',
  'northernmost': 'NOR-thern-mohst',
  'northward': 'NORTH-werd',
  'northwest': 'north-WEST',
  'northwestern': 'north-WES-tern',
  'nose': 'NOHZ',
  'nosebag': 'NOHZ-bag',
  'nosebleed': 'NOHZ-bleed',
  'nosedive': 'NOHZ-dyv',
  'nosegay': 'NOHZ-gay',
  'nosh': 'NOSH',
  'nostalgia': 'no-STAL-juh',
  'nostalgic': 'no-STAL-jik',
  'nostrum': 'NOS-trum',
  'nosy': 'NOH-zee',
  'notable': 'NOH-tuh-bul',
  'notably': 'NOH-tuh-blee',
  'notarize': 'NOH-tuh-ryz',
  'notch': 'NOCH',
  'notebook': 'NOHT-book',
  'noted': 'NOH-tid',
  'notepad': 'NOHT-pad',
  'noteworthy': 'NOHT-wer-thee',
  'nothing': 'NUTH-ing',
  'nothingness': 'NUTH-ing-nis',
  'notice': 'NOH-tis',
  'noticeable': 'NOH-tis-uh-bul',
  'notification': 'noh-tih-fih-KAY-shun',
  'notify': 'NOH-tuh-fy',
  'notion': 'NOH-shun',
  'notional': 'NOH-shuh-nul',
  'notorious': 'noh-TOR-ee-us',
  'nougat': 'NOO-gut',
  'nought': 'NAWT',
  'noun': 'NOWN',
  'nourish': 'NER-ish',
  'nourishing': 'NER-ish-ing',
  'nourishment': 'NER-ish-munt',
  'nouveau': 'noo-VOH',
  'nova': 'NOH-vuh',
  'novel': 'NOV-ul',
  'novelist': 'NOV-ul-ist',
  'novelty': 'NOV-ul-tee',
  'november': 'noh-VEM-ber',
  'novena': 'noh-VEE-nuh',
  'novice': 'NOV-is',
  'novitiate': 'noh-VISH-ee-it',
  'now': 'NOW',
  'nowadays': 'NOW-uh-dayz',
  'nowhere': 'NOH-wair',
  'noxious': 'NOK-shus',
  'nozzle': 'NOZ-ul'
};

async function updateRemainingNWords2() {
  try {
    console.log('Processing remaining N-words second batch...');
    
    // Get remaining N-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'n%')
      .limit(100);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} remaining N-words missing pronunciation`);
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
    
    console.log(`\nRemaining N-words second batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`N-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 30) {
        console.log('Missing N-words:');
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
    
    // Check if we've reached 90%
    if (progress >= 90.0) {
      console.log('\n🎯 MILESTONE ACHIEVED: 90%+ PRONUNCIATION COVERAGE!');
    }
    
  } catch (error) {
    console.error('Remaining N-words second batch failed:', error);
  }
}

updateRemainingNWords2();