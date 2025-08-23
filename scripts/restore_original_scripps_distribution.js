const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTI0MTMzNSwiZXhwIjoyMDcwODE3MzM1fQ.x-QbhMeO7HzECupWqq_XuHXeTbQmQwvVKasC61jb7Ws';

const supabase = createClient(supabaseUrl, supabaseKey);

async function restoreOriginalScrippsDistribution() {
  console.log('Restoring original Scripps difficulty distribution...');
  
  try {
    // Get all words with their original source_difficulties
    const batchSize = 1000;
    const totalBatches = 9;
    let allWords = [];
    
    console.log('Fetching all words with original difficulty data...');
    
    for (let batch = 0; batch < totalBatches; batch++) {
      const start = batch * batchSize;
      const end = start + batchSize - 1;
      
      const { data: batchWords, error } = await supabase
        .from('spelling_words')
        .select('id, word, source_difficulties, source_difficulty')
        .range(start, end);
      
      if (error) {
        console.error(`Error fetching batch ${batch + 1}:`, error);
        continue;
      }
      
      allWords = allWords.concat(batchWords || []);
      console.log(`Fetched batch ${batch + 1}/${totalBatches}: ${batchWords?.length || 0} words`);
    }
    
    console.log(`Total words fetched: ${allWords.length}`);
    
    // Analyze original distribution
    const originalDistribution = {};
    const currentDistribution = {};
    
    allWords.forEach(word => {
      // Current distribution
      const current = word.source_difficulty;
      currentDistribution[current] = (currentDistribution[current] || 0) + 1;
      
      // Original distribution 
      const original = word.source_difficulties;
      if (original && typeof original === 'string') {
        const difficulties = original.split(',').map(d => d.trim());
        difficulties.forEach(diff => {
          originalDistribution[diff] = (originalDistribution[diff] || 0) + 1;
        });
      }
    });
    
    console.log('\\nCurrent (incorrect) distribution:');
    Object.entries(currentDistribution).sort((a, b) => b[1] - a[1]).forEach(([key, value]) => {
      console.log(`  ${key}: ${value} words`);
    });
    
    console.log('\\nOriginal distribution from source_difficulties:');
    Object.entries(originalDistribution).sort((a, b) => b[1] - a[1]).forEach(([key, value]) => {
      console.log(`  ${key}: ${value} words`);
    });
    
    // Plan redistribution based on original data
    const updates = [];
    
    allWords.forEach(word => {
      if (!word.source_difficulties || typeof word.source_difficulties !== 'string') return;
      
      const originalDiffs = word.source_difficulties.split(',').map(d => d.trim());
      
      // If word appears in multiple difficulties, assign based on priority and balance
      let newDifficulty;
      
      if (originalDiffs.length === 1) {
        // Single difficulty - use it
        const diff = originalDiffs[0];
        if (diff === 'One Bee' || diff === 'Two Bee' || diff === 'Three Bee') {
          newDifficulty = diff;
        }
      } else if (originalDiffs.length > 1) {
        // Multiple difficulties - assign to balance the distribution
        // Priority: Two Bee > Three Bee > One Bee (to balance out the current skew)
        if (originalDiffs.includes('Two Bee')) {
          newDifficulty = 'Two Bee';
        } else if (originalDiffs.includes('Three Bee')) {
          newDifficulty = 'Three Bee';  
        } else if (originalDiffs.includes('One Bee')) {
          newDifficulty = 'One Bee';
        }
      }
      
      // Only update if we determined a new difficulty and it's different
      if (newDifficulty && newDifficulty !== word.source_difficulty) {
        updates.push({
          id: word.id,
          word: word.word,
          oldDifficulty: word.source_difficulty,
          newDifficulty: newDifficulty,
          originalDifficulties: word.source_difficulties
        });
      }
    });
    
    console.log(`\\nPlanning to update ${updates.length} words`);
    
    // Show planned final distribution
    const plannedDistribution = { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 };
    
    allWords.forEach(word => {
      const update = updates.find(u => u.id === word.id);
      const finalDiff = update ? update.newDifficulty : word.source_difficulty;
      if (finalDiff && plannedDistribution.hasOwnProperty(finalDiff)) {
        plannedDistribution[finalDiff]++;
      }
    });
    
    console.log('\\nPlanned final distribution:');
    Object.entries(plannedDistribution).forEach(([key, value]) => {
      console.log(`  ${key}: ${value} words (${(value/8873*100).toFixed(1)}%)`);
    });
    
    // Show sample updates
    console.log('\\nSample planned updates:');
    updates.slice(0, 10).forEach(update => {
      console.log(`  "${update.word}": ${update.oldDifficulty} → ${update.newDifficulty} (was: ${update.originalDifficulties})`);
    });
    
    // Apply updates
    console.log('\\nApplying updates...');
    const updateBatchSize = 100;
    
    for (let i = 0; i < updates.length; i += updateBatchSize) {
      const batch = updates.slice(i, i + updateBatchSize);
      
      for (const update of batch) {
        const { error } = await supabase
          .from('spelling_words')
          .update({ source_difficulty: update.newDifficulty })
          .eq('id', update.id);
        
        if (error) {
          console.error(`Error updating "${update.word}":`, error);
        }
      }
      
      console.log(`Updated batch ${Math.floor(i/updateBatchSize) + 1}/${Math.ceil(updates.length/updateBatchSize)}`);
      
      // Brief pause
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    console.log('\\n✅ Restored original Scripps difficulty distribution!');
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

if (require.main === module) {
  restoreOriginalScrippsDistribution()
    .then(() => {
      console.log('Script completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Script failed:', error);
      process.exit(1);
    });
}

module.exports = { restoreOriginalScrippsDistribution };