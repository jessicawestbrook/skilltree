const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function analyzeBackupTables() {
  console.log('Analyzing backup tables...');
  
  const backupTables = ['spelling_words_bkp', 'spelling_words_bkp3', 'spelling_words_backup'];
  
  for (const tableName of backupTables) {
    try {
      console.log(`\n--- ${tableName} ---`);
      
      // Get total count by fetching all data in batches
      let allData = [];
      const batchSize = 1000;
      let offset = 0;
      let hasMore = true;

      while (hasMore) {
        const { data: batch, error } = await supabase
          .from(tableName)
          .select('id, word, source_difficulty')
          .range(offset, offset + batchSize - 1)
          .order('id');

        if (error) {
          console.log(`Error fetching from ${tableName}:`, error.message);
          break;
        }

        if (batch && batch.length > 0) {
          allData = allData.concat(batch);
          offset += batchSize;
          hasMore = batch.length === batchSize;
        } else {
          hasMore = false;
        }
      }
        
      if (allData && allData.length > 0) {
        console.log(`Total rows: ${allData.length}`);
        
        // Check source_difficulty patterns
        const difficultyPatterns = {};
        let nullCount = 0;
        
        allData.forEach(row => {
          if (row.source_difficulty) {
            const pattern = row.source_difficulty;
            difficultyPatterns[pattern] = (difficultyPatterns[pattern] || 0) + 1;
          } else {
            nullCount++;
          }
        });
        
        console.log(`Null source_difficulty: ${nullCount}`);
        console.log('Source difficulty patterns:');
        Object.entries(difficultyPatterns)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 10)
          .forEach(([pattern, count]) => {
            console.log(`  ${pattern}: ${count} words`);
          });
      }
    } catch (e) {
      console.log(`Error checking ${tableName}:`, e.message);
    }
  }
}

analyzeBackupTables().then(() => process.exit(0)).catch(console.error);