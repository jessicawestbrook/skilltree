const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTI0MTMzNSwiZXhwIjoyMDcwODE3MzM1fQ.x-QbhMeO7HzECupWqq_XuHXeTbQmQwvVKasC61jb7Ws';

const supabase = createClient(supabaseUrl, supabaseKey);

async function redistributeAllSpellingWords() {
  console.log('Redistributing ALL spelling words across Scripps difficulty levels...');
  
  try {
    // Get total count first
    const { count: totalCount, error: countError } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });
      
    if (countError) {
      console.error('Error getting count:', countError);
      return;
    }
    
    console.log(`Total spelling words to process: ${totalCount}`);
    
    // Fetch all words in batches to avoid query limits
    const batchSize = 1000;
    const totalBatches = Math.ceil(totalCount / batchSize);
    let allWords = [];
    
    console.log(`Fetching words in ${totalBatches} batches...`);
    
    for (let batch = 0; batch < totalBatches; batch++) {
      const start = batch * batchSize;
      const end = start + batchSize - 1;
      
      const { data: batchWords, error: batchError } = await supabase
        .from('spelling_words')
        .select('id, word, source_difficulty, spelling_difficulty_level, ai_spelling_difficulty_level, word')
        .range(start, end);
      
      if (batchError) {
        console.error(`Error fetching batch ${batch + 1}:`, batchError);
        continue;
      }
      
      allWords = allWords.concat(batchWords || []);
      console.log(`Fetched batch ${batch + 1}/${totalBatches}: ${batchWords?.length || 0} words`);
    }
    
    console.log(`Total words fetched: ${allWords.length}`);
    
    // Analyze current distribution
    const currentDistribution = {};
    allWords.forEach(word => {
      const diff = word.source_difficulty || 'NULL';
      currentDistribution[diff] = (currentDistribution[diff] || 0) + 1;
    });
    
    console.log('\\nCurrent distribution:');
    Object.entries(currentDistribution)
      .sort((a, b) => b[1] - a[1])
      .forEach(([key, value]) => {
        console.log(`  ${key}: ${value} words`);
      });
    
    // Redistribute all words to Scripps levels
    const updates = [];
    
    allWords.forEach(word => {
      let newDifficulty;
      
      // If already has a single Scripps difficulty, keep it
      if (word.source_difficulty === 'One Bee' || 
          word.source_difficulty === 'Two Bee' || 
          word.source_difficulty === 'Three Bee') {
        return; // Skip, already properly assigned
      }
      
      // For all other cases, assign based on AI difficulty and word characteristics
      const aiLevel = word.ai_spelling_difficulty_level || word.spelling_difficulty_level || 1;
      const wordLength = word.word.length;
      
      // Distribution logic:
      // - 60% to One Bee (beginner)
      // - 25% to Three Bee (advanced) 
      // - 15% to Two Bee (intermediate)
      
      const random = Math.random();
      
      if (aiLevel <= 2 && wordLength <= 6 && random < 0.7) {
        newDifficulty = 'One Bee';
      } else if (aiLevel >= 4 || wordLength >= 9 || random < 0.25) {
        newDifficulty = 'Three Bee';
      } else {
        newDifficulty = 'Two Bee';
      }
      
      // Adjust for better distribution
      if (aiLevel === 1 && wordLength <= 5) {
        newDifficulty = 'One Bee';
      } else if (aiLevel >= 5 && wordLength >= 10) {
        newDifficulty = 'Three Bee';
      }
      
      updates.push({
        id: word.id,
        word: word.word,
        oldDifficulty: word.source_difficulty,
        newDifficulty: newDifficulty
      });
    });
    
    console.log(`\\nPlanning to update ${updates.length} words`);
    
    // Show planned distribution
    const plannedDistribution = { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 };
    
    // Count existing properly assigned words
    allWords.forEach(word => {
      if (word.source_difficulty === 'One Bee' || 
          word.source_difficulty === 'Two Bee' || 
          word.source_difficulty === 'Three Bee') {
        plannedDistribution[word.source_difficulty]++;
      }
    });
    
    // Add planned updates
    updates.forEach(update => {
      plannedDistribution[update.newDifficulty]++;
    });
    
    console.log('\\nPlanned final distribution:');
    Object.entries(plannedDistribution).forEach(([key, value]) => {
      console.log(`  ${key}: ${value} words`);
    });
    
    // Apply updates in batches
    console.log('\\nApplying updates...');
    const updateBatchSize = 100;
    
    for (let i = 0; i < updates.length; i += updateBatchSize) {
      const batch = updates.slice(i, i + updateBatchSize);
      
      for (const update of batch) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ source_difficulty: update.newDifficulty })
          .eq('id', update.id);
        
        if (updateError) {
          console.error(`Error updating word "${update.word}":`, updateError);
        }
      }
      
      console.log(`Updated batch ${Math.floor(i/updateBatchSize) + 1}/${Math.ceil(updates.length/updateBatchSize)}`);
      
      // Brief pause to avoid overwhelming the database
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    console.log('\\nRedistribution completed successfully!');
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

if (require.main === module) {
  redistributeAllSpellingWords()
    .then(() => {
      console.log('Script completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Script failed:', error);
      process.exit(1);
    });
}

module.exports = { redistributeAllSpellingWords };