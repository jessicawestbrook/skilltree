const script = require('./fill_missing_pronunciations.js');
const cleaner = require('./clean_and_separate_spelling_words.js');
const fs = require('fs');

async function runValidPronunciationUpdate() {
  const startTime = Date.now();
  console.log('Starting pronunciation updates for VALID words only...');
  console.log(`Started at: ${new Date().toISOString()}`);
  
  try {
    // Get all missing pronunciations
    const missingWords = await script.getMissingPronunciations();
    console.log(`Total words missing pronunciations: ${missingWords.length}`);
    
    // Filter to only valid spelling words
    const validWords = [];
    const invalidWords = [];
    
    for (const item of missingWords) {
      // Skip words already marked as invalid
      if (item.pronunciation_guide && item.pronunciation_guide.startsWith('INVALID_')) {
        invalidWords.push({ ...item, reason: 'already-marked-invalid' });
        continue;
      }
      
      const validation = cleaner.isValidSpellingWord(item.word);
      if (validation.valid) {
        validWords.push(item);
      } else {
        invalidWords.push({ ...item, reason: validation.reason });
      }
    }
    
    console.log(`Valid spelling words to process: ${validWords.length}`);
    console.log(`Invalid words skipped: ${invalidWords.length}`);
    
    if (invalidWords.length > 0) {
      console.log('\\nInvalid words breakdown:');
      const reasonCounts = {};
      invalidWords.forEach(item => {
        reasonCounts[item.reason] = (reasonCounts[item.reason] || 0) + 1;
      });
      Object.entries(reasonCounts).forEach(([reason, count]) => {
        console.log(`- ${reason}: ${count} words`);
      });
    }
    
    // Save list of invalid words
    if (invalidWords.length > 0) {
      fs.writeFileSync(
        'scripts/skipped_invalid_words.json',
        JSON.stringify(invalidWords.map(item => ({ 
          id: item.id, 
          word: item.word, 
          reason: item.reason 
        })), null, 2)
      );
      console.log('\\nSkipped invalid words saved to scripts/skipped_invalid_words.json');
    }
    
    if (validWords.length === 0) {
      console.log('\\nNo valid words need pronunciation updates!');
      return;
    }
    
    // Process valid words in batches
    const batchSize = 20;
    const totalBatches = Math.ceil(validWords.length / batchSize);
    let processedCount = 0;
    let successCount = 0;
    let failureCount = 0;
    
    console.log(`\\nProcessing ${validWords.length} VALID words in ${totalBatches} batches of ${batchSize}...\\n`);
    
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
        progress_percentage: Math.round((processedCount / validWords.length) * 100),
        invalid_words_skipped: invalidWords.length
      };
      
      fs.writeFileSync(
        `scripts/valid_pronunciation_progress_${Date.now()}.json`,
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
    
    console.log('\\n=== VALID PRONUNCIATION UPDATE COMPLETE ===');
    console.log(`Total processing time: ${duration} seconds`);
    console.log(`Valid words processed: ${processedCount}`);
    console.log(`Successful pronunciations: ${successCount}`);
    console.log(`Failed pronunciations: ${failureCount}`);
    console.log(`Success rate: ${Math.round((successCount / processedCount) * 100)}%`);
    console.log(`Invalid words skipped: ${invalidWords.length}`);
    
    // Final verification
    console.log('\\nRunning final verification...');
    
    // Count remaining valid words without pronunciations
    const remainingWords = await script.getMissingPronunciations();
    const remainingValid = [];
    
    for (const item of remainingWords) {
      if (item.pronunciation_guide && item.pronunciation_guide.startsWith('INVALID_')) {
        continue;
      }
      const validation = cleaner.isValidSpellingWord(item.word);
      if (validation.valid) {
        remainingValid.push(item);
      }
    }
    
    console.log(`Remaining VALID words without pronunciations: ${remainingValid.length}`);
    
    if (remainingValid.length > 0) {
      console.log('First 10 remaining valid words:');
      remainingValid.slice(0, 10).forEach(item => console.log(`- ${item.word}`));
    } else {
      console.log('🎉 ALL VALID WORDS NOW HAVE PRONUNCIATIONS!');
    }
    
  } catch (error) {
    console.error('Valid pronunciation update process failed:', error);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  runValidPronunciationUpdate()
    .then(() => {
      console.log('\\nValid pronunciation update process completed successfully!');
      process.exit(0);
    })
    .catch(error => {
      console.error('Process failed:', error);
      process.exit(1);
    });
}

module.exports = { runValidPronunciationUpdate };