const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Remaining N-words pronunciations
const pronunciations = {
  'narcissus': 'nar-SIS-us',
  'narcotic': 'nar-KOT-ik',
  'nasturtium': 'nuh-STER-shum',
  'natatorium': 'nay-tuh-TOR-ee-um',
  'national': 'NASH-uh-nul',
  'native': 'NAY-tiv',
  'nativity': 'nuh-TIV-uh-tee',
  'naught': 'NAWT',
  'nausea': 'NAW-zee-uh',
  'nautical': 'NAW-ti-kul',
  'naval': 'NAY-vul',
  'nave': 'NAYV',
  'navel': 'NAY-vul',
  'navigate': 'NAV-uh-gayt',
  'navy': 'NAY-vee',
  'nearest': 'NEER-ist',
  'neat': 'NEET',
  'nebraska': 'nuh-BRAS-kuh',
  'nebula': 'NEB-yuh-luh',
  'nebular': 'NEB-yuh-ler',
  'necessary': 'NES-uh-ser-ee',
  'negative': 'NEG-uh-tiv',
  'neglect': 'nuh-GLEKT',
  'negligee': 'neg-luh-ZHAY',
  'negligent': 'NEG-luh-junt',
  'negotiate': 'nuh-GOH-shee-ayt',
  'neighbor': 'NAY-ber',
  'neither': 'NEE-ther',
  'nemesis': 'NEM-uh-sis',
  'neon': 'NEE-on',
  'nerve': 'NERV',
  'nestle': 'NES-ul',
  'net': 'NET',
  'nether': 'NETH-er',
  'nettle': 'NET-ul',
  'neural': 'NOOR-ul',
  'neurology': 'noo-ROL-uh-jee',
  'neuron': 'NOOR-on',
  'neurosis': 'noo-ROH-sis',
  'neuter': 'NOO-ter',
  'neutral': 'NOO-trul',
  'nevada': 'nuh-VAD-uh',
  'nevertheless': 'nev-er-thuh-LES',
  'new': 'NOO',
  'newborn': 'NOO-born',
  'newer': 'NOO-er',
  'newest': 'NOO-ist',
  'newspaper': 'NOOZ-pay-per',
  'nib': 'NIB',
  'nick': 'NIK',
  'nickel': 'NIK-ul',
  'nickname': 'NIK-naym',
  'nicotine': 'NIK-uh-teen',
  'niece': 'NEES',
  'nifty': 'NIF-tee',
  'nightingale': 'NY-tin-gayl',
  'nightmare': 'NYT-mair',
  'nineteen': 'nyn-TEEN',
  'ninety': 'NYN-tee',
  'ninth': 'NYNTH',
  'nip': 'NIP',
  'nipple': 'NIP-ul',
  'nitpick': 'NIT-pik',
  'nitroglycerin': 'ny-troh-GLIS-er-in',
  'no': 'NOH',
  'noah': 'NOH-uh',
  'nod': 'NOD',
  'node': 'NOHD',
  'noel': 'noh-EL',
  'noise': 'NOYZ',
  'nomad': 'NOH-mad',
  'nominate': 'NOM-uh-nayt',
  'non': 'NON',
  'nonchalant': 'non-shuh-LAHNT',
  'noodle': 'NOO-dul',
  'noose': 'NOOS',
  'nor': 'NOR',
  'norm': 'NORM',
  'normal': 'NOR-mul',
  'norman': 'NOR-mun',
  'nostril': 'NOS-tril',
  'not': 'NOT',
  'notary': 'NOH-tuh-ree',
  'notation': 'noh-TAY-shun',
  'notch': 'NOCH',
  'note': 'NOHT',
  'noted': 'NOH-tid',
  'noteworthy': 'NOHT-wer-thee',
  'nothing': 'NUTH-ing',
  'notice': 'NOH-tis',
  'notify': 'NOH-tuh-fy',
  'notion': 'NOH-shun',
  'notorious': 'noh-TOR-ee-us',
  'novel': 'NOV-ul',
  'novelty': 'NOV-ul-tee',
  'november': 'noh-VEM-ber',
  'now': 'NOW',
  'nub': 'NUB',
  'nubile': 'NOO-byl',
  'nuclear': 'NOO-klee-er',
  'nucleus': 'NOO-klee-us',
  'nude': 'NOOD',
  'nudge': 'NUJ',
  'nugget': 'NUG-it',
  'null': 'NUL',
  'nullify': 'NUL-uh-fy',
  'numb': 'NUM',
  'numeral': 'NOO-mer-ul',
  'numeric': 'noo-MAIR-ik',
  'numerous': 'NOO-mer-us',
  'nun': 'NUN',
  'nuncio': 'NUN-see-oh',
  'nuptial': 'NUP-shul',
  'nurse': 'NERS',
  'nursery': 'NER-suh-ree',
  'nut': 'NUT',
  'nutcracker': 'NUT-krak-er',
  'nutmeg': 'NUT-meg',
  'nutrient': 'NOO-tree-unt',
  'nutrition': 'noo-TRISH-un',
  'nutritious': 'noo-TRISH-us',
  'nylon': 'NY-lon',
  'nymph': 'NIMF'
};

async function updateRemainingNWords() {
  try {
    console.log('Processing remaining N-words pronunciation batch...');
    
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
    
    console.log(`\nRemaining N-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`N-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 40) {
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
    console.error('Remaining N-words batch failed:', error);
  }
}

updateRemainingNWords();