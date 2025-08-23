const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkInvalidSpellingWords() {
  console.log('=== CHECKING FOR INVALID SPELLING WORDS ===\n');
  
  try {
    // Get words without definitions
    const { data: wordsNoDefinition, error: error1 } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty')
      .is('definition', null)
      .order('word');
    
    if (error1) {
      console.error('Error fetching words without definitions:', error1);
      return;
    }
    
    console.log(`Found ${wordsNoDefinition?.length || 0} words without definitions:\n`);
    
    // Categorize potentially invalid words
    const suspiciousPatterns = {
      concatenated: [],
      withNumbers: [],
      tooShort: [],
      nonAlpha: [],
      allCaps: [],
      other: []
    };
    
    wordsNoDefinition?.forEach(({ word, source_difficulty }) => {
      // Check for concatenated words (unusually long or mixed case in middle)
      if (word.length > 20) {
        suspiciousPatterns.concatenated.push({ word, source_difficulty });
      }
      // Check for numbers
      else if (/\d/.test(word)) {
        suspiciousPatterns.withNumbers.push({ word, source_difficulty });
      }
      // Check for very short words (1-2 chars might be invalid)
      else if (word.length <= 2 && !['a', 'i', 'am', 'an', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'if', 'in', 'is', 'it', 'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'us', 'we'].includes(word.toLowerCase())) {
        suspiciousPatterns.tooShort.push({ word, source_difficulty });
      }
      // Check for non-alphabetic characters (except hyphens and apostrophes)
      else if (/[^a-zA-Z\-']/.test(word)) {
        suspiciousPatterns.nonAlpha.push({ word, source_difficulty });
      }
      // Check for all caps (might be acronyms)
      else if (word === word.toUpperCase() && word.length > 2) {
        suspiciousPatterns.allCaps.push({ word, source_difficulty });
      }
      else {
        suspiciousPatterns.other.push({ word, source_difficulty });
      }
    });
    
    // Print categorized results
    console.log('📊 SUSPICIOUS PATTERNS FOUND:\n');
    
    if (suspiciousPatterns.concatenated.length > 0) {
      console.log(`🔗 Potentially Concatenated (${suspiciousPatterns.concatenated.length} words):`);
      suspiciousPatterns.concatenated.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (difficulty: ${source_difficulty})`);
      });
      console.log();
    }
    
    if (suspiciousPatterns.withNumbers.length > 0) {
      console.log(`🔢 Contains Numbers (${suspiciousPatterns.withNumbers.length} words):`);
      suspiciousPatterns.withNumbers.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (difficulty: ${source_difficulty})`);
      });
      console.log();
    }
    
    if (suspiciousPatterns.tooShort.length > 0) {
      console.log(`📏 Too Short (${suspiciousPatterns.tooShort.length} words):`);
      suspiciousPatterns.tooShort.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (difficulty: ${source_difficulty})`);
      });
      console.log();
    }
    
    if (suspiciousPatterns.nonAlpha.length > 0) {
      console.log(`❓ Non-Alphabetic Characters (${suspiciousPatterns.nonAlpha.length} words):`);
      suspiciousPatterns.nonAlpha.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (difficulty: ${source_difficulty})`);
      });
      console.log();
    }
    
    if (suspiciousPatterns.allCaps.length > 0) {
      console.log(`🔠 All Caps (${suspiciousPatterns.allCaps.length} words):`);
      suspiciousPatterns.allCaps.forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (difficulty: ${source_difficulty})`);
      });
      console.log();
    }
    
    if (suspiciousPatterns.other.length > 0) {
      console.log(`📝 Other Words Without Definitions (${suspiciousPatterns.other.length} words):`);
      console.log('First 20:');
      suspiciousPatterns.other.slice(0, 20).forEach(({ word, source_difficulty }) => {
        console.log(`  - ${word} (difficulty: ${source_difficulty})`);
      });
      if (suspiciousPatterns.other.length > 20) {
        console.log(`  ... and ${suspiciousPatterns.other.length - 20} more`);
      }
      console.log();
    }
    
    // Summary
    console.log('=== SUMMARY ===');
    console.log(`Total words without definitions: ${wordsNoDefinition?.length || 0}`);
    console.log(`- Potentially concatenated: ${suspiciousPatterns.concatenated.length}`);
    console.log(`- Contains numbers: ${suspiciousPatterns.withNumbers.length}`);
    console.log(`- Too short: ${suspiciousPatterns.tooShort.length}`);
    console.log(`- Non-alphabetic chars: ${suspiciousPatterns.nonAlpha.length}`);
    console.log(`- All caps: ${suspiciousPatterns.allCaps.length}`);
    console.log(`- Other valid words: ${suspiciousPatterns.other.length}`);
    
    // Save the suspicious words to a file for review
    const fs = require('fs');
    const invalidWords = {
      timestamp: new Date().toISOString(),
      totalWithoutDefinitions: wordsNoDefinition?.length || 0,
      categories: suspiciousPatterns
    };
    
    const filename = `scripts/invalid_spelling_words_${Date.now()}.json`;
    fs.writeFileSync(filename, JSON.stringify(invalidWords, null, 2));
    console.log(`\n💾 Saved detailed results to: ${filename}`);
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkInvalidSpellingWords().catch(console.error);