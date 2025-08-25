const fs = require('fs');

function generateUpdateSQL() {
  console.log('=== GENERATING SQL UPDATE STATEMENTS ===\n');
  
  try {
    // Read the CSV files
    console.log('1. Reading update CSV files...');
    
    const spellingCSV = fs.readFileSync('spelling_level_updates.csv', 'utf8');
    const vocabCSV = fs.readFileSync('vocabulary_level_updates.csv', 'utf8');
    
    // Parse spelling updates
    const spellingLines = spellingCSV.split('\n').slice(1).filter(line => line.trim()); // Skip header and empty lines
    const spellingUpdates = spellingLines.map(line => {
      // Handle UUID format and potential nulls
      const match = line.match(/^([a-f0-9-]+),"([^"]+)",([^,]+),(\d+),"([^"]+)"$/);
      if (match) {
        return {
          id: match[1],
          word: match[2],
          old_level: match[3],
          new_level: match[4],
          source: match[5]
        };
      }
      return null;
    }).filter(Boolean);
    
    console.log(`   Found ${spellingUpdates.length} spelling updates`);
    
    // Parse vocabulary updates
    const vocabLines = vocabCSV.split('\n').slice(1).filter(line => line.trim()); // Skip header and empty lines
    const vocabUpdates = vocabLines.map(line => {
      // Handle UUID format and potential nulls
      const match = line.match(/^([a-f0-9-]+),"([^"]+)",([^,]+),(\d+),"([^"]*)"$/);
      if (match) {
        return {
          id: match[1],
          word: match[2],
          old_level: match[3],
          new_level: match[4]
        };
      }
      return null;
    }).filter(Boolean);
    
    console.log(`   Found ${vocabUpdates.length} vocabulary updates\n`);
    
    // Generate SQL statements
    console.log('2. Generating SQL statements...');
    
    let sql = `-- SQL Script to Fix Difficulty Levels for Adaptive Learning
-- Generated: ${new Date().toISOString()}
-- This script updates spelling_difficulty_level and vocabulary_difficulty_level
-- to properly distribute words across 1-5 scales for adaptive learning

-- Create backup table first
CREATE TABLE IF NOT EXISTS spelling_words_bkp_difficulty_fix_${new Date().toISOString().slice(0,10).replace(/-/g, '_')} AS 
SELECT * FROM spelling_words;

-- Update spelling difficulty levels based on bee ratings
-- Distribution: Level 1 (1.5%), Level 2 (27%), Level 3 (39%), Level 4 (28%), Level 5 (4.4%)
`;
    
    // Group spelling updates by level for efficiency
    const spellingByLevel = {};
    spellingUpdates.forEach(u => {
      if (!spellingByLevel[u.new_level]) {
        spellingByLevel[u.new_level] = [];
      }
      spellingByLevel[u.new_level].push(u.id);
    });
    
    // Generate spelling update statements
    Object.keys(spellingByLevel).sort().forEach(level => {
      const ids = spellingByLevel[level];
      // Split into batches of 500 IDs to avoid query size limits
      for (let i = 0; i < ids.length; i += 500) {
        const batch = ids.slice(i, i + 500);
        sql += `
UPDATE spelling_words 
SET spelling_difficulty_level = ${level}
WHERE id IN (${batch.map(id => `'${id}'`).join(',')});
`;
      }
    });
    
    sql += `
-- Update vocabulary difficulty levels based on semantic complexity
-- Distribution: Level 1 (10.8%), Level 2 (49.7%), Level 3 (25.4%), Level 4 (8.4%), Level 5 (5.8%)
`;
    
    // Group vocabulary updates by level
    const vocabByLevel = {};
    vocabUpdates.forEach(u => {
      if (!vocabByLevel[u.new_level]) {
        vocabByLevel[u.new_level] = [];
      }
      vocabByLevel[u.new_level].push(u.id);
    });
    
    // Generate vocabulary update statements
    Object.keys(vocabByLevel).sort().forEach(level => {
      const ids = vocabByLevel[level];
      // Split into batches of 500 IDs
      for (let i = 0; i < ids.length; i += 500) {
        const batch = ids.slice(i, i + 500);
        sql += `
UPDATE spelling_words 
SET vocabulary_difficulty_level = ${level}
WHERE id IN (${batch.map(id => `'${id}'`).join(',')});
`;
      }
    });
    
    // Add verification queries
    sql += `
-- Verification queries to check the new distributions
-- Check spelling difficulty distribution
SELECT 
  spelling_difficulty_level,
  COUNT(*) as count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM spelling_words
WHERE spelling_difficulty_level IS NOT NULL
GROUP BY spelling_difficulty_level
ORDER BY spelling_difficulty_level;

-- Check vocabulary difficulty distribution
SELECT 
  vocabulary_difficulty_level,
  COUNT(*) as count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM spelling_words
WHERE vocabulary_difficulty_level IS NOT NULL
GROUP BY vocabulary_difficulty_level
ORDER BY vocabulary_difficulty_level;

-- Check alignment with bee ratings
SELECT 
  source_difficulty,
  spelling_difficulty_level,
  COUNT(*) as count
FROM spelling_words
WHERE source_difficulty IN ('One Bee', 'Two Bee', 'Three Bee')
  AND spelling_difficulty_level IS NOT NULL
GROUP BY source_difficulty, spelling_difficulty_level
ORDER BY source_difficulty, spelling_difficulty_level;
`;
    
    // Save SQL file
    const sqlFile = 'fix_difficulty_levels.sql';
    fs.writeFileSync(sqlFile, sql);
    console.log(`   Generated ${sqlFile} with ${spellingUpdates.length + vocabUpdates.length} updates\n`);
    
    // Generate summary report
    console.log('3. Summary of changes:');
    console.log('\n   Spelling Difficulty Changes:');
    Object.keys(spellingByLevel).sort().forEach(level => {
      console.log(`   Level ${level}: ${spellingByLevel[level].length} words`);
    });
    
    console.log('\n   Vocabulary Difficulty Changes:');
    Object.keys(vocabByLevel).sort().forEach(level => {
      console.log(`   Level ${level}: ${vocabByLevel[level].length} words`);
    });
    
    console.log('\n4. Next steps:');
    console.log('   1. Review fix_difficulty_levels.sql');
    console.log('   2. Run the SQL in Supabase SQL editor');
    console.log('   3. Verify the distributions with the verification queries');
    console.log('   4. Test adaptive learning with the new difficulty levels');
    
  } catch (error) {
    console.error('Error:', error);
    console.log('\nMake sure you run fix_difficulty_levels.js first to generate the CSV files.');
  }
}

generateUpdateSQL();