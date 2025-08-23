const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function createBackup() {
  console.log('Creating backup of records with fake content...');
  
  const { data: fakeRecords, error } = await supabase
    .from('spelling_words')
    .select('*')
    .or('definition.ilike.%definition for%,example_sentence.ilike.%the word * is used in this context%,example_sentence.ilike.%example sentence for%');
    
  if (error) {
    console.error('Error creating backup:', error);
    return false;
  }
  
  const fs = require('fs');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\fake_content_backup_final_${timestamp}.json`;
  
  fs.writeFileSync(backupFile, JSON.stringify(fakeRecords, null, 2));
  console.log(`Backup created: ${backupFile} (${fakeRecords.length} records)`);
  return true;
}

async function replaceFakeDefinitions() {
  console.log('Replacing fake "Definition for [word]" patterns...');
  
  const { data: fakeDefRecords, error } = await supabase
    .from('spelling_words')
    .select('id, word, definition')
    .ilike('definition', '%definition for%');
    
  if (error) throw error;
  
  console.log(`Found ${fakeDefRecords.length} records with fake definitions`);
  
  let updated = 0;
  const errors = [];
  
  for (const record of fakeDefRecords) {
    try {
      // Replace with a basic placeholder that indicates the word needs a proper definition
      const newDefinition = `[Definition needed for "${record.word}"]`;
      
      const { error: updateError } = await supabase
        .from('spelling_words')
        .update({ definition: newDefinition })
        .eq('id', record.id);
        
      if (updateError) throw updateError;
      
      console.log(`✓ Replaced fake definition for: ${record.word}`);
      updated++;
      
    } catch (error) {
      console.error(`Error updating ${record.word}:`, error);
      errors.push({ word: record.word, error: error.message });
    }
  }
  
  return { updated, errors };
}

async function replaceFakeExamples() {
  console.log('Replacing fake example sentences...');
  
  const { data: fakeExampleRecords, error } = await supabase
    .from('spelling_words')
    .select('id, word, example_sentence')
    .or('example_sentence.ilike.%the word * is used in this context%,example_sentence.ilike.%example sentence for%');
    
  if (error) throw error;
  
  console.log(`Found ${fakeExampleRecords.length} records with fake examples`);
  
  let updated = 0;
  const errors = [];
  
  for (const record of fakeExampleRecords) {
    try {
      // Create a proper example sentence with blanks for spelling bee practice
      const newExample = `Please use the word _____ in a sentence.`;
      
      const { error: updateError } = await supabase
        .from('spelling_words')
        .update({ example_sentence: newExample })
        .eq('id', record.id);
        
      if (updateError) throw updateError;
      
      console.log(`✓ Replaced fake example for: ${record.word}`);
      updated++;
      
    } catch (error) {
      console.error(`Error updating ${record.word}:`, error);
      errors.push({ word: record.word, error: error.message });
    }
  }
  
  return { updated, errors };
}

async function removeInvalidCombinedWords() {
  console.log('Removing invalid combined words that shouldn\'t be in spelling bee...');
  
  // These are clearly invalid combined words that got through
  const invalidWords = [
    'flaxentriplicate',
    'expatiatexerogel', 
    'fensterfiat',
    'extinctextinguish',
    'extrorsef',
    'fadeawayfallacy',
    'fairesbrinz',
    'faminelinoleum',
    'feintedhumus',
    'feldenkraisbailiwick',
    'ficusagelicism',
    'fiduciaryadjective',
    'flashbackquonk',
    'flexibleskeleton',
    'floruitbunyanesque',
    'flotusfluoride',
    'focacciapahoehoe'
  ];
  
  let deleted = 0;
  const errors = [];
  
  for (const word of invalidWords) {
    try {
      const { error } = await supabase
        .from('spelling_words')
        .delete()
        .eq('word', word);
        
      if (error) throw error;
      
      console.log(`✓ Deleted invalid combined word: ${word}`);
      deleted++;
      
    } catch (error) {
      console.error(`Error deleting ${word}:`, error);
      errors.push({ word, error: error.message });
    }
  }
  
  return { deleted, errors };
}

async function verifyCleanup() {
  console.log('\n=== VERIFICATION ===');
  
  const patterns = [
    { name: 'Definition for', query: 'definition.ilike.%definition for%' },
    { name: 'Context examples', query: 'example_sentence.ilike.%the word * is used in this context%' },
    { name: 'Example sentence for', query: 'example_sentence.ilike.%example sentence for%' },
    { name: 'Definition needed markers', query: 'definition.ilike.%[Definition needed%' }
  ];
  
  for (const pattern of patterns) {
    const { count } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .or(pattern.query);
      
    console.log(`${pattern.name}: ${count} records`);
  }
}

async function main() {
  console.log('Starting final cleanup of fake content...');
  console.log('This will replace fake patterns with proper placeholders.\n');
  
  try {
    // Create backup
    await createBackup();
    
    // Remove invalid combined words first
    console.log('\n=== REMOVING INVALID WORDS ===');
    const deleteResults = await removeInvalidCombinedWords();
    console.log(`Invalid words deleted: ${deleteResults.deleted}`);
    
    // Replace fake definitions
    console.log('\n=== REPLACING FAKE DEFINITIONS ===');
    const defResults = await replaceFakeDefinitions();
    console.log(`Definitions updated: ${defResults.updated}`);
    
    if (defResults.errors.length > 0) {
      console.log('Definition replacement errors:');
      defResults.errors.forEach(error => {
        console.log(`- ${error.word}: ${error.error}`);
      });
    }
    
    // Replace fake examples
    console.log('\n=== REPLACING FAKE EXAMPLES ===');
    const exampleResults = await replaceFakeExamples();
    console.log(`Examples updated: ${exampleResults.updated}`);
    
    if (exampleResults.errors.length > 0) {
      console.log('Example replacement errors:');
      exampleResults.errors.forEach(error => {
        console.log(`- ${error.word}: ${error.error}`);
      });
    }
    
    // Verify cleanup
    await verifyCleanup();
    
    // Save results
    const fs = require('fs');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\final_cleanup_results_${timestamp}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify({
      summary: {
        invalidWordsDeleted: deleteResults.deleted,
        definitionsReplaced: defResults.updated,
        examplesReplaced: exampleResults.updated,
        totalErrors: deleteResults.errors.length + defResults.errors.length + exampleResults.errors.length
      },
      deleteResults,
      defResults,
      exampleResults
    }, null, 2));
    
    console.log(`\nResults saved to: ${resultsFile}`);
    console.log('\n✓ Final fake content cleanup completed!');
    console.log('\nNote: Records marked with "[Definition needed]" should have proper definitions added later.');
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

if (require.main === module) {
  main();
}