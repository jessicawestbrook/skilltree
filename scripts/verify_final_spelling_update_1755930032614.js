const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyFinalUpdate() {
  console.log('=== VERIFICATION OF FINAL SPELLING WORDS UPDATE ===\n');
  
  // Get total counts
  const { data: totals, error: totalsError } = await supabase
    .from('spelling_words')
    .select('COUNT(*)');
    
  if (!totalsError && totals) {
    console.log(`Total words in database: ${totals[0].count}`);
  }
  
  // Get source difficulty distribution
  let allWords = [];
  const batchSize = 1000;
  let offset = 0;
  let hasMore = true;

  while (hasMore) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('source_difficulty')
      .not('source_difficulty', 'is', null)
      .range(offset, offset + batchSize - 1);

    if (error) break;

    if (batch && batch.length > 0) {
      allWords = allWords.concat(batch);
      offset += batchSize;
      hasMore = batch.length === batchSize;
    } else {
      hasMore = false;
    }
  }
    
  if (allWords.length > 0) {
    const distribution = {};
    allWords.forEach(row => {
      distribution[row.source_difficulty] = (distribution[row.source_difficulty] || 0) + 1;
    });
    
    console.log('\nFinal Source Difficulty Distribution:');
    Object.entries(distribution)
      .sort()
      .forEach(([diff, count]) => {
        const percentage = ((count / allWords.length) * 100).toFixed(1);
        console.log(`  ${diff}: ${count} words (${percentage}%)`);
      });
      
    console.log(`\nTotal words with source difficulties: ${allWords.length}`);
  }
  
  // Check for null difficulties
  const { data: nulls, error: nullError } = await supabase
    .from('spelling_words')
    .select('COUNT(*)')
    .is('source_difficulty', null);
    
  if (!nullError && nulls) {
    const nullCount = nulls[0].count;
    if (nullCount > 0) {
      console.log(`\n⚠️  ${nullCount} words still have null source_difficulty`);
    } else {
      console.log('\n✅ All words have source difficulties assigned!');
    }
  }
}

verifyFinalUpdate().then(() => process.exit(0)).catch(console.error);