const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

const CLAUDE_API_KEY = process.env.ANTHROPIC_API_KEY;
const CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages';

// Claude API pronunciation generation
async function getPhoneticFromClaude(word) {
  try {
    const response = await fetch(CLAUDE_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-3-haiku-20240307',
        max_tokens: 100,
        messages: [{
          role: 'user',
          content: `Create a phonetic respelling for the word "${word}" using simple syllable-based pronunciation guide format like "RIHTH-uhm" for rhythm or "KAS-uhl" for castle. Use capital letters for stressed syllables and lowercase for unstressed. Separate syllables with hyphens. Return ONLY the pronunciation, no explanation.`
        }]
      })
    });

    if (!response.ok) {
      throw new Error(`Claude API error: ${response.status}`);
    }

    const data = await response.json();
    if (data.content && data.content[0] && data.content[0].text) {
      return data.content[0].text.trim();
    }
  } catch (error) {
    console.log(`Claude API failed for ${word}: ${error.message}`);
  }
  return null;
}


// Generate pronunciation using Claude API only
async function generatePhoneticRespelling(word) {
  const cleanWord = word.toLowerCase().trim();
  
  // Get pronunciation from Claude API
  const pronunciation = await getPhoneticFromClaude(cleanWord);
  
  if (!pronunciation) {
    throw new Error(`Failed to get pronunciation for word: ${word}`);
  }
  
  return pronunciation;
}

async function getMissingPronunciations() {
  try {
    const { data, error } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide')
      .or('pronunciation_guide.is.null,pronunciation_guide.eq.')
      .order('word');
    
    if (error) {
      throw error;
    }
    
    console.log(`Found ${data.length} words missing pronunciation guides`);
    return data;
  } catch (error) {
    console.error('Error fetching missing pronunciations:', error);
    return [];
  }
}

function isValidWord(word) {
  // Check if word contains only letters and common punctuation
  const cleanWord = word.trim();
  
  // Skip words that are clearly malformed
  if (cleanWord.length < 2) return false;
  if (cleanWord.length > 50) return false;
  if (/\d/.test(cleanWord)) return false; // Contains numbers
  if (/[^a-zA-Z'-]/.test(cleanWord)) return false; // Contains invalid characters
  
  // Check for obvious combined words (heuristic)
  const lowerWord = cleanWord.toLowerCase();
  if (lowerWord.includes('the') && lowerWord !== 'the' && !lowerWord.endsWith('the')) return false;
  if (lowerWord.includes('noun') && lowerWord !== 'noun' && !lowerWord.endsWith('noun')) return false;
  if (lowerWord.includes('verb') && lowerWord !== 'verb' && !lowerWord.endsWith('verb')) return false;
  
  return true;
}

async function updatePronunciations(batchSize = 50) {
  try {
    const missingWords = await getMissingPronunciations();
    
    if (missingWords.length === 0) {
      console.log('No words need pronunciation updates');
      return;
    }
    
    const updates = [];
    const invalidWords = [];
    
    console.log('Processing pronunciations...');
    
    for (let i = 0; i < missingWords.length; i++) {
      const { id, word } = missingWords[i];
      
      if (!isValidWord(word)) {
        console.log(`Skipping invalid word: "${word}"`);
        invalidWords.push({ id, word, reason: 'Invalid format' });
        continue;
      }
      
      // Get pronunciation from Claude API only
      let pronunciation;
      try {
        pronunciation = await generatePhoneticRespelling(word);
      } catch (error) {
        console.log(`Failed to get pronunciation for ${word}: ${error.message}`);
        invalidWords.push({ id, word, reason: 'Claude API failed' });
        continue;
      }
      
      updates.push({ id, word, pronunciation_guide: pronunciation });
      
      console.log(`${i + 1}/${missingWords.length}: ${word} -> ${pronunciation}`);
      
      // Rate limiting - pause between Claude API calls (more conservative)
      if ((i + 1) % 5 === 0) {
        console.log('Pausing for Claude API rate limiting...');
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
      
      // Process in batches
      if (updates.length >= batchSize) {
        await processBatch(updates);
        updates.length = 0; // Clear the array
        
        // Save progress
        fs.writeFileSync(
          `scripts/pronunciation_progress_${Date.now()}.json`,
          JSON.stringify({ completed: i + 1, total: missingWords.length, invalidWords })
        );
      }
    }
    
    // Process remaining updates
    if (updates.length > 0) {
      await processBatch(updates);
    }
    
    // Report invalid words
    if (invalidWords.length > 0) {
      console.log(`\nFound ${invalidWords.length} invalid words:`);
      fs.writeFileSync(
        'scripts/invalid_pronunciation_words.json',
        JSON.stringify(invalidWords, null, 2)
      );
      invalidWords.slice(0, 10).forEach(item => {
        console.log(`- ${item.word} (${item.reason})`);
      });
      if (invalidWords.length > 10) {
        console.log(`... and ${invalidWords.length - 10} more (see invalid_pronunciation_words.json)`);
      }
    }
    
    console.log('\nPronunciation updates completed!');
    
  } catch (error) {
    console.error('Error updating pronunciations:', error);
  }
}

async function processBatch(updates) {
  try {
    for (const update of updates) {
      const { error } = await supabase
        .from('spelling_words')
        .update({ pronunciation_guide: update.pronunciation_guide })
        .eq('id', update.id);
      
      if (error) {
        console.error(`Error updating word ${update.word}:`, error);
      }
    }
    console.log(`Updated batch of ${updates.length} pronunciations`);
  } catch (error) {
    console.error('Error processing batch:', error);
  }
}

// Run the script
if (require.main === module) {
  updatePronunciations()
    .then(() => process.exit(0))
    .catch(error => {
      console.error('Script failed:', error);
      process.exit(1);
    });
}

module.exports = {
  generatePhoneticRespelling,
  updatePronunciations,
  getMissingPronunciations,
  getPhoneticFromClaude
};