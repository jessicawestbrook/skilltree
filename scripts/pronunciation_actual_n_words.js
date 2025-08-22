const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Actual remaining N-words pronunciations
const pronunciations = {
  'naranjilla': 'nah-rahn-HEE-yah',
  'narcoleptic': 'nar-kuh-LEP-tik',
  'narwal': 'NAR-wul',
  'narwhal': 'NAR-wul',
  'nationalism': 'NASH-uh-nul-izm',
  'nattily': 'NAT-uh-lee',
  'naugahyde': 'NAW-guh-hyd',
  'naumachia': 'naw-MAH-kee-uh',
  'nauseam': 'NAW-zee-um',
  'navaho': 'NAV-uh-hoh',
  'navajo': 'NAV-uh-hoh',
  'navigation': 'nav-uh-GAY-shun',
  'navigator': 'NAV-uh-gay-ter',
  'naysayers': 'NAY-say-erz',
  'neapolitan': 'nee-uh-POL-uh-tun',
  'neaten': 'NEE-tun',
  'nebulous': 'NEB-yuh-lus',
  'necessity': 'nuh-SES-uh-tee',
  'necklace': 'NEK-lis',
  'necks': 'NEKS',
  'necromancer': 'NEK-roh-man-ser',
  'necrotic': 'nuh-KROT-ik',
  'nectarine': 'NEK-tuh-reen',
  'needs': 'NEEDZ',
  'neem': 'NEEM',
  'neigh': 'NAY',
  'neighborhood': 'NAY-ber-hood',
  'neighbors': 'NAY-berz',
  'neologism': 'nee-OL-uh-jizm',
  'neonatology': 'nee-oh-nay-TOL-uh-jee',
  'nepotism': 'NEP-uh-tizm',
  'neptune': 'NEP-toon',
  'nerds': 'NERDZ',
  'nereid': 'NEER-ee-id',
  'nerfing': 'NERF-ing',
  'nervily': 'NER-vuh-lee',
  'nescience': 'NESH-ee-unts',
  'netflix': 'NET-fliks',
  'nethinim': 'NETH-uh-nim',
  'netiquette': 'NET-uh-ket',
  'nets': 'NETS',
  'networks': 'NET-werks',
  'neuhauser': 'NOY-how-zer',
  'neuropathy': 'noo-ROP-uh-thee',
  'neuroticism': 'noo-ROT-uh-sizm',
  'newbie': 'NOO-bee',
  'newfoundland': 'NOO-fun-lund',
  'newspapers': 'NOOZ-pay-perz',
  'newsroom': 'NOOZ-room',
  'newsy': 'NOO-zee',
  'newton': 'NOO-tun',
  'nibbled': 'NIB-uld',
  'nicely': 'NYS-lee',
  'niceness': 'NYS-nis',
  'nicer': 'NY-ser',
  'nicest': 'NY-sist',
  'niche': 'NEESH',
  'nickels': 'NIK-ulz',
  'nicks': 'NIKS',
  'nieces': 'NEE-siz',
  'niger': 'NY-jer',
  'nigeria': 'ny-JEER-ee-uh',
  'nightfall': 'NYT-fawl',
  'nightgown': 'NYT-gown',
  'nightlife': 'NYT-lyf',
  'nightly': 'NYT-lee',
  'nightmares': 'NYT-mairz',
  'nightstand': 'NYT-stand',
  'nighttime': 'NYT-tym',
  'nimble': 'NIM-bul',
  'nimbly': 'NIM-blee',
  'nineties': 'NYN-teez',
  'nineteenth': 'nyn-TEENTH',
  'ninetieth': 'NYN-tee-uth',
  'ninety': 'NYN-tee',
  'ninjas': 'NIN-juhz',
  'nipples': 'NIP-ulz',
  'nips': 'NIPS',
  'nitpicking': 'NIT-pik-ing',
  'nitrates': 'NY-trayts',
  'nitric': 'NY-trik',
  'nitrous': 'NY-trus',
  'nits': 'NITS',
  'nitty': 'NIT-ee',
  'nix': 'NIKS',
  'nixon': 'NIK-sun',
  'nobility': 'noh-BIL-uh-tee',
  'nobles': 'NOH-bulz',
  'nobly': 'NOH-blee',
  'nocturne': 'NOK-tern',
  'nods': 'NODZ',
  'nodules': 'NOJ-oolz',
  'noes': 'NOHZ',
  'noetic': 'noh-ET-ik',
  'noisily': 'NOY-zuh-lee',
  'noisy': 'NOY-zee',
  'nomads': 'NOH-madz',
  'nomenclatures': 'NOH-mun-klay-cherz',
  'nominals': 'NOM-uh-nulz',
  'nominally': 'NOM-uh-nuh-lee',
  'nominations': 'nom-uh-NAY-shunz',
  'nominative': 'NOM-uh-nuh-tiv',
  'nominee': 'nom-uh-NEE',
  'nonchalantly': 'non-shuh-LAHNT-lee',
  'nonfiction': 'non-FIK-shun',
  'nonpartisan': 'non-PAR-tuh-zun',
  'nonprofit': 'non-PROF-it',
  'nonsensical': 'non-SEN-si-kul',
  'nonstop': 'non-STOP',
  'noodles': 'NOO-dulz',
  'nooks': 'NOOKS',
  'noonday': 'NOON-day',
  'noontime': 'NOON-tym',
  'nooses': 'NOO-siz',
  'nordic': 'NOR-dik',
  'norms': 'NORMZ',
  'northeast': 'north-EEST',
  'northerly': 'NOR-ther-lee',
  'northernmost': 'NOR-thern-mohst',
  'northward': 'NORTH-werd',
  'northwest': 'north-WEST',
  'noses': 'NOH-ziz',
  'nostalgia': 'no-STAL-juh',
  'nostalgic': 'no-STAL-jik',
  'nostrils': 'NOS-trilz',
  'notables': 'NOH-tuh-bulz',
  'notably': 'NOH-tuh-blee',
  'notaries': 'NOH-tuh-reez',
  'notations': 'noh-TAY-shunz',
  'notches': 'NOCH-iz',
  'notebooks': 'NOHT-books',
  'notes': 'NOHTS',
  'nothingness': 'NUTH-ing-nis',
  'notices': 'NOH-tis-iz',
  'noticing': 'NOH-tis-ing',
  'notification': 'noh-tuh-fuh-KAY-shun',
  'notified': 'NOH-tuh-fyd',
  'notifies': 'NOH-tuh-fyze',
  'notifying': 'NOH-tuh-fy-ing',
  'notions': 'NOH-shunz',
  'notoriety': 'noh-tuh-RY-uh-tee',
  'notoriously': 'noh-TOR-ee-us-lee',
  'nouns': 'NOWNZ',
  'nourished': 'NER-isht',
  'nourishes': 'NER-ish-iz',
  'nourishing': 'NER-ish-ing',
  'nourishment': 'NER-ish-munt',
  'novelist': 'NOV-ul-ist',
  'novelties': 'NOV-ul-teez',
  'novels': 'NOV-ulz',
  'novices': 'NOV-is-iz',
  'nowadays': 'NOW-uh-dayz',
  'nowhere': 'NOH-wair',
  'nozzle': 'NOZ-ul',
  'nuance': 'NOO-ahns',
  'nuanced': 'NOO-ahnst',
  'nubs': 'NUBZ',
  'nuclei': 'NOO-klee-y',
  'nudes': 'NOODZ',
  'nudged': 'NUJD',
  'nudges': 'NUJ-iz',
  'nudging': 'NUJ-ing',
  'nudist': 'NOO-dist',
  'nudity': 'NOO-duh-tee',
  'nuggets': 'NUG-its',
  'nuisances': 'NOO-sun-siz',
  'nullification': 'nul-uh-fuh-KAY-shun',
  'nullified': 'NUL-uh-fyd',
  'nullifies': 'NUL-uh-fyze',
  'nullifying': 'NUL-uh-fy-ing',
  'numbed': 'NUMD',
  'numbing': 'NUM-ing',
  'numbly': 'NUM-lee',
  'numbness': 'NUM-nis',
  'numbers': 'NUM-berz',
  'numbering': 'NUM-ber-ing',
  'numerals': 'NOO-mer-ulz',
  'numerator': 'NOO-mer-ay-ter',
  'numerically': 'noo-MAIR-ik-lee',
  'nums': 'NUMZ',
  'nuns': 'NUNZ',
  'nuncios': 'NUN-see-ohz',
  'nuptials': 'NUP-shulz',
  'nursed': 'NERST',
  'nurseries': 'NER-suh-reez',
  'nurses': 'NER-siz',
  'nursing': 'NER-sing',
  'nurtured': 'NER-cherd',
  'nurtures': 'NER-cherz',
  'nurturing': 'NER-cher-ing',
  'nuts': 'NUTS',
  'nutshell': 'NUT-shel',
  'nutty': 'NUT-ee',
  'nuzzle': 'NUZ-ul',
  'nylons': 'NY-lonz',
  'nymphs': 'NIMFS'
};

async function updateActualNWords() {
  try {
    console.log('Processing actual remaining N-words...');
    
    // Get remaining N-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'n%')
      .limit(200);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} actual N-words missing pronunciation`);
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
    
    console.log(`\nActual N-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`N-words still not found: ${notFound.length}`);
      if (notFound.length <= 20) {
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
    
  } catch (error) {
    console.error('Actual N-words batch failed:', error);
  }
}

updateActualNWords();