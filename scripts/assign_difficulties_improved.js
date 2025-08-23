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

// Common words that should be elementary level
const elementaryWords = new Set([
  'hem', 'polo', 'zither', 'foxes', 'hot', 'bad', 'tell', 'yak', 'van', 
  'gem', 'jug', 'map', 'win', 'yet', 'yes', 'bet', 'met', 'get', 'let'
]);

// Complex spelling patterns
const complexSpellingPatterns = [
  /ough/, /augh/, /eigh/, /tion/, /sion/, /ious/, /eous/, /ious/, 
  /cion/, /tial/, /cial/, /ient/, /ence/, /ance/, /ible/, /able/,
  /ph/, /gh/, /kn/, /wr/, /ps/, /pn/, /gn/, /mb/, /mn/
];

// Function to determine vocabulary difficulty
function determineVocabularyDifficulty(word, definition) {
  const wordLower = word.toLowerCase();
  const wordLength = word.length;
  
  // Check if it's a known elementary word
  if (elementaryWords.has(wordLower)) {
    return 1; // Elementary
  }
  
  // Check for compound words or complex structures
  if (wordLower.includes('-') || wordLower.includes(' ')) {
    return wordLength > 10 ? 3 : 2; // Compound words tend to be harder
  }
  
  // Check for prefixes and suffixes that indicate complexity
  const complexPrefixes = ['anti', 'pre', 'post', 'fore', 'inter', 'trans', 'super', 'ultra'];
  const complexSuffixes = ['tion', 'sion', 'ment', 'ness', 'ity', 'ious', 'eous', 'ial', 'ual'];
  
  let hasComplexAffix = false;
  for (const prefix of complexPrefixes) {
    if (wordLower.startsWith(prefix)) {
      hasComplexAffix = true;
      break;
    }
  }
  
  for (const suffix of complexSuffixes) {
    if (wordLower.endsWith(suffix)) {
      hasComplexAffix = true;
      break;
    }
  }
  
  // Scoring based on various factors
  let score = 0;
  
  // Length scoring
  if (wordLength <= 4) score += 1;
  else if (wordLength <= 6) score += 2;
  else if (wordLength <= 8) score += 3;
  else if (wordLength <= 10) score += 4;
  else score += 5;
  
  // Complexity scoring
  if (hasComplexAffix) score += 2;
  
  // Check for double consonants or vowel clusters
  if (/[bcdfghjklmnpqrstvwxyz]{3,}/.test(wordLower)) score += 1;
  if (/[aeiou]{3,}/.test(wordLower)) score += 1;
  
  // Map score to difficulty level (1-5)
  if (score <= 2) return 1;      // Elementary
  else if (score <= 4) return 2;  // Middle School
  else if (score <= 6) return 3;  // High School  
  else if (score <= 8) return 4;  // College
  else return 5;                  // Advanced
}

// Function to determine spelling difficulty
function determineSpellingDifficulty(word) {
  const wordLower = word.toLowerCase();
  
  let difficulty = 1; // Start with Easy
  
  // Check for complex spelling patterns
  for (const pattern of complexSpellingPatterns) {
    if (pattern.test(wordLower)) {
      difficulty = Math.max(difficulty, 3); // At least Hard
      break;
    }
  }
  
  // Check for silent letters
  const silentLetterPatterns = [
    /kn/, /wr/, /gn/, /ps/, /pn/, /mb/, /mn/, /lk/, /lf/, /lm/, /bt/, /tch/, /dge/
  ];
  
  for (const pattern of silentLetterPatterns) {
    if (pattern.test(wordLower)) {
      difficulty = Math.max(difficulty, 2); // At least Medium
      break;
    }
  }
  
  // Check for irregular vowel patterns
  if (/ie|ei|ue|oe|ae/.test(wordLower)) {
    difficulty = Math.max(difficulty, 2);
  }
  
  // Very long words are harder to spell
  if (word.length > 10) {
    difficulty = Math.max(difficulty, 3);
  }
  if (word.length > 15) {
    difficulty = 4; // Expert
  }
  
  // Words with q not followed by u
  if (/q(?!u)/.test(wordLower)) {
    difficulty = Math.max(difficulty, 3);
  }
  
  return difficulty;
}

