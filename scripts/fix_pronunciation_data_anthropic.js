const { createClient } = require('@supabase/supabase-js');
const Anthropic = require('@anthropic-ai/sdk');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const BATCH_SIZE = 5;
const DELAY_BETWEEN_REQUESTS = 2000; // 2 seconds

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function categorizeWord(word) {
  // Check if it's a combined word (multiple words mashed together)
  if (word.length > 15 && /[a-z][A-Z]/.test(word)) {
    return 'combined';
  }
  
  // Check for obvious combined patterns
  const combinedPatterns = [
    /noun$/, /the$/, /viscount$/, /pulse$/, /charitable$/, /aerials$/,
    /remorseful$/, /jungian$/, /reveille$/, /retina$/, /arithmetic$/,
    /ancestors$/, /domesticity$/, /tarry$/, /corner$/, /interim$/,
    /dishevel$/, /sousaphone$/, /limbering$/
  ];
  
  if (combinedPatterns.some(pattern => pattern.test(word))) {
    return 'combined';
  }
  
  // Check for special characters
  if (/[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]/.test(word)) {
    return 'special_chars';
  }
  
  // Check for interjections or non-words
  if (word === 'shhh' || word.length < 2) {
    return 'non_word';
  }
  
  // Everything else is legitimate
  return 'legitimate';
}

function attemptWordSeparation(combinedWord) {
  const separationPatterns = [
    { pattern: /(.+)noun$/, replacement: '$1' },
    { pattern: /(.+)the$/, replacement: '$1' },
    { pattern: /(.+)viscount$/, replacement: '$1' },
    { pattern: /(.+)pulse$/, replacement: '$1' },
    { pattern: /(.+)charitable$/, replacement: '$1' },
    { pattern: /(.+)aerials$/, replacement: '$1' },
    { pattern: /(.+)remorseful$/, replacement: '$1' },
    { pattern: /(.+)jungian$/, replacement: '$1' },
    { pattern: /(.+)reveille$/, replacement: '$1' },
    { pattern: /(.+)retina$/, replacement: '$1' },
    { pattern: /(.+)arithmetic$/, replacement: '$1' },
    { pattern: /(.+)ancestors$/, replacement: '$1' },
    { pattern: /(.+)domesticity$/, replacement: '$1' },
    { pattern: /(.+)tarry$/, replacement: '$1' },
    { pattern: /(.+)corner$/, replacement: '$1' },
    { pattern: /(.+)interim$/, replacement: '$1' },
    { pattern: /(.+)dishevel$/, replacement: '$1' },
    { pattern: /(.+)sousaphone$/, replacement: '$1' },
    { pattern: /(.+)limbering$/, replacement: '$1' }
  ];
  
  for (const { pattern, replacement } of separationPatterns) {
    if (pattern.test(combinedWord)) {
      return combinedWord.replace(pattern, replacement);
    }
  }
  
  return null;
}

async function getPronunciationFromAnthropic(word) {
  try {
    const message = await anthropic.messages.create({
      model: "claude-3-haiku-20240307",
      max_tokens: 150,
      messages: [{
        role: "user",
        content: `Provide the phonetic respelling pronunciation for the word "${word}" in the format used for spelling bees (like AY-bul for "able" or KROH-kus for "crocus"). Return ONLY the pronunciation, nothing else. If the word is not a real English word, return "INVALID".`
      }]
    });
    
    const pronunciation = message.content[0].text.trim();
    
    if (pronunciation === "INVALID" || pronunciation.toLowerCase().includes("invalid")) {
      return null;
    }
    
    return pronunciation;
  } catch (error) {
    console.error(`Error getting pronunciation for ${word}:`, error.message);
    return null;
  }
}

