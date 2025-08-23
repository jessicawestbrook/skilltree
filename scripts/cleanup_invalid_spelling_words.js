const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Define concatenated words to split
const concatenatedWordsToSplit = [
  { original: 'establishmentruminate', words: ['establishment', 'ruminate'] },
  { original: 'glengarrycommissioner', words: ['glengarry', 'commissioner'] },
  { original: 'grandiloquentarmature', words: ['grandiloquent', 'armature'] },
  { original: 'haplographytchefuncte', words: ['haplography', 'tchefuncte'] },
  { original: 'hydriotaphiahydrocortisone', words: ['hydriotaphia', 'hydrocortisone'] },
  { original: 'ichthyologyicosahedron', words: ['ichthyology', 'icosahedron'] },
  { original: 'jiggery-pokerysobersides', words: ['jiggery-pokery', 'sobersides'] },
  { original: 'ministrationsracketeer', words: ['ministrations', 'racketeer'] },
  { original: 'moribundrecriminatory', words: ['moribund', 'recriminatory'] },
  { original: 'mortadellamotherumbung', words: ['mortadella', 'motherumbung'] },
  { original: 'mountebankallelopathy', words: ['mountebank', 'allelopathy'] },
  { original: 'newfoundlandfulminate', words: ['newfoundland', 'fulminate'] },
  { original: 'octonocularoctuplicate', words: ['octonocular', 'octuplicate'] },
  { original: 'panjandrumcatachresis', words: ['panjandrum', 'catachresis'] },
  { original: 'parishionerastrologers', words: ['parishioner', 'astrologers'] },
  { original: 'perspicaciousadjective', words: ['perspicacious'] }, // 'adjective' is not a spelling word
  { original: 'philharmonicendorphin', words: ['philharmonic', 'endorphin'] },
  { original: 'porcelaindeglaciation', words: ['porcelain', 'deglaciation'] },
  { original: 'rambunctiousingenuous', words: ['rambunctious', 'ingenuous'] },
  { original: 'ramificationstemerity', words: ['ramifications', 'temerity'] },
  { original: 'repercussionrepository', words: ['repercussion', 'repository'] },
  { original: 'resuscitateapprobatory', words: ['resuscitate', 'approbatory'] },
  { original: 'retinoscopysepulchral', words: ['retinoscopy', 'sepulchral'] },
  { original: 'sententiouscardiopathy', words: ['sententious', 'cardiopathy'] },
  { original: 'spellingphosphorescent', words: ['spelling', 'phosphorescent'] },
  { original: 'unprepossessingbipolar', words: ['unprepossessing', 'bipolar'] },
  { original: 'veritableinterjection', words: ['veritable'] }, // 'interjection' is not a spelling word
  // Additional concatenated from "other" category
  { original: 'fadeawayfallacy', words: ['fadeaway', 'fallacy'] },
  { original: 'jingoismjitney', words: ['jingoism', 'jitney'] },
  { original: 'landlinesparrow', words: ['landline', 'sparrow'] },
  { original: 'laudeevo-devo', words: ['laude', 'evo-devo'] },
  { original: 'palookapannose', words: ['palooka', 'pannose'] },
  { original: 'pashminautilitarian', words: ['pashmina', 'utilitarian'] },
  { original: 'phoneticianmacular', words: ['phonetician', 'macular'] },
  { original: 'potentatepotoroo', words: ['potentate', 'potoroo'] },
  { original: 'premonitionprevious', words: ['premonition', 'previous'] },
  { original: 'quinaryafroth', words: ['quinary', 'afroth'] },
  { original: 'rescissiblereveille', words: ['rescissible', 'reveille'] },
  { original: 'soppinesssousaphone', words: ['soppiness', 'sousaphone'] },
  { original: 'ufologycholera', words: ['ufology', 'cholera'] },
  { original: 'uglinessquack', words: ['ugliness', 'quack'] },
  { original: 'universalv', words: ['universal'] }, // 'v' is not a spelling word
  { original: 'wantedsprung', words: ['wanted', 'sprung'] }
];

