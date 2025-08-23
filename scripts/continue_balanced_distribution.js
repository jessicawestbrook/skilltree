const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTI0MTMzNSwiZXhwIjoyMDcwODE3MzM1fQ.x-QbhMeO7HzECupWqq_XuHXeTbQmQwvVKasC61jb7Ws';

const supabase = createClient(supabaseUrl, supabaseKey);

async function continueBalancedDistribution() {
  console.log('Continuing balanced distribution to reach targets...');
  console.log('Target: 40% One Bee (3549), 35% Two Bee (3105), 25% Three Bee (2218)');
  
  try {
    // Check current distribution
    const currentCounts = { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 };
    
    for (let batch = 0; batch < 9; batch++) {
      const start = batch * 1000;
      const end = start + 999;
      
      const { data: words } = await supabase
        .from('spelling_words')
        .select('source_difficulty')
        .range(start, end);
      
      words?.forEach(w => {
        if (currentCounts.hasOwnProperty(w.source_difficulty)) {
          currentCounts[w.source_difficulty]++;
        }
      });
    }
    
    console.log('\\nCurrent distribution:');
    Object.entries(currentCounts).forEach(([level, count]) => {
      console.log('  ' + level + ': ' + count + ' (' + (count/8873*100).toFixed(1) + '%)');
    });
    
    const targets = { 'One Bee': 3549, 'Two Bee': 3105, 'Three Bee': 2218 };
    const needed = {};
    
    console.log('\\nAdjustments needed:');
    Object.entries(targets).forEach(([level, target]) => {
      const current = currentCounts[level];
      needed[level] = target - current;
      const direction = needed[level] > 0 ? 'need +' : 'excess ';
      console.log('  ' + level + ': ' + direction + Math.abs(needed[level]) + ' words');
    });
    
    // Strategy: Move excess One Bee words to Two Bee and Three Bee
    if (needed['One Bee'] < 0 && (needed['Two Bee'] > 0 || needed['Three Bee'] > 0)) {
      console.log('\\nMoving excess One Bee words to Two Bee and Three Bee...');
      
      // Get One Bee words that can be moved (prioritize longer/harder words)
      const { data: oneBeeWords } = await supabase
        .from('spelling_words')
        .select('id, word, ai_spelling_difficulty_level, spelling_difficulty_level')
        .eq('source_difficulty', 'One Bee')
        .limit(Math.abs(needed['One Bee']));
      
      if (oneBeeWords && oneBeeWords.length > 0) {
        // Sort by difficulty (move harder One Bee words first)
        oneBeeWords.sort((a, b) => {
          const aLevel = a.ai_spelling_difficulty_level || a.spelling_difficulty_level || 1;
          const bLevel = b.ai_spelling_difficulty_level || b.spelling_difficulty_level || 1;
          return bLevel - aLevel; // Descending order
        });
        
        const updates = [];
        let twoBeeToAdd = Math.min(needed['Two Bee'], Math.floor(oneBeeWords.length * 0.6));
        let threeBeeToAdd = Math.min(needed['Three Bee'], oneBeeWords.length - twoBeeToAdd);
        
        // Assign to Two Bee
        for (let i = 0; i < twoBeeToAdd; i++) {
          updates.push({
            id: oneBeeWords[i].id,
            word: oneBeeWords[i].word,
            newDifficulty: 'Two Bee'
          });
        }
        
        // Assign to Three Bee  
        for (let i = twoBeeToAdd; i < twoBeeToAdd + threeBeeToAdd; i++) {
          updates.push({
            id: oneBeeWords[i].id,
            word: oneBeeWords[i].word,
            newDifficulty: 'Three Bee'
          });
        }
        
        console.log('Planned moves:');
        console.log('  One Bee → Two Bee: ' + twoBeeToAdd + ' words');
        console.log('  One Bee → Three Bee: ' + threeBeeToAdd + ' words');
        
        // Apply updates
        console.log('\\nApplying updates...');
        for (let i = 0; i < updates.length; i += 50) {
          const batch = updates.slice(i, i + 50);
          
          for (const update of batch) {
            const { error } = await supabase
              .from('spelling_words')
              .update({ source_difficulty: update.newDifficulty })
              .eq('id', update.id);
            
            if (error) {
              console.error('Error updating ' + update.word + ':', error);
            }
          }
          
          console.log('Updated batch ' + (Math.floor(i/50) + 1) + '/' + Math.ceil(updates.length/50));
          await new Promise(resolve => setTimeout(resolve, 50));
        }
        
        // Verify final distribution
        const finalCounts = { 'One Bee': 0, 'Two Bee': 0, 'Three Bee': 0 };
        
        for (let batch = 0; batch < 9; batch++) {
          const start = batch * 1000;
          const end = start + 999;
          
          const { data: words } = await supabase
            .from('spelling_words')
            .select('source_difficulty')
            .range(start, end);
          
          words?.forEach(w => {
            if (finalCounts.hasOwnProperty(w.source_difficulty)) {
              finalCounts[w.source_difficulty]++;
            }
          });
        }
        
        console.log('\\n✅ Final distribution:');
        Object.entries(finalCounts).forEach(([level, count]) => {
          console.log('  ' + level + ': ' + count + ' (' + (count/8873*100).toFixed(1) + '%)');
        });
      }
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

continueBalancedDistribution()
  .then(() => {
    console.log('\\nDistribution balancing completed');
    process.exit(0);
  })
  .catch(error => {
    console.error('Script failed:', error);
    process.exit(1);
  });