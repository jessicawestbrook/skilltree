const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Function to calculate spelling difficulty based on word characteristics
function calculateSpellingDifficultyId(word) {
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
  
  // Map to difficulty IDs from spelling_difficulty_levels table
  // ID 1: Beginner (Grades 1-3)
  // ID 2: Elementary (Grades 4-5)
  // ID 3: Intermediate (Grades 6-8)
  // ID 4: Advanced (Grades 9-12)
  // ID 5: Expert (Competition Level)
  
  if (score <= 3) return 1; // Beginner
  else if (score <= 6) return 2; // Elementary
  else if (score <= 9) return 3; // Intermediate
  else if (score <= 12) return 4; // Advanced
  else return 5; // Expert
}

// Function to calculate vocabulary difficulty based on word characteristics
function calculateVocabularyDifficultyId(word, definition) {
  let score = 0;
  const wordLower = word.toLowerCase();
  
  // Common everyday words - Foundation (ID 1)
  const commonWords = ['hem', 'polo', 'drool', 'trap', 'trip', 'trim', 'spin', 'twin', 
                      'drag', 'drop', 'flip', 'grip', 'snap', 'skip', 'slip', 'spot'];
  if (commonWords.includes(wordLower)) return 1;
  
  // Basic words that are slightly more complex - Academic (ID 2)
  const academicWords = ['forgive', 'fragile', 'humble', 'noble', 'puzzle', 'riddle',
                         'struggle', 'triumph', 'wisdom', 'courage', 'justice', 'freedom'];
  if (academicWords.includes(wordLower)) return 2;
  
  // Length as a basic indicator
  if (word.length <= 5) score += 1;
  else if (word.length <= 7) score += 2;
  else if (word.length <= 10) score += 3;
  else score += 4;
  
  // Morphological complexity
  const prefixes = ['un', 'pre', 'dis', 'mis', 'over', 'under', 'out', 'sub', 'super', 'anti', 'de', 'non', 'inter', 'trans'];
  const suffixes = ['able', 'ible', 'ment', 'ness', 'ity', 'tion', 'sion', 'ous', 'ful', 'less', 'ize', 'ify', 'ology'];
  
  prefixes.forEach(prefix => {
    if (wordLower.startsWith(prefix)) score += 1;
  });
  
  suffixes.forEach(suffix => {
    if (wordLower.endsWith(suffix)) score += 1;
  });
  
  // Latin/Greek roots (higher difficulty)
  const classicalRoots = ['psych', 'phil', 'morph', 'graph', 'path', 'chron', 'geo', 'bio', 'theo', 'anthro',
                         'auto', 'tele', 'micro', 'macro', 'poly', 'mono', 'hyper', 'hypo'];
  classicalRoots.forEach(root => {
    if (wordLower.includes(root)) score += 3;
  });
  
  // Map to difficulty IDs from vocabulary_difficulty_levels table
  // ID 1: Foundation - Basic everyday concepts
  // ID 2: Academic - School-level vocabulary
  // ID 3: Sophisticated - Advanced academic and professional
  // ID 4: Specialized - Domain-specific terminology
  // ID 5: Scholarly - Research and expert-level
  
  if (score <= 2) return 1; // Foundation
  else if (score <= 4) return 2; // Academic
  else if (score <= 6) return 3; // Sophisticated
  else if (score <= 8) return 4; // Specialized
  else return 5; // Scholarly
}

async function assignActualDifficultyIds() {
  console.log('=== ASSIGNING ACTUAL DIFFICULTY IDS ===\n');
  
  const timestamp = Date.now();
  const progressFile = `scripts/difficulty_assignment_actual_${timestamp}.json`;
  const progress = {
    timestamp: new Date().toISOString(),
    processed: [],
    errors: [],
    assignments: []
  };
  
  try {
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
    
    console.log(`📝 Processing ${wordsToUpdate?.length || 0} words without difficulty IDs...\n`);
    
    // Process words and create assignments
    const assignments = [];
    for (const wordData of wordsToUpdate || []) {
      const spellingDiffId = calculateSpellingDifficultyId(wordData.word);
      const vocabDiffId = calculateVocabularyDifficultyId(wordData.word, wordData.definition);
      
      assignments.push({
        id: wordData.id,
        word: wordData.word,
        spelling_difficulty_id: spellingDiffId,
        vocabulary_difficulty_id: vocabDiffId
      });
      
      progress.assignments.push({
        word: wordData.word,
        spelling_id: spellingDiffId,
        vocab_id: vocabDiffId
      });
    }
    
    // Show sample assignments for review
    console.log('📋 SAMPLE ASSIGNMENTS (first 20):');
    const diffNames = {
      spelling: {
        1: 'Beginner', 2: 'Elementary', 3: 'Intermediate', 4: 'Advanced', 5: 'Expert'
      },
      vocab: {
        1: 'Foundation', 2: 'Academic', 3: 'Sophisticated', 4: 'Specialized', 5: 'Scholarly'
      }
    };
    
    progress.assignments.slice(0, 20).forEach(a => {
      const spellingName = diffNames.spelling[a.spelling_id];
      const vocabName = diffNames.vocab[a.vocab_id];
      console.log(`  ${a.word}: Spelling ${spellingName} (${a.spelling_id}), Vocabulary ${vocabName} (${a.vocab_id})`);
    });
    
    // Show distribution
    console.log(`\n📊 ASSIGNMENT DISTRIBUTION:`);
    const spellingCounts = {};
    const vocabCounts = {};
    
    progress.assignments.forEach(a => {
      spellingCounts[a.spelling_id] = (spellingCounts[a.spelling_id] || 0) + 1;
      vocabCounts[a.vocab_id] = (vocabCounts[a.vocab_id] || 0) + 1;
    });
    
    console.log('\nSpelling difficulty distribution:');
    Object.entries(spellingCounts).sort().forEach(([id, count]) => {
      const name = diffNames.spelling[id];
      const percent = ((count / progress.assignments.length) * 100).toFixed(1);
      console.log(`  ${name} (ID ${id}): ${count} words (${percent}%)`);
    });
    
    console.log('\nVocabulary difficulty distribution:');
    Object.entries(vocabCounts).sort().forEach(([id, count]) => {
      const name = diffNames.vocab[id];
      const percent = ((count / progress.assignments.length) * 100).toFixed(1);
      console.log(`  ${name} (ID ${id}): ${count} words (${percent}%)`);
    });
    
    // Save plan for review
    fs.writeFileSync(progressFile, JSON.stringify(progress, null, 2));
    console.log(`\n💾 Assignment plan saved to: ${progressFile}`);
    
    console.log('\n🔄 APPLYING UPDATES...');
    
    // Apply updates in batches
    const batchSize = 100;
    let updateCount = 0;
    
    for (let i = 0; i < assignments.length; i += batchSize) {
      const batch = assignments.slice(i, i + batchSize);
      console.log(`Processing batch ${Math.floor(i/batchSize) + 1}/${Math.ceil(assignments.length/batchSize)} (${batch.length} words)...`);
      
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
      if (i + batchSize < assignments.length) {
        await new Promise(resolve => setTimeout(resolve, 500));
      }
    }
    
    // Verify results
    const { count: remainingNull } = await supabase
      .from('spelling_words')
      .select('id', { count: 'exact', head: true })
      .is('spelling_difficulty_id', null);
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ DIFFICULTY ASSIGNMENT COMPLETE!');
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

assignActualDifficultyIds().catch(console.error);