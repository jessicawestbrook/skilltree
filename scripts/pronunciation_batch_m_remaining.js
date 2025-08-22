const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// More M-words pronunciations
const pronunciations = {
  'mischievousbionic': 'MIS-chuh-vus by-ON-ik',
  'millisecondmillivolt': 'MIL-uh-sek-und MIL-uh-vohlt',
  'microwavegabled': 'MY-kroh-wayv GAY-buld',
  'midriffteaspoon': 'MID-rif TEE-spoon',
  'millivoltherringbone': 'MIL-uh-vohlt HAIR-ing-bohn',
  'mimeticunabated': 'muh-MET-ik un-uh-BAY-tid',
  'moleculemonopolize': 'MOL-uh-kyool muh-NOP-uh-lyz',
  'monochromefacade': 'MON-uh-krohm fuh-SAHD',
  'monstrositysofa': 'mon-STROS-uh-tee SOH-fuh',
  'morionmortadella': 'MOR-ee-on mor-tuh-DEL-uh',
  'mosquitotarget': 'muh-SKEE-toh TAR-git',
  'motherumbung': 'MUTH-er UM-bung',
  'mouthfilters': 'MOWTH FIL-terz',
  'mugwumpdollars': 'MUG-wump DOL-erz',
  'mulliganmunich': 'MUL-uh-gun MYOO-nik',
  'mustardcruel': 'MUS-terd KROO-ul',
  'muttonchops': 'MUT-un-chops',
  'mythicaln': 'MITH-uh-kul N',
  'marinate': 'MAIR-uh-nayt',
  'mesial': 'MEE-zee-ul',
  'mesopotamian': 'mes-uh-puh-TAY-mee-un',
  'mess': 'MES',
  'message': 'MES-ij',
  'messenger': 'MES-un-jer',
  'metadata': 'MET-uh-day-tuh',
  'metals': 'MET-ulz',
  'metaplasia': 'met-uh-PLAY-zhuh',
  'metastasize': 'muh-TAS-tuh-syz',
  'metatarsal': 'met-uh-TAR-sul',
  'mete': 'MEET',
  'meteor': 'MEE-tee-or',
  'methodology': 'meth-uh-DOL-uh-jee',
  'methods': 'METH-udz',
  'metonic': 'muh-TON-ik',
  'metrical': 'MET-ri-kul',
  'metronome': 'MET-ruh-nohm',
  'metropolis': 'muh-TROP-uh-lis',
  'meunière': 'men-YAIR',
  'mexico': 'MEK-si-koh',
  'mezzanine': 'MEZ-uh-neen',
  'miasma': 'my-AZ-muh',
  'mice': 'MYS',
  'micellar': 'my-SEL-er',
  'michaelmas': 'MIK-ul-mus',
  'michel': 'mee-SHEL',
  'michigander': 'MISH-uh-gan-der',
  'microfiche': 'MY-kroh-feesh',
  'microphone': 'MY-kroh-fohn',
  'midair': 'MID-air',
  'midday': 'MID-day',
  'middle': 'MID-ul',
  'midnight': 'MID-nyt',
  'midriff': 'MID-rif',
  'mien': 'MEEN',
  'might': 'MYT',
  'mighty': 'MY-tee',
  'mignonette': 'min-yuh-NET',
  'migraine': 'MY-grayn',
  'migratory': 'MY-gruh-tor-ee',
  'mildew': 'MIL-doo',
  'mile': 'MYL',
  'miles': 'MYLZ',
  'milieu': 'mil-YER',
  'militant': 'MIL-uh-tunt',
  'military': 'MIL-uh-ter-ee',
  'milk': 'MILK',
  'millegrain': 'MIL-uh-grayn',
  'millennial': 'muh-LEN-ee-ul',
  'millet': 'MIL-it',
  'million': 'MIL-yun',
  'millionaire': 'mil-yun-AIR',
  'millisecond': 'MIL-uh-sek-und',
  'millivolt': 'MIL-uh-vohlt',
  'mimeograph': 'MIM-ee-uh-graf',
  'minacious': 'muh-NAY-shus',
  'mince': 'MINS',
  'mineral': 'MIN-er-ul',
  'minerals': 'MIN-er-ulz',
  'minestra': 'mee-NES-truh',
  'minette': 'mee-NET',
  'minimise': 'MIN-uh-myz',
  'minimize': 'MIN-uh-myz',
  'minimus': 'MIN-uh-mus',
  'miniscule': 'MIN-uh-skyool',
  'ministrations': 'min-uh-STRAY-shunz',
  'ministry': 'MIN-uh-stree',
  'minivan': 'MIN-ee-van',
  'minivets': 'MIN-ee-vets',
  'mink': 'MINGK',
  'minnesota': 'min-uh-SOH-tuh',
  'minnow': 'MIN-oh',
  'minority': 'muh-NOR-uh-tee',
  'minotaur': 'MIN-uh-tor',
  'minuscule': 'muh-NUS-kyool',
  'minute': 'muh-NOOT',
  'minutia': 'muh-NOO-shee-uh',
  'miombo': 'mee-OM-boh',
  'mirach': 'MY-rak',
  'miraculous': 'muh-RAK-yuh-lus',
  'mirage': 'muh-RAZH',
  'miranda': 'muh-RAN-duh',
  'miscellaneous': 'mis-uh-LAY-nee-us',
  'mischief': 'MIS-chif',
  'miscible': 'MIS-uh-bul',
  'misconception': 'mis-kun-SEP-shun',
  'misconstrue': 'mis-kun-STROO',
  'miscreant': 'MIS-kree-unt',
  'misdemeanor': 'mis-duh-MEE-ner',
  'misdemeanour': 'mis-duh-MEE-ner',
  'misericordes': 'mis-uh-ri-KOR-deez',
  'misericords': 'mis-uh-ri-KORDZ',
  'misery': 'MIZ-uh-ree',
  'misinterpret': 'mis-in-TER-prit',
  'mislead': 'mis-LEED',
  'misnomer': 'mis-NOH-mer',
  'miss': 'MIS',
  'missile': 'MIS-ul',
  'mission': 'MISH-un',
  'missive': 'MIS-iv',
  'mistake': 'muh-STAYK',
  'mistaken': 'muh-STAY-kun',
  'mister': 'MIS-ter',
  'mitigative': 'MIT-uh-gay-tiv',
  'mitochondria': 'my-tuh-KON-dree-uh',
  'mittimus': 'MIT-uh-mus',
  'mitty': 'MIT-ee',
  'mixed': 'MIKST',
  'mixture': 'MIKS-cher',
  'mizuna': 'mee-ZOO-nah',
  'mobility': 'moh-BIL-uh-tee',
  'mochi': 'MOH-chee',
  'mockery': 'MOK-uh-ree',
  'modality': 'moh-DAL-uh-tee',
  'model': 'MOD-ul',
  'modem': 'MOH-dem',
  'modern': 'MOD-ern',
  'modesty': 'MOD-uh-stee',
  'modicum': 'MOD-uh-kum',
  'modify': 'MOD-uh-fy',
  'modiste': 'moh-DEEST',
  'modular': 'MOJ-uh-ler',
  'mogul': 'MOH-gul',
  'moiety': 'MOY-uh-tee',
  'moines': 'MOYNZ',
  'moira': 'MOY-ruh',
  'moissanite': 'moy-suh-NYT',
  'moisture': 'MOYS-cher',
  'molars': 'MOH-lerz',
  'molasses': 'muh-LAS-iz',
  'molds': 'MOHLDZ',
  'molecule': 'MOL-uh-kyool',
  'moline': 'moh-LEEN',
  'mollify': 'MOL-uh-fy',
  'mollusk': 'MOL-usk',
  'momentous': 'moh-MEN-tus',
  'monarch': 'MON-ark',
  'monastery': 'MON-uh-ster-ee',
  'monday': 'MUN-day',
  'mondegreen': 'MON-duh-green',
  'money': 'MUN-ee',
  'monitory': 'MON-uh-tor-ee',
  'monk': 'MUNGK',
  'monkey': 'MUNG-kee',
  'monochrome': 'MON-uh-krohm',
  'monocle': 'MON-uh-kul',
  'monopolise': 'muh-NOP-uh-lyz',
  'monopolize': 'muh-NOP-uh-lyz',
  'monotone': 'MON-uh-tohn',
  'monster': 'MON-ster',
  'monstrosity': 'mon-STROS-uh-tee',
  'montage': 'mon-TAZH',
  'month': 'MUNTH',
  'monthly': 'MUNTH-lee',
  'months': 'MUNTHS',
  'monture': 'mon-TUR',
  'monumental': 'mon-yuh-MEN-tul',
  'mood': 'MOOD',
  'moon': 'MOON',
  'moorage': 'MOOR-ij',
  'moose': 'MOOS',
  'moped': 'MOH-ped',
  'moppet': 'MOP-it',
  'mops': 'MOPS',
  'moraine': 'muh-RAYN',
  'moratorium': 'mor-uh-TOR-ee-um',
  'morbidity': 'mor-BID-uh-tee',
  'mordant': 'MOR-dunt',
  'morel': 'muh-REL',
  'mores': 'MOR-ayz',
  'morgana': 'mor-GAN-uh',
  'moribund': 'MOR-uh-bund',
  'morion': 'MOR-ee-on',
  'moroccan': 'muh-ROK-un',
  'morose': 'muh-ROHS',
  'morphological': 'mor-fuh-LOJ-uh-kul',
  'mortadella': 'mor-tuh-DEL-uh',
  'mortal': 'MOR-tul',
  'mortgage': 'MOR-gij',
  'mortician': 'mor-TISH-un',
  'mortification': 'mor-tuh-fuh-KAY-shun',
  'mosaic': 'moh-ZAY-ik',
  'most': 'MOHST',
  'mostaccioli': 'mos-tah-chee-OH-lee',
  'mother': 'MUTH-er',
  'motion': 'MOH-shun',
  'motley': 'MOT-lee',
  'motor': 'MOH-ter',
  'motrin': 'MOH-trin',
  'motto': 'MOT-oh',
  'moulage': 'moo-LAZH',
  'mound': 'MOWND',
  'mountain': 'MOWN-tin',
  'mourners': 'MOR-nerz',
  'mournful': 'MORN-ful',
  'moussaka': 'moo-SAH-kah',
  'mousse': 'MOOS',
  'moustache': 'MUS-tash',
  'move': 'MOOV',
  'movie': 'MOO-vee',
  'movimento': 'moh-vee-MEN-toh',
  'moving': 'MOO-ving',
  'mower': 'MOH-er',
  'moxie': 'MOK-see',
  'mozo': 'MOH-zoh',
  'muchacha': 'moo-CHAH-chah',
  'muddy': 'MUD-ee',
  'muesli': 'MYOOZ-lee',
  'mufti': 'MUF-tee',
  'mugs': 'MUGZ',
  'muktuk': 'MUK-tuk',
  'mulberry': 'MUL-ber-ee',
  'mule': 'MYOOL',
  'muliebrity': 'myoo-lee-EB-ruh-tee',
  'mulish': 'MYOO-lish',
  'mulligan': 'MUL-uh-gun',
  'mullioned': 'MUL-yund',
  'multifarious': 'mul-tuh-FAIR-ee-us',
  'multiple': 'MUL-tuh-pul',
  'multiplication': 'mul-tuh-pluh-KAY-shun',
  'multitude': 'MUL-tuh-tood',
  'multivalent': 'mul-tuh-VAY-lunt',
  'mumbai': 'mum-BY',
  'mumble': 'MUM-bul',
  'mummified': 'MUM-uh-fyd',
  'munchkin': 'MUNCH-kin',
  'mundane': 'mun-DAYN',
  'munich': 'MYOO-nik',
  'municipal': 'myoo-NIS-uh-pul',
  'murals': 'MYOOR-ulz',
  'murky': 'MER-kee',
  'murmuration': 'mer-myuh-RAY-shun',
  'muscles': 'MUS-ulz',
  'muscular': 'MUS-kyuh-ler',
  'museum': 'myoo-ZEE-um',
  'mushy': 'MUSH-ee',
  'music': 'MYOO-zik',
  'musical': 'MYOO-zi-kul',
  'musicians': 'myoo-ZISH-unz',
  'musings': 'MYOO-zingz',
  'muskeg': 'MUS-keg',
  'musketeers': 'mus-kuh-TEERZ',
  'must': 'MUST',
  'mustache': 'MUS-tash',
  'mustelid': 'MUS-tuh-lid',
  'muster': 'MUS-ter',
  'mutiny': 'MYOO-tuh-nee',
  'mutter': 'MUT-er',
  'mutual': 'MYOO-chuh-wul',
  'muzak': 'MYOO-zak',
  'mycology': 'my-KOL-uh-jee',
  'myeloma': 'my-uh-LOH-muh',
  'mylar': 'MY-lar',
  'myocarditis': 'my-oh-kar-DY-tis',
  'myoglobin': 'my-uh-GLOH-bin',
  'myopic': 'my-OP-ik',
  'myself': 'my-SELF',
  'mystery': 'MIS-tuh-ree',
  'mystified': 'MIS-tuh-fyd',
  'mythical': 'MITH-uh-kul',
  'mythology': 'muh-THOL-uh-jee'
};

async function updateRemainingMWords() {
  try {
    console.log('Processing remaining M-words pronunciation batch...');
    
    // Get remaining M-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'm%')
      .limit(300);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} remaining M-words missing pronunciation`);
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
    
    console.log(`\nRemaining M-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`M-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 30) {
        console.log('Missing M-words:');
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
    console.error('Remaining M-words batch failed:', error);
  }
}

updateRemainingMWords();