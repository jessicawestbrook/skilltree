const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// L-words pronunciations
const pronunciations = {
  'limpkin': 'LIMP-kin',
  'lincoln': 'LING-kun',
  'line': 'LYN',
  'lineage': 'LIN-ee-ij',
  'linen': 'LIN-un',
  'lines': 'LYNZ',
  'lingua': 'LING-gwuh',
  'linguistic': 'ling-GWIS-tik',
  'linguistics': 'ling-GWIS-tiks',
  'linked': 'LINGKT',
  'linnet': 'LIN-it',
  'linsey': 'LIN-zee',
  'linstock': 'LIN-stok',
  'lionize': 'LY-uh-nyz',
  'lipophilic': 'lip-uh-FIL-ik',
  'liquefaction': 'lik-wuh-FAK-shun',
  'lisp': 'LISP',
  'listener': 'LIS-uh-ner',
  'listlessly': 'LIST-lis-lee',
  'lists': 'LISTS',
  'listsevery': 'LISTS EV-ree',
  'listspage': 'LISTS PAYJ',
  'lisztian': 'LIST-see-un',
  'litany': 'LIT-uh-nee',
  'literacy': 'LIT-er-uh-see',
  'literacydifficulty': 'LIT-er-uh-see DIF-i-kul-tee',
  'literally': 'LIT-er-uh-lee',
  'literatim': 'lit-uh-RAY-tim',
  'literature': 'LIT-er-uh-cher',
  'lithium': 'LITH-ee-um',
  'lithophone': 'LITH-uh-fohn',
  'lithuania': 'lith-oo-AY-nee-uh',
  'litigious': 'li-TIJ-us',
  'litmus': 'LIT-mus',
  'littoral': 'LIT-er-ul',
  'liturgy': 'LIT-er-jee',
  'live': 'LIV',
  'lived': 'LIVD',
  'liver': 'LIV-er',
  'livery': 'LIV-uh-ree',
  'lives': 'LIVZ',
  'livid': 'LIV-id',
  'living': 'LIV-ing',
  'llama': 'LAH-muh',
  'llanero': 'yah-NAIR-oh',
  'llullaillaco': 'yoo-yigh-YIGH-koh',
  'loathe': 'LOHTH',
  'lobectomy': 'loh-BEK-tuh-mee',
  'lobotomy': 'luh-BOT-uh-mee',
  'lobscouse': 'LOB-skows',
  'local': 'LOH-kul',
  'located': 'LOH-kay-tid',
  'locavore': 'LOH-kuh-vor',
  'loch': 'LOKH',
  'locker': 'LOK-er',
  'locus': 'LOH-kus',
  'locust': 'LOH-kust',
  'loess': 'LOH-is',
  'logarithmic': 'log-uh-RITH-mik',
  'loggia': 'LOH-juh',
  'logical': 'LOJ-i-kul',
  'logodaedaly': 'log-oh-DEE-duh-lee',
  'logographic': 'log-uh-GRAF-ik',
  'logographicarmistice': 'log-uh-GRAF-ik AR-mi-stis',
  'logothete': 'LOG-uh-theet',
  'logs': 'LOGZ',
  'lokelani': 'loh-kay-LAH-nee',
  'lolled': 'LOLD',
  'lollygag': 'LOL-ee-gag',
  'london': 'LUN-dun',
  'loneliness': 'LOHN-lee-nis',
  'longer': 'LAWNG-ger',
  'longest': 'LAWNG-gist',
  'longevous': 'lon-JEE-vus',
  'longitude': 'LON-ji-tood',
  'longtime': 'LAWNG-tym',
  'look': 'LOOK',
  'lookout': 'LOOK-owt',
  'looks': 'LOOKS',
  'loose': 'LOOS',
  'loppers': 'LOP-erz',
  'loquacious': 'loh-KWAY-shus',
  'lorikeet': 'LOR-i-keet',
  'lorikeetnoun': 'LOR-i-keet NOWN',
  'losing': 'LOO-zing',
  'lossy': 'LOS-ee',
  'lost': 'LOST',
  'louche': 'LOOSH',
  'loud': 'LOWD',
  'loudly': 'LOWD-lee',
  'louis': 'LOO-is',
  'louisiana': 'loo-ee-zee-AN-uh',
  'louisville': 'LOO-ee-vil',
  'lounge': 'LOWNJ',
  'loup': 'LOOP',
  'loupe': 'LOOP',
  'lousicide': 'LOW-si-syd',
  'lousy': 'LOW-zee',
  'lovage': 'LUV-ij',
  'love': 'LUV',
  'loved': 'LUVD',
  'loving': 'LUV-ing',
  'loyal': 'LOY-ul',
  'lozenge': 'LOZ-inj',
  'luau': 'LOO-ow',
  'lubbers': 'LUB-erz',
  'luciferin': 'loo-SIF-er-in',
  'lucky': 'LUK-ee',
  'lucrative': 'LOO-kruh-tiv',
  'luculent': 'LOO-kyuh-lunt',
  'luddite': 'LUD-yt',
  'ludicrous': 'LOO-di-krus',
  'luftmensch': 'LOOFT-mensh',
  'lugubrious': 'loo-GOO-bree-us',
  'lullaby': 'LUL-uh-by',
  'lumbar': 'LUM-bar',
  'lumen': 'LOO-mun',
  'lumenluthier': 'LOO-mun LOO-thee-er',
  'luminance': 'LOO-muh-nuns',
  'lunch': 'LUNCH',
  'lunulae': 'LOO-nyuh-lee',
  'lunulaem': 'LOO-nyuh-leem',
  'lupercalia': 'loo-per-KAY-lee-uh',
  'lupercaliam': 'loo-per-KAY-lee-um',
  'lupine': 'LOO-pyn',
  'lurching': 'LER-ching',
  'lurid': 'LOOR-id',
  'lustrum': 'LUS-trum',
  'lutheran': 'LOO-ther-un',
  'luthier': 'LOO-thee-er',
  'lutrine': 'LOO-tryn',
  'luxuriate': 'lug-ZHOOR-ee-ayt',
  'lymphoma': 'lim-FOH-muh',
  'lyricist': 'LEER-i-sist',
  'lysozyme': 'LY-suh-zym'
};

async function updateLWords() {
  try {
    console.log('Processing L-words pronunciation batch...');
    
    // Get L-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'l%')
      .limit(200);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} L-words missing pronunciation`);
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
    
    console.log(`\nL-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`L-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 20) {
        console.log('Missing L-words:');
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
    console.error('L-words batch failed:', error);
  }
}

updateLWords();