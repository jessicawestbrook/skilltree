const script = require('./fill_missing_pronunciations.js');
const cleaner = require('./clean_and_separate_spelling_words.js');
const fs = require('fs');

async function resumePronunciationUpdate() {
  const startTime = Date.now();
  console.log('Resuming pronunciation updates for remaining valid words...');
  console.log(`Started at: ${new Date().toISOString()}`);
  
  try {
    const { createClient } = require('@supabase/supabase-js');
    require('dotenv').config({ path: '.env.local' });

    // Use SERVICE_ROLE_KEY for write operations
    const supabase = createClient(
      process.env.REACT_APP_SUPABASE_URL,
      process.env.SUPABASE_SERVICE_ROLE_KEY
    );
    
    // Get all missing pronunciations
    const missingWords = await script.getMissingPronunciations();
    console.log(`Total words missing pronunciations: ${missingWords.length}`);
    
    // Filter to only valid spelling words that don't have pronunciations
    const validWords = [];
    const invalidWords = [];
    
    for (const item of missingWords) {
      // Skip words already marked as invalid
      if (item.pronunciation_guide && item.pronunciation_guide.startsWith('INVALID_')) {
        continue;
      }
      
      const validation = cleaner.isValidSpellingWord(item.word);
      if (validation.valid) {
        validWords.push(item);
      } else {
        invalidWords.push({ ...item, reason: validation.reason });
      }
    }
    
    console.log(`Valid words still needing pronunciations: ${validWords.length}`);
    console.log(`Invalid words to skip: ${invalidWords.length}`);
    
    if (validWords.length === 0) {
      console.log('\\n🎉 ALL VALID WORDS ALREADY HAVE PRONUNCIATIONS!');
      return;
    }
    
    // Process valid words in smaller batches with better error handling
    const batchSize = 10; // Smaller batch size
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
      
      for (let i = 0; i < batch.length; i++) {
        const { id, word } = batch[i];
        processedCount++;
        
        try {
          console.log(`${processedCount}/${validWords.length}: Processing "${word}"...`);
          
          // Generate pronunciation
          const pronunciation = await script.getPhoneticFromClaude(word);
          console.log(`  Generated: ${pronunciation}`);
          
          // Update database immediately
          const { error: updateError } = await supabase
            .from('spelling_words')
            .update({ 
              pronunciation_guide: pronunciation,
              updated_at: new Date().toISOString()
            })
            .eq('id', id);
          
          if (updateError) {
            throw new Error(`Database update failed: ${updateError.message}`);
          }
          
          console.log(`  ✅ Updated in database`);
          successCount++;
          
        } catch (error) {
          failureCount++;
          console.log(`  ❌ FAILED: ${error.message}`);
        }
        
        // Longer pause between requests for stability
        if (i < batch.length - 1 || batchIndex < totalBatches - 1) {
          console.log(`  Pausing...`);
          await new Promise(resolve => setTimeout(resolve, 2000));
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
        `scripts/resume_pronunciation_progress_${Date.now()}.json`,
        JSON.stringify(progress, null, 2)
      );
      
      console.log(`\\n📊 Batch ${batchIndex + 1} complete:`);
      console.log(`   Progress: ${processedCount}/${validWords.length} (${progress.progress_percentage}%)`);
      console.log(`   Success: ${successCount} | Failed: ${failureCount}`);
      console.log(`   Success rate: ${Math.round((successCount / processedCount) * 100)}%`);
      
      // Longer pause between batches
      if (batchIndex < totalBatches - 1) {
        console.log('\\n⏳ Long pause between batches...');
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
    }
    
    const endTime = Date.now();
    const duration = Math.round((endTime - startTime) / 1000);
    
    console.log('\\n=== PRONUNCIATION UPDATE RESUME COMPLETE ===');
    console.log(`Total processing time: ${duration} seconds (${Math.round(duration/60)} minutes)`);
    console.log(`Words processed: ${processedCount}`);
    console.log(`Successful pronunciations: ${successCount}`);
    console.log(`Failed pronunciations: ${failureCount}`);
    console.log(`Final success rate: ${Math.round((successCount / processedCount) * 100)}%`);
    
    // Final verification
    console.log('\\n🔍 Running final verification...');
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
    
    console.log(`\\n📈 FINAL RESULTS:`);
    console.log(`   Remaining valid words without pronunciations: ${remainingValid.length}`);
    
    if (remainingValid.length === 0) {
      console.log('\\n🎉 SUCCESS: ALL VALID SPELLING WORDS NOW HAVE PRONUNCIATIONS!');
    } else {
      console.log(`\\n⚠️  Still need to process ${remainingValid.length} words`);
      console.log('First 10 remaining words:');
      remainingValid.slice(0, 10).forEach(item => console.log(`   - ${item.word}`));
    }
    
  } catch (error) {
    console.error('Resume process failed:', error);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  resumePronunciationUpdate()
    .then(() => {
      console.log('\\nResume pronunciation update process completed!');
      process.exit(0);
    })
    .catch(error => {
      console.error('Process failed:', error);
      process.exit(1);
    });
}

module.exports = { resumePronunciationUpdate };