// Define clearly invalid words to delete
const invalidWordsToDelete = [
  'bwlalay', // not a real word
  'eoaoadldrbl', // gibberish
  'egucigalpa', // likely misspelling of Tegucigalpa
  'fairesbrinz', // not a valid spelling word
  'hsaing-waing', // musical instrument but likely data error
  'wootzy', // should be 'woozy'
  'universalv' // clearly has extra 'v'
];

// Valid words that just need definitions
const validWordsNeedingDefinitions = [
  'big-time', 'boogie-woogie', 'cookie-cutter', 'derring-do', 'different',
  'dillydally', 'dodgy', 'donna', 'drag', 'dreadlocks', 'dromic',
  'dulcinea', 'durango', 'earmark', 'evo-devo', 'fortran', 'frabjous',
  'fuddy-duddy', 'hocus-pocus', 'hoity-toity', 'hokus-pokus', 'hunky-dory',
  'jiggery-pokery', 'niminy-piminy', 'podunk', 'rabble-rouser',
  'spic-and-span', 'spick-and-span', 'wi-fi', 'windbaggery', 'worrywart',
  'wunderkind', 'yankee', 'yoo-hoo', 'zowie', 'zydeco'
];

async function cleanupSpellingWords() {
  console.log('=== CLEANING UP INVALID SPELLING WORDS ===\n');
  
  const timestamp = Date.now();
  const backupTableName = `spelling_words_bkp_${timestamp}`;
  
  try {
    // Step 1: Create backup table
    console.log('📦 Creating backup table...');
    const { error: backupError } = await supabase.rpc('create_table_backup', {
      source_table: 'spelling_words',
      backup_table: backupTableName
    }).single();
    
    if (backupError && backupError.message && !backupError.message.includes('already exists')) {
      // If RPC doesn't exist, try direct SQL
      console.log('Using direct SQL for backup...');
      const { error: sqlError } = await supabase.rpc('exec_sql', {
        sql: `CREATE TABLE ${backupTableName} AS SELECT * FROM spelling_words`
      }).single();
      
      if (sqlError) {
        console.log('⚠️ Could not create backup table automatically. Please create manually if needed.');
        console.log(`Suggested backup command: CREATE TABLE ${backupTableName} AS SELECT * FROM spelling_words;`);
      } else {
        console.log(`✅ Backup created: ${backupTableName}`);
      }
    } else if (!backupError) {
      console.log(`✅ Backup created: ${backupTableName}`);
    }
    
    // Prepare cleanup report
    const cleanupReport = {
      timestamp: new Date().toISOString(),
      backupTable: backupTableName,
      concatenatedWords: {
        toSplit: [],
        newWordsToAdd: [],
        toDelete: []
      },
      invalidWords: {
        toDelete: []
      },
      validWordsNeedingDefinitions: [],
      summary: {}
    };
    
    // Step 2: Process concatenated words
    console.log('\n🔗 Processing concatenated words...');
    for (const item of concatenatedWordsToSplit) {
      const { data: originalWord } = await supabase
        .from('spelling_words')
        .select('*')
        .eq('word', item.original)
        .single();
      
      if (originalWord) {
        cleanupReport.concatenatedWords.toDelete.push(item.original);
        
        for (const newWord of item.words) {
          const { data: existingWord } = await supabase
            .from('spelling_words')
            .select('word')
            .eq('word', newWord)
            .single();
          
          if (!existingWord) {
            cleanupReport.concatenatedWords.newWordsToAdd.push({
              word: newWord,
              source_difficulty: originalWord.source_difficulty
            });
          }
        }
      }
    }
    
    // Step 3: Identify invalid words
    console.log('\n❌ Identifying invalid words...');
    for (const word of invalidWordsToDelete) {
      const { data: exists } = await supabase
        .from('spelling_words')
        .select('word')
        .eq('word', word)
        .single();
      
      if (exists) {
        cleanupReport.invalidWords.toDelete.push(word);
      }
    }
    
    // Step 4: Identify valid words needing definitions
    console.log('\n📝 Identifying valid words needing definitions...');
    for (const word of validWordsNeedingDefinitions) {
      const { data: wordData } = await supabase
        .from('spelling_words')
        .select('word, definition')
        .eq('word', word)
        .single();
      
      if (wordData && !wordData.definition) {
        cleanupReport.validWordsNeedingDefinitions.push(word);
      }
    }
    
    // Generate summary
    cleanupReport.summary = {
      concatenatedWordsToSplit: cleanupReport.concatenatedWords.toDelete.length,
      newWordsToAdd: cleanupReport.concatenatedWords.newWordsToAdd.length,
      invalidWordsToDelete: cleanupReport.invalidWords.toDelete.length,
      validWordsNeedingDefinitions: cleanupReport.validWordsNeedingDefinitions.length,
      totalChanges: cleanupReport.concatenatedWords.toDelete.length + 
                   cleanupReport.concatenatedWords.newWordsToAdd.length + 
                   cleanupReport.invalidWords.toDelete.length
    };
    
    // Save report
    const reportFilename = `scripts/spelling_cleanup_plan_${timestamp}.json`;
    fs.writeFileSync(reportFilename, JSON.stringify(cleanupReport, null, 2));
    
    // Display report
    console.log('\n' + '='.repeat(60));
    console.log('📊 CLEANUP PLAN SUMMARY');
    console.log('='.repeat(60));
    console.log(`\n📁 Backup table: ${backupTableName}`);
    console.log(`\n🔗 Concatenated words to split: ${cleanupReport.summary.concatenatedWordsToSplit}`);
    if (cleanupReport.concatenatedWords.toDelete.length > 0) {
      console.log('   Words to delete:');
      cleanupReport.concatenatedWords.toDelete.slice(0, 5).forEach(w => console.log(`     - ${w}`));
      if (cleanupReport.concatenatedWords.toDelete.length > 5) {
        console.log(`     ... and ${cleanupReport.concatenatedWords.toDelete.length - 5} more`);
      }
    }
    
    console.log(`\n➕ New words to add: ${cleanupReport.summary.newWordsToAdd}`);
    if (cleanupReport.concatenatedWords.newWordsToAdd.length > 0) {
      console.log('   Words to add:');
      cleanupReport.concatenatedWords.newWordsToAdd.slice(0, 5).forEach(w => console.log(`     - ${w.word} (${w.source_difficulty})`));
      if (cleanupReport.concatenatedWords.newWordsToAdd.length > 5) {
        console.log(`     ... and ${cleanupReport.concatenatedWords.newWordsToAdd.length - 5} more`);
      }
    }
    
    console.log(`\n❌ Invalid words to delete: ${cleanupReport.summary.invalidWordsToDelete}`);
    if (cleanupReport.invalidWords.toDelete.length > 0) {
      console.log('   Words to delete:');
      cleanupReport.invalidWords.toDelete.forEach(w => console.log(`     - ${w}`));
    }
    
    console.log(`\n📝 Valid words needing definitions: ${cleanupReport.summary.validWordsNeedingDefinitions}`);
    if (cleanupReport.validWordsNeedingDefinitions.length > 0) {
      console.log('   Sample words:');
      cleanupReport.validWordsNeedingDefinitions.slice(0, 5).forEach(w => console.log(`     - ${w}`));
      if (cleanupReport.validWordsNeedingDefinitions.length > 5) {
        console.log(`     ... and ${cleanupReport.validWordsNeedingDefinitions.length - 5} more`);
      }
    }
    
    console.log(`\n💾 Detailed plan saved to: ${reportFilename}`);
    console.log('\n' + '='.repeat(60));
    console.log('⚠️  IMPORTANT: Review the plan above before proceeding!');
    console.log('To apply these changes, run: node scripts/apply_spelling_cleanup.js');
    console.log('='.repeat(60));
    
  } catch (error) {
    console.error('Error during cleanup analysis:', error);
  }
}

cleanupSpellingWords().catch(console.error);