async function assignImprovedDifficulties() {
  console.log('Fetching words with missing difficulty levels...\n');
  
  // Fetch words with missing difficulties
  const { data: wordsToUpdate, error } = await supabase
    .from('spelling_words')
    .select('id, word, definition')
    .or('vocabulary_difficulty_id.is.null,spelling_difficulty_id.is.null');
  
  if (error) {
    console.error('Error fetching words:', error);
    return;
  }
  
  console.log(`Found ${wordsToUpdate.length} words to process\n`);
  
  // Process words and assign difficulties
  const updates = wordsToUpdate.map(wordData => {
    const vocabDiff = wordData.vocabulary_difficulty_id || 
                      determineVocabularyDifficulty(wordData.word, wordData.definition);
    const spellingDiff = wordData.spelling_difficulty_id || 
                        determineSpellingDifficulty(wordData.word);
    
    return {
      id: wordData.id,
      word: wordData.word,
      vocabulary_difficulty_id: vocabDiff,
      spelling_difficulty_id: spellingDiff
    };
  });
  
  // Calculate distribution
  const vocabDist = {};
  const spellingDist = {};
  
  updates.forEach(u => {
    vocabDist[u.vocabulary_difficulty_id] = (vocabDist[u.vocabulary_difficulty_id] || 0) + 1;
    spellingDist[u.spelling_difficulty_id] = (spellingDist[u.spelling_difficulty_id] || 0) + 1;
  });
  
  console.log('Proposed Vocabulary Difficulty Distribution:');
  const vocabLabels = ['Elementary', 'Middle School', 'High School', 'College', 'Advanced'];
  Object.entries(vocabDist).sort(([a], [b]) => a - b).forEach(([id, count]) => {
    const percent = ((count / updates.length) * 100).toFixed(1);
    console.log(`  ${id} - ${vocabLabels[id-1] || 'Unknown'}: ${count} words (${percent}%)`);
  });
  
  console.log('\nProposed Spelling Difficulty Distribution:');
  const spellingLabels = ['Easy', 'Medium', 'Hard', 'Expert'];
  Object.entries(spellingDist).sort(([a], [b]) => a - b).forEach(([id, count]) => {
    const percent = ((count / updates.length) * 100).toFixed(1);
    console.log(`  ${id} - ${spellingLabels[id-1] || 'Unknown'}: ${count} words (${percent}%)`);
  });
  
  // Show examples from each category
  console.log('\nExample words by vocabulary difficulty:');
  for (let i = 1; i <= 5; i++) {
    const examples = updates.filter(u => u.vocabulary_difficulty_id === i)
                           .slice(0, 3)
                           .map(u => u.word);
    if (examples.length > 0) {
      console.log(`  Level ${i}: ${examples.join(', ')}`);
    }
  }
  
  console.log('\nExample words by spelling difficulty:');
  for (let i = 1; i <= 4; i++) {
    const examples = updates.filter(u => u.spelling_difficulty_id === i)
                           .slice(0, 3)
                           .map(u => u.word);
    if (examples.length > 0) {
      console.log(`  Level ${i}: ${examples.join(', ')}`);
    }
  }
  
  // Save to file
  const outputPath = join(__dirname, 'difficulty_assignments_improved.json');
  fs.writeFileSync(outputPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    totalWords: updates.length,
    vocabularyDistribution: vocabDist,
    spellingDistribution: spellingDist,
    assignments: updates
  }, null, 2));
  
  console.log(`\n✓ Analysis complete. Saved to: ${outputPath}`);
  console.log('\nReview the assignments before applying to database.');
  
  return updates;
}

// Create update script
async function createUpdateScript() {
  const updates = await assignImprovedDifficulties();
  
  if (!updates) return;
  
  // Create SQL update script
  const sqlPath = join(__dirname, 'update_spelling_difficulties.sql');
  
  let sql = '-- Update spelling_words table with difficulty assignments\n';
  sql += '-- Generated: ' + new Date().toISOString() + '\n\n';
  sql += 'BEGIN;\n\n';
  
  // Create update statements in batches
  updates.forEach(u => {
    sql += `UPDATE spelling_words SET \n`;
    sql += `  vocabulary_difficulty_id = ${u.vocabulary_difficulty_id},\n`;
    sql += `  spelling_difficulty_id = ${u.spelling_difficulty_id}\n`;
    sql += `WHERE id = '${u.id}';\n\n`;
  });
  
  sql += 'COMMIT;\n\n';
  sql += '-- Verification query\n';
  sql += 'SELECT \n';
  sql += '  COUNT(*) FILTER (WHERE vocabulary_difficulty_id IS NULL) as missing_vocab,\n';
  sql += '  COUNT(*) FILTER (WHERE spelling_difficulty_id IS NULL) as missing_spelling,\n';
  sql += '  COUNT(*) as total\n';
  sql += 'FROM spelling_words;';
  
  fs.writeFileSync(sqlPath, sql);
  console.log(`\nSQL update script created: ${sqlPath}`);
}

createUpdateScript().catch(console.error);