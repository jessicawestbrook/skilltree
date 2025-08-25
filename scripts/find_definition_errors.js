const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function findDefinitionErrors() {
  console.log('Searching for data cleaning opportunities in definitions...\n');
  
  const issues = {
    wordError: [],
    emptyDefinition: [],
    veryShortDefinition: [],
    veryLongDefinition: [],
    duplicateDefinitions: new Map(),
    specialCharacters: [],
    multipleMeanings: [],
    selfReferential: []
  };
  
  let offset = 0;
  const batchSize = 1000;
  let totalProcessed = 0;
  
  while (true) {
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition, example_sentence')
      .range(offset, offset + batchSize - 1)
      .order('id');
      
    if (error) {
      console.error('Error fetching words:', error);
      break;
    }
    
    if (!words || words.length === 0) {
      break;
    }
    
    // Process each word
    for (const wordData of words) {
      const { id, word, definition, example_sentence } = wordData;
      
      // Check for "word error" in definition
      if (definition && definition.toLowerCase().includes('word error')) {
        issues.wordError.push({ id, word, definition });
      }
      
      // Check for empty or null definitions
      if (!definition || definition.trim() === '') {
        issues.emptyDefinition.push({ id, word });
      }
      
      // Check for very short definitions (less than 10 characters)
      if (definition && definition.trim().length < 10 && definition.trim().length > 0) {
        issues.veryShortDefinition.push({ id, word, definition });
      }
      
      // Check for very long definitions (more than 500 characters)
      if (definition && definition.length > 500) {
        issues.veryLongDefinition.push({ 
          id, 
          word, 
          definitionLength: definition.length,
          definitionPreview: definition.substring(0, 100) + '...' 
        });
      }
      
      // Track duplicate definitions
      if (definition && definition.trim().length > 20) {
        const normalizedDef = definition.trim().toLowerCase();
        if (issues.duplicateDefinitions.has(normalizedDef)) {
          issues.duplicateDefinitions.get(normalizedDef).push({ id, word });
        } else {
          issues.duplicateDefinitions.set(normalizedDef, [{ id, word }]);
        }
      }
      
      // Check for unusual special characters that might indicate encoding issues
      if (definition && /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(definition)) {
        issues.specialCharacters.push({ id, word, definition });
      }
      
      // Check for definitions that start with numbers (might be multiple meanings concatenated)
      if (definition && /^\d+\./.test(definition.trim())) {
        issues.multipleMeanings.push({ id, word, definitionPreview: definition.substring(0, 100) });
      }
      
      // Check for self-referential definitions (definition contains the word itself)
      if (definition && word && definition.toLowerCase().includes(word.toLowerCase())) {
        issues.selfReferential.push({ id, word, definition });
      }
    }
    
    totalProcessed += words.length;
    if (totalProcessed % 5000 === 0) {
      console.log(`Processed ${totalProcessed} words...`);
    }
    
    offset += batchSize;
  }
  
  // Generate report
  console.log('\n========== DATA CLEANING OPPORTUNITIES REPORT ==========\n');
  
  console.log(`Total words processed: ${totalProcessed}\n`);
  
  console.log('1. CRITICAL ISSUES:');
  console.log('-------------------');
  
  if (issues.wordError.length > 0) {
    console.log(`\n📛 "Word Error" found in ${issues.wordError.length} definitions:`);
    issues.wordError.slice(0, 10).forEach(item => {
      console.log(`   - ID: ${item.id}, Word: "${item.word}"`);
      console.log(`     Definition: "${item.definition.substring(0, 100)}..."`);
    });
    if (issues.wordError.length > 10) {
      console.log(`   ... and ${issues.wordError.length - 10} more`);
    }
  }
  
  if (issues.emptyDefinition.length > 0) {
    console.log(`\n📛 Empty/null definitions: ${issues.emptyDefinition.length} words`);
    issues.emptyDefinition.slice(0, 10).forEach(item => {
      console.log(`   - ID: ${item.id}, Word: "${item.word}"`);
    });
    if (issues.emptyDefinition.length > 10) {
      console.log(`   ... and ${issues.emptyDefinition.length - 10} more`);
    }
  }
  
  console.log('\n2. QUALITY ISSUES:');
  console.log('------------------');
  
  if (issues.veryShortDefinition.length > 0) {
    console.log(`\n⚠️  Very short definitions (< 10 chars): ${issues.veryShortDefinition.length} words`);
    issues.veryShortDefinition.slice(0, 5).forEach(item => {
      console.log(`   - ID: ${item.id}, Word: "${item.word}", Definition: "${item.definition}"`);
    });
  }
  
  if (issues.veryLongDefinition.length > 0) {
    console.log(`\n⚠️  Very long definitions (> 500 chars): ${issues.veryLongDefinition.length} words`);
    issues.veryLongDefinition.slice(0, 5).forEach(item => {
      console.log(`   - ID: ${item.id}, Word: "${item.word}", Length: ${item.definitionLength} chars`);
    });
  }
  
  // Find actual duplicates (more than 1 word with same definition)
  const actualDuplicates = Array.from(issues.duplicateDefinitions.entries())
    .filter(([def, words]) => words.length > 1);
    
  if (actualDuplicates.length > 0) {
    console.log(`\n⚠️  Duplicate definitions: ${actualDuplicates.length} unique definitions used by multiple words`);
    actualDuplicates.slice(0, 5).forEach(([def, words]) => {
      console.log(`   - Definition: "${def.substring(0, 50)}..."`);
      console.log(`     Used by: ${words.map(w => w.word).join(', ')}`);
    });
  }
  
  if (issues.selfReferential.length > 0) {
    console.log(`\n⚠️  Self-referential definitions: ${issues.selfReferential.length} words`);
    console.log('   (Definitions that contain the word being defined)');
    issues.selfReferential.slice(0, 5).forEach(item => {
      console.log(`   - Word: "${item.word}", Definition: "${item.definition.substring(0, 80)}..."`);
    });
  }
  
  console.log('\n3. FORMAT ISSUES:');
  console.log('-----------------');
  
  if (issues.specialCharacters.length > 0) {
    console.log(`\n⚠️  Special/control characters found: ${issues.specialCharacters.length} definitions`);
    issues.specialCharacters.slice(0, 5).forEach(item => {
      console.log(`   - ID: ${item.id}, Word: "${item.word}"`);
    });
  }
  
  if (issues.multipleMeanings.length > 0) {
    console.log(`\n⚠️  Possible multiple meanings (starts with number): ${issues.multipleMeanings.length} definitions`);
    issues.multipleMeanings.slice(0, 5).forEach(item => {
      console.log(`   - ID: ${item.id}, Word: "${item.word}"`);
      console.log(`     Definition: "${item.definitionPreview}..."`);
    });
  }
  
  // Save detailed results to file
  const detailedReport = {
    generatedAt: new Date().toISOString(),
    totalProcessed,
    issues: {
      wordError: issues.wordError,
      emptyDefinition: issues.emptyDefinition,
      veryShortDefinition: issues.veryShortDefinition,
      veryLongDefinition: issues.veryLongDefinition,
      duplicateDefinitions: actualDuplicates.map(([def, words]) => ({
        definition: def,
        words: words
      })),
      specialCharacters: issues.specialCharacters,
      multipleMeanings: issues.multipleMeanings,
      selfReferential: issues.selfReferential
    }
  };
  
  const fs = require('fs');
  const reportPath = 'definition_errors_report.json';
  fs.writeFileSync(reportPath, JSON.stringify(detailedReport, null, 2));
  console.log(`\n📄 Detailed report saved to: ${reportPath}`);
  
  // Summary
  console.log('\n========== SUMMARY ==========');
  console.log(`Total issues found: ${
    issues.wordError.length + 
    issues.emptyDefinition.length + 
    issues.veryShortDefinition.length + 
    issues.veryLongDefinition.length + 
    actualDuplicates.length +
    issues.specialCharacters.length +
    issues.multipleMeanings.length +
    issues.selfReferential.length
  }`);
  
  console.log('\nPriority fixes:');
  console.log(`1. Fix ${issues.wordError.length} "word error" definitions`);
  console.log(`2. Add definitions for ${issues.emptyDefinition.length} words with missing definitions`);
  console.log(`3. Review ${issues.selfReferential.length} self-referential definitions`);
  console.log(`4. Expand ${issues.veryShortDefinition.length} very short definitions`);
}

findDefinitionErrors()
  .then(() => console.log('\nAnalysis complete!'))
  .catch(console.error);