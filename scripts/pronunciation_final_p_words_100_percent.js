const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Final P-words pronunciations for 100% completion
const pronunciations = {
  'parenthetic': 'pair-un-THET-ik',
  'parkour': 'par-KOOR',
  'parmentier': 'par-mahn-TYAY',
  'parodic': 'puh-ROD-ik',
  'paronomasia': 'pair-uh-noh-MAY-zee-uh',
  'parquetit': 'par-KET-it',
  'parr': 'PAR',
  'parroting': 'PAIR-uh-ting',
  'parsnips': 'PAR-snips',
  'parti': 'par-TEE',
  'parturient': 'par-TOOR-ee-unt',
  'parvo': 'PAR-voh',
  'paschal': 'PAS-kul',
  'pashmina': 'pash-MEE-nuh',
  'pasilla': 'pah-SEE-yah',
  'pasquinade': 'pas-kwih-NAYD',
  'passersby': 'pass-erz-BY',
  'pastitsio': 'pahs-TEET-see-oh',
  'patagonia': 'pat-uh-GOH-nee-uh',
  'pathways': 'PATH-wayz',
  'patripassianism': 'pay-tree-pas-ee-AN-izm',
  'patronise': 'PAY-truh-nyz',
  'pavilions': 'puh-VIL-yunz',
  'pavlova': 'pav-LOH-vuh',
  'peacenik': 'PEES-nik',
  'pearlescent': 'per-LES-unt',
  'pebbles': 'PEB-ulz',
  'peculiarities': 'pih-kyoo-lee-AIR-ih-teez',
  'pedestals': 'PED-ih-stulz',
  'peekaboo': 'PEEK-uh-boo',
  'pejerrey': 'peh-heh-RAY',
  'pejorate': 'PEE-juh-rayt',
  'pelagial': 'puh-LAY-jee-ul',
  'pelerine': 'pel-uh-REEN',
  'pelisse': 'puh-LEES',
  'pell': 'PEL',
  'pembroke': 'PEM-brohk',
  'pendeloque': 'pen-duh-LOHK',
  'pendentive': 'pen-DEN-tiv',
  'pomato': 'poh-MAY-toh',
  'pomeranian': 'pom-uh-RAY-nee-un',
  'pomology': 'poh-MOL-uh-jee',
  'ponzi': 'PON-zee',
  'popovers': 'POP-oh-verz',
  'penelope': 'puh-NEL-uh-pee',
  'penurious': 'puh-NYOOR-ee-us',
  'pepita': 'peh-PEE-tah',
  'peplos': 'PEP-los',
  'peplus': 'PEP-lus',
  'pepysian': 'PEP-see-un',
  'perciatelli': 'per-chah-TEL-ee',
  'perdue': 'per-DOO',
  'peregrination': 'per-uh-grih-NAY-shun',
  'periodontist': 'pair-ee-oh-DON-tist',
  'permafrost': 'PER-muh-frost',
  'perorate': 'PER-uh-rayt',
  'postdiction': 'pohst-DIK-shun',
  'posteriori': 'pos-teer-ee-OR-ee',
  'postural': 'POS-chur-ul',
  'pothos': 'POH-thos',
  'princeps': 'PRIN-seps',
  'privatim': 'pry-VAH-tim',
  'probative': 'PROH-buh-tiv',
  'proctors': 'PROK-terz',
  'proteron': 'PROH-ter-on',
  'protruding': 'proh-TROO-ding',
  'pruritus': 'proo-RY-tus',
  'porosity': 'puh-ROS-ih-tee',
  'portugais': 'por-too-GAY',
  'porwigle': 'POR-wig-ul',
  'pulvillus': 'pul-VIL-us',
  'punctually': 'PUNGK-choo-uh-lee',
  'potoroo': 'pot-uh-ROO',
  'pouched': 'POWCHT',
  'poudre': 'POO-druh',
  'powers': 'POW-erz',
  'pranks': 'PRANGKS',
  'prepares': 'prih-PAIRZ',
  'pressed': 'PRESD',
  'prevenient': 'prih-VEEN-yunt',
  'prima': 'PREE-muh',
  'primaeval': 'pry-MEE-vul',
  'primarily': 'PRY-mair-uh-lee',
  'prolusory': 'proh-LOO-suh-ree',
  'promethean': 'pruh-MEE-thee-un',
  'promyshlennik': 'proh-MISH-len-ik',
  'pronouncer': 'pruh-NOWN-ser',
  'pronunciations': 'pruh-nun-see-AY-shunz',
  'properties': 'PROP-er-teez',
  'prophecies': 'PROF-uh-seez',
  'prophetically': 'pruh-FET-ih-kul-ee',
  'propre': 'PROH-pruh',
  'proprioceptive': 'proh-pree-oh-SEP-tiv',
  'proscribed': 'proh-SKRYBD',
  'proselytiser': 'PROS-uh-ly-ty-zer',
  'proselytizer': 'PROS-uh-ly-ty-zer',
  'psalmody': 'SAL-muh-dee',
  'psamm': 'SAM',
  'psammophile': 'SAM-oh-fyl',
  'pschent': 'SHENT',
  'pseudonymous': 'soo-DON-ih-mus',
  'psychometry': 'sy-KOM-ih-tree',
  'ptosis': 'TOH-sis',
  'ptyxis': 'TIK-sis',
  'published': 'PUB-lisht',
  'publishes': 'PUB-lish-iz',
  'puchero': 'poo-CHAY-roh',
  'pudibund': 'PYOO-dih-bund',
  'puerilely': 'PYOOR-il-lee',
  'pulitzer': 'PUHL-it-ser',
  'pullets': 'PUHL-its',
  'pulverised': 'PUL-ver-yzd',
  'pulverized': 'PUL-ver-yzd',
  'punily': 'PYOO-nih-lee',
  'puniness': 'PYOO-nee-nis',
  'punting': 'PUN-ting',
  'puppets': 'PUP-its',
  'purposes': 'PER-puh-siz',
  'putsch': 'POOCH',
  'puzzles': 'PUZ-ulz',
  'pylorus': 'py-LOR-us',
  'pyramid': 'PEER-uh-mid',
  'pyrite': 'PY-ryt',
  'pyrotechnics': 'py-roh-TEK-niks',
  'pythagorean': 'pih-thag-uh-REE-un',
  'python': 'PY-thon',
  'pyxis': 'PIK-sis',
  'pâtissier': 'pah-tee-SYAY',
  'proximo': 'PROK-sih-moh',
  'puerto': 'PWAIR-toh',
  'posada': 'poh-SAH-dah',
  'preprandial': 'pree-PRAN-dee-ul',
  'presentient': 'prih-SEN-shunt',
  'preserving': 'prih-ZER-ving',
  'presidio': 'prih-SID-ee-oh',
  'prespinous': 'pree-SPY-nus',
  'preternaturally': 'pree-ter-NACH-er-uh-lee',
  'prion': 'PREE-on',
  'pris': 'PREE',
  'produced': 'pruh-DOOSD',
  'professes': 'pruh-FES-iz',
  'professing': 'pruh-FES-ing',
  'professionally': 'pruh-FESH-uh-nul-ee',
  'proffered': 'PROF-erd',
  'profiterole': 'pruh-FIT-uh-rohl',
  'projects': 'PROJ-ekts',
  'papeterie': 'pap-uh-tree',
  'pappardelle': 'pah-par-DEL-ay',
  'patissier': 'pah-tee-SYAY',
  'pompeii': 'pom-PAY',
  'pompey': 'POM-pee',
  'pomposity': 'pom-POS-ih-tee',
  'puttering': 'PUT-er-ing',
  'proviant': 'PROH-vee-unt'
};

