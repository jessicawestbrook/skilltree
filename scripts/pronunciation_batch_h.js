const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// H-words pronunciations (first batch)
const pronunciations = {
  'habanero': 'hab-uh-NAIR-oh',
  'habeas': 'HAY-bee-us',
  'haberdasher': 'HAB-er-dash-er',
  'habiliments': 'huh-BIL-uh-munts',
  'habitual': 'huh-BICH-oo-ul',
  'habitue': 'huh-BICH-oo-ay',
  'habitué': 'huh-BICH-oo-ay',
  'hackamore': 'HAK-uh-mor',
  'hackles': 'HAK-ulz',
  'hackneyed': 'HAK-need',
  'hadith': 'hah-DEETH',
  'haggisdolce': 'HAG-is DOHL-chay',
  'haggle': 'HAG-ul',
  'hagiographer': 'hag-ee-OG-ruh-fer',
  'hair': 'HAIR',
  'haitian': 'HAY-shun',
  'halala': 'hah-LAH-lah',
  'halalah': 'hah-LAH-lah',
  'halcyon': 'HAL-see-un',
  'halibut': 'HAL-uh-but',
  'halifax': 'HAL-uh-faks',
  'halifaxhallucinate': 'HAL-uh-faks huh-LOO-suh-nayt',
  'hall': 'HAWL',
  'hallowed': 'HAL-ohd',
  'hallucinate': 'huh-LOO-suh-nayt',
  'hallux': 'HAL-uks',
  'halo': 'HAY-loh',
  'halogens': 'HAL-uh-junz',
  'hamadryad': 'ham-uh-DRY-ad',
  'hamlet': 'HAM-lit',
  'hamstring': 'HAM-string',
  'hamtramck': 'HAM-tram-ik',
  'hand': 'HAND',
  'handcuffs': 'HAND-kufs',
  'handle': 'HAN-dul',
  'handles': 'HAN-dulz',
  'handstand': 'HAND-stand',
  'handwriting': 'HAND-ry-ting',
  'handyman': 'HAN-dee-man',
  'hangar': 'HANG-er',
  'hangnail': 'HANG-nayl',
  'hangul': 'HAHN-gool',
  'hankering': 'HANG-ker-ing',
  'haori': 'hah-OH-ree',
  'haphazard': 'hap-HAZ-erd',
  'haplography': 'hap-LOG-ruh-fee',
  'happenstance': 'HAP-un-stants',
  'happy': 'HAP-ee',
  'harangue': 'huh-RANG',
  'harangueniveau': 'huh-RANG nee-VOH',
  'harbinger': 'HAR-bin-jer',
  'harbor': 'HAR-ber',
  'harbour': 'HAR-ber',
  'hard': 'HARD',
  'harder': 'HAR-der',
  'hardtack': 'HARD-tak',
  'hardtackrabid': 'HARD-tak RAB-id',
  'haricot': 'HAR-i-koh',
  'hariolation': 'hair-ee-uh-LAY-shun',
  'harlem': 'HAR-lum',
  'harmattan': 'har-muh-TAN',
  'harmful': 'HARM-ful',
  'harmonious': 'har-MOH-nee-us',
  'harpoons': 'har-POONZ',
  'harrier': 'HAR-ee-er',
  'harrierdifficulty': 'HAR-ee-er DIF-i-kul-tee',
  'harrowing': 'HAR-oh-ing',
  'harrumph': 'hah-RUMF',
  'harvest': 'HAR-vist',
  'hasten': 'HAY-sun',
  'hatchet': 'HACH-it',
  'hatchling': 'HACH-ling',
  'hathor': 'HATH-or',
  'hauberk': 'HAW-berk',
  'haughty': 'HAW-tee',
  'hauling': 'HAWL-ing',
  'haupia': 'how-PEE-ah',
  'haupiakeplerian': 'how-PEE-ah kep-LEER-ee-un',
  'haute': 'OHNT',
  'hauteur': 'oh-TER',
  'haven': 'HAY-vun',
  'havens': 'HAY-vunz',
  'having': 'HAV-ing',
  'havoc': 'HAV-uk',
  'hawaiian': 'huh-WY-un',
  'hawk': 'HAWK',
  'hawok': 'HAW-ok',
  'hawsers': 'HAW-zerz',
  'hazardous': 'HAZ-er-dus',
  'hazelnut': 'HAY-zul-nut',
  'hazmat': 'HAZ-mat',
  'head': 'HED',
  'headdress': 'HED-dres',
  'headlong': 'HED-lawng',
  'headquartered': 'HED-kwar-terd',
  'health': 'HELTH',
  'hear': 'HEER',
  'heard': 'HERD',
  'heartthrob': 'HART-throb',
  'heavenly': 'HEV-un-lee',
  'heavenlyheiress': 'HEV-un-lee AIR-is',
  'heavy': 'HEV-ee',
  'hebdomadal': 'heb-DOM-uh-dul',
  'hebrides': 'HEB-ri-deez',
  'hedgehog': 'HEJ-hawg',
  'hegemony': 'huh-JEM-uh-nee',
  'hegirae': 'HEJ-i-ree',
  'hegiraeanomaliped': 'HEJ-i-ree uh-nom-uh-LY-ped',
  'hegiraemoissanite': 'HEJ-i-ree moy-suh-NYT',
  'heinousness': 'HAY-nus-nis',
  'heiress': 'AIR-is',
  'heirloom': 'AIR-loom',
  'heist': 'HYST',
  'held': 'HELD',
  'heleoplankton': 'hee-lee-oh-PLANGK-tun',
  'heleoplanktonpliant': 'hee-lee-oh-PLANGK-tun PLY-unt',
  'heliacal': 'hee-LY-uh-kul',
  'heliotrope': 'HEE-lee-uh-trohp',
  'helium': 'HEE-lee-um',
  'hellebore': 'HEL-uh-bor',
  'helmet': 'HEL-mit',
  'help': 'HELP',
  'helped': 'HELPT',
  'helpful': 'HELP-ful',
  'helvetia': 'hel-VEE-shuh',
  'hematology': 'hee-muh-TOL-uh-jee',
  'hemorrhage': 'HEM-uh-rij',
  'hennery': 'HEN-uh-ree',
  'hennin': 'hen-EEN',
  'henotheism': 'HEN-uh-thee-izm',
  'henry': 'HEN-ree',
  'hepatectomy': 'hep-uh-TEK-tuh-mee',
  'heptad': 'HEP-tad',
  'heraldic': 'huh-RAL-dik',
  'herb': 'ERB',
  'herbaceous': 'her-BAY-shus',
  'herbalist': 'ER-buh-list'
};

async function updateHWords() {
  try {
    console.log('Processing H-words pronunciation batch...');
    
    // Get H-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'h%')
      .limit(150);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} H-words missing pronunciation`);
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
    
    console.log(`\nH-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`H-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 20) {
        console.log('Missing H-words:');
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
    console.error('H-words batch failed:', error);
  }
}

updateHWords();