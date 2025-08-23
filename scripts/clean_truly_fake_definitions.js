const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

function isTrulyFakeDefinition(definition) {
  const fakePatterns = [
    /^Definition for /i,
    /^This is a definition/i,
    /^\[.*DEFINITION.*\]/i,
    /^PLACEHOLDER/i,
    /needs a definition/i,
    /definition not available/i,
    /^Definition of /i,
    /^\(definition\)/i
  ];
  
  return fakePatterns.some(pattern => pattern.test(definition));
}

function isTrulyFakeExample(example) {
  const fakePatterns = [
    /^The word .* is used in this context\.?$/i,
    /^Example sentence for /i,
    /^\[.*EXAMPLE.*\]/i,
    /^PLACEHOLDER/i,
    /needs an example/i,
    /example not available/i,
    /^\(example\)/i,
    /^This is an example/i
  ];
  
  return fakePatterns.some(pattern => pattern.test(example));
}

async function createBackup() {
  console.log('Creating backup of truly fake records...');
  
  const { data: fakeRecords, error } = await supabase
    .from('spelling_words')
    .select('*')
    .or('definition.ilike.%definition for%,definition.ilike.%placeholder%,definition.ilike.%needs a definition%,example_sentence.ilike.%the word * is used in this context%,example_sentence.ilike.%example sentence for%,example_sentence.ilike.%placeholder%');
    
  if (error) {
    console.error('Error creating backup:', error);
    return false;
  }
  
  const fs = require('fs');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\truly_fake_backup_${timestamp}.json`;
  
  fs.writeFileSync(backupFile, JSON.stringify(fakeRecords, null, 2));
  console.log(`Backup created: ${backupFile} (${fakeRecords.length} records)`);
  return true;
}

async function identifyTrulyFakeRecords() {
  console.log('Identifying truly fake/placeholder records...');
  
  const { data: allRecords, error } = await supabase
    .from('spelling_words')
    .select('id, word, definition, example_sentence');
    
  if (error) throw error;
  
  const trulyFake = [];
  
  for (const record of allRecords) {
    const hasFakeDefinition = isTrulyFakeDefinition(record.definition || '');
    const hasFakeExample = isTrulyFakeExample(record.example_sentence || '');
    
    if (hasFakeDefinition || hasFakeExample) {
      trulyFake.push({
        ...record,
        issues: {
          fakeDefinition: hasFakeDefinition,
          fakeExample: hasFakeExample
        }
      });
    }
  }
  
  console.log(`Found ${trulyFake.length} truly fake records out of ${allRecords.length} total`);
  return trulyFake;
}

async function showSampleFakeRecords(fakeRecords) {
  console.log('\n=== SAMPLE FAKE RECORDS ===');
  
  const samples = fakeRecords.slice(0, 10);
  samples.forEach((record, i) => {
    console.log(`${i + 1}. ${record.word}`);
    if (record.issues.fakeDefinition) {
      console.log(`   FAKE DEFINITION: ${record.definition}`);
    }
    if (record.issues.fakeExample) {
      console.log(`   FAKE EXAMPLE: ${record.example_sentence}`);
    }
    console.log('');
  });
}

async function cleanupFakeRecords(fakeRecords) {
  console.log('Cleaning up fake records...');
  
  const results = {
    updated: 0,
    deleted: 0,
    errors: []
  };
  
  for (const record of fakeRecords) {
    try {
      if (record.issues.fakeDefinition && record.issues.fakeExample) {
        // Both definition and example are fake - delete the record
        const { error } = await supabase
          .from('spelling_words')
          .delete()
          .eq('id', record.id);
          
        if (error) throw error;
        
        console.log(`✓ Deleted completely fake record: ${record.word}`);
        results.deleted++;
        
      } else if (record.issues.fakeDefinition) {
        // Only definition is fake - set to null
        const { error } = await supabase
          .from('spelling_words')
          .update({ definition: null })
          .eq('id', record.id);
          
        if (error) throw error;
        
        console.log(`✓ Cleared fake definition for: ${record.word}`);
        results.updated++;
        
      } else if (record.issues.fakeExample) {
        // Only example is fake - set to null
        const { error } = await supabase
          .from('spelling_words')
          .update({ example_sentence: null })
          .eq('id', record.id);
          
        if (error) throw error;
        
        console.log(`✓ Cleared fake example for: ${record.word}`);
        results.updated++;
      }
      
    } catch (error) {
      console.error(`Error processing ${record.word}:`, error);
      results.errors.push({ word: record.word, error: error.message });
    }
  }
  
  return results;
}

async function verifyCleanup() {
  console.log('\n=== VERIFICATION ===');
  
  const patterns = [
    { name: 'Definition for', query: 'definition.ilike.%definition for%' },
    { name: 'Placeholder definitions', query: 'definition.ilike.%placeholder%' },
    { name: 'Used in context examples', query: 'example_sentence.ilike.%the word * is used in this context%' },
    { name: 'Example sentence for', query: 'example_sentence.ilike.%example sentence for%' }
  ];
  
  for (const pattern of patterns) {
    const { count } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .or(pattern.query);
      
    console.log(`${pattern.name}: ${count} records remaining`);
  }
}

async function main() {
  console.log('Starting cleanup of truly fake definitions and examples...');
  console.log('NOTE: Blanks (____) in example sentences are legitimate for spelling bee practice.\n');
  
  try {
    // Create backup
    await createBackup();
    
    // Identify truly fake records (not just those with blanks)
    const fakeRecords = await identifyTrulyFakeRecords();
    
    if (fakeRecords.length === 0) {
      console.log('✓ No truly fake records found!');
      return;
    }
    
    // Show samples
    await showSampleFakeRecords(fakeRecords);
    
    // Show issue breakdown
    console.log('=== ISSUE BREAKDOWN ===');
    const issueTypes = {
      fakeDefinition: 0,
      fakeExample: 0,
      both: 0
    };
    
    fakeRecords.forEach(record => {
      if (record.issues.fakeDefinition && record.issues.fakeExample) {
        issueTypes.both++;
      } else if (record.issues.fakeDefinition) {
        issueTypes.fakeDefinition++;
      } else if (record.issues.fakeExample) {
        issueTypes.fakeExample++;
      }
    });
    
    console.log(`Records with fake definitions only: ${issueTypes.fakeDefinition}`);
    console.log(`Records with fake examples only: ${issueTypes.fakeExample}`);
    console.log(`Records with both fake: ${issueTypes.both}`);
    console.log(`Total fake records: ${fakeRecords.length}`);
    
    // Clean up the fake records
    console.log('\n=== CLEANUP ===');
    const results = await cleanupFakeRecords(fakeRecords);
    
    console.log('\n=== RESULTS ===');
    console.log(`Records updated: ${results.updated}`);
    console.log(`Records deleted: ${results.deleted}`);
    console.log(`Errors: ${results.errors.length}`);
    
    if (results.errors.length > 0) {
      console.log('\\nErrors:');
      results.errors.forEach(error => {
        console.log(`- ${error.word}: ${error.error}`);
      });
    }
    
    // Verify cleanup
    await verifyCleanup();
    
    // Save results
    const fs = require('fs');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\fake_cleanup_results_${timestamp}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify({
      summary: {
        totalFakeRecords: fakeRecords.length,
        issueTypes,
        results
      },
      processedRecords: fakeRecords.map(r => ({
        word: r.word,
        issues: r.issues,
        definition: r.definition,
        example: r.example_sentence
      }))
    }, null, 2));
    
    console.log(`\\nDetailed results saved to: ${resultsFile}`);
    console.log('\\n✓ Cleanup of truly fake content completed!');
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

if (require.main === module) {
  main();
}