async function finalPWordsFor100Percent() {
  try {
    console.log('🚀 FINAL P-WORDS PUSH FOR 100% COMPLETION');
    
    // Get all remaining P-words
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'p%')
      .limit(200);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Processing ${wordsToUpdate.length} remaining P-words for 100% completion`);
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
        await new Promise(resolve => setTimeout(resolve, 40));
      } else {
        notFound.push(word);
      }
    }
    
    console.log(`\\nP-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`P-words not found: ${notFound.length}`);
      if (notFound.length <= 20) {
        console.log('Missing P-words:', notFound.join(', '));
      }
    }
    
    // Check overall progress toward 100%
    const { count: totalCount } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });
      
    const { count: withPronunciation } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .not('pronunciation_guide', 'is', null);
      
    const progress = ((withPronunciation/totalCount)*100).toFixed(1);
    const remaining = totalCount - withPronunciation;
    
    console.log(`\\nProgress toward 100%: ${withPronunciation}/${totalCount} (${progress}%)`);
    console.log(`Remaining: ${remaining} words`);
    
    if (progress >= 100.0) {
      console.log('\\n🎉🎉🎉 100% PRONUNCIATION COVERAGE ACHIEVED! 🎉🎉🎉');
    } else {
      console.log(`Words needed to reach 100%: ${remaining}`);
    }
    
  } catch (error) {
    console.error('Final P-words processing failed:', error);
  }
}

finalPWordsFor100Percent();