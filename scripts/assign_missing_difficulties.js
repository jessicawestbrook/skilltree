const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Function to calculate spelling difficulty based on word characteristics
function calculateSpellingDifficulty(word) {
  const wordLower = word.toLowerCase();
  let score = 0;
  
  // Length factor
  if (word.length <= 4) score += 1;
  else if (word.length <= 6) score += 2;
  else if (word.length <= 8) score += 3;
  else if (word.length <= 10) score += 4;
  else score += 5;
  
  // Silent letters
  const silentPatterns = ['igh', 'kn', 'gn', 'wr', 'mb', 'mn', 'ps', 'rh', 'gh', 'ue'];
  silentPatterns.forEach(pattern => {
    if (wordLower.includes(pattern)) score += 2;
  });
  
  // Double consonants
  if (/([bcdfghjklmnpqrstvwxyz])\1/i.test(word)) score += 1;
  
  // Unusual letter combinations
  const unusualPatterns = ['ph', 'ch', 'qu', 'tion', 'sion', 'ough', 'eigh', 'cie', 'sci'];
  unusualPatterns.forEach(pattern => {
    if (wordLower.includes(pattern)) score += 2;
  });
  
  // Foreign origin indicators
  const foreignPatterns = ['eau', 'eux', 'ois', 'eux', 'sch', 'tsch', 'tz', 'cz', 'sz'];
  foreignPatterns.forEach(pattern => {
    if (wordLower.includes(pattern)) score += 3;
  });
  
  // Convert score to difficulty level (1-5)
  if (score <= 3) return 1; // Beginner
  else if (score <= 6) return 2; // Elementary  
  else if (score <= 9) return 3; // Intermediate
  else if (score <= 12) return 4; // Advanced
  else return 5; // Expert
}

// Function to calculate vocabulary difficulty based on word characteristics
function calculateVocabularyDifficulty(word, definition) {
  let score = 0;
  
  // Common everyday words (level 1)
  const commonWords = ['hem', 'polo', 'drool', 'forgive', 'fragile', 'twin', 'trap', 'trip', 'trim', 'spin'];
  if (commonWords.includes(word.toLowerCase())) return 1;
  
  // Length as a basic indicator
  if (word.length <= 5) score += 1;
  else if (word.length <= 7) score += 2;
  else if (word.length <= 10) score += 3;
  else score += 4;
  
  // Morphological complexity
  const prefixes = ['un', 'pre', 'dis', 'mis', 'over', 'under', 'out', 'sub', 'super', 'anti', 'de', 'non'];
  const suffixes = ['able', 'ible', 'ment', 'ness', 'ity', 'tion', 'sion', 'ous', 'ful', 'less', 'ize'];
  
  prefixes.forEach(prefix => {
    if (word.toLowerCase().startsWith(prefix)) score += 1;
  });
  
  suffixes.forEach(suffix => {
    if (word.toLowerCase().endsWith(suffix)) score += 1;
  });
  
  // Latin/Greek roots (higher difficulty)
  const classicalRoots = ['psych', 'phil', 'morph', 'graph', 'path', 'chron', 'geo', 'bio', 'theo', 'anthro'];
  classicalRoots.forEach(root => {
    if (word.toLowerCase().includes(root)) score += 3;
  });
  
  // Convert score to difficulty level (1-5)
  if (score <= 2) return 1; // Basic
  else if (score <= 4) return 2; // Intermediate
  else if (score <= 6) return 3; // Advanced
  else if (score <= 8) return 4; // Sophisticated
  else return 5; // Academic
}

