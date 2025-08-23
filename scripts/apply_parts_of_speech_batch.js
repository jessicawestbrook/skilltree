const { createClient } = require('@supabase/supabase-js');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env.local') });
const fs = require('fs');

// Read the JSON file
const data = JSON.parse(fs.readFileSync('nlp_parts_of_speech.json', 'utf8'));

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing required environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function applyUpdatesBatch() {
  console.log('Applying parts of speech updates in batches...');
  console.log('Total words to update:', data.results.length);
  
  // Group updates by part of speech for more efficient batch updates
  const grouped = {};
  data.results.forEach(item => {
    if (!grouped[item.part_of_speech]) {
      grouped[item.part_of_speech] = [];
    }
    grouped[item.part_of_speech].push(item.id);
  });
  
  console.log('\nGrouped by part of speech:');
  Object.entries(grouped).forEach(([pos, ids]) => {
    console.log(`  ${pos}: ${ids.length} words`);
  });
  
  let totalSuccess = 0;
  let totalError = 0;
  
  // Try batch updates by part of speech
  for (const [partOfSpeech, ids] of Object.entries(grouped)) {
    console.log(`\nUpdating ${ids.length} ${partOfSpeech}s...`);
    
    // Process in chunks of 100
    const chunkSize = 100;
    for (let i = 0; i < ids.length; i += chunkSize) {
      const chunk = ids.slice(i, i + chunkSize);
      
      try {
        // Try batch update
        const { data: result, error } = await supabase
          .from('spelling_words')
          .update({ part_of_speech: partOfSpeech })
          .in('id', chunk);
        
        if (error) {
          console.log(`  Batch ${Math.floor(i/chunkSize) + 1} failed:`, error.message);
          
          // If batch fails, try individual updates
          console.log('  Trying individual updates...');
          for (const id of chunk) {
            const { error: singleError } = await supabase
              .from('spelling_words')
              .update({ part_of_speech: partOfSpeech })
              .eq('id', id);
            
            if (singleError) {
              totalError++;
            } else {
              totalSuccess++;
            }
          }
        } else {
          totalSuccess += chunk.length;
          console.log(`  Batch ${Math.floor(i/chunkSize) + 1} succeeded (${chunk.length} words)`);
        }
      } catch (err) {
        console.error('Unexpected error:', err);
        totalError += chunk.length;
      }
      
      // Small delay between batches
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  console.log('\n=== Final Results ===');
  console.log('Successfully updated:', totalSuccess);
  console.log('Failed:', totalError);
  
  // Verify the updates
  const { count: withPos } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .not('part_of_speech', 'is', null);
  
  const { count: total } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log('\nDatabase status:');
  console.log('Total words:', total);
  console.log('Words with part_of_speech:', withPos);
  console.log('Coverage:', ((withPos / total) * 100).toFixed(1) + '%');
}

// Alternative: Generate SQL file for manual execution
function generateSQLFile() {
  console.log('\nGenerating SQL file as backup option...');
  
  let sql = `-- Batch update parts of speech
-- If direct updates fail due to triggers, try these approaches:

-- Approach 1: Disable triggers temporarily
ALTER TABLE spelling_words DISABLE TRIGGER ALL;

`;
  
  // Group by part of speech for cleaner SQL
  const grouped = {};
  data.results.forEach(item => {
    if (!grouped[item.part_of_speech]) {
      grouped[item.part_of_speech] = [];
    }
    grouped[item.part_of_speech].push(item.id);
  });
  
  Object.entries(grouped).forEach(([pos, ids]) => {
    sql += `\n-- Update ${ids.length} ${pos}s\n`;
    sql += `UPDATE spelling_words\n`;
    sql += `SET part_of_speech = '${pos}'\n`;
    sql += `WHERE id IN (\n`;
    
    // Add IDs in chunks for readability
    ids.forEach((id, index) => {
      sql += `  '${id}'${index < ids.length - 1 ? ',' : ''}\n`;
      if ((index + 1) % 10 === 0 && index < ids.length - 1) {
        sql += `  -- ${index + 1}/${ids.length}\n`;
      }
    });
    
    sql += `);\n`;
  });
  
  sql += `
-- Re-enable triggers
ALTER TABLE spelling_words ENABLE TRIGGER ALL;

-- Verify updates
SELECT 
  part_of_speech,
  COUNT(*) as count
FROM spelling_words
WHERE part_of_speech IS NOT NULL
GROUP BY part_of_speech
ORDER BY count DESC;
`;
  
  const outputPath = path.join(__dirname, 'parts_of_speech_batch_update.sql');
  fs.writeFileSync(outputPath, sql);
  console.log(`SQL file saved to: ${outputPath}`);
}

// Run both approaches
applyUpdatesBatch()
  .then(() => generateSQLFile())
  .catch(console.error);