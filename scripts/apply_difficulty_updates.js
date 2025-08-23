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

async function applyDifficultyUpdates() {
  console.log('Loading difficulty assignments...\n');
  
  // Load the assignments from JSON
  const assignmentsPath = join(__dirname, 'difficulty_assignments_improved.json');
  const data = JSON.parse(fs.readFileSync(assignmentsPath, 'utf8'));
  const updates = data.assignments;
  
  console.log(`Preparing to update ${updates.length} words...`);
  console.log('\nDistribution summary:');
  console.log('Vocabulary:', data.vocabularyDistribution);
  console.log('Spelling:', data.spellingDistribution);
  
  // Process updates in batches to avoid timeout
  const batchSize = 50;
  let successCount = 0;
  let errorCount = 0;
  const errors = [];
  
  console.log(`\nProcessing updates in batches of ${batchSize}...`);
  
  for (let i = 0; i < updates.length; i += batchSize) {
    const batch = updates.slice(i, i + batchSize);
    const batchNumber = Math.floor(i / batchSize) + 1;
    const totalBatches = Math.ceil(updates.length / batchSize);
    
    process.stdout.write(`Batch ${batchNumber}/${totalBatches}: `);
    
    // Update each word in the batch
    const promises = batch.map(async (update) => {
      const { error } = await supabase
        .from('spelling_words')
        .update({
          vocabulary_difficulty_id: update.vocabulary_difficulty_id,
          spelling_difficulty_id: update.spelling_difficulty_id
        })
        .eq('id', update.id);
      
      if (error) {
        errors.push({ word: update.word, error: error.message });
        return false;
      }
      return true;
    });
    
    const results = await Promise.all(promises);
    const batchSuccess = results.filter(r => r).length;
    const batchErrors = results.filter(r => !r).length;
    
    successCount += batchSuccess;
    errorCount += batchErrors;
    
    console.log(`✓ ${batchSuccess} updated, ${batchErrors} errors`);
    
    // Small delay between batches to avoid rate limiting
    if (i + batchSize < updates.length) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  console.log('\n--- Update Summary ---');
  console.log(`Total words processed: ${updates.length}`);
  console.log(`Successfully updated: ${successCount}`);
  console.log(`Errors: ${errorCount}`);
  
  if (errors.length > 0) {
    console.log('\nErrors encountered:');
    errors.slice(0, 10).forEach(e => {
      console.log(`  ${e.word}: ${e.error}`);
    });
    if (errors.length > 10) {
      console.log(`  ... and ${errors.length - 10} more errors`);
    }
  }
  
  // Verify the updates
  console.log('\n--- Verification ---');
  
  const { data: missingVocab, count: missingVocabCount } = await supabase
    .from('spelling_words')
    .select('id', { count: 'exact' })
    .is('vocabulary_difficulty_id', null);
  
  const { data: missingSpelling, count: missingSpellingCount } = await supabase
    .from('spelling_words')
    .select('id', { count: 'exact' })
    .is('spelling_difficulty_id', null);
  
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`Total words in database: ${totalCount}`);
  console.log(`Words still missing vocabulary difficulty: ${missingVocabCount}`);
  console.log(`Words still missing spelling difficulty: ${missingSpellingCount}`);
  
  if (missingVocabCount === 0 && missingSpellingCount === 0) {
    console.log('\n✅ Success! All words now have difficulty levels assigned.');
  } else {
    console.log('\n⚠ Some words still have missing difficulty levels.');
  }
  
  // Show final distribution
  console.log('\n--- Final Distribution ---');
  
  const { data: vocabDist } = await supabase
    .from('spelling_words')
    .select('vocabulary_difficulty_id')
    .not('vocabulary_difficulty_id', 'is', null);
  
  const vocabCounts = {};
  vocabDist?.forEach(w => {
    vocabCounts[w.vocabulary_difficulty_id] = (vocabCounts[w.vocabulary_difficulty_id] || 0) + 1;
  });
  
  console.log('\nVocabulary Difficulty Distribution:');
  const vocabLabels = {1: 'Elementary', 2: 'Middle School', 3: 'High School', 4: 'College', 5: 'Advanced'};
  Object.entries(vocabCounts).sort(([a], [b]) => a - b).forEach(([id, count]) => {
    const percent = ((count / totalCount) * 100).toFixed(1);
    console.log(`  ${vocabLabels[id] || `Level ${id}`}: ${count} words (${percent}%)`);
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
  const spellingLabels = {1: 'Easy', 2: 'Medium', 3: 'Hard', 4: 'Expert'};
  Object.entries(spellingCounts).sort(([a], [b]) => a - b).forEach(([id, count]) => {
    const percent = ((count / totalCount) * 100).toFixed(1);
    console.log(`  ${spellingLabels[id] || `Level ${id}`}: ${count} words (${percent}%)`);
  });
}

applyDifficultyUpdates().catch(console.error);