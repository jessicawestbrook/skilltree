const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function fixDifficultyLevels() {
  try {
    console.log('=== FIXING DIFFICULTY LEVELS FOR ADAPTIVE LEARNING ===\n');
    
    // First, get all words with their current data
    console.log('1. Fetching all spelling words...');
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('id, word, source_difficulty, spelling_difficulty_level, vocabulary_difficulty_level, definition')
      .order('word');
    
    if (error) throw error;
    console.log(`   Found ${words.length} words to process\n`);
    
    // Process spelling difficulty levels
    console.log('2. Calculating new spelling difficulty levels based on bee ratings...');
    const spellingUpdates = [];
    
    words.forEach(word => {
      let newSpellingLevel = null;
      
      if (word.source_difficulty) {
        // Clean up source difficulty (handle multiple ratings)
        const sourceDiff = word.source_difficulty.split(';')[0].trim();
        
        // Map bee ratings to 1-5 scale with distribution
        if (sourceDiff === 'One Bee') {
          // One Bee words: mostly levels 1-2
          if (word.word.length <= 5) {
            newSpellingLevel = 1; // Very easy (short One Bee words)
          } else {
            newSpellingLevel = 2; // Easy (regular One Bee words)
          }
        } else if (sourceDiff === 'Two Bee') {
          // Two Bee words: level 3
          newSpellingLevel = 3; // Medium
        } else if (sourceDiff === 'Three Bee') {
          // Three Bee words: levels 4-5
          if (word.word.length >= 12 || word.word.includes('ph') || word.word.includes('gh') || 
              word.word.includes('ough') || word.word.includes('eigh')) {
            newSpellingLevel = 5; // Very hard (complex Three Bee words)
          } else {
            newSpellingLevel = 4; // Hard (regular Three Bee words)
          }
        }
      }
      
      if (newSpellingLevel !== null && newSpellingLevel !== word.spelling_difficulty_level) {
        spellingUpdates.push({
          id: word.id,
          word: word.word,
          old_level: word.spelling_difficulty_level,
          new_level: newSpellingLevel,
          source: word.source_difficulty
        });
      }
    });
    
    console.log(`   ${spellingUpdates.length} spelling levels need updating\n`);
    
    // Process vocabulary difficulty levels
    console.log('3. Calculating new vocabulary difficulty levels...');
    const vocabUpdates = [];
    
    // Common everyday words (should be level 1-2)
    const commonWords = new Set([
      'cat', 'dog', 'run', 'walk', 'happy', 'sad', 'big', 'small', 'good', 'bad',
      'eat', 'drink', 'sleep', 'play', 'work', 'home', 'school', 'friend', 'family',
      'water', 'food', 'sun', 'moon', 'day', 'night', 'hot', 'cold', 'new', 'old',
      'idea', 'people', 'lived', 'lives', 'logs', 'search', 'europe', 'set'
    ]);
    
    // Academic/technical indicators
    const academicSuffixes = ['tion', 'sion', 'ment', 'ance', 'ence', 'ity', 'ism', 'ogy', 'phy'];
    const technicalPrefixes = ['bio', 'geo', 'hydro', 'micro', 'macro', 'poly', 'mono', 'multi'];
    
    words.forEach(word => {
      let newVocabLevel = null;
      const w = word.word.toLowerCase();
      const def = word.definition?.toLowerCase() || '';
      
      // Level 1: Basic everyday words
      if (commonWords.has(w) || (w.length <= 4 && !def.includes('technical') && !def.includes('scientific'))) {
        newVocabLevel = 1;
      }
      // Level 5: Rare/scholarly words
      else if (def.includes('rare') || def.includes('archaic') || def.includes('obsolete') || 
               w.length > 15 || def.includes('highly technical')) {
        newVocabLevel = 5;
      }
      // Level 4: Specialized/technical terms
      else if (technicalPrefixes.some(prefix => w.startsWith(prefix)) ||
               def.includes('medical') || def.includes('scientific') || def.includes('technical') ||
               def.includes('mathematical') || def.includes('chemical')) {
        newVocabLevel = 4;
      }
      // Level 2: Common academic words
      else if (w.length <= 7 && !academicSuffixes.some(suffix => w.endsWith(suffix))) {
        newVocabLevel = 2;
      }
      // Level 3: Advanced general vocabulary (default for everything else)
      else {
        newVocabLevel = 3;
      }
      
      if (newVocabLevel !== null && newVocabLevel !== word.vocabulary_difficulty_level) {
        vocabUpdates.push({
          id: word.id,
          word: word.word,
          old_level: word.vocabulary_difficulty_level,
          new_level: newVocabLevel,
          definition_preview: def.substring(0, 50)
        });
      }
    });
    
    console.log(`   ${vocabUpdates.length} vocabulary levels need updating\n`);
    
    // Show distribution analysis
    console.log('4. New distribution analysis:');
    
    // Spelling distribution
    const newSpellingDist = {};
    spellingUpdates.forEach(u => {
      newSpellingDist[u.new_level] = (newSpellingDist[u.new_level] || 0) + 1;
    });
    
    console.log('\n   New Spelling Difficulty Distribution:');
    for (let i = 1; i <= 5; i++) {
      const count = newSpellingDist[i] || 0;
      const pct = (count / spellingUpdates.length * 100).toFixed(1);
      console.log(`   Level ${i}: ${count} words (${pct}%)`);
    }
    
    // Vocabulary distribution
    const newVocabDist = {};
    vocabUpdates.forEach(u => {
      newVocabDist[u.new_level] = (newVocabDist[u.new_level] || 0) + 1;
    });
    
    console.log('\n   New Vocabulary Difficulty Distribution:');
    for (let i = 1; i <= 5; i++) {
      const count = newVocabDist[i] || 0;
      const pct = (count / vocabUpdates.length * 100).toFixed(1);
      console.log(`   Level ${i}: ${count} words (${pct}%)`);
    }
    
    // Sample updates to review
    console.log('\n5. Sample updates to review:');
    
    console.log('\n   Spelling Level Changes (first 10):');
    spellingUpdates.slice(0, 10).forEach(u => {
      console.log(`   ${u.word}: ${u.old_level || 'null'} → ${u.new_level} (${u.source})`);
    });
    
    console.log('\n   Vocabulary Level Changes (first 10):');
    vocabUpdates.slice(0, 10).forEach(u => {
      console.log(`   ${u.word}: ${u.old_level || 'null'} → ${u.new_level}`);
    });
    
    // Save update data to CSV for review
    console.log('\n6. Saving update data to CSV files for review...');
    
    // Save spelling updates
    const spellingCSV = 'id,word,old_level,new_level,source_difficulty\n' +
      spellingUpdates.map(u => `${u.id},"${u.word}",${u.old_level || 'null'},${u.new_level},"${u.source}"`).join('\n');
    
    const fs = require('fs');
    fs.writeFileSync('spelling_level_updates.csv', spellingCSV);
    console.log('   Saved spelling_level_updates.csv');
    
    // Save vocabulary updates
    const vocabCSV = 'id,word,old_level,new_level,definition_preview\n' +
      vocabUpdates.map(u => `${u.id},"${u.word}",${u.old_level || 'null'},${u.new_level},"${u.definition_preview}"`).join('\n');
    
    fs.writeFileSync('vocabulary_level_updates.csv', vocabCSV);
    console.log('   Saved vocabulary_level_updates.csv');
    
    console.log('\n7. Next steps:');
    console.log('   1. Review the CSV files to verify the changes look correct');
    console.log('   2. Run generate_update_sql.js to create the SQL update statements');
    console.log('   3. Execute the SQL in Supabase to apply the changes');
    
  } catch (error) {
    console.error('Error:', error);
  }
}

fixDifficultyLevels();