const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function populateMissingContent() {
  console.log('=== IDENTIFYING WORDS MISSING CONTENT ===\n');

  try {
    // Step 1: Find words missing definitions and example sentences
    console.log('Step 1: Finding words missing content...');
    const missingContentWords = await findMissingContentWords();
    
    // Step 2: Display analysis
    console.log('\nStep 2: Analyzing missing content...');
    displayMissingContentAnalysis(missingContentWords);
    
    // Step 3: Generate content population script
    console.log('\nStep 3: Generating content population script...');
    await generateContentPopulationScript(missingContentWords);
    
  } catch (error) {
    console.error('Error during content analysis:', error);
  }
}

async function findMissingContentWords() {
  const missingWords = [];
  const batchSize = 1000;
  let offset = 0;
  let hasMore = true;

  console.log('Fetching words from database...');

  while (hasMore) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition, example_sentence, pronunciation_guide, etymology, source_difficulty')
      .range(offset, offset + batchSize - 1)
      .order('id');

    if (error) {
      throw new Error(`Error fetching words: ${error.message}`);
    }

    if (batch && batch.length > 0) {
      batch.forEach(word => {
        const missingContent = {
          id: word.id,
          word: word.word,
          source_difficulty: word.source_difficulty,
          missing_definition: !word.definition || word.definition.trim() === '',
          missing_example_sentence: !word.example_sentence || word.example_sentence.trim() === '',
          missing_pronunciation: !word.pronunciation_guide || word.pronunciation_guide.trim() === '',
          missing_etymology: !word.etymology || word.etymology.trim() === ''
        };

        // Only include words that are missing at least one piece of content
        if (missingContent.missing_definition || 
            missingContent.missing_example_sentence || 
            missingContent.missing_pronunciation || 
            missingContent.missing_etymology) {
          missingWords.push(missingContent);
        }
      });

      console.log(`Processed ${offset + batch.length} words so far...`);
      offset += batchSize;
      hasMore = batch.length === batchSize;
    } else {
      hasMore = false;
    }
  }

  return missingWords;
}

function displayMissingContentAnalysis(missingWords) {
  console.log(`\n📊 MISSING CONTENT ANALYSIS:`);
  console.log(`Total words missing some content: ${missingWords.length}`);
  
  const stats = {
    missing_definition: 0,
    missing_example_sentence: 0,
    missing_pronunciation: 0,
    missing_etymology: 0,
    missing_all_four: 0,
    by_difficulty: {
      'One Bee': 0,
      'Two Bee': 0,
      'Three Bee': 0,
      'Other': 0
    }
  };

  missingWords.forEach(word => {
    if (word.missing_definition) stats.missing_definition++;
    if (word.missing_example_sentence) stats.missing_example_sentence++;
    if (word.missing_pronunciation) stats.missing_pronunciation++;
    if (word.missing_etymology) stats.missing_etymology++;
    
    if (word.missing_definition && word.missing_example_sentence && 
        word.missing_pronunciation && word.missing_etymology) {
      stats.missing_all_four++;
    }
    
    // Count by difficulty
    if (['One Bee', 'Two Bee', 'Three Bee'].includes(word.source_difficulty)) {
      stats.by_difficulty[word.source_difficulty]++;
    } else {
      stats.by_difficulty['Other']++;
    }
  });

  console.log(`\n📋 Missing content breakdown:`);
  console.log(`  - Missing definitions: ${stats.missing_definition}`);
  console.log(`  - Missing example sentences: ${stats.missing_example_sentence}`);
  console.log(`  - Missing pronunciations: ${stats.missing_pronunciation}`);
  console.log(`  - Missing etymology: ${stats.missing_etymology}`);
  console.log(`  - Missing all four: ${stats.missing_all_four}`);
  
  console.log(`\n📈 By difficulty level:`);
  Object.entries(stats.by_difficulty).forEach(([level, count]) => {
    console.log(`  - ${level}: ${count} words`);
  });

  // Show sample of words missing all content
  const missingAll = missingWords.filter(word => 
    word.missing_definition && word.missing_example_sentence && 
    word.missing_pronunciation && word.missing_etymology
  );

  if (missingAll.length > 0) {
    console.log(`\n🔍 Sample words missing all content (first 10):`);
    missingAll.slice(0, 10).forEach(word => {
      console.log(`  - "${word.word}" (${word.source_difficulty})`);
    });
  }
}

