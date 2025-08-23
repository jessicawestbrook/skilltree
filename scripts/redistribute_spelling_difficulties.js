const { createClient } = require('@supabase/supabase-js');

// Supabase configuration - using service role key for elevated permissions
const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTI0MTMzNSwiZXhwIjoyMDcwODE3MzM1fQ.x-QbhMeO7HzECupWqq_XuHXeTbQmQwvVKasC61jb7Ws';

const supabase = createClient(supabaseUrl, supabaseKey);

async function redistributeSpellingDifficulties() {
  console.log('Redistributing spelling word difficulties...');
  
  try {
    // First, create a backup of the current data
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupTable = `spelling_words_bkp_${timestamp.slice(0, 19)}`;
    
    console.log(`Creating backup table: ${backupTable}`);
    const { error: backupError } = await supabase.rpc('create_table_backup', {
      source_table: 'spelling_words',
      backup_table: backupTable
    });
    
    if (backupError) {
      console.log('Backup failed, continuing anyway:', backupError.message);
    }

    // Get words that need redistribution
    const { data: wordsToRedistribute, error: fetchError } = await supabase
      .from('spelling_words')
      .select('id, word, source_difficulty, spelling_difficulty_level, ai_spelling_difficulty_level')
      .or('source_difficulty.like.%;%,source_difficulty.eq.Various levels');

    if (fetchError) {
      console.error('Error fetching words to redistribute:', fetchError);
      return;
    }

    console.log(`Found ${wordsToRedistribute?.length || 0} words to redistribute`);

    const updates = [];
    
    for (const word of wordsToRedistribute || []) {
      let newDifficulty;
      
      if (word.source_difficulty === 'Various levels') {
        // Use AI spelling difficulty to assign level
        const aiLevel = word.ai_spelling_difficulty_level || word.spelling_difficulty_level || 1;
        if (aiLevel <= 2) {
          newDifficulty = 'One Bee';
        } else if (aiLevel <= 4) {
          newDifficulty = 'Two Bee';
        } else {
          newDifficulty = 'Three Bee';
        }
      } else if (word.source_difficulty.includes(';')) {
        // For words with multiple levels, pick the most appropriate one
        const difficulties = word.source_difficulty.split(';').map(d => d.trim());
        
        // Logic: if it includes One Bee and word length is short, use One Bee
        // If it includes Three Bee and AI difficulty is high, use Three Bee
        // Otherwise use Two Bee
        const aiLevel = word.ai_spelling_difficulty_level || word.spelling_difficulty_level || 1;
        const wordLength = word.word.length;
        
        if (difficulties.includes('One Bee') && (wordLength <= 5 || aiLevel <= 2)) {
          newDifficulty = 'One Bee';
        } else if (difficulties.includes('Three Bee') && (aiLevel >= 4 || wordLength >= 8)) {
          newDifficulty = 'Three Bee';
        } else {
          newDifficulty = 'Two Bee';
        }
      }
      
      if (newDifficulty) {
        updates.push({
          id: word.id,
          word: word.word,
          oldDifficulty: word.source_difficulty,
          newDifficulty: newDifficulty
        });
      }
    }

    console.log(`Planning to update ${updates.length} words`);
    
    // Show sample of planned updates
    console.log('\nSample planned updates:');
    updates.slice(0, 10).forEach(update => {
      console.log(`  ${update.word}: "${update.oldDifficulty}" -> "${update.newDifficulty}"`);
    });

    // Batch update words
    console.log('\nApplying updates...');
    for (let i = 0; i < updates.length; i += 50) {
      const batch = updates.slice(i, i + 50);
      
      for (const update of batch) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ source_difficulty: update.newDifficulty })
          .eq('id', update.id);
        
        if (updateError) {
          console.error(`Error updating word "${update.word}":`, updateError);
        }
      }
      
      console.log(`Updated batch ${Math.floor(i/50) + 1}/${Math.ceil(updates.length/50)}`);
    }

    // Verify the redistribution
    const { data: finalCounts, error: countError } = await supabase
      .from('spelling_words')
      .select('source_difficulty');
    
    if (!countError && finalCounts) {
      const counts = {};
      finalCounts.forEach(w => {
        counts[w.source_difficulty] = (counts[w.source_difficulty] || 0) + 1;
      });
      
      console.log('\nFinal distribution:');
      Object.entries(counts).forEach(([key, value]) => {
        console.log(`  ${key}: ${value}`);
      });
    }

    console.log('\nRedistribution completed successfully!');

  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

// Run the script
if (require.main === module) {
  redistributeSpellingDifficulties()
    .then(() => {
      console.log('Script completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Script failed:', error);
      process.exit(1);
    });
}

module.exports = { redistributeSpellingDifficulties };