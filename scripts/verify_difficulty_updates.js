const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyUpdates() {
  console.log('=== VERIFYING DIFFICULTY UPDATES ===\n');
  
  // Get updated distributions
  const { data: allWords } = await supabase
    .from('spelling_words')
    .select('spelling_difficulty_level, vocabulary_difficulty_level, frequency, word');
  
  // Count distributions
  const spellDist = {};
  const vocabDist = {};
  const freqByVocab = {};
  const combined = {};
  
  allWords.forEach(w => {
    if (w.spelling_difficulty_level) {
      spellDist[w.spelling_difficulty_level] = (spellDist[w.spelling_difficulty_level] || 0) + 1;
    }
    
    if (w.vocabulary_difficulty_level) {
      vocabDist[w.vocabulary_difficulty_level] = (vocabDist[w.vocabulary_difficulty_level] || 0) + 1;
      
      // Track average frequency by vocab level
      if (!freqByVocab[w.vocabulary_difficulty_level]) {
        freqByVocab[w.vocabulary_difficulty_level] = { sum: 0, count: 0 };
      }
      if (w.frequency !== null) {
        freqByVocab[w.vocabulary_difficulty_level].sum += w.frequency;
        freqByVocab[w.vocabulary_difficulty_level].count++;
      }
    }
    
    // Combined distribution
    if (w.spelling_difficulty_level && w.vocabulary_difficulty_level) {
      const key = `S${w.spelling_difficulty_level}_V${w.vocabulary_difficulty_level}`;
      combined[key] = (combined[key] || 0) + 1;
    }
  });
  
  // Display spelling distribution
  console.log('SPELLING DIFFICULTY DISTRIBUTION:');
  const totalSpelling = Object.values(spellDist).reduce((a, b) => a + b, 0);
  for (let i = 1; i <= 5; i++) {
    const count = spellDist[i] || 0;
    const pct = (count / totalSpelling * 100).toFixed(1);
    const bar = '█'.repeat(Math.floor(pct / 2));
    console.log(`  Level ${i}: ${count.toString().padStart(5)} words (${pct.padStart(5)}%) ${bar}`);
  }
  
  // Display vocabulary distribution with frequency ranges
  console.log('\nVOCABULARY DIFFICULTY DISTRIBUTION:');
  const vocabLabels = {
    1: 'Basic (freq 6+)     ',
    2: 'Elementary (5-6)    ',
    3: 'Intermediate (3-5)  ',
    4: 'Advanced (2-3)      ',
    5: 'Expert (0-2)        '
  };
  
  const totalVocab = Object.values(vocabDist).reduce((a, b) => a + b, 0);
  for (let i = 1; i <= 5; i++) {
    const count = vocabDist[i] || 0;
    const pct = (count / totalVocab * 100).toFixed(1);
    const avgFreq = freqByVocab[i] ? (freqByVocab[i].sum / freqByVocab[i].count).toFixed(2) : 'N/A';
    const bar = '█'.repeat(Math.floor(pct / 2));
    console.log(`  Level ${i} ${vocabLabels[i]}: ${count.toString().padStart(5)} words (${pct.padStart(5)}%) avg_freq=${avgFreq} ${bar}`);
  }
  
  // Check if vocabulary levels match frequency expectations
  console.log('\nVOCABULARY LEVEL VALIDATION:');
  for (let i = 1; i <= 5; i++) {
    if (freqByVocab[i] && freqByVocab[i].count > 0) {
      const avgFreq = freqByVocab[i].sum / freqByVocab[i].count;
      let expected = '';
      
      switch(i) {
        case 1: expected = avgFreq >= 6 ? '✓ Correct' : '✗ Should be 6+'; break;
        case 2: expected = avgFreq >= 5 && avgFreq < 6 ? '✓ Correct' : '✗ Should be 5-6'; break;
        case 3: expected = avgFreq >= 3 && avgFreq < 5 ? '✓ Correct' : '✗ Should be 3-5'; break;
        case 4: expected = avgFreq >= 2 && avgFreq < 3 ? '✓ Correct' : '✗ Should be 2-3'; break;
        case 5: expected = avgFreq < 2 ? '✓ Correct' : '✗ Should be 0-2'; break;
      }
      
      console.log(`  Level ${i}: avg frequency = ${avgFreq.toFixed(2)} ${expected}`);
    }
  }
  
  // Show some example words
  console.log('\nSAMPLE WORDS BY DIFFICULTY:');
  
  // Easy spelling + basic vocab (should be very common words)
  const easyCommon = allWords.filter(w => 
    w.spelling_difficulty_level <= 2 && 
    w.vocabulary_difficulty_level <= 2
  ).slice(0, 5);
  
  console.log('\nEasy Spelling + Common Vocabulary:');
  easyCommon.forEach(w => {
    console.log(`  ${w.word.padEnd(15)} (spell=${w.spelling_difficulty_level}, vocab=${w.vocabulary_difficulty_level}, freq=${w.frequency?.toFixed(2)})`);
  });
  
  // Hard spelling + rare vocab (should be complex rare words)
  const hardRare = allWords.filter(w => 
    w.spelling_difficulty_level >= 4 && 
    w.vocabulary_difficulty_level >= 4
  ).slice(0, 5);
  
  console.log('\nHard Spelling + Rare Vocabulary:');
  hardRare.forEach(w => {
    console.log(`  ${w.word.padEnd(15)} (spell=${w.spelling_difficulty_level}, vocab=${w.vocabulary_difficulty_level}, freq=${w.frequency?.toFixed(2)})`);
  });
  
  // Summary
  console.log('\n=== SUMMARY ===');
  console.log(`Total words: ${allWords.length}`);
  console.log(`Words with spelling difficulty: ${totalSpelling}`);
  console.log(`Words with vocabulary difficulty: ${totalVocab}`);
  console.log(`Words with both difficulties: ${Object.values(combined).reduce((a, b) => a + b, 0)}`);
  
  // Check for issues
  const issues = [];
  if (spellDist[1] > totalSpelling * 0.8) {
    issues.push('⚠️  Spelling difficulty still concentrated at Level 1');
  }
  if (vocabDist[1] === 0) {
    issues.push('⚠️  No words at vocabulary Level 1 (Basic)');
  }
  if (vocabDist[5] > totalVocab * 0.5) {
    issues.push('⚠️  Too many words at vocabulary Level 5 (Expert)');
  }
  
  if (issues.length > 0) {
    console.log('\n⚠️  POTENTIAL ISSUES:');
    issues.forEach(issue => console.log(`  ${issue}`));
  } else {
    console.log('\n✅ All difficulty distributions look reasonable!');
  }
}

verifyUpdates();