const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Final T-words pronunciations for 100% completion
const pronunciations = {
  'tuschet': 'TUSH-it',
  'tutelage': 'TOO-tuh-lij',
  'tutti': 'TOO-tee',
  'twee': 'TWEE',
  'twirled': 'TWERLD',
  'twisting': 'TWIS-ting',
  'twisty': 'TWIS-tee',
  'twitchy': 'TWICH-ee',
  'tympanum': 'TIM-puh-num',
  'typhlology': 'tif-LOL-uh-jee',
  'typhoean': 'ty-FOH-ee-un',
  'typhoeanu': 'ty-FOH-ee-ah-noo',
  'typically': 'TIP-ih-kul-ee',
  'typing': 'TY-ping',
  'tyrannical': 'tih-RAN-ih-kul',
  'toccata': 'toh-KAH-tuh',
  'transfixed': 'trans-FIKST',
  'transgressions': 'trans-GRESH-unz',
  'transhumance': 'trans-HYOO-muns',
  'transience': 'TRAN-shuns',
  'triceratopssandal': 'try-SAIR-uh-tops-SAN-dul',
  'trovato': 'troh-VAH-toh',
  'toey': 'TOH-ee',
  'toga': 'TOH-guh',
  'toggenburg': 'TOG-un-berg',
  'togo': 'TOH-goh',
  'toile': 'TOYL',
  'toilsome': 'TOYL-sum',
  'toilsometempestuous': 'TOYL-sum-tem-PES-choo-us',
  'toity': 'TOY-tee',
  'tokendifficulty': 'TOH-kun-DIF-ih-kul-tee',
  'tokonoma': 'toh-koh-NOH-mah',
  'tokonomaunguiculate': 'toh-koh-NOH-mah-ung-GWIK-yuh-lit',
  'tolerable': 'TOL-er-uh-bul',
  'tomalley': 'toh-MAL-ee',
  'tomfoolery': 'tom-FOO-ler-ee',
  'tommyrot': 'TOM-ee-rot',
  'tomography': 'toh-MOG-ruh-fee',
  'tongued': 'TUNGD',
  'tools': 'TOOLZ',
  'toorie': 'TOR-ee',
  'topazolite': 'toh-PAZ-oh-lyt',
  'topgallant': 'top-GAL-unt',
  'topiary': 'TOH-pee-air-ee',
  'topics': 'TOP-iks',
  'toploftical': 'top-LOF-tih-kul',
  'topologically': 'top-uh-LOJ-ih-kul-ee',
  'toponymic': 'top-uh-NIM-ik',
  'topped': 'TOPT',
  'toppings': 'TOP-ingz',
  'toppled': 'TOP-uld',
  'toque': 'TOHK',
  'toreador': 'TOR-ee-uh-dor',
  'toreutics': 'tor-YOO-tiks',
  'torii': 'TOR-ee-ee',
  'toril': 'TOR-il',
  'toroidalbialy': 'tor-OY-dul-bee-AH-lee',
  'torsionjusticiable': 'TOR-shun-jus-TISH-uh-bul',
  'tosh': 'TOSH',
  'tosteson': 'TOHS-tih-sun',
  'tostones': 'tohs-TOH-nays',
  'toties': 'TOH-teez',
  'totipotency': 'toh-TIP-oh-tun-see',
  'toughness': 'TUF-nis',
  'tourelle': 'too-REL',
  'tourists': 'TOOR-ists',
  'tournedos': 'toor-nuh-DOH',
  'touted': 'TOW-tid',
  'towhee': 'TOW-hee',
  'toxicosis': 'tok-sih-KOH-sis',
  'toys': 'TOYZ',
  'tracheotomy': 'tray-kee-OT-uh-mee',
  'tracks': 'TRAKS',
  'tractability': 'trak-tuh-BIL-ih-tee',
  'traditionally': 'truh-DISH-uh-nul-ee',
  'tragedian': 'truh-JEE-dee-un',
  'traiteur': 'tray-TER',
  'traitorous': 'TRAY-ter-us',
  'tralatitious': 'tral-uh-TISH-us',
  'trampolines': 'TRAM-puh-leenz',
  'transcription': 'tran-SKRIP-shun',
  'transducer': 'trans-DOO-ser',
  'transept': 'TRAN-sept',
  'transference': 'TRANS-fer-uns',
  'translates': 'trans-LAYTS',
  'transmissibility': 'trans-mis-ih-BIL-ih-tee',
  'transmontane': 'trans-MON-tayn',
  'transparencies': 'trans-PAIR-un-seez',
  'transpiration': 'tran-spih-RAY-shun',
  'transportation': 'tran-spor-TAY-shun',
  'transposable': 'trans-POH-zuh-bul',
  'trapezoid': 'TRAP-ih-zoyd',
  'trashbobbed': 'TRASH-bobd',
  'travails': 'truh-VAYLZ',
  'traveled': 'TRAV-uld',
  'travels': 'TRAV-ulz',
  'treadle': 'TRED-ul',
  'treatise': 'TREE-tis',
  'treatments': 'TREET-munts',
  'treble': 'TREB-ul',
  'trebuchet': 'TREB-yuh-shet',
  'trees': 'TREEZ',
  'trefoil': 'TREE-foyl',
  'trembling': 'TREM-bling',
  'tremulous': 'TREM-yuh-lus',
  'tremuloustrepanation': 'TREM-yuh-lus-trep-uh-NAY-shun',
  'trencher': 'TREN-cher',
  'trepanation': 'trep-uh-NAY-shun',
  'trey': 'TRAY',
  'triage': 'tree-AHZH',
  'triagetrinkets': 'tree-AHZH-TRING-kits',
  'trichinosis': 'trik-ih-NOH-sis',
  'trichotillomania': 'trik-oh-til-oh-MAY-nee-uh',
  'trickster': 'TRIK-ster',
  'triduum': 'TRID-oo-um',
  'trifecta': 'try-FEK-tuh',
  'triforium': 'try-FOR-ee-um',
  'trigeminal': 'try-JEM-ih-nul',
  'trigeminalbruja': 'try-JEM-ih-nul-BROO-hah',
  'triglycerides': 'try-GLIS-er-ydz',
  'trilby': 'TRIL-bee',
  'trillado': 'tree-YAH-doh',
  'trillium': 'TRIL-ee-um',
  'trinidadian': 'trin-ih-DAD-ee-un',
  'trinkets': 'TRING-kits',
  'tripartite': 'try-PAR-tyt',
  'tripe': 'TRYP',
  'triquetra': 'try-KWET-ruh',
  'triskelion': 'try-SKEL-ee-un',
  'triste': 'TRIST',
  'tristetrituration': 'TRIST-trit-yuh-RAY-shun',
  'tristeza': 'tree-STAY-zah',
  'triton': 'TRY-tun',
  'trituration': 'trit-yuh-RAY-shun',
  'trochee': 'TROH-kee',
  'trocheetrompe': 'TROH-kee-TROMP',
  'trompe': 'TROMP',
  'trope': 'TROHP',
  'trophic': 'TROH-fik',
  'trotteur': 'trot-UR',
  'trous': 'TROO',
  'trovatobeowulf': 'troh-VAH-toh-BAY-oh-wulf',
  'trowel': 'TROW-ul',
  'trowsers': 'TROW-zerz',
  'truckee': 'TRUK-ee',
  'truculence': 'TRUK-yuh-luns',
  'truereal': 'TROO-ree-ul',
  'truncheon': 'TRUN-chun',
  'tryptophan': 'TRIP-toh-fan',
  'tryptophanneophyte': 'TRIP-toh-fan-NEE-oh-fyt',
  'tsked': 'TISKED',
  'tsukupin': 'tsoo-KOO-pin',
  'tsunami': 'tsoo-NAH-mee',
  'tuatara': 'too-ah-TAH-rah',
  'tubers': 'TOO-berz',
  'tubes': 'TOOBZ',
  'tufts': 'TUFTS',
  'tulipmyself': 'TOO-lip-my-SELF',
  'tullibee': 'TUL-ih-bee',
  'tulsi': 'TUHL-see',
  'tumbling': 'TUM-bling',
  'tumpline': 'TUMP-lyn',
  'tumultuouscommodore': 'too-MUL-choo-us-KOM-uh-dor',
  'tumulus': 'TOO-myuh-lus',
  'tungsten': 'TUNG-stun',
  'tupelo': 'TOO-pih-loh',
  'turbinado': 'ter-bih-NAH-doh',
  'turbinadobrethren': 'ter-bih-NAH-doh-BRETH-ren',
  'turducken': 'TER-duk-un'
};

async function finalTWordsFor100Percent() {
  try {
    console.log('🎯 FINAL T-WORDS PUSH FOR 100% COMPLETION');
    
    // Get all remaining T-words
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 't%')
      .limit(200);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Processing ${wordsToUpdate.length} remaining T-words for 100% completion`);
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
    
    console.log(`\nT-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`T-words not found: ${notFound.length}`);
      console.log('Missing T-words:', notFound.join(', '));
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
    
    console.log(`\nProgress toward 100%: ${withPronunciation}/${totalCount} (${progress}%)`);
    console.log(`Remaining: ${remaining} words`);
    
    if (progress >= 100.0) {
      console.log('\n🎉🎉🎉 100% PRONUNCIATION COVERAGE ACHIEVED! 🎉🎉🎉');
    }
    
  } catch (error) {
    console.error('Final T-words processing failed:', error);
  }
}

finalTWordsFor100Percent();