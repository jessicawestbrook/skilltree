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
  const backupFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\fake_content_backup_${timestamp}.json`;
  
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
      // Set definition to null so it can be filled in later with proper content
      const { error: updateError } = await supabase
        .from('spelling_words')
        .update({ definition: null })
        .eq('id', record.id);
        
      if (updateError) throw updateError;
      
      console.log(`✓ Cleared fake definition for: ${record.word}`);
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
      // Create a basic template example sentence with blanks
      const newExample = `The word _____ can be used in various contexts.`;
      
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

async function verifyCleanup() {
  console.log('\n=== VERIFICATION ===');
  
  const patterns = [
    { name: 'Definition for', query: 'definition.ilike.%definition for%' },
    { name: 'Context examples', query: 'example_sentence.ilike.%the word * is used in this context%' },
    { name: 'Example sentence for', query: 'example_sentence.ilike.%example sentence for%' }
  ];
  
  for (const pattern of patterns) {
    const { count } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .or(pattern.query);
      
    console.log(`${pattern.name}: ${count} records remaining`);
  }
  
  // Check how many records now have null definitions
  const { count: nullDefs } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('definition', null);
    
  console.log(`Records with null definitions (need proper content): ${nullDefs}`);
}

async function main() {
  console.log('Starting manual replacement of fake content...');
  console.log('This will replace fake patterns with proper placeholders or null values.\n');
  
  try {
    // Create backup
    await createBackup();
    
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
    const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\manual_replacement_results_${timestamp}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify({
      summary: {
        definitionsReplaced: defResults.updated,
        examplesReplaced: exampleResults.updated,
        totalErrors: defResults.errors.length + exampleResults.errors.length
      },
      definitionErrors: defResults.errors,
      exampleErrors: exampleResults.errors
    }, null, 2));
    
    console.log(`\nResults saved to: ${resultsFile}`);
    console.log('\n✓ Manual fake content replacement completed!');
    console.log('\nNote: Records with null definitions will need proper content added later.');
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

if (require.main === module) {
  main();
}