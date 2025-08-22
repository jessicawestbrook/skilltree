const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Pronunciations for the remaining words (v-n range)
const pronunciations = {
  'voltammetry': 'vol-TAM-uh-tree',
  'volucrine': 'VOL-yoo-kryn',
  'volumetric': 'vol-yoo-MET-rik',
  'voluminous': 'vuh-LOO-muh-nus',
  'voluntary': 'VOL-un-ter-ee',
  'vortices': 'VOR-tuh-seez',
  'votive': 'VOH-tiv',
  'vouch': 'VOWCH',
  'vowel': 'VOW-ul',
  'voyage': 'VOY-ij',
  'vulcan': 'VUL-kun',
  'vulpine': 'VUL-pyn',
  'vultures': 'VUL-cherz',
  'vuvuzela': 'voo-voo-ZEH-luh',
  'véronique': 'vay-roh-NEEK',
  'wabeno': 'wah-BEE-noh',
  'wafer': 'WAY-fer',
  'wafting': 'WAFT-ing',
  'wagon': 'WAG-un',
  'wahine': 'wah-HEE-nay',
  'waistcoat': 'WAYST-koht',
  'waive': 'WAYV',
  'wake': 'WAYK',
  'walking': 'WAWK-ing',
  'walnut': 'WAWL-nut',
  'walrus': 'WAWL-rus',
  'wampum': 'WOM-pum',
  'wander': 'WON-der',
  'wanton': 'WON-tun',
  'warble': 'WOR-bul',
  'warehouse': 'WAIR-hows',
  'warfare': 'WOR-fair',
  'warm': 'WORM',
  'warmth': 'WORMTH',
  'warning': 'WOR-ning',
  'warp': 'WORP',
  'warranty': 'WOR-un-tee',
  'warrior': 'WOR-ee-or',
  'wary': 'WAIR-ee',
  'wash': 'WOSH',
  'wasp': 'WOSP',
  'waste': 'WAYST',
  'watch': 'WOCH',
  'water': 'WAW-ter',
  'watermelon': 'WAW-ter-mel-un',
  'wattle': 'WOT-ul',
  'wave': 'WAYV',
  'waver': 'WAY-ver',
  'wax': 'WAKS',
  'way': 'WAY',
  'wayward': 'WAY-werd',
  'weak': 'WEEK',
  'wealth': 'WELTH',
  'weapon': 'WEP-un',
  'wear': 'WAIR',
  'weary': 'WEER-ee',
  'weather': 'WETH-er',
  'weave': 'WEEV',
  'web': 'WEB',
  'wedding': 'WED-ing',
  'wedge': 'WEJ',
  'weed': 'WEED',
  'week': 'WEEK',
  'weep': 'WEEP',
  'weevil': 'WEE-vul',
  'weigh': 'WAY',
  'weight': 'WAYT',
  'weird': 'WEERD',
  'welcome': 'WEL-kum',
  'weld': 'WELD',
  'welfare': 'WEL-fair',
  'well': 'WEL',
  'welsh': 'WELSH',
  'wench': 'WENCH',
  'west': 'WEST',
  'western': 'WES-tern',
  'wet': 'WET',
  'whale': 'HWAYL',
  'wharf': 'HWORF',
  'wheat': 'HWEET',
  'wheel': 'HWEEL',
  'when': 'HWEN',
  'where': 'HWAIR',
  'whet': 'HWET',
  'whether': 'HWETH-er',
  'which': 'HWICH',
  'whiff': 'HWIF',
  'while': 'HWYL',
  'whim': 'HWIM',
  'whine': 'HWYN',
  'whip': 'HWIP',
  'whirl': 'HWERL',
  'whisk': 'HWISK',
  'whisper': 'HWIS-per',
  'whistle': 'HWIS-ul',
  'white': 'HWYT',
  'who': 'HOO',
  'whole': 'HOHL',
  'whom': 'HOOM',
  'whoop': 'HOOP',
  'whose': 'HOOZ',
  'why': 'HWY',
  'wick': 'WIK',
  'wicked': 'WIK-id',
  'wide': 'WYD',
  'widow': 'WID-oh',
  'width': 'WIDTH',
  'wield': 'WEELD',
  'wife': 'WYF',
  'wig': 'WIG',
  'wild': 'WYLD',
  'will': 'WIL',
  'willow': 'WIL-oh',
  'wilt': 'WILT',
  'wily': 'WY-lee',
  'win': 'WIN',
  'wind': 'WIND',
  'window': 'WIN-doh',
  'wine': 'WYN',
  'wing': 'WING',
  'wink': 'WINK',
  'winter': 'WIN-ter',
  'wipe': 'WYP',
  'wire': 'WYR',
  'wisdom': 'WIZ-dum',
  'wise': 'WYZ',
  'wish': 'WISH',
  'wisp': 'WISP',
  'witch': 'WICH',
  'with': 'WITH',
  'wither': 'WITH-er',
  'within': 'with-IN',
  'without': 'with-OWT',
  'witness': 'WIT-nis',
  'wizard': 'WIZ-erd',
  'woe': 'WOH',
  'wok': 'WOK',
  'woke': 'WOHK',
  'wolf': 'WOOLF',
  'woman': 'WOOM-un',
  'womb': 'WOOM',
  'women': 'WIM-in',
  'won': 'WUN',
  'wonder': 'WUN-der',
  'wont': 'WOHNT',
  'wood': 'WOOD',
  'woodland': 'WOOD-lund',
  'wool': 'WOOL',
  'word': 'WERD',
  'work': 'WERK',
  'world': 'WERLD',
  'worm': 'WERM',
  'worn': 'WORN',
  'worry': 'WER-ee',
  'worse': 'WERS',
  'worship': 'WER-ship',
  'worst': 'WERST',
  'worth': 'WERTH',
  'worthy': 'WER-thee',
  'would': 'WOOD',
  'wound': 'WOOND',
  'woven': 'WOH-vun',
  'wow': 'WOW',
  'wrack': 'RAK',
  'wrap': 'RAP',
  'wrath': 'RATH',
  'wreath': 'REETH',
  'wreck': 'REK',
  'wren': 'REN',
  'wrench': 'RENCH',
  'wrest': 'REST',
  'wrestle': 'RES-ul',
  'wretch': 'RECH',
  'wriggle': 'RIG-ul',
  'wring': 'RING',
  'wrinkle': 'RING-kul',
  'wrist': 'RIST',
  'write': 'RYT',
  'writhe': 'RYTH',
  'written': 'RIT-un',
  'wrong': 'RONG',
  'wrote': 'ROHT',
  'wrought': 'RAWT',
  'wry': 'RY',
  'xenophobia': 'zee-nuh-FOH-bee-uh',
  'xerophyte': 'ZEER-uh-fyt',
  'xiphoid': 'ZY-foyd',
  'xylophone': 'ZY-luh-fohn',
  'yacht': 'YAHT',
  'yak': 'YAK',
  'yam': 'YAM',
  'yard': 'YARD',
  'yarn': 'YARN',
  'yawn': 'YAWN',
  'yeah': 'YEH',
  'year': 'YEER',
  'yeast': 'YEEST',
  'yell': 'YEL',
  'yellow': 'YEL-oh',
  'yelp': 'YELP',
  'yes': 'YES',
  'yesterday': 'YES-ter-day',
  'yet': 'YET',
  'yield': 'YEELD',
  'yodel': 'YOH-dul',
  'yoga': 'YOH-guh',
  'yoke': 'YOHK',
  'yolk': 'YOHLK',
  'you': 'YOO',
  'young': 'YUNG',
  'your': 'YOR',
  'youth': 'YOOTH',
  'yowl': 'YOWL',
  'yucca': 'YUK-uh',
  'yummy': 'YUM-ee',
  'zany': 'ZAY-nee',
  'zap': 'ZAP',
  'zeal': 'ZEEL',
  'zebra': 'ZEE-bruh',
  'zenith': 'ZEE-nith',
  'zephyr': 'ZEF-er',
  'zero': 'ZEER-oh',
  'zest': 'ZEST',
  'zigzag': 'ZIG-zag',
  'zinc': 'ZINGK',
  'zip': 'ZIP',
  'zodiac': 'ZOH-dee-ak',
  'zombie': 'ZOM-bee',
  'zone': 'ZOHN',
  'zoo': 'ZOO',
  'zoom': 'ZOOM',
  'zucchini': 'zoo-KEE-nee'
};

async function updateRemaining() {
  try {
    console.log('Completing pronunciation updates...');
    
    // Get words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} words missing pronunciation`);
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
    
    console.log(`\nCompleted: ${updated} pronunciations added`);
    console.log(`Not found in our list: ${notFound.length}`);
    
    if (notFound.length > 0 && notFound.length <= 20) {
      console.log('Words not found:');
      notFound.forEach(word => console.log(`- ${word}`));
    }
    
    // Final status check
    const { data: finalStats } = await supabase
      .from('spelling_words')
      .select('pronunciation_guide');
      
    const finalTotal = finalStats.length;
    const finalWithPronunciation = finalStats.filter(w => w.pronunciation_guide).length;
    const finalProgress = ((finalWithPronunciation/finalTotal)*100).toFixed(1);
    
    console.log(`\nFinal status: ${finalWithPronunciation}/${finalTotal} (${finalProgress}%)`);
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

updateRemaining();