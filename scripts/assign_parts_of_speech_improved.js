import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: join(__dirname, '..', '.env.local') });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceRoleKey = process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceRoleKey) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceRoleKey);

function inferPartOfSpeech(word, definition) {
  if (!word) return 'noun'; // Default fallback
  
  const wordLower = word.toLowerCase();
  const def = definition ? definition.toLowerCase() : '';
  
  // Strong indicators in definitions
  if (def.startsWith('to ') && !def.startsWith('to the') && !def.startsWith('to a')) {
    return 'verb';
  }
  
  if (def.includes('feeling') || def.includes('characterized by') || 
      def.includes('having the quality') || def.includes('marked by')) {
    return 'adjective';
  }
  
  if (def.includes('in a manner') || def.includes('in a way') || 
      def.endsWith('manner') || def.endsWith('way')) {
    return 'adverb';
  }
  
  // Word ending patterns with higher priority
  if (wordLower.endsWith('ing')) {
    if (def.includes('action') || def.includes('process') || def.includes('act of')) {
      return 'noun'; // Gerund
    }
    if (def.includes('continuous') || def.includes('ongoing')) {
      return 'verb'; // Present participle
    }
    return 'verb'; // Default for -ing
  }
  
  if (wordLower.endsWith('ed')) {
    if (def.includes('past tense') || def.includes('past form')) {
      return 'verb';
    }
    if (def.includes('having been') || def.includes('characterized')) {
      return 'adjective';
    }
    // Check context - if definition describes a state/quality, it's likely adjective
    if (def.includes('feeling') || def.includes('state')) {
      return 'adjective';
    }
    return 'verb'; // Default for -ed
  }
  
  // Strong suffix indicators
  if (wordLower.endsWith('ly')) {
    if (!def.includes('person') && !def.includes('thing')) {
      return 'adverb';
    }
  }
  
  if (wordLower.endsWith('ness') || wordLower.endsWith('ment') || 
      wordLower.endsWith('tion') || wordLower.endsWith('sion') ||
      wordLower.endsWith('ity') || wordLower.endsWith('ance') ||
      wordLower.endsWith('ence') || wordLower.endsWith('ship') ||
      wordLower.endsWith('hood') || wordLower.endsWith('dom')) {
    return 'noun';
  }
  
  if (wordLower.endsWith('ive') || wordLower.endsWith('ous') ||
      wordLower.endsWith('ful') || wordLower.endsWith('less') ||
      wordLower.endsWith('able') || wordLower.endsWith('ible') ||
      wordLower.endsWith('some') || wordLower.endsWith('ish')) {
    return 'adjective';
  }
  
  if (wordLower.endsWith('ize') || wordLower.endsWith('ise') ||
      wordLower.endsWith('ify') || wordLower.endsWith('ate')) {
    return 'verb';
  }
  
  // Check definition patterns
  if (def.startsWith('a ') || def.startsWith('an ') || def.startsWith('the ') ||
      def.startsWith('one who') || def.startsWith('someone who') ||
      def.startsWith('something that') || def.includes('type of') ||
      def.includes('kind of') || def.includes('person who')) {
    return 'noun';
  }
  
  // Specific word checks based on the samples
  const knownAdjectives = ['fragile', 'distraught', 'winsome', 'elderly'];
  const knownVerbs = ['forgive', 'help', 'evince', 'dwindled'];
  const knownNouns = ['polo', 'drool', 'sound', 'explanation', 'foxes', 'dojo', 
                       'foothills', 'zither', 'mystery', 'polenta'];
  
  if (knownAdjectives.some(adj => wordLower.includes(adj))) return 'adjective';
  if (knownVerbs.some(verb => wordLower.includes(verb))) return 'verb';
  if (knownNouns.some(noun => wordLower.includes(noun))) return 'noun';
  
  // Plural check
  if (wordLower.endsWith('s') && !wordLower.endsWith('ss') && 
      !wordLower.endsWith('us') && !wordLower.endsWith('is')) {
    if (def.includes('plural') || def.includes('more than one')) {
      return 'noun';
    }
  }
  
  // Default based on word length and structure
  if (wordLower.length <= 4) {
    // Short words are often verbs or basic nouns
    if (def.includes('action') || def.includes('to do')) {
      return 'verb';
    }
  }
  
  // Ultimate default
  return 'noun';
}

