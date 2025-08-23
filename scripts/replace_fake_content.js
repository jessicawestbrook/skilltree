const { createClient } = require('@supabase/supabase-js');
const Anthropic = require('@anthropic-ai/sdk');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const BATCH_SIZE = 5;
const DELAY_BETWEEN_REQUESTS = 2000;

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function isFakeDefinition(definition) {
  const fakePatterns = [
    /^Definition for /i,
    /^\[.*definition.*\]/i,
    /^placeholder/i,
    /needs a definition/i,
    /definition not available/i,
    /^\(definition\)/i
  ];
  
  return fakePatterns.some(pattern => pattern.test(definition));
}

function isFakeExample(example) {
  const fakePatterns = [
    /^The word .* is used in this context\.?$/i,
    /^\[.*example.*not available\]/i,
    /^example sentence for/i,
    /^placeholder/i,
    /needs an example/i,
    /example not available/i,
    /^\(example\)/i
  ];
  
  return fakePatterns.some(pattern => pattern.test(example));
}

async function getProperContentFromAnthropic(word) {
  try {
    const message = await anthropic.messages.create({
      model: "claude-3-haiku-20240307",
      max_tokens: 400,
      messages: [{
        role: "user",
        content: `For the spelling bee word "${word}", provide:

1. A clear, concise definition (1-2 sentences)
2. An example sentence that uses blanks (_____ or _____) where the word should go, suitable for spelling bee practice

Format your response as:
DEFINITION: [definition here]
EXAMPLE: [example sentence with blanks]

Make the definition educational and age-appropriate. The example should clearly show the word's usage context while using blanks for the actual word.`
      }]
    });
    
    const response = message.content[0].text.trim();
    
    // Parse the response
    const defMatch = response.match(/DEFINITION:\s*(.+)/);
    const exampleMatch = response.match(/EXAMPLE:\s*(.+)/);
    
    if (defMatch && exampleMatch) {
      return {
        definition: defMatch[1].trim(),
        example: exampleMatch[1].trim()
      };
    }
    
    return null;
  } catch (error) {
    console.error(`Error getting content for ${word}:`, error.message);
    return null;
  }
}

