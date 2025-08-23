const { createClient } = require('@supabase/supabase-js');
const Anthropic = require('@anthropic-ai/sdk');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

// Use service role key for admin access to bypass RLS
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Load list of failed words to skip
const FAILED_WORDS_FILE = 'scripts/failed_words_list.json';
let failedWords = new Set();

try {
  if (fs.existsSync(FAILED_WORDS_FILE)) {
    const data = JSON.parse(fs.readFileSync(FAILED_WORDS_FILE, 'utf8'));
    failedWords = new Set(data);
    console.log(`Loaded ${failedWords.size} previously failed words to skip`);
  }
} catch (error) {
  console.log('No previous failed words list found');
}

// Check if word looks concatenated/invalid
function isLikelyConcatenated(word) {
  // Check for camelCase pattern or extremely long words without hyphens
  return /[a-z][A-Z]/.test(word) || 
         (word.length > 20 && !word.includes('-') && !word.includes(' '));
}

async function populateLegitimateWords() {
  console.log('=== POPULATING WORD CONTENT WITH CLAUDE API ===\n');
  
  const batchSize = 10;
  const progressFile = `scripts/claude_words_progress_${Date.now()}.json`;
  let progress = { processed: 0, successful: 0, skipped: 0, failed: 0 };
  
  try {
    // Get words that need content, excluding known failed words
    const { data: allWordsNeedingContent, error } = await supabase
      .from('spelling_words')
      .select('id, word, source_difficulty, definition, example_sentence, pronunciation_guide, etymology')
      .or('definition.is.null,example_sentence.is.null,pronunciation_guide.is.null,etymology.is.null')
      .order('word')
      .limit(1000); // Get more words to filter from

    if (error) {
      throw new Error(`Error fetching words: ${error.message}`);
    }

    if (!allWordsNeedingContent || allWordsNeedingContent.length === 0) {
      console.log('✅ All words have complete content!');
      return;
    }

    // Filter out failed words and concatenated words
    const wordsToProcess = [];
    for (const word of allWordsNeedingContent) {
      if (!failedWords.has(word.word) && !isLikelyConcatenated(word.word)) {
        wordsToProcess.push(word);
        if (wordsToProcess.length >= batchSize) break;
      }
    }

    if (wordsToProcess.length === 0) {
      console.log('No processable words found (all are either failed or concatenated)');
      console.log(`Total words needing content: ${allWordsNeedingContent.length}`);
      console.log(`Failed words: ${failedWords.size}`);
      return;
    }

    console.log(`Found ${wordsToProcess.length} words to process (from ${allWordsNeedingContent.length} total)\n`);

    for (const wordData of wordsToProcess) {
      progress.processed++;
      
      console.log(`[${progress.processed}/${wordsToProcess.length}] Processing: "${wordData.word}"`);
      
      try {
        // Get content from Claude API
        const wordContent = await getWordContentFromClaude(wordData.word, wordData.source_difficulty);
        
        if (!wordContent) {
          console.log(`    ⚠️ Skipping - Claude couldn't generate content for "${wordData.word}"`);
          failedWords.add(wordData.word);
          progress.skipped++;
          continue;
        }
        
        // Only update fields that are missing
        const updates = {};
        let needsUpdate = false;
        
        if (!wordData.definition && wordContent.definition) {
          updates.definition = wordContent.definition;
          needsUpdate = true;
        }
        if (!wordData.example_sentence && wordContent.example_sentence) {
          updates.example_sentence = wordContent.example_sentence;
          needsUpdate = true;
        }
        if (!wordData.pronunciation_guide && wordContent.pronunciation_guide) {
          updates.pronunciation_guide = wordContent.pronunciation_guide;
          needsUpdate = true;
        }
        if (!wordData.etymology && wordContent.etymology) {
          updates.etymology = wordContent.etymology;
          needsUpdate = true;
        }

        if (needsUpdate) {
          console.log(`    Updating with:`, Object.keys(updates).join(', '));
          
          const { data: updatedData, error: updateError } = await supabase
            .from('spelling_words')
            .update(updates)
            .eq('id', wordData.id)
            .select();

          if (updateError) {
            console.log(`    ❌ Update failed: ${updateError.message}`);
            failedWords.add(wordData.word);
            progress.failed++;
          } else if (!updatedData || updatedData.length === 0) {
            console.log(`    ❌ Update returned no data - check if word exists in db`);
            failedWords.add(wordData.word);
            progress.failed++;
          } else {
            console.log(`    ✅ Successfully updated ${updatedData.length} row(s)`);
            progress.successful++;
          }
        } else {
          console.log(`    ↪ Already has all content`);
          progress.successful++;
        }

        // Rate limiting - pause between API requests
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Save progress every 5 words
        if (progress.processed % 5 === 0) {
          fs.writeFileSync(progressFile, JSON.stringify({
            ...progress,
            timestamp: new Date().toISOString(),
            lastWord: wordData.word
          }, null, 2));
          
          // Also save failed words list
          fs.writeFileSync(FAILED_WORDS_FILE, JSON.stringify(Array.from(failedWords), null, 2));
        }

      } catch (error) {
        console.log(`    ❌ Error: ${error.message}`);
        failedWords.add(wordData.word);
        progress.failed++;
      }
    }

    console.log(`\n📊 COMPLETION SUMMARY:`);
    console.log(`  Total processed: ${progress.processed}`);
    console.log(`  Successfully updated: ${progress.successful}`);
    console.log(`  Skipped: ${progress.skipped}`);
    console.log(`  Failed: ${progress.failed}`);

    // Save final progress and failed words
    fs.writeFileSync(progressFile, JSON.stringify({
      ...progress,
      timestamp: new Date().toISOString(),
      completed: true
    }, null, 2));
    fs.writeFileSync(FAILED_WORDS_FILE, JSON.stringify(Array.from(failedWords), null, 2));
    
    console.log(`\n💾 Progress saved to: ${progressFile}`);
    console.log(`💾 Failed words saved to: ${FAILED_WORDS_FILE}`);

  } catch (error) {
    console.error('Error in content population:', error);
  }
}

async function getWordContentFromClaude(word, sourceDifficulty) {
  try {
    const prompt = `For the spelling bee word "${word}"${sourceDifficulty ? ` (difficulty level: ${sourceDifficulty})` : ''}, provide the following information in JSON format:

1. definition: A clear, concise definition suitable for students
2. example_sentence: A contextual sentence using the word, with the word replaced by _____ (five underscores)
3. pronunciation_guide: Phonetic respelling using simple syllables (e.g., "difficulty" → "DIF-ih-kul-tee")
4. etymology: Brief word origin and history

Return ONLY valid JSON without any markdown formatting or code blocks. If the word appears to be invalid or concatenated, return null.

Example response format:
{
  "definition": "The state or quality of being hard to do",
  "example_sentence": "The math problem presented a significant _____ for the students.",
  "pronunciation_guide": "DIF-ih-kul-tee",
  "etymology": "From Latin difficilis, from dis- (not) + facilis (easy)"
}`;

    const response = await anthropic.messages.create({
      model: 'claude-3-haiku-20240307',
      max_tokens: 500,
      temperature: 0.3,
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    const responseText = response.content[0].text.trim();
    
    // Check if Claude returned null (invalid word)
    if (responseText === 'null' || responseText.toLowerCase().includes('invalid') || responseText.toLowerCase().includes('concatenated')) {
      return null;
    }

    // Try to parse the JSON
    try {
      const parsed = JSON.parse(responseText);
      
      // Validate the response has all required fields
      if (parsed && parsed.definition && parsed.example_sentence && parsed.pronunciation_guide && parsed.etymology) {
        return parsed;
      } else {
        console.log(`    ⚠️ Response missing required fields`);
        return null;
      }
    } catch (parseError) {
      console.log(`    ⚠️ Failed to parse Claude response for "${word}"`);
      return null;
    }

  } catch (error) {
    console.log(`    ⚠️ Claude API error: ${error.message}`);
    return null;
  }
}

// Run the population
populateLegitimateWords().catch(console.error);