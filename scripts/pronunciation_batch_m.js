const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// M-words pronunciations
const pronunciations = {
  'macadam': 'muh-KAD-um',
  'macao': 'muh-KOW',
  'macaque': 'muh-KAHK',
  'macaroonbrazenness': 'mak-uh-ROON BRAY-zun-nis',
  'macau': 'muh-KOW',
  'macaw': 'muh-KAW',
  'macchiato': 'mah-kee-AH-toh',
  'macedonia': 'mas-uh-DOH-nee-uh',
  'machete': 'muh-SHET-ee',
  'machiavellian': 'mak-ee-uh-VEL-ee-un',
  'machicolation': 'muh-CHIK-uh-lay-shun',
  'machination': 'mak-uh-NAY-shun',
  'machine': 'muh-SHEEN',
  'macigno': 'mah-CHEE-nyoh',
  'mackerel': 'MAK-er-ul',
  'mackinaw': 'MAK-uh-naw',
  'macrobiotics': 'mak-roh-by-OT-iks',
  'macrocosm': 'MAK-roh-kozm',
  'macropterous': 'mak-ROP-ter-us',
  'macular': 'MAK-yuh-ler',
  'macushla': 'muh-KOOSH-luh',
  'madagascar': 'mad-uh-GAS-ker',
  'mademoiselle': 'mad-uh-mwah-ZEL',
  'madrigal': 'MAD-ri-gul',
  'magellan': 'muh-JEL-un',
  'magenta': 'muh-JEN-tuh',
  'magician': 'muh-JISH-un',
  'magistrates': 'MAJ-uh-strayts',
  'magma': 'MAG-muh',
  'magnate': 'MAG-nayt',
  'magnificent': 'mag-NIF-uh-sunt',
  'magnolia': 'mag-NOHL-yuh',
  'maharaja': 'mah-hah-RAH-juh',
  'maharajah': 'mah-hah-RAH-juh',
  'mahogany': 'muh-HOG-uh-nee',
  'maidenhair': 'MAY-dun-hair',
  'maillot': 'my-OH',
  'maize': 'MAYZ',
  'majeure': 'mah-ZER',
  'major': 'MAY-jer',
  'majuscule': 'muh-JUS-kyool',
  'makes': 'MAYKS',
  'makgadikgadi': 'mahk-gah-dee-KHAH-dee',
  'making': 'MAY-king',
  'malachite': 'MAL-uh-kyt',
  'malacology': 'mal-uh-KOL-uh-jee',
  'malady': 'MAL-uh-dee',
  'malaise': 'muh-LAYZ',
  'malapropism': 'MAL-uh-prop-izm',
  'male': 'MAYL',
  'males': 'MAYLZ',
  'malevolent': 'muh-LEV-uh-lunt',
  'malfeasance': 'mal-FEE-zuns',
  'malicious': 'muh-LISH-us',
  'malignant': 'muh-LIG-nunt',
  'malinger': 'muh-LING-ger',
  'malleable': 'MAL-ee-uh-bul',
  'malleolus': 'muh-LEE-uh-lus',
  'mallet': 'MAL-it',
  'malnutrition': 'mal-noo-TRISH-un',
  'mambo': 'MAM-boh',
  'mambomanacle': 'MAM-boh MAN-uh-kul',
  'mammal': 'MAM-ul',
  'mammalian': 'muh-MAY-lee-un',
  'mamushi': 'mah-MOO-shee',
  'manacle': 'MAN-uh-kul',
  'manage': 'MAN-ij',
  'manages': 'MAN-ij-iz',
  'mañana': 'mahn-YAH-nah',
  'mandarin': 'MAN-duh-rin',
  'mandate': 'MAN-dayt',
  'mandelbrot': 'MAN-dul-brot',
  'mandorla': 'man-DOR-lah',
  'mandragora': 'man-DRAG-uh-ruh',
  'mandrill': 'MAN-dril',
  'maneuverable': 'muh-NOO-ver-uh-bul',
  'mange': 'MAYNJ',
  'mangels': 'MANG-gulz',
  'manger': 'MAYN-jer',
  'mango': 'MANG-goh',
  'mangonel': 'MANG-guh-nel',
  'mangrove': 'MAN-grohv',
  'manhattan': 'man-HAT-un',
  'maniacal': 'muh-NY-uh-kul',
  'manifesto': 'man-uh-FES-toh',
  'manifests': 'MAN-uh-fests',
  'manipulable': 'muh-NIP-yuh-luh-bul',
  'manner': 'MAN-er',
  'mano': 'MAH-noh',
  'mansard': 'MAN-sard',
  'mansion': 'MAN-shun',
  'manta': 'MAN-tuh',
  'manteau': 'man-TOH',
  'mantel': 'MAN-tul',
  'manticore': 'MAN-ti-kor',
  'mantle': 'MAN-tul',
  'mantra': 'MAN-truh',
  'mantua': 'MAN-choo-uh',
  'manu': 'MAH-noo',
  'manualthe': 'MAN-yoo-ul THUH',
  'manufacture': 'man-yuh-FAK-cher',
  'manumit': 'MAN-yuh-mit',
  'manure': 'muh-NOOR',
  'manuscript': 'MAN-yuh-skript',
  'maquette': 'mah-KET',
  'maquillage': 'mah-kee-YAZH',
  'marathi': 'muh-RAH-thee',
  'marathon': 'MAIR-uh-thon',
  'marble': 'MAR-bul',
  'marcel': 'mar-SEL',
  'marcescent': 'mar-SES-unt',
  'marginalia': 'mar-jin-AY-lee-uh',
  'marginalize': 'MAR-jin-uh-lyz',
  'marguerite': 'mar-guh-REET',
  'maria': 'muh-REE-uh',
  'marimba': 'muh-RIM-buh',
  'marine': 'muh-REEN',
  'maringouin': 'mair-in-GWEEN',
  'marionette': 'mair-ee-uh-NET',
  'marionetteneapolitan': 'mair-ee-uh-NET nee-uh-POL-i-tun',
  'mariposa': 'mair-uh-POH-suh',
  'maritime': 'MAIR-uh-tym',
  'mark': 'MARK',
  'marked': 'MARKT',
  'markets': 'MAR-kits',
  'marksmanship': 'MARKS-mun-ship',
  'marmoset': 'MAR-muh-set',
  'marooned': 'muh-ROOND',
  'marquee': 'mar-KEE',
  'married': 'MAIR-eed',
  'marring': 'MAIR-ing',
  'marry': 'MAIR-ee',
  'mars': 'MARZ',
  'marsupial': 'mar-SOO-pee-ul',
  'marsupialtrefoil': 'mar-SOO-pee-ul TREE-foyl',
  'martial': 'MAR-shul',
  'martinet': 'mar-tuh-NET',
  'martinoe': 'mar-tee-NOH',
  'marvel': 'MAR-vul',
  'marvellous': 'MAR-vuh-lus',
  'marvelous': 'MAR-vuh-lus',
  'maryland': 'MAIR-uh-lund',
  'masa': 'MAH-sah',
  'mascarpone': 'mas-kar-POH-nay',
  'mashed': 'MASHT',
  'mask': 'MASK',
  'masks': 'MASKS',
  'mason': 'MAY-sun',
  'masse': 'ma-SAY',
  'masses': 'MAS-iz',
  'massestroganoff': 'MAS-iz STROH-guh-nof',
  'masseuse': 'mah-SOOZ',
  'mässig': 'MESS-ikh',
  'massive': 'MAS-iv',
  'mastering': 'MAS-ter-ing',
  'masthead': 'MAST-hed',
  'mastiff': 'MAS-tif',
  'mastodon': 'MAS-tuh-don',
  'matching': 'MACH-ing',
  'mater': 'MAY-ter',
  'materialize': 'muh-TEER-ee-uh-lyz',
  'maternity': 'muh-TER-ni-tee',
  'maternitybungee': 'muh-TER-ni-tee BUN-jee',
  'math': 'MATH',
  'mathematical': 'math-uh-MAT-i-kul',
  'mathematician': 'math-uh-muh-TISH-un',
  'matriculation': 'muh-trik-yuh-LAY-shun',
  'matrimony': 'MAT-ruh-moh-nee',
  'matterhorn': 'MAT-er-horn',
  'mattress': 'MAT-ris',
  'mausoleum': 'maw-suh-LEE-um',
  'mauve': 'MOHV',
  'maverick': 'MAV-er-ik',
  'mawkish': 'MAW-kish',
  'mawkishflambé': 'MAW-kish flam-BAY',
  'maxillae': 'mak-SIL-ee',
  'maximum': 'MAK-suh-mum',
  'maxwell': 'MAKS-wel',
  'maybe': 'MAY-bee',
  'mayhem': 'MAY-hem',
  'mayonnaise': 'may-uh-NAYZ',
  'mazda': 'MAZ-duh',
  'mccoy': 'muh-KOY',
  'mcintosh': 'MAK-in-tosh',
  'mcmansion': 'mik-MAN-shun',
  'meal': 'MEEL',
  'mean': 'MEEN',
  'meaning': 'MEE-ning',
  'meaningless': 'MEE-ning-lis',
  'means': 'MEENZ',
  'measly': 'MEE-zlee',
  'measurement': 'MEZH-er-munt',
  'meat': 'MEET',
  'mecca': 'MEK-uh',
  'mechanics': 'muh-KAN-iks',
  'medallion': 'muh-DAL-yun',
  'media': 'MEE-dee-uh',
  'mediaeval': 'mee-dee-EE-vul',
  'medias': 'MEE-dee-uhz',
  'medical': 'MED-i-kul',
  'medici': 'MED-i-chee',
  'medicine': 'MED-uh-sin',
  'medicines': 'MED-uh-sinz',
  'medieval': 'mee-dee-EE-vul',
  'mediobrome': 'mee-dee-oh-BROHM',
  'meditation': 'med-uh-TAY-shun',
  'mediterranean': 'med-uh-tuh-RAY-nee-un',
  'medium': 'MEE-dee-um',
  'medulla': 'muh-DUL-uh',
  'medusa': 'muh-DOO-suh',
  'meekness': 'MEEK-nis',
  'meet': 'MEET',
  'meeting': 'MEE-ting',
  'megacephalic': 'meg-uh-suh-FAL-ik',
  'megahertz': 'MEG-uh-herts',
  'megahertzgnash': 'MEG-uh-herts NASH',
  'megalomaniac': 'meg-uh-loh-MAY-nee-ak',
  'megaron': 'MEG-uh-ron',
  'megrims': 'MEE-grimz',
  'meiosis': 'my-OH-sis',
  'meitnerium': 'myt-NEER-ee-um',
  'melamine': 'MEL-uh-meen',
  'melancholy': 'MEL-un-kol-ee',
  'mele': 'MEH-lay',
  'melee': 'MAY-lay',
  'melismatic': 'mel-iz-MAT-ik',
  'mell': 'MEL',
  'mellifluous': 'muh-LIF-loo-us',
  'mellifluousclemency': 'muh-LIF-loo-us KLEM-un-see',
  'mellow': 'MEL-oh',
  'melodramatic': 'mel-oh-druh-MAT-ik',
  'melody': 'MEL-uh-dee',
  'melted': 'MEL-tid',
  'meltedmembership': 'MEL-tid MEM-ber-ship',
  'member': 'MEM-ber',
  'membership': 'MEM-ber-ship',
  'membrane': 'MEM-brayn',
  'memes': 'MEEMZ',
  'memorandum': 'mem-uh-RAN-dum',
  'memorial': 'muh-MOR-ee-ul',
  'menacing': 'MEN-uh-sing',
  'menagerie': 'muh-NAJ-uh-ree',
  'menaia': 'muh-NY-uh',
  'mendacious': 'men-DAY-shus',
  'mendicity': 'men-DIS-uh-tee',
  'menial': 'MEE-nee-ul',
  'meningitis': 'men-in-JY-tis',
  'meningitismephitic': 'men-in-JY-tis muh-FIT-ik',
  'menthol': 'MEN-thol',
  'mention': 'MEN-shun',
  'mentor': 'MEN-tor',
  'mephitic': 'muh-FIT-ik',
  'merak': 'MEE-rak',
  'mercenary': 'MER-suh-nair-ee',
  'merchandise': 'MER-chun-dyz',
  'mercury': 'MER-kyuh-ree',
  'merely': 'MEER-lee',
  'merfolk': 'MER-fohk',
  'merganser': 'mer-GAN-ser',
  'meridian': 'muh-RID-ee-un',
  'meringue': 'muh-RANG',
  'merino': 'muh-REE-noh',
  'merlin': 'MER-lin',
  'merriam': 'MAIR-ee-um',
  'merrier': 'MAIR-ee-er',
  'merrimack': 'MAIR-uh-mak'
};

async function updateMWords() {
  try {
    console.log('Processing M-words pronunciation batch...');
    
    // Get M-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'm%')
      .limit(250);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} M-words missing pronunciation`);
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
    
    console.log(`\nM-words batch completed: ${updated} pronunciations added`);
    
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
    console.error('M-words batch failed:', error);
  }
}

updateMWords();