import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';
import nlp from 'compromise';
import fetch from 'node-fetch';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: join(__dirname, '..', '.env.local') });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Get part of speech using compromise NLP
function getPartOfSpeech(word) {
  const doc = nlp(word);
  
  // Check for different parts of speech
  if (doc.has('#Noun')) return 'noun';
  if (doc.has('#Verb')) return 'verb';
  if (doc.has('#Adjective')) return 'adjective';
  if (doc.has('#Adverb')) return 'adverb';
  if (doc.has('#Pronoun')) return 'pronoun';
  if (doc.has('#Preposition')) return 'preposition';
  if (doc.has('#Conjunction')) return 'conjunction';
  if (doc.has('#Interjection')) return 'interjection';
  if (doc.has('#Determiner')) return 'determiner';
  
  // Try to get more specific tags
  const tags = doc.json()[0]?.terms?.[0]?.tags || [];
  
  // Map compromise tags to our categories
  if (tags.includes('Noun') || tags.includes('Singular') || tags.includes('Plural')) return 'noun';
  if (tags.includes('Verb') || tags.includes('PastTense') || tags.includes('PresentTense') || 
      tags.includes('Gerund') || tags.includes('Infinitive')) return 'verb';
  if (tags.includes('Adjective') || tags.includes('Comparable')) return 'adjective';
  if (tags.includes('Adverb')) return 'adverb';
  if (tags.includes('Pronoun') || tags.includes('Possessive')) return 'pronoun';
  if (tags.includes('Preposition')) return 'preposition';
  if (tags.includes('Conjunction')) return 'conjunction';
  if (tags.includes('Interjection')) return 'interjection';
  if (tags.includes('Determiner') || tags.includes('Article')) return 'determiner';
  
  // Default to noun if unknown
  return 'noun';
}

// Get definition using Free Dictionary API (no key required)
async function getDefinition(word) {
  try {
    const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
    if (!response.ok) return null;
    
    const data = await response.json();
    if (!data || !data[0]) return null;
    
    // Get the first definition from the first meaning
    const firstMeaning = data[0].meanings?.[0];
    if (!firstMeaning) return null;
    
    const definition = firstMeaning.definitions?.[0]?.definition;
    return definition || null;
  } catch (error) {
    return null;
  }
}

function getPartsOfSpeechBatch(words) {
  return words.map(w => {
    // Use compromise to determine part of speech
    const pos = getPartOfSpeech(w.word);
    
    return {
      ...w,
      part_of_speech: pos
    };
  });
}

async function assignPartsOfSpeechWithNLP() {
  console.log('=== ASSIGNING PARTS OF SPEECH USING NLP ===\n');
  
  // Fetch words missing parts of speech
  let allWords = [];
  let offset = 0;
  const fetchBatchSize = 1000;
  
  console.log('Fetching words missing parts of speech...');
  
  while (true) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition')
      .or('part_of_speech.is.null,part_of_speech.eq.')
      .range(offset, offset + fetchBatchSize - 1);
    
    if (error) {
      console.error('Error fetching words:', error);
      break;
    }
    
    if (!batch || batch.length === 0) break;
    
    allWords = allWords.concat(batch);
    console.log(`  Fetched ${allWords.length} words...`);
    
    if (batch.length < fetchBatchSize) break;
    offset += fetchBatchSize;
  }
  
  console.log(`\nTotal words to process: ${allWords.length}\n`);
  
  if (allWords.length === 0) {
    console.log('No words need processing!');
    return;
  }
  
  // Process in batches for better performance
  const processBatchSize = 100; // Process 100 words at a time (no API limits with local library)
  const results = [];
  
  console.log(`Processing ${allWords.length} words in batches of ${processBatchSize}...\n`);
  
  for (let i = 0; i < allWords.length; i += processBatchSize) {
    const batch = allWords.slice(i, i + processBatchSize);
    const batchNum = Math.floor(i / processBatchSize) + 1;
    const totalBatches = Math.ceil(allWords.length / processBatchSize);
    
    process.stdout.write(`Processing batch ${batchNum}/${totalBatches}... `);
    
    const batchResults = getPartsOfSpeechBatch(batch);
    results.push(...batchResults);
    
    console.log('✓');
    
    // Show some examples from first few batches
    if (batchNum <= 3) {
      batchResults.slice(0, 3).forEach(r => {
        console.log(`    ${r.word} → ${r.part_of_speech}`);
      });
    }
    
    // Small delay to prevent overwhelming the system
    if (i + processBatchSize < allWords.length) {
      await new Promise(resolve => setTimeout(resolve, 100)); // 100ms delay
    }
  }
  
  // Save results to file
  const outputPath = join(__dirname, 'nlp_parts_of_speech.json');
  fs.writeFileSync(outputPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    totalWords: results.length,
    results: results
  }, null, 2));
  
  console.log(`\n✓ Saved NLP results to: ${outputPath}`);
  
  // Apply to database
  console.log('\nApplying to database...\n');
  
  const updateBatchSize = 100;
  let successCount = 0;
  let errorCount = 0;
  
  for (let i = 0; i < results.length; i += updateBatchSize) {
    const batch = results.slice(i, i + updateBatchSize);
    const batchNum = Math.floor(i / updateBatchSize) + 1;
    const totalBatches = Math.ceil(results.length / updateBatchSize);
    
    process.stdout.write(`Updating batch ${batchNum}/${totalBatches}: `);
    
    const promises = batch.map(async (item) => {
      const { error } = await supabase
        .from('spelling_words')
        .update({ part_of_speech: item.part_of_speech })
        .eq('id', item.id);
      
      return !error;
    });
    
    const updateResults = await Promise.all(promises);
    const batchSuccess = updateResults.filter(r => r).length;
    const batchErrors = updateResults.filter(r => !r).length;
    
    successCount += batchSuccess;
    errorCount += batchErrors;
    
    console.log(`✓ ${batchSuccess} updated, ${batchErrors} errors`);
    
    // Small delay between update batches
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // Final summary
  console.log('\n--- Summary ---');
  console.log(`Total words processed: ${results.length}`);
  console.log(`Successfully updated: ${successCount}`);
  console.log(`Errors: ${errorCount}`);
  
  // Verify coverage
  const { count: stillMissing } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .or('part_of_speech.is.null,part_of_speech.eq.');
  
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`\nWords still missing part_of_speech: ${stillMissing}`);
  console.log(`Total words: ${totalCount}`);
  console.log(`Coverage: ${(((totalCount - stillMissing) / totalCount) * 100).toFixed(1)}%`);
  
  if (stillMissing === 0) {
    console.log('\n✅ All words now have parts of speech assigned!');
  }
}