async function createBackup() {
  console.log('Creating backup of words with missing pronunciations...');
  
  const { data: wordsToBackup, error } = await supabase
    .from('spelling_words')
    .select('*')
    .is('pronunciation_guide', null);
    
  if (error) {
    console.error('Error creating backup:', error);
    return false;
  }
  
  const fs = require('fs');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\pronunciation_backup_${timestamp}.json`;
  
  fs.writeFileSync(backupFile, JSON.stringify(wordsToBackup, null, 2));
  console.log(`Backup created: ${backupFile}`);
  return true;
}

async function processWordsWithMissingPronunciations() {
  const results = {
    combined_words_removed: [],
    non_words_removed: [],
    special_chars_handled: [],
    legitimate_words_updated: [],
    errors: []
  };
  
  try {
    // Create backup first
    const backupSuccess = await createBackup();
    if (!backupSuccess) {
      console.log('Backup failed, but continuing...');
    }
    
    // Get all words missing pronunciations
    const { data: missingWords, error } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide')
      .is('pronunciation_guide', null);
      
    if (error) throw error;
    
    console.log(`Found ${missingWords.length} words missing pronunciation data`);
    
    for (let i = 0; i < missingWords.length; i++) {
      const word = missingWords[i];
      const category = categorizeWord(word.word);
      
      console.log(`Processing ${i + 1}/${missingWords.length}: "${word.word}" (${category})`);
      
      switch (category) {
        case 'combined':
          // Try to separate the word first
          const separated = attemptWordSeparation(word.word);
          if (separated && separated !== word.word) {
            console.log(`  Attempting to fix combined word: "${word.word}" -> "${separated}"`);
            
            // Update the word
            const { error: updateError } = await supabase
              .from('spelling_words')
              .update({ word: separated })
              .eq('id', word.id);
              
            if (updateError) {
              console.error(`  Error updating combined word:`, updateError);
              results.errors.push({ word: word.word, error: updateError.message });
            } else {
              // Now get pronunciation for the corrected word
              await delay(DELAY_BETWEEN_REQUESTS);
              const pronunciation = await getPronunciationFromAnthropic(separated);
              
              if (pronunciation) {
                const { error: pronError } = await supabase
                  .from('spelling_words')
                  .update({ pronunciation_guide: pronunciation })
                  .eq('id', word.id);
                  
                if (pronError) {
                  console.error(`  Error adding pronunciation:`, pronError);
                } else {
                  console.log(`  ✓ Fixed and added pronunciation: ${separated} = ${pronunciation}`);
                  results.combined_words_removed.push({ original: word.word, fixed: separated, pronunciation });
                }
              }
            }
          } else {
            // Delete the combined word that can't be separated
            console.log(`  Deleting unseparable combined word: "${word.word}"`);
            const { error: deleteError } = await supabase
              .from('spelling_words')
              .delete()
              .eq('id', word.id);
              
            if (deleteError) {
              console.error(`  Error deleting combined word:`, deleteError);
            } else {
              results.combined_words_removed.push({ word: word.word, action: 'deleted' });
            }
          }
          break;
          
        case 'non_word':
          console.log(`  Deleting non-word: "${word.word}"`);
          const { error: deleteError } = await supabase
            .from('spelling_words')
            .delete()
            .eq('id', word.id);
            
          if (deleteError) {
            console.error(`  Error deleting non-word:`, deleteError);
          } else {
            results.non_words_removed.push(word.word);
          }
          break;
          
        case 'special_chars':
        case 'legitimate':
          // Get pronunciation using Anthropic API
          await delay(DELAY_BETWEEN_REQUESTS);
          const pronunciation = await getPronunciationFromAnthropic(word.word);
          
          if (pronunciation) {
            const { error: updateError } = await supabase
              .from('spelling_words')
              .update({ pronunciation_guide: pronunciation })
              .eq('id', word.id);
              
            if (updateError) {
              console.error(`  Error updating pronunciation:`, updateError);
              results.errors.push({ word: word.word, error: updateError.message });
            } else {
              console.log(`  ✓ Added pronunciation: ${word.word} = ${pronunciation}`);
              if (category === 'special_chars') {
                results.special_chars_handled.push({ word: word.word, pronunciation });
              } else {
                results.legitimate_words_updated.push({ word: word.word, pronunciation });
              }
            }
          } else {
            console.log(`  ⚠ Could not get pronunciation for: ${word.word}`);
            results.errors.push({ word: word.word, error: 'No pronunciation available' });
          }
          break;
      }
      
      // Rate limiting - batch processing
      if ((i + 1) % BATCH_SIZE === 0) {
        console.log(`  Batch complete, waiting before next batch...`);
        await delay(DELAY_BETWEEN_REQUESTS * 2);
      }
    }
    
  } catch (error) {
    console.error('Process failed:', error);
    results.errors.push({ error: error.message });
  }
  
  return results;
}

async function main() {
  console.log('Starting pronunciation data fix using Anthropic API...\n');
  
  const results = await processWordsWithMissingPronunciations();
  
  console.log('\n=== PROCESSING RESULTS ===');
  console.log(`Combined words handled: ${results.combined_words_removed.length}`);
  console.log(`Non-words removed: ${results.non_words_removed.length}`);
  console.log(`Special character words handled: ${results.special_chars_handled.length}`);
  console.log(`Legitimate words updated: ${results.legitimate_words_updated.length}`);
  console.log(`Errors: ${results.errors.length}`);
  
  if (results.errors.length > 0) {
    console.log('\nErrors encountered:');
    results.errors.forEach(error => {
      console.log(`- ${error.word || 'Unknown'}: ${error.error}`);
    });
  }
  
  // Save results to file
  const fs = require('fs');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\pronunciation_fix_results_${timestamp}.json`;
  fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
  console.log(`\nResults saved to: ${resultsFile}`);
  
  // Verify final state
  console.log('\n=== VERIFICATION ===');
  const { data: remainingMissing, error } = await supabase
    .from('spelling_words')
    .select('word')
    .is('pronunciation_guide', null);
    
  if (!error) {
    console.log(`Words still missing pronunciations: ${remainingMissing.length}`);
    if (remainingMissing.length > 0 && remainingMissing.length <= 10) {
      console.log('Remaining words:', remainingMissing.map(w => w.word));
    }
  }
  
  console.log('\n✓ Pronunciation fix process completed!');
}

if (require.main === module) {
  main().catch(console.error);
}