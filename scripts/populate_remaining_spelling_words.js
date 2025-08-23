const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Dictionary definitions for the remaining words
const wordDefinitions = {
  'allelopathy': {
    definition: 'The chemical inhibition of one plant by another due to the release of toxic substances',
    pronunciation: 'al-leh-LOP-uh-thee',
    etymology: 'From Greek allos (other) + pathos (suffering)',
    example: 'The walnut tree exhibits allelopathy, preventing other plants from growing near its roots.'
  },
  'astrologers': {
    definition: 'People who study the movements and positions of celestial bodies to predict earthly events',
    pronunciation: 'uh-STROL-uh-jerz',
    etymology: 'From Greek astron (star) + logos (study)',
    example: 'Ancient astrologers believed the planets influenced human behavior.'
  },
  'big-time': {
    definition: 'On a large scale; at the highest level; very successful or important',
    pronunciation: 'BIG-time',
    etymology: 'American slang from early 20th century',
    example: 'She made it big-time when her novel became a bestseller.'
  },
  'bipolar': {
    definition: 'Having two opposite poles or extremes; relating to a mental disorder with alternating manic and depressive episodes',
    pronunciation: 'bye-POH-lar',
    etymology: 'From Latin bi- (two) + polaris (of the pole)',
    example: 'The bipolar disorder causes extreme mood swings between mania and depression.'
  },
  'boogie-woogie': {
    definition: 'A style of blues piano playing with a regular left-hand bass pattern',
    pronunciation: 'BOO-gee-WOO-gee',
    etymology: 'African American origin, possibly from West African languages',
    example: 'The pianist played an energetic boogie-woogie that got everyone dancing.'
  },
  'cardiopathy': {
    definition: 'Any disease or disorder of the heart',
    pronunciation: 'kar-dee-OP-uh-thee',
    etymology: 'From Greek kardia (heart) + pathos (disease)',
    example: 'The patient was diagnosed with cardiopathy after experiencing chest pains.'
  },
  'cookie-cutter': {
    definition: 'Mass-produced or lacking individuality; made to a standard pattern',
    pronunciation: 'KOOK-ee-KUT-er',
    etymology: 'From the tool used to cut cookie dough into shapes',
    example: 'The subdivision was full of cookie-cutter houses that all looked the same.'
  },
  'derring-do': {
    definition: 'Brave and heroic deeds; daring action',
    pronunciation: 'DARE-ing-DOO',
    etymology: 'From Middle English dorryng do, meaning "daring to do"',
    example: 'The knight\'s tales of derring-do inspired the young squires.'
  },
  'different': {
    definition: 'Not the same as another; distinct or separate',
    pronunciation: 'DIF-er-ent',
    etymology: 'From Latin differre (to carry apart)',
    example: 'Each snowflake has a different pattern.'
  },
  'dillydally': {
    definition: 'To waste time through indecision or loitering',
    pronunciation: 'DIL-ee-DAL-ee',
    etymology: 'Reduplication possibly from "dally"',
    example: 'Don\'t dillydally or we\'ll be late for the movie.'
  },
  'dodgy': {
    definition: 'Evasive, tricky, or unreliable; of doubtful quality',
    pronunciation: 'DOJ-ee',
    etymology: 'British slang from "dodge"',
    example: 'That used car dealer seems a bit dodgy to me.'
  },
  'donna': {
    definition: 'An Italian title of respect for a woman, equivalent to lady',
    pronunciation: 'DON-nah',
    etymology: 'From Latin domina (mistress, lady)',
    example: 'Donna Maria was respected throughout the village.'
  },
  'drag': {
    definition: 'To pull along with effort; something tedious; clothing worn by a performer impersonating another gender',
    pronunciation: 'drag',
    etymology: 'From Old Norse draga (to draw)',
    example: 'The heavy suitcase was a drag to carry up the stairs.'
  },
  'dreadlocks': {
    definition: 'Hair worn in rope-like strands formed by matting or braiding',
    pronunciation: 'DRED-locks',
    etymology: 'From dread (fear, awe) + locks (hair), associated with Rastafarian culture',
    example: 'Bob Marley was famous for his dreadlocks.'
  },
  'dromic': {
    definition: 'Relating to or suitable for running; pertaining to a racecourse',
    pronunciation: 'DROH-mik',
    etymology: 'From Greek dromos (running, racecourse)',
    example: 'The dromic track was designed for speed racing.'
  },
  'dulcinea': {
    definition: 'A sweetheart or lady love; an idealized woman',
    pronunciation: 'dul-sin-AY-uh',
    etymology: 'From Don Quixote\'s idealized love, Spanish dulce (sweet)',
    example: 'He wrote sonnets to his dulcinea every day.'
  },
  'durango': {
    definition: 'A state in northwestern Mexico; its capital city',
    pronunciation: 'doo-RANG-go',
    etymology: 'From Basque Urango, meaning "water town"',
    example: 'The film was shot on location in Durango, Mexico.'
  },
  'earmark': {
    definition: 'To designate for a specific purpose; an identifying mark',
    pronunciation: 'EER-mark',
    etymology: 'From the practice of marking livestock ears',
    example: 'The funds were earmarked for educational programs.'
  },
  'evo-devo': {
    definition: 'Evolutionary developmental biology; the study of how evolution affects development',
    pronunciation: 'EE-voh-DEE-voh',
    etymology: 'Abbreviation of evolutionary developmental biology',
    example: 'Evo-devo explains how small genetic changes can cause major evolutionary shifts.'
  },
  'fortran': {
    definition: 'A high-level computer programming language especially suited to numeric computation',
    pronunciation: 'FOR-tran',
    etymology: 'From Formula Translation',
    example: 'Many scientific calculations are still performed using FORTRAN.'
  },
  'frabjous': {
    definition: 'Fabulous and joyous; wonderful',
    pronunciation: 'FRAB-jus',
    etymology: 'Coined by Lewis Carroll in "Jabberwocky"',
    example: 'O frabjous day! Callooh! Callay!'
  },
  'fuddy-duddy': {
    definition: 'A person who is old-fashioned and fussy',
    pronunciation: 'FUD-ee-DUD-ee',
    etymology: 'American slang, origin uncertain',
    example: 'Don\'t be such a fuddy-duddy; try the new restaurant!'
  },
  'hocus-pocus': {
    definition: 'Meaningless talk used to deceive; sleight of hand; trickery',
    pronunciation: 'HOH-kus-POH-kus',
    etymology: 'Mock Latin used by conjurers',
    example: 'The magician shouted "hocus-pocus" as he performed the trick.'
  },
  'hoity-toity': {
    definition: 'Haughty and pretentious; putting on airs',
    pronunciation: 'HOY-tee-TOY-tee',
    etymology: 'Possibly from obsolete hoit (to romp)',
    example: 'She became hoity-toity after winning the lottery.'
  },
  'hokus-pokus': {
    definition: 'Alternative spelling of hocus-pocus; trickery or nonsense',
    pronunciation: 'HOH-kus-POH-kus',
    etymology: 'Variant of hocus-pocus',
    example: 'The contract was full of legal hokus-pokus.'
  },
  'hunky-dory': {
    definition: 'Quite satisfactory; fine',
    pronunciation: 'HUN-kee-DOR-ee',
    etymology: 'American slang, possibly from Dutch honk (home base)',
    example: 'Everything is hunky-dory now that the problem is solved.'
  },
  'jiggery-pokery': {
    definition: 'Dishonest or suspicious activity; trickery',
    pronunciation: 'JIG-er-ee-POH-ker-ee',
    etymology: 'Scottish dialect, probably from joukery-pawkery',
    example: 'There\'s some jiggery-pokery going on with those financial records.'
  },
  'landline': {
    definition: 'A telephone connection that uses wires rather than radio waves',
    pronunciation: 'LAND-line',
    etymology: 'From land + line',
    example: 'Many homes no longer have a landline, relying only on cell phones.'
  },
  'mountebank': {
    definition: 'A charlatan; a person who deceives others, especially to obtain money',
    pronunciation: 'MOUN-tuh-bank',
    etymology: 'From Italian montambanco (one who mounts a bench)',
    example: 'The mountebank sold fake medicine to gullible customers.'
  },
  'niminy-piminy': {
    definition: 'Affectedly refined; mincing',
    pronunciation: 'NIM-in-ee-PIM-in-ee',
    etymology: 'Imitative of affected speech',
    example: 'Her niminy-piminy manners annoyed her more casual friends.'
  },
  'parishioner': {
    definition: 'A member or inhabitant of a parish',
    pronunciation: 'puh-RISH-un-er',
    etymology: 'From Middle English parissh + -ioner',
    example: 'The parishioners gathered for Sunday service.'
  },
  'podunk': {
    definition: 'A small, unimportant, and isolated town',
    pronunciation: 'POH-dunk',
    etymology: 'From Algonquian, name of a place in Connecticut',
    example: 'He left his podunk hometown to seek fame in the big city.'
  },
  'rabble-rouser': {
    definition: 'A person who stirs up the emotions of the masses',
    pronunciation: 'RAB-ul-ROW-zer',
    etymology: 'From rabble + rouse',
    example: 'The rabble-rouser incited the crowd to protest.'
  },
  'sententious': {
    definition: 'Given to moralizing in a pompous manner; terse and energetic in expression',
    pronunciation: 'sen-TEN-shus',
    etymology: 'From Latin sententia (opinion, maxim)',
    example: 'His sententious remarks about hard work annoyed his colleagues.'
  },
  'sparrow': {
    definition: 'A small brown and gray bird common in many parts of the world',
    pronunciation: 'SPAR-oh',
    etymology: 'From Old English spearwa',
    example: 'A sparrow built its nest under the eaves of our house.'
  },
  'spelling': {
    definition: 'The forming of words from letters; the way a word is spelled',
    pronunciation: 'SPEL-ing',
    etymology: 'From spell + -ing',
    example: 'Good spelling is important in formal writing.'
  },
  'spic-and-span': {
    definition: 'Spotlessly clean and neat',
    pronunciation: 'spik-and-SPAN',
    etymology: 'From spick (spike, nail) + span-new (brand new)',
    example: 'The house was spic-and-span for the guests.'
  },
  'spick-and-span': {
    definition: 'Alternative spelling of spic-and-span; perfectly clean',
    pronunciation: 'spik-and-SPAN',
    etymology: 'Variant of spic-and-span',
    example: 'She kept her kitchen spick-and-span.'
  },
  'sprung': {
    definition: 'Past participle of spring; having jumped or leaped',
    pronunciation: 'sprung',
    etymology: 'From Old English springan',
    example: 'The trap had already sprung when we arrived.'
  },
  'unprepossessing': {
    definition: 'Not attractive or appealing to the eye',
    pronunciation: 'un-pree-puh-ZES-ing',
    etymology: 'From un- + prepossessing',
    example: 'Despite his unprepossessing appearance, he was quite charming.'
  },
  'wanted': {
    definition: 'Desired or wished for; being searched for by the police',
    pronunciation: 'WON-tid',
    etymology: 'From want + -ed',
    example: 'The wanted criminal was finally captured.'
  },
  'wi-fi': {
    definition: 'A technology for wireless local area networking',
    pronunciation: 'WYE-fye',
    etymology: 'From Wireless Fidelity',
    example: 'The coffee shop offers free wi-fi to customers.'
  },
  'windbaggery': {
    definition: 'Verbose and empty talk',
    pronunciation: 'WIND-bag-er-ee',
    etymology: 'From windbag + -ery',
    example: 'The politician\'s speech was pure windbaggery.'
  },
  'worrywart': {
    definition: 'A person who worries excessively',
    pronunciation: 'WUR-ee-wort',
    etymology: 'American slang from worry + wart',
    example: 'Don\'t be such a worrywart; everything will be fine.'
  },
  'wunderkind': {
    definition: 'A person who achieves great success at a young age; a child prodigy',
    pronunciation: 'VOON-der-kind',
    etymology: 'German: Wunder (wonder) + Kind (child)',
    example: 'Mozart was a musical wunderkind who composed at age five.'
  },
  'yankee': {
    definition: 'An American, especially from the northern states; a Union soldier in the Civil War',
    pronunciation: 'YANG-kee',
    etymology: 'Possibly from Dutch Janke (little Jan)',
    example: 'The British called the American colonists Yankees.'
  },
  'yoo-hoo': {
    definition: 'An exclamation used to attract attention',
    pronunciation: 'YOO-hoo',
    etymology: 'Imitative',
    example: 'She called "yoo-hoo" to get her friend\'s attention.'
  },
  'zowie': {
    definition: 'An exclamation expressing surprise or admiration',
    pronunciation: 'ZOW-ee',
    etymology: 'American slang, imitative',
    example: 'Zowie! That\'s an amazing magic trick!'
  },
  'zydeco': {
    definition: 'A form of American folk music originating in Louisiana, combining blues, rhythm and blues, and Cajun music',
    pronunciation: 'ZYE-dih-koh',
    etymology: 'From Louisiana Creole, possibly from French les haricots (the beans)',
    example: 'The zydeco band played accordion and washboard music.'
  }
};