// Function to add definitions to words that don't have them
async function addMissingDefinitions() {
  console.log('\n=== ADDING MISSING DEFINITIONS ===\n');
  
  // Fetch words without definitions
  const { data: wordsWithoutDef, error } = await supabase
    .from('spelling_words')
    .select('id, word')
    .or('definition.is.null,definition.eq.')
    .limit(100); // Start with 100 to test
  
  if (error) {
    console.error('Error fetching words without definitions:', error);
    return;
  }
  
  console.log(`Found ${wordsWithoutDef.length} words without definitions\n`);
  
  let successCount = 0;
  let failCount = 0;
  
  for (const item of wordsWithoutDef) {
    process.stdout.write(`Getting definition for "${item.word}"... `);
    
    const definition = await getDefinition(item.word);
    
    if (definition) {
      const { error: updateError } = await supabase
        .from('spelling_words')
        .update({ definition })
        .eq('id', item.id);
      
      if (!updateError) {
        console.log('✓');
        successCount++;
      } else {
        console.log('✗ (update failed)');
        failCount++;
      }
    } else {
      console.log('✗ (no definition found)');
      failCount++;
    }
    
    // Rate limit for API calls (about 60 requests per minute)
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  console.log(`\n--- Definition Summary ---`);
  console.log(`Successfully added: ${successCount}`);
  console.log(`Failed: ${failCount}`);
}

// Check if we should run in test mode
const testMode = process.argv[2] === 'test';
const definitionsMode = process.argv[2] === 'definitions';

if (testMode) {
  // Test mode - just process 5 words
  console.log('=== TEST MODE - Processing 5 words ===\n');
  
  const testWords = [
    { id: '1', word: 'run', definition: 'To move quickly' },
    { id: '2', word: 'beautiful', definition: 'Pleasing to look at' },
    { id: '3', word: 'quickly', definition: 'In a fast manner' },
    { id: '4', word: 'happiness', definition: 'The state of being happy' },
    { id: '5', word: 'and', definition: 'A conjunction' }
  ];
  
  const results = getPartsOfSpeechBatch(testWords);
  console.log('Test results:');
  results.forEach(r => {
    console.log(`  ${r.word} → ${r.part_of_speech}`);
  });
  
  // Test definition fetching
  console.log('\nTesting definition fetching:');
  for (const word of ['run', 'beautiful', 'quickly']) {
    const def = await getDefinition(word);
    console.log(`  ${word}: ${def ? def.substring(0, 50) + '...' : 'Not found'}`);
  }
} else if (definitionsMode) {
  // Add missing definitions
  addMissingDefinitions().catch(console.error);
} else {
  // Run the full process
  assignPartsOfSpeechWithNLP().catch(console.error);
}