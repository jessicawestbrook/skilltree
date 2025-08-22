const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Pronunciations for G-words batch
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
  'grumpy': 'GRUM-pee',
  'gruyère': 'groo-YAIR',
  'guam': 'GWAHM',
  'guan': 'GWAHN',
  'guanine': 'GWAH-neen',
  'guapena': 'gwah-PEH-nah',
  'guarantor': 'gar-un-TOR',
  'guardian': 'GAR-dee-un',
  'guarnerius': 'gwar-NAIR-ee-us',
  'guava': 'GWAH-vuh',
  'guayabera': 'gwy-uh-BAIR-uh',
  'gubernatorial': 'goo-ber-nuh-TOR-ee-ul',
  'gudgeon': 'GUJ-un',
  'guerilla': 'guh-RIL-uh',
  'guerite': 'guh-REET',
  'gueritegallivat': 'guh-REET GAL-i-vat',
  'guerrilla': 'guh-RIL-uh',
  'guess': 'GES',
  'gueule': 'GEL',
  'guffaw': 'guh-FAW',
  'guichet': 'gee-SHAY',
  'guido': 'GEE-doh',
  'guidonian': 'gwy-DOH-nee-un',
  'guilloche': 'gi-LOHSH',
  'guineas': 'GIN-eez',
  'gules': 'GYOOLZ',
  'gullet': 'GUL-it',
  'gullibility': 'gul-uh-BIL-i-tee',
  'gummy': 'GUM-ee',
  'gumption': 'GUMP-shun',
  'gung': 'GUNG',
  'gurdy': 'GER-dee',
  'gurmukhi': 'goor-MUK-hee',
  'gurmukhigyascutus': 'goor-MUK-hee jy-AS-kyoo-tus',
  'gurney': 'GER-nee',
  'gurneysanctimonious': 'GER-nee sangk-tuh-MOH-nee-us',
  'gushedchina': 'GUSHT CHY-nuh',
  'gustatory': 'GUS-tuh-tor-ee',
  'gusto': 'GUS-toh',
  'gutter': 'GUT-er',
  'guttural': 'GUT-er-ul',
  'gyascutus': 'jy-AS-kyoo-tus',
  'gyascutusgyokuro': 'jy-AS-kyoo-tus joh-koo-ROH',
  'gymnastics': 'jim-NAS-tiks',
  'gyokuro': 'joh-koo-ROH',
  'gypsophila': 'jip-SOF-i-luh',
  'gypsum': 'JIP-sum',
  'gyrocopter': 'JY-roh-kop-ter',
  'gyttja': 'GIT-yah'
};

async function updateGWords() {
  try {
    console.log('Processing G-words pronunciation batch...');
    
    // Get current G-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'g%')
      .limit(100);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} G-words missing pronunciation`);
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
    
    console.log(`\nG-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`G-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 10) {
        notFound.forEach(word => console.log(`- ${word}`));
      }
    }
    
    // Overall progress check
    const { data: finalStats } = await supabase
      .from('spelling_words')
      .select('pronunciation_guide');
      
    const finalTotal = finalStats.length;
    const finalWithPronunciation = finalStats.filter(w => w.pronunciation_guide).length;
    const finalProgress = ((finalWithPronunciation/finalTotal)*100).toFixed(1);
    
    console.log(`\nOverall progress: ${finalWithPronunciation}/${finalTotal} (${finalProgress}%)`);
    
  } catch (error) {
    console.error('G-words batch failed:', error);
  }
}

updateGWords();