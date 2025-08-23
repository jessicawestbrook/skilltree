const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyUpdate() {
  console.log('=== VERIFICATION OF SPELLING WORDS UPDATE ===\n');
  
  // Get total counts
  const { data: totals, error: totalsError } = await supabase
    .from('spelling_words')
    .select('COUNT(*)');
    
  if (!totalsError && totals) {
    console.log(`Total words in database: ${totals[0].count}`);
  }
  
  // Get source difficulty distribution
  const { data: difficulties, error: diffError } = await supabase
    .from('spelling_words')
    .select('source_difficulty')
    .not('source_difficulty', 'is', null);
    
  if (!diffError && difficulties) {
    const distribution = {};
    difficulties.forEach(row => {
      distribution[row.source_difficulty] = (distribution[row.source_difficulty] || 0) + 1;
    });
    
    console.log('\nSource Difficulty Distribution:');
    Object.entries(distribution)
      .sort((a, b) => b[1] - a[1])
      .forEach(([diff, count]) => {
        console.log(`  ${diff}: ${count} words`);
      });
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

verifyUpdate().then(() => process.exit(0)).catch(console.error);