async function populateDefinitions() {
  console.log('=== POPULATING DEFINITIONS FOR REMAINING WORDS ===\n');
  
  const timestamp = Date.now();
  const progressFile = `scripts/definition_population_progress_${timestamp}.json`;
  let progress = {
    timestamp: new Date().toISOString(),
    processed: [],
    errors: [],
    skipped: []
  };
  
  try {
    // Get words without definitions
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty')
      .is('definition', null)
      .order('word');
    
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsToUpdate?.length || 0} words without definitions\n`);
    
    let updateCount = 0;
    
    for (const { word, source_difficulty } of wordsToUpdate || []) {
      const definition = wordDefinitions[word];
      
      if (definition) {
        console.log(`Updating: ${word} (${source_difficulty})`);
        
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({
            definition: definition.definition,
            pronunciation_guide: definition.pronunciation,
            etymology: definition.etymology,
            example_sentence: definition.example
          })
          .eq('word', word);
        
        if (updateError) {
          console.error(`  ❌ Error updating ${word}:`, updateError.message);
          progress.errors.push({ word, error: updateError.message });
        } else {
          console.log(`  ✅ Updated successfully`);
          progress.processed.push(word);
          updateCount++;
        }
        
        // Small delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 100));
      } else {
        console.log(`⚠️ No definition found for: ${word}`);
        progress.skipped.push(word);
      }
      
      // Save progress periodically
      if (updateCount % 10 === 0) {
        fs.writeFileSync(progressFile, JSON.stringify(progress, null, 2));
      }
    }
    
    // Final save
    fs.writeFileSync(progressFile, JSON.stringify(progress, null, 2));
    
    // Verify results
    const { count: remainingCount } = await supabase
      .from('spelling_words')
      .select('word', { count: 'exact', head: true })
      .is('definition', null);
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ POPULATION COMPLETE!');
    console.log('='.repeat(60));
    console.log(`Updated: ${updateCount} words`);
    console.log(`Errors: ${progress.errors.length}`);
    console.log(`Skipped: ${progress.skipped.length}`);
    console.log(`Remaining without definitions: ${remainingCount}`);
    console.log(`\nProgress saved to: ${progressFile}`);
    
    if (remainingCount === 0) {
      console.log('\n🎉 All spelling words now have definitions!');
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

populateDefinitions().catch(console.error);