const script = require('./fill_missing_pronunciations.js');
const fs = require('fs');

async function runFullPronunciationUpdate() {
  const startTime = Date.now();
  console.log('Starting full pronunciation update process...');
  console.log(`Started at: ${new Date().toISOString()}`);
  
  try {
    // Get all missing pronunciations
    const missingWords = await script.getMissingPronunciations();
    console.log(`Total words missing pronunciations: ${missingWords.length}`);
    
    // Filter out malformed words
    const validWords = missingWords.filter(item => {
      const word = item.word.toLowerCase().trim();
      
      // Skip words that are clearly malformed
      if (word.length < 2 || word.length > 50) return false;
      if (/\d/.test(word)) return false; // Contains numbers
      if (/[^a-zA-Z'-]/.test(word)) return false; // Contains invalid characters
      
      // Check for obvious combined words (heuristic)
      const lowerWord = word.toLowerCase();
      if (lowerWord.includes('the') && lowerWord !== 'the' && !lowerWord.endsWith('the')) return false;
      if (lowerWord.includes('noun') && lowerWord !== 'noun' && !lowerWord.endsWith('noun')) return false;
      if (lowerWord.includes('verb') && lowerWord !== 'verb' && !lowerWord.endsWith('verb')) return false;
      
      return true;
    });
    
    const invalidWords = missingWords.filter(item => {
      const word = item.word.toLowerCase().trim();
      return !(validWords.find(v => v.id === item.id));
    });
    
    console.log(`Valid words to process: ${validWords.length}`);
    console.log(`Invalid words filtered out: ${invalidWords.length}`);
    
    // Save list of invalid words
    if (invalidWords.length > 0) {
      fs.writeFileSync(
        'scripts/invalid_words_filtered.json',
        JSON.stringify(invalidWords.map(item => ({ id: item.id, word: item.word })), null, 2)
      );
      console.log('Invalid words saved to scripts/invalid_words_filtered.json');
    }
    
    // Process in batches
    const batchSize = 20;
    const totalBatches = Math.ceil(validWords.length / batchSize);
    let processedCount = 0;
    let successCount = 0;
    let failureCount = 0;
    
    console.log(`\\nProcessing ${validWords.length} words in ${totalBatches} batches of ${batchSize}...\\n`);
    
    for (let batchIndex = 0; batchIndex < totalBatches; batchIndex++) {
      const batchStart = batchIndex * batchSize;
      const batchEnd = Math.min(batchStart + batchSize, validWords.length);
      const batch = validWords.slice(batchStart, batchEnd);
      
      console.log(`\\n--- Batch ${batchIndex + 1}/${totalBatches} (words ${batchStart + 1}-${batchEnd}) ---`);
      
      const updates = [];
      
      for (let i = 0; i < batch.length; i++) {
        const { id, word } = batch[i];
        processedCount++;
        
        try {
          const pronunciation = await script.getPhoneticFromClaude(word);
          updates.push({ id, word, pronunciation_guide: pronunciation });
          successCount++;
          
          console.log(`${processedCount}/${validWords.length}: ${word} -> ${pronunciation}`);
          
        } catch (error) {
          failureCount++;
          console.log(`${processedCount}/${validWords.length}: FAILED ${word} - ${error.message}`);
        }
        
        // Rate limiting - pause between Claude API calls
        if (i < batch.length - 1) {
          await new Promise(resolve => setTimeout(resolve, 1500));
        }
      }
      
      // Update database with this batch
      if (updates.length > 0) {
        try {
          for (const update of updates) {
            const { createClient } = require('@supabase/supabase-js');
            require('dotenv').config({ path: '.env.local' });

            const supabase = createClient(
              process.env.REACT_APP_SUPABASE_URL,
              process.env.REACT_APP_SUPABASE_ANON_KEY
            );
            
            const { error } = await supabase
              .from('spelling_words')
              .update({ pronunciation_guide: update.pronunciation_guide })
              .eq('id', update.id);
            
            if (error) {
              console.error(`Database update error for ${update.word}:`, error);
            }
          }
          
          console.log(`✓ Updated ${updates.length} pronunciations in database`);
          
        } catch (error) {
          console.error('Batch database update failed:', error);
        }
      }
      
      // Save progress after each batch
      const progress = {
        timestamp: new Date().toISOString(),
        batchIndex: batchIndex + 1,
        totalBatches,
        processed: processedCount,
        total: validWords.length,
        successful: successCount,
        failed: failureCount,
        progress_percentage: Math.round((processedCount / validWords.length) * 100)
      };
      
      fs.writeFileSync(
        `scripts/pronunciation_progress_${Date.now()}.json`,
        JSON.stringify(progress, null, 2)
      );
      
      console.log(`Progress: ${processedCount}/${validWords.length} (${progress.progress_percentage}%) | Success: ${successCount} | Failed: ${failureCount}`);
      
      // Longer pause between batches
      if (batchIndex < totalBatches - 1) {
        console.log('Pausing between batches...');
        await new Promise(resolve => setTimeout(resolve, 3000));
      }
    }
    
    const endTime = Date.now();
    const duration = Math.round((endTime - startTime) / 1000);
    
    console.log('\\n=== PRONUNCIATION UPDATE COMPLETE ===');
    console.log(`Total processing time: ${duration} seconds`);
    console.log(`Total words processed: ${processedCount}`);
    console.log(`Successful pronunciations: ${successCount}`);
    console.log(`Failed pronunciations: ${failureCount}`);
    console.log(`Success rate: ${Math.round((successCount / processedCount) * 100)}%`);
    console.log(`Invalid words filtered: ${invalidWords.length}`);
    
    // Final verification
    console.log('\\nRunning final verification...');
    const remaining = await script.getMissingPronunciations();
    console.log(`Remaining words without pronunciations: ${remaining.length}`);
    
    if (remaining.length > 0) {
      console.log('First 10 remaining words:');
      remaining.slice(0, 10).forEach(item => console.log(`- ${item.word}`));
    }
    
  } catch (error) {
    console.error('Full update process failed:', error);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  runFullPronunciationUpdate()
    .then(() => {
      console.log('\\nPronunciation update process completed successfully!');
      process.exit(0);
    })
    .catch(error => {
      console.error('Process failed:', error);
      process.exit(1);
    });
}

module.exports = { runFullPronunciationUpdate };