async function generateContentPopulationScript(missingWords) {
  const timestamp = Date.now();
  
  // Filter to words missing all content (likely the new words)
  const completelyMissingWords = missingWords.filter(word => 
    word.missing_definition && word.missing_example_sentence && 
    word.missing_pronunciation && word.missing_etymology
  );

  console.log(`Generating content population script for ${completelyMissingWords.length} words...`);

  const scriptContent = `const { createClient } = require('@supabase/supabase-js');
const axios = require('axios');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Words that need complete content population
const wordsToPopulate = ${JSON.stringify(completelyMissingWords.slice(0, 50), null, 2)};

let processedCount = 0;
let successCount = 0;
let failedWords = [];

async function populateWordContent() {
  console.log(\`=== POPULATING CONTENT FOR \${wordsToPopulate.length} WORDS ===\\n\`);
  
  for (const wordData of wordsToPopulate) {
    try {
      console.log(\`Processing: "\${wordData.word}" (\${processedCount + 1}/\${wordsToPopulate.length})\`);
      
      // Get definition and pronunciation from Dictionary API
      const dictionaryData = await fetchDictionaryData(wordData.word);
      
      // Generate example sentence (you'll need Claude API key for this)
      const exampleSentence = generateExampleSentence(wordData.word, dictionaryData?.definition);
      
      // Extract etymology if available
      const etymology = dictionaryData?.etymology || '';
      
      // Update database
      const { error } = await supabase
        .from('spelling_words')
        .update({
          definition: dictionaryData?.definition || '',
          example_sentence: exampleSentence,
          pronunciation_guide: dictionaryData?.pronunciation || '',
          etymology: etymology,
          definition_source: dictionaryData?.definition ? 'Dictionary API' : '',
          etymology_source: dictionaryData?.etymology ? 'Dictionary API' : ''
        })
        .eq('id', wordData.id);
      
      if (error) {
        console.log(\`  ❌ Failed to update database: \${error.message}\`);
        failedWords.push({ word: wordData.word, error: error.message });
      } else {
        console.log(\`  ✅ Successfully updated\`);
        successCount++;
      }
      
      processedCount++;
      
      // Rate limiting - wait 1 second between requests
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Save progress every 10 words
      if (processedCount % 10 === 0) {
        saveProgress();
      }
      
    } catch (error) {
      console.log(\`  ❌ Error processing "\${wordData.word}": \${error.message}\`);
      failedWords.push({ word: wordData.word, error: error.message });
      processedCount++;
    }
  }
  
  // Final summary
  console.log(\`\\n📊 COMPLETION SUMMARY:\`);
  console.log(\`  Processed: \${processedCount}/\${wordsToPopulate.length}\`);
  console.log(\`  Successful: \${successCount}\`);
  console.log(\`  Failed: \${failedWords.length}\`);
  
  if (failedWords.length > 0) {
    const failedFile = \`content_population_failed_\${Date.now()}.json\`;
    fs.writeFileSync(failedFile, JSON.stringify(failedWords, null, 2));
    console.log(\`  ❌ Failed words saved to: \${failedFile}\`);
  }
}

async function fetchDictionaryData(word) {
  try {
    const response = await axios.get(\`https://api.dictionaryapi.dev/api/v2/entries/en/\${word}\`);
    const entry = response.data[0];
    
    const definition = entry.meanings[0]?.definitions[0]?.definition || '';
    const pronunciation = entry.phonetics?.find(p => p.text)?.text || '';
    const etymology = entry.origin || '';
    
    return { definition, pronunciation, etymology };
  } catch (error) {
    console.log(\`    Dictionary API failed for "\${word}": \${error.message}\`);
    return null;
  }
}

function generateExampleSentence(word, definition) {
  // Simple example sentence generation - replace with Claude API call if available
  if (definition && definition.length > 10) {
    return \`The word _____ can be understood from its definition.\`;
  }
  return \`The spelling of _____ requires careful attention.\`;
}

function saveProgress() {
  const progress = {
    processed: processedCount,
    successful: successCount,
    failed: failedWords.length,
    timestamp: new Date().toISOString()
  };
  
  fs.writeFileSync(\`content_population_progress_\${Date.now()}.json\`, JSON.stringify(progress, null, 2));
}

// Run the population
populateWordContent().catch(console.error);`;

  const scriptFile = `scripts/populate_word_content_${timestamp}.js`;
  fs.writeFileSync(scriptFile, scriptContent);

  console.log(`✅ Content population script generated: ${scriptFile}`);
  console.log(`\n📋 This script will:`);
  console.log(`  1. Process ${Math.min(completelyMissingWords.length, 50)} words missing all content`);
  console.log(`  2. Fetch definitions and pronunciations from Dictionary API`);
  console.log(`  3. Generate example sentences`);
  console.log(`  4. Update database with new content`);
  console.log(`  5. Save progress and handle failures gracefully`);
  console.log(`\n⚠️  Note: You may need to install axios: npm install axios`);
  console.log(`⚠️  For better example sentences, consider adding Claude API integration`);
}

populateMissingContent();