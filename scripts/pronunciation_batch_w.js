const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// W-words pronunciations (first 100 words)
const pronunciations = {
  'waing': 'WAYNG',
  'waist': 'WAYST',
  'waited': 'WAY-tid',
  'waiter': 'WAY-ter',
  'waiver': 'WAY-ver',
  'wakame': 'wah-KAH-may',
  'wales': 'WAYLZ',
  'walk': 'WAWK',
  'wallaby': 'WOL-uh-bee',
  'walter': 'WAWL-ter',
  'wamble': 'WOM-bul',
  'wampanoag': 'wom-puh-NOH-ag',
  'wand': 'WOND',
  'want': 'WONT',
  'wapiti': 'WOP-i-tee',
  'warden': 'WOR-dun',
  'wardrobe': 'WOR-drohb',
  'warison': 'WAIR-i-sun',
  'washing': 'WOSH-ing',
  'washington': 'WOSH-ing-tun',
  'wasn': 'WUZ-unt',
  'wassail': 'WOS-ayl',
  'watched': 'WOCHT',
  'waters': 'WAW-terz',
  'wattage': 'WOT-ij',
  'wattles': 'WOT-ulz',
  'ways': 'WAYZ',
  'weakness': 'WEEK-nis',
  'weald': 'WEELD',
  'wealthy': 'WEL-thee',
  'weaponry': 'WEP-un-ree',
  'wearing': 'WAIR-ing',
  'wearisome': 'WEER-i-sum',
  'wears': 'WAIRZ',
  'weasels': 'WEE-zulz',
  'webisode': 'WEB-i-sohd',
  'webster': 'WEB-ster',
  'websterian': 'web-STEER-ee-un',
  'wednesday': 'WENZ-day',
  'weka': 'WEH-kah',
  'welding': 'WEL-ding',
  'welterweight': 'WEL-ter-wayt',
  'weltschmerz': 'VELT-shmerts',
  'wensleydale': 'WENZ-lee-dayl',
  'went': 'WENT',
  'wentletrap': 'WENT-luh-trap',
  'werf': 'WERF',
  'whakapapa': 'fah-kah-PAH-pah',
  'whales': 'HWAYLZ',
  'whee': 'HWEE',
  'wheedle': 'HWEE-dul',
  'wheedling': 'HWEE-dling',
  'wheezy': 'HWEE-zee',
  'whelp': 'HWELP',
  'whenever': 'hwen-EV-er',
  'whereas': 'hwair-AZ',
  'wherewithal': 'HWAIR-with-awl',
  'whey': 'HWAY',
  'whidah': 'HWEE-dah',
  'whimsical': 'HWIM-zi-kul',
  'whipped': 'HWIPT',
  'whippoorwill': 'HWIP-er-wil',
  'whirlybird': 'HWERL-ee-berd',
  'whiskers': 'HWIS-kerz',
  'whitefish': 'HWYT-fish',
  'whittle': 'HWIT-ul',
  'whizzed': 'HWIZD',
  'wholehearted': 'HOHL-har-tid',
  'whydah': 'HWEE-dah',
  'wickiup': 'WIK-ee-up',
  'widdershins': 'WID-er-shinz',
  'widely': 'WYD-lee',
  'widget': 'WIJ-it',
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
  'why': 'HWY'
};

async function updateWWords() {
  try {
    console.log('Processing W-words pronunciation batch...');
    
    // Get W-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'w%')
      .limit(150);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} W-words missing pronunciation`);
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
    
    console.log(`\nW-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`W-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 20) {
        console.log('Missing W-words:');
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
    console.error('W-words batch failed:', error);
  }
}

updateWWords();