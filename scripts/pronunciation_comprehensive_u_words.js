const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// U-words pronunciations
const pronunciations = {
  'ubiquitous': 'yoo-BIK-wih-tus',
  'udder': 'UD-er',
  'ugly': 'UG-lee',
  'ugliness': 'UG-lee-nis',
  'ukulele': 'oo-kuh-LAY-lee',
  'ulcer': 'UL-ser',
  'ulna': 'UL-nuh',
  'ulterior': 'ul-TEER-ee-er',
  'ultimate': 'UL-tuh-mit',
  'ultimately': 'UL-tuh-mit-lee',
  'ultimatum': 'ul-tih-MAY-tum',
  'ultra': 'UL-truh',
  'ultraviolet': 'ul-truh-VY-uh-lit',
  'umbilical': 'um-BIL-ih-kul',
  'umbrage': 'UM-brij',
  'umbrella': 'um-BREL-uh',
  'umpire': 'UM-pyr',
  'unable': 'un-AY-bul',
  'unabashed': 'un-uh-BASHТ',
  'unaccountable': 'un-uh-KOWNT-uh-bul',
  'unaffected': 'un-uh-FEK-tid',
  'unanimous': 'yoo-NAN-ih-mus',
  'unapproachable': 'un-uh-PROH-chuh-bul',
  'unassuming': 'un-uh-SOO-ming',
  'unavoidable': 'un-uh-VOY-duh-bul',
  'unaware': 'un-uh-WAIR',
  'unbearable': 'un-BAIR-uh-bul',
  'unbecoming': 'un-bih-KUM-ing',
  'unbiased': 'un-BY-ust',
  'unbridled': 'un-BRY-duld',
  'uncanny': 'un-KAN-ee',
  'uncertain': 'un-SER-tun',
  'uncle': 'UNG-kul',
  'uncomfortable': 'un-KUM-fer-tuh-bul',
  'unconscious': 'un-KON-shus',
  'uncover': 'un-KUV-er',
  'unctuous': 'UNGK-choo-us',
  'under': 'UN-der',
  'undercover': 'un-der-KUV-er',
  'underdog': 'UN-der-dawg',
  'undergo': 'un-der-GOH',
  'undergraduate': 'un-der-GRAD-yoo-it',
  'underground': 'UN-der-grownd',
  'underline': 'un-der-LYN',
  'undermine': 'un-der-MYN',
  'underneath': 'un-der-NEETH',
  'understand': 'un-der-STAND',
  'undertake': 'un-der-TAYK',
  'undertaker': 'UN-der-tay-ker',
  'undertaking': 'un-der-TAY-king',
  'undertone': 'UN-der-tohn',
  'underway': 'UN-der-way',
  'underworld': 'UN-der-werld',
  'undesirable': 'un-dih-ZYR-uh-bul',
  'undo': 'un-DOO',
  'undoubtedly': 'un-DOW-tid-lee',
  'undress': 'un-DRES',
  'undue': 'un-DOO',
  'undulate': 'UN-juh-layt',
  'uneasy': 'un-EE-zee',
  'unemployed': 'un-im-PLOYD',
  'unequal': 'un-EE-kwul',
  'uneven': 'un-EE-vun',
  'unexpected': 'un-ik-SPEK-tid',
  'unfair': 'un-FAIR',
  'unfamiliar': 'un-fuh-MIL-yer',
  'unfavorable': 'un-FAY-ver-uh-bul',
  'unfit': 'un-FIT',
  'unfold': 'un-FOHLD',
  'unfortunate': 'un-FOR-chuh-nit',
  'unfurl': 'un-FERL',
  'unhappy': 'un-HAP-ee',
  'unhealthy': 'un-HEL-thee',
  'unicorn': 'YOO-nih-korn',
  'uniform': 'YOO-nih-form',
  'unify': 'YOO-nih-fy',
  'unilateral': 'yoo-nih-LAT-er-ul',
  'unimpeachable': 'un-im-PEE-chuh-bul',
  'unimportant': 'un-im-POR-tunt',
  'uninhabited': 'un-in-HAB-ih-tid',
  'union': 'YOON-yun',
  'unique': 'yoo-NEEK',
  'unison': 'YOO-nih-sun',
  'unit': 'YOO-nit',
  'unite': 'yoo-NYT',
  'unity': 'YOO-nih-tee',
  'universal': 'yoo-nih-VER-sul',
  'universe': 'YOO-nih-vers',
  'university': 'yoo-nih-VER-sih-tee',
  'unkempt': 'un-KEMPT',
  'unkind': 'un-KYND',
  'unknown': 'un-NOHN',
  'unlawful': 'un-LAW-ful',
  'unless': 'un-LES',
  'unlike': 'un-LYK',
  'unlikely': 'un-LYK-lee',
  'unlimited': 'un-LIM-ih-tid',
  'unload': 'un-LOHD',
  'unlock': 'un-LOK',
  'unlucky': 'un-LUK-ee',
  'unmistakable': 'un-mih-STAY-kuh-bul',
  'unnatural': 'un-NACH-er-ul',
  'unnecessary': 'un-NES-uh-sair-ee',
  'unnoticed': 'un-NOH-tist',
  'unpack': 'un-PAK',
  'unparalleled': 'un-PAIR-uh-leld',
  'unpleasant': 'un-PLEZ-unt',
  'unprecedented': 'un-PRES-ih-den-tid',
  'unprepared': 'un-prih-PAIRD',
  'unreasonable': 'un-REE-zuh-nuh-bul',
  'unrest': 'un-REST',
  'unruly': 'un-ROO-lee',
  'unsafe': 'un-SAYF',
  'unsatisfactory': 'un-sat-is-FAK-ter-ee',
  'unscrupulous': 'un-SKROO-pyuh-lus',
  'unseen': 'un-SEEN',
  'unselfish': 'un-SEL-fish',
  'unstable': 'un-STAY-bul',
  'unsuccessful': 'un-suk-SES-ful',
  'unsuitable': 'un-SOO-tuh-bul',
  'unsullied': 'un-SUL-eed',
  'until': 'un-TIL',
  'untrue': 'un-TROO',
  'unusual': 'un-YOO-zhoo-ul',
  'unveil': 'un-VAYL',
  'unwelcome': 'un-WEL-kum',
  'unwieldy': 'un-WEEL-dee',
  'unwilling': 'un-WIL-ing',
  'unworthy': 'un-WER-thee',
  'up': 'UP',
  'upbraid': 'up-BRAYD',
  'upbringing': 'UP-bring-ing',
  'update': 'up-DAYT',
  'upgrade': 'UP-grayd',
  'upheaval': 'up-HEE-vul',
  'uphill': 'UP-hil',
  'uphold': 'up-HOHLD',
  'upholster': 'up-HOHL-ster',
  'upkeep': 'UP-keep',
  'upland': 'UP-lund',
  'upload': 'UP-lohd',
  'upon': 'uh-PON',
  'upper': 'UP-er',
  'upright': 'UP-ryt',
  'uprising': 'UP-ry-zing',
  'uproar': 'UP-ror',
  'uproot': 'up-ROOT',
  'upset': 'up-SET',
  'upshot': 'UP-shot',
  'upside': 'UP-syd',
  'upstairs': 'up-STAIRZ',
  'upstart': 'UP-start',
  'upstream': 'UP-streem',
  'uptight': 'up-TYT',
  'uptown': 'UP-town',
  'upturn': 'UP-tern',
  'upward': 'UP-werd',
  'uranium': 'yoo-RAY-nee-um',
  'urban': 'ER-bun',
  'urbane': 'er-BAYN',
  'urchin': 'ER-chin',
  'urge': 'ERJ',
  'urgent': 'ER-junt',
  'urine': 'YOOR-in',
  'urn': 'ERN',
  'usable': 'YOO-zuh-bul',
  'usage': 'YOO-sij',
  'use': 'YOOZ',
  'used': 'YOOZD',
  'useful': 'YOOS-ful',
  'useless': 'YOOS-lis',
  'user': 'YOO-zer',
  'usher': 'USH-er',
  'using': 'YOO-zing',
  'usual': 'YOO-zhoo-ul',
  'usually': 'YOO-zhoo-uh-lee',
  'usurp': 'yoo-SERP',
  'usury': 'YOO-zuh-ree',
  'utensil': 'yoo-TEN-sil',
  'uterus': 'YOO-ter-us',
  'utilitarian': 'yoo-til-uh-TAIR-ee-un',
  'utility': 'yoo-TIL-ih-tee',
  'utilize': 'YOO-tuh-lyz',
  'utmost': 'UT-mohst',
  'utopia': 'yoo-TOH-pee-uh',
  'utter': 'UT-er',
  'utterance': 'UT-er-uns',
  'utterly': 'UT-er-lee',
  'uvula': 'YOO-vyuh-luh',
  'ukrainian': 'yoo-KRAY-nee-un',
  'ullage': 'UL-ij'
};

async function updateUWords() {
  try {
    console.log('Processing U-words pronunciation batch...');
    
    // Get U-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'u%')
      .limit(150);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} U-words missing pronunciation`);
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
    
    console.log(`\nU-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`U-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 50) {
        console.log('Missing U-words:');
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
    
    // Final summary
    console.log('\n=== COMPREHENSIVE PRONUNCIATION PROJECT COMPLETE ===');
    console.log(`Total words processed: ${withPronunciation}/${totalCount}`);
    console.log(`Final completion rate: ${progress}%`);
    
  } catch (error) {
    console.error('U-words batch failed:', error);
  }
}

updateUWords();