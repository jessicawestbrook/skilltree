import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: join(__dirname, '..', '.env.local') });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceRoleKey = process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceRoleKey) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceRoleKey);

// Function to determine vocabulary difficulty based on word characteristics
function determineVocabularyDifficulty(word, definition) {
  const wordLower = word.toLowerCase();
  const wordLength = word.length;
  
  // ID 1 = Elementary (ages 6-10)
  // ID 2 = Middle School (ages 11-13)
  // No other IDs currently exist, need to check what the actual IDs are
  
  // Simple criteria for now - can be refined
  if (wordLength <= 4) {
    return 1; // Elementary
  } else if (wordLength <= 7) {
    return Math.random() < 0.6 ? 1 : 2; // Mix based on length
  } else {
    return 2; // Middle School for longer words
  }
}

// Function to determine spelling difficulty based on word characteristics
function determineSpellingDifficulty(word) {
  const wordLower = word.toLowerCase();
  const wordLength = word.length;
  
  // Currently only ID 1 exists in the data
  // For now, assign all to ID 1 since that's what exists
  return 1;
}

async function analyzeAndAssignDifficulties() {
  console.log('Fetching words with missing difficulty levels...\n');
  
  // First, get the actual difficulty IDs from the tables
  const { data: vocabDiffs } = await supabase
    .from('vocabulary_difficulties')
    .select('id, name');
  
  const { data: spellingDiffs } = await supabase
    .from('spelling_difficulties')
    .select('id, name');
  
  console.log('Available Vocabulary Difficulties:');
  vocabDiffs?.forEach(d => console.log(`  ${d.id}: ${d.name}`));
  
  console.log('\nAvailable Spelling Difficulties:');
  spellingDiffs?.forEach(d => console.log(`  ${d.id}: ${d.name}`));
  
  // If no difficulties exist, we need to create them first
  if (!vocabDiffs || vocabDiffs.length === 0) {
    console.log('\n⚠ No vocabulary difficulties found in database!');
    console.log('Creating default vocabulary difficulties...');
    
    const defaultVocabDifficulties = [
      { id: 1, name: 'Elementary', description: 'Ages 6-10' },
      { id: 2, name: 'Middle School', description: 'Ages 11-13' },
      { id: 3, name: 'High School', description: 'Ages 14-17' },
      { id: 4, name: 'College', description: 'Ages 18+' },
      { id: 5, name: 'Advanced', description: 'Graduate level and beyond' }
    ];
    
    for (const diff of defaultVocabDifficulties) {
      const { error } = await supabase
        .from('vocabulary_difficulties')
        .insert(diff);
      if (!error) {
        console.log(`  Created: ${diff.name}`);
      }
    }
  }
  
  if (!spellingDiffs || spellingDiffs.length === 0) {
    console.log('\n⚠ No spelling difficulties found in database!');
    console.log('Creating default spelling difficulties...');
    
    const defaultSpellingDifficulties = [
      { id: 1, name: 'Easy', description: 'Common phonetic patterns' },
      { id: 2, name: 'Medium', description: 'Some irregular patterns' },
      { id: 3, name: 'Hard', description: 'Complex or irregular spelling' },
      { id: 4, name: 'Expert', description: 'Very challenging spelling' }
    ];
    
    for (const diff of defaultSpellingDifficulties) {
      const { error } = await supabase
        .from('spelling_difficulties')
        .insert(diff);
      if (!error) {
        console.log(`  Created: ${diff.name}`);
      }
    }
  }
  
  // Fetch words with missing difficulties
  const { data: wordsToUpdate, error } = await supabase
    .from('spelling_words')
    .select('id, word, definition')
    .or('vocabulary_difficulty_id.is.null,spelling_difficulty_id.is.null');
  
  if (error) {
    console.error('Error fetching words:', error);
    return;
  }
  
  console.log(`\nFound ${wordsToUpdate.length} words to update`);
  
  // Prepare updates
  const updates = wordsToUpdate.map(word => {
    const vocabDiff = word.vocabulary_difficulty_id || determineVocabularyDifficulty(word.word, word.definition);
    const spellingDiff = word.spelling_difficulty_id || determineSpellingDifficulty(word.word);
    
    return {
      id: word.id,
      word: word.word,
      vocabulary_difficulty_id: vocabDiff,
      spelling_difficulty_id: spellingDiff
    };
  });
  
  // Save to file for review
  const outputPath = join(__dirname, 'difficulty_assignments.json');
  fs.writeFileSync(outputPath, JSON.stringify(updates, null, 2));
  console.log(`\nSaved proposed assignments to: ${outputPath}`);
  
  // Show sample of assignments
  console.log('\nSample of proposed assignments (first 10):');
  updates.slice(0, 10).forEach(u => {
    console.log(`  ${u.word}: vocab=${u.vocabulary_difficulty_id}, spelling=${u.spelling_difficulty_id}`);
  });
  
  // Distribution summary
  const vocabCounts = {};
  const spellingCounts = {};
  
  updates.forEach(u => {
    vocabCounts[u.vocabulary_difficulty_id] = (vocabCounts[u.vocabulary_difficulty_id] || 0) + 1;
    spellingCounts[u.spelling_difficulty_id] = (spellingCounts[u.spelling_difficulty_id] || 0) + 1;
  });
  
  console.log('\nProposed Vocabulary Difficulty Distribution:');
  Object.entries(vocabCounts).forEach(([id, count]) => {
    console.log(`  Difficulty ${id}: ${count} words`);
  });
  
  console.log('\nProposed Spelling Difficulty Distribution:');
  Object.entries(spellingCounts).forEach(([id, count]) => {
    console.log(`  Difficulty ${id}: ${count} words`);
  });
  
  console.log('\n✓ Analysis complete. Review difficulty_assignments.json before applying updates.');
}

analyzeAndAssignDifficulties().catch(console.error);