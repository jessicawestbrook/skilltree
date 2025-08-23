const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

// Use service role key for admin access
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Known concatenated words to split
const concatenatedWords = [
  { original: 'accordaturacavalletti', words: ['accordatura', 'cavalletti'] },
  { original: 'billiardsobstreperous', words: ['billiards', 'obstreperous'] },
  { original: 'brucellosiswasteweir', words: ['brucellosis', 'wasteweir'] },
  { original: 'cirrhosisbangalore', words: ['cirrhosis', 'bangalore'] },
  { original: 'collegialityinclement', words: ['collegiality', 'inclement'] },
  { original: 'colloqueonychorrhexis', words: ['colloque', 'onychorrhexis'] },
  { original: 'contaminatedmadagascar', words: ['contaminated', 'madagascar'] },
  { original: 'contrivancecontumelious', words: ['contrivance', 'contumelious'] },
  { original: 'cornilycontraction', words: ['cornily', 'contraction'] },
  { original: 'daguerreotypeyakitori', words: ['daguerreotype', 'yakitori'] },
  { original: 'decumbituremultivalent', words: ['decumbiture', 'multivalent'] },
  { original: 'deficienciesincarnated', words: ['deficiencies', 'incarnated'] },
  { original: 'depredationignominious', words: ['depredation', 'ignominious'] },
  { original: 'dispositionremonstrance', words: ['disposition', 'remonstrance'] },
  // Additional concatenated words found
  { original: 'charlotteelation', words: ['charlotte', 'elation'] },
  { original: 'chastisechief', words: ['chastise', 'chief'] },
  { original: 'chastisechortle', words: ['chastise', 'chortle'] },
  { original: 'chauve-sourisadjective', words: ['chauve-souris', 'adjective'] },
  { original: 'chemistryquandary', words: ['chemistry', 'quandary'] },
  { original: 'chupacabraacadians', words: ['chupacabra', 'acadians'] },
  { original: 'cinerariumpolemic', words: ['cinerarium', 'polemic'] },
  { original: 'circuitouscircumflex', words: ['circuitous', 'circumflex'] },
  { original: 'circuitousveracity', words: ['circuitous', 'veracity'] },
  { original: 'clarinetcapillary', words: ['clarinet', 'capillary'] },
  { original: 'climateyankee', words: ['climate', 'yankee'] },
  { original: 'coaxationardoise', words: ['coaxation', 'ardoise'] },
  { original: 'cohesiveadjectives', words: ['cohesive', 'adjectives'] },
  { original: 'coiffurerepartee', words: ['coiffure', 'repartee'] },
  { original: 'colcannonnoun', words: ['colcannon', 'noun'] },
  { original: 'commissionergrande', words: ['commissioner', 'grande'] },
  { original: 'competitivelounge', words: ['competitive', 'lounge'] },
  { original: 'complacencykraken', words: ['complacency', 'kraken'] },
  { original: 'condimentsconference', words: ['condiments', 'conference'] },
  { original: 'consecrateadjective', words: ['consecrate', 'adjective'] },
  { original: 'constantbalm', words: ['constant', 'balm'] },
  { original: 'contusionconundrum', words: ['contusion', 'conundrum'] },
  { original: 'cordaunchristened', words: ['cordaun', 'christened'] }
];

async function splitConcatenatedWords() {
  console.log('=== SPLITTING CONCATENATED WORDS ===\n');
  
  let processedCount = 0;
  let newWordsAdded = 0;
  let deletedCount = 0;
  const wordsToAdd = [];
  const wordsToDelete = [];
  
  try {
    // First, get the original concatenated words from the database
    for (const item of concatenatedWords) {
      console.log(`Processing: "${item.original}"`);
      
      // Get the original word data
      const { data: originalWord, error } = await supabase
        .from('spelling_words')
        .select('*')
        .eq('word', item.original)
        .single();
      
      if (error || !originalWord) {
        console.log(`  ⚠️ Word not found in database: "${item.original}"`);
        continue;
      }
      
      console.log(`  Found in database with source difficulty: ${originalWord.source_difficulty}`);
      wordsToDelete.push(item.original);
      
      // Check if the split words already exist
      for (const newWord of item.words) {
        const { data: existingWord } = await supabase
          .from('spelling_words')
          .select('word')
          .eq('word', newWord)
          .single();
        
        if (!existingWord) {
          console.log(`  → Will add: "${newWord}"`);
          wordsToAdd.push({
            word: newWord,
            source_difficulty: originalWord.source_difficulty,
            // Leave other fields null - they'll be populated by the Claude script
            definition: null,
            example_sentence: null,
            pronunciation_guide: null,
            etymology: null
          });
        } else {
          console.log(`  ↪ Already exists: "${newWord}"`);
        }
      }
      
      processedCount++;
    }
    
    console.log(`\n📊 ANALYSIS COMPLETE:`);
    console.log(`  Concatenated words found: ${processedCount}`);
    console.log(`  New words to add: ${wordsToAdd.length}`);
    console.log(`  Words to delete: ${wordsToDelete.length}`);
    
    if (wordsToAdd.length === 0 && wordsToDelete.length === 0) {
      console.log('\n✅ No changes needed!');
      return;
    }
    
    // Ask for confirmation
    console.log('\n📋 PLANNED CHANGES:');
    console.log('Words to add:', wordsToAdd.map(w => w.word).join(', '));
    console.log('Words to delete:', wordsToDelete.join(', '));
    
    // Insert new words
    if (wordsToAdd.length > 0) {
      console.log(`\n➕ Adding ${wordsToAdd.length} new words...`);
      const { data: inserted, error: insertError } = await supabase
        .from('spelling_words')
        .insert(wordsToAdd)
        .select();
      
      if (insertError) {
        console.error('❌ Error inserting words:', insertError);
      } else {
        console.log(`✅ Successfully added ${inserted.length} words`);
        newWordsAdded = inserted.length;
      }
    }
    
    // Delete concatenated words
    if (wordsToDelete.length > 0) {
      console.log(`\n🗑️ Deleting ${wordsToDelete.length} concatenated words...`);
      const { error: deleteError } = await supabase
        .from('spelling_words')
        .delete()
        .in('word', wordsToDelete);
      
      if (deleteError) {
        console.error('❌ Error deleting words:', deleteError);
      } else {
        console.log(`✅ Successfully deleted ${wordsToDelete.length} words`);
        deletedCount = wordsToDelete.length;
      }
    }
    
    console.log('\n=== FINAL SUMMARY ===');
    console.log(`✅ New words added: ${newWordsAdded}`);
    console.log(`✅ Concatenated words deleted: ${deletedCount}`);
    console.log(`\nThe new words will need content population. Run the populate_legitimate_words_claude_improved.js script to add definitions, pronunciations, etc.`);
    
  } catch (error) {
    console.error('Error:', error);
  }
}

// Run the script
splitConcatenatedWords().catch(console.error);