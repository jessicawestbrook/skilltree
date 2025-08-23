const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTI0MTMzNSwiZXhwIjoyMDcwODE3MzM1fQ.x-QbhMeO7HzECupWqq_XuHXeTbQmQwvVKasC61jb7Ws';

const supabase = createClient(supabaseUrl, supabaseKey);

async function createBalancedScrippsDistribution() {
  console.log('Creating balanced Scripps difficulty distribution...');
  console.log('Target: 40% One Bee, 35% Two Bee, 25% Three Bee');
  
  try {
    // Fetch all words
    const batchSize = 1000;
    const totalBatches = 9;
    let allWords = [];
    
    console.log('Fetching all words...');
    
    for (let batch = 0; batch < totalBatches; batch++) {
      const start = batch * batchSize;
      const end = start + batchSize - 1;
      
      const { data: batchWords, error } = await supabase
        .from('spelling_words')
        .select('id, word, source_difficulty, source_difficulties, ai_spelling_difficulty_level, spelling_difficulty_level')
        .range(start, end);
      
      if (error) {
        console.error(`Error fetching batch ${batch + 1}:`, error);
        continue;
      }
      
      allWords = allWords.concat(batchWords || []);
      console.log(`Fetched batch ${batch + 1}/${totalBatches}: ${batchWords?.length || 0} words`);
    }
    
    console.log(`Total words: ${allWords.length}`);
    
    // Calculate target counts
    const targets = {
      'One Bee': Math.floor(allWords.length * 0.40),   // 40% ≈ 3,549
      'Two Bee': Math.floor(allWords.length * 0.35),   // 35% ≈ 3,105  
      'Three Bee': Math.floor(allWords.length * 0.25)  // 25% ≈ 2,218
    };
    
    console.log('\\nTarget distribution:');
    Object.entries(targets).forEach(([level, count]) => {
      console.log(`  ${level}: ${count} words (${(count/allWords.length*100).toFixed(1)}%)`);
    });
    
    // Categorize words by difficulty characteristics
    const wordCategories = {
      easy: [],      // Short, simple words -> One Bee
      medium: [],    // Medium complexity -> Two Bee  
      hard: []       // Long, complex words -> Three Bee
    };
    
    allWords.forEach(word => {
      const aiLevel = word.ai_spelling_difficulty_level || word.spelling_difficulty_level || 1;
      const wordLength = word.word.length;
      const hasOriginalData = word.source_difficulties && typeof word.source_difficulties === 'string';
      
      // Scoring system to categorize difficulty
      let difficultyScore = 0;
      
      // AI difficulty contribution (0-5 points)
      difficultyScore += Math.min(aiLevel, 5);
      
      // Word length contribution (0-4 points)
      if (wordLength <= 5) difficultyScore += 0;
      else if (wordLength <= 8) difficultyScore += 2;
      else if (wordLength <= 12) difficultyScore += 3;
      else difficultyScore += 4;
      
      // Original data bonus (prefer words with multiple difficulties for higher levels)
      if (hasOriginalData) {
        const originalDiffs = word.source_difficulties.split(',').map(d => d.trim());
        if (originalDiffs.includes('Three Bee')) difficultyScore += 2;
        else if (originalDiffs.includes('Two Bee')) difficultyScore += 1;
      }
      
      // Categorize based on total score
      if (difficultyScore <= 3) {
        wordCategories.easy.push({...word, score: difficultyScore});
      } else if (difficultyScore <= 6) {
        wordCategories.medium.push({...word, score: difficultyScore});
      } else {
        wordCategories.hard.push({...word, score: difficultyScore});
      }
    });
    
    console.log('\\nWord categorization:');
    console.log(`  Easy (→ One Bee): ${wordCategories.easy.length}`);
    console.log(`  Medium (→ Two Bee): ${wordCategories.medium.length}`);
    console.log(`  Hard (→ Three Bee): ${wordCategories.hard.length}`);
    
    // Sort each category by score for better distribution
    wordCategories.easy.sort((a, b) => a.score - b.score);
    wordCategories.medium.sort((a, b) => a.score - b.score);
    wordCategories.hard.sort((a, b) => b.score - a.score);
    
    // Assign words to reach target distribution
    const assignments = [];
    const assigned = new Set();
    
    // First, assign from appropriate categories
    let oneBeeCount = 0, twoBeeCount = 0, threeBeeCount = 0;
    
    // Assign easy words to One Bee
    for (const word of wordCategories.easy) {
      if (oneBeeCount < targets['One Bee']) {
        assignments.push({...word, newDifficulty: 'One Bee'});
        assigned.add(word.id);
        oneBeeCount++;
      }
    }
    
    // Assign hard words to Three Bee
    for (const word of wordCategories.hard) {
      if (threeBeeCount < targets['Three Bee'] && !assigned.has(word.id)) {
        assignments.push({...word, newDifficulty: 'Three Bee'});
        assigned.add(word.id);
        threeBeeCount++;
      }
    }
    
    // Assign medium words to Two Bee
    for (const word of wordCategories.medium) {
      if (twoBeeCount < targets['Two Bee'] && !assigned.has(word.id)) {
        assignments.push({...word, newDifficulty: 'Two Bee'});
        assigned.add(word.id);
        twoBeeCount++;
      }
    }
    
    // Fill remaining slots by redistributing from categories with excess
    const remaining = allWords.filter(word => !assigned.has(word.id));
    
    for (const word of remaining) {
      if (oneBeeCount < targets['One Bee']) {
        assignments.push({...word, newDifficulty: 'One Bee'});
        oneBeeCount++;
      } else if (twoBeeCount < targets['Two Bee']) {
        assignments.push({...word, newDifficulty: 'Two Bee'});
        twoBeeCount++;
      } else {
        assignments.push({...word, newDifficulty: 'Three Bee'});
        threeBeeCount++;
      }
    }
    
    console.log('\\nPlanned final distribution:');
    console.log(`  One Bee: ${oneBeeCount} words (${(oneBeeCount/allWords.length*100).toFixed(1)}%)`);
    console.log(`  Two Bee: ${twoBeeCount} words (${(twoBeeCount/allWords.length*100).toFixed(1)}%)`);
    console.log(`  Three Bee: ${threeBeeCount} words (${(threeBeeCount/allWords.length*100).toFixed(1)}%)`);
    
    // Create updates for words that need to change
    const updates = assignments.filter(word => 
      word.source_difficulty !== word.newDifficulty
    );
    
    console.log(`\\nWords to update: ${updates.length}`);
    
    // Show sample updates
    console.log('\\nSample updates:');
    updates.slice(0, 10).forEach(word => {
      console.log(`  "${word.word}": ${word.source_difficulty} → ${word.newDifficulty} (score: ${word.score})`);
    });
    
    // Apply updates in batches
    console.log('\\nApplying updates...');
    const updateBatchSize = 100;
    
    for (let i = 0; i < updates.length; i += updateBatchSize) {
      const batch = updates.slice(i, i + updateBatchSize);
      
      for (const word of batch) {
        const { error } = await supabase
          .from('spelling_words')
          .update({ source_difficulty: word.newDifficulty })
          .eq('id', word.id);
        
        if (error) {
          console.error(`Error updating "${word.word}":`, error);
        }
      }
      
      console.log(`Updated batch ${Math.floor(i/updateBatchSize) + 1}/${Math.ceil(updates.length/updateBatchSize)}`);
      
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    console.log('\\n✅ Created balanced Scripps difficulty distribution!');
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

if (require.main === module) {
  createBalancedScrippsDistribution()
    .then(() => {
      console.log('Script completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Script failed:', error);
      process.exit(1);
    });
}

module.exports = { createBalancedScrippsDistribution };