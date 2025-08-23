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

async function checkMissingDifficultyLevels() {
  console.log('Checking for missing difficulty levels in spelling words table...\n');

  // Check total count of words
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`Total spelling words: ${totalCount}`);

  // Check words with missing vocabulary_difficulty_id
  const { data: missingVocab, count: missingVocabCount } = await supabase
    .from('spelling_words')
    .select('id, word', { count: 'exact' })
    .is('vocabulary_difficulty_id', null)
    .limit(10);
  
  console.log(`\nWords missing vocabulary_difficulty_id: ${missingVocabCount}`);
  if (missingVocab && missingVocab.length > 0) {
    console.log('Sample words missing vocabulary difficulty:');
    missingVocab.forEach(w => console.log(`  - ${w.word} (id: ${w.id})`));
  }

  // Check words with missing spelling_difficulty_id
  const { data: missingSpelling, count: missingSpellingCount } = await supabase
    .from('spelling_words')
    .select('id, word', { count: 'exact' })
    .is('spelling_difficulty_id', null)
    .limit(10);
  
  console.log(`\nWords missing spelling_difficulty_id: ${missingSpellingCount}`);
  if (missingSpelling && missingSpelling.length > 0) {
    console.log('Sample words missing spelling difficulty:');
    missingSpelling.forEach(w => console.log(`  - ${w.word} (id: ${w.id})`));
  }

  // Check available difficulty levels
  console.log('\n--- Available Difficulty Levels ---');
  
  const { data: vocabDifficulties } = await supabase
    .from('vocabulary_difficulties')
    .select('id, name')
    .order('id');
  
  console.log('\nVocabulary Difficulties:');
  vocabDifficulties?.forEach(d => console.log(`  ${d.id}: ${d.name}`));

  const { data: spellingDifficulties } = await supabase
    .from('spelling_difficulties')
    .select('id, name')
    .order('id');
  
  console.log('\nSpelling Difficulties:');
  spellingDifficulties?.forEach(d => console.log(`  ${d.id}: ${d.name}`));

  // Check distribution of existing difficulty assignments
  console.log('\n--- Current Distribution ---');
  
  const { data: vocabDist } = await supabase
    .from('spelling_words')
    .select('vocabulary_difficulty_id')
    .not('vocabulary_difficulty_id', 'is', null);
  
  const vocabCounts = {};
  vocabDist?.forEach(w => {
    vocabCounts[w.vocabulary_difficulty_id] = (vocabCounts[w.vocabulary_difficulty_id] || 0) + 1;
  });
  
  console.log('\nVocabulary Difficulty Distribution:');
  Object.entries(vocabCounts).sort(([a], [b]) => a - b).forEach(([id, count]) => {
    const diff = vocabDifficulties?.find(d => d.id == id);
    console.log(`  ${diff?.name || `ID ${id}`}: ${count} words`);
  });

  const { data: spellingDist } = await supabase
    .from('spelling_words')
    .select('spelling_difficulty_id')
    .not('spelling_difficulty_id', 'is', null);
  
  const spellingCounts = {};
  spellingDist?.forEach(w => {
    spellingCounts[w.spelling_difficulty_id] = (spellingCounts[w.spelling_difficulty_id] || 0) + 1;
  });
  
  console.log('\nSpelling Difficulty Distribution:');
  Object.entries(spellingCounts).sort(([a], [b]) => a - b).forEach(([id, count]) => {
    const diff = spellingDifficulties?.find(d => d.id == id);
    console.log(`  ${diff?.name || `ID ${id}`}: ${count} words`);
  });

  console.log('\n--- Summary ---');
  console.log(`Total words: ${totalCount}`);
  console.log(`Missing vocabulary difficulty: ${missingVocabCount} (${((missingVocabCount/totalCount)*100).toFixed(1)}%)`);
  console.log(`Missing spelling difficulty: ${missingSpellingCount} (${((missingSpellingCount/totalCount)*100).toFixed(1)}%)`);
}

checkMissingDifficultyLevels().catch(console.error);