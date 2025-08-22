const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Helper function to generate respelling pronunciation
function generateRespellingPronunciation(word) {
  // Basic respelling patterns for common word patterns
  const pronunciationMap = {
    // Common patterns
    'tricenary': 'try-SEE-ner-ee',
    'triste': 'TREEST',
    'alberta': 'al-BER-tuh',
    'difficulty': 'DIF-ih-kul-tee',
    'alcarraza': 'al-kar-RAH-sah',
    'americana': 'uh-mer-ih-KAH-nuh',
    'amiably': 'AY-mee-uh-blee',
    'amid': 'uh-MID',
    'cathect': 'kuh-THEKT',
    'andean': 'an-DEE-un',
    'scrawled': 'SKRAWLD',
    'abstruse': 'ab-STROOS',
    'nephrolith': 'NEF-roh-lith',
    'abnegation': 'ab-nih-GAY-shun',
    'beguile': 'bih-GYL'
  };
  
  return pronunciationMap[word.toLowerCase()] || null;
}

// Helper function to generate definition
function generateDefinition(word) {
  const definitionMap = {
    'tricenary': 'Relating to or consisting of thirty; occurring every thirty years.',
    'triste': 'Sad, melancholy, or sorrowful in mood or character.',
    'abnegation': 'The practice of renouncing or rejecting something; self-denial.',
    'beguile': 'To charm or enchant someone, often in a deceptive way.',
    'abstruse': 'Difficult to understand; obscure or esoteric.',
    'nephrolith': 'A kidney stone; a solid deposit formed in the kidneys.',
    'abundance': 'A very large quantity of something; plentifulness.',
    'calamitous': 'Involving or causing a catastrophe; disastrous.',
    'acquit': 'To free someone from a criminal charge by a verdict of not guilty.',
    'capnometer': 'A medical device that measures carbon dioxide concentration.'
  };
  
  return definitionMap[word.toLowerCase()] || `Definition for ${word}`;
}

// Helper function to generate example sentence
function generateExampleSentence(word) {
  const exampleMap = {
    'tricenary': 'The _____ celebration marked thirty years of the institution.',
    'triste': 'The _____ melody filled the concert hall with melancholy.',
    'abnegation': 'His _____ of worldly pleasures surprised his friends.',
    'beguile': 'The storyteller could _____ audiences with her tales.',
    'abstruse': 'The professor\'s _____ theories were difficult to follow.',
    'nephrolith': 'The doctor identified a _____ on the patient\'s kidney scan.',
    'abundance': 'The garden produced an _____ of fresh vegetables.',
    'calamitous': 'The earthquake had _____ effects on the region.',
    'acquit': 'The jury voted to _____ the defendant of all charges.',
    'capnometer': 'The _____ showed normal carbon dioxide levels.'
  };
  
  return exampleMap[word.toLowerCase()] || `The word _____ is used in this context.`;
}

// Helper function to generate etymology
function generateEtymology(word) {
  const etymologyMap = {
    'tricenary': 'From Latin tricenarius, from triceni ("thirty each")',
    'triste': 'From Latin tristis meaning "sad" or "sorrowful"',
    'abnegation': 'From Latin abnegatio, from abnegare "to deny"',
    'beguile': 'From Middle English, from be- + guile "deceit"',
    'abstruse': 'From Latin abstrusus "hidden, concealed"',
    'nephrolith': 'From Greek nephros "kidney" + lithos "stone"'
  };
  
  return etymologyMap[word.toLowerCase()] || `Etymology for ${word} not available`;
}