async function assignMissingDifficulties() {
  console.log('=== ASSIGNING MISSING DIFFICULTIES ===\n');
  
  const timestamp = Date.now();
  const progressFile = `scripts/difficulty_assignment_progress_${timestamp}.json`;
  const progress = {
    timestamp: new Date().toISOString(),
    processed: [],
    errors: [],
    assignments: []
  };
  
  try {
    // Get difficulties mapping
    const { data: difficulties } = await supabase
      .from('difficulties')
      .select('*')
      .order('category', { ascending: true })
      .order('level', { ascending: true });
    
    // Create lookup maps
    const spellingDiffMap = new Map();
    const vocabDiffMap = new Map();
    
    difficulties?.forEach(d => {
      if (d.category === 'spelling') {
        spellingDiffMap.set(d.level, d.id);
      } else if (d.category === 'vocabulary') {
        vocabDiffMap.set(d.level, d.id);
      }
    });
    
    console.log('📊 Difficulty mappings loaded:');
    console.log('Spelling:', Array.from(spellingDiffMap.entries()));
    console.log('Vocabulary:', Array.from(vocabDiffMap.entries()));
    
    // Get words missing difficulties
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition')
      .is('spelling_difficulty_id', null)
      .order('word');
    
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`\n📝 Processing ${wordsToUpdate?.length || 0} words...\n`);
    
    let updateCount = 0;
    const batchSize = 50;
    const batches = [];
    
    // Process words and create batches
    for (let i = 0; i < wordsToUpdate.length; i += batchSize) {
      const batch = wordsToUpdate.slice(i, i + batchSize);
      const updates = [];
      
      for (const wordData of batch) {
        const spellingLevel = calculateSpellingDifficulty(wordData.word);
        const vocabLevel = calculateVocabularyDifficulty(wordData.word, wordData.definition);
        
        const spellingDiffId = spellingDiffMap.get(spellingLevel);
        const vocabDiffId = vocabDiffMap.get(vocabLevel);
        
        if (spellingDiffId && vocabDiffId) {
          updates.push({
            id: wordData.id,
            word: wordData.word,
            spelling_difficulty_id: spellingDiffId,
            vocabulary_difficulty_id: vocabDiffId
          });
          
          progress.assignments.push({
            word: wordData.word,
            spelling_level: spellingLevel,
            vocab_level: vocabLevel
          });
        }
      }
      
      if (updates.length > 0) {
        batches.push(updates);
      }
    }
    
    // Show sample assignments for review
    console.log('📋 SAMPLE ASSIGNMENTS (first 10):');
    progress.assignments.slice(0, 10).forEach(a => {
      console.log(`  ${a.word}: Spelling L${a.spelling_level}, Vocabulary L${a.vocab_level}`);
    });
    
    console.log(`\n📊 ASSIGNMENT SUMMARY:`);
    const levelCounts = { spelling: {}, vocabulary: {} };
    progress.assignments.forEach(a => {
      levelCounts.spelling[a.spelling_level] = (levelCounts.spelling[a.spelling_level] || 0) + 1;
      levelCounts.vocabulary[a.vocab_level] = (levelCounts.vocabulary[a.vocab_level] || 0) + 1;
    });
    
    console.log('\nSpelling difficulty distribution:');
    Object.entries(levelCounts.spelling).sort().forEach(([level, count]) => {
      console.log(`  Level ${level}: ${count} words`);
    });
    
    console.log('\nVocabulary difficulty distribution:');
    Object.entries(levelCounts.vocabulary).sort().forEach(([level, count]) => {
      console.log(`  Level ${level}: ${count} words`);
    });
    
    // Save plan for review
    fs.writeFileSync(progressFile, JSON.stringify(progress, null, 2));
    console.log(`\n💾 Assignment plan saved to: ${progressFile}`);
    
    console.log('\n🔄 APPLYING UPDATES...');
    
    // Apply updates in batches
    for (let i = 0; i < batches.length; i++) {
      const batch = batches[i];
      console.log(`Processing batch ${i + 1}/${batches.length} (${batch.length} words)...`);
      
      for (const update of batch) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({
            spelling_difficulty_id: update.spelling_difficulty_id,
            vocabulary_difficulty_id: update.vocabulary_difficulty_id
          })
          .eq('id', update.id);
        
        if (updateError) {
          console.error(`Error updating ${update.word}:`, updateError);
          progress.errors.push({ word: update.word, error: updateError.message });
        } else {
          updateCount++;
          progress.processed.push(update.word);
        }
      }
      
      // Small delay between batches
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    // Verify results
    const { count: remainingNull } = await supabase
      .from('spelling_words')
      .select('id', { count: 'exact', head: true })
      .is('spelling_difficulty_id', null);
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ ASSIGNMENT COMPLETE!');
    console.log('='.repeat(60));
    console.log(`Updated: ${updateCount} words`);
    console.log(`Errors: ${progress.errors.length}`);
    console.log(`Remaining without difficulties: ${remainingNull || 0}`);
    
    // Save final results
    fs.writeFileSync(progressFile, JSON.stringify(progress, null, 2));
    
  } catch (error) {
    console.error('Error:', error);
  }
}

assignMissingDifficulties().catch(console.error);