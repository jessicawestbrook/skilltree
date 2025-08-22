const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// N-words pronunciations
const pronunciations = {
  'nabal': 'NAY-bul',
  'nacelle': 'nuh-SEL',
  'nacho': 'NAH-choh',
  'nada': 'NAH-dah',
  'nagged': 'NAGD',
  'nahcolite': 'NAH-kuh-lyt',
  'nails': 'NAYLZ',
  'nainsook': 'NAYN-sook',
  'naissant': 'NAY-sunt',
  'naissantadieu': 'NAY-sunt ah-DYOO',
  'naïveté': 'nah-eev-TAY',
  'named': 'NAYMD',
  'names': 'NAYMZ',
  'namesake': 'NAYM-sayk',
  'namibian': 'nuh-MIB-ee-un',
  'nanotechnology': 'nan-oh-tek-NOL-uh-jee',
  'napkin': 'NAP-kin',
  'napoleon': 'nuh-POH-lee-un',
  'narcissus': 'nar-SIS-us',
  'narcotic': 'nar-KOT-ik',
  'narrative': 'NAIR-uh-tiv',
  'narrow': 'NAIR-oh',
  'nascent': 'NAS-unt',
  'nasturtium': 'nuh-STER-shum',
  'natatorium': 'nay-tuh-TOR-ee-um',
  'nation': 'NAY-shun',
  'national': 'NASH-uh-nul',
  'native': 'NAY-tiv',
  'nativity': 'nuh-TIV-uh-tee',
  'natural': 'NACH-er-ul',
  'nature': 'NAY-cher',
  'naught': 'NAWT',
  'naughty': 'NAW-tee',
  'nausea': 'NAW-zee-uh',
  'nautical': 'NAW-ti-kul',
  'nautilus': 'NAW-tuh-lus',
  'naval': 'NAY-vul',
  'nave': 'NAYV',
  'navel': 'NAY-vul',
  'navigate': 'NAV-uh-gayt',
  'navy': 'NAY-vee',
  'near': 'NEER',
  'nearby': 'NEER-by',
  'nearest': 'NEER-ist',
  'nearly': 'NEER-lee',
  'neat': 'NEET',
  'nebraska': 'nuh-BRAS-kuh',
  'nebula': 'NEB-yuh-luh',
  'nebular': 'NEB-yuh-ler',
  'necessary': 'NES-uh-ser-ee',
  'neck': 'NEK',
  'nectar': 'NEK-ter',
  'need': 'NEED',
  'needle': 'NEE-dul',
  'nefarious': 'nuh-FAIR-ee-us',
  'negative': 'NEG-uh-tiv',
  'neglect': 'nuh-GLEKT',
  'negligee': 'neg-luh-ZHAY',
  'negligent': 'NEG-luh-junt',
  'negotiate': 'nuh-GOH-shee-ayt',
  'neighbor': 'NAY-ber',
  'neither': 'NEE-ther',
  'nemesis': 'NEM-uh-sis',
  'neon': 'NEE-on',
  'neonbeeswax': 'NEE-on BEEZ-waks',
  'neophyte': 'NEE-uh-fyt',
  'neoterism': 'nee-OT-uh-rizm',
  'nepal': 'nuh-PAWL',
  'nephew': 'NEF-yoo',
  'nephrolith': 'NEF-roh-lith',
  'nerve': 'NERV',
  'nervous': 'NER-vus',
  'nest': 'NEST',
  'nestle': 'NES-ul',
  'net': 'NET',
  'nether': 'NETH-er',
  'nettle': 'NET-ul',
  'network': 'NET-werk',
  'neural': 'NOOR-ul',
  'neurology': 'noo-ROL-uh-jee',
  'neuron': 'NOOR-on',
  'neuropathynoun': 'noo-ROP-uh-thee NOWN',
  'neurosis': 'noo-ROH-sis',
  'neuter': 'NOO-ter',
  'neutral': 'NOO-trul',
  'neutron': 'NOO-tron',
  'nevada': 'nuh-VAD-uh',
  'never': 'NEV-er',
  'nevertheless': 'nev-er-thuh-LES',
  'new': 'NOO',
  'newbienirvana': 'NOO-bee neer-VAH-nuh',
  'newborn': 'NOO-born',
  'newer': 'NOO-er',
  'newest': 'NOO-ist',
  'newly': 'NOO-lee',
  'news': 'NOOZ',
  'newspaper': 'NOOZ-pay-per',
  'next': 'NEKST',
  'nexus': 'NEK-sus',
  'niacin': 'NY-uh-sin',
  'nib': 'NIB',
  'nibble': 'NIB-ul',
  'nice': 'NYS',
  'niche': 'NEESH',
  'nick': 'NIK',
  'nickel': 'NIK-ul',
  'nickname': 'NIK-naym',
  'nicotine': 'NIK-uh-teen',
  'niece': 'NEES',
  'nifty': 'NIF-tee',
  'night': 'NYT',
  'nightingale': 'NY-tin-gayl',
  'nightmare': 'NYT-mair',
  'nine': 'NYN',
  'nineteen': 'nyn-TEEN',
  'ninety': 'NYN-tee',
  'ninth': 'NYNTH',
  'nip': 'NIP',
  'nipple': 'NIP-ul',
  'nirvana': 'neer-VAH-nuh',
  'nitpick': 'NIT-pik',
  'nitrate': 'NY-trayt',
  'nitratejoinery': 'NY-trayt JOY-nuh-ree',
  'nitrogen': 'NY-truh-jun',
  'nitroglycerin': 'ny-troh-GLIS-er-in',
  'niveaurouille': 'nee-VOH ROO-ee',
  'no': 'NOH',
  'noah': 'NOH-uh',
  'noble': 'NOH-bul',
  'nobody': 'NOH-bod-ee',
  'nocturnal': 'nok-TER-nul',
  'nod': 'NOD',
  'node': 'NOHD',
  'noel': 'noh-EL',
  'noise': 'NOYZ',
  'nomad': 'NOH-mad',
  'nomenclature': 'NOH-mun-klay-cher',
  'nominal': 'NOM-uh-nul',
  'nominate': 'NOM-uh-nayt',
  'non': 'NON',
  'nonchalant': 'non-shuh-LAHNT',
  'none': 'NUN',
  'nonpareil': 'non-puh-REL',
  'nonsense': 'NON-sens',
  'noodle': 'NOO-dul',
  'noon': 'NOON',
  'noose': 'NOOS',
  'nor': 'NOR',
  'norm': 'NORM',
  'normal': 'NOR-mul',
  'norman': 'NOR-mun',
  'north': 'NORTH',
  'northern': 'NOR-thern',
  'norovirus': 'NOR-oh-vy-rus',
  'nose': 'NOHZ',
  'nostalgia': 'no-STAL-juh',
  'nostradame': 'nos-truh-DAHM',
  'nostril': 'NOS-tril',
  'not': 'NOT',
  'notable': 'NOH-tuh-bul',
  'notary': 'NOH-tuh-ree',
  'notation': 'noh-TAY-shun',
  'notch': 'NOCH',
  'note': 'NOHT',
  'notebook': 'NOHT-book',
  'noted': 'NOH-tid',
  'noteworthy': 'NOHT-wer-thee',
  'nothing': 'NUTH-ing',
  'notice': 'NOH-tis',
  'notify': 'NOH-tuh-fy',
  'notion': 'NOH-shun',
  'notorious': 'noh-TOR-ee-us',
  'noun': 'NOWN',
  'nourish': 'NER-ish',
  'novel': 'NOV-ul',
  'novelist': 'NOV-ul-ist',
  'novelty': 'NOV-ul-tee',
  'november': 'noh-VEM-ber',
  'novice': 'NOV-is',
  'now': 'NOW',
  'nub': 'NUB',
  'nubile': 'NOO-byl',
  'nuce': 'NOOS',
  'nuclear': 'NOO-klee-er',
  'nucleus': 'NOO-klee-us',
  'nude': 'NOOD',
  'nudge': 'NUJ',
  'nugget': 'NUG-it',
  'nuisance': 'NOO-suns',
  'null': 'NUL',
  'nullify': 'NUL-uh-fy',
  'numb': 'NUM',
  'number': 'NUM-ber',
  'numeral': 'NOO-mer-ul',
  'numeric': 'noo-MAIR-ik',
  'numerous': 'NOO-mer-us',
  'nun': 'NUN',
  'nuncio': 'NUN-see-oh',
  'nuptial': 'NUP-shul',
  'nurse': 'NERS',
  'nursery': 'NER-suh-ree',
  'nurture': 'NER-cher',
  'nut': 'NUT',
  'nutcracker': 'NUT-krak-er',
  'nutmeg': 'NUT-meg',
  'nutrient': 'NOO-tree-unt',
  'nutrition': 'noo-TRISH-un',
  'nutritious': 'noo-TRISH-us',
  'nylon': 'NY-lon',
  'nymph': 'NIMF',
  'nymphal': 'NIM-ful'
};

async function updateNWords() {
  try {
    console.log('Processing N-words pronunciation batch...');
    
    // Get N-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'n%')
      .limit(250);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} N-words missing pronunciation`);
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
    
    console.log(`\nN-words batch completed: ${updated} pronunciations added`);
    
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
    
  } catch (error) {
    console.error('N-words batch failed:', error);
  }
}

updateNWords();