// Parse combined words from error messages
function parseCombinedWord(word, definition) {
  // Extract the component words from error messages
  let components = [];
  
  if (definition.includes('[COMBINED WORD ERROR]')) {
    // Look for patterns like "word1" + "word2" or "word1" (description) + "word2"
    const matches = definition.match(/"([^"]+)"/g);
    if (matches && matches.length >= 2) {
      components = matches.slice(0, 2).map(m => m.replace(/"/g, ''));
    }
  }
  
  // If parsing fails, try some known patterns
  if (components.length === 0) {
    const knownCombinations = {
      'tricenarytriste': ['tricenary', 'triste'],
      'albertadifficulty': ['alberta'],
      'alcarrazadifficulty': ['alcarraza'],
      'americanaamiably': ['americana', 'amiably'],
      'amidcathect': ['amid', 'cathect'],
      'andeanscrawled': ['andean', 'scrawled'],
      'abstrusenephrolith': ['abstruse', 'nephrolith'],
      'abnegationbeguile': ['abnegation', 'beguile'],
      'abundancecalamitous': ['abundance', 'calamitous'],
      'acquitcapnometer': ['acquit', 'capnometer']
    };
    
    components = knownCombinations[word.toLowerCase()] || [];
  }
  
  return components;
}

async function processCombinedWords() {
  try {
    console.log('Finding all combined words with errors...');
    
    // Get all words with error markers
    const { data: errorWords, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition, source_difficulty, difficulty_level, difficulty_name, original_source, source_access_date')
      .or('definition.ilike.%[COMBINED WORD ERROR]%,definition.ilike.%ERROR:%,definition.ilike.%incorrectly joined%')
      .order('word');
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${errorWords.length} combined words to process`);
    
    let processedCount = 0;
    let successCount = 0;
    
    for (const wordEntry of errorWords) {
      processedCount++;
      console.log(`\n[${processedCount}/${errorWords.length}] Processing: ${wordEntry.word}`);
      
      // Parse the combined word
      const components = parseCombinedWord(wordEntry.word, wordEntry.definition);
      
      if (components.length === 0) {
        console.log(`  ⚠ Could not parse components for: ${wordEntry.word}`);
        continue;
      }
      
      console.log(`  → Separating into: ${components.join(', ')}`);
      
      // Delete the combined word
      const { error: deleteError } = await supabase
        .from('spelling_words')
        .delete()
        .eq('id', wordEntry.id);
        
      if (deleteError) {
        console.error(`  ✗ Failed to delete ${wordEntry.word}:`, deleteError);
        continue;
      }
      
      // Create entries for each component
      for (const component of components) {
        if (!component || component === 'difficulty') continue; // Skip empty or non-spelling words
        
        // Check if component already exists
        const { data: existing } = await supabase
          .from('spelling_words')
          .select('word')
          .eq('word', component)
          .single();
          
        if (existing) {
          console.log(`    ⚠ "${component}" already exists, skipping...`);
          continue;
        }
        
        // Create new entry
        const newEntry = {
          word: component,
          definition: generateDefinition(component),
          example_sentence: generateExampleSentence(component),
          part_of_speech: 'noun', // Default, would need API to determine
          pronunciation_guide: generateRespellingPronunciation(component),
          etymology: generateEtymology(component),
          etymology_source: 'Claude',
          definition_source: 'Claude',
          memory_tips: `Remember the spelling of ${component}`,
          // Inherit some properties from original
          source_difficulty: wordEntry.source_difficulty,
          difficulty_level: wordEntry.difficulty_level || 2,
          difficulty_name: wordEntry.difficulty_name || 'Elementary',
          original_source: wordEntry.original_source,
          source_access_date: wordEntry.source_access_date,
          frequency: 1,
          phonetic_transparency_score: 50,
          word_frequency_score: 50,
          morphology_score: 50,
          etymology_score: 50,
          difficulty_calculation_method: 'manual_separation'
        };
        
        const { error: insertError } = await supabase
          .from('spelling_words')
          .insert(newEntry);
          
        if (insertError) {
          console.error(`    ✗ Failed to insert ${component}:`, insertError);
        } else {
          console.log(`    ✓ Created: ${component}`);
        }
      }
      
      successCount++;
      
      // Rate limiting
      if (processedCount % 10 === 0) {
        console.log(`\n--- Progress: ${processedCount}/${errorWords.length} processed ---`);
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    console.log(`\n✓ Processing complete!`);
    console.log(`Total processed: ${processedCount}`);
    console.log(`Successfully handled: ${successCount}`);
    
    // Verify cleanup
    const { data: remainingErrors, error: verifyError } = await supabase
      .from('spelling_words')
      .select('word', { count: 'exact' })
      .or('definition.ilike.%[COMBINED WORD ERROR]%,definition.ilike.%ERROR:%');
      
    if (!verifyError) {
      console.log(`Remaining error words: ${remainingErrors.length}`);
    }
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

// Run the process
processCombinedWords();