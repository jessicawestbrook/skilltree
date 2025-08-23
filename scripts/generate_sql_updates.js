const fs = require('fs');
const path = require('path');

// Read the JSON file
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'nlp_parts_of_speech.json'), 'utf8'));

// Generate SQL updates
let sql = `-- SQL script to update parts of speech in spelling_words table
-- Generated from NLP analysis using compromise library
-- Total updates: ${data.results.length} words
-- Generated at: ${new Date().toISOString()}

-- NOTE: There may be a trigger issue with column "spelling_difficulty_name"
-- If updates fail, you may need to:
-- 1. Check for triggers: SELECT * FROM information_schema.triggers WHERE event_object_table = 'spelling_words';
-- 2. Temporarily disable problematic triggers
-- 3. Run these updates
-- 4. Re-enable triggers

BEGIN;

`;

// Generate UPDATE statements
data.results.forEach((item, index) => {
  // Escape single quotes in word for SQL
  const wordEscaped = item.word.replace(/'/g, "''");
  sql += `UPDATE spelling_words SET part_of_speech = '${item.part_of_speech}' WHERE id = '${item.id}'; -- ${wordEscaped}\n`;
  
  // Add progress comments every 500 updates
  if ((index + 1) % 500 === 0) {
    sql += `-- Progress: ${index + 1}/${data.results.length}\n\n`;
  }
});

sql += `
COMMIT;

-- Verify the updates
SELECT 
  COUNT(*) FILTER (WHERE part_of_speech IS NOT NULL) as with_pos,
  COUNT(*) FILTER (WHERE part_of_speech IS NULL) as without_pos,
  COUNT(*) as total
FROM spelling_words;
`;

// Write to file
const outputPath = path.join(__dirname, 'parts_of_speech_updates_full.sql');
fs.writeFileSync(outputPath, sql);

console.log(`SQL script generated: ${outputPath}`);
console.log(`Total UPDATE statements: ${data.results.length}`);
console.log('\nTo apply these updates:');
console.log('1. Open Supabase SQL Editor');
console.log('2. Check for problematic triggers first');
console.log('3. Run the SQL script');
console.log('\nAlternatively, if you fix the trigger issue, run: node scripts/apply_parts_of_speech.js');