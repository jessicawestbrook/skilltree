import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';
import Anthropic from '@anthropic-ai/sdk';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: join(__dirname, '..', '.env.local') });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceRoleKey = process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY;
const anthropicApiKey = process.env.ANTHROPIC_API_KEY;

if (!supabaseUrl || !supabaseServiceRoleKey) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

if (!anthropicApiKey) {
  console.error('Missing Anthropic API key');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceRoleKey);
const anthropic = new Anthropic({ apiKey: anthropicApiKey });

async function getPartsOfSpeechBatch(words) {
  try {
    const wordList = words.map(w => `"${w.word}"`).join(', ');
    
    const prompt = `Analyze these words and return ONLY their primary part of speech (noun, verb, adjective, adverb, pronoun, preposition, conjunction, interjection, or determiner). 
    
Words: ${wordList}

Return a JSON array with exactly ${words.length} items, each containing:
- word: the word
- pos: the part of speech

Example format:
[{"word":"example","pos":"noun"},{"word":"run","pos":"verb"}]

Important: 
- Choose the MOST COMMON usage if a word can be multiple parts of speech
- For past tense verbs ending in -ed, mark as "verb"
- For gerunds/present participles ending in -ing, mark as "verb" unless clearly used as noun
- For plural nouns, mark as "noun"

Return ONLY the JSON array, no other text.`;

    const response = await anthropic.messages.create({
      model: 'claude-3-haiku-20240307',
      max_tokens: 1000,
      temperature: 0.1,
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ]
    });

    const content = response.content[0].text;
    
    try {
      const results = JSON.parse(content);
      
      const posMap = {};
      results.forEach(r => {
        posMap[r.word.toLowerCase()] = r.pos;
      });
      
      return words.map(w => ({
        ...w,
        part_of_speech: posMap[w.word.toLowerCase()] || 'noun'
      }));
    } catch (parseError) {
      console.error('Error parsing Anthropic response:', parseError);
      console.log('Response was:', content);
      return words.map(w => ({ ...w, part_of_speech: 'noun' }));
    }
  } catch (error) {
    console.error('Error calling Anthropic API:', error.message);
    return words.map(w => ({ ...w, part_of_speech: 'noun' }));
  }
}

async function assignPartsOfSpeechWithNLP() {
  console.log('=== ASSIGNING PARTS OF SPEECH USING ANTHROPIC NLP ===\n');
  
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
  
  const processBatchSize = 20;
  const results = [];
  
  console.log(`Processing ${allWords.length} words in batches of ${processBatchSize}...\n`);
  
  for (let i = 0; i < allWords.length; i += processBatchSize) {
    const batch = allWords.slice(i, i + processBatchSize);
    const batchNum = Math.floor(i / processBatchSize) + 1;
    const totalBatches = Math.ceil(allWords.length / processBatchSize);
    
    process.stdout.write(`Processing batch ${batchNum}/${totalBatches}... `);
    
    const batchResults = await getPartsOfSpeechBatch(batch);
    results.push(...batchResults);
    
    console.log('✓');
    
    if (batchNum <= 3) {
      batchResults.slice(0, 3).forEach(r => {
        console.log(`    ${r.word} → ${r.part_of_speech}`);
      });
    }
    
    // Rate limiting for Anthropic API (adjust as needed)
    if (i + processBatchSize < allWords.length) {
      await new Promise(resolve => setTimeout(resolve, 1000)); // 1 second delay
    }
  }
  
  const outputPath = join(__dirname, 'anthropic_parts_of_speech.json');
  fs.writeFileSync(outputPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    totalWords: results.length,
    results: results
  }, null, 2));
  
  console.log(`\n✓ Saved NLP results to: ${outputPath}`);
  
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
    
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  console.log('\n--- Summary ---');
  console.log(`Total words processed: ${results.length}`);
  console.log(`Successfully updated: ${successCount}`);
  console.log(`Errors: ${errorCount}`);
  
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

// Check if we should run in test mode
const testMode = process.argv[2] === 'test';

if (testMode) {
  console.log('=== TEST MODE - Processing 5 words ===\n');
  
  const testWords = [
    { id: '1', word: 'run', definition: 'To move quickly' },
    { id: '2', word: 'beautiful', definition: 'Pleasing to look at' },
    { id: '3', word: 'quickly', definition: 'In a fast manner' },
    { id: '4', word: 'happiness', definition: 'The state of being happy' },
    { id: '5', word: 'and', definition: 'A conjunction' }
  ];
  
  getPartsOfSpeechBatch(testWords).then(results => {
    console.log('Test results:');
    results.forEach(r => {
      console.log(`  ${r.word} → ${r.part_of_speech}`);
    });
  }).catch(console.error);
} else {
  assignPartsOfSpeechWithNLP().catch(console.error);
}