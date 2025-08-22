const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Batch pronunciation updates - focusing on first 100 words
const pronunciations = {
  'gone': 'GAWN',
  'gonzo': 'GON-zoh',
  'goober': 'GOO-ber',
  'goodnik': 'GOOD-nik',
  'goods': 'GOODZ',
  'goofy': 'GOO-fee',
  'google': 'GOO-gul',
  'googly': 'GOO-glee',
  'googol': 'GOO-gol',
  'goondie': 'GOON-dee',
  'goosander': 'goo-SAN-der',
  'gorgon': 'GOR-gun',
  'gorilla': 'guh-RIL-uh',
  'gorp': 'GORP',
  'gosling': 'GOS-ling',
  'gossamer': 'GOS-uh-mer',
  'gossip': 'GOS-ip',
  'gotcha': 'GOT-chuh',
  'gothamite': 'GOTH-uh-myt',
  'gothic': 'GOTH-ik',
  'gouda': 'GOO-duh',
  'gouge': 'GOWJ',
  'gourd': 'GOORD',
  'grab': 'GRAB',
  'grace': 'GRAYS',
  'graduate': 'GRAD-yoo-it',
  'graham': 'GRAY-um',
  'grammarian': 'gruh-MAIR-ee-un',
  'grand': 'GRAND',
  'grande': 'GRAN-day',
  'grandeur': 'GRAN-jer',
  'grandeurgraphologist': 'GRAN-jer GRAF-ol-uh-jist',
  'grandeurottoman': 'GRAN-jer OT-uh-mun',
  'grandi': 'GRAN-dee',
  'grandiloquent': 'gran-DIL-uh-kwunt',
  'grandrelle': 'gran-DREL',
  'granite': 'GRAN-it',
  'granola': 'gruh-NOH-luh',
  'granules': 'GRAN-yoolz',
  'grapheme': 'GRAF-eem',
  'graphite': 'GRAF-yt',
  'graphologist': 'graf-OL-uh-jist',
  'grapple': 'GRAP-ul',
  'grass': 'GRAS',
  'grateful': 'GRAYT-ful',
  'graticule': 'GRAT-i-kyool',
  'gratingly': 'GRAYT-ing-lee',
  'gratis': 'GRAT-is',
  'gratitude': 'GRAT-i-tood',
  'gravelly': 'GRAV-ul-ee',
  'gravimetry': 'gruh-VIM-i-tree',
  'gravitas': 'GRAV-i-tas',
  'gravy': 'GRAY-vee',
  'graywacke': 'GRAY-wak',
  'grazioso': 'grah-tsee-OH-zoh',
  'greasy': 'GREE-see',
  'great': 'GRAYT',
  'greaves': 'GREEVZ',
  'grebe': 'GREEB',
  'grecque': 'GREK',
  'greedy': 'GREE-dee',
  'greek': 'GREEK',
  'green': 'GREEN',
  'greens': 'GREENZ',
  'greetingdifficulty': 'GREET-ing DIF-i-kul-tee',
  'gregorian': 'gruh-GOR-ee-un',
  'gressorial': 'gruh-SOR-ee-ul',
  'grew': 'GROO',
  'grewsome': 'GROO-sum',
  'grid': 'GRID',
  'gridiron': 'GRID-y-urn',
  'griefful': 'GREEF-ful',
  'grievance': 'GREE-vunts',
  'griffonage': 'GRIF-uh-nij',
  'grimaces': 'GRIM-is-iz',
  'grimthorpe': 'GRIM-thorp',
  'grimy': 'GRY-mee',
  'grins': 'GRINZ',
  'griot': 'GREE-oh',
  'grison': 'GREE-sun',
  'grisonphulkari': 'GREE-sun FUL-kar-ee',
  'grissino': 'grih-SEE-noh',
  'grit': 'GRIT',
  'grits': 'GRITS',
  'groats': 'GROHTS',
  'grobian': 'GROH-bee-un',
  'groceries': 'GROH-sur-eez',
  'groenendael': 'GROO-nun-dal',
  'groom': 'GROOM',
  'groove': 'GROOV',
  'grosgrain': 'GROH-grayn',
  'gross': 'GROHS',
  'grotesque': 'groh-TESK',
  'grotesqueness': 'groh-TESK-nis',
  'grotto': 'GROT-oh',
  'ground': 'GROWND',
  'group': 'GROOP',
  'grouped': 'GROOPT',
  'grouse': 'GROWS',
  'grousegubernatorial': 'GROWS goo-ber-nuh-TOR-ee-ul',
  'grout': 'GROWT',
  'grouth': 'GROWTH',
  'groves': 'GROHVZ',
  'growing': 'GROH-ing',
  'growling': 'GROWL-ing',
  'grown': 'GROHN',
  'grub': 'GRUB',
  'grudgingly': 'GRUJ-ing-lee',
  'grudginglycanopy': 'GRUJ-ing-lee KAN-uh-pee',
  'gruel': 'GROO-ul',
  'grueldifficulty': 'GROO-ul DIF-i-kul-tee',
  'gruelgroom': 'GROO-ul GROOM',
  'gruesome': 'GROO-sum',
  'grumbling': 'GRUM-bling',
  'grumpy': 'GRUM-pee'
};

async function updateBatch() {
  try {
    console.log('Starting final pronunciation batch update...');
    
    // Get current status
    const { data: allWords } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide');
    
    const total = allWords.length;
    const withPronunciation = allWords.filter(w => w.pronunciation_guide).length;
    console.log(`Current status: ${withPronunciation}/${total} (${((withPronunciation/total)*100).toFixed(1)}%)`);
    
    let updated = 0;
    
    for (const [word, pronunciation] of Object.entries(pronunciations)) {
      const wordData = allWords.find(w => w.word === word && !w.pronunciation_guide);
      
      if (wordData) {
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
      }
    }
    
    console.log(`\nBatch completed: ${updated} pronunciations added`);
    
    // Final status check
    const { data: finalStats } = await supabase
      .from('spelling_words')
      .select('pronunciation_guide');
      
    const finalTotal = finalStats.length;
    const finalWithPronunciation = finalStats.filter(w => w.pronunciation_guide).length;
    const finalProgress = ((finalWithPronunciation/finalTotal)*100).toFixed(1);
    
    console.log(`Final status: ${finalWithPronunciation}/${finalTotal} (${finalProgress}%)`);
    
  } catch (error) {
    console.error('Batch update failed:', error);
  }
}

updateBatch();