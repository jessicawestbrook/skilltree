const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// V-words pronunciations
const pronunciations = {
  'vacancy': 'VAY-kun-see',
  'vacant': 'VAY-kunt',
  'vacate': 'VAY-kayt',
  'vacation': 'vay-KAY-shun',
  'vaccinate': 'VAK-suh-nayt',
  'vaccination': 'vak-suh-NAY-shun',
  'vaccine': 'vak-SEEN',
  'vacillate': 'VAS-uh-layt',
  'vacuous': 'VAK-yoo-us',
  'vacuum': 'VAK-yoom',
  'vagabond': 'VAG-uh-bond',
  'vagary': 'VAG-uh-ree',
  'vagrant': 'VAY-grunt',
  'vague': 'VAYG',
  'vain': 'VAYN',
  'vainglory': 'VAYN-glor-ee',
  'vale': 'VAYL',
  'valence': 'VAY-luns',
  'valentine': 'VAL-un-tyn',
  'valet': 'VAL-it',
  'valiant': 'VAL-yunt',
  'valid': 'VAL-id',
  'validate': 'VAL-ih-dayt',
  'valley': 'VAL-ee',
  'valor': 'VAL-er',
  'valuable': 'VAL-yoo-uh-bul',
  'valuation': 'val-yoo-AY-shun',
  'value': 'VAL-yoo',
  'valve': 'VALV',
  'vampire': 'VAM-pyr',
  'van': 'VAN',
  'vandal': 'VAN-dul',
  'vandalism': 'VAN-dul-izm',
  'vane': 'VAYN',
  'vanguard': 'VAN-gard',
  'vanilla': 'vuh-NIL-uh',
  'vanish': 'VAN-ish',
  'vanity': 'VAN-ih-tee',
  'vanquish': 'VAN-kwish',
  'vapor': 'VAY-per',
  'vaporize': 'VAY-per-yz',
  'variable': 'VAIR-ee-uh-bul',
  'variant': 'VAIR-ee-unt',
  'variation': 'vair-ee-AY-shun',
  'varicose': 'VAIR-ih-kohs',
  'varied': 'VAIR-eed',
  'variety': 'vuh-RY-ih-tee',
  'various': 'VAIR-ee-us',
  'variscite': 'VAIR-ih-syt',
  'varnish': 'VAR-nish',
  'varsity': 'VAR-sih-tee',
  'vary': 'VAIR-ee',
  'vascular': 'VAS-kyuh-ler',
  'vase': 'VAYS',
  'vaseline': 'VAS-uh-leen',
  'vassal': 'VAS-ul',
  'vast': 'VAST',
  'vat': 'VAT',
  'vaudeville': 'VAWD-vil',
  'vault': 'VAWLT',
  'vaunt': 'VAWNT',
  'veal': 'VEEL',
  'veer': 'VEER',
  'vegetable': 'VEJ-tuh-bul',
  'vegetarian': 'vej-uh-TAIR-ee-un',
  'vegetate': 'VEJ-uh-tayt',
  'vegetation': 'vej-uh-TAY-shun',
  'vehement': 'VEE-uh-munt',
  'vehicle': 'VEE-ih-kul',
  'veil': 'VAYL',
  'vein': 'VAYN',
  'velocity': 'vuh-LOS-ih-tee',
  'velour': 'vuh-LOOR',
  'velvet': 'VEL-vit',
  'venal': 'VEE-nul',
  'vend': 'VEND',
  'vendor': 'VEN-der',
  'veneer': 'vuh-NEER',
  'venerable': 'VEN-er-uh-bul',
  'venerate': 'VEN-er-ayt',
  'vengeance': 'VEN-juns',
  'vengeful': 'VENJ-ful',
  'venison': 'VEN-ih-sun',
  'venom': 'VEN-um',
  'venomous': 'VEN-uh-mus',
  'vent': 'VENT',
  'ventilate': 'VEN-tuh-layt',
  'ventilation': 'ven-tuh-LAY-shun',
  'ventral': 'VEN-trul',
  'ventricle': 'VEN-trih-kul',
  'ventriloquist': 'ven-TRIL-uh-kwist',
  'venture': 'VEN-chur',
  'venturesome': 'VEN-chur-sum',
  'venue': 'VEN-yoo',
  'veracity': 'vuh-RAS-ih-tee',
  'veranda': 'vuh-RAN-duh',
  'verb': 'VERB',
  'verbal': 'VER-bul',
  'verbatim': 'ver-BAY-tim',
  'verbose': 'ver-BOHS',
  'verdict': 'VER-dikt',
  'verge': 'VERJ',
  'verify': 'VAIR-uh-fy',
  'verisimilitude': 'vair-ih-sih-MIL-ih-tood',
  'verism': 'VAIR-izm',
  'veritable': 'VAIR-ih-tuh-bul',
  'verity': 'VAIR-ih-tee',
  'vermeil': 'VER-mayl',
  'vermillion': 'ver-MIL-yun',
  'vermin': 'VER-min',
  'vernacular': 'ver-NAK-yuh-ler',
  'vernal': 'VER-nul',
  'versatile': 'VER-suh-tyl',
  'verse': 'VERS',
  'versed': 'VERST',
  'version': 'VER-zhun',
  'versus': 'VER-sus',
  'vertebra': 'VER-tuh-bruh',
  'vertebrate': 'VER-tuh-brit',
  'vertex': 'VER-teks',
  'vertical': 'VER-tih-kul',
  'vertigo': 'VER-tih-goh',
  'verve': 'VERV',
  'very': 'VAIR-ee',
  'vesicle': 'VES-ih-kul',
  'vesper': 'VES-per',
  'vessel': 'VES-ul',
  'vest': 'VEST',
  'vestal': 'VES-tul',
  'vestibule': 'VES-tih-byool',
  'vestige': 'VES-tij',
  'vestigial': 'ves-TIJ-ee-ul',
  'vestment': 'VEST-munt',
  'vestry': 'VES-tree',
  'veteran': 'VET-er-un',
  'veterinarian': 'vet-er-ih-NAIR-ee-un',
  'veterinary': 'VET-er-ih-nair-ee',
  'veto': 'VEE-toh',
  'vex': 'VEKS',
  'vexation': 'vek-SAY-shun',
  'via': 'VY-uh',
  'viable': 'VY-uh-bul',
  'viaduct': 'VY-uh-dukt',
  'vial': 'VY-ul',
  'viand': 'VY-und',
  'vibrant': 'VY-brunt',
  'vibrate': 'VY-brayt',
  'vibration': 'vy-BRAY-shun',
  'vicar': 'VIK-er',
  'vicarious': 'vy-KAIR-ee-us',
  'vice': 'VYS',
  'viceroy': 'VYS-roy',
  'vicinity': 'vuh-SIN-ih-tee',
  'vicious': 'VISH-us',
  'vicissitude': 'vuh-SIS-ih-tood',
  'victim': 'VIK-tim',
  'victor': 'VIK-ter',
  'victorious': 'vik-TOR-ee-us',
  'victory': 'VIK-ter-ee',
  'victual': 'VIT-ul',
  'video': 'VID-ee-oh',
  'vie': 'VY',
  'view': 'VYOO',
  'viewpoint': 'VYOO-poynt',
  'vigil': 'VIJ-il',
  'vigilant': 'VIJ-ih-lunt',
  'vigilante': 'vij-ih-LAN-tee',
  'vignette': 'vin-YET',
  'vigor': 'VIG-er',
  'vigorous': 'VIG-er-us',
  'vile': 'VYL',
  'vilify': 'VIL-uh-fy',
  'villa': 'VIL-uh',
  'village': 'VIL-ij',
  'villager': 'VIL-ij-er',
  'villain': 'VIL-un',
  'villainous': 'VIL-uh-nus',
  'villainy': 'VIL-uh-nee',
  'vim': 'VIM',
  'vinaigrette': 'vin-ih-GRET',
  'vine': 'VYN',
  'vinegar': 'VIN-ih-ger',
  'vineyard': 'VIN-yerd',
  'vintage': 'VIN-tij',
  'vinyl': 'VY-nul',
  'viola': 'vee-OH-luh',
  'violate': 'VY-uh-layt',
  'violation': 'vy-uh-LAY-shun',
  'violence': 'VY-uh-luns',
  'violent': 'VY-uh-lunt',
  'violet': 'VY-uh-lit',
  'violin': 'vy-uh-LIN',
  'violinist': 'vy-uh-LIN-ist',
  'viper': 'VY-per',
  'virgin': 'VER-jin',
  'virginity': 'ver-JIN-ih-tee',
  'virgule': 'VER-gyool',
  'virile': 'VEER-il',
  'virility': 'vuh-RIL-ih-tee',
  'virtual': 'VER-choo-ul',
  'virtue': 'VER-choo',
  'virtuous': 'VER-choo-us',
  'virtuoso': 'ver-choo-OH-soh',
  'virulent': 'VEER-yuh-lunt',
  'virus': 'VY-rus',
  'visa': 'VEE-zuh',
  'visage': 'VIZ-ij',
  'viscera': 'VIS-er-uh',
  'visceral': 'VIS-er-ul',
  'viscid': 'VIS-id',
  'viscount': 'VY-kownt',
  'viscous': 'VIS-kus',
  'vise': 'VYS',
  'visibility': 'viz-uh-BIL-ih-tee',
  'visible': 'VIZ-uh-bul',
  'vision': 'VIZH-un',
  'visionary': 'VIZH-uh-nair-ee',
  'visit': 'VIZ-it',
  'visitor': 'VIZ-ih-ter',
  'visor': 'VY-zer',
  'vista': 'VIS-tuh',
  'visual': 'VIZH-oo-ul',
  'visualize': 'VIZH-oo-uh-lyz',
  'vital': 'VY-tul',
  'vitality': 'vy-TAL-ih-tee',
  'vitalize': 'VY-tuh-lyz',
  'vitamin': 'VY-tuh-min',
  'vitiate': 'VISH-ee-ayt',
  'vitreous': 'VIT-ree-us',
  'vitriol': 'VIT-ree-ul',
  'vitriolic': 'vit-ree-OL-ik',
  'vivacious': 'vuh-VAY-shus',
  'vivacity': 'vuh-VAS-ih-tee',
  'vivid': 'VIV-id',
  'vixen': 'VIK-sun',
  'vocabulary': 'voh-KAB-yuh-lair-ee',
  'vocal': 'VOH-kul',
  'vocalist': 'VOH-kuh-list',
  'vocation': 'voh-KAY-shun',
  'vocational': 'voh-KAY-shuh-nul',
  'vocative': 'VOK-uh-tiv',
  'vociferous': 'voh-SIF-er-us',
  'vodka': 'VOD-kuh',
  'vogue': 'VOHG',
  'voice': 'VOYS',
  'void': 'VOYD',
  'voile': 'VOYL',
  'volatile': 'VOL-uh-tyl',
  'volatility': 'vol-uh-TIL-ih-tee',
  'volcanic': 'vol-KAN-ik',
  'volcano': 'vol-KAY-noh',
  'volition': 'voh-LISH-un',
  'volley': 'VOL-ee',
  'volleyball': 'VOL-ee-bawl',
  'volt': 'VOHLT',
  'voltage': 'VOHL-tij',
  'voluble': 'VOL-yuh-bul',
  'volume': 'VOL-yoom',
  'voluminous': 'vuh-LOO-muh-nus',
  'voluntary': 'VOL-un-tair-ee',
  'volunteer': 'vol-un-TEER',
  'voluptuous': 'vuh-LUP-choo-us',
  'vomit': 'VOM-it',
  'voracious': 'vor-AY-shus',
  'vortex': 'VOR-teks',
  'votary': 'VOH-tuh-ree',
  'vote': 'VOHT',
  'voter': 'VOH-ter',
  'vouch': 'VOWCH',
  'voucher': 'VOW-cher',
  'vouchsafe': 'vowch-SAYF',
  'vow': 'VOW',
  'vowel': 'VOW-ul',
  'voyage': 'VOY-ij',
  'voyager': 'VOY-ij-er',
  'voyeur': 'voy-UR',
  'vulgar': 'VUL-ger',
  'vulgarity': 'vul-GAIR-ih-tee',
  'vulnerable': 'VUL-ner-uh-bul',
  'vulpine': 'VUL-pyn',
  'vulture': 'VUL-chur'
};

async function updateVWords() {
  try {
    console.log('Processing V-words pronunciation batch...');
    
    // Get V-words missing pronunciations
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word')
      .is('pronunciation_guide', null)
      .ilike('word', 'v%')
      .limit(200);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate.length} V-words missing pronunciation`);
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
    
    console.log(`\nV-words batch completed: ${updated} pronunciations added`);
    
    if (notFound.length > 0) {
      console.log(`V-words not found in our list: ${notFound.length}`);
      if (notFound.length <= 50) {
        console.log('Missing V-words:');
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
    console.error('V-words batch failed:', error);
  }
}

updateVWords();