async function assignPartsOfSpeechImproved() {
  console.log('=== ASSIGNING PARTS OF SPEECH (IMPROVED) ===\n');
  
  // Fetch all words missing parts of speech
  let allWords = [];
  let offset = 0;
  const batchSize = 1000;
  
  while (true) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition')
      .or('part_of_speech.is.null,part_of_speech.eq.')
      .range(offset, offset + batchSize - 1);
    
    if (error) {
      console.error('Error fetching words:', error);
      break;
    }
    
    if (!batch || batch.length === 0) break;
    
    allWords = allWords.concat(batch);
    console.log(`Fetched ${allWords.length} words...`);
    
    if (batch.length < batchSize) break;
    offset += batchSize;
  }
  
  console.log(`\nTotal words to process: ${allWords.length}\n`);
  
  // Apply the improved algorithm and update directly
  const batchUpdateSize = 100;
  let totalUpdated = 0;
  let totalErrors = 0;
  
  // Track distribution
  const distribution = {};
  
  for (let i = 0; i < allWords.length; i += batchUpdateSize) {
    const batch = allWords.slice(i, i + batchUpdateSize);
    const batchNum = Math.floor(i / batchUpdateSize) + 1;
    const totalBatches = Math.ceil(allWords.length / batchUpdateSize);
    
    process.stdout.write(`Processing batch ${batchNum}/${totalBatches}: `);
    
    const updates = await Promise.all(batch.map(async (wordData) => {
      const pos = inferPartOfSpeech(wordData.word, wordData.definition);
      distribution[pos] = (distribution[pos] || 0) + 1;
      
      const { error } = await supabase
        .from('spelling_words')
        .update({ part_of_speech: pos })
        .eq('id', wordData.id);
      
      if (!error) {
        return { success: true, word: wordData.word, pos };
      } else {
        return { success: false, word: wordData.word, error };
      }
    }));
    
    const successCount = updates.filter(u => u.success).length;
    const errorCount = updates.filter(u => !u.success).length;
    
    totalUpdated += successCount;
    totalErrors += errorCount;
    
    console.log(`✓ ${successCount} updated, ${errorCount} errors`);
    
    // Show some examples from this batch
    if (batchNum <= 3) {
      const examples = updates.filter(u => u.success).slice(0, 3);
      examples.forEach(ex => {
        console.log(`    ${ex.word} → ${ex.pos}`);
      });
    }
    
    // Small delay between batches
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // Final summary
  console.log('\n--- Update Summary ---');
  console.log(`Total words processed: ${allWords.length}`);
  console.log(`Successfully updated: ${totalUpdated}`);
  console.log(`Errors: ${totalErrors}`);
  
  console.log('\n--- Part of Speech Distribution ---');
  Object.entries(distribution)
    .sort(([,a], [,b]) => b - a)
    .forEach(([pos, count]) => {
      const percent = ((count / allWords.length) * 100).toFixed(1);
      console.log(`  ${pos}: ${count} words (${percent}%)`);
    });
  
  // Verify
  const { count: stillMissing } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .or('part_of_speech.is.null,part_of_speech.eq.');
  
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`\nWords still missing part_of_speech: ${stillMissing}`);
  console.log(`Total words in database: ${totalCount}`);
  console.log(`Coverage: ${(((totalCount - stillMissing) / totalCount) * 100).toFixed(1)}%`);
  
  if (stillMissing === 0) {
    console.log('\n✅ All words now have parts of speech assigned!');
  } else {
    console.log('\n⚠️ Some words still need parts of speech.');
  }
}

assignPartsOfSpeechImproved().catch(console.error);