async function createBackup() {
  console.log('Creating backup of records with fake content...');
  
  const { data: fakeRecords, error } = await supabase
    .from('spelling_words')
    .select('*')
    .or('definition.ilike.%definition for%,definition.ilike.%placeholder%,example_sentence.ilike.%the word * is used in this context%,example_sentence.ilike.%example sentence for%');
    
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

async function findRecordsWithFakeContent() {
  console.log('Finding records with fake content to replace...');
  
  const { data: allRecords, error } = await supabase
    .from('spelling_words')
    .select('id, word, definition, example_sentence')
    .or('definition.ilike.%definition for%,definition.ilike.%placeholder%,example_sentence.ilike.%the word * is used in this context%,example_sentence.ilike.%example sentence for%');
    
  if (error) throw error;
  
  const recordsNeedingReplacement = [];
  
  for (const record of allRecords) {
    const hasFakeDefinition = isFakeDefinition(record.definition || '');
    const hasFakeExample = isFakeExample(record.example_sentence || '');
    
    if (hasFakeDefinition || hasFakeExample) {
      recordsNeedingReplacement.push({
        ...record,
        needsNewDefinition: hasFakeDefinition,
        needsNewExample: hasFakeExample
      });
    }
  }
  
  console.log(`Found ${recordsNeedingReplacement.length} records needing content replacement`);
  return recordsNeedingReplacement;
}

async function replaceFakeContent(recordsToReplace) {
  console.log('Replacing fake content with proper definitions and examples...');
  
  const results = {
    successful: [],
    failed: [],
    errors: []
  };
  
  for (let i = 0; i < recordsToReplace.length; i++) {
    const record = recordsToReplace[i];
    
    console.log(`Processing ${i + 1}/${recordsToReplace.length}: ${record.word}`);
    
    try {
      // Get proper content from Anthropic API
      await delay(DELAY_BETWEEN_REQUESTS);
      const properContent = await getProperContentFromAnthropic(record.word);
      
      if (properContent) {
        // Prepare update object
        const updateData = {};
        
        if (record.needsNewDefinition) {
          updateData.definition = properContent.definition;
        }
        
        if (record.needsNewExample) {
          updateData.example_sentence = properContent.example;
        }
        
        // Update the record
        const { error } = await supabase
          .from('spelling_words')
          .update(updateData)
          .eq('id', record.id);
          
        if (error) throw error;
        
        console.log(`✓ Replaced content for: ${record.word}`);
        if (record.needsNewDefinition) {
          console.log(`  New definition: ${properContent.definition}`);
        }
        if (record.needsNewExample) {
          console.log(`  New example: ${properContent.example}`);
        }
        console.log('');
        
        results.successful.push({
          word: record.word,
          oldDefinition: record.definition,
          newDefinition: record.needsNewDefinition ? properContent.definition : record.definition,
          oldExample: record.example_sentence,
          newExample: record.needsNewExample ? properContent.example : record.example_sentence,
          replacedDefinition: record.needsNewDefinition,
          replacedExample: record.needsNewExample
        });
        
      } else {
        console.log(`⚠ Could not get proper content for: ${record.word}`);
        results.failed.push({ 
          word: record.word, 
          reason: 'No content from API' 
        });
      }
      
    } catch (error) {
      console.error(`Error processing ${record.word}:`, error);
      results.errors.push({ 
        word: record.word, 
        error: error.message 
      });
    }
    
    // Rate limiting
    if ((i + 1) % BATCH_SIZE === 0) {
      console.log(`Batch ${Math.ceil((i + 1) / BATCH_SIZE)} complete, waiting...`);
      await delay(DELAY_BETWEEN_REQUESTS * 2);
    }
  }
  
  return results;
}

async function verifyReplacements() {
  console.log('\n=== VERIFICATION ===');
  
  const patterns = [
    { name: 'Definition for', query: 'definition.ilike.%definition for%' },
    { name: 'Placeholder definitions', query: 'definition.ilike.%placeholder%' },
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
}

async function main() {
  console.log('Starting replacement of fake content with proper definitions and examples...');
  console.log('This will preserve all words but replace fake content with real content.\n');
  
  try {
    // Create backup
    await createBackup();
    
    // Find records with fake content
    const recordsToReplace = await findRecordsWithFakeContent();
    
    if (recordsToReplace.length === 0) {
      console.log('✓ No fake content found to replace!');
      return;
    }
    
    // Show what will be replaced
    console.log('\n=== CONTENT TO REPLACE ===');
    const definitionReplacements = recordsToReplace.filter(r => r.needsNewDefinition).length;
    const exampleReplacements = recordsToReplace.filter(r => r.needsNewExample).length;
    
    console.log(`Words needing new definitions: ${definitionReplacements}`);
    console.log(`Words needing new examples: ${exampleReplacements}`);
    console.log(`Total records to process: ${recordsToReplace.length}`);
    
    // Show sample of what will be replaced
    console.log('\nSample records to be updated:');
    recordsToReplace.slice(0, 5).forEach((record, i) => {
      console.log(`${i + 1}. ${record.word}`);
      if (record.needsNewDefinition) {
        console.log(`   FAKE DEF: ${record.definition}`);
      }
      if (record.needsNewExample) {
        console.log(`   FAKE EX: ${record.example_sentence}`);
      }
    });
    
    // Process a limited batch first (to test)
    console.log(`\nProcessing first ${Math.min(20, recordsToReplace.length)} records...`);
    const batchToProcess = recordsToReplace.slice(0, 20);
    
    // Replace fake content
    console.log('\n=== REPLACEMENT PROCESS ===');
    const results = await replaceFakeContent(batchToProcess);
    
    console.log('\n=== RESULTS ===');
    console.log(`Successfully replaced: ${results.successful.length}`);
    console.log(`Failed: ${results.failed.length}`);
    console.log(`Errors: ${results.errors.length}`);
    
    if (results.errors.length > 0) {
      console.log('\nErrors:');
      results.errors.forEach(error => {
        console.log(`- ${error.word}: ${error.error}`);
      });
    }
    
    if (results.failed.length > 0) {
      console.log('\nFailed:');
      results.failed.forEach(fail => {
        console.log(`- ${fail.word}: ${fail.reason}`);
      });
    }
    
    // Verify replacements
    await verifyReplacements();
    
    // Save results
    const fs = require('fs');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\replacement_results_${timestamp}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify({
      summary: {
        totalToReplace: recordsToReplace.length,
        processed: batchToProcess.length,
        successful: results.successful.length,
        failed: results.failed.length,
        errors: results.errors.length
      },
      replacements: results.successful,
      failures: results.failed,
      errors: results.errors
    }, null, 2));
    
    console.log(`\nDetailed results saved to: ${resultsFile}`);
    
    if (recordsToReplace.length > 20) {
      console.log(`\nNote: ${recordsToReplace.length - 20} more records need processing.`);
      console.log('Run the script again to continue with the remaining records.');
    }
    
    console.log('\n✓ Fake content replacement completed!');
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

if (require.main === module) {
  main();
}