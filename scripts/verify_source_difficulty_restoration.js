const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifySourceDifficultyRestoration() {
  console.log('Verifying source difficulty restoration...');
  
  // Get all words and count source difficulties
  let allWords = [];
  const batchSize = 1000;
  let offset = 0;
  let hasMore = true;

  while (hasMore) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('id, word, source_difficulty')
      .range(offset, offset + batchSize - 1)
      .order('id');

    if (error) {
      console.error('Error fetching words:', error);
      return;
    }

    if (batch && batch.length > 0) {
      allWords = allWords.concat(batch);
      console.log(`Fetched ${allWords.length} words so far...`);
      offset += batchSize;
      hasMore = batch.length === batchSize;
    } else {
      hasMore = false;
    }
  }
  
  // Count source difficulties
  const sourceDifficultyCount = {};
  let nullCount = 0;
  
  allWords.forEach(word => {
    if (word.source_difficulty) {
      sourceDifficultyCount[word.source_difficulty] = (sourceDifficultyCount[word.source_difficulty] || 0) + 1;
    } else {
      nullCount++;
    }
  });
  
  console.log(`\nTotal words in database: ${allWords.length}`);
  console.log('\nSource Difficulty Distribution:');
  
  const sortedDifficulties = Object.entries(sourceDifficultyCount)
    .sort((a, b) => b[1] - a[1]); // Sort by count descending
  
  let totalAssigned = 0;
  
  sortedDifficulties.forEach(([difficulty, count]) => {
    totalAssigned += count;
    const percentage = ((count / allWords.length) * 100).toFixed(1);
    console.log(`${difficulty}: ${count} words (${percentage}%)`);
  });
  
  console.log(`\nWords with source difficulties assigned: ${totalAssigned}`);
  
  if (nullCount > 0) {
    console.log(`⚠️  Words with NULL source difficulties: ${nullCount}`);
  } else {
    console.log('✅ All words have source difficulties assigned!');
  }
  
  // Show some sample words for verification
  console.log('\nSample words by source difficulty:');
  for (const [difficulty, count] of sortedDifficulties.slice(0, 3)) {
    const samples = allWords.filter(w => w.source_difficulty === difficulty).slice(0, 5);
    console.log(`\n${difficulty} (${count} total):`);
    samples.forEach(word => console.log(`  - ${word.word}`));
  }
}

verifySourceDifficultyRestoration().then(() => process.exit(0)).catch(console.error);