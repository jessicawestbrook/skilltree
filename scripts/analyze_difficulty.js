const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function analyzeDifficulty() {
  try {
    // Get overall difficulty distribution
    const { data: difficultyDist, error: distError } = await supabase
      .from('spelling_words')
      .select('difficulty, source_difficulty, word')
      .order('difficulty');
    
    if (distError) throw distError;
    
    // Count words by difficulty
    const diffCounts = {};
    const sourceDiffCounts = {};
    const diffBySource = {};
    const sampleWords = {};
    
    difficultyDist.forEach(word => {
      // Count by difficulty
      const diff = word.difficulty || 'null';
      diffCounts[diff] = (diffCounts[diff] || 0) + 1;
      
      // Count by source_difficulty
      const sourceDiff = word.source_difficulty || 'null';
      sourceDiffCounts[sourceDiff] = (sourceDiffCounts[sourceDiff] || 0) + 1;
      
      // Cross-tabulation
      const key = diff + '_vs_' + sourceDiff;
      diffBySource[key] = (diffBySource[key] || 0) + 1;
      
      // Collect sample words (first 5 for each difficulty)
      if (!sampleWords[diff]) sampleWords[diff] = [];
      if (sampleWords[diff].length < 5) {
        sampleWords[diff].push(word.word);
      }
    });
    
    console.log('\n=== DIFFICULTY DISTRIBUTION ===');
    console.log('Calculated Difficulty Counts:');
    Object.keys(diffCounts).sort().forEach(diff => {
      const count = diffCounts[diff];
      const pct = (count/difficultyDist.length*100).toFixed(1);
      console.log(`  ${diff}: ${count} words (${pct}%)`);
    });
    
    console.log('\nSource Difficulty (Bee Rating) Counts:');
    Object.keys(sourceDiffCounts).sort().forEach(diff => {
      const count = sourceDiffCounts[diff];
      const pct = (count/difficultyDist.length*100).toFixed(1);
      console.log(`  ${diff}: ${count} words (${pct}%)`);
    });
    
    console.log('\n=== CROSS-TABULATION: Calculated vs Source ===');
    console.log('Format: [calculated]_vs_[source]: count');
    const sortedKeys = Object.keys(diffBySource).sort();
    sortedKeys.forEach(key => {
      console.log(`  ${key}: ${diffBySource[key]}`);
    });
    
    console.log('\n=== SAMPLE WORDS BY DIFFICULTY ===');
    Object.keys(sampleWords).sort().forEach(diff => {
      console.log(`\n${diff}:`);
      sampleWords[diff].forEach(word => {
        console.log(`  - ${word}`);
      });
    });
    
    console.log(`\nTotal words analyzed: ${difficultyDist.length}`);
    
    // Now get more detailed analysis for mismatches
    console.log('\n=== MISMATCH ANALYSIS ===');
    console.log('Words where calculated difficulty differs from source:');
    
    const mismatches = difficultyDist.filter(w => 
      w.difficulty && w.source_difficulty && w.difficulty !== w.source_difficulty
    );
    
    console.log(`Total mismatches: ${mismatches.length} out of ${difficultyDist.filter(w => w.difficulty && w.source_difficulty).length} words with both values`);
    
    // Group mismatches by type
    const mismatchTypes = {};
    mismatches.forEach(w => {
      const type = `${w.difficulty} (calc) vs ${w.source_difficulty} (source)`;
      if (!mismatchTypes[type]) mismatchTypes[type] = [];
      if (mismatchTypes[type].length < 3) {
        mismatchTypes[type].push(w.word);
      }
    });
    
    console.log('\nMismatch patterns (showing up to 3 examples each):');
    Object.keys(mismatchTypes).sort().forEach(type => {
      console.log(`\n${type}: ${mismatches.filter(w => `${w.difficulty} (calc) vs ${w.source_difficulty} (source)` === type).length} words`);
      mismatchTypes[type].forEach(word => {
        console.log(`  - ${word}`);
      });
    });
    
  } catch (error) {
    console.error('Error:', error);
  }
}

analyzeDifficulty();