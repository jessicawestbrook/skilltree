import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

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

async function checkPartsOfSpeech() {
  console.log('=== CHECKING PARTS OF SPEECH IN SPELLING_WORDS ===\n');
  
  // Get total count
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`Total words: ${totalCount}`);
  
  // Check words with NULL or empty part_of_speech
  const { count: nullPOSCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .or('part_of_speech.is.null,part_of_speech.eq.');
  
  console.log(`Words with missing part_of_speech: ${nullPOSCount}`);
  
  // Check distribution of existing parts of speech
  console.log('\n--- Current Part of Speech Distribution ---');
  
  // Get all unique parts of speech
  const { data: partsOfSpeech } = await supabase
    .from('spelling_words')
    .select('part_of_speech')
    .not('part_of_speech', 'is', null)
    .neq('part_of_speech', '');
  
  if (partsOfSpeech) {
    const posCounts = {};
    partsOfSpeech.forEach(row => {
      const pos = row.part_of_speech;
      if (pos) {
        // Normalize to lowercase for counting
        const normalized = pos.toLowerCase().trim();
        posCounts[normalized] = (posCounts[normalized] || 0) + 1;
      }
    });
    
    // Sort by count
    Object.entries(posCounts)
      .sort(([,a], [,b]) => b - a)
      .forEach(([pos, count]) => {
        const percent = ((count / totalCount) * 100).toFixed(2);
        console.log(`  ${pos}: ${count} words (${percent}%)`);
      });
  }
  
  // Sample words without parts of speech
  console.log('\n--- Sample Words Missing Parts of Speech ---');
  const { data: missingPOS } = await supabase
    .from('spelling_words')
    .select('id, word, definition')
    .or('part_of_speech.is.null,part_of_speech.eq.')
    .limit(20);
  
  if (missingPOS && missingPOS.length > 0) {
    missingPOS.forEach(word => {
      // Truncate definition for display
      const shortDef = word.definition ? 
        (word.definition.length > 60 ? word.definition.substring(0, 60) + '...' : word.definition) : 
        'No definition';
      console.log(`  ${word.word}: "${shortDef}"`);
    });
  }
  
  // Check for non-standard part of speech values
  console.log('\n--- Checking for Non-Standard Values ---');
  
  const standardPOS = [
    'noun', 'verb', 'adjective', 'adverb', 'pronoun', 
    'preposition', 'conjunction', 'interjection', 'article',
    'determiner', 'auxiliary verb', 'modal verb'
  ];
  
  if (partsOfSpeech) {
    const nonStandard = new Set();
    partsOfSpeech.forEach(row => {
      if (row.part_of_speech) {
        const normalized = row.part_of_speech.toLowerCase().trim();
        if (!standardPOS.includes(normalized) && 
            !normalized.includes('noun') && 
            !normalized.includes('verb') &&
            !normalized.includes('adjective') &&
            !normalized.includes('adverb')) {
          nonStandard.add(row.part_of_speech);
        }
      }
    });
    
    if (nonStandard.size > 0) {
      console.log('Found non-standard part of speech values:');
      Array.from(nonStandard).slice(0, 20).forEach(pos => {
        console.log(`  "${pos}"`);
      });
    } else {
      console.log('All existing parts of speech appear to be standard.');
    }
  }
  
  console.log('\n--- Summary ---');
  console.log(`Total words: ${totalCount}`);
  console.log(`Missing part_of_speech: ${nullPOSCount} (${((nullPOSCount/totalCount)*100).toFixed(1)}%)`);
  console.log(`Has part_of_speech: ${totalCount - nullPOSCount} (${(((totalCount - nullPOSCount)/totalCount)*100).toFixed(1)}%)`);
}

checkPartsOfSpeech().catch(console.error);