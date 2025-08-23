const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function restoreSourceDifficulty() {
  console.log('=== RESTORING SOURCE DIFFICULTY FROM BACKUP ===\n');

  try {
    console.log('Fetching source difficulty data from backup table...');
    
    // Get all source difficulty values from backup table
    let backupData = [];
    const batchSize = 1000;
    let offset = 0;
    let hasMore = true;

    while (hasMore) {
      const { data: batch, error } = await supabase
        .from('spelling_words_bkp3')
        .select('id, word, source_difficulty')
        .range(offset, offset + batchSize - 1)
        .order('id');

      if (error) {
        console.error('Error fetching backup data:', error);
        return;
      }

      if (batch && batch.length > 0) {
        backupData = backupData.concat(batch);
        console.log(`Fetched ${backupData.length} backup records so far...`);
        offset += batchSize;
        hasMore = batch.length === batchSize;
      } else {
        hasMore = false;
      }
    }

    console.log(`\nTotal backup records: ${backupData.length}`);

    // Generate SQL update statements
    console.log('Generating SQL update statements...');
    const sqlStatements = [];
    
    for (const word of backupData) {
      if (word.source_difficulty) {
        // Escape single quotes in the source difficulty string
        const escapedDifficulty = word.source_difficulty.replace(/'/g, "''");
        const sqlUpdate = `UPDATE spelling_words SET source_difficulty = '${escapedDifficulty}' WHERE id = '${word.id}';`;
        sqlStatements.push(sqlUpdate);
      }
    }

    // Write SQL file
    const timestamp = Date.now();
    const sqlFile = `scripts/restore_source_difficulty_${timestamp}.sql`;
    
    const sqlContent = `-- Restore source difficulty values from backup
-- Generated on ${new Date().toISOString()}
-- Total updates: ${sqlStatements.length}

BEGIN;

-- Restore all source difficulty values
${sqlStatements.join('\n')}

COMMIT;

-- Verify results
SELECT 
  source_difficulty, 
  COUNT(*) as count 
FROM spelling_words 
WHERE source_difficulty IS NOT NULL 
GROUP BY source_difficulty 
ORDER BY count DESC;`;

    fs.writeFileSync(sqlFile, sqlContent);
    
    console.log(`\n✅ SQL file generated: ${sqlFile}`);
    console.log(`📋 Next steps:`);
    console.log(`1. Open your Supabase SQL Editor`);
    console.log(`2. Copy and paste the contents of the SQL file`);
    console.log(`3. Execute the SQL to restore all source difficulty values`);
    console.log(`4. Run the verification query at the end to confirm results`);

    // Save summary
    const summary = {
      totalUpdates: sqlStatements.length,
      backupTable: 'spelling_words_bkp3',
      sqlFile: sqlFile,
      generatedAt: new Date().toISOString()
    };
    
    const summaryFile = `scripts/restore_source_difficulty_summary_${timestamp}.json`;
    fs.writeFileSync(summaryFile, JSON.stringify(summary, null, 2));
    
    console.log(`\n📊 Summary saved: ${summaryFile}`);

  } catch (error) {
    console.error('Error during restoration:', error);
  }
}

restoreSourceDifficulty();