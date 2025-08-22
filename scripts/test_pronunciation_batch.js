const script = require('./fill_missing_pronunciations.js');

async function testPronunciationBatch() {
  try {
    console.log('Running test batch of pronunciation updates...');
    
    // Get missing pronunciations
    const missingWords = await script.getMissingPronunciations();
    console.log(`Total words missing pronunciations: ${missingWords.length}`);
    
    // Filter out obviously malformed words for testing
    const validWords = missingWords.filter(item => {
      const word = item.word.toLowerCase().trim();
      
      // Skip words that are clearly malformed
      if (word.length < 3 || word.length > 30) return false;
      if (/\d/.test(word)) return false; // Contains numbers
      if (/[^a-zA-Z'-]/.test(word)) return false; // Contains invalid characters
      if (word.includes('the') && word !== 'the' && !word.endsWith('the')) return false;
      if (word.includes('noun') && word !== 'noun') return false;
      if (word.includes('verb') && word !== 'verb') return false;
      
      return true;
    });
    
    console.log(`Valid words after filtering: ${validWords.length}`);
    console.log(`Malformed words filtered out: ${missingWords.length - validWords.length}`);
    
    // Test with first 3 valid words only
    const testWords = validWords.slice(0, 3);
    console.log('\\nTesting with these words:');
    testWords.forEach((item, i) => {
      console.log(`${i+1}. ${item.word} (ID: ${item.id})`);
    });
    
    console.log('\\nGenerating pronunciations...');
    const results = [];
    
    for (let i = 0; i < testWords.length; i++) {
      const { id, word } = testWords[i];
      
      try {
        const pronunciation = await script.getPhoneticFromClaude(word);
        results.push({ id, word, pronunciation });
        console.log(`${i + 1}. ${word} -> ${pronunciation}`);
        
        // Small delay between requests
        await new Promise(resolve => setTimeout(resolve, 1000));
        
      } catch (error) {
        console.log(`Failed for ${word}: ${error.message}`);
      }
    }
    
    console.log('\\nTest batch results:');
    results.forEach(result => {
      console.log(`ID ${result.id}: ${result.word} -> ${result.pronunciation}`);
    });
    
    console.log(`\\nSuccessfully generated ${results.length} out of ${testWords.length} pronunciations`);
    
  } catch (error) {
    console.error('Test batch failed:', error);
  }
}

// Run the test
testPronunciationBatch();