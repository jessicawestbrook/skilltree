const { createClient } = require('@supabase/supabase-js');
const { getPhoneticFromClaude } = require('./fill_missing_pronunciations.js');
const { LEGITIMATE_WORDS } = require('./review_filtered_words.js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

// Use SERVICE_ROLE_KEY for write operations
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function restoreLegitimateWords() {
  const startTime = Date.now();
  console.log('🔄 RESTORING PRONUNCIATIONS FOR LEGITIMATE WORDS\n');
  console.log(`Started at: ${new Date().toISOString()}`);
  
  try {
    // Get the filtered words that are actually legitimate
    const { data: filteredWords, error: fetchError } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide')
      .in('word', LEGITIMATE_WORDS);
    
    if (fetchError) {
      throw fetchError;
    }
    
    console.log(`Found ${filteredWords.length} legitimate words to restore pronunciations for:\n`);
    
    let processedCount = 0;
    let successCount = 0;
    let failureCount = 0;
    const results = [];
    
    for (const wordItem of filteredWords) {
      const { id, word } = wordItem;
      processedCount++;
      
      try {
        console.log(`${processedCount}/${filteredWords.length}: Processing "${word}"...`);
        
        // Generate pronunciation using Claude API
        const pronunciation = await getPhoneticFromClaude(word);
        
        if (!pronunciation) {
          throw new Error('Claude API returned empty pronunciation');
        }
        
        console.log(`  Generated: ${pronunciation}`);
        
        // Update database
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
        
        results.push({
          word,
          pronunciation,
          status: 'success'
        });
        
      } catch (error) {
        failureCount++;
        console.log(`  ❌ FAILED: ${error.message}`);
        
        results.push({
          word,
          pronunciation: null,
          status: 'failed',
          error: error.message
        });
      }
      
      // Pause between requests for API stability
      if (processedCount < filteredWords.length) {
        console.log(`  Pausing...`);
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    }
    
    const endTime = Date.now();
    const duration = Math.round((endTime - startTime) / 1000);
    
    console.log('\n=== RESTORATION COMPLETE ===');
    console.log(`Total processing time: ${duration} seconds`);
    console.log(`Words processed: ${processedCount}`);
    console.log(`Successful pronunciations: ${successCount}`);
    console.log(`Failed pronunciations: ${failureCount}`);
    console.log(`Success rate: ${Math.round((successCount / processedCount) * 100)}%`);
    
    // Save detailed results
    const report = {
      timestamp: new Date().toISOString(),
      duration_seconds: duration,
      summary: {
        processed: processedCount,
        successful: successCount,
        failed: failureCount,
        success_rate: Math.round((successCount / processedCount) * 100)
      },
      results
    };
    
    fs.writeFileSync('scripts/legitimate_words_restoration_report.json', JSON.stringify(report, null, 2));
    console.log('\n📄 Detailed report saved to scripts/legitimate_words_restoration_report.json');
    
    // Final verification
    console.log('\n🔍 Running final verification...');
    const { data: verifyWords, error: verifyError } = await supabase
      .from('spelling_words')
      .select('word, pronunciation_guide')
      .in('word', LEGITIMATE_WORDS);
    
    if (!verifyError) {
      const withPronunciations = verifyWords.filter(w => w.pronunciation_guide && w.pronunciation_guide.trim() !== '');
      console.log(`\n📈 VERIFICATION RESULTS:`);
      console.log(`   Words with pronunciations: ${withPronunciations.length}/${verifyWords.length}`);
      
      if (withPronunciations.length === verifyWords.length) {
        console.log('\n🎉 SUCCESS: ALL LEGITIMATE WORDS NOW HAVE PRONUNCIATIONS!');
      } else {
        const missing = verifyWords.filter(w => !w.pronunciation_guide || w.pronunciation_guide.trim() === '');
        console.log(`\n⚠️  Still missing pronunciations for: ${missing.map(w => w.word).join(', ')}`);
      }
    }
    
    return report;
    
  } catch (error) {
    console.error('Restoration process failed:', error);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  restoreLegitimateWords()
    .then(() => {
      console.log('\n✅ Legitimate word pronunciation restoration completed!');
      process.exit(0);
    })
    .catch(error => {
      console.error('Process failed:', error);
      process.exit(1);
    });
}

module.exports = { restoreLegitimateWords };