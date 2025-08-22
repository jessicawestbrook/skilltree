const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function standardizePronunciationFormat() {
  try {
    console.log('🔧 PRONUNCIATION FORMAT STANDARDIZATION PROJECT');
    
    // Find pronunciations with various formatting inconsistencies
    const { data: wordsWithParentheses, error } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide')
      .not('pronunciation_guide', 'is', null)
      .or('pronunciation_guide.ilike.%(%,pronunciation_guide.ilike.%IPA%,pronunciation_guide.ilike.%emphasis%,pronunciation_guide.ilike.%stress%')
      .limit(100);
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${wordsWithParentheses.length} words with formatting that could be standardized`);
    
    let standardized = 0;
    let processed = 0;
    
    for (const wordData of wordsWithParentheses) {
      const word = wordData.word;
      const originalPronunciation = wordData.pronunciation_guide;
      
      // Standardize pronunciation format
      let cleanedPronunciation = originalPronunciation;
      
      // Remove common parenthetical notes
      cleanedPronunciation = cleanedPronunciation
        .replace(/\s*\(emphasis on .*?\)/gi, '')
        .replace(/\s*\(stress on .*?\)/gi, '')
        .replace(/\s*\(.*?syllable\)/gi, '')
        .replace(/\s*\([^)]*IPA[^)]*\)/gi, '')
        .replace(/\s*-\([^)]+\)/g, '') // Remove trailing IPA notations like -(kɒLtAn)
        .replace(/\s*\([^)]*ɒ[^)]*\)/gi, '') // Remove IPA symbols
        .replace(/\s*\([^)]*ɪ[^)]*\)/gi, '') // Remove more IPA symbols
        .replace(/\s*\([^)]*ʌ[^)]*\)/gi, '') // Remove more IPA symbols
        .trim();
      
      // Clean up multiple spaces and normalize formatting
      cleanedPronunciation = cleanedPronunciation
        .replace(/\s+/g, ' ')
        .replace(/\s*-\s*/g, '-')
        .trim();
      
      // Only update if we actually made changes
      if (cleanedPronunciation !== originalPronunciation && cleanedPronunciation.length > 0) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ pronunciation_guide: cleanedPronunciation })
          .eq('id', wordData.id);
          
        if (updateError) {
          console.error(`Failed to update ${word}:`, updateError);
        } else {
          console.log(`✓ Standardized ${word}:`);
          console.log(`  Before: ${originalPronunciation}`);
          console.log(`  After:  ${cleanedPronunciation}`);
          standardized++;
        }
        
        // Small delay to avoid rate limits
        await new Promise(resolve => setTimeout(resolve, 30));
      }
      
      processed++;
    }
    
    console.log(`\\n📊 STANDARDIZATION RESULTS:`);
    console.log(`Processed: ${processed} words`);
    console.log(`Standardized: ${standardized} pronunciations`);
    console.log(`Format consistency improved for spelling bee application`);
    
    // Check overall pronunciation quality after cleanup
    const { count: totalCount } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });
      
    const { count: withPronunciation } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .not('pronunciation_guide', 'is', null);
      
    const progress = ((withPronunciation/totalCount)*100).toFixed(1);
    console.log(`\\nMaintained pronunciation coverage: ${withPronunciation}/${totalCount} (${progress}%)`);
    
    console.log('\\n✅ Pronunciation format standardization completed!');
    console.log('Database is now more consistent for spelling bee application use.');
    
  } catch (error) {
    console.error('Pronunciation standardization failed:', error);
  }
}

standardizePronunciationFormat();