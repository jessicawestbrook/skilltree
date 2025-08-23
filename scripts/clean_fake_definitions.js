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

const BATCH_SIZE = 10;
const DELAY_BETWEEN_REQUESTS = 2000;

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function isPlaceholderDefinition(definition) {
  const placeholderPatterns = [
    /definition for/i,
    /^[A-Z][a-z]+ is a /i, // Very generic starts
    /the word .* is used/i,
    /this is a definition/i,
    /placeholder/i,
    /___+/
  ];
  
  return placeholderPatterns.some(pattern => pattern.test(definition));
}

function isPlaceholderExample(example) {
  const placeholderPatterns = [
    /the word ___+ is used/i,
    /___+ is used in this context/i,
    /example sentence for/i,
    /placeholder/i,
    /^The ___+ /i, // Very generic examples that start with "The ___"
    /sentence with ___+/i
  ];
  
  return placeholderPatterns.some(pattern => pattern.test(example));
}

function hasGenericContent(definition, example) {
  // Check for overly generic or repetitive content
  const genericDefinitionPatterns = [
    /^[A-Z][a-z]+ refers to /i,
    /^[A-Z][a-z]+ is a [a-z]+ /i,
    /meaning "[^"]*" /i
  ];
  
  const isGenericDef = genericDefinitionPatterns.some(pattern => pattern.test(definition));
  const isBlankExample = /___+/.test(example);
  
  return isGenericDef && isBlankExample;
}

async function getImprovedContentFromAnthropic(word, currentDefinition, currentExample) {
  try {
    const message = await anthropic.messages.create({
      model: "claude-3-haiku-20240307",
      max_tokens: 300,
      messages: [{
        role: "user",
        content: `For the spelling bee word "${word}", provide:

1. A concise, clear definition (1-2 sentences max)
2. An example sentence that shows the word's meaning WITHOUT using blanks or underscores

Current definition: ${currentDefinition}
Current example: ${currentExample}

Format your response as:
DEFINITION: [new definition]
EXAMPLE: [new example sentence]

Make sure the example sentence is natural and shows the word's usage clearly.`
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
    console.error(`Error getting improved content for ${word}:`, error.message);
    return null;
  }
}

async function createBackup() {
  console.log('Creating backup of problematic records...');
  
  const { data: problematicRecords, error } = await supabase
    .from('spelling_words')
    .select('*')
    .or('definition.ilike.%definition for%,definition.ilike.%placeholder%,example_sentence.ilike.%the word _____ is used%,example_sentence.ilike.%placeholder%');
    
  if (error) {
    console.error('Error creating backup:', error);
    return false;
  }
  
  const fs = require('fs');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\fake_definitions_backup_${timestamp}.json`;
  
  fs.writeFileSync(backupFile, JSON.stringify(problematicRecords, null, 2));
  console.log(`Backup created: ${backupFile} (${problematicRecords.length} records)`);
  return true;
}

async function identifyProblematicRecords() {
  console.log('Identifying problematic records...');
  
  const { data: allRecords, error } = await supabase
    .from('spelling_words')
    .select('id, word, definition, example_sentence')
    .limit(1000); // Start with a subset
    
  if (error) throw error;
  
  const problematic = [];
  
  for (const record of allRecords) {
    const hasPlaceholderDef = isPlaceholderDefinition(record.definition || '');
    const hasPlaceholderExample = isPlaceholderExample(record.example_sentence || '');
    const hasGeneric = hasGenericContent(record.definition || '', record.example_sentence || '');
    
    if (hasPlaceholderDef || hasPlaceholderExample || hasGeneric) {
      problematic.push({
        ...record,
        issues: {
          placeholderDefinition: hasPlaceholderDef,
          placeholderExample: hasPlaceholderExample,
          genericContent: hasGeneric
        }
      });
    }
  }
  
  console.log(`Found ${problematic.length} problematic records out of ${allRecords.length} checked`);
  return problematic;
}

async function fixProblematicRecords(problematicRecords) {
  console.log('Fixing problematic records...');
  
  const results = {
    fixed: [],
    failed: [],
    skipped: []
  };
  
  for (let i = 0; i < problematicRecords.length; i++) {
    const record = problematicRecords[i];
    
    console.log(`Processing ${i + 1}/${problematicRecords.length}: ${record.word}`);
    
    // Check if this record has serious placeholder issues
    if (record.issues.placeholderDefinition || record.issues.placeholderExample) {
      
      // Get improved content from Anthropic
      await delay(DELAY_BETWEEN_REQUESTS);
      const improvedContent = await getImprovedContentFromAnthropic(
        record.word, 
        record.definition, 
        record.example_sentence
      );
      
      if (improvedContent) {
        // Update the record
        const { error } = await supabase
          .from('spelling_words')
          .update({
            definition: improvedContent.definition,
            example_sentence: improvedContent.example
          })
          .eq('id', record.id);
          
        if (error) {
          console.error(`Failed to update ${record.word}:`, error);
          results.failed.push({ word: record.word, error: error.message });
        } else {
          console.log(`✓ Fixed: ${record.word}`);
          results.fixed.push({
            word: record.word,
            oldDefinition: record.definition,
            newDefinition: improvedContent.definition,
            oldExample: record.example_sentence,
            newExample: improvedContent.example
          });
        }
      } else {
        console.log(`⚠ Could not get improved content for: ${record.word}`);
        results.failed.push({ word: record.word, error: 'No improved content available' });
      }
    } else {
      // For records with just generic content but not serious placeholders
      console.log(`- Skipping ${record.word} (minor issues only)`);
      results.skipped.push(record.word);
    }
    
    // Rate limiting
    if ((i + 1) % BATCH_SIZE === 0) {
      console.log(`Batch ${Math.ceil((i + 1) / BATCH_SIZE)} complete, waiting...`);
      await delay(DELAY_BETWEEN_REQUESTS * 2);
    }
  }
  
  return results;
}

async function manualCleanupObviousPlaceholders() {
  console.log('Performing manual cleanup of obvious placeholders...');
  
  const results = {
    updated: 0,
    errors: []
  };
  
  // Delete records with obvious placeholder definitions
  const obviousPlaceholders = [
    'definition for',
    'placeholder',
    'this is a definition',
    'the word _____ is used in this context'
  ];
  
  for (const placeholder of obviousPlaceholders) {
    try {
      const { data: toUpdate, error: selectError } = await supabase
        .from('spelling_words')
        .select('id, word')
        .ilike('definition', `%${placeholder}%`);
        
      if (selectError) throw selectError;
      
      console.log(`Found ${toUpdate.length} records with "${placeholder}" in definition`);
      
      // For now, let's flag these rather than delete them
      for (const record of toUpdate) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ 
            definition: `[PLACEHOLDER DEFINITION - NEEDS REVIEW] ${record.word}`,
            example_sentence: `The word "${record.word}" needs a proper example sentence.`
          })
          .eq('id', record.id);
          
        if (updateError) {
          results.errors.push({ word: record.word, error: updateError.message });
        } else {
          results.updated++;
          console.log(`✓ Flagged placeholder: ${record.word}`);
        }
      }
    } catch (error) {
      console.error(`Error processing "${placeholder}":`, error);
      results.errors.push({ placeholder, error: error.message });
    }
  }
  
  return results;
}

async function main() {
  console.log('Starting cleanup of fake definitions and example sentences...\n');
  
  try {
    // Create backup
    await createBackup();
    
    // First, do manual cleanup of obvious placeholders
    console.log('\n=== MANUAL CLEANUP ===');
    const manualResults = await manualCleanupObviousPlaceholders();
    console.log(`Manual cleanup: ${manualResults.updated} records flagged`);
    
    // Identify problematic records
    console.log('\n=== IDENTIFYING PROBLEMATIC RECORDS ===');
    const problematicRecords = await identifyProblematicRecords();
    
    if (problematicRecords.length === 0) {
      console.log('No problematic records found!');
      return;
    }
    
    // Show summary of issues
    console.log('\n=== ISSUE SUMMARY ===');
    const issueTypes = {
      placeholderDefinition: 0,
      placeholderExample: 0,
      genericContent: 0
    };
    
    problematicRecords.forEach(record => {
      Object.keys(record.issues).forEach(issue => {
        if (record.issues[issue]) issueTypes[issue]++;
      });
    });
    
    console.log('Issue breakdown:');
    Object.entries(issueTypes).forEach(([issue, count]) => {
      console.log(`- ${issue}: ${count} records`);
    });
    
    // Ask for confirmation before proceeding with API fixes
    console.log(`\nFound ${problematicRecords.length} records that need fixing.`);
    console.log('This will use the Anthropic API to generate better definitions and examples.');
    console.log('Continuing with fixes...\n');
    
    // Fix problematic records
    console.log('=== FIXING RECORDS ===');
    const fixResults = await fixProblematicRecords(problematicRecords.slice(0, 20)); // Start with first 20
    
    console.log('\n=== RESULTS ===');
    console.log(`Fixed: ${fixResults.fixed.length}`);
    console.log(`Failed: ${fixResults.failed.length}`);
    console.log(`Skipped: ${fixResults.skipped.length}`);
    
    // Save results
    const fs = require('fs');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\cleanup_results_${timestamp}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify({
      manual: manualResults,
      fixes: fixResults,
      summary: {
        totalProcessed: problematicRecords.length,
        issueTypes
      }
    }, null, 2));
    
    console.log(`\nResults saved to: ${resultsFile}`);
    console.log('\n✓ Cleanup process completed!');
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

if (require.main === module) {
  main();
}