const { createClient } = require('@supabase/supabase-js');
const axios = require('axios');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Claude API configuration
const CLAUDE_API_KEY = process.env.ANTHROPIC_API_KEY;
const CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages';

async function callClaudeAPI(prompt) {
  try {
    const response = await axios.post(CLAUDE_API_URL, {
      model: 'claude-3-haiku-20240307',
      max_tokens: 1000,
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ]
    }, {
      headers: {
        'Authorization': `Bearer ${CLAUDE_API_KEY}`,
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01'
      }
    });
    
    return response.data.content[0].text;
  } catch (error) {
    console.error('Claude API error:', error.response?.data || error.message);
    return null;
  }
}

async function generateWordContent(word) {
  const prompt = `For the spelling bee word "${word}", provide the following information in this exact JSON format:

{
  "pronunciation": "phonetic respelling like AY-bul",
  "definition": "Clear, concise definition suitable for spelling bee",
  "example_sentence": "Example sentence with the word replaced by ___",
  "etymology": "Word origin and etymology",
  "memory_tips": "Helpful tips for remembering the spelling",
  "part_of_speech": "noun/verb/adjective/etc"
}

Make sure the example sentence uses ___ where the word would go and provides good context for understanding the word's meaning. Keep the definition concise but complete. Etymology should be accurate and educational.`;

  const response = await callClaudeAPI(prompt);
  
  if (response) {
    try {
      // Extract JSON from response
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
    } catch (error) {
      console.error(`Failed to parse JSON for ${word}:`, error);
    }
  }
  
  return null;
}

async function fixCombinedWords() {
  const combinedWordsToFix = [
    {
      combined: "abstrusenephrolith",
      separated: ["abstruse", "nephrolith"]
    },
    {
      combined: "albertadifficulty", 
      separated: ["alberta"]
    },
    {
      combined: "alcarrazadifficulty",
      separated: ["alcarraza"]
    },
    {
      combined: "americanaamiably",
      separated: ["americana", "amiably"]
    },
    {
      combined: "amidcathect",
      separated: ["amid", "cathect"]
    },
    {
      combined: "andeanscrawled",
      separated: ["andean", "scrawled"]
    },
    {
      combined: "tricenarytriste",
      separated: ["tricenary", "triste"]
    }
  ];

  try {
    console.log('Starting combined words fix process with Claude API...');
    
    for (const wordPair of combinedWordsToFix) {
      console.log(`\nProcessing: ${wordPair.combined} -> ${wordPair.separated.join(', ')}`);
      
      // Get the original entry
      const { data: originalEntry, error: fetchError } = await supabase
        .from('spelling_words')
        .select('*')
        .eq('word', wordPair.combined)
        .single();
        
      if (fetchError) {
        console.log(`Could not find word: ${wordPair.combined}`);
        continue;
      }
      
      // Delete the combined word
      const { error: deleteError } = await supabase
        .from('spelling_words')
        .delete()
        .eq('word', wordPair.combined);
        
      if (deleteError) {
        console.error(`Failed to delete ${wordPair.combined}:`, deleteError);
        continue;
      }
      console.log(`  ✓ Deleted combined word: ${wordPair.combined}`);
      
      // Create entries for separated words
      for (const newWord of wordPair.separated) {
        console.log(`  Creating entry for: ${newWord}`);
        
        // Check if word already exists
        const { data: existing } = await supabase
          .from('spelling_words')
          .select('word')
          .eq('word', newWord)
          .single();
          
        if (existing) {
          console.log(`    Word "${newWord}" already exists, skipping...`);
          continue;
        }
        
        // Generate content using Claude API
        const claudeData = await generateWordContent(newWord);
        await new Promise(resolve => setTimeout(resolve, 2000)); // Rate limiting
        
        if (claudeData) {
          const newEntry = {
            word: newWord,
            definition: claudeData.definition,
            example_sentence: claudeData.example_sentence,
            part_of_speech: claudeData.part_of_speech,
            pronunciation_guide: claudeData.pronunciation,
            etymology: claudeData.etymology,
            etymology_source: 'Claude',
            definition_source: 'Claude',
            memory_tips: claudeData.memory_tips,
            // Inherit some properties from original
            source_difficulty: originalEntry.source_difficulty,
            difficulty_level: originalEntry.difficulty_level,
            difficulty_name: originalEntry.difficulty_name,
            original_source: originalEntry.original_source,
            source_access_date: originalEntry.source_access_date,
            frequency: 1,
            // Calculate difficulty scores
            phonetic_transparency_score: 50,
            word_frequency_score: 50,
            morphology_score: 50,
            etymology_score: 50,
            difficulty_calculation_method: 'claude_generated'
          };
          
          const { error: insertError } = await supabase
            .from('spelling_words')
            .insert(newEntry);
            
          if (insertError) {
            console.error(`Failed to insert ${newWord}:`, insertError);
          } else {
            console.log(`    ✓ Created entry for: ${newWord}`);
          }
        } else {
          console.log(`    ⚠ Failed to generate content for: ${newWord}`);
        }
      }
    }
    
    console.log('\n✓ Combined words fix completed!');
    
  } catch (error) {
    console.error('Fix process failed:', error);
  }
}

async function addMissingPronunciations() {
  try {
    console.log('Starting process to add missing pronunciations...');
    
    // Get words with missing pronunciation
    const { data: missingPronunciation, error } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide')
      .is('pronunciation_guide', null)
      .limit(20); // Start with smaller batch
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${missingPronunciation.length} words missing pronunciation`);
    
    let processed = 0;
    let updated = 0;
    
    for (const entry of missingPronunciation) {
      console.log(`Processing: ${entry.word}`);
      processed++;
      
      const prompt = `Provide the pronunciation for the word "${entry.word}" using phonetic respelling format (like "AY-bul" for "able").

Use capital letters for stressed syllables, hyphens to separate syllables, and familiar letter combinations:
- AY for long A sound
- EE for long E sound  
- OW for "ow" sound
- ER for "er" sound
- etc.

Just return the respelling pronunciation, nothing else.`;
      
      const pronunciation = await callClaudeAPI(prompt);
      await new Promise(resolve => setTimeout(resolve, 1500)); // Rate limiting
      
      if (pronunciation && pronunciation.trim().length > 0) {
        const cleanPronunciation = pronunciation.trim();
        
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ pronunciation_guide: cleanPronunciation })
          .eq('id', entry.id);
          
        if (updateError) {
          console.error(`Failed to update ${entry.word}:`, updateError);
        } else {
          console.log(`  ✓ Added pronunciation: ${cleanPronunciation}`);
          updated++;
        }
      } else {
        console.log(`  ⚠ Invalid pronunciation response for: ${entry.word}`);
      }
    }
    
    console.log(`\n✓ Pronunciation process completed!`);
    console.log(`Processed: ${processed} words`);
    console.log(`Updated: ${updated} words`);
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

// Main execution
async function main() {
  if (!CLAUDE_API_KEY) {
    console.error('Please add ANTHROPIC_API_KEY to your .env.local file');
    return;
  }
  
  console.log('Choose an option:');
  console.log('1. Fix combined words');
  console.log('2. Add missing pronunciations');
  console.log('3. Both');
  
  const option = process.argv[2] || '3';
  
  switch(option) {
    case '1':
      await fixCombinedWords();
      break;
    case '2':
      await addMissingPronunciations();
      break;
    case '3':
    default:
      await fixCombinedWords();
      await addMissingPronunciations();
      break;
  }
}

main();