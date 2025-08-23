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

async function debugDifficultyIssues() {
  console.log('=== DEBUGGING DIFFICULTY LEVELS ===\n');
  
  // 1. Check if difficulty tables exist and have data
  console.log('1. Checking difficulty tables...\n');
  
  const { data: vocabDiffs, error: vocabError } = await supabase
    .from('vocabulary_difficulties')
    .select('*')
    .order('id');
  
  if (vocabError) {
    console.log('Error fetching vocabulary_difficulties:', vocabError.message);
  } else {
    console.log('Vocabulary Difficulties table:');
    if (vocabDiffs && vocabDiffs.length > 0) {
      vocabDiffs.forEach(d => {
        console.log(`  ID ${d.id}: ${d.name} - ${d.description || 'no description'}`);
      });
    } else {
      console.log('  ⚠️ Table is empty!');
    }
  }
  
  console.log();
  
  const { data: spellingDiffs, error: spellingError } = await supabase
    .from('spelling_difficulties')
    .select('*')
    .order('id');
  
  if (spellingError) {
    console.log('Error fetching spelling_difficulties:', spellingError.message);
  } else {
    console.log('Spelling Difficulties table:');
    if (spellingDiffs && spellingDiffs.length > 0) {
      spellingDiffs.forEach(d => {
        console.log(`  ID ${d.id}: ${d.name} - ${d.description || 'no description'}`);
      });
    } else {
      console.log('  ⚠️ Table is empty!');
    }
  }
  
  // 2. Check spelling_words table structure
  console.log('\n2. Checking spelling_words table structure...\n');
  
  const { data: sampleWords, error: sampleError } = await supabase
    .from('spelling_words')
    .select('*')
    .limit(5);
  
  if (sampleError) {
    console.log('Error fetching sample words:', sampleError.message);
  } else if (sampleWords && sampleWords.length > 0) {
    console.log('Sample word structure:');
    const firstWord = sampleWords[0];
    console.log('Columns:', Object.keys(firstWord).join(', '));
    console.log('\nFirst word details:');
    console.log(`  word: ${firstWord.word}`);
    console.log(`  vocabulary_difficulty_id: ${firstWord.vocabulary_difficulty_id}`);
    console.log(`  spelling_difficulty_id: ${firstWord.spelling_difficulty_id}`);
  }
  
  // 3. Check for NULL values
  console.log('\n3. Checking for NULL difficulty values...\n');
  
  const { count: nullVocabCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('vocabulary_difficulty_id', null);
  
  const { count: nullSpellingCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('spelling_difficulty_id', null);
  
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`Total words: ${totalCount}`);
  console.log(`Words with NULL vocabulary_difficulty_id: ${nullVocabCount}`);
  console.log(`Words with NULL spelling_difficulty_id: ${nullSpellingCount}`);
  
  // 4. Check for invalid foreign keys
  console.log('\n4. Checking for invalid foreign key references...\n');
  
  // Get all unique difficulty IDs from spelling_words
  const { data: allWords } = await supabase
    .from('spelling_words')
    .select('vocabulary_difficulty_id, spelling_difficulty_id')
    .not('vocabulary_difficulty_id', 'is', null)
    .not('spelling_difficulty_id', 'is', null)
    .limit(1000);
  
  if (allWords) {
    const uniqueVocabIds = [...new Set(allWords.map(w => w.vocabulary_difficulty_id).filter(id => id))];
    const uniqueSpellingIds = [...new Set(allWords.map(w => w.spelling_difficulty_id).filter(id => id))];
    
    console.log(`Unique vocabulary_difficulty_ids in use: ${uniqueVocabIds.join(', ')}`);
    console.log(`Unique spelling_difficulty_ids in use: ${uniqueSpellingIds.join(', ')}`);
    
    // Check if these IDs exist in the difficulty tables
    const validVocabIds = vocabDiffs ? vocabDiffs.map(d => d.id) : [];
    const validSpellingIds = spellingDiffs ? spellingDiffs.map(d => d.id) : [];
    
    const invalidVocabIds = uniqueVocabIds.filter(id => !validVocabIds.includes(id));
    const invalidSpellingIds = uniqueSpellingIds.filter(id => !validSpellingIds.includes(id));
    
    if (invalidVocabIds.length > 0) {
      console.log(`\n⚠️ Invalid vocabulary_difficulty_ids found: ${invalidVocabIds.join(', ')}`);
      for (const id of invalidVocabIds) {
        const { count } = await supabase
          .from('spelling_words')
          .select('*', { count: 'exact', head: true })
          .eq('vocabulary_difficulty_id', id);
        console.log(`  ID ${id}: ${count} words`);
      }
    }
    
    if (invalidSpellingIds.length > 0) {
      console.log(`\n⚠️ Invalid spelling_difficulty_ids found: ${invalidSpellingIds.join(', ')}`);
      for (const id of invalidSpellingIds) {
        const { count } = await supabase
          .from('spelling_words')
          .select('*', { count: 'exact', head: true })
          .eq('spelling_difficulty_id', id);
        console.log(`  ID ${id}: ${count} words`);
      }
    }
  }
  
  // 5. Check actual distribution
  console.log('\n5. Actual distribution of difficulty levels...\n');
  
  // For each valid difficulty level, count words
  if (vocabDiffs && vocabDiffs.length > 0) {
    console.log('Vocabulary Difficulty Distribution:');
    for (const diff of vocabDiffs) {
      const { count } = await supabase
        .from('spelling_words')
        .select('*', { count: 'exact', head: true })
        .eq('vocabulary_difficulty_id', diff.id);
      console.log(`  ${diff.name} (ID ${diff.id}): ${count} words`);
    }
  }
  
  if (spellingDiffs && spellingDiffs.length > 0) {
    console.log('\nSpelling Difficulty Distribution:');
    for (const diff of spellingDiffs) {
      const { count } = await supabase
        .from('spelling_words')
        .select('*', { count: 'exact', head: true })
        .eq('spelling_difficulty_id', diff.id);
      console.log(`  ${diff.name} (ID ${diff.id}): ${count} words`);
    }
  }
  
  // 6. Check if there are words with difficulty IDs but the difficulty tables are empty
  console.log('\n6. Summary of issues found:');
  
  const issues = [];
  
  if (!vocabDiffs || vocabDiffs.length === 0) {
    issues.push('❌ vocabulary_difficulties table is empty');
  }
  
  if (!spellingDiffs || spellingDiffs.length === 0) {
    issues.push('❌ spelling_difficulties table is empty');
  }
  
  if (nullVocabCount > 0) {
    issues.push(`❌ ${nullVocabCount} words have NULL vocabulary_difficulty_id`);
  }
  
  if (nullSpellingCount > 0) {
    issues.push(`❌ ${nullSpellingCount} words have NULL spelling_difficulty_id`);
  }
  
  if (issues.length === 0) {
    console.log('✅ No issues found!');
  } else {
    issues.forEach(issue => console.log(issue));
  }
}

debugDifficultyIssues().catch(console.error);