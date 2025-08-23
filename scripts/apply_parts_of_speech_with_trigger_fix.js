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

const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: {
    persistSession: false
  }
});

async function executeSql(sql) {
  // Since Supabase doesn't expose direct SQL execution through the JS client,
  // we need to use a workaround or create the SQL file for manual execution
  console.log('Executing SQL:', sql.substring(0, 100) + '...');
  
  // Try using the Supabase REST API directly
  const response = await fetch(`${supabaseUrl}/rest/v1/rpc/exec_sql`, {
    method: 'POST',
    headers: {
      'apikey': supabaseKey,
      'Authorization': `Bearer ${supabaseKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: sql })
  });
  
  if (!response.ok) {
    const error = await response.text();
    console.log('SQL execution failed:', error);
    return false;
  }
  
  return true;
}

async function applyUpdatesWithTriggerDisabled() {
  console.log('=== APPLYING PARTS OF SPEECH WITH TRIGGER MANAGEMENT ===\n');
  console.log('Total words to update:', data.results.length);
  
  // Since we can't execute raw SQL through the JS client, let's generate a complete SQL script
  let sqlScript = `-- Script to apply parts of speech updates
-- Generated at: ${new Date().toISOString()}

-- Step 1: Disable the problematic trigger
ALTER TABLE spelling_words DISABLE TRIGGER update_spelling_difficulty_name_trigger;

-- Step 2: Apply updates in batches
BEGIN;

`;

  // Group by part of speech for more efficient updates
  const grouped = {};
  data.results.forEach(item => {
    if (!grouped[item.part_of_speech]) {
      grouped[item.part_of_speech] = [];
    }
    grouped[item.part_of_speech].push(item.id);
  });

  console.log('Grouped by part of speech:');
  Object.entries(grouped).forEach(([pos, ids]) => {
    console.log(`  ${pos}: ${ids.length} words`);
    
    // Add batch update to SQL script
    sqlScript += `\n-- Update ${ids.length} ${pos}s\n`;
    
    // Split into smaller batches for the IN clause
    const batchSize = 500;
    for (let i = 0; i < ids.length; i += batchSize) {
      const batch = ids.slice(i, i + batchSize);
      sqlScript += `UPDATE spelling_words SET part_of_speech = '${pos}' WHERE id IN (\n`;
      batch.forEach((id, index) => {
        sqlScript += `  '${id}'${index < batch.length - 1 ? ',' : ''}\n`;
      });
      sqlScript += `);\n`;
    }
  });

  sqlScript += `
COMMIT;

-- Step 3: Re-enable the trigger
ALTER TABLE spelling_words ENABLE TRIGGER update_spelling_difficulty_name_trigger;

-- Step 4: Verify the updates
SELECT 
  part_of_speech,
  COUNT(*) as count
FROM spelling_words
WHERE part_of_speech IS NOT NULL
GROUP BY part_of_speech
ORDER BY count DESC;

-- Check total coverage
SELECT 
  COUNT(*) FILTER (WHERE part_of_speech IS NOT NULL) as with_pos,
  COUNT(*) FILTER (WHERE part_of_speech IS NULL) as without_pos,
  COUNT(*) as total,
  ROUND(100.0 * COUNT(*) FILTER (WHERE part_of_speech IS NOT NULL) / COUNT(*), 1) as coverage_percent
FROM spelling_words;
`;

  // Save the SQL script
  const outputPath = path.join(__dirname, 'apply_parts_of_speech_final.sql');
  fs.writeFileSync(outputPath, sqlScript);
  
  console.log(`\n✅ SQL script generated: ${outputPath}`);
  console.log('\n📋 Instructions:');
  console.log('1. Open Supabase Dashboard');
  console.log('2. Go to SQL Editor');
  console.log('3. Paste and run the contents of apply_parts_of_speech_final.sql');
  console.log('4. The script will:');
  console.log('   - Disable the update_spelling_difficulty_name_trigger');
  console.log('   - Apply all 4,628 parts of speech updates');
  console.log('   - Re-enable the trigger');
  console.log('   - Show verification statistics');
  
  // Also try applying updates through the client (in case trigger is already disabled)
  console.log('\n🔄 Attempting direct updates (in case trigger is already disabled)...');
  
  let successCount = 0;
  let errorCount = 0;
  const testBatch = data.results.slice(0, 10);
  
  for (const item of testBatch) {
    const { error } = await supabase
      .from('spelling_words')
      .update({ part_of_speech: item.part_of_speech })
      .eq('id', item.id);
    
    if (error) {
      errorCount++;
      if (errorCount === 1) {
        console.log('First error:', error.message);
      }
    } else {
      successCount++;
    }
  }
  
  if (successCount > 0) {
    console.log(`✅ Direct updates working! ${successCount}/10 test updates succeeded`);
    console.log('The trigger may have been disabled. Running full update...');
    
    // Run full update
    for (let i = 0; i < data.results.length; i += 100) {
      const batch = data.results.slice(i, i + 100);
      
      for (const item of batch) {
        const { error } = await supabase
          .from('spelling_words')
          .update({ part_of_speech: item.part_of_speech })
          .eq('id', item.id);
        
        if (!error) successCount++;
      }
      
      if (i % 1000 === 0) {
        console.log(`Progress: ${i}/${data.results.length}`);
      }
    }
    
    console.log(`\n✅ Updates complete! ${successCount} words updated`);
  } else {
    console.log(`❌ Direct updates still failing. Please use the SQL script.`);
  }
  
  // Final verification
  const { count: withPos } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .not('part_of_speech', 'is', null);
  
  const { count: total } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log('\n📊 Current database status:');
  console.log(`Total words: ${total}`);
  console.log(`Words with part_of_speech: ${withPos}`);
  console.log(`Coverage: ${((withPos / total) * 100).toFixed(1)}%`);
}

applyUpdatesWithTriggerDisabled